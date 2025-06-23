def load_contact_info(driver, file_path="extracted_contact_info.json"):
    """
    Loads contact information from a JSON file into the Neo4j graph database.
    Creates Department nodes and links them to Email nodes.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        departments_data = data.get('departments')

        if not departments_data:
            print(f"No 'departments' found in {file_path}. Skipping contact info loading.")
            return

        with driver.session() as session:
            for department_info in departments_data:
                department_name = department_info.get('name')
                emails = department_info.get('emails', [])

                if department_name:
                    # Create Department node
                    session.run(
                        "MERGE (d:Department {name: $name})",
                        name=department_name
                    )

                    # Create Email nodes and link to Department
                    for email in emails:
                        session.run(
                            "MERGE (e:Email {address: $email}) "
                            "MERGE (d:Department {name: $department_name})-[:HAS_CONTACT_EMAIL]->(e)",
                            email=email, department_name=department_name
                        )
            print(f"Successfully loaded contact information from {file_path}")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
    except Exception as e:
        print(f"An error occurred during the contact info loading process: {e}")