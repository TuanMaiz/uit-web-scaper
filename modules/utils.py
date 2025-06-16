"""
Utility functions for file operations and data management.
"""

import json


def read_urls_from_file(filename='urls.txt'):
    """Read URLs from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return []
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []


def save_output_data(data, filename='enhanced_unstructured_output.json'):
    """Save extracted data to JSON file"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")
        return False


def create_output_data(all_elements, categorized_elements):
    """Create structured output data with summary"""
    return {
        'total_elements': len(all_elements),
        'categorized_elements': categorized_elements,
        'raw_elements': all_elements,
        'summary': {
            'faculty_members': len(categorized_elements.get('faculty_member', [])),
            'departments': len(categorized_elements.get('department', [])),
            'courses': len(categorized_elements.get('course_info', [])),
            'contact_info': len(categorized_elements.get('contact_info', [])),
            'main_content': len(categorized_elements.get('main_content', []))
        }
    }


def print_summary(output_data):
    """Print processing summary"""
    print("Enhanced extraction complete.")
    print(f"Summary: {output_data['summary']}")
    print(f"Total elements processed: {output_data['total_elements']}")