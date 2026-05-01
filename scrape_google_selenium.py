# scrape_google_selenium.py
# Using Selenium for better Google Images scraping
import os
import requests
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PIL import Image
from io import BytesIO
from urllib.parse import quote
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# ======================================================
# Dataset
# ======================================================
dataset = {
    "jernih": [
        "sungai jernih",
        "clear river indonesia",
        "air sungai bening",
        "mountain stream clear",
        "kristal clear river",
    ],
    "keruh": [
        "sungai keruh",
        "muddy river indonesia",
        "turbid river water",
        "polluted brown river",
        "dirty river water",
    ]
}

BASE_DIR = "datasetScrap3"
os.makedirs(BASE_DIR, exist_ok=True)

def setup_driver():
    """Setup Chrome driver dengan opsi headless"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def download_image(url, filepath):
    """Download image dari URL"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        
        # Check minimum size
        if img.size[0] < 200 or img.size[1] < 200:
            return False
        
        img.save(filepath, quality=95)
        return True
    except Exception as e:
        logger.debug(f"Failed: {str(e)[:40]}")
        return False

def scrape_google_images(keyword, max_images=150):
    """Scrape Google Images using Selenium"""
    driver = setup_driver()
    image_urls = set()
    
    try:
        url = f"https://www.google.com/search?q={quote(keyword)}&tbm=isch"
        logger.info(f"Opening: {url}")
        driver.get(url)
        
        # Scroll and load images
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for scroll_num in range(5):  # Scroll 5 times
            if len(image_urls) >= max_images:
                break
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 3))
            
            # Click "Show more results" if exists
            try:
                show_more = driver.find_element(By.CLASS_NAME, "mye4qd")
                show_more.click()
                time.sleep(1)
            except:
                pass
            
            # Extract image URLs
            thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.rg_i")
            logger.info(f"Found {len(thumbnails)} thumbnails")
            
            for img in thumbnails:
                try:
                    img.click()
                    time.sleep(random.uniform(0.3, 0.7))
                    
                    images = driver.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
                    for image in images:
                        src = image.get_attribute('src')
                        if src and 'http' in src and len(image_urls) < max_images:
                            image_urls.add(src)
                except:
                    continue
        
        logger.info(f"Collected {len(image_urls)} image URLs")
    
    except Exception as e:
        logger.error(f"Scraping error: {e}")
    
    finally:
        driver.quit()
    
    return list(image_urls)

def scrape_category(category_name, keywords, target_count=200):
    """Scrape category"""
    folder_path = os.path.join(BASE_DIR, category_name)
    os.makedirs(folder_path, exist_ok=True)
    
    downloaded = 0
    current_num = len(os.listdir(folder_path))
    
    logger.info(f"\n{'='*60}")
    logger.info(f"🎯 {category_name.upper()} (Target: {target_count})")
    logger.info(f"{'='*60}")
    
    for keyword in keywords:
        if downloaded >= target_count:
            break
        
        logger.info(f"\n🔍 '{keyword}'")
        urls = scrape_google_images(keyword, max_images=100)
        
        for idx, url in enumerate(urls):
            if downloaded >= target_count:
                break
            
            current_num += 1
            filename = f"{current_num:04d}.jpg"
            filepath = os.path.join(folder_path, filename)
            
            if os.path.exists(filepath):
                continue
            
            if download_image(url, filepath):
                downloaded += 1
                logger.info(f"  ✅ {filename}")
                time.sleep(random.uniform(0.5, 1.5))
            else:
                logger.info(f"  ❌ Failed")
                time.sleep(random.uniform(0.2, 0.5))
        
        time.sleep(random.uniform(3, 5))
    
    logger.info(f"\n✅ Downloaded: {downloaded}/{target_count}")

if __name__ == "__main__":
    for category, keywords in dataset.items():
        scrape_category(category, keywords, target_count=200)
    
    logger.info("\n" + "="*60)
    logger.info("🎉 Done!")
    logger.info("="*60)
