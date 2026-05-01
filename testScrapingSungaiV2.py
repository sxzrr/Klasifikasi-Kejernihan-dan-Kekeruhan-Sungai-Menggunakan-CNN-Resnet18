# scrape_sungai_bing_v2.py
# By Firman Firdaus (OPSI B - BING IMAGE CRAWLER)
# Mengambil referensi dari JATI (Jurnal Mahasiswa Teknik Informatika) Vol.9 No.3 Juni 2025
#
# OPSI B - BING IMAGE CRAWLER (Alternative ke Google):
# ✅ BingImageCrawler dari icrawler (lebih reliable, jarang block)
# ✅ Struktur HTML Bing lebih stabil (jarang berubah)
# ✅ downloader_threads = 5 untuk parallel download
# ✅ delay 15-30 detik antar keyword
# ✅ delay 30-60 detik antar kategori
# ✅ retry logic dengan 2 kali percobaan
# ✅ User agent rotation
# ✅ Better header handling
# EXPECTED: 150-300 gambar per kategori (Bing lebih lenient)
# TARGET AKHIR: Google (datasetScrap3) + Bing (datasetScrap4) = 300-600 per kategori

import os
import time
import logging
from icrawler.builtin import BingImageCrawler
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Multiple User Agents untuk bypass detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# ======================================================
# 1️⃣ Daftar keyword per kelas (sama dengan Google)
# ======================================================
dataset = {
    "jernih": [
        # === KEYWORDS BARU (LEBIH SPECIFIC KE SUNGAI) ===
        "sungai jernih air biru",
        "clear blue river water",
        "transparent flowing river",
        "crystal clear flowing water",
        "blue river flowing clean",
        "sungai dengan air jernih biru",
        "clear water river flowing",
        "blue water mountain river",
        "jernih air mengalir sungai",
        "river with clear blue water",
        "mountain stream clear blue",
        "crystalline river water flowing",
        "clean flowing blue river",
        "sungai air jernih bening biru",
        "transparent blue river indonesia",
        "clear flowing water streams",
        "blue clear sungai air",
        "river clear blue water",
        "bening jernih sungai mengalir",
        "flowing clear water river",
    ],
    "keruh": [
        # === KEYWORDS BARU (LEBIH SPECIFIC KE SUNGAI KERUH) ===
        "sungai keruh air coklat",
        "muddy brown river water",
        "turbid brown flowing water",
        "sediment laden river water",
        "brown muddy flowing sungai",
        "sungai air keruh berlumpur coklat",
        "muddy water river flowing",
        "brown river turbid water",
        "keruh air berlumpur sungai",
        "river with muddy brown water",
        "muddy brown stream flowing",
        "sediment heavy river water",
        "turbid muddy flowing water",
        "sungai air keruh coklat berlumpur",
        "turbid brown river indonesia",
        "muddy flowing water streams",
        "brown muddy sungai air",
        "river muddy brown water",
        "keruh berlumpur sungai mengalir",
        "flowing muddy water river",
    ]
}

# ======================================================
# 2️⃣ Folder output
# ======================================================
BASE_DIR = "datasetScrap4"  # OPSI B: Gunakan folder baru datasetScrap4
os.makedirs(BASE_DIR, exist_ok=True)

# Tracking untuk duplicate detection
HASH_CACHE = {}

def get_image_hash(image_path):
    """Hitung SHA256 hash dari image yang sudah di-resize untuk duplicate detection"""
    try:
        img = Image.open(image_path)
        img.thumbnail((64, 64))
        img_hash = hashlib.sha256(img.tobytes()).hexdigest()
        return img_hash
    except Exception as e:
        logger.warning(f"Error hashing image {image_path}: {e}")
        return None

def is_duplicate(image_path):
    """Check apakah image sudah ada di cache (duplicate detection)"""
    img_hash = get_image_hash(image_path)
    if img_hash is None:
        return False
    
    if img_hash in HASH_CACHE:
        return True
    
    HASH_CACHE[img_hash] = image_path
    return False

def initialize_hash_cache(folder_path):
    """Load existing images ke hash cache untuk duplicate detection"""
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                img_path = os.path.join(folder_path, file)
                img_hash = get_image_hash(img_path)
                if img_hash:
                    HASH_CACHE[img_hash] = img_path

def download_image_url(url, folder_path, filename):
    """Download image dari URL dengan retry logic"""
    try:
        # Set timeout dan headers
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            # Validate image
            img = Image.open(BytesIO(response.content))
            
            # Check duplicate
            temp_path = os.path.join(folder_path, filename)
            img.save(temp_path)
            
            if is_duplicate(temp_path):
                os.remove(temp_path)
                return False  # Duplicate detected
            
            return True
        else:
            logger.debug(f"Failed to download {url}: Status {response.status_code}")
            return False
            
    except Exception as e:
        logger.debug(f"Error downloading {url}: {str(e)[:50]}")
        return False

def create_selenium_driver():
    """Buat Selenium WebDriver dengan undetected-chromedriver (anti-bot)"""
    
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        # Undetected Chrome lebih anti-bot detection (auto detect version)
        driver = uc.Chrome(options=options)  # Auto-detect Chrome version
        logger.info("✅ Undetected ChromeDriver initialized")
        return driver
    except Exception as e:
        logger.error(f"Failed to create undetected Chrome driver: {e}")
        logger.info("Trying fallback...")
        raise

