import json
from neo4j import GraphDatabase
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Neo4jLoader:
    def __init__(self, uri, username, password):
        """Initialize Neo4j connection"""
        try:
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
            # Verify connection
            self.driver.verify_connectivity()
            logger.info("Connected to Neo4j database")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        """Close the Neo4j connection"""
        if hasattr(self, 'driver'):
            self.driver.close()
            logger.info("Neo4j connection closed")

    def load_general_info(self, file_path):
        """Load general university information from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            logger.info(f"Loaded general info from {file_path}")
            
            # Create University node
            with self.driver.session() as session:
                session.execute_write(self._create_university_node, data)
            
            logger.info("General information loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading general info: {e}")
            return False

    def _create_university_node(self, tx, data):
        """Create University node with general information"""
        query = """
        MERGE (u:University {name: $name})
        SET u.description = $description,
            u.website = $website,
            u.founded = $founded
        RETURN u
        """
        # Extract relevant fields from data
        params = {
            "name": data.get("name", "Unknown University"),
            "description": data.get("description", ""),
            "website": data.get("website", ""),
            "founded": data.get("founded", "")
        }
        result = tx.run(query, **params)
        return result.single()

    def load_faculty_data(self, file_path):
        """Load faculty information from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                faculty_data = json.load(file)
            
            logger.info(f"Loaded faculty data from {file_path}")
            
            with self.driver.session() as session:
                # Create faculty nodes
                for faculty in faculty_data:
                    session.execute_write(self._create_faculty_node, faculty)
                
                # Create department nodes and relationships
                for faculty in faculty_data:
                    if "department" in faculty and faculty["department"]:
                        session.execute_write(
                            self._create_department_relationship, 
                            faculty["name"], 
                            faculty["department"]
                        )
                
                # Create research interest nodes and relationships
                for faculty in faculty_data:
                    if "research_interests" in faculty and faculty["research_interests"]:
                        interests = faculty["research_interests"]
                        if isinstance(interests, str):
                            # Split by commas if it's a string
                            interests = [i.strip() for i in interests.split(',')]
                        
                        for interest in interests:
                            if interest:  # Skip empty interests
                                session.execute_write(
                                    self._create_research_interest_relationship,
                                    faculty["name"],
                                    interest
                                )
            
            logger.info("Faculty data loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading faculty data: {e}")
            return False

    def _create_faculty_node(self, tx, faculty):
        """Create a Faculty node"""
        query = """
        MERGE (f:Faculty {name: $name})
        SET f.title = $title,
            f.email = $email,
            f.phone = $phone,
            f.bio = $bio,
            f.website = $website
        RETURN f
        """
        params = {
            "name": faculty.get("name", "Unknown"),
            "title": faculty.get("title", ""),
            "email": faculty.get("email", ""),
            "phone": faculty.get("phone", ""),
            "bio": faculty.get("bio", ""),
            "website": faculty.get("website", "")
        }
        result = tx.run(query, **params)
        return result.single()

    def _create_department_relationship(self, tx, faculty_name, department_name):
        """Create Department node and relationship to Faculty"""
        query = """
        MATCH (f:Faculty {name: $faculty_name})
        MERGE (d:Department {name: $department_name})
        MERGE (f)-[:BELONGS_TO]->(d)
        MERGE (d)-[:PART_OF]->(u:University)
        RETURN f, d
        """
        result = tx.run(query, faculty_name=faculty_name, department_name=department_name)
        return result.single()

    def _create_research_interest_relationship(self, tx, faculty_name, interest):
        """Create ResearchInterest node and relationship to Faculty"""
        query = """
        MATCH (f:Faculty {name: $faculty_name})
        MERGE (r:ResearchInterest {name: $interest})
        MERGE (f)-[:INTERESTED_IN]->(r)
        RETURN f, r
        """
        result = tx.run(query, faculty_name=faculty_name, interest=interest)
        return result.single()

    def load_course_info(self, file_path):
        """Load course information from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                course_data = json.load(file)
            
            logger.info(f"Loaded course data from {file_path}")
            
            with self.driver.session() as session:
                for course in course_data:
                    session.execute_write(self._create_course_node, course)
                    
                    # Create relationship between course and department
                    if "department" in course and course["department"]:
                        session.execute_write(
                            self._create_course_department_relationship,
                            course["code"],
                            course["department"]
                        )
            
            logger.info("Course data loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading course data: {e}")
            return False

    def _create_course_node(self, tx, course):
        """Create a Course node"""
        query = """
        MERGE (c:Course {code: $code})
        SET c.title = $title,
            c.description = $description,
            c.credits = $credits,
            c.prerequisites = $prerequisites,
            c.website = $website
        RETURN c
        """
        params = {
            "code": course.get("code", "Unknown"),
            "title": course.get("title", ""),
            "description": course.get("description", ""),
            "credits": course.get("credits", 0),
            "prerequisites": course.get("prerequisites", ""),
            "website": course.get("website", "")
        }
        result = tx.run(query, **params)
        return result.single()

    def _create_course_department_relationship(self, tx, course_code, department_name):
        """Create relationship between Course and Department"""
        query = """
        MATCH (c:Course {code: $course_code})
        MERGE (d:Department {name: $department_name})
        MERGE (c)-[:OFFERED_BY]->(d)
        RETURN c, d
        """
        result = tx.run(query, course_code=course_code, department_name=department_name)
        return result.single()

    def load_contact_info(self, file_path):
        """Load contact information from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contact_data = json.load(file)
            
            logger.info(f"Loaded contact data from {file_path}")
            
            with self.driver.session() as session:
                for contact in contact_data:
                    session.execute_write(self._create_contact_node, contact)
                    
                    # Create relationship between contact and department if applicable
                    if "department" in contact and contact["department"]:
                        session.execute_write(
                            self._create_contact_department_relationship,
                            contact["name"],
                            contact["department"]
                        )
            
            logger.info("Contact data loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading contact data: {e}")
            return False

    def _create_contact_node(self, tx, contact):
        """Create a Contact node"""
        query = """
        MERGE (c:Contact {name: $name})
        SET c.role = $role,
            c.email = $email,
            c.phone = $phone,
            c.office = $office
        RETURN c
        """
        params = {
            "name": contact.get("name", "Unknown"),
            "role": contact.get("role", ""),
            "email": contact.get("email", ""),
            "phone": contact.get("phone", ""),
            "office": contact.get("office", "")
        }
        result = tx.run(query, **params)
        return result.single()

    def _create_contact_department_relationship(self, tx, contact_name, department_name):
        """Create relationship between Contact and Department"""
        query = """
        MATCH (c:Contact {name: $contact_name})
        MERGE (d:Department {name: $department_name})
        MERGE (c)-[:WORKS_FOR]->(d)
        RETURN c, d
        """
        result = tx.run(query, contact_name=contact_name, department_name=department_name)
        return result.single()


