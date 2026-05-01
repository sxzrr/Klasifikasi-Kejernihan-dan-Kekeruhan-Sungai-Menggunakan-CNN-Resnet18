#!/usr/bin/env python3
"""
Script untuk menjalankan full scraping dengan single query optimized
"""

from testScrapingSungai import RiverImageScraper

print('\n' + '='*70)
print('🚀 STARTING OPTIMIZED FULL SCRAPING')
print('='*70)
print('Method: Single Query per Category')
print('Target: 200 images jernih + 200 images keruh')
print('Expected: ~400 images total')
print('='*70)

# Initialize scraper
scraper = RiverImageScraper('f:\\TA1\\datasetScrap3')

# Run full scraping dengan target 200 per kategori
results = scraper.scrape_all(max_num_per_category=200)

print('\n' + '='*70)
print('✅ SCRAPING COMPLETE!')
print('='*70)
print(f'Jernih: {results["jernih"]} images')
print(f'Keruh: {results["keruh"]} images')
print(f'TOTAL: {sum(results.values())} images')
print('='*70)
print(f'\n📁 Images saved to: f:\\TA1\\datasetScrap3\\')
print('='*70)
