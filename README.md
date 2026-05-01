# 🌊 River Turbidity Classification with PyTorch & ResNet18# River Turbidity Classification with PyTorch & ResNet18# 🌊 River Turbidity Detection - CNN Xception Model



## 📋 Project Overview



Binary classification model to detect river water turbidity (clarity):## 📋 Project OverviewProyek untuk deteksi kekeruhan sungai menggunakan Deep Learning (Xception Transfer Learning)

- **Clear (Jernih)**: Clean, transparent water

- **Turbid (Keruh)**: Muddy, cloudy water



**Model**: ResNet18 (Pre-trained on ImageNet, fine-tuned for turbidity)  Binary classification model to detect river water turbidity (clarity):## 📊 Dataset

**Framework**: PyTorch with GPU acceleration  

**GPU**: NVIDIA RTX 4070 Super (12GB VRAM)  - **Clear (Jernih)**: 清水/透明水体- **Sumber**: Google Image Search via icrawler

**Dataset**: 204 images (95 clear, 109 turbid)

- **Turbid (Keruh)**: 浑浊水体- **Kategori**: 

---

  - `keruh` (Turbid/Muddy): Sungai keruh dengan air kotor

## 🚀 Quick Start

**Model**: ResNet18 (Pre-trained on ImageNet, fine-tuned for turbidity)    - `jernih` (Clear): Sungai jernih dengan air bersih

### 1. Activate Environment

```powershell**Framework**: PyTorch  - **Target**: 500 gambar per keyword × 5 keywords × 2 kategori = ~5000 gambar

cd f:\TA1

.\venv\Scripts\Activate.ps1**GPU**: NVIDIA RTX 4070 Super (12GB VRAM)  - **Format**: JPG, PNG, GIF, BMP, WebP

```

**Dataset**: 204 images (95 clear, 109 turbid)- **Resolusi**: 200×200 hingga 1920×1080 px

### 2. Open Jupyter Notebooks

```powershell

jupyter notebook

```---## 🏗️ Struktur Proyek



### 3. Run Notebooks in Order

1. **1_Preprocessing.ipynb** - Load & process dataset

2. **2_Training_ResNet18.ipynb** - Train model with GPU (15-30 min)## 🚀 Quick Start```

3. **3_Evaluation.ipynb** - Test & generate metrics

4. **4_Inference.ipynb** - Predict on new imagesF:\TA1\



---### 1. Activate Environment├── dataset_sungai/              # Raw dataset dari scraper



## 📁 Project Structure```powershell│   ├── keruh/                   # Gambar sungai keruh



```cd f:\TA1│   └── jernih/                  # Gambar sungai jernih

f:\TA1\

├── 1_Preprocessing.ipynb.\venv_tf210\Scripts\Activate.ps1│

├── 2_Training_ResNet18.ipynb

├── 3_Evaluation.ipynb```├── data_processed/              # Processed dataset (299×299)

├── 4_Inference.ipynb

├── README.md│   ├── train/                   # 70% dari setiap kategori

│

├── dataset_sungai/          (204 raw images)### 2. Open Jupyter Notebooks│   │   ├── keruh/

├── data_processed/          (Preprocessed data)

├── models/                  (Trained model weights)```powershell│   │   └── jernih/

├── logs/                    (Training metrics & plots)

├── Test Scraping/           (Web scraper)jupyter notebook│   ├── val/                     # 15% dari setiap kategori

└── venv/                    (Virtual environment)

``````│   │   ├── keruh/



---│   │   └── jernih/



## 🔧 Model Architecture### 3. Run Notebooks in Order│   └── test/                    # 15% dari setiap kategori



**ResNet18 + Custom Classification Head**1. **1_Preprocessing.ipynb** - Load & process dataset (run once)│       ├── keruh/

- Pre-trained ImageNet backbone

- Custom head: Linear(512→256) → ReLU → Dropout → Linear(256→2)2. **2_Training_ResNet18.ipynb** - Train model with GPU (15-30 min)│       └── jernih/

- 2-stage training:

  - Stage 1: Frozen backbone (5 epochs, lr=0.001)3. **3_Evaluation.ipynb** - Test & generate metrics│

  - Stage 2: Fine-tune all layers (20 epochs, lr=0.0001)

4. **4_Inference.ipynb** - Predict on new images├── models/                      # Saved models

---

│   ├── xception_model.keras    # Best model

## 💻 GPU Setup

---│   └── model_weights.h5        # Model weights

**Verified**: ✅ PyTorch 2.7.1 + CUDA 11.8

- GPU: NVIDIA RTX 4070 Super│

- VRAM: 12.88 GB

- Status: Ready for training## 📁 Project Structure├── scripts/                     # Python scripts



---│   ├── preprocessing.py         # Dataset preprocessing



## 📊 Expected Performance```│   ├── setup_dependencies.py    # Install dependencies



