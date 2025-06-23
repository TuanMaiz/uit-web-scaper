import json
import logging
from typing import Dict, List, Any

class ContactProcessor:
    """
    Processes contact data and prepares queries for the knowledge graph.
    """
    
    def __init__(self, graph_builder):
        """
        Initialize the contact processor with a graph builder.
        
        Args:
            graph_builder: An instance of GraphBuilder
        """
        self.graph_builder = graph_builder
        self.logger = logging.getLogger(__name__)
    
    def load_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load contact data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            dict: The loaded contact data
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
    
    def process(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process contact data and prepare queries for the knowledge graph.
        
        Args:
            file_path (str): Path to the contact data JSON file
            
        Returns:
            list: The prepared queries
        """
        # Load the data
        data = self.load_data(file_path)
        if not data:
            return self.graph_builder.get_queries()
        
        try:
            # Create a default university node
            university_name = "University of Information Technology"
            self.graph_builder.create_node("University", {"name": university_name})
            
            # Process the contact data
            if isinstance(data, dict) and 'departments' in data:
                # Extract departments and their contact information
                departments = data.get('departments', [])
                
                if isinstance(departments, list):
                    for dept_info in departments:
                        if isinstance(dept_info, dict):
                            dept_name = dept_info.get('name', 'general')
                            emails = dept_info.get('emails', [])
                            phones = dept_info.get('phones', [])
                            addresses = dept_info.get('addresses', [])
                            
                            # Create Department node
                            self.graph_builder.create_node("Department", {"name": dept_name})
                            
                            # Link Department to University
                            self.graph_builder.create_relationship(
                                "Department", "name", dept_name,
                                "University", "name", university_name,
                                "BELONGS_TO"
                            )
                            
                            # Also create the reverse relationship from University to Department
                            self.graph_builder.create_relationship(
                                "University", "name", university_name,
                                "Department", "name", dept_name,
                                "HAS_DEPARTMENT"
                            )
                            
                            # Process emails
                            for email in emails:
                                if email:
                                    self.graph_builder.create_node("Email", {"address": email})
                                    
                                    # Link Department to Email
                                    self.graph_builder.create_relationship(
                                        "Department", "name", dept_name,
                                        "Email", "address", email,
                                        "HAS_CONTACT_EMAIL"
                                    )
                                    
                                    # If this is a general department, also link to University
                                    if dept_name.lower() == "general":
                                        self.graph_builder.create_relationship(
                                            "University", "name", university_name,
                                            "Email", "address", email,
                                            "HAS_CONTACT_EMAIL"
                                        )
                            
                            # Process phone numbers
                            for phone in phones:
                                if phone:
                                    self.graph_builder.create_node("PhoneNumber", {"number": phone})
                                    
                                    # Link Department to Phone
                                    self.graph_builder.create_relationship(
                                        "Department", "name", dept_name,
                                        "PhoneNumber", "number", phone,
                                        "HAS_CONTACT_PHONE"
                                    )
                                    
                                    # If this is a general department, also link to University
                                    if dept_name.lower() == "general":
                                        self.graph_builder.create_relationship(
                                            "University", "name", university_name,
                                            "PhoneNumber", "number", phone,
                                            "HAS_CONTACT_PHONE"
                                        )
                            
                            # Process addresses
                            for address in addresses:
                                if address:
                                    self.graph_builder.create_node("Address", {"value": address})
                                    
                                    # Link Department to Address
                                    self.graph_builder.create_relationship(
                                        "Department", "name", dept_name,
                                        "Address", "value", address,
                                        "HAS_LOCATION"
                                    )
                                    
                                    # If this is a general department, also link to University
                                    if dept_name.lower() == "general":
                                        self.graph_builder.create_relationship(
                                            "University", "name", university_name,
                                            "Address", "value", address,
                                            "HAS_LOCATION"
                                        )
                                        
                            # Try to extract faculty information from department name
                            if len(dept_name) > 100:  # This is likely a faculty description
                                import re
                                # Extract faculty names and emails
                                faculty_pattern = re.compile(r'([A-Z][a-z]+\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)?)')
                                faculty_matches = faculty_pattern.findall(dept_name)
                                
                                email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
                                email_matches = email_pattern.findall(dept_name)
                                
                                # Create faculty nodes and link them to departments
                                for faculty_name in faculty_matches:
                                    if len(faculty_name.split()) >= 2:  # At least first and last name
                                        self.graph_builder.create_node("Faculty", {"name": faculty_name})
                                        
                                        # Link Faculty to Department
                                        self.graph_builder.create_relationship(
                                            "Faculty", "name", faculty_name,
                                            "Department", "name", dept_name,
                                            "BELONGS_TO"
                                        )
                                        
                                        # Link Department to Faculty
                                        self.graph_builder.create_relationship(
                                            "Department", "name", dept_name,
                                            "Faculty", "name", faculty_name,
                                            "HAS_MEMBER"
                                        )
                                
                                # Link emails to faculty if possible
                                for i, email in enumerate(email_matches):
                                    if i < len(faculty_matches):
                                        faculty_name = faculty_matches[i]
                                        self.graph_builder.create_node("Email", {"address": email})
                                        
                                        # Link Faculty to Email
                                        self.graph_builder.create_relationship(
                                            "Faculty", "name", faculty_name,
                                            "Email", "address", email,
                                            "HAS_EMAIL"
                                        )
        except Exception as e:
            self.logger.error(f"Error processing contact data: {e}")
        
        return self.graph_builder.get_queries()