# 🚀 NEXT STEPS: Retrain Model with Expanded Dataset

## Overview
Now that we have 800 images (400 jernih + 400 keruh), we need to:
1. Update preprocessing for new dataset
2. Retrain the model
3. Evaluate improvements
4. Deploy new model

---

## STEP 1: Update 1_Preprocessing.ipynb

### What to Change
Find this line:
```python
dataset_root = Path("./dataset_sungai")
```

Change to:
```python
dataset_root = Path("./dataset_sungai_expanded")
```

### What Will Happen
- Loads all 800 images from expanded dataset
- Creates train/val/test split (70/15/15):
  - Train: ~560 images (increased from 143!)
  - Validation: ~120 images
  - Test: ~120 images
- Saves preprocessed data to: `data_processed_expanded/`

### Run the Notebook
1. Open `1_Preprocessing.ipynb`
2. Change the dataset path
3. Run all cells
4. Wait for preprocessing to complete (~1-2 minutes)

Expected output:
```
Train: 560 images
Validation: 120 images
Test: 120 images
Total: 800 images
```

---

## STEP 2: Update 2_Training_ResNet18.ipynb

### What to Change
Find this line:
```python
self.data_dir = Path("./data_processed/")
```

Change to:
```python
self.data_dir = Path("./data_processed_expanded/")
```

### Important: Use Original Configuration
✅ Keep the **ORIGINAL hyperparameters**:
- Stage 1: 5 epochs (frozen backbone)
- Stage 2: 20 epochs (fine-tuning)
- Learning rate: 0.0001
- Batch size: 16
- **NO weight decay**
- **NO early stopping**
- **NO augmentation during training**

### Why?
- Original config was already optimal for this architecture
- Larger dataset eliminates need for aggressive regularization
- More data = automatic regularization benefit

### Run the Training
1. Open `2_Training_ResNet18.ipynb`
2. Change the data directory path
3. **Ensure hyperparameters match original config**
4. Run all training cells
5. Wait for training (~30-40 minutes)

Expected output:
```
Stage 1 (5 epochs):
  Final Val Acc: ~85-88%

Stage 2 (20 epochs):
  Final Val Acc: ~92-95%
  Final Test Acc: 88-92% (↑ from 83.9%!)
```

---

## STEP 3: Evaluate New Model

### Run 3_Evaluation.ipynb
1. Ensure it uses the new model from Step 2
2. Run all evaluation cells
3. Check metrics

Expected results:
```
Test Accuracy: 88-92% (↑ +4-8%)
ROC-AUC: 0.88-0.92 (↑ from 0.846)
Turbidity Recall: >99% (perfect!)
Overfitting Gap: 5-8% (↓ from 16.1%)
```

### Compare with Original
| Metric | Original | Expected | Improvement |
|--------|----------|----------|------------|
| Test Accuracy | 83.9% | 88-92% | +4-8% |
| Val Accuracy | 93.5% | 91-94% | Similar |
| ROC-AUC | 0.846 | 0.88-0.92 | +0.03-0.07 |
| Overfitting Gap | 16.1% | 5-8% | Much Better |
| Turbidity Recall | 100% | >99% | Maintained |

---

## STEP 4: Save and Backup New Model

If new model is better (test acc > 85%):

```python
# Save new model
torch.save(model.state_dict(), "./models/resnet18_turbidity_expanded.pt")

# Backup original
# (Already done in backups/model_original_83.9_percent/)

# Document new model
with open("models/resnet18_turbidity_expanded_info.txt", "w") as f:
    f.write("""
Model: ResNet18 (Expanded Dataset)
Dataset: 800 images (400 jernih + 400 keruh)
Test Accuracy: [YOUR RESULT]%
Training Date: 2025-11-02
Framework: PyTorch 2.7.1
GPU: NVIDIA RTX 4070 Super
""")
```

---

## STEP 5: Update Inference (Optional)

Update `4_Inference.ipynb` to use new model:

```python
# Old
model_path = "./models/resnet18_turbidity.pt"

# New
model_path = "./models/resnet18_turbidity_expanded.pt"
```

---

## Expected Timeline

| Step | Time | Status |
|------|------|--------|
| 1. Preprocessing | 1-2 min | ⏳ Ready |
| 2. Training (5 epochs) | 3-5 min | ⏳ Ready |
| 3. Training (20 epochs) | 30-40 min | ⏳ Ready |
| 4. Evaluation | 1-2 min | ⏳ Ready |
| 5. Save & Backup | <1 min | ⏳ Ready |
| **Total** | **35-50 min** | ⏳ Ready |

---

## Troubleshooting

### Problem: Preprocessing fails with "File not found"
**Solution**: Verify path is correct:
```
F:\TA1\dataset_sungai_expanded\
├── jernih\ (400 files)
└── keruh\ (400 files)
```

### Problem: Training slower than before
**Solution**: Normal! More images = longer training. Should be ~3-4x duration.

### Problem: Test accuracy lower than expected
**Solution**: 
1. Check data is correctly loaded (560 train, 120 val, 120 test)
2. Verify hyperparameters match original config
3. Check GPU memory (should be fine with RTX 4070)

### Problem: CUDA out of memory
**Solution**: Reduce batch size 16→8 (not recommended, will slow training)

---

## Success Criteria

Model is ready for deployment when:
✅ Test Accuracy: ≥ 85% (preferably 88-92%)
✅ Validation Accuracy: ≥ 90%
✅ Turbidity Recall: > 95%
✅ Overfitting Gap: < 10%
✅ Training completes without errors

---

## Command Reference

### Run Preprocessing
```python
# In notebook
exec(open("1_Preprocessing.ipynb").read())
```

### Run Training
```python
# In notebook
exec(open("2_Training_ResNet18.ipynb").read())
```

### Check Expanded Dataset
```powershell
# PowerShell
Get-ChildItem "F:\TA1\dataset_sungai_expanded\jernih" | Measure-Object
Get-ChildItem "F:\TA1\dataset_sungai_expanded\keruh" | Measure-Object
```

### View Sample Augmentations
```
Open: F:\TA1\dataset_expansion_samples.png
```

---

## Important Notes

⚠️ **DO NOT**:
- Delete original dataset_sungai/ (backup)
- Use old data_processed/ for new training
- Change hyperparameters without reason

✅ **DO**:
- Use original hyperparameters (they're optimal!)
- Monitor training progress
- Save model regularly
- Document results
- Keep backup of new model after training

---

## Quick Start Template

```python
# 1_Preprocessing.ipynb - Change this line:
dataset_root = Path("./dataset_sungai_expanded")  # ← NEW

# 2_Training_ResNet18.ipynb - Change this line:
self.data_dir = Path("./data_processed_expanded/")  # ← NEW

# Keep all hyperparameters the same!
# Run → Evaluate → Compare
```

---

## Success! 🎉

After retraining, you should see:
- ✅ Test accuracy improvement: 83.9% → 88-92%
- ✅ Better generalization (smaller overfitting gap)
- ✅ More robust model for real-world deployment
- ✅ Production-ready performance

---

**Questions?** Check DATASET_EXPANSION_SUMMARY.md for details.

Last updated: November 2, 2025
Ready for retraining! 🚀
