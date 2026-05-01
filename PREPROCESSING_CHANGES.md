# Preprocessing Changes - Best Practice Implementation

## Summary
Rombak preprocessing pipeline untuk mengikuti best practice: **Split FIRST, Augmentasi HANYA training set**.

## What Changed

### BEFORE (Data Leakage Risk ❌)
```
1. Load 233 original images
2. Augment all 233 images → 1000 images
3. Split 1000 images into train/val/test (70/15/15)
   - Problem: Test set bisa berisi augmented version dari training images!
```

### AFTER (Best Practice ✅)
```
1. Load 233 original images
2. Split into train/val/test FIRST (70/15/15)
   - Train: 163 images (original only)
   - Val:   35 images (original only)
   - Test:  35 images (original only)
3. Augment ONLY training set (4x augmentation)
   - Result: 163 + (163×4) = 815 training images
   - Val & Test: UNCHANGED (35 each)
```

## Benefits

| Aspect | Before | After |
|--------|--------|-------|
| Data Leakage | ⚠️ Risk | ✅ None |
| Test Eval | Inflated | True |
| Val Eval | Inflated | True |
| Training Data | 700 aug | 815 aug |
| Pipeline | Risky | Industry Standard |

## File Changes

### New Files
- `1_Preprocessing_NEW.ipynb` - New best-practice preprocessing pipeline

### Output Structure
```
data_processed_best_practice/
├── train/
│   ├── images.npy (815, 224, 224, 3) - Original + Augmented
│   └── labels.npy (815,)
├── val/
│   ├── images.npy (35, 224, 224, 3) - Original ONLY
│   └── labels.npy (35,)
├── test/
│   ├── images.npy (35, 224, 224, 3) - Original ONLY
│   └── labels.npy (35,)
└── metadata.json
```

## Training Adjustment Needed

Update training notebooks to:
1. Load from `data_processed_best_practice/` instead of `data_processed/`
2. No need for additional augmentation during training (already done!)
3. Models should converge faster due to larger training set (815 vs 700)

## Next Steps

1. Run `1_Preprocessing_NEW.ipynb` to generate new preprocessed data
2. Update `2_Model_Training.ipynb` to load from new directory
3. Re-train models (should see same or better results)
4. Update evaluation with new test set

## Important Notes

- ✅ Validation & Test sets NEVER touched with augmentation
- ✅ Training set has 4.3× expansion for better generalization
- ✅ No data leakage between train/val/test splits
- ✅ Follows industry best practices
- ✅ Reproducible with `random_state=42`

## Augmentation Techniques Applied (Train Only)
- RandomResizedCrop (224×224, scale 0.8-1.0)
- HorizontalFlip (50%)
- VerticalFlip (50%)
- Rotate (±15°)
- ColorJitter (brightness, contrast, saturation)
- Affine (scale & translate)
