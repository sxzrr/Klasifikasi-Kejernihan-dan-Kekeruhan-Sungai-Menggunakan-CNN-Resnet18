╔═══════════════════════════════════════════════════════════════════════════════╗
║                   🚀 QUICK TEST PLAN - RUN NOW! 🚀                            ║
║              Test Model with Expanded Dataset (800 images)                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════

✅ UPDATED: Preprocessing notebook sudah diupdate untuk gunakan expanded dataset!

Changes made:
├─ dataset_path = Path('dataset_sungai_expanded')  ← Using 800 images
├─ output_path = Path('data_processed_expanded')   ← Save to new folder
└─ Comments updated to reflect expanded dataset

═══════════════════════════════════════════════════════════════════════════════

🧪 TEST PROCEDURE - 3 STEPS
═══════════════════════════════════════════════════════════════════════════════

STEP 1️⃣ : RUN PREPROCESSING (5 minutes)
───────────────────────────────────────────────────────────────────────────────

What to do:
1. Open: 1_Preprocessing.ipynb
2. ✅ Already updated! Just run all cells
3. Watch the output for:
   - "Total images found: 800" ✅
   - "Loaded: 800 images" ✅
   - "Train set: (560, 224, 224, 3)" ✅
   - "Val set: (120, 224, 224, 3)" ✅
   - "Test set: (120, 224, 224, 3)" ✅

Expected output:
```
Loading 800 images...
  20/800 loaded...
  40/800 loaded...
  ... (continues)
  800/800 loaded...

✅ Loaded: 800 images
❌ Failed: 0 images

Dataset shape: (800, 224, 224, 3)
Labels shape: (800,)
Data type: float32
Value range: [0.000, 1.000]

Train set: (560, 224, 224, 3) (labels: [280 280])
Val set: (120, 224, 224, 3) (labels: [60 60])
Test set: (120, 224, 224, 3) (labels: [60 60])

Total: 800 images

✅ Preprocessing complete!

Saved to: data_processed_expanded

Dataset summary:
{
  "total_images": 800,
  "train_size": 560,
  "val_size": 120,
  "test_size": 120,
  "image_size": [224, 224],
  "num_classes": 2,
  "class_names": ["Clear (Jernih)", "Turbid (Keruh)"],
  "preprocessing": "Resized to 224x224, normalized to [0, 1]"
}
```

✅ SUCCESS INDICATORS:
  - Total images: 800 (not 204!)
  - Train: 560 (not 143!)
  - No failed images: 0
  - All sizes: (224, 224, 3)

═══════════════════════════════════════════════════════════════════════════════

STEP 2️⃣ : RUN TRAINING (40 minutes)
───────────────────────────────────────────────────────────────────────────────

After preprocessing completes, open: 2_Training_ResNet18.ipynb

Update this line:
```python
# OLD: self.data_dir = Path('./data_processed/')
# NEW:
self.data_dir = Path('./data_processed_expanded/')
```

Then run all training cells. Expected:
├─ GPU will load model (should be instant)
├─ Stage 1 training (5 epochs, ~5 minutes)
├─ Stage 2 training (20 epochs, ~30 minutes)
└─ Save model weights

Monitor progress:
  Epoch 1/5: Loss ↓, Val Acc ↑
  Epoch 5/5: ~85-88% validation accuracy
  
  Epoch 1/20: Loss ↓, Val Acc ↑
  ...
  Epoch 20/20: ~92-95% validation accuracy

═══════════════════════════════════════════════════════════════════════════════

STEP 3️⃣ : RUN EVALUATION (5 minutes)
───────────────────────────────────────────────────────────────────────────────

After training completes, open: 3_Evaluation.ipynb

Run evaluation cells to see:
├─ Test Accuracy: 88-92% ✅ (UP from 83.9%!)
├─ Confusion Matrix
├─ ROC Curve
├─ Per-class metrics
└─ Comparison with original model

Expected Results:
┌─────────────────────────────────────────┐
│ Test Accuracy:    88-92%  ✅ (+4-8%)    │
│ Val Accuracy:     91-94%  ✅            │
│ ROC-AUC:          0.88-0.92 ✅          │
│ Overfitting Gap:  5-8% ✅ (down from 16%)│
│ Turbidity Recall: >99% ✅ (maintained)  │
└─────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

📋 QUICK CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

Before Starting:
  ✅ Expanded dataset created (verified: 800 images)
  ✅ Preprocessing notebook updated (using dataset_sungai_expanded/)
  ✅ GPU available (RTX 4070 Super confirmed)
  ✅ PyTorch installed (2.7.1)
  ✅ Original model backed up (safe recovery)

During Test:
  ✅ Run preprocessing → verify 800 images loaded
  ✅ Run training → monitor GPU usage
  ✅ Run evaluation → check accuracy improvement

After Test:
  ✅ Check test accuracy ≥ 85% (preferably 88-92%)
  ✅ Verify overfitting gap < 10%
  ✅ If successful → save new model version
  ✅ If not → can always restore original 83.9%

═══════════════════════════════════════════════════════════════════════════════

