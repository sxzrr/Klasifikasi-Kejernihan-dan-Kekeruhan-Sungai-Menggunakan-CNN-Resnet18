# scrape_google_simple.py
# Direct Google Images scraping without Selenium
import os
import requests
import time
from urllib.parse import urlencode, quote
from PIL import Image
from io import BytesIO
import json
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

dataset = {
    "jernih": [
        "sungai jernih",
        "clear river",
        "air sungai bening",
        "river clear water",
        "bening jernih",
    ],
    "keruh": [
        "sungai keruh",
        "muddy river",
        "turbid river",
        "brown muddy river",
        "dirty river water",
    ]
}

BASE_DIR = "datasetScrap3"
os.makedirs(BASE_DIR, exist_ok=True)

def get_google_images_urls(keyword, num_images=100):
    """Extract Google Images URLs"""
    urls = []
    
    try:
        # Use Google Images direct link
        params = {
            'q': keyword,
            'tbm': 'isch',
            'ijn': '0'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        # Try multiple image search APIs
        # Method 1: Direct Google Images scraping
        google_url = "https://www.google.com/search?" + urlencode(params)
        
        response = requests.get(google_url, headers=headers, timeout=10)
        
        # Extract image URLs from HTML
        import re
        # Pattern untuk image URLs di Google Images
        patterns = [
            r'"https://[^"]*?/image[^"]*?"',
            r'data-src="([^"]+)"',
            r'"url":"([^"]*?)"',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response.text)
            urls.extend([m.strip('"') for m in matches if 'http' in m])
        
        # Remove duplicates and clean URLs
        urls = list(set(u for u in urls if u.startswith('http')))[:num_images]
        
        logger.info(f"Found {len(urls)} image URLs for '{keyword}'")
    
    except Exception as e:
        logger.error(f"Error: {e}")
    
    return urls

def download_image(url, filepath, timeout=15):
    """Download image"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.google.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout, stream=True, verify=False)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        
        if img.size[0] < 200 or img.size[1] < 200:
            return False
        
        img.save(filepath, quality=95)
        return True
    
    except Exception as e:
        return False

def scrape_category(category_name, keywords, target=200):
    """Scrape one category"""
    folder = os.path.join(BASE_DIR, category_name)
    os.makedirs(folder, exist_ok=True)
    
    downloaded = 0
    current_num = len([f for f in os.listdir(folder) if f.endswith('.jpg')])
    
    logger.info(f"\n{'='*60}")
    logger.info(f"📥 {category_name.upper()} - Target: {target} images")
    logger.info(f"{'='*60}")
    
    for keyword in keywords:
        if downloaded >= target:
            break
        
        logger.info(f"\n🔍 '{keyword}'")
        
        urls = get_google_images_urls(keyword, num_images=80)
        
        for idx, url in enumerate(urls):
            if downloaded >= target:
                break
            
            current_num += 1
            filename = f"{current_num:04d}.jpg"
            filepath = os.path.join(folder, filename)
            
            if os.path.exists(filepath):
                continue
            
            logger.info(f"  {idx+1}/{len(urls)}: ", end="")
            
            if download_image(url, filepath):
                downloaded += 1
                logger.info(f"✅ {filename}")
                time.sleep(random.uniform(0.3, 1))
            else:
                logger.info("❌")
                time.sleep(random.uniform(0.1, 0.3))
        
        time.sleep(random.uniform(2, 4))
    
    logger.info(f"\n✅ {category_name}: {downloaded} images saved")

if __name__ == "__main__":
    logger.info("🚀 Starting Google Images Scraper")
    
    for category, keywords in dataset.items():
        scrape_category(category, keywords, target=200)
    
    logger.info("\n" + "="*60)
    logger.info("✅ COMPLETE!")
    for cat in dataset:
        count = len([f for f in os.listdir(os.path.join(BASE_DIR, cat)) if f.endswith('.jpg')])
        logger.info(f"{cat}: {count} images")
