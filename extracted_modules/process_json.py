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


def extract_faculty_member(items: List[ElementData]):
    keywords = ['ts.', 'ths.', 'pgs.', 'gs.']

    results = []
    for item in items:
        if any(keyword in item['text'].lower() for keyword in keywords):
            results.append(item)

    return results


if __name__ == "__main__":

    # Example usage
    json_data = read_json_file("output_20250616_231950.json")

    faculty_raw_data = json_data['categorized_elements']['faculty_member']

    extracted_faculty = extract_faculty_member(faculty_raw_data)

    # Save extracted faculty to JSON file
    with open('extracted_faculty.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_faculty, f, indent=2, ensure_ascii=False)

    print("RAW faculty members length:", len(faculty_raw_data))
    print("Extracted faculty members length:", len(extracted_faculty))
