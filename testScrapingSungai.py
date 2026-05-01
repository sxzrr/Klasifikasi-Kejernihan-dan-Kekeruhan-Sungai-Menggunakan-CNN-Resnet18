# scrape_sungai_icrawler.py
# By Firman Firdaus (OPTIMIZED UNTUK HASIL MAKSIMAL - FOKUS KUALITAS BUKAN KECEPATAN)
# Mengambil referensi dari JATI (Jurnal Mahasiswa Teknik Informatika) Vol.9 No.3 Juni 2025
#
# IMPROVEMENT UNTUK TARGET 300+ GAMBAR PER KATEGORI:
# ✅ 25 keywords per kategori (50 total)
# ✅ max_num = 800 (lebih banyak attempts)
# ✅ downloader_threads = 5 (parallel download)
# ✅ delay 8-15 detik antar keyword
# ✅ delay 20-30 detik antar kategori
# ✅ retry logic dengan 2 kali percobaan
# ✅ Timeout 30 detik untuk koneksi stabil
# ✅ User agent rotation untuk bypass detection
# ✅ Better header handling (Connection, Pragma, Cache-Control)

import os
import time
import logging
from icrawler.builtin import GoogleImageCrawler
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
# 1️⃣ Daftar keyword per kelas (diperluas dengan variations)
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
        
        # === KEYWORDS LAMA (UNCOMMENT JIKA INGIN DIGUNAKAN) ===
        # "sungai jernih",
        # "clear river water",
        # "air sungai bening",
        # "mountain stream clear",
        # "crystal clear river",
        # "sungai yang bersih",
        # "clear flowing river",
        # "transparent water river",
        # "jernih bening river",
        # "clear water stream indonesia",
        # "sungai air bersih",
        # "clean river water",
        # "river clear water flowing",
        # "clear river indonesia",
        # "water transparent bening",
        # "sungai air jernih mengalir",
        # "clean clear water stream",
        # "beautiful clear river",
        # "pristine clear water",
        # "river crystal water",
        # "sungai dengan air jernih",
        # "clear blue river water",
        # "transparent flowing water",
        # "jernih air sungai",
        # "clean flowing water stream",
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
        
        # === KEYWORDS LAMA (UNCOMMENT JIKA INGIN DIGUNAKAN) ===
        # "sungai keruh",
        # "muddy river water",
        # "turbid river water",
        # "polluted brown river",
        # "dirty river water",
        # "sungai yang kotor",
        # "murky river water",
        # "brown muddy river",
        # "turbid muddy water",
        # "sungai keruh berlumpur",
        # "polluted water river",
        # "dirty muddy river",
        # "river muddy water flowing",
        # "turbid water indonesia",
        # "murky dirty water",
        # "sungai air keruh berlumpur",
        # "brown polluted river water",
        # "muddy turbid water stream",
        # "dirty murky water",
        # "river pollution muddy",
        # "sungai dengan air keruh",
        # "brown muddy river water",
        # "turbid flowing water",
        # "keruh berlumpur air sungai",
        # "polluted muddy water stream",
    ]
}

# ======================================================
# 2️⃣ Folder output
# ======================================================
BASE_DIR = "datasetScrap3"
os.makedirs(BASE_DIR, exist_ok=True)

# ======================================================
# 3️⃣ Loop scraping per kelas dan keyword (dengan retry logic)
# ======================================================
for label, keywords in dataset.items():
    folder_path = os.path.join(BASE_DIR, label)
    os.makedirs(folder_path, exist_ok=True)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"🎯 Scraping category: {label.upper()}")
    logger.info(f"{'='*60}")

    # Membuat instance crawler dengan setting yang better
    crawler = GoogleImageCrawler(
        storage={"root_dir": folder_path},
        downloader_threads=2,  # OPSI A: Kurangi ke 2 threads (lebih stabil, bypass bot detection)
    )

    # ======================================================
    # 4️⃣ Jalankan crawling untuk tiap keyword dengan delay dan retry
    # ======================================================
    for idx, keyword in enumerate(keywords, 1):
        retry_count = 0
        max_retries = 2  # Retry hingga 2 kali jika ada error
        
        while retry_count <= max_retries:
            try:
                logger.info(f"\n[{idx}/{len(keywords)}] 🔍 '{keyword}'" + (f" (Retry {retry_count})" if retry_count > 0 else ""))
                
                # Rotate user agent untuk setiap keyword
                random_ua = random.choice(USER_AGENTS)
                crawler.downloader.session.headers.update({
                    "User-Agent": random_ua,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Referer": "https://www.google.com/",
                    "Connection": "keep-alive",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                })
                
                # Set timeout yang lebih lama untuk koneksi yang lebih stabil
                crawler.downloader.session.timeout = 30
                
                crawler.crawl(
                    keyword=keyword,
                    max_num=800,              # Maksimal attempts untuk hasil terbaik
                    min_size=(200, 200),      # ukuran minimum
                    max_size=(1920, 1080)     # ukuran maksimum
                )
                
                logger.info(f"✅ Selesai: {keyword}")
                break  # Jika berhasil, keluar dari retry loop
            
            except KeyboardInterrupt:
                logger.warning("❌ Scraping dihentikan oleh user")
                raise
            except Exception as e:
                retry_count += 1
                error_msg = str(e)[:100]
                if retry_count <= max_retries:
                    logger.warning(f"⚠️ Error pada '{keyword}': {error_msg} - Retry {retry_count}/{max_retries}")
                    time.sleep(random.uniform(10, 15))  # Tunggu lebih lama sebelum retry
                else:
                    logger.error(f"❌ Gagal setelah {max_retries} kali retry: {error_msg}")
                    break
            
            # Jika sudah mencoba, tunggu lebih lama sebelum keyword berikutnya
            if retry_count > 0 and retry_count <= max_retries:
                continue
        
        # Delay PENTING antar keyword untuk hindari bot detection
        delay = random.uniform(20, 40)  # OPSI A: Naikkan ke 20-40 detik (lebih strategic)
        logger.info(f"⏳ Menunggu {delay:.1f} detik sebelum keyword berikutnya...")
        time.sleep(delay)

    logger.info(f"\n📁 Semua gambar untuk kelas '{label}' tersimpan di: {folder_path}")
    
    # Delay PENTING antar kategori untuk hindari bot detection
    # Jangan dikurangi - lebih lama lebih baik untuk hasil maksimal
    logger.info("⏳ Menunggu LAMA sebelum scraping kategori berikutnya (jangan di interrupt)...")
    time.sleep(random.uniform(60, 90))  # OPSI A: Naikkan ke 60-90 detik (lebih efektif bypass detection)

logger.info("\n" + "="*60)
logger.info("🎉 Semua proses scraping selesai!")
logger.info("="*60)

# Summary
logger.info("\n📊 RINGKASAN HASIL:")
for cat in dataset.keys():
    folder = os.path.join(BASE_DIR, cat)
    count = len([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))])
    logger.info(f"  {cat}: {count} gambar")
