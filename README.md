# HTML Content Extraction Tool - Modular Version

This project has been refactored into a modular structure for better maintainability and organization.

## Project Structure

```
├── main.py                     # Main entry point
├── modules/                    # Modular components
│   ├── __init__.py            # Package initialization
│   ├── html_processor.py      # HTML processing utilities
│   ├── text_processor.py      # Text analysis and pattern extraction
│   ├── data_processor.py      # Data extraction and categorization
│   ├── web_scraper.py         # Web scraping utilities
│   └── utils.py               # File operations and utilities
├── urls.txt                   # Input URLs
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## Module Overview

### `html_processor.py`
- **Purpose**: HTML parsing and attribute extraction
- **Key Functions**:
  - `extract_html_attributes()`: Extract HTML attributes (class, id, href, etc.)
  - `extract_table_info()`: Extract table-specific information

### `text_processor.py`
- **Purpose**: Text analysis and pattern recognition
- **Key Functions**:
  - `extract_regex_patterns()`: Extract emails, phone numbers, course codes, etc.
  - `classify_element_semantic_type()`: Classify elements by semantic meaning

### `data_processor.py`
- **Purpose**: Data extraction and element processing
- **Key Functions**:
  - `extract_enhanced_element_data()`: Extract comprehensive element data
  - `filter_and_categorize_elements()`: Filter and categorize extracted elements

### `web_scraper.py`
- **Purpose**: Web scraping and HTML content fetching
- **Key Functions**:
  - `fetch_html_content()`: Fetch HTML from URLs with error handling
  - `partition_html_content()`: Partition HTML into structured elements
  - `process_url()`: Complete URL processing pipeline

### `utils.py`
- **Purpose**: Utility functions for file operations and data management
- **Key Functions**:
  - `read_urls_from_file()`: Read URLs from input file
  - `save_output_data()`: Save results to JSON file
  - `create_output_data()`: Structure output data with summary
  - `print_summary()`: Display processing results

## Usage

The main script remains the same:

```bash
python main.py
```

## Benefits of Modular Structure

1. **Separation of Concerns**: Each module handles a specific aspect of the processing
2. **Reusability**: Individual modules can be imported and used independently
3. **Maintainability**: Easier to modify and extend specific functionality
4. **Testing**: Each module can be tested independently
5. **Readability**: Cleaner, more organized code structure

## Dependencies

The project requires the same dependencies as before:
- `unstructured[html]`
- `requests`
- `beautifulsoup4`
- `lxml` (for HTML parsing)

## Example Usage of Individual Modules

```python
# Import specific functions
from modules import extract_html_attributes, extract_regex_patterns

# Or import the entire module
import modules

# Use individual functions
html_attrs = modules.extract_html_attributes(html_string)
patterns = modules.extract_regex_patterns(text)
```

## Migration Notes

- All functionality remains the same
- The main.py interface is unchanged
- Individual functions can now be imported and used separately
- Error handling and logging have been improved
- Code is more modular and testable