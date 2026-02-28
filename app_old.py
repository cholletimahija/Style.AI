from PIL import Image
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
from dotenv import load_dotenv
from groq import Groq
from werkzeug.utils import secure_filename
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Upload configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# AI Test Route
@app.route("/test")
def test():
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": "Suggest an outfit for a casual college day."
        }],
        max_tokens=200
    )
    return response.choices[0].message.content


# Upload Route (Full AI Pipeline)
@app.route("/upload", methods=["POST"])
def upload_image():

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Open and process image
        img = Image.open(filepath)
        img = img.convert("RGB")
        img_array = np.array(img)

        # Average RGB
        avg_color = img_array.mean(axis=(0, 1))
        r, g, b = avg_color

        # Brightness
        brightness = (r + g + b) / 3

        # Skin tone classification
        if brightness > 200:
            skin_tone = "Fair"
        elif brightness > 160:
            skin_tone = "Medium"
        elif brightness > 120:
            skin_tone = "Olive"
        else:
            skin_tone = "Deep"

        # AI Prompt
        prompt = f"""
        A person has {skin_tone} skin tone.
        Suggest a stylish outfit for a casual college day.
        Include:
        - Top wear
        - Bottom wear
        - Footwear
        - Accessories
        Keep it modern and trendy.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        style_advice = response.choices[0].message.content

        return render_template(
            "result.html",
            image_path=filename,
            skin_tone=skin_tone,
            brightness=int(brightness),
            style_suggestion=style_advice
        )

    return jsonify({"error": "Invalid file type"}), 400


if __name__ == "__main__":
    app.run(debug=True)