- Test Accuracy: ~82-85%f:\TA1\│   ├── train_model.py          # Model training

- ROC AUC: ~0.90

- Training time: 15-30 min (GPU)├── 1_Preprocessing.ipynb              ← Load & resize images│   ├── predict.py              # Inference/prediction



---├── 2_Training_ResNet18.ipynb          ← Train model (GPU)│   └── evaluate_model.py        # Model evaluation



## 🐛 Troubleshooting├── 3_Evaluation.ipynb                 ← Test & metrics│



**GPU not detected?**├── 4_Inference.ipynb                  ← Predict new images├── notebooks/                   # Jupyter notebooks (optional)

```powershell

.\venv\Scripts\python.exe -c "import torch; print(torch.cuda.is_available())"││   └── exploration.ipynb       # Data exploration & visualization

```

├── dataset_sungai/                    ← Raw images (204 total)│

**OutOfMemory?**

Reduce batch size from 16 to 8 in training notebook│   ├── keruh/                         ← Turbid images (109)├── logs/                        # Training logs



---│   └── jernih/                        ← Clear images (95)│   ├── training_log.txt



**Status**: ✅ Ready to Use││   ├── preprocessing_log.txt


├── data_processed/                    ← Preprocessed normalized data│   ├── training_history.csv

│   ├── train/                         ← 70% (142 images)│   ├── evaluation_results.json

│   ├── val/                           ← 15% (31 images)│   └── tensorboard/            # TensorBoard logs

│   ├── test/                          ← 15% (31 images)│

│   └── metadata.json                  ← Dataset info├── Test Scraping/

││   └── testScrapingSungai.py    # Web scraper

├── models/│

│   ├── resnet18_turbidity.pt          ← Trained model weights└── README.md                    # This file

│   └── xception_final.keras           ← Previous model (reference)```

│

├── logs/## 🚀 Quick Start

│   ├── training_history_*.json        ← Training metrics

│   ├── evaluation_results.json        ← Test metrics### 1. Setup Environment & Install Dependencies

│   ├── batch_predictions.csv          ← Inference results

│   ├── training_curves.png            ← Loss & accuracy plots```bash

│   ├── confusion_matrix.png           ← Test predictionscd f:\TA1

│   ├── roc_curve.png                  ← ROC analysis

│   └── sample_predictions.png         ← Sample inferences# Install dependencies

│python scripts/setup_dependencies.py

├── Test Scraping/```

│   └── testScrapingSungai.py          ← Web scraper (collect images)

│**Output yang diharapkan:**

└── venv_tf210/                        ← Virtual environment```

    └── (PyTorch, CUDA 11.8, etc.)✓ tensorflow installed successfully

```✓ keras installed successfully

...

---✓ GPU detected: 1 GPU(s) found

  GPU 0: PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')

## 🔧 Model Architecture✓ CUDA available: True

```

### ResNet18 + Custom Head

- **Backbone**: ResNet18 (pre-trained ImageNet)### 2. Preprocess Dataset

- **Feature extraction**: Layer4 → AdaptiveAvgPool (512 channels)

- **Classification head**:```bash

  - Linear(512 → 256)python scripts/preprocessing.py

  - ReLU + Dropout(0.5)```

  - Linear(256 → 2)  # [Clear, Turbid]

**What it does:**

### Training Strategy (2-Stage)- Resize semua gambar ke 299×299 (format Xception)

- Split ke train/val/test (70/15/15)

**Stage 1: Frozen Backbone (5 epochs)**- Simpan di `data_processed/`

- Only train custom head

- Learning rate: 0.001**Output:**

- Prevents catastrophic forgetting```

RINGKASAN DATASET SETELAH PREPROCESSING

**Stage 2: Fine-tuning (20 epochs)**

- Train entire networkTRAIN:

- Learning rate: 0.0001 (lower, with scheduler)  - keruh: 329

- Adaptive learning rate reduction on plateau  - jernih: 284

  Total: 613

---

VAL:

## 📊 Expected Performance  - keruh: 70

  - jernih: 61

| Metric | Value |  Total: 131

|--------|-------|

| Test Accuracy | ~82-85% |TEST:

| Precision (Turbid) | ~0.85 |  - keruh: 70

| Recall (Turbid) | ~0.80 |  - jernih: 61

| ROC AUC | ~0.90 |  Total: 131

```

