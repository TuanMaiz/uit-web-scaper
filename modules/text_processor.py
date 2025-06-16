"""
Text processing utilities for pattern extraction and semantic classification.
"""

import re


def extract_regex_patterns(text):
    """Extract common patterns like emails, phone numbers, course codes"""
    patterns = {
        'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
        'phone_numbers': re.findall(r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b', text),
        'course_codes': re.findall(r'\b[A-Z]{2,4}[-\s]?\d{3,4}[A-Z]?\b', text),
        'years': re.findall(r'\b(19|20)\d{2}\b', text),
        'urls': re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text),
        'room_numbers': re.findall(r'\b[A-Z]?\d{1,4}[A-Z]?\b(?:\s*(?:Room|Rm|Office|Bldg|Building))?', text, re.IGNORECASE)
    }
    
    # Remove empty lists
    return {k: v for k, v in patterns.items() if v}


def classify_element_semantic_type(element_data):
    """Classify elements based on content patterns and HTML attributes"""
    text = element_data['text'].lower()
    html_attrs = element_data.get('html_attributes', {})
    classes = ' '.join(html_attrs.get('class', [])).lower()
    element_id = (html_attrs.get('id') or '').lower()
    
    # Classification rules based on content and attributes
    semantic_types = []
    
    # Faculty/Staff indicators
    if any(keyword in text for keyword in ['professor', 'dr.', 'ph.d', 'faculty', 'instructor', 'lecturer']):
        semantic_types.append('faculty_member')
    
    if any(keyword in classes + element_id for keyword in ['faculty', 'staff', 'professor', 'instructor']):
        semantic_types.append('faculty_member')
    
    # Department indicators
    if any(keyword in text for keyword in ['department', 'school of', 'college of', 'division']):
        semantic_types.append('department')
    
    if any(keyword in classes + element_id for keyword in ['department', 'dept', 'school', 'college']):
        semantic_types.append('department')
    
    # Course indicators
    if element_data.get('regex_patterns', {}).get('course_codes'):
        semantic_types.append('course_info')
    
    if any(keyword in text for keyword in ['course', 'credit', 'prerequisite', 'syllabus']):
        semantic_types.append('course_info')
    
    # Contact information
    if element_data.get('regex_patterns', {}).get('emails') or element_data.get('regex_patterns', {}).get('phone_numbers'):
        semantic_types.append('contact_info')
    
    # Navigation elements
    if any(keyword in classes + element_id for keyword in ['nav', 'menu', 'breadcrumb', 'sidebar']):
        semantic_types.append('navigation')
    
    # Content areas
    if any(keyword in classes + element_id for keyword in ['content', 'main', 'article', 'post']):
        semantic_types.append('main_content')
    
    # Headers and footers
    if any(keyword in classes + element_id for keyword in ['header', 'footer', 'banner']):
        semantic_types.append('page_structure')
    
    return semantic_types if semantic_types else ['general_content']