def main():
    """Main function to load all data into Neo4j"""
    # Neo4j connection parameters
    uri = "neo4j://localhost:7687"  # Update with your Neo4j URI
    username = "neo4j"              # Update with your username
    password = "password"           # Update with your password
    
    # File paths
    data_dir = "data"  # Update with your data directory
    general_file = os.path.join(data_dir, "extracted_general.json")
    faculty_file = os.path.join(data_dir, "extracted_faculty.json")
    course_file = os.path.join(data_dir, "extracted_course_info.json")
    contact_file = os.path.join(data_dir, "extracted_contact_info.json")
    
    # Initialize loader
    try:
        loader = Neo4jLoader(uri, username, password)
        
        # Load data (uncomment when ready to execute)
        # loader.load_general_info(general_file)
        # loader.load_faculty_data(faculty_file)
        # loader.load_course_info(course_file)
        # loader.load_contact_info(contact_file)
        
        # For testing, just print what would be loaded
        print(f"Would load general info from: {general_file}")
        print(f"Would load faculty data from: {faculty_file}")
        print(f"Would load course info from: {course_file}")
        print(f"Would load contact info from: {contact_file}")
        
        # Close connection
        loader.close()
    except Exception as e:
        logger.error(f"Error in main function: {e}")


if __name__ == "__main__":
    main()