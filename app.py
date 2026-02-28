from flask import Flask, render_template, request, send_from_directory
import os
from PIL import Image
import numpy as np
from groq import Groq

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🔥 PASTE YOUR GROQ API KEY HERE
client = Groq(api_key="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")

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/upload", methods=["POST"])
def upload_image():
    file = request.files.get("file")
    gender = request.form.get("gender")
    occasion = request.form.get("occasion")

    if file and gender and occasion:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        image = Image.open(filepath)
        image = image.resize((100, 100))
        img_array = np.array(image)

        avg_color = np.mean(img_array, axis=(0, 1))
        brightness = np.mean(avg_color)

        if brightness < 85:
            skin_tone = "Deep"
        elif brightness < 170:
            skin_tone = "Medium"
        else:
            skin_tone = "Fair"

        # 🔥 STRICT GENDER CONTROL PROMPT
        prompt = f"""
You are a professional fashion stylist.

IMPORTANT RULE:
If Gender is Male → Suggest ONLY men's outfits.
If Gender is Female → Suggest ONLY women's outfits.
Do NOT mix genders.
Do NOT mention the opposite gender.

Give response strictly in this format:

Top Wear:
(1 short paragraph)

Bottom Wear:
(1 short paragraph)

Footwear:
(1 short paragraph)

Details:
Gender: {gender}
Occasion: {occasion}
Skin Tone: {skin_tone}

Keep suggestions brief and professional.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )

        style_advice = response.choices[0].message.content

        return render_template(
            "result.html",
            image_path=file.filename,
            skin_tone=skin_tone,
            brightness=int(brightness),
            style_suggestion=style_advice,
            gender=gender
        )

    return "Missing required data"

if __name__ == "__main__":
    app.run(debug=True)