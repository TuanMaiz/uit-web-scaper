"""
Web scraping utilities for fetching and processing HTML content from URLs.
"""

import requests


def fetch_html_content(url, timeout=30):
    """Fetch HTML content from a URL with error handling"""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def partition_html_content(html_content, url):
    """Partition HTML content into structured elements"""
    try:
        from unstructured.partition.html import partition_html
        elements = partition_html(
            text=html_content, 
            url=url,
            include_page_breaks=True,
            include_metadata=True
        )
        return elements
    except Exception as e:
        print(f"Error partitioning HTML for {url}: {e}")
        return []


def process_url(url, extract_element_data_func):
    """Process a single URL and extract element data"""
    print(f"Processing URL: {url}")
    
    # Fetch HTML content
    html_content = fetch_html_content(url)
    if not html_content:
        return []
    
    # Partition HTML into elements
    elements = partition_html_content(html_content, url)
    if not elements:
        return []
    
    # Extract enhanced data for each element
    extracted_elements = []
    for element in elements:
        enhanced_data = extract_element_data_func(element)
        if enhanced_data['text']:  # Only add non-empty elements
            extracted_elements.append(enhanced_data)
    
    return extracted_elements