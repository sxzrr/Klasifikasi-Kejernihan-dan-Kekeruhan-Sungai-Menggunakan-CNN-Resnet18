# scrape_sungai_advanced.py
# Download langsung dengan delay + proxy rotation
# Lebih cepat dan tidak mudah terdeteksi

import os
import requests
import time
from urllib.parse import urlencode
from PIL import Image
from io import BytesIO
import random
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# User agents untuk rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# ======================================================
# 1️⃣ Dataset keywords
# ======================================================
dataset = {
    "jernih": [
        "sungai jernih",
        "clear river",
        "air sungai bening",
        "mountain stream",
        "crystal clear water",
        "river clear water",
    ],
    "keruh": [
        "sungai keruh",
        "muddy river",
        "turbid river",
        "polluted river",
        "brown river",
        "dirty river water",
    ]
}

BASE_DIR = "datasetScrap3"
os.makedirs(BASE_DIR, exist_ok=True)

def get_random_headers():
    """Return random headers untuk bypass bot detection"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.bing.com/"
    }

def search_bing_images(query, max_images=50):
    """Search images from Bing"""
    images_urls = []
    
    try:
        # Bing Image Search endpoint
        params = {
            "q": query,
            "count": min(max_images, 150),
        }
        
        url = "https://www.bing.com/images/search?" + urlencode(params)
        headers = get_random_headers()
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Extract image URLs dari HTML (simple parsing)
        import re
        pattern = r'"murl":"([^"]+)"'
        matches = re.findall(pattern, response.text)
        
        images_urls = list(set(matches[:max_images]))  # Remove duplicates
        logger.info(f"Found {len(images_urls)} images for '{query}'")
        
    except Exception as e:
        logger.error(f"Error searching Bing: {e}")
    
    return images_urls

def download_image(url, filepath, timeout=10):
    """Download single image"""
    try:
        headers = get_random_headers()
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()
        
        # Verify it's an image
        img = Image.open(BytesIO(response.content))
        if img.size[0] < 200 or img.size[1] < 200:
            return False
        
        # Save image
        img.save(filepath, quality=95)
        return True
        
    except Exception as e:
        logger.debug(f"Failed to download {url}: {str(e)[:50]}")
        return False

def scrape_category(category_name, keywords, target_count=200):
    """Scrape images for a category"""
    folder_path = os.path.join(BASE_DIR, category_name)
    os.makedirs(folder_path, exist_ok=True)
    
    downloaded = 0
    current_image_num = len(os.listdir(folder_path))
    
    logger.info(f"\n{'='*60}")
    logger.info(f"🎯 Scraping category: {category_name} (target: {target_count} images)")
    logger.info(f"{'='*60}")
    
    for keyword in keywords:
        if downloaded >= target_count:
            break
            
        logger.info(f"\n🔍 Searching: '{keyword}'")
        
        # Search images
        urls = search_bing_images(keyword, max_images=100)
        
        for idx, url in enumerate(urls):
            if downloaded >= target_count:
                break
            
            current_image_num += 1
            filename = f"{current_image_num:04d}.jpg"
            filepath = os.path.join(folder_path, filename)
            
            # Skip if already exists
            if os.path.exists(filepath):
                continue
            
            logger.info(f"  Downloading {filename} ({idx+1}/{len(urls)})...", end=" ")
            
            if download_image(url, filepath):
                downloaded += 1
                logger.info("✅")
                time.sleep(random.uniform(0.5, 2))  # Random delay
            else:
                logger.info("❌")
                time.sleep(random.uniform(0.3, 1))
        
        time.sleep(random.uniform(3, 7))  # Delay between keywords
    
    logger.info(f"\n✅ Category '{category_name}' complete: {downloaded} images downloaded")
    logger.info(f"📁 Saved to: {folder_path}")

# ======================================================
# Main scraping
# ======================================================
if __name__ == "__main__":
    logger.info("🚀 Starting advanced river image scraping...")
    
    for category, keywords in dataset.items():
        scrape_category(category, keywords, target_count=200)
    
    logger.info("\n" + "="*60)
    logger.info("🎉 Scraping complete!")
    logger.info("="*60)
    
    # Summary
    for category in dataset.keys():
        folder = os.path.join(BASE_DIR, category)
        count = len(os.listdir(folder))
        logger.info(f"{category}: {count} images")
