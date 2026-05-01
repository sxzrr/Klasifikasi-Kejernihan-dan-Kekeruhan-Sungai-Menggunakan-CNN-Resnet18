"""
Shared training utilities untuk River Turbidity Classification models
Mendukung ResNet18, XceptionNet, dan model lainnya
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import time
from tqdm import tqdm
import os

class ModelTrainer:
    """Unified trainer untuk berbagai model CNN"""
    
    def __init__(self, model, device='cuda', model_name='model'):
        """
        Args:
            model: PyTorch model
            device: 'cuda' atau 'cpu'
            model_name: Nama model untuk saving (e.g., 'ResNet18', 'XceptionNet')
        """
        self.model = model.to(device)
        self.device = device
        self.model_name = model_name
        self.history = {
            'train_loss': [],
            'val_loss': [],
            'train_acc': [],
            'val_acc': []
        }
        
    def train_epoch(self, train_loader, criterion, optimizer):
        """Train satu epoch"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(train_loader, desc='Training', unit='batch')
        for images, labels in pbar:
            images = images.to(self.device)
            labels = labels.to(self.device)
            
            # Forward pass
            outputs = self.model(images)
            loss = criterion(outputs, labels)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Statistics
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            pbar.set_postfix({'loss': loss.item():.4f}, refresh=True)
        
        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100 * correct / total
        
        return epoch_loss, epoch_acc
    
    def validate_epoch(self, val_loader, criterion):
        """Validate satu epoch"""
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            pbar = tqdm(val_loader, desc='Validating', unit='batch')
            for images, labels in pbar:
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model(images)
                loss = criterion(outputs, labels)
                
                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                
                pbar.set_postfix({'loss': loss.item():.4f}, refresh=True)
        
        epoch_loss = running_loss / len(val_loader)
        epoch_acc = 100 * correct / total
        
        return epoch_loss, epoch_acc
    
    def train(self, train_loader, val_loader, num_epochs=20, lr=0.001, 
              save_path='models/', early_stopping=True, patience=5):
        """
        Train model dengan optional early stopping
        
        Args:
            train_loader: DataLoader untuk training
            val_loader: DataLoader untuk validation
            num_epochs: Jumlah epoch
            lr: Learning rate
            save_path: Path untuk save best model
            early_stopping: Enable early stopping
            patience: Berapa epoch menunggu sebelum stop
        """
        os.makedirs(save_path, exist_ok=True)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=3, verbose=True
        )
        
        best_val_loss = float('inf')
        patience_counter = 0
        
        print(f"\n{'='*60}")
        print(f"🚀 Training {self.model_name}")
        print(f"{'='*60}\n")
        
        for epoch in range(num_epochs):
            print(f"\n[Epoch {epoch+1}/{num_epochs}]")
            
            # Train
            train_loss, train_acc = self.train_epoch(train_loader, criterion, optimizer)
            print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
            
            # Validate
            val_loss, val_acc = self.validate_epoch(val_loader, criterion)
            print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
            
            # History
            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_acc'].append(val_acc)
            
            # Learning rate scheduling
            scheduler.step(val_loss)
            
            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                
                model_path = os.path.join(save_path, f"{self.model_name.lower()}_best.pth")
                torch.save(self.model.state_dict(), model_path)
                print(f"✅ Saved best model to {model_path}")
            else:
                patience_counter += 1
                
                if early_stopping and patience_counter >= patience:
                    print(f"\n⚠️ Early stopping triggered (patience {patience} reached)")
                    break
        
        print(f"\n{'='*60}")
        print(f"✅ Training completed!")
        print(f"Best Val Loss: {best_val_loss:.4f}")
        print(f"Final Val Acc: {self.history['val_acc'][-1]:.2f}%")
        print(f"{'='*60}\n")
        
        return self.history
    
    def load_best_model(self, model_path):
        """Load best model weights"""
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        print(f"✅ Loaded model from {model_path}")
    
    def get_history(self):
        """Return training history"""
        return self.history
