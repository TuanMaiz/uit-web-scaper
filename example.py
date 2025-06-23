#!/usr/bin/env python3

"""
Example usage of the Knowledge Graph system.
"""

import logging
from modules.knowledge_graph import KnowledgeGraph

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Main function demonstrating the usage of the Knowledge Graph system.
    """
    # Initialize the knowledge graph with Neo4j connection details
    # Replace with your actual Neo4j credentials
    kg = KnowledgeGraph("bolt://localhost:7687", "neo4j", "12345678")
    
    # Process data from different sources
    logger.info("Processing faculty data...")
    faculty_queries = kg.process_faculty_data("extracted_faculty.json")
    logger.info(f"Generated {len(faculty_queries)} faculty queries")
    
    logger.info("Processing course data...")
    course_queries = kg.process_course_data("extracted_course_info.json")
    logger.info(f"Generated {len(course_queries)} course queries")
    
    logger.info("Processing contact data...")
    contact_queries = kg.process_contact_data("extracted_contact_info.json")
    logger.info(f"Generated {len(contact_queries)} contact queries")
    
    logger.info("Processing general information data...")
    general_queries = kg.process_general_data("extracted_general.json")
    logger.info(f"Generated {len(general_queries)} general information queries")
    
    # Total number of queries
    total_queries = len(faculty_queries) + len(course_queries) + len(contact_queries) + len(general_queries)
    logger.info(f"Total queries prepared: {total_queries}")
    
    # Example of some interesting queries that can be run on the knowledge graph
    logger.info("\nExample Cypher queries to run on the knowledge graph:")
    
    # Find all departments and their faculty members
    logger.info("\n1. Find all departments and their faculty members:")
    logger.info("""
    MATCH (d:Department)-[:HAS_MEMBER]->(f:Faculty)
    RETURN d.name AS Department, collect(f.name) AS Faculty_Members
    """)
    
    # Find all courses taught by a specific faculty member
    logger.info("\n2. Find all courses taught by a specific faculty member:")
    logger.info("""
    MATCH (f:Faculty {name: 'Faculty Name'})-[:TEACHES]->(c:Course)
    RETURN f.name AS Faculty, collect(c.name) AS Courses
    """)
    
    # Find all departments and their courses
    logger.info("\n3. Find all departments and their courses:")
    logger.info("""
    MATCH (d:Department)-[:OFFERS_COURSE]->(c:Course)
    RETURN d.name AS Department, collect(c.name) AS Courses
    """)
    
    # Find the university's contact information
    logger.info("\n4. Find the university's contact information:")
    logger.info("""
    MATCH (u:University {name: 'University of Information Technology'})
    OPTIONAL MATCH (u)-[:HAS_CONTACT_EMAIL]->(e:Email)
    OPTIONAL MATCH (u)-[:HAS_CONTACT_PHONE]->(p:PhoneNumber)
    OPTIONAL MATCH (u)-[:HAS_LOCATION]->(a:Address)
    RETURN u.name AS University, 
           collect(DISTINCT e.address) AS Emails, 
           collect(DISTINCT p.number) AS Phones, 
           collect(DISTINCT a.value) AS Addresses
    """)
    
    # Find courses and their prerequisites
    logger.info("\n5. Find courses and their prerequisites:")
    logger.info("""
    MATCH (c1:Course)-[:IS_PREREQUISITE_FOR]->(c2:Course)
    RETURN c2.name AS Course, collect(c1.name) AS Prerequisites
    """)
    
    # Find faculty members and their research interests
    logger.info("\n6. Find faculty members and their research interests:")
    logger.info("""
    MATCH (f:Faculty)-[:INTERESTED_IN]->(r:ResearchInterest)
    RETURN f.name AS Faculty, collect(r.name) AS Research_Interests
    """)
    
    # Find the complete path from University to Courses
    logger.info("\n7. Find the complete path from University to Courses:")
    logger.info("""
    MATCH path = (u:University)-[:HAS_DEPARTMENT]->(d:Department)-[:OFFERS_COURSE]->(c:Course)
    RETURN u.name AS University, d.name AS Department, c.name AS Course
    """)
    
    # Find faculty members who teach courses in their own department
    logger.info("\n8. Find faculty members who teach courses in their own department:")
    logger.info("""
    MATCH (f:Faculty)-[:BELONGS_TO]->(d:Department)-[:OFFERS_COURSE]->(c:Course),
          (f)-[:TEACHES]->(c)
    RETURN f.name AS Faculty, d.name AS Department, collect(c.name) AS Courses
    """)
    
    # Execute the queries to build the graph (commented out for safety)
    logger.info("\nTo execute these queries and build the graph, uncomment the following line:")
    logger.info("# kg.execute_queries()")

if __name__ == "__main__":
    main()