from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy as np
from PIL import Image
import tensorflow as tf
import base64
import os

app = Flask(__name__)
app.secret_key = 'casia_dl_project_secret_key_2025'

# ── Email Config (fill in your Gmail details) ────────────────
EMAIL_ADDRESS  = "youremail@gmail.com"
EMAIL_PASSWORD = "your_16_char_app_password"
RECEIVER_EMAIL = "youremail@gmail.com"

# ── Lazy Model Loading ───────────────────────────────────────
# Model loads only on first prediction — prevents Azure startup timeout
# Supports both .keras (new) and .h5 (old) formats automatically
_model = None

def get_model():
    global _model
    if _model is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Try .keras format first (new, Azure-compatible)
        keras_path = os.path.join(base_dir, 'casia_model.keras')
        h5_path    = os.path.join(base_dir, 'casia_model.h5')

        if os.path.exists(keras_path):
            print("Loading model from casia_model.keras ...")
            _model = tf.keras.models.load_model(keras_path)
        elif os.path.exists(h5_path):
            print("Loading model from casia_model.h5 ...")
            _model = tf.keras.models.load_model(
                h5_path,
                custom_objects=None,
                compile=False      # skips renorm/compile issues
            )
        else:
            raise FileNotFoundError(
                "No model file found! Place casia_model.keras or "
                "casia_model.h5 next to app.py"
            )
        print("Model loaded successfully!")
    return _model

# ── Constants ────────────────────────────────────────────────
IMG_SIZE = (128, 128)
CLASSES  = ["REAL", "FAKE"]

def preprocess_image(file):
    """Preprocess uploaded image — must match training preprocessing."""
    img = Image.open(file).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, axis=0)   # shape: (1, 128, 128, 3)


# ── Routes ───────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/predict', methods=["GET", "POST"])
def predict():
    prediction = None
    confidence = None
    prob_real  = None
    prob_fake  = None
    img_src    = None
    is_fake    = False
    error      = None

    if request.method == "POST":
        if "image" not in request.files or request.files["image"].filename == "":
            error = "Please upload an image file."
        else:
            file = request.files["image"]
            try:
                model      = get_model()
                img_array  = preprocess_image(file)
                probs      = model.predict(img_array)[0]
                pred_index = int(np.argmax(probs))
                prediction = CLASSES[pred_index]
                confidence = round(float(np.max(probs)) * 100, 2)
                prob_real  = round(float(probs[0]) * 100, 2)
                prob_fake  = round(float(probs[1]) * 100, 2)
                is_fake    = (pred_index == 1)

                # Image preview
                file.seek(0)
                img_data = base64.b64encode(file.read()).decode("utf-8")
                img_src  = f"data:image/jpeg;base64,{img_data}"

            except Exception as e:
                error = f"Error processing image: {str(e)}"

    return render_template(
        "predict.html",
        prediction = prediction,
        confidence = confidence,
        prob_real  = prob_real,
        prob_fake  = prob_fake,
        img_src    = img_src,
        is_fake    = is_fake,
        error      = error
    )


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=['GET'])
def contact():
    return render_template("contact.html")


@app.route('/contact', methods=['POST'])
def send_email():
    full_name = request.form['name']
    email     = request.form['email']
    message   = request.form['message']

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg_admin = MIMEMultipart()
        msg_admin['From']     = EMAIL_ADDRESS
        msg_admin['To']       = RECEIVER_EMAIL
        msg_admin['Subject']  = f"New Contact Message from {full_name}"
        msg_admin['Reply-To'] = email

        body_admin = f"""
        New message received from CASIA Detector website:

        Name:    {full_name}
        Email:   {email}
        Message: {message}
        """
        msg_admin.attach(MIMEText(body_admin, 'plain'))
        server.send_message(msg_admin)

        msg_user = MIMEMultipart()
        msg_user['From']    = EMAIL_ADDRESS
        msg_user['To']      = email
        msg_user['Subject'] = "We received your message — CASIA Detector"

        body_user = f"""
        Dear {full_name},

        Thank you for contacting us.
        We have received your message and will respond as soon as possible.

        Best regards,
        CASIA Detector Team
        """
        msg_user.attach(MIMEText(body_user, 'plain'))
        server.send_message(msg_user)
        server.quit()

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('contact'))

    except Exception as e:
        print(e)
        flash("Something went wrong. Please try again.", "danger")
        return redirect(url_for('contact'))


if __name__ == '__main__':
    app.run(debug=True)
