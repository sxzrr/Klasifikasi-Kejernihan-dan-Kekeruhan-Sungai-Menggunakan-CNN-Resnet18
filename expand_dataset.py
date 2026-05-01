#!/usr/bin/env python3
"""
🌊 River Turbidity Dataset Expansion Script
Expand dataset from 204 → 800 images (400 jernih + 400 keruh)
Using advanced data augmentation techniques
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import random
import shutil
from tqdm import tqdm
import json
from datetime import datetime

# Configuration
DATASET_ROOT = r"F:\TA1\dataset_sungai"
OUTPUT_ROOT = r"F:\TA1\dataset_sungai_expanded"
TARGET_COUNT = 400
SEED = 42

# Set random seeds
random.seed(SEED)
np.random.seed(SEED)

class AugmentationPipeline:
    """Data augmentation using PIL and OpenCV"""
    
    @staticmethod
    def rotate(img):
        """Rotate image ±30 degrees"""
        angle = random.randint(-30, 30)
        return img.rotate(angle, expand=False, fillcolor='white')
    
    @staticmethod
    def flip(img):
        """Randomly flip horizontally or vertically"""
        if random.random() < 0.5:
            img = ImageOps.mirror(img)
        if random.random() < 0.3:
            img = ImageOps.flip(img)
        return img
    
    @staticmethod
    def color_jitter(img):
        """Adjust brightness, contrast, color"""
        if random.random() < 0.5:
            enhancer = ImageEnhance.Brightness(img)
            factor = random.uniform(0.8, 1.2)
            img = enhancer.enhance(factor)
        
        if random.random() < 0.5:
            enhancer = ImageEnhance.Contrast(img)
            factor = random.uniform(0.8, 1.2)
            img = enhancer.enhance(factor)
        
        if random.random() < 0.5:
            enhancer = ImageEnhance.Color(img)
            factor = random.uniform(0.8, 1.2)
            img = enhancer.enhance(factor)
        
        return img
    
    @staticmethod
    def blur(img):
        """Apply Gaussian blur"""
        if random.random() < 0.3:
            img = img.filter(Image.BLUR)
        return img
    
    @staticmethod
    def perspective_crop(img):
        """Apply slight perspective via crop-resize"""
        if random.random() < 0.4:
            width, height = img.size
            offset = random.randint(5, 20)
            
            crop_box = (
                random.randint(0, offset),
                random.randint(0, offset),
                width - random.randint(0, offset),
                height - random.randint(0, offset)
            )
            img = img.crop(crop_box)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        return img
    
    @staticmethod
    def apply_augmentations(img_pil):
        """Apply 2-4 random augmentations"""
        augmentations = [
            AugmentationPipeline.rotate,
            AugmentationPipeline.flip,
            AugmentationPipeline.color_jitter,
            AugmentationPipeline.blur,
            AugmentationPipeline.perspective_crop,
        ]
        
        num_augs = random.randint(2, 4)
        selected_augs = random.sample(augmentations, num_augs)
        
        for aug_func in selected_augs:
            img_pil = aug_func(img_pil)
        
        return img_pil


def augment_category(source_dir, target_dir, category_name, target_total):
    """Augment images in a category"""
    image_files = [f for f in os.listdir(source_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    current_count = len(image_files)
    augmentations_needed = target_total - current_count
    
    print(f"\n📸 Processing {category_name}:")
    print(f"   Current: {current_count} images")
    print(f"   Need: +{augmentations_needed} augmented images")
    print(f"   Total target: {target_total} images")
    
    # Step 1: Copy originals
    print(f"\n   Step 1: Copying original images...")
    for idx, img_file in enumerate(image_files, 1):
        src = os.path.join(source_dir, img_file)
        dst = os.path.join(target_dir, f"{category_name}_000_{idx:03d}.jpg")
        shutil.copy2(src, dst)
    print(f"   ✅ Copied {current_count} original images")
    
    # Step 2: Generate augmented images
    print(f"\n   Step 2: Generating augmented images...")
    aug_count = 0
    aug_idx = 1
    
    with tqdm(total=augmentations_needed, desc=f"   Augmenting {category_name}", unit="img") as pbar:
        while aug_count < augmentations_needed:
            try:
                img_file = random.choice(image_files)
                img_path = os.path.join(source_dir, img_file)
                
                # Load and augment
                img_pil = Image.open(img_path).convert('RGB')
                aug_img_pil = AugmentationPipeline.apply_augmentations(img_pil)
                
                # Save
                save_path = os.path.join(target_dir, f"{category_name}_aug_{aug_idx:03d}.jpg")
                aug_img_pil.save(save_path, quality=95)
                
                aug_count += 1
                aug_idx += 1
                pbar.update(1)
            
            except Exception as e:
                print(f"   ⚠️  Error processing {img_file}: {e}")
                continue
    
    final_count = len(os.listdir(target_dir))
    print(f"   ✅ Complete! Final count: {final_count}")
    return final_count


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("🌊 RIVER TURBIDITY DATASET EXPANSION")
    print("="*70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create output directories
    jernih_source = os.path.join(DATASET_ROOT, "jernih")
    keruh_source = os.path.join(DATASET_ROOT, "keruh")
    jernih_target = os.path.join(OUTPUT_ROOT, "jernih")
    keruh_target = os.path.join(OUTPUT_ROOT, "keruh")
    
    os.makedirs(jernih_target, exist_ok=True)
    os.makedirs(keruh_target, exist_ok=True)
    
    # Count original images
    orig_jernih = len([f for f in os.listdir(jernih_source) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))])
    orig_keruh = len([f for f in os.listdir(keruh_source) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))])
    
    print(f"\n📊 Original Dataset:")
    print(f"   Jernih (Clear): {orig_jernih} images")
    print(f"   Keruh (Turbid): {orig_keruh} images")
    print(f"   Total: {orig_jernih + orig_keruh} images")
    
    print(f"\n🎯 Target Dataset:")
    print(f"   Jernih (Clear): {TARGET_COUNT} images")
    print(f"   Keruh (Turbid): {TARGET_COUNT} images")
    print(f"   Total: {TARGET_COUNT * 2} images")
    
    print(f"\n🔧 Augmentation Settings:")
    print(f"   Rotation: ±30°")
    print(f"   Flip: Horizontal + Vertical")
    print(f"   Color Jitter: Brightness, Contrast, Saturation")
    print(f"   Blur: Gaussian")
    print(f"   Perspective: Crop-Resize")
    print(f"   Augmentations per image: 2-4 random")
    
    print(f"\n" + "="*70)
    
    # Augment jernih
    final_jernih = augment_category(jernih_source, jernih_target, "jernih", TARGET_COUNT)
    
    print(f"\n" + "-"*70)
    
    # Augment keruh
    final_keruh = augment_category(keruh_source, keruh_target, "keruh", TARGET_COUNT)
    
    print(f"\n" + "="*70)
    print(f"\n✅ DATASET EXPANSION COMPLETE!\n")
    
    # Final statistics
    print(f"📊 EXPANSION RESULTS:")
    print(f"\n   Jernih (Clear):")
    print(f"   • Before: {orig_jernih} images")
    print(f"   • After: {final_jernih} images")
    print(f"   • Multiplier: {final_jernih/orig_jernih:.1f}x")
    
    print(f"\n   Keruh (Turbid):")
    print(f"   • Before: {orig_keruh} images")
    print(f"   • After: {final_keruh} images")
    print(f"   • Multiplier: {final_keruh/orig_keruh:.1f}x")
    
    print(f"\n   Overall:")
    print(f"   • Before: {orig_jernih + orig_keruh} images")
    print(f"   • After: {final_jernih + final_keruh} images")
    print(f"   • Growth: +{final_jernih + final_keruh - orig_jernih - orig_keruh} images")
    print(f"   • Multiplier: {(final_jernih + final_keruh)/(orig_jernih + orig_keruh):.1f}x")
    
    # Dataset size
    jernih_size = sum(os.path.getsize(os.path.join(jernih_target, f)) for f in os.listdir(jernih_target)) / (1024*1024)
    keruh_size = sum(os.path.getsize(os.path.join(keruh_target, f)) for f in os.listdir(keruh_target)) / (1024*1024)
    total_size = jernih_size + keruh_size
    
    print(f"\n💾 STORAGE:")
    print(f"   Jernih: {jernih_size:.1f} MB")
    print(f"   Keruh: {keruh_size:.1f} MB")
    print(f"   Total: {total_size:.1f} MB")
    
    print(f"\n📁 Output Location:")
    print(f"   {OUTPUT_ROOT}")
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"   1. Update 1_Preprocessing.ipynb to use dataset_sungai_expanded/")
    print(f"   2. Run preprocessing to create preprocessed_expanded/")
    print(f"   3. Update 2_Training_ResNet18.ipynb to use expanded dataset")
    print(f"   4. Retrain model (expect 88-92% accuracy)")
    
    print(f"\n✨ End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    # Save metadata
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "original_jernih": orig_jernih,
        "original_keruh": orig_keruh,
        "expanded_jernih": final_jernih,
        "expanded_keruh": final_keruh,
        "target_count": TARGET_COUNT,
        "total_size_mb": round(total_size, 1),
        "seed": SEED
    }
    
    with open(os.path.join(OUTPUT_ROOT, "expansion_metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return final_jernih, final_keruh


if __name__ == "__main__":
    main()
