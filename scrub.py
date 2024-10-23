import json
from collections import Counter

def scrub_unique_images_across_pages(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Flatten all image URLs into a single list
    all_images = [img for images in data.values() for img in images if img]
    
    # Count occurrences of each image URL
    image_counts = Counter(all_images)
    
    scrubbed_data = {}
    
    for url, images in data.items():
        # Only include images that appear exactly once across all pages
        unique_images = [img for img in images if image_counts[img] == 1]
        if unique_images:
            scrubbed_data[url] = unique_images
    
    with open(output_file, 'w') as f:
        json.dump(scrubbed_data, f, indent=4)

if __name__ == "__main__":
    input_file = 'non_webp_images.json'
    output_file = 'scrubbed_unique_non_webp_images.json'
    scrub_unique_images_across_pages(input_file, output_file)
