#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
import traceback

from modules.knowledge_graph import KnowledgeGraph

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Build a knowledge graph from extracted data')
    
    # Neo4j connection details
    parser.add_argument('--uri', default='bolt://localhost:7687', help='Neo4j URI')
    parser.add_argument('--username', default='neo4j', help='Neo4j username')
    parser.add_argument('--password', default='12345678', help='Neo4j password')
    
    # Data file paths
    parser.add_argument('--faculty', default='extracted_faculty.json', help='Path to faculty data JSON file')
    parser.add_argument('--course', default='extracted_course_info.json', help='Path to course data JSON file')
    parser.add_argument('--contact', default='extracted_contact_info.json', help='Path to contact data JSON file')
    parser.add_argument('--general', default='extracted_general.json', help='Path to general information data JSON file')
    
    # Execution options
    parser.add_argument('--execute', action='store_true', help='Execute the queries (default is to just generate them)')
    parser.add_argument('--output', help='Path to output file for generated queries (if not executing)')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    return parser.parse_args()

def main():
    """
    Main function to build the knowledge graph.
    """
    args = parse_arguments()
    
    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Initialize the knowledge graph
    kg = KnowledgeGraph(args.uri, args.username, args.password)
    
    try:
        # Process data files
        faculty_queries = []
        course_queries = []
        contact_queries = []
        general_queries = []
        
        if os.path.exists(args.faculty):
            logger.info(f"Processing faculty data from {args.faculty}")
            faculty_queries = kg.process_faculty_data(args.faculty)
            logger.info(f"Generated {len(faculty_queries)} faculty queries")
        else:
            logger.warning(f"Faculty data file not found: {args.faculty}")
        
        if os.path.exists(args.course):
            logger.info(f"Processing course data from {args.course}")
            course_queries = kg.process_course_data(args.course)
            logger.info(f"Generated {len(course_queries)} course queries")
        else:
            logger.warning(f"Course data file not found: {args.course}")
        
        if os.path.exists(args.contact):
            logger.info(f"Processing contact data from {args.contact}")
            contact_queries = kg.process_contact_data(args.contact)
            logger.info(f"Generated {len(contact_queries)} contact queries")
        else:
            logger.warning(f"Contact data file not found: {args.contact}")
        
        if os.path.exists(args.general):
            logger.info(f"Processing general information data from {args.general}")
            general_queries = kg.process_general_data(args.general)
            logger.info(f"Generated {len(general_queries)} general information queries")
        else:
            logger.warning(f"General information data file not found: {args.general}")
        
        # Get all prepared queries
        all_queries = kg.get_all_queries()
        logger.info(f"Total queries prepared: {len(all_queries)}")
        
        if args.execute:
            # Connect to Neo4j and execute queries
            if kg.connect():
                logger.info("Connected to Neo4j database")
                executed = kg.build_knowledge_graph(execute=True)
                logger.info(f"Executed {executed} queries")
            else:
                logger.error("Failed to connect to Neo4j database")
        elif args.output:
            # Save queries to output file
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(all_queries, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(all_queries)} queries to {args.output}")
        else:
            # Print queries to stdout
            print(json.dumps(all_queries, indent=2, ensure_ascii=False))
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        if args.debug:
            logger.error(traceback.format_exc())
    finally:
        # Close the Neo4j connection
        kg.close()

if __name__ == "__main__":
    main()