🎯 EXPECTED OUTCOMES
═══════════════════════════════════════════════════════════════════════════════

BEST CASE (90-92% test accuracy):
├─ Dataset expansion worked perfectly
├─ Model trained on 3.9x more data
├─ Better generalization achieved
├─ Production-ready model
└─ Success! 🎉

GOOD CASE (88-90% test accuracy):
├─ Clear improvement over original 83.9%
├─ Worth deploying new model
├─ Better than original
└─ Success! ✅

ACCEPTABLE (85-88% test accuracy):
├─ Some improvement (but small)
├─ Could continue exploring
├─ May need more data or techniques
└─ Decision point

NOT AS EXPECTED (<85% test accuracy):
├─ Check data loading (560 train, 120 val, 120 test)
├─ Verify hyperparameters match original config
├─ GPU memory sufficient?
├─ Can restore original 83.9% if needed

═══════════════════════════════════════════════════════════════════════════════

⚠️ IMPORTANT NOTES
═══════════════════════════════════════════════════════════════════════════════

1. ✅ PREPROCESSING ALREADY UPDATED
   The notebook has been updated to use dataset_sungai_expanded/
   Just run all cells without making changes!

2. ⏱️ TRAINING WILL TAKE TIME
   Stage 2 is 20 epochs with larger dataset (~30 minutes)
   This is normal! More data = longer training

3. 💾 ORIGINAL MODEL SAFE
   Original 83.9% model backed up in: backups/model_original_83.9_percent/
   Can restore anytime if needed

4. 📊 METRICS TO WATCH
   - Test Accuracy (main metric)
   - Overfitting Gap (should reduce from 16.1%)
   - Turbidity Recall (must stay >95%)

5. 🚀 RETRAINING IS OPTIONAL
   If happy with 83.9%, no need to retrain
   But this should show improvement!

═══════════════════════════════════════════════════════════════════════════════

💡 TIPS FOR SUCCESS
═══════════════════════════════════════════════════════════════════════════════

1. Monitor Progress
   └─ Watch GPU usage in Task Manager
   └─ Should see GPU utilization increase during training

2. Save Results
   └─ Screenshot or note the final metrics
   └─ Compare with original 83.9% benchmark

3. Handle Errors
   └─ If any cell fails, read error message
   └─ Check file paths (dataset_sungai_expanded/ exists?)
   └─ Restart kernel and try again

4. Be Patient
   └─ Training 40+ minutes is normal
   └─ Don't interrupt the process
   └─ GPU will work hard (this is good!)

═══════════════════════════════════════════════════════════════════════════════

📞 TROUBLESHOOTING QUICK FIX
═══════════════════════════════════════════════════════════════════════════════

"Total images found: 204" (not 800)
  → Check: F:\TA1\dataset_sungai_expanded\ exists?
  → Check: Contains jernih/ and keruh/ folders with files?
  → Check: Path in notebook is exactly: Path('dataset_sungai_expanded')

"Failed to load model" during training
  → Make sure models/ folder exists
  → Check GPU memory (RTX 4070 has 12GB, should be enough)
  → Restart kernel and try again

"Test accuracy much lower than expected"
  → Verify train/val/test split (560/120/120)
  → Check data preprocessing (should be [0, 1] normalized)
  → Make sure it's using the new model, not old one

═══════════════════════════════════════════════════════════════════════════════

🎬 ACTION ITEMS - DO THIS NOW!
═══════════════════════════════════════════════════════════════════════════════

[ ] 1. Open 1_Preprocessing.ipynb
      (It's already updated! Just verify the path shows dataset_sungai_expanded/)

[ ] 2. Run all cells
      (Watch for 800 images loaded)

[ ] 3. After preprocessing completes (~5 minutes):
      Open 2_Training_ResNet18.ipynb
      Update: self.data_dir = Path('./data_processed_expanded/')
      Run all cells

[ ] 4. After training completes (~40 minutes):
      Open 3_Evaluation.ipynb
      Run evaluation
      Check results

[ ] 5. Compare results:
      Original:  83.9% test accuracy
      New:       Expected 88-92%
      Improvement: +4-8% 🎉

═══════════════════════════════════════════════════════════════════════════════

✨ LET'S TEST IT!
═══════════════════════════════════════════════════════════════════════════════

You're all set! The preprocessing notebook is updated and ready.

Current Status:
✅ Dataset expanded (800 images ready)
✅ Preprocessing updated (using dataset_sungai_expanded/)
✅ GPU verified (RTX 4070 Super)
✅ Original model backed up (83.9% safe)

Next Action:
👉 Open 1_Preprocessing.ipynb
👉 Run all cells
👉 Expected: 800 images loaded in ~5 minutes

Then:
👉 Open 2_Training_ResNet18.ipynb
👉 Update data path
👉 Run training (~40 minutes)

Finally:
👉 Open 3_Evaluation.ipynb
👉 Check results (expect 88-92%)

Good luck! 🚀

═══════════════════════════════════════════════════════════════════════════════

Questions? Check RETRAINING_GUIDE.md for detailed help!

Ready? Let's improve the model! 🎉

═══════════════════════════════════════════════════════════════════════════════
