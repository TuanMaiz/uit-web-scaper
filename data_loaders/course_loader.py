import json
from neo4j import GraphDatabase

def load_course_info(uri, username, password, file_path='extracted_course_info.json'):
    """
    Loads course information from a JSON file into Neo4j.
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

    for item in data:
        department_name = item.get('department_name')
        course_website = item.get('course_website')
        courses = item.get('courses', [])
        urls = item.get('urls', [])

        if department_name:
            # Create Department node
            queries.append({
                "query": "MERGE (d:Department {name: $department_name})",
                "params": {"department_name": department_name}
            })
            if course_website:
                queries.append({
                    "query": "MATCH (d:Department {name: $department_name}) SET d.course_website = $course_website",
                    "params": {"department_name": department_name, "course_website": course_website}
                })

            # Create Course nodes and link to Department
            for course in courses:
                course_name = course.get('name')
                course_code = course.get('code')
                course_description = course.get('description')

                if course_name:
                    queries.append({
                        "query": "MERGE (c:Course {name: $course_name}) SET c.code = $course_code, c.description = $course_description",
                        "params": {"course_name": course_name, "course_code": course_code, "course_description": course_description}
                    })
                    queries.append({
                        "query": "MATCH (d:Department {name: $department_name}) MATCH (c:Course {name: $course_name}) MERGE (d)-[:OFFERS]->(c)",
                        "params": {"department_name": department_name, "course_name": course_name}
                    })
        
        # Handle general URLs that might not be tied to a specific department or course
        for url in urls:
            if url:
                queries.append({
                    "query": "MERGE (l:Link {url: $url})",
                    "params": {"url": url}
                })
                # Link to a general 'CourseInfoSection' node
                queries.append({
                    "query": "MERGE (ci:CourseInfoSection {name: 'Overall Course Information'})",
                    "params": {}
                })
                queries.append({
                    "query": "MATCH (ci:CourseInfoSection {name: 'Overall Course Information'}) MATCH (l:Link {url: $url}) MERGE (ci)-[:REFERENCES]->(l)",
                    "params": {"url": url}
                })
    
    print(f"Prepared queries for course information from '{file_path}'.")
    return queries