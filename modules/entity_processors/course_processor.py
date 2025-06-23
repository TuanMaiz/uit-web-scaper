import json
import logging
from typing import Dict, List, Any

class CourseProcessor:
    """
    Processes course data and prepares queries for the knowledge graph.
    """
    
    def __init__(self, graph_builder):
        """
        Initialize the course processor with a graph builder.
        
        Args:
            graph_builder: An instance of GraphBuilder
        """
        self.graph_builder = graph_builder
        self.logger = logging.getLogger(__name__)
    
    def load_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load course data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            dict: The loaded course data
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
    
    def extract_course_info(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract course information from the data.
        
        Args:
            data (dict): The raw data
            
        Returns:
            list: Extracted course information
        """
        course_list = []
        
        # Try to extract course information from different data structures
        if isinstance(data, list):
            # If data is a list of course items
            for item in data:
                if isinstance(item, dict):
                    course = {
                        'code': item.get('code', ''),
                        'name': item.get('name', ''),
                        'description': item.get('description', ''),
                        'credits': item.get('credits', ''),
                        'department': item.get('department', ''),
                        'instructors': item.get('instructors', []),
                        'prerequisites': item.get('prerequisites', [])
                    }
                    course_list.append(course)
        elif isinstance(data, dict):
            # If data is a dictionary with items or deduplicated_items
            items = data.get('items', data.get('deduplicated_items', []))
            
            if isinstance(items, list):
                current_course = None
                current_department = None
                
                for item in items:
                    if isinstance(item, dict):
                        text = item.get('text', '')
                        semantic_types = item.get('semantic_types', [])
                        
                        # Check if this is a course code or name
                        if 'course_code' in semantic_types or 'course_name' in semantic_types:
                            # Start a new course entry
                            course_code = ''
                            course_name = text.strip()
                            
                            # Try to extract course code if it's in the text
                            import re
                            code_match = re.search(r'[A-Z]{2,}\d{3,}', text)
                            if code_match:
                                course_code = code_match.group(0)
                                # Remove the code from the name
                                course_name = re.sub(r'[A-Z]{2,}\d{3,}', '', course_name).strip()
                            
                            current_course = {
                                'code': course_code,
                                'name': course_name,
                                'description': '',
                                'credits': '',
                                'department': current_department,
                                'instructors': [],
                                'prerequisites': []
                            }
                            course_list.append(current_course)
                        
                        # Check if this is a department
                        elif 'department' in semantic_types or 'Khoa' in text or 'Bu1ed9 mu00f4n' in text:
                            current_department = text.strip()
                            # Update all courses without a department
                            for course in course_list:
                                if not course['department']:
                                    course['department'] = current_department
                        
                        # Update current course if we have one
                        elif current_course:
                            # Check for description
                            if 'course_description' in semantic_types or 'description' in semantic_types:
                                current_course['description'] = text.strip()
                            
                            # Check for credits
                            elif 'credits' in semantic_types or 'credit' in text.lower() or 'tu00edn chu1ec9' in text.lower():
                                # Extract credit value
                                import re
                                credit_match = re.search(r'\d+', text)
                                if credit_match:
                                    current_course['credits'] = credit_match.group(0)
                            
                            # Check for instructors
                            elif 'instructor' in semantic_types or 'giu1ea3ng viu00ean' in text.lower() or 'lecturer' in text.lower():
                                # Extract instructor names
                                instructor_text = text.replace('Giu1ea3ng viu00ean:', '').replace('Instructor:', '').strip()
                                instructors = [name.strip() for name in instructor_text.split(',')]
                                current_course['instructors'].extend(instructors)
                            
                            # Check for prerequisites
                            elif 'prerequisite' in semantic_types or 'hu1ecdc phu1ea7n tiu00ean quyu1ebft' in text.lower():
                                # Extract prerequisite course codes
                                import re
                                prereq_codes = re.findall(r'[A-Z]{2,}\d{3,}', text)
                                current_course['prerequisites'].extend(prereq_codes)
        
        return course_list
    
    def process(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process course data and prepare queries for the knowledge graph.
        
        Args:
            file_path (str): Path to the course data JSON file
            
        Returns:
            list: The prepared queries
        """
        # Load the data
        data = self.load_data(file_path)
        if not data:
            return self.graph_builder.get_queries()
        
        # Extract course information
        course_list = self.extract_course_info(data)
        
        # Process each course
        for course in course_list:
            course_code = course.get('code')
            course_name = course.get('name')
            course_description = course.get('description')
            course_credits = course.get('credits')
            course_department = course.get('department')
            course_instructors = course.get('instructors', [])
            course_prerequisites = course.get('prerequisites', [])
            
            # Use course name as identifier if code is not available
            course_identifier = course_code if course_code else course_name
            
            if course_identifier:
                # Create Course node
                course_props = {"name": course_identifier}
                if course_name and course_code:  # If we have both code and name
                    course_props["title"] = course_name
                if course_description:
                    course_props["description"] = course_description
                if course_credits:
                    course_props["credits"] = course_credits
                    
                self.graph_builder.create_node("Course", course_props)
                
                # Create Department node and relationship if department is specified
                if course_department:
                    self.graph_builder.create_node("Department", {"name": course_department})
                    
                    # Link Course to Department
                    self.graph_builder.create_relationship(
                        "Course", "name", course_identifier,
                        "Department", "name", course_department,
                        "BELONGS_TO"
                    )
                    
                    # Also create the reverse relationship from Department to Course
                    self.graph_builder.create_relationship(
                        "Department", "name", course_department,
                        "Course", "name", course_identifier,
                        "OFFERS_COURSE"
                    )
                
                # Create Faculty nodes and relationships for instructors
                for instructor in course_instructors:
                    if instructor:
                        self.graph_builder.create_node("Faculty", {"name": instructor})
                        
                        # Link Faculty to Course (teaches relationship)
                        self.graph_builder.create_relationship(
                            "Faculty", "name", instructor,
                            "Course", "name", course_identifier,
                            "TEACHES"
                        )
                        
                        # Link Course to Faculty (taught by relationship)
                        self.graph_builder.create_relationship(
                            "Course", "name", course_identifier,
                            "Faculty", "name", instructor,
                            "TAUGHT_BY"
                        )
                
                # Create prerequisite relationships
                for prerequisite in course_prerequisites:
                    if prerequisite:
                        self.graph_builder.create_node("Course", {"name": prerequisite})
                        
                        # Link Course to Prerequisite Course
                        self.graph_builder.create_relationship(
                            "Course", "name", prerequisite,
                            "Course", "name", course_identifier,
                            "IS_PREREQUISITE_FOR"
                        )
        
        return self.graph_builder.get_queries()