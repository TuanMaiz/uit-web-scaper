#!/usr/bin/env python3

"""
Test script for the knowledge graph system.
"""

import json
import logging
import os
import sys

from modules.knowledge_graph import KnowledgeGraph

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_faculty_processing():
    """
    Test faculty data processing.
    """
    kg = KnowledgeGraph("bolt://localhost:7687", "neo4j", "12345678")
    
    try:
        logger.info("Testing faculty data processing...")
        queries = kg.process_faculty_data("extracted_faculty.json")
        logger.info(f"Generated {len(queries)} faculty queries")
        
        # Print the first 5 queries
        for i, query in enumerate(queries[:5]):
            logger.info(f"Query {i+1}: {query['query']}")
            logger.info(f"Params: {query['params']}")
        
        return True
    except Exception as e:
        logger.error(f"Error testing faculty data processing: {e}")
        return False

def test_course_processing():
    """
    Test course data processing.
    """
    kg = KnowledgeGraph("bolt://localhost:7687", "neo4j", "12345678")
    
    try:
        logger.info("Testing course data processing...")
        queries = kg.process_course_data("extracted_course_info.json")
        logger.info(f"Generated {len(queries)} course queries")
        
        # Print the first 5 queries
        for i, query in enumerate(queries[:5]):
            logger.info(f"Query {i+1}: {query['query']}")
            logger.info(f"Params: {query['params']}")
        
        return True
    except Exception as e:
        logger.error(f"Error testing course data processing: {e}")
        return False

def test_contact_processing():
    """
    Test contact data processing.
    """
    kg = KnowledgeGraph("bolt://localhost:7687", "neo4j", "12345678")
    
    try:
        logger.info("Testing contact data processing...")
        queries = kg.process_contact_data("extracted_contact_info.json")
        logger.info(f"Generated {len(queries)} contact queries")
        
        # Print the first 5 queries
        for i, query in enumerate(queries[:5]):
            logger.info(f"Query {i+1}: {query['query']}")
            logger.info(f"Params: {query['params']}")
        
        return True
    except Exception as e:
        logger.error(f"Error testing contact data processing: {e}")
        return False

def test_general_processing():
    """
    Test general information data processing.
    """
    kg = KnowledgeGraph("bolt://localhost:7687", "neo4j", "12345678")
    
    try:
        logger.info("Testing general information data processing...")
        queries = kg.process_general_data("extracted_general.json")
        logger.info(f"Generated {len(queries)} general information queries")
        
        # Print the first 5 queries
        for i, query in enumerate(queries[:5]):
            logger.info(f"Query {i+1}: {query['query']}")
            logger.info(f"Params: {query['params']}")
        
        return True
    except Exception as e:
        logger.error(f"Error testing general information data processing: {e}")
        return False

def main():
    """
    Main function to run all tests.
    """
    tests = [
        ("Faculty Processing", test_faculty_processing),
        ("Course Processing", test_course_processing),
        ("Contact Processing", test_contact_processing),
        ("General Processing", test_general_processing)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n=== Running Test: {test_name} ===")
        success = test_func()
        results.append((test_name, success))
        logger.info(f"=== Test Result: {test_name} - {'SUCCESS' if success else 'FAILURE'} ===\n")
    
    # Print summary
    logger.info("\n=== Test Summary ===")
    for test_name, success in results:
        logger.info(f"{test_name}: {'SUCCESS' if success else 'FAILURE'}")
    
    # Overall result
    if all(success for _, success in results):
        logger.info("\nAll tests passed!")
        return 0
    else:
        logger.error("\nSome tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())