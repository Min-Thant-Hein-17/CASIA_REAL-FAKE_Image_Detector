# CASIA_REAL-FAKE_Image_Detector

This is my Final Project from the Advanced Machine Learning (AML) class. The goal of this project is to detect whether an image is **real (authentic)** or **fake (tampered)** by using a **CNN (Convolutional Neural Network)** model with binary classification.

---

## About the Project

I used the CASIA2 dataset which contains real and tampered images. I trained a deep learning model using TensorFlow and Keras, then deployed it as a web application using Flask.

**Dataset:** https://www.kaggle.com/code/shaft49/real-vs-fake-images-casia-dataset

---

## How to Run the Project

### Step 1 — Clone the repository
```bash
git clone https://github.com/minthanthein17/CASIA_REAL-FAKE_Image_Detector.git
cd CASIA_REAL-FAKE_Image_Detector
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Generate the model file
Since the model file is too large to upload to GitHub, I only uploaded the `.ipynb` notebook file. You need to run all the cells in the notebook to generate the model file:
```
DL_final_project_copy_2.ipynb → run all cells → model.keras will be created
```

### Step 4 — Run the Flask app
```bash
cd casia_app
python app.py
```

### Step 5 — Open in browser
```
http://127.0.0.1:5000
```

---

## File Structure

```
casia_app/
├── app.py                  ← main Flask application
├── model.keras             ← generated after running the notebook
├── requirements.txt        ← required Python packages
│
├── templates/              ← HTML pages
│   ├── base.html
│   ├── banner.html
│   ├── slider.html
│   ├── sidebar.html
│   ├── home.html
│   ├── predict.html
│   ├── about.html
│   └── contact.html
│
└── static/                 ← CSS and images
    ├── css/
    │   └── style.css
    └── images/
        ├── 1.jpg
        ├── 2.jpg
        └── 3.jpg
```

---

## Notes

- The model file is not included in this repository because the file size is too large for GitHub.
- By running all the code in the notebook, it will automatically generate and save the `model.keras` file.
- During Azure Cloud deployment, the model had errors with the `.h5` format, so I switched to `.keras` format.
- The first `.keras` file was around 200 MB (old format). After regenerating with the new format, the file size is now around 60 MB which works correctly with Azure.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Main programming language |
| TensorFlow / Keras | Deep learning model |
| Flask | Web application framework |
| HTML / CSS | Frontend UI |
| Kaggle API | Dataset download |
| Microsoft Azure | Cloud deployment |

---

## Dataset Info

| | Count |
|---|---|
| Real images (Authentic) | 7,491 |
| Fake images (Tampered) | 5,123 |
| Total | 12,614 |
| Image input size | 128 × 128 × 3 |

---

*AML Final Project 2025 — Min Thant Hein*
