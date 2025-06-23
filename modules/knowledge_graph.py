import logging
import os
from typing import List, Dict, Any

from modules.db_connector import Neo4jConnector
from modules.graph_builder import GraphBuilder
from modules.entity_processors.faculty_processor import FacultyProcessor
from modules.entity_processors.course_processor import CourseProcessor
from modules.entity_processors.contact_processor import ContactProcessor
from modules.entity_processors.general_processor import GeneralProcessor

class KnowledgeGraph:
    """
    Main class for creating and managing the knowledge graph.
    """
    
    def __init__(self, uri, username, password):
        """
        Initialize the knowledge graph with Neo4j connection details.
        
        Args:
            uri (str): The URI for the Neo4j database
            username (str): The username for authentication
            password (str): The password for authentication
        """
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.db_connector = Neo4jConnector(uri, username, password)
        self.graph_builder = GraphBuilder(self.db_connector)
        
        # Initialize processors
        self.faculty_processor = FacultyProcessor(self.graph_builder)
        self.course_processor = CourseProcessor(self.graph_builder)
        self.contact_processor = ContactProcessor(self.graph_builder)
        self.general_processor = GeneralProcessor(self.graph_builder)
        
        # Track all queries
        self.all_queries = []
    
    def connect(self):
        """
        Connect to the Neo4j database.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        return self.db_connector.connect()
    
    def close(self):
        """
        Close the connection to the Neo4j database.
        """
        self.db_connector.close()
    
    def process_faculty_data(self, file_path):
        """
        Process faculty data and add queries to the queue.
        
        Args:
            file_path (str): Path to the faculty data JSON file
            
        Returns:
            list: The prepared queries
        """
        try:
            self.logger.info(f"Processing faculty data from {file_path}")
            queries = self.faculty_processor.process(file_path)
            self.all_queries.extend(queries)
            return queries
        except Exception as e:
            self.logger.error(f"Error processing faculty data: {e}")
            return []
    
    def process_course_data(self, file_path):
        """
        Process course data and add queries to the queue.
        
        Args:
            file_path (str): Path to the course data JSON file
            
        Returns:
            list: The prepared queries
        """
        try:
            self.logger.info(f"Processing course data from {file_path}")
            queries = self.course_processor.process(file_path)
            self.all_queries.extend(queries)
            return queries
        except Exception as e:
            self.logger.error(f"Error processing course data: {e}")
            return []
    
    def process_contact_data(self, file_path):
        """
        Process contact data and add queries to the queue.
        
        Args:
            file_path (str): Path to the contact data JSON file
            
        Returns:
            list: The prepared queries
        """
        try:
            self.logger.info(f"Processing contact data from {file_path}")
            queries = self.contact_processor.process(file_path)
            self.all_queries.extend(queries)
            return queries
        except Exception as e:
            self.logger.error(f"Error processing contact data: {e}")
            return []
    
    def process_general_data(self, file_path):
        """
        Process general information data and add queries to the queue.
        
        Args:
            file_path (str): Path to the general information data JSON file
            
        Returns:
            list: The prepared queries
        """
        try:
            self.logger.info(f"Processing general information data from {file_path}")
            queries = self.general_processor.process(file_path)
            self.all_queries.extend(queries)
            return queries
        except Exception as e:
            self.logger.error(f"Error processing general information data: {e}")
            return []
    
    def build_knowledge_graph(self, execute=False):
        """
        Build the knowledge graph by executing all queued queries.
        
        Args:
            execute (bool): Whether to execute the queries or just return them
            
        Returns:
            list or int: The list of queries if execute is False, otherwise the number of executed queries
        """
        if not self.all_queries:
            self.logger.warning("No queries to execute")
            return 0 if execute else []
        
        self.logger.info(f"Building knowledge graph with {len(self.all_queries)} queries")
        
        if execute:
            if not self.db_connector.driver:
                connected = self.connect()
                if not connected:
                    self.logger.error("Failed to connect to Neo4j database")
                    return 0
            
            result = self.db_connector.execute_queries(self.all_queries)
            self.all_queries = []  # Clear the queue after execution
            return result
        else:
            return self.all_queries
    
    def get_all_queries(self):
        """
        Get all queued queries without executing them.
        
        Returns:
            list: The list of all queued queries
        """
        return self.all_queries
    
    def clear_all_queries(self):
        """
        Clear all queued queries without executing them.
        """
        self.all_queries = []
        self.graph_builder.clear_queries()