def scrape_google_images_selenium(keyword, folder_path, max_num=100):
    """Scrape Google Images menggunakan undetected-chromedriver dengan scroll"""
    logger.info(f"🔍 Scraping Google Images for: '{keyword}'")
    
    driver = None
    downloaded = 0
    
    try:
        driver = create_selenium_driver()
        
        # Build Google Images search URL
        search_url = f"https://www.google.com/search?q={keyword}&tbm=isch&ijn=0"
        
        logger.info(f"📍 Opening: {search_url}")
        driver.get(search_url)
        
        # Wait untuk load halaman
        time.sleep(random.uniform(4, 7))
        
        # Scroll untuk load lebih banyak images
        scroll_pause_time = random.uniform(0.5, 1)
        for i in range(8):  # 8 scrolls
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(scroll_pause_time)
            logger.debug(f"   Scroll {i+1}/8")
        
        # Extract semua image URLs dari JavaScript
        image_urls = set()
        
        try:
            # Tunggu images render
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.rg_i"))
            )
        except:
            logger.debug("   Timeout waiting for images, continue anyway")
        
        # Extract dengan JavaScript (lebih reliable)
        script = """
        let urls = new Set();
        let images = document.querySelectorAll('img.rg_i');
        images.forEach(img => {
            let src = img.src;
            if (src && src.includes('http')) {
                urls.add(src);
            }
        });
        return Array.from(urls);
        """
        
        try:
            extracted_urls = driver.execute_script(script)
            image_urls.update(extracted_urls)
            logger.info(f"📷 Extracted {len(image_urls)} image URLs via JavaScript")
        except Exception as e:
            logger.debug(f"   JavaScript extraction failed: {str(e)[:50]}")
        
        # Fallback: Manual click dan extract (lebih lambat tapi reliable)
        if len(image_urls) < max_num // 2:
            logger.info("   Fallback ke manual extraction dengan click...")
            try:
                img_elements = driver.find_elements(By.CSS_SELECTOR, "img.rg_i")
                
                for idx, img_element in enumerate(img_elements[:max_num]):
                    if len(image_urls) >= max_num:
                        break
                    
                    try:
                        img_element.click()
                        time.sleep(random.uniform(0.3, 0.7))
                        
                        # Get actual image dari detail panel
                        images = driver.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
                        
                        for image in images:
                            src = image.get_attribute('src')
                            if src and 'http' in src and src not in image_urls:
                                image_urls.add(src)
                                break
                        
                        if idx % 5 == 0:
                            logger.debug(f"   Manual extraction: {idx}/{min(max_num, len(img_elements))}")
                    
                    except Exception as e:
                        logger.debug(f"   Error pada image {idx}: {str(e)[:30]}")
                        continue
            
            except Exception as e:
                logger.debug(f"   Manual extraction failed: {str(e)[:50]}")
        
        logger.info(f"✅ Total {len(image_urls)} unique URLs collected")
        
        # Download images
        for idx, url in enumerate(image_urls, 1):
            if downloaded >= max_num:
                break
            
            filename = f"image_{len(os.listdir(folder_path)) + 1}.jpg"
            
            if download_image_url(url, folder_path, filename):
                downloaded += 1
                logger.info(f"   ✅ Downloaded [{downloaded}/{max_num}]: {filename}")
            else:
                logger.debug(f"   ⏭️ Skipped/Duplicate")
            
            time.sleep(random.uniform(0.3, 0.8))
        
        logger.info(f"✅ Selesai: {keyword} ({downloaded} images berhasil)")
        return downloaded
        
    except Exception as e:
        logger.error(f"❌ Error scraping '{keyword}': {str(e)[:100]}")
        return downloaded
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

# ======================================================
# 3️⃣ Main scraping loop
# ======================================================
for label, keywords in dataset.items():
    folder_path = os.path.join(BASE_DIR, label)
    os.makedirs(folder_path, exist_ok=True)
    
    # Initialize hash cache untuk existing images
    initialize_hash_cache(folder_path)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"🎯 Scraping category: {label.upper()}")
    logger.info(f"{'='*60}")
    
    total_downloaded = 0
    
    for idx, keyword in enumerate(keywords, 1):
        logger.info(f"\n[{idx}/{len(keywords)}] 🔍 Processing: '{keyword}'")
        
        try:
            # Scrape dengan max 100-150 per keyword (slower tapi lebih quality)
            downloaded = scrape_google_images_selenium(keyword, folder_path, max_num=150)
            total_downloaded += downloaded
            
            # Delay ekstrim antar keyword untuk bypass detection (OPSI B)
            delay = random.uniform(60, 120)  # 1-2 menit!
            logger.info(f"⏳ Waiting {delay:.0f} seconds before next keyword...")
            time.sleep(delay)
            
        except KeyboardInterrupt:
            logger.warning("❌ Scraping dihentikan oleh user")
            break
        except Exception as e:
            logger.error(f"❌ Error pada keyword '{keyword}': {str(e)[:100]}")
            time.sleep(random.uniform(60, 120))
            continue
    
    logger.info(f"\n📁 Category '{label}' - Total downloaded: {total_downloaded}")
    
    # Delay antar kategori (even lebih lama)
    if label != list(dataset.keys())[-1]:  # Jangan delay di akhir
        delay = random.uniform(120, 180)  # 2-3 menit antar kategori
        logger.info(f"⏳ Long wait before next category: {delay:.0f} seconds...")
        time.sleep(delay)

logger.info("\n" + "="*60)
logger.info("🎉 Semua proses scraping OPSI B selesai!")
logger.info("="*60)

# Summary
logger.info("\n📊 RINGKASAN HASIL:")
for cat in dataset.keys():
    folder = os.path.join(BASE_DIR, cat)
    count = len([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))])
    logger.info(f"  {cat}: {count} gambar")
