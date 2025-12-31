from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import pytesseract

from app import load_image_safe, extract_top_colors, calculate_brightness_contrast, get_color_suggestion, detect_font_from_text
from remove_bg import remove_background
from resize_image import resize_image
from rotate_image import rotate_image

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Uncomment if needed (Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def detect_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if "image" not in request.files:
            return "No file uploaded!", 400

        file = request.files["image"]

        if file.filename == "":
            return "No selected file!", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            feature = request.form.get("feature")

            detected_text = detect_text(filepath)
            no_text = True if detected_text == "" else False

            # 1️⃣ COLOR + FONT
            if feature == "color_font":
                cv_img = cv2.cvtColor(np.array(Image.open(filepath)), cv2.COLOR_RGB2BGR)

                palette = extract_top_colors(cv_img, k=5)
                brightness, contrast = calculate_brightness_contrast(cv_img)
                color_suggestions = [
                    get_color_suggestion(c, brightness, contrast) for c in palette
                ]

                font_output = detect_font_from_text(cv_img)

                return render_template(
                    "result.html",
                    image_path=filepath,
                    palette=palette,
                    color_suggestions=color_suggestions,
                    font_output=font_output,
                    feature="color_font",
                    no_text=no_text
                )

            # 2️⃣ REMOVE BG
            elif feature == "remove_bg":
                output_path = remove_background(filepath)
                return render_template(
                    "result.html",
                    image_path=output_path,
                    feature="remove_bg",
                    no_text=no_text
                )

            # 3️⃣ RESIZE
            elif feature == "resize":
                width = request.form.get("width")
                height = request.form.get("height")

                width = int(width) if width else None
                height = int(height) if height else None

                output_path = os.path.join(UPLOAD_FOLDER, f"resized_{filename}")
                resize_image(filepath, output_path, width, height)

                return render_template(
                    "result.html",
                    image_path=output_path,
                    feature="resize",
                    no_text=no_text
                )

            # 4️⃣ ROTATE
            elif feature == "rotate":
                angle = int(request.form.get("angle", 0))
                output_path = os.path.join(UPLOAD_FOLDER, f"rotated_{filename}")

                img = cv2.imread(filepath)
                rotated = rotate_image(img, angle)
                cv2.imwrite(output_path, rotated)

                return render_template(
                    "result.html",
                    image_path=output_path,
                    feature="rotate",
                    no_text=no_text
                )

    return render_template("index.html")


# ✍️ ADD TEXT ROUTE
@app.route("/add-text", methods=["POST"])
def add_text():
    image_path = request.form.get("image_path")
    user_text = request.form.get("user_text")
    font_size = int(request.form.get("font_size", 30))

    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    draw.text((50, 50), user_text, fill="black", font=font)
    img.save(image_path)

    return render_template(
        "result.html",
        image_path=image_path,
        feature=None,
        no_text=False
    )


if __name__ == "__main__":
    app.run(debug=True)