*(Baseline Xception achieved 80.65% on CPU in 6-7 hours)*

### 3. Train Model

---

```bash

## 💻 GPU Accelerationpython scripts/train_model.py

```

**PyTorch GPU Verification**:

```python**Training Strategy:**

import torch- **Stage 1** (20 epochs): Base model frozen

print(torch.cuda.is_available())        # True- **Stage 2** (80 epochs): Fine-tuning dengan base model unfrozen

print(torch.cuda.device_count())        # 1- **Total**: ~100 epochs

print(torch.cuda.get_device_name(0))    # NVIDIA GeForce RTX 4070 Super

```**Callbacks:**

- Early Stopping (patience=10)

**Expected Training Time**:- Model Checkpoint (save best model)

- Preprocessing: 1-2 minutes- ReduceLROnPlateau

- Training: 15-30 minutes (GPU) vs 6-7 hours (CPU)- TensorBoard logging

- Evaluation: 1-2 minutes

- Inference on 204 images: <1 minute**Expected hasil:**

```

---Epoch 1/100

123/123 [==============================] - 245s - loss: 0.5234 - accuracy: 0.7823

## 🔄 Preprocessing Pipelineval_loss: 0.3421 - val_accuracy: 0.8632



1. **Load Images**...

   - Read JPG/PNG from `dataset_sungai/`

   - Size range: varied (typically 200-500px)✅ Training selesai!

Model disimpan di: models/xception_model.keras

2. **Resize**```

   - Target: 224×224 (ResNet18 standard)

   - Interpolation: Linear### 4. Evaluate Model



3. **Normalize**```bash

   - Pixel values: [0, 1]python scripts/evaluate_model.py

   - ImageNet stats:```

     - Mean: [0.485, 0.456, 0.406]

     - Std: [0.229, 0.224, 0.225]**Output:**

```

4. **Split Dataset**MODEL EVALUATION

   - Train: 70% (142 images)================================================

   - Val: 15% (31 images)Accuracy:  0.8876

   - Test: 15% (31 images)Precision: 0.8934

   - **Stratified split** to preserve class balanceRecall:    0.8912

F1-Score:  0.8923

5. **Save**

   - NumPy arrays: `data_processed/train|val|test/images.npy`CLASSIFICATION REPORT

   - Labels: `data_processed/train|val|test/labels.npy`                precision    recall  f1-score   support

        jernih       0.89      0.88      0.88        61

---         keruh       0.90      0.89      0.89        70



## 📈 Training Monitoring    accuracy                           0.89       131

   macro avg       0.89      0.89      0.89       131

Each notebook saves:```

- **Training curves** (loss & accuracy)

- **Confusion matrix** (predictions breakdown)### 5. Predict/Inference

- **ROC curve** (classification threshold analysis)

- **Metrics JSON** (detailed metrics)```python

from scripts.predict import RiverTurbidityPredictor

---

# Initialize

## 🎯 Usage Examplespredictor = RiverTurbidityPredictor()



### Example 1: Predict Single Image# Predict single image

```pythonresult = predictor.predict_single("path/to/image.jpg")

from pathlib import Pathprint(result)

pred_class, confidence, original = predict_single('new_river_photo.jpg')# Output:

print(f"{class_names[pred_class]} ({confidence:.2%})")# {

# Output: Clear (Jernih) (94.23%)#     'image_path': 'path/to/image.jpg',

```#     'class': 'Keruh (Turbid)',

#     'confidence': 0.9234,

### Example 2: Batch Predict Folder#     'probabilities': {'jernih': 0.0766, 'keruh': 0.9234},

```python#     'is_confident': True

results_df = predict_batch('new_images_folder/')# }

results_df.to_csv('predictions.csv')

# Output: CSV with [Image, Prediction, Confidence, Clear_Prob, Turbid_Prob]# Predict batch

```results = predictor.predict_batch("path/to/folder/")

```

---

## 🧠 Model Architecture

## 🐛 Troubleshooting

### Base Model: Xception (ImageNet pre-trained)

### GPU Not Detected?```

