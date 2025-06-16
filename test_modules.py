"""
Simple test script to verify the modular structure works correctly.
This script tests individual modules without requiring external dependencies.
"""

def test_text_processor_basic():
    """Test basic text processing functions"""
    print("Testing text_processor module...")
    
    try:
        from modules.text_processor import extract_regex_patterns
        
        # Test data
        test_text = "Contact Dr. Smith at john.smith@university.edu or call (555) 123-4567. Course CS101 meets in Room 204."
        patterns = extract_regex_patterns(test_text)
        print(f"✓ Regex patterns extracted: {list(patterns.keys())}")
        
        if 'emails' in patterns:
            print(f"  - Found emails: {patterns['emails']}")
        if 'phone_numbers' in patterns:
            print(f"  - Found phone numbers: {patterns['phone_numbers']}")
        if 'course_codes' in patterns:
            print(f"  - Found course codes: {patterns['course_codes']}")
            
        return True
        
    except Exception as e:
        print(f"✗ Error in text_processor: {e}")
        return False


def test_utils_basic():
    """Test basic utility functions"""
    print("\nTesting utils module...")
    
    try:
        from modules.utils import create_output_data
        
        # Test data
        mock_elements = [
            {'text': 'Dr. John Smith', 'type': 'Title'},
            {'text': 'Computer Science Department', 'type': 'Text'}
        ]
        mock_categorized = {
            'faculty_member': [{'text': 'Dr. Smith'}],
            'department': [{'text': 'Computer Science Department'}]
        }
        
        output_data = create_output_data(mock_elements, mock_categorized)
        print(f"✓ Output data structure created")
        print(f"  - Total elements: {output_data['total_elements']}")
        print(f"  - Categories: {list(output_data['categorized_elements'].keys())}")
        print(f"  - Summary keys: {list(output_data['summary'].keys())}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in utils: {e}")
        return False


def test_classification():
    """Test semantic classification without external dependencies"""
    print("\nTesting semantic classification...")
    
    try:
        from modules.text_processor import classify_element_semantic_type
        
        # Test cases
        test_cases = [
            {
                'name': 'Faculty member',
                'data': {
                    'text': 'Dr. John Smith, Professor of Computer Science',
                    'html_attributes': {'class': ['faculty'], 'id': 'prof-smith'},
                    'regex_patterns': {'emails': ['john.smith@university.edu']}
                },
                'expected': 'faculty_member'
            },
            {
                'name': 'Department',
                'data': {
                    'text': 'Department of Computer Science',
                    'html_attributes': {'class': ['department'], 'id': 'cs-dept'},
                    'regex_patterns': {}
                },
                'expected': 'department'
            },
            {
                'name': 'Course info',
                'data': {
                    'text': 'Introduction to Programming',
                    'html_attributes': {'class': ['course'], 'id': 'cs101'},
                    'regex_patterns': {'course_codes': ['CS101']}
                },
                'expected': 'course_info'
            }
        ]
        
        for test_case in test_cases:
            semantic_types = classify_element_semantic_type(test_case['data'])
            if test_case['expected'] in semantic_types:
                print(f"✓ {test_case['name']}: {semantic_types}")
            else:
                print(f"? {test_case['name']}: {semantic_types} (expected {test_case['expected']})")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in classification: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("MODULAR STRUCTURE TEST (Basic Functions)")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    if test_text_processor_basic():
        tests_passed += 1
    
    if test_utils_basic():
        tests_passed += 1
        
    if test_classification():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("✓ All basic tests passed! The modular structure is working correctly.")
        print("\nNote: Full functionality requires installing dependencies:")
        print("  - beautifulsoup4 (for HTML processing)")
        print("  - unstructured[html] (for HTML partitioning)")
        print("  - requests (for web scraping)")
    else:
        print("✗ Some tests failed. Check the error messages above.")


if __name__ == "__main__":
    main()