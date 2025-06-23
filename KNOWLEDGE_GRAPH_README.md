# Knowledge Graph System for University Data

This system builds a knowledge graph from extracted university data, creating a comprehensive representation of the university's structure, courses, faculty, and contact information.

## Project Structure

```
├── modules/
│   ├── db_connector.py            # Neo4j database connection management
│   ├── graph_builder.py           # Core knowledge graph building functionality
│   ├── knowledge_graph.py         # Main knowledge graph orchestration
│   ├── entity_processors/         # Entity-specific processors
│   │   ├── faculty_processor.py   # Faculty data processing
│   │   ├── course_processor.py    # Course data processing
│   │   ├── contact_processor.py   # Contact information processing
│   │   └── general_processor.py   # General university information processing
├── build_knowledge_graph.py       # Command-line script to build the graph
├── test_knowledge_graph.py        # Test script for the knowledge graph system
└── example.py                     # Example usage script
```

## Data Files

The system processes the following data files:

- `extracted_faculty.json`: Faculty information
- `extracted_course_info.json`: Course information
- `extracted_contact_info.json`: Contact information
- `extracted_general.json`: General university information

## Usage

### Command-line Usage

```bash
# Generate queries without executing them
python build_knowledge_graph.py --output queries.json

# Execute queries and build the graph in Neo4j
python build_knowledge_graph.py --execute

# Run with debug logging
python build_knowledge_graph.py --debug

# Specify custom Neo4j connection details
python build_knowledge_graph.py --uri bolt://localhost:7687 --user neo4j --password password
```

### Programmatic Usage

```python
from modules.knowledge_graph import KnowledgeGraph

# Initialize the knowledge graph
kg = KnowledgeGraph("bolt://localhost:7687", "neo4j", "password")

# Process data from different sources
kg.process_faculty_data("extracted_faculty.json")
kg.process_course_data("extracted_course_info.json")
kg.process_contact_data("extracted_contact_info.json")
kg.process_general_data("extracted_general.json")

# Execute the queries to build the graph
kg.execute_queries()
```

## Knowledge Graph Schema

### Nodes

- **University**: Represents the university
  - Properties: name, description, website

- **Department**: Represents academic departments
  - Properties: name, description, website

- **Faculty**: Represents faculty members
  - Properties: name, title

- **Course**: Represents courses offered
  - Properties: name, title, description, credits

- **Program**: Represents academic programs
  - Properties: name, description, level

- **ResearchInterest**: Represents research areas
  - Properties: name

- **Email**: Represents email addresses
  - Properties: address

- **PhoneNumber**: Represents phone numbers
  - Properties: number

- **Address**: Represents physical addresses
  - Properties: value

### Relationships

- **University - Department**
  - `(University)-[:HAS_DEPARTMENT]->(Department)`
  - `(Department)-[:BELONGS_TO]->(University)`

- **University - Program**
  - `(University)-[:OFFERS_PROGRAM]->(Program)`

- **University - Contact Information**
  - `(University)-[:HAS_CONTACT_EMAIL]->(Email)`
  - `(University)-[:HAS_CONTACT_PHONE]->(PhoneNumber)`
  - `(University)-[:HAS_LOCATION]->(Address)`

- **Department - Faculty**
  - `(Department)-[:HAS_MEMBER]->(Faculty)`
  - `(Faculty)-[:BELONGS_TO]->(Department)`

- **Department - Course**
  - `(Department)-[:OFFERS_COURSE]->(Course)`
  - `(Course)-[:BELONGS_TO]->(Department)`

- **Department - Contact Information**
  - `(Department)-[:HAS_CONTACT_EMAIL]->(Email)`
  - `(Department)-[:HAS_CONTACT_PHONE]->(PhoneNumber)`
  - `(Department)-[:HAS_LOCATION]->(Address)`

- **Faculty - Course**
  - `(Faculty)-[:TEACHES]->(Course)`
  - `(Course)-[:TAUGHT_BY]->(Faculty)`

- **Faculty - Research Interest**
  - `(Faculty)-[:INTERESTED_IN]->(ResearchInterest)`

- **Faculty - Contact Information**
  - `(Faculty)-[:HAS_EMAIL]->(Email)`
  - `(Faculty)-[:HAS_PHONE]->(PhoneNumber)`

- **Course - Course** (Prerequisites)
  - `(Course)-[:IS_PREREQUISITE_FOR]->(Course)`

## Requirements

- Python 3.6+
- Neo4j Database
- Python packages:
  - neo4j
  - logging
  - argparse
  - json

## Installation

1. Install required packages:
   ```bash
   pip install neo4j
   ```

2. Set up a Neo4j database:
   - Download and install Neo4j from https://neo4j.com/download/
   - Create a new database or use an existing one
   - Note the connection URI, username, and password

## Testing

Run the test script to verify the functionality of the knowledge graph system:

```bash
python test_knowledge_graph.py
```

This will test the processing of each data file and display sample queries that would be executed.