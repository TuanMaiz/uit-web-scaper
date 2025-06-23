#!/usr/bin/env python3

"""
Script to analyze the generated queries.
"""

import json
import re

def main():
    # Load the queries
    with open('queries.json', 'r', encoding='utf-8') as f:
        queries = json.load(f)
    
    print(f"Total queries: {len(queries)}")
    
    # Extract relationship types
    relationship_types = set()
    for query in queries:
        q = query.get('query', '')
        if 'MATCH' in q and 'MERGE (a)-[' in q:
            # Extract relationship type
            match = re.search(r'MERGE \(a\)-\[:(\w+)\]->\(b\)', q)
            if match:
                relationship_types.add(match.group(1))
    
    print("\nUnique relationship types:")
    for rt in sorted(relationship_types):
        print(f"- {rt}")
    
    # Count node types
    node_types = set()
    for query in queries:
        q = query.get('query', '')
        if q.startswith('MERGE (n:'):
            # Extract node type
            match = re.search(r'MERGE \(n:(\w+)', q)
            if match:
                node_types.add(match.group(1))
    
    print("\nUnique node types:")
    for nt in sorted(node_types):
        print(f"- {nt}")
    
    # Count specific relationships
    relationship_counts = {}
    for query in queries:
        q = query.get('query', '')
        if 'MATCH' in q and 'MERGE (a)-[' in q:
            # Extract from and to node types
            from_match = re.search(r'MATCH \(a:(\w+)', q)
            to_match = re.search(r'MATCH \(b:(\w+)', q)
            rel_match = re.search(r'MERGE \(a\)-\[:(\w+)\]->\(b\)', q)
            
            if from_match and to_match and rel_match:
                from_type = from_match.group(1)
                to_type = to_match.group(1)
                rel_type = rel_match.group(1)
                
                key = f"({from_type})-[:{rel_type}]->({to_type})"
                relationship_counts[key] = relationship_counts.get(key, 0) + 1
    
    print("\nRelationship patterns:")
    for pattern, count in sorted(relationship_counts.items()):
        print(f"- {pattern}: {count} instances")

if __name__ == "__main__":
    main()