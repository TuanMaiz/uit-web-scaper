from typing import Optional, List, Dict
from typing_extensions import TypedDict
import json

# Read from JSON file and parse to Python
def read_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in {filename}")
        return None


class ElementData(TypedDict):
    text: str
    type: str
    source_url: str
    page_number: Optional[int]
    text_as_html: Optional[str]
    html_attributes: Dict[str, str]
    emphasized_text: Optional[str]
    emphasis_tags: Optional[str]
    parent_id: Optional[str]
    category_depth: Optional[int]
    link_urls: Optional[List[str]]
    link_texts: Optional[List[str]]
    regex_patterns: Dict[str, List[str]]
    semantic_types: List[str]
    word_count: int
    char_count: int

def extract_course_info(items: List[ElementData]):
    """
    Process raw JSON items to:
    1. Deduplicate
    2. Group by semantic types
    3. Map parent-child relationships
    """

    # Step 1: Deduplicate
    unique = {}
    for item in items:
        key = (item['text'], tuple(item['link_urls']) if item['link_urls'] else ())
        if key not in unique:
            unique[key] = item

    deduplicated_items = list(unique.values())

    # Step 2: Group by semantic types
    grouped = {}
    for item in deduplicated_items:
        for s_type in item.get('semantic_types', []):
            if s_type not in grouped:
                grouped[s_type] = []
            grouped[s_type].append(item)

    # Step 3: Build parent-child map
    entity_map = {}
    children_map = {}

    for item in deduplicated_items:
        entity_id = id(item)  # You can replace this with a UUID if needed
        entity_map[entity_id] = {
            'text': item['text'],
            'type': item['semantic_types'],
            'parent_id': item['parent_id'],
            'link_urls': item['link_urls']
        }

        parent_id = item['parent_id']
        if parent_id:
            if parent_id not in children_map:
                children_map[parent_id] = []
            children_map[parent_id].append(entity_id)

    # Step 4: Add children to entities
    for entity_id in entity_map:
        entity_map[entity_id]['children_ids'] = children_map.get(entity_id, [])

    return {
        'deduplicated_items': deduplicated_items,
        'grouped_by_type': grouped,
        'entity_map': entity_map
    }

def extract_faculty_member(items: List[ElementData]):
    keywords = ['ts.', 'ths.', 'pgs.', 'gs.']

    results = []
    for item in items:
        if any(keyword in item['text'].lower() for keyword in keywords):
            results.append(item)

    return results

def extract_contact_info(items: List[ElementData]):
    """
    Extract contact information (primarily emails) from the provided items.
    Groups by department (course_code) to associate emails with departments.
    
    Args:
        items: List of ElementData items containing text and metadata
        
    Returns:
        Dictionary with department information and associated emails
    """
    # Dictionary to store the final result
    result = {
        "departments": []
    }
    
    # Dictionary to track departments by name
    departments_by_name = {}
    
    # First pass: collect all departments and their emails
    for item in items:
        # Extract emails from the item
        emails = []
        if 'regex_patterns' in item and 'emails' in item['regex_patterns'] and item['regex_patterns']['emails']:
            emails = item['regex_patterns']['emails']
        
        # Extract department name (course_code)
        department_name = 'general'
        if 'regex_patterns' in item and 'course_codes' in item['regex_patterns'] and item['regex_patterns']['course_codes']:
            # Use the first course code as the department name
            department_name = item['regex_patterns']['course_codes'][0]
        
        # Add department if it doesn't exist
        if department_name not in departments_by_name:
            departments_by_name[department_name] = {
                "name": department_name,
                "emails": set()
            }
        
        # Add emails to the department
        departments_by_name[department_name]["emails"].update(emails)
    
    # Convert sets to lists for JSON serialization
    for dept_name, dept_data in departments_by_name.items():
        dept_data["emails"] = list(dept_data["emails"])
        result["departments"].append(dept_data)
    
    return result

if __name__ == "__main__":

    # Example usage
    json_data = read_json_file("output_20250617_182455.json")

    # faculty_raw_data = json_data['categorized_elements']['faculty_member']
    # extracted_faculty = extract_faculty_member(faculty_raw_data)
    # # Save extracted faculty to JSON file
    # with open('extracted_faculty.json', 'w', encoding='utf-8') as f:
    #     json.dump(extracted_faculty, f, indent=2, ensure_ascii=False)

    # print("RAW faculty members length:", len(faculty_raw_data))
    # print("Extracted faculty members length:", len(extracted_faculty))


    # contact_info_raw_data = json_data['categorized_elements']['contact_info']
    # extracted_contact_info = extract_contact_info(contact_info_raw_data)

    # with open('extracted_contact_info.json', 'w', encoding='utf-8') as f:
    #     json.dump(extracted_contact_info, f, indent=2, ensure_ascii=False)

    # print("RAW contact_info length:", len(contact_info_raw_data))
    # print("Extracted contact_info length:", len(extracted_contact_info))

    # course_info_raw_data = json_data['categorized_elements']['course_info']
    # extracted_course_info = extract_course_info(course_info_raw_data)

    # with open('extracted_course_info.json', 'w', encoding='utf-8') as f:
    #     json.dump(extracted_course_info, f, indent=2, ensure_ascii=False)

    general_raw_data = json_data['categorized_elements']['general_content']
    extracted_general = extract_course_info(general_raw_data)

    with open('extracted_general.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_general, f, indent=2, ensure_ascii=False)







