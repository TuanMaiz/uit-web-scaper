import json
import logging
from typing import Dict, List, Any

class GeneralProcessor:
    """
    Processes general information data and prepares queries for the knowledge graph.
    """
    
    def __init__(self, graph_builder):
        """
        Initialize the general information processor with a graph builder.
        
        Args:
            graph_builder: An instance of GraphBuilder
        """
        self.graph_builder = graph_builder
        self.logger = logging.getLogger(__name__)
    
    def load_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load general information data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            dict: The loaded general information data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in file: {file_path}")
            return {}
        except Exception as e:
            self.logger.error(f"Error loading data from {file_path}: {e}")
            return {}
    
    def extract_university_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract university information from the data.
        
        Args:
            data (dict): The raw data
            
        Returns:
            dict: Extracted university information
        """
        university_info = {
            'name': 'University of Information Technology',  # Default name
            'description': None,
            'website': 'https://www.uit.edu.vn',  # Default website
            'contact_info': {
                'emails': [],
                'phone_numbers': [],
                'addresses': []
            },
            'departments': [],
            'programs': [],
            'facilities': [],
            'events': []
        }
        
        # Try to extract university information from different data structures
        if isinstance(data, dict):
            # If data is a dictionary with items or deduplicated_items
            items = data.get('items', data.get('deduplicated_items', []))
            
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        text = item.get('text', '')
                        semantic_types = item.get('semantic_types', [])
                        
                        # Extract university name and description
                        if 'university_name' in semantic_types or 'university' in semantic_types:
                            university_info['name'] = text.strip()
                        elif 'university_description' in semantic_types or 'description' in semantic_types:
                            university_info['description'] = text.strip()
                        
                        # Extract contact information
                        if 'email' in semantic_types or '@' in text:
                            # Simple email extraction
                            if '@' in text:
                                words = text.split()
                                for word in words:
                                    if '@' in word and '.' in word:
                                        email = word.strip('.,;:()[]{}"')
                                        if email not in university_info['contact_info']['emails']:
                                            university_info['contact_info']['emails'].append(email)
                        
                        if 'phone' in semantic_types or 'tel' in text.lower() or 'phone' in text.lower():
                            # Simple phone number extraction
                            import re
                            phone_pattern = re.compile(r'\+?[\d\s\-\(\)]{7,}')
                            matches = phone_pattern.findall(text)
                            for match in matches:
                                phone = match.strip()
                                if phone and phone not in university_info['contact_info']['phone_numbers']:
                                    university_info['contact_info']['phone_numbers'].append(phone)
                        
                        if 'address' in semantic_types or 'location' in semantic_types:
                            # Add as address if it seems like one
                            if len(text.split()) > 3 and not text.startswith('http'):
                                if text not in university_info['contact_info']['addresses']:
                                    university_info['contact_info']['addresses'].append(text)
                        
                        # Extract department information
                        if 'department' in semantic_types or 'Khoa' in text or 'B\u1ed9 m\u00f4n' in text:
                            department = {
                                'name': text.strip(),
                                'description': None,
                                'website': None
                            }
                            
                            # Extract website if available
                            if item.get('link_urls'):
                                department['website'] = item.get('link_urls')[0]
                                
                            university_info['departments'].append(department)
                        
                        # Extract program information
                        if 'program' in semantic_types or 'Ch\u01b0\u01a1ng tr\u00ecnh' in text:
                            program = {
                                'name': text.strip(),
                                'description': None,
                                'level': None
                            }
                            
                            # Try to determine program level
                            if '\u0111\u1ea1i h\u1ecdc' in text.lower():
                                program['level'] = 'undergraduate'
                            elif 'th\u1ea1c s\u0129' in text.lower() or 'cao h\u1ecdc' in text.lower():
                                program['level'] = 'graduate'
                            elif 'ti\u1ebfn s\u0129' in text.lower():
                                program['level'] = 'doctorate'
                                
                            university_info['programs'].append(program)
        
        return university_info
    
    def process(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process general information data and prepare queries for the knowledge graph.
        
        Args:
            file_path (str): Path to the general information data JSON file
            
        Returns:
            list: The prepared queries
        """
        # Load the data
        data = self.load_data(file_path)
        if not data:
            # Create a default university node even if no data is available
            self.graph_builder.create_node("University", {"name": "University of Information Technology"})
            return self.graph_builder.get_queries()
        
        # Extract university information
        university_info = self.extract_university_info(data)
        
        # Create University node
        university_props = {"name": university_info['name']}
        if university_info['description']:
            university_props["description"] = university_info['description']
        if university_info['website']:
            university_props["website"] = university_info['website']
            
        self.graph_builder.create_node("University", university_props)
        
        # Process university contact information
        for email in university_info['contact_info']['emails']:
            if email:
                self.graph_builder.create_node("Email", {"address": email})
                self.graph_builder.create_relationship(
                    "University", "name", university_info['name'],
                    "Email", "address", email,
                    "HAS_CONTACT_EMAIL"
                )
        
        for phone in university_info['contact_info']['phone_numbers']:
            if phone:
                self.graph_builder.create_node("PhoneNumber", {"number": phone})
                self.graph_builder.create_relationship(
                    "University", "name", university_info['name'],
                    "PhoneNumber", "number", phone,
                    "HAS_CONTACT_PHONE"
                )
        
        for address in university_info['contact_info']['addresses']:
            if address:
                self.graph_builder.create_node("Address", {"value": address})
                self.graph_builder.create_relationship(
                    "University", "name", university_info['name'],
                    "Address", "value", address,
                    "HAS_LOCATION"
                )
        
        # Process departments
        for dept in university_info['departments']:
            dept_name = dept.get('name')
            dept_description = dept.get('description')
            dept_website = dept.get('website')
            
            if dept_name:
                # Create Department node
                dept_props = {"name": dept_name}
                if dept_description:
                    dept_props["description"] = dept_description
                if dept_website:
                    dept_props["website"] = dept_website
                    
                self.graph_builder.create_node("Department", dept_props)
                
                # Link Department to University
                self.graph_builder.create_relationship(
                    "University", "name", university_info['name'],
                    "Department", "name", dept_name,
                    "HAS_DEPARTMENT"
                )
        
        # Process programs
        for program in university_info['programs']:
            program_name = program.get('name')
            program_description = program.get('description')
            program_level = program.get('level')
            
            if program_name:
                # Create Program node
                program_props = {"name": program_name}
                if program_description:
                    program_props["description"] = program_description
                if program_level:
                    program_props["level"] = program_level
                    
                self.graph_builder.create_node("Program", program_props)
                
                # Link Program to University
                self.graph_builder.create_relationship(
                    "University", "name", university_info['name'],
                    "Program", "name", program_name,
                    "OFFERS_PROGRAM"
                )
        
        return self.graph_builder.get_queries()