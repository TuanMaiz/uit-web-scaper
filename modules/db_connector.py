from neo4j import GraphDatabase
import logging

class Neo4jConnector:
    """
    Manages connections to the Neo4j database.
    """
    
    def __init__(self, uri, username, password):
        """
        Initialize the Neo4j connector with connection details.
        
        Args:
            uri (str): The URI for the Neo4j database
            username (str): The username for authentication
            password (str): The password for authentication
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = None
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """
        Establish a connection to the Neo4j database.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self.driver.verify_connectivity()
            self.logger.info("Successfully connected to Neo4j database")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Neo4j database: {e}")
            return False
    
    def close(self):
        """
        Close the connection to the Neo4j database.
        """
        if self.driver:
            self.driver.close()
            self.logger.info("Neo4j connection closed")
    
    def execute_query(self, query, params=None):
        """
        Execute a single Cypher query.
        
        Args:
            query (str): The Cypher query to execute
            params (dict, optional): Parameters for the query
            
        Returns:
            list: The result of the query execution
        """
        if not self.driver:
            self.logger.error("No active connection to Neo4j database")
            return None
            
        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                return list(result)
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            return None
    
    def execute_queries(self, queries):
        """
        Execute a list of Cypher queries in a single Neo4j session.
        
        Args:
            queries (list): List of dictionaries containing 'query' and 'params' keys
            
        Returns:
            int: Number of successfully executed queries
        """
        if not self.driver:
            self.logger.error("No active connection to Neo4j database")
            return 0
            
        successful_queries = 0
        with self.driver.session() as session:
            for q in queries:
                try:
                    session.run(q["query"], q["params"])
                    successful_queries += 1
                except Exception as e:
                    self.logger.error(f"Error executing query: {q['query']} with params {q['params']}. Error: {e}")
        
        self.logger.info(f"Executed {successful_queries} out of {len(queries)} queries")
        return successful_queries