```powershell- Input: 299×299×3

# Verify PyTorch installation- 36 convolutional layers

.\venv_tf210\Scripts\python.exe verify_pytorch_gpu.py- Separable convolutions

```- Pre-trained weights: ImageNet

```

Expected output: `CUDA available: True`

### Custom Head:

### OutOfMemory Error?```

- Reduce batch size in `2_Training_ResNet18.ipynb` from 16 to 8GlobalAveragePooling2D()

↓

### Slow Training?Dense(256, relu) + Dropout(0.5)

- Ensure GPU is being used (check NVIDIA-SMI while training)↓

- If CPU only: check CUDA availabilityDense(128, relu) + Dropout(0.3)

↓

---Dense(2, softmax)  → [jernih, keruh]

```

## 📝 Reference: Previous Model

### Hyperparameters:

**Xception Model** (superseded by ResNet18):- **Optimizer**: Adam (lr=0.001, decay 0.1× pada fine-tuning)

- Parameters: 20.9M (larger)- **Loss**: Categorical Crossentropy

- Test Accuracy: 80.65%- **Metrics**: Accuracy, Precision, Recall

- Training Time: ~6-7 hours (CPU)- **Batch Size**: 32

- Model file: `models/xception_final.keras`- **Image Size**: 299×299

- Issue: Potential overfitting (100% train vs 87% val)- **Data Augmentation**: Rotation, Flip, Zoom, Brightness



**Why ResNet18 is Better**:## 📈 Training Monitoring

- 11.2M parameters (46% smaller)

- Faster training (15-30 min vs 6-7 hours)### TensorBoard

- Better generalization (less overfitting)```bash

- Native PyTorch supporttensorboard --logdir=logs/tensorboard

```

---Buka http://localhost:6006 untuk visualisasi training



## 🔗 Dependencies### Metrics tracked:

- Training & Validation Loss

```- Training & Validation Accuracy

torch==2.7.1+cu118          # PyTorch with CUDA 11.8- Precision, Recall per epoch

torchvision>=0.18.0         # Image utilities- Learning rate decay

numpy>=1.24.0- Gradient histograms

opencv-python>=4.8.0

pillow>=10.0.0## 📊 Expected Performance

matplotlib>=3.8.0

seaborn>=0.12.0Dengan dataset ~2500 per kategori dan fine-tuning:

pandas>=2.0.0- **Accuracy**: 85-92%

scikit-learn>=1.3.0- **Precision**: 85-91%

jupyter>=1.0.0- **Recall**: 85-90%

```- **F1-Score**: 85-90%



Install with:## 🎯 Requirements

```powershell

pip install -r requirements.txt### Hardware

```- **GPU**: NVIDIA RTX 4070 Super (12 GB VRAM) ✓

- **RAM**: 16+ GB

---- **Storage**: 50+ GB untuk dataset + model



## 📧 Notes### Software

- Python 3.8+

- All notebooks use `device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')`- CUDA 11.8+ (untuk GPU support)

- Images are normalized per-pixel using ImageNet statistics- cuDNN 8.6+

- Model evaluation uses 31 test images (stratified split)

- Confidence scores are softmax probabilities### Python Packages

- ROC curves are computed for the "Turbid" class vs others```

tensorflow>=2.13.0

---keras>=2.13.0

scikit-learn>=1.3.0

**Last Updated**: 2025-01-02  numpy>=1.24.0

**Status**: ✅ Production Ready  pillow>=10.0.0

**GPU Verified**: NVIDIA RTX 4070 Super @ 12GB VRAMopencv-python>=4.8.0

matplotlib>=3.7.0
seaborn>=0.12.0
```

## 🔍 Troubleshooting

### GPU tidak detected
```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

Jika kosong, install CUDA Toolkit 11.8+ dan cuDNN

### Out of Memory (OOM)
Kurangi BATCH_SIZE di `train_model.py`:
```python
BATCH_SIZE = 16  # atau lebih kecil
```

### Preprocessing error
Pastikan folder `dataset_sungai/keruh` dan `dataset_sungai/jernih` ada dan berisi gambar

## 📝 Authors & References

- Transfer Learning: https://www.tensorflow.org/tutorials/images/transfer_learning
- Xception: https://arxiv.org/abs/1610.02357
- Data Augmentation: https://keras.io/api/preprocessing/image/

## 📄 License

MIT License - Feel free to use for academic/research purposes

---

**Last Updated**: 2025-10-30
**Status**: ✅ Production Ready
