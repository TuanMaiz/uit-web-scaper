#!/usr/bin/env python3

"""
Example script to demonstrate the knowledge graph relationships.
"""

import json
import logging
from modules.knowledge_graph import KnowledgeGraph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Load queries from the generated file
    try:
        with open('queries.json', 'r', encoding='utf-8') as f:
            queries = json.load(f)
        logger.info(f"Loaded {len(queries)} queries from queries.json")
    except FileNotFoundError:
        logger.error("queries.json not found. Run build_knowledge_graph.py first.")
        return
    except json.JSONDecodeError:
        logger.error("Invalid JSON in queries.json")
        return
    
    # Print example queries for each relationship type
    relationship_types = {
        "University-Department": [],
        "University-Contact": [],
        "Department-Faculty": [],
        "Faculty-Course": []
    }
    
    # Categorize queries by relationship type
    for query in queries:
        q = query.get('query', '')
        
        # University-Department relationships
        if 'MATCH (a:University' in q and 'MATCH (b:Department' in q or \
           'MATCH (a:Department' in q and 'MATCH (b:University' in q:
            relationship_types["University-Department"].append(query)
        
        # University-Contact relationships
        elif 'MATCH (a:University' in q and ('MATCH (b:Email' in q or 'MATCH (b:PhoneNumber' in q or 'MATCH (b:Address' in q):
            relationship_types["University-Contact"].append(query)
        
        # Department-Faculty relationships
        elif 'MATCH (a:Department' in q and 'MATCH (b:Faculty' in q or \
             'MATCH (a:Faculty' in q and 'MATCH (b:Department' in q:
            relationship_types["Department-Faculty"].append(query)
        
        # Faculty-Course relationships
        elif 'MATCH (a:Faculty' in q and 'MATCH (b:Course' in q or \
             'MATCH (a:Course' in q and 'MATCH (b:Faculty' in q:
            relationship_types["Faculty-Course"].append(query)
    
    # Print example queries for each category
    for category, category_queries in relationship_types.items():
        logger.info(f"\n=== {category} Relationships ({len(category_queries)} queries) ===\n")
        
        # Print up to 3 example queries for each category
        for i, query in enumerate(category_queries[:3]):
            logger.info(f"Example {i+1}:")
            logger.info(f"Query: {query.get('query')}")
            logger.info(f"Params: {query.get('parameters')}\n")
    
    # Print example Cypher queries for exploring the knowledge graph
    logger.info("\n=== Example Cypher Queries for Neo4j ===\n")
    
    example_queries = [
        {
            "description": "Find all departments in the university",
            "query": "MATCH (u:University)-[:HAS_DEPARTMENT]->(d:Department) RETURN u.name AS University, d.name AS Department"
        },
        {
            "description": "Find all contact information for the university",
            "query": "MATCH (u:University)-[r]->(c) WHERE type(r) IN ['HAS_CONTACT_EMAIL', 'HAS_CONTACT_PHONE', 'HAS_LOCATION'] RETURN u.name AS University, type(r) AS RelationType, c AS ContactInfo"
        },
        {
            "description": "Find all faculty members and their departments",
            "query": "MATCH (f:Faculty)-[:BELONGS_TO]->(d:Department) RETURN f.name AS Faculty, f.title AS Title, d.name AS Department"
        },
        {
            "description": "Find all courses and their instructors",
            "query": "MATCH (c:Course)-[:TAUGHT_BY]->(f:Faculty) RETURN c.name AS Course, f.name AS Instructor"
        },
        {
            "description": "Find all departments and their contact information",
            "query": "MATCH (d:Department)-[r]->(c) WHERE type(r) IN ['HAS_CONTACT_EMAIL', 'HAS_CONTACT_PHONE', 'HAS_LOCATION'] RETURN d.name AS Department, type(r) AS RelationType, c AS ContactInfo"
        },
        {
            "description": "Find faculty members with their contact information",
            "query": "MATCH (f:Faculty)-[r]->(c) WHERE type(r) IN ['HAS_EMAIL', 'HAS_PHONE'] RETURN f.name AS Faculty, type(r) AS RelationType, c AS ContactInfo"
        }
    ]
    
    for i, example in enumerate(example_queries):
        logger.info(f"Example {i+1}: {example['description']}")
        logger.info(f"Query: {example['query']}\n")

if __name__ == "__main__":
    main()