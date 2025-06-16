"""
Main script for extracting and categorizing information from HTML content.

This script processes URLs from urls.txt, extracts structured data from HTML content,
and saves the results to enhanced_unstructured_output.json.
"""

import datetime


def main():
    """Main function to orchestrate the HTML content extraction process"""
    # Import modules locally to avoid dependency issues during import
    from modules.utils import (
        read_urls_from_file,
        create_output_data,
        save_output_data,
        print_summary
    )
    from modules.web_scraper import process_url
    from modules.data_processor import extract_enhanced_element_data, filter_and_categorize_elements
    
    # Read URLs from urls.txt
    target_urls = read_urls_from_file('urls.txt')
    if not target_urls:
        print("No URLs found to process.")
        return

    all_elements = []
    total_urls = len(target_urls)

    # Process each URL
    for idx, url in enumerate(target_urls, start=1):
        print(f"[{idx}/{total_urls}] Processing URL: {url}")
        
        # Process URL and extract elements
        elements = process_url(url, extract_enhanced_element_data)
        all_elements.extend(elements)

    # Filter and categorize elements
    categorized_elements = filter_and_categorize_elements(all_elements)
    
    # Create output data structure
    output_data = create_output_data(all_elements, categorized_elements)
    
    # Save data to file
    save_output_data(output_data, f"enhanced_unstructured_output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    # Print summary
    print_summary(output_data)


if __name__ == "__main__":
    main()