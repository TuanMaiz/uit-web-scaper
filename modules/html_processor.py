"""
HTML processing utilities for extracting attributes and element data.
"""

from bs4 import BeautifulSoup


def extract_html_attributes(text_as_html):
    """Extract HTML attributes like class, id, href from raw HTML"""
    if not text_as_html:
        return {}
    
    attributes = {}
    try:
        soup = BeautifulSoup(text_as_html, 'html.parser')
        if soup.find():
            tag = soup.find()
            attributes = {
                'tag_name': tag.name,
                'class': tag.get('class', []),
                'id': tag.get('id'),
                'href': tag.get('href'),
                'title': tag.get('title'),
                'data_attributes': {k: v for k, v in tag.attrs.items() if k.startswith('data-')}
            }
    except Exception as e:
        print(f"Error parsing HTML attributes: {e}")
    
    return attributes


def extract_table_info(text_as_html):
    """Extract table-specific information from HTML"""
    if not text_as_html:
        return {}
    
    try:
        soup = BeautifulSoup(text_as_html, 'html.parser')
        rows = soup.find_all('tr')
        return {
            'row_count': len(rows),
            'column_count': len(rows[0].find_all(['td', 'th'])) if rows else 0,
            'has_header': bool(soup.find('th'))
        }
    except Exception:
        return {}