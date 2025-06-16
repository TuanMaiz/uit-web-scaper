# Migration Guide: From Monolithic to Modular Structure

## Overview

The original `main.py` file has been successfully refactored into a modular structure. This document explains what changed and how to use the new structure.

## What Changed

### Before (Monolithic Structure)
```
main.py (234 lines)
├── All imports at the top
├── extract_html_attributes()
├── extract_regex_patterns()
├── classify_element_semantic_type()
├── extract_enhanced_element_data()
├── filter_and_categorize_elements()
└── main()
```

### After (Modular Structure)
```
main.py (simplified, 45 lines)
modules/
├── __init__.py
├── html_processor.py      # HTML parsing functions
├── text_processor.py      # Text analysis functions
├── data_processor.py      # Data extraction functions
├── web_scraper.py         # Web scraping functions
└── utils.py               # Utility functions
```

## Function Migration Map

| Original Function | New Location | Purpose |
|------------------|--------------|---------|
| `extract_html_attributes()` | `modules/html_processor.py` | HTML attribute extraction |
| `extract_regex_patterns()` | `modules/text_processor.py` | Pattern extraction |
| `classify_element_semantic_type()` | `modules/text_processor.py` | Semantic classification |
| `extract_enhanced_element_data()` | `modules/data_processor.py` | Element data extraction |
| `filter_and_categorize_elements()` | `modules/data_processor.py` | Data filtering |
| `main()` | `main.py` | Main execution (simplified) |
| New: `fetch_html_content()` | `modules/web_scraper.py` | URL fetching |
| New: `process_url()` | `modules/web_scraper.py` | URL processing |
| New: `read_urls_from_file()` | `modules/utils.py` | File operations |
| New: `save_output_data()` | `modules/utils.py` | Data saving |

## Benefits Achieved

### 1. **Separation of Concerns**
- HTML processing is isolated in `html_processor.py`
- Text analysis is contained in `text_processor.py`
- Data operations are centralized in `data_processor.py`
- Web scraping logic is in `web_scraper.py`
- Utility functions are in `utils.py`

### 2. **Improved Maintainability**
- Each module has a single responsibility
- Easier to locate and modify specific functionality
- Reduced code complexity per file

### 3. **Better Reusability**
```python
# You can now import specific functions
from modules.text_processor import extract_regex_patterns
from modules.html_processor import extract_html_attributes

# Or use individual modules
import modules.utils as utils
urls = utils.read_urls_from_file('my_urls.txt')
```

### 4. **Enhanced Testing**
- Each module can be tested independently
- Easier to mock dependencies
- Better test coverage possible

### 5. **Cleaner Dependencies**
- Dependencies are loaded only when needed
- Reduced import-time overhead
- Better error handling for missing dependencies

## Usage Examples

### Using Individual Functions
```python
from modules.text_processor import extract_regex_patterns

text = "Contact john@example.com or call (555) 123-4567"
patterns = extract_regex_patterns(text)
print(patterns)  # {'emails': ['john@example.com'], 'phone_numbers': ['(555) 123-4567']}
```

### Using Complete Modules
```python
from modules import utils

# Read URLs
urls = utils.read_urls_from_file('urls.txt')

# Create output data
output_data = utils.create_output_data(elements, categorized)

# Save results
utils.save_output_data(output_data, 'results.json')
```

### Custom Processing Pipeline
```python
from modules.web_scraper import fetch_html_content, partition_html_content
from modules.data_processor import extract_enhanced_element_data

# Custom processing
html = fetch_html_content('https://example.com')
elements = partition_html_content(html, 'https://example.com')
enhanced_data = [extract_enhanced_element_data(el) for el in elements]
```

## Backward Compatibility

The main interface remains unchanged:
```bash
python main.py
```

The output format and functionality are identical to the original version.

## Testing

Run the test suite to verify everything works:
```bash
python test_modules.py
```

## Dependencies

The same dependencies are required:
- `unstructured[html]`
- `requests`
- `beautifulsoup4`
- `lxml`

## File Size Comparison

| File | Original | New | Reduction |
|------|----------|-----|-----------|
| main.py | 234 lines | 45 lines | 81% smaller |
| Total LOC | 234 lines | ~280 lines | Better organized |

## Next Steps

1. **Install dependencies** if not already installed
2. **Run tests** to verify functionality
3. **Use individual modules** for custom processing
4. **Extend functionality** by adding new modules

The modular structure makes it easy to add new features, such as:
- Database storage modules
- Additional text processors
- Custom output formatters
- API integration modules