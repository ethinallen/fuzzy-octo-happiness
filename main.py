import requests
from bs4 import BeautifulSoup
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_blog_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract blog links
    blog_links = soup.find_all('a', href=True)
    blog_urls = [link['href'] for link in blog_links if '/blog/' in link['href']]
    
    # Ensure URLs are absolute
    blog_urls = [url if url.startswith('http') else f"https://workos.com{url}" for url in blog_urls]
    
    return blog_urls

def find_non_webp_images(blog_url):
    try:
        logging.info(f"Checking images on blog URL: {blog_url}")
        response = requests.get(blog_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = soup.find_all('img', src=True)
        non_webp_images = [img['src'] for img in images if not img['src'].endswith('.webp')]
        
        return non_webp_images
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve images from {blog_url}: {e}")
        return []

def main():
    file_path = './blog.html'
    blog_urls = get_blog_urls_from_file(file_path)
    
    results = {}
    
    for blog_url in blog_urls:
        non_webp_images = find_non_webp_images(blog_url)
        if non_webp_images:
            results[blog_url] = non_webp_images
    
    with open('non_webp_images.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()
