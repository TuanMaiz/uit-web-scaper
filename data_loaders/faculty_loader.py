import json
from neo4j import GraphDatabase

def load_faculty_info(uri, username, password, file_path='extracted_faculty.json'):
    """
    Loads faculty information from a JSON file into Neo4j.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return []

    queries = []

    for faculty_member in data:
        name = faculty_member.get('name')
        title = faculty_member.get('title')
        department = faculty_member.get('department')
        email = faculty_member.get('email')
        research_interests = faculty_member.get('research_interests', [])

        if name:
            # Create Faculty node
            queries.append({
                "query": "MERGE (f:Faculty {name: $name}) SET f.title = $title, f.email = $email",
                "params": {"name": name, "title": title, "email": email}
            })

            # Create Department node and relationship
            if department:
                queries.append({
                    "query": "MERGE (d:Department {name: $department})",
                    "params": {"department": department}
                })
                queries.append({
                    "query": "MATCH (f:Faculty {name: $name}) MATCH (d:Department {name: $department}) MERGE (f)-[:BELONGS_TO]->(d)",
                    "params": {"name": name, "department": department}
                })

            # Create ResearchInterest nodes and relationships
            for interest in research_interests:
                if interest:
                    queries.append({
                        "query": "MERGE (ri:ResearchInterest {name: $interest})",
                        "params": {"interest": interest}
                    })
                    queries.append({
                        "query": "MATCH (f:Faculty {name: $name}) MATCH (ri:ResearchInterest {name: $interest}) MERGE (f)-[:HAS_INTEREST_IN]->(ri)",
                        "params": {"name": name, "interest": interest}
                    })
    
    print(f"Prepared queries for faculty information from '{file_path}'.")
    return queries