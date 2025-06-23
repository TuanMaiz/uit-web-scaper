import logging
from typing import List, Dict, Any

class GraphBuilder:
    """
    Core functionality for building a knowledge graph in Neo4j.
    """
    
    def __init__(self, db_connector):
        """
        Initialize the graph builder with a database connector.
        
        Args:
            db_connector: An instance of Neo4jConnector
        """
        self.db_connector = db_connector
        self.logger = logging.getLogger(__name__)
        self.queries = []
    
    def add_query(self, query: str, params: Dict[str, Any] = None):
        """
        Add a query to the queue for execution.
        
        Args:
            query (str): The Cypher query to execute
            params (dict, optional): Parameters for the query
        """
        self.queries.append({
            "query": query,
            "params": params or {}
        })
    
    def create_node(self, label: str, properties: Dict[str, Any]):
        """
        Create a node with the given label and properties.
        
        Args:
            label (str): The label for the node
            properties (dict): The properties for the node
            
        Returns:
            self: For method chaining
        """
        # Identify a primary key for the MERGE operation
        primary_key = next(iter(properties.keys()))
        
        # Build the query
        query = f"MERGE (n:{label} {{{primary_key}: ${primary_key}}}) "
        
        # Add SET clauses for other properties
        set_clauses = []
        for key in properties.keys():
            if key != primary_key:
                set_clauses.append(f"n.{key} = ${key}")
        
        if set_clauses:
            query += "SET " + ", ".join(set_clauses)
        
        self.add_query(query, properties)
        return self
    
    def create_relationship(self, from_label: str, from_property: str, from_value: Any,
                           to_label: str, to_property: str, to_value: Any,
                           relationship_type: str, relationship_properties: Dict[str, Any] = None):
        """
        Create a relationship between two nodes.
        
        Args:
            from_label (str): The label of the source node
            from_property (str): The property name to identify the source node
            from_value (Any): The value of the property to identify the source node
            to_label (str): The label of the target node
            to_property (str): The property name to identify the target node
            to_value (Any): The value of the property to identify the target node
            relationship_type (str): The type of relationship
            relationship_properties (dict, optional): Properties for the relationship
            
        Returns:
            self: For method chaining
        """
        query = f"MATCH (a:{from_label} {{{from_property}: $from_value}}) "
        query += f"MATCH (b:{to_label} {{{to_property}: $to_value}}) "
        
        if relationship_properties:
            props_str = ", ".join([f"{k}: ${k}" for k in relationship_properties.keys()])
            query += f"MERGE (a)-[r:{relationship_type} {{{props_str}}}]->(b)"
            params = {"from_value": from_value, "to_value": to_value, **relationship_properties}
        else:
            query += f"MERGE (a)-[:{relationship_type}]->(b)"
            params = {"from_value": from_value, "to_value": to_value}
        
        self.add_query(query, params)
        return self
    
    def execute(self):
        """
        Execute all queued queries.
        
        Returns:
            int: Number of successfully executed queries
        """
        if not self.queries:
            self.logger.warning("No queries to execute")
            return 0
            
        result = self.db_connector.execute_queries(self.queries)
        self.queries = []  # Clear the queue after execution
        return result
    
    def get_queries(self):
        """
        Get all queued queries without executing them.
        
        Returns:
            list: The list of queued queries
        """
        return self.queries
    
    def clear_queries(self):
        """
        Clear all queued queries without executing them.
        """
        self.queries = []