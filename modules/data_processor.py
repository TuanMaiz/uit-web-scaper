"""
Data processing utilities for element extraction, filtering, and categorization.
"""

from collections import defaultdict


def extract_enhanced_element_data(element):
    """Extract comprehensive data from each element"""
    # Import functions locally to avoid circular imports
    from .html_processor import extract_html_attributes, extract_table_info
    from .text_processor import extract_regex_patterns, classify_element_semantic_type
    
    # Basic element data
    element_data = {
        "text": element.text.strip() if element.text else "",
        "type": str(type(element).__name__),
        "source_url": element.metadata.url if hasattr(element.metadata, 'url') else None,
        "page_number": element.metadata.page_number if hasattr(element.metadata, 'page_number') else None,
    }
    
    # HTML attributes and raw HTML
    text_as_html = getattr(element.metadata, 'text_as_html', None)
    element_data['text_as_html'] = text_as_html
    element_data['html_attributes'] = extract_html_attributes(text_as_html)
    
    # Emphasis and formatting
    if hasattr(element.metadata, 'emphasized_text_contents'):
        element_data['emphasized_text'] = element.metadata.emphasized_text_contents
    
    if hasattr(element.metadata, 'emphasized_text_tags'):
        element_data['emphasis_tags'] = element.metadata.emphasized_text_tags
    
    # Hierarchical information
    if hasattr(element.metadata, 'parent_id'):
        element_data['parent_id'] = element.metadata.parent_id
    
    if hasattr(element.metadata, 'category_depth'):
        element_data['category_depth'] = element.metadata.category_depth
    
    # Link information
    if hasattr(element.metadata, 'link_urls'):
        element_data['link_urls'] = element.metadata.link_urls
    
    if hasattr(element.metadata, 'link_texts'):
        element_data['link_texts'] = element.metadata.link_texts
    
    # Table-specific metadata
    if element_data['type'] == 'Table' and hasattr(element.metadata, 'text_as_html'):
        element_data['table_info'] = extract_table_info(element.metadata.text_as_html)
    
    # Extract regex patterns
    if element_data['text']:
        element_data['regex_patterns'] = extract_regex_patterns(element_data['text'])
    
    # Classify semantic type
    element_data['semantic_types'] = classify_element_semantic_type(element_data)
    
    # Additional metadata
    element_data['word_count'] = len(element_data['text'].split()) if element_data['text'] else 0
    element_data['char_count'] = len(element_data['text']) if element_data['text'] else 0
    
    return element_data


def filter_and_categorize_elements(all_elements):
    """Filter and categorize elements for easier processing"""
    categorized = defaultdict(list)
    
    for element in all_elements:
        # Skip empty or very short elements
        if element['word_count'] < 2 and not element.get('regex_patterns'):
            continue
        
        # Skip navigation and structural elements unless they contain useful info
        if 'navigation' in element['semantic_types'] or 'page_structure' in element['semantic_types']:
            if not any(pattern in element.get('regex_patterns', {}) for pattern in ['emails', 'phone_numbers']):
                continue
        
        # Categorize by semantic type
        for semantic_type in element['semantic_types']:
            categorized[semantic_type].append(element)
    
    return dict(categorized)