"""
HTML Content Extraction and Processing Modules

This package provides modular functionality for extracting and processing
HTML content from web pages, including:

- HTML processing and attribute extraction
- Text processing and pattern recognition
- Data filtering and categorization
- Web scraping utilities
- File operations and data management

Import modules individually to avoid dependency issues:
    from modules.text_processor import extract_regex_patterns
    from modules.utils import read_urls_from_file
"""

# Define what's available when importing the package
__all__ = [
    'html_processor',
    'text_processor', 
    'data_processor',
    'web_scraper',
    'utils'
]

# Convenience imports - only import what's needed
def get_html_processor():
    """Get HTML processor functions"""
    from . import html_processor
    return html_processor

def get_text_processor():
    """Get text processor functions"""
    from . import text_processor
    return text_processor

def get_data_processor():
    """Get data processor functions"""
    from . import data_processor
    return data_processor

def get_web_scraper():
    """Get web scraper functions"""
    from . import web_scraper
    return web_scraper

def get_utils():
    """Get utility functions"""
    from . import utils
    return utils