"""Quick U-Net training script (5 epochs, synthetic data) for demo"""
import os, json, random, time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# Paths
ROOT = Path(__file__).parent
MODELS = ROOT / 'models'
MODELS.mkdir(exist_ok=True, parents=True)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Device: {device}')
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# U-Net model
class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.seq = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1), nn.BatchNorm2d(out_ch), nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1), nn.BatchNorm2d(out_ch), nn.ReLU(inplace=True),
        )
    def forward(self, x):
        return self.seq(x)

class UNetSmall(nn.Module):
    def __init__(self, in_ch=2, out_ch=1):
        super().__init__()
        self.down1 = DoubleConv(in_ch, 32)
        self.pool1 = nn.MaxPool2d(2)
        self.down2 = DoubleConv(32, 64)
        self.pool2 = nn.MaxPool2d(2)
        self.down3 = DoubleConv(64, 128)
        self.pool3 = nn.MaxPool2d(2)
        self.bott = DoubleConv(128, 256)
        self.up3 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.conv3 = DoubleConv(256, 128)
        self.up2 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.conv2 = DoubleConv(128, 64)
        self.up1 = nn.ConvTranspose2d(64, 32, 2, stride=2)
        self.conv1 = DoubleConv(64, 32)
        self.outc = nn.Conv2d(32, out_ch, 1)
    
    def forward(self, x):
        d1 = self.down1(x); p1 = self.pool1(d1)
        d2 = self.down2(p1); p2 = self.pool2(d2)
        d3 = self.down3(p2); p3 = self.pool3(d3)
        b = self.bott(p3)
        u3 = self.up3(b); c3 = self.conv3(torch.cat([u3, d3], dim=1))
        u2 = self.up2(c3); c2 = self.conv2(torch.cat([u2, d2], dim=1))
        u1 = self.up1(c2); c1 = self.conv1(torch.cat([u1, d1], dim=1))
        return self.outc(c1)

# Loss & metrics
bce = nn.BCEWithLogitsLoss()

def dice_loss(pred, target, smooth=1.):
    pred = torch.sigmoid(pred)
    inter = (pred * target).sum(dim=(1,2,3))
    union = pred.sum(dim=(1,2,3)) + target.sum(dim=(1,2,3))
    dice = (2*inter + smooth) / (union + smooth)
    return 1 - dice.mean()

def loss_fn(pred, target):
    return bce(pred, target) + dice_loss(pred, target)

def iou_score(pred, target, thr=0.5, eps=1e-6):
    pred_bin = (torch.sigmoid(pred) > thr).float()
    inter = (pred_bin * target).sum(dim=(1,2,3))
    union = pred_bin.sum(dim=(1,2,3)) + target.sum(dim=(1,2,3)) - inter
    return ((inter + eps) / (union + eps)).mean().item()

# Synthetic dataset
def synth(n=64, size=256):
    imgs, msks = [], []
    for _ in range(n):
        img = np.random.rand(2, size, size).astype('float32') * 0.1
        msk = np.zeros((size, size), dtype='float32')
        cx, cy = np.random.randint(64, size-64, 2)
        rr, cc = np.ogrid[:size, :size]
        rad = np.random.randint(20, 60)
        circle = (rr - cy)**2 + (cc - cx)**2 <= rad*rad
        msk[circle] = 1.0
        img[0][circle] += 0.8
        img[1][circle] += 0.6
        imgs.append(img)
        msks.append(msk)
    return np.array(imgs), np.array(msks)

class DS(Dataset):
    def __init__(self, X, Y, aug=False):
        self.X, self.Y, self.aug = X, Y, aug
    def __len__(self):
        return len(self.X)
    def __getitem__(self, i):
        x, y = self.X[i], self.Y[i]
        if self.aug and random.random() < 0.5:
            x = x[:, :, ::-1].copy()
            y = y[:, ::-1].copy()
        return torch.from_numpy(x), torch.from_numpy(y)[None, ...]

print('Generating synthetic data...')
Xtr, Ytr = synth(96)
Xv, Yv = synth(24)
train_ds = DS(Xtr, Ytr, aug=True)
val_ds = DS(Xv, Yv, aug=False)
train_loader = DataLoader(train_ds, batch_size=8, shuffle=True, num_workers=0)
val_loader = DataLoader(val_ds, batch_size=8, shuffle=False, num_workers=0)

# Train
model = UNetSmall(in_ch=2, out_ch=1).to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
best_iou = -1.0
best_path = MODELS / 'best_unet.pt'
EPOCHS = int(os.getenv("UNET_EPOCHS", "5"))

print(f'Training for {EPOCHS} epochs on {device}...')
for ep in range(1, EPOCHS + 1):
    model.train()
    tr_loss = 0.0
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        p = model(x)
        loss = loss_fn(p, y)
        loss.backward()
        optimizer.step()
        tr_loss += loss.item()
    
    # Validation
    model.eval()
    val_iou = 0.0
    n = 0
    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(device), y.to(device)
            p = model(x)
            val_iou += iou_score(p, y)
            n += 1
    val_iou /= max(1, n)
    print(f'Epoch {ep:02d} | TrainLoss {(tr_loss/len(train_loader)):.3f} | ValIoU {val_iou:.3f}')
    
    if val_iou > best_iou:
        best_iou = val_iou
        torch.save(model.state_dict(), best_path)

print(f'Saved best to {best_path} | ValIoU={best_iou:.3f}')
