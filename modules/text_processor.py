"""
Text processing utilities for pattern extraction and semantic classification.
"""

import re


def extract_regex_patterns(text):
    """Extract common patterns like emails, phone numbers, course codes"""
    patterns = {
        'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
        'phone_numbers': re.findall(r'\b(?:\+84|0)(?:\d{9})\b', text), # change to vietnam phone number
        'course_codes': re.findall(r'\b[A-Z]{2,4}\d{3,4}(?:\.[A-Z]{2,4}\d{3,4})?\b|.+\s*\(.*?\)', text), # code for uit course
        'years': re.findall(r'\b(19|20)\d{2}\b', text),
        'urls': re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text),
        'room_numbers': re.findall(r'\b[A-Z]?\d{1,4}[A-Z]?\b(?:\s*(?:Room|Rm|Office|Bldg|Building))?', text, re.IGNORECASE)
    }
    
    # Remove empty lists
    return {k: v for k, v in patterns.items() if v}


def classify_element_semantic_type(element_data):
    """Phân loại phần tử dựa trên mẫu nội dung và thuộc tính HTML"""
    text = element_data['text'].lower()
    html_attrs = element_data.get('html_attributes', {})
    classes = ' '.join(html_attrs.get('class', [])).lower()
    element_id = (html_attrs.get('id') or '').lower()

    # Quy tắc phân loại dựa trên nội dung và thuộc tính
    semantic_types = []

    # Dấu hiệu Giảng viên/Nhân sự
    if any(keyword in text for keyword in ['giáo sư', 'gs.', 'phó giáo sư', 'pgs.', 'tiến sĩ', 'ts.', 'giảng viên', 'gv.', 'giáo viên', 'giảng dạy']):
        semantic_types.append('faculty_member')

    if any(keyword in classes + element_id for keyword in ['giảng viên', 'nhân sự', 'giáo sư', 'giảng dạy']):
        semantic_types.append('faculty_member')

    # Dấu hiệu Khoa/Bộ môn
    if any(keyword in text for keyword in ['khoa', 'ngành']):
        semantic_types.append('department')

    # if any(keyword in classes + element_id for keyword in ['khoa', 'bộ môn', 'trường', 'đại học']):
    #     semantic_types.append('department')

    # Dấu hiệu Môn học
    if element_data.get('regex_patterns', {}).get('course_codes'):
        semantic_types.append('course_info')

    if any(keyword in text for keyword in ['môn', 'tín chỉ', 'điều kiện tiên quyết', 'đề cương']):
        semantic_types.append('course_info')

    # Thông tin liên hệ
    if element_data.get('regex_patterns', {}).get('emails') or element_data.get('regex_patterns', {}).get('phone_numbers'):
        semantic_types.append('contact_info')

    # Dấu hiệu Điều hướng
    if any(keyword in classes + element_id for keyword in ['nav', 'menu', 'breadcrumb', 'sidebar', 'title-menu']):
        semantic_types.append('navigation')

    # Khu vực nội dung
    if any(keyword in classes + element_id for keyword in ['content', 'nội dung', 'chính', 'bài viết', 'bài đăng']):
        semantic_types.append('main_content')

    # Header và Footer
    if any(keyword in classes + element_id for keyword in ['đầu trang', 'cuối trang', 'banner']):
        semantic_types.append('page_structure')

    return semantic_types if semantic_types else ['general_content']
