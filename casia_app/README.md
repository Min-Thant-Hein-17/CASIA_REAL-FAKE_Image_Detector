# CASIA Image Detector — Flask Web App
## AML Final Project 2025

---

## Folder Structure (place everything in D:\MachineLearning\)
```
D:\MachineLearning\
├── app.py
├── casia_model.h5          ← save from your notebook
├── requirements.txt
├── startup.txt             ← for Azure deployment
├── templates\
│   ├── base.html
│   ├── banner.html
│   ├── slider.html
│   ├── sidebar.html
│   ├── home.html
│   ├── predict.html
│   ├── about.html
│   └── contact.html
└── static\
    ├── css\style.css
    └── images\
        ├── 1.jpg           ← add any image (AI/tech theme)
        ├── 2.jpg           ← add any image (image analysis)
        └── 3.jpg           ← add any image (deep learning)
```

---

## Step 1 — Save model (last cell in notebook)
```python
model.save("casia_model.h5")
```

## Step 2 — Install dependencies
```bash
pip install flask tensorflow pillow numpy gunicorn
```

## Step 3 — Run locally
```bash
python app.py
```
Open: http://127.0.0.1:5000

---

## Azure Deployment

```bash
# Install Azure CLI: https://aka.ms/installazurecliwindows
az login
az webapp up --name casia-detector-2025 --runtime "PYTHON:3.10" --sku B1
```

Then in Azure Portal → App Service → Configuration → add startup command:
```
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

---

## Slider Images
Add 3 JPG images to static/images/ named 1.jpg, 2.jpg, 3.jpg
Recommended: search for "AI image forensics", "deep learning", "image tampering detection"
from free sites like Unsplash (unsplash.com) or Pexels (pexels.com)
