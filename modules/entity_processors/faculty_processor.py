import json
import logging
from typing import Dict, List, Any

class FacultyProcessor:
    """
    Processes faculty data and prepares queries for the knowledge graph.
    """
    
    def __init__(self, graph_builder):
        """
        Initialize the faculty processor with a graph builder.
        
        Args:
            graph_builder: An instance of GraphBuilder
        """
        self.graph_builder = graph_builder
        self.logger = logging.getLogger(__name__)
    
    def load_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load faculty data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            dict: The loaded faculty data
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
    
    def extract_faculty_info(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract faculty information from the data.
        
        Args:
            data (dict): The raw data
            
        Returns:
            list: Extracted faculty information
        """
        faculty_list = []
        
        # Try to extract faculty information from different data structures
        if isinstance(data, list):
            # If data is a list of faculty items
            for item in data:
                if isinstance(item, dict):
                    faculty = {
                        'name': item.get('name', ''),
                        'title': item.get('title', ''),
                        'department': item.get('department', ''),
                        'research_interests': item.get('research_interests', []),
                        'email': item.get('email', ''),
                        'phone': item.get('phone', '')
                    }
                    faculty_list.append(faculty)
        elif isinstance(data, dict):
            # If data is a dictionary with items or deduplicated_items
            items = data.get('items', data.get('deduplicated_items', []))
            
            if isinstance(items, list):
                current_faculty = None
                current_department = None
                
                for item in items:
                    if isinstance(item, dict):
                        text = item.get('text', '')
                        semantic_types = item.get('semantic_types', [])
                        
                        # Check if this is a faculty name
                        if 'faculty_name' in semantic_types or 'person_name' in semantic_types:
                            # Start a new faculty entry
                            current_faculty = {
                                'name': text.strip(),
                                'title': '',
                                'department': current_department,
                                'research_interests': [],
                                'email': '',
                                'phone': ''
                            }
                            faculty_list.append(current_faculty)
                        
                        # Check if this is a department
                        elif 'department' in semantic_types or 'Khoa' in text or 'Bộ môn' in text:
                            current_department = text.strip()
                            # Update all faculty without a department
                            for faculty in faculty_list:
                                if not faculty['department']:
                                    faculty['department'] = current_department
                        
                        # Update current faculty if we have one
                        elif current_faculty:
                            # Check for title
                            if 'title' in semantic_types or any(title in text for title in ['GS', 'PGS', 'TS', 'ThS', 'CN']):
                                current_faculty['title'] = text.strip()
                            
                            # Check for research interests
                            elif 'research_interest' in semantic_types or 'research' in semantic_types:
                                current_faculty['research_interests'].append(text.strip())
                            
                            # Check for email
                            elif 'email' in semantic_types or '@' in text:
                                # Simple email extraction
                                if '@' in text:
                                    words = text.split()
                                    for word in words:
                                        if '@' in word and '.' in word:
                                            current_faculty['email'] = word.strip('.,;:()[]{}"')
                            
                            # Check for phone
                            elif 'phone' in semantic_types or 'tel' in text.lower() or 'phone' in text.lower():
                                # Simple phone number extraction
                                import re
                                phone_pattern = re.compile(r'\+?[\d\s\-\(\)]{7,}')
                                matches = phone_pattern.findall(text)
                                if matches:
                                    current_faculty['phone'] = matches[0].strip()
        
        return faculty_list
    
    def process(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process faculty data and prepare queries for the knowledge graph.
        
        Args:
            file_path (str): Path to the faculty data JSON file
            
        Returns:
            list: The prepared queries
        """
        # Load the data
        data = self.load_data(file_path)
        if not data:
            return self.graph_builder.get_queries()
        
        # Extract faculty information
        faculty_list = self.extract_faculty_info(data)
        
        # Process each faculty member
        for faculty in faculty_list:
            faculty_name = faculty.get('name')
            faculty_title = faculty.get('title')
            faculty_department = faculty.get('department')
            faculty_research_interests = faculty.get('research_interests', [])
            faculty_email = faculty.get('email')
            faculty_phone = faculty.get('phone')
            
            if faculty_name:
                # Create Faculty node
                faculty_props = {"name": faculty_name}
                if faculty_title:
                    faculty_props["title"] = faculty_title
                    
                self.graph_builder.create_node("Faculty", faculty_props)
                
                # Create Department node and relationship if department is specified
                if faculty_department:
                    self.graph_builder.create_node("Department", {"name": faculty_department})
                    
                    # Link Faculty to Department
                    self.graph_builder.create_relationship(
                        "Faculty", "name", faculty_name,
                        "Department", "name", faculty_department,
                        "BELONGS_TO"
                    )
                    
                    # Also create the reverse relationship from Department to Faculty
                    self.graph_builder.create_relationship(
                        "Department", "name", faculty_department,
                        "Faculty", "name", faculty_name,
                        "HAS_MEMBER"
                    )
                
                # Create Research Interest nodes and relationships
                for interest in faculty_research_interests:
                    if interest:
                        self.graph_builder.create_node("ResearchInterest", {"name": interest})
                        
                        # Link Faculty to Research Interest
                        self.graph_builder.create_relationship(
                            "Faculty", "name", faculty_name,
                            "ResearchInterest", "name", interest,
                            "INTERESTED_IN"
                        )
                
                # Create Email node and relationship if email is specified
                if faculty_email:
                    self.graph_builder.create_node("Email", {"address": faculty_email})
                    
                    # Link Faculty to Email
                    self.graph_builder.create_relationship(
                        "Faculty", "name", faculty_name,
                        "Email", "address", faculty_email,
                        "HAS_EMAIL"
                    )
                
                # Create Phone node and relationship if phone is specified
                if faculty_phone:
                    self.graph_builder.create_node("PhoneNumber", {"number": faculty_phone})
                    
                    # Link Faculty to Phone
                    self.graph_builder.create_relationship(
                        "Faculty", "name", faculty_name,
                        "PhoneNumber", "number", faculty_phone,
                        "HAS_PHONE"
                    )
        
        return self.graph_builder.get_queries()