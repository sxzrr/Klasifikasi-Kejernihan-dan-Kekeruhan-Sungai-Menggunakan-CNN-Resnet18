# QUICK START - Best Practice Pipeline

## 3 Simple Steps

### Step 1️⃣: Preprocess Data (10 menit)
```
File: 1_Preprocessing_NEW.ipynb
├── Load 233 original images
├── Split 70/15/15 FIRST
├── Augment ONLY training set (4x)
└── Output: data_processed_best_practice/
   └── 815 training + 35 val + 35 test
```

### Step 2️⃣: Train Model (pilih salah satu)
```
Option A - ResNet18 (cepat):
  File: 2_Training_ResNet18_NEW.ipynb
  Output: resnet18_final_best_practice.pth
  
Option B - XceptionNet (akurat):
  File: 2_Training_XceptionNet_NEW.ipynb
  Output: xceptionnet_final_best_practice.pth
```

### Step 3️⃣: Evaluate & Inference
```
Update existing notebooks:
├── 3_Evaluation.ipynb
└── 4_Inference.ipynb

Changes:
- Load from: data_processed_best_practice/
- Use models: *_best_practice.pth
```

---

## What's Different?

### ❌ OLD (Data Leakage Problem)
```
Augment first (1000 images) → Then split
Risk: Test set might have augmented versions of training data
Result: Metrics artificially high
```

### ✅ NEW (Correct Way)
```
Split first (163/35/35) → Then augment only training
Benefit: No data leakage, true metrics
Result: Realistic performance numbers
```

---

## File Guide

| File | Purpose | Status |
|------|---------|--------|
| `1_Preprocessing_NEW.ipynb` | Split & augment correctly | ✅ Ready |
| `2_Training_ResNet18_NEW.ipynb` | Train ResNet18 | ✅ Ready |
| `2_Training_XceptionNet_NEW.ipynb` | Train XceptionNet | ✅ Ready |
| `PREPROCESSING_CHANGES.md` | Technical details | 📖 Read |
| `BEST_PRACTICE_IMPLEMENTATION_GUIDE.md` | Full guide | 📖 Read |

---

## Expected Results

```
Metrics might be LOWER than before:
✅ That's CORRECT (no more inflated numbers)
✅ Shows real generalization ability
✅ Better for production deployment
```

---

## FAQ

**Q: Should I use new pipeline?**
A: YES! It's the correct way.

**Q: Can I keep old files?**
A: YES! Both exist for comparison.

**Q: Will training take longer?**
A: Slightly (815 training images vs 700), but worth it.

**Q: What if metrics are lower?**
A: That's GOOD! Means metrics are now HONEST.

---

## Start Here
👉 Open and run: **`1_Preprocessing_NEW.ipynb`** first!
