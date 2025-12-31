import cv2
import numpy as np
import pytesseract
import pickle
import os
from glob import glob
import colorsys

# ---------------------------
# Tesseract Setup
# ---------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------------------------
# Load Models
# ---------------------------
def load_model(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    with open(path, "rb") as f:
        return pickle.load(f)

color_model = load_model("tesco_model.pkl")
font_model = load_model("font_suggestion_model.pkl")

# ---------------------------
# Safe Image Loader
# ---------------------------
def load_image_safe(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    img = cv2.imread(path)
    if img is None:
        raise ValueError("Could not load image.")
    return img

# ---------------------------
# Multi-Color Detection
# ---------------------------
def extract_top_colors(image, k=5):
    data = image.reshape((-1, 3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(
        data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    counts = np.bincount(labels.flatten())
    sorted_indices = np.argsort(counts)[::-1]

    palette = []
    for i in sorted_indices:
        c = centers[i]
        color_hex = "#{:02x}{:02x}{:02x}".format(int(c[2]), int(c[1]), int(c[0]))
        palette.append(color_hex)

    return palette

# ---------------------------
# Brightness / Contrast
# ---------------------------
def calculate_brightness_contrast(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray) / 255
    contrast = np.std(gray) / 255
    return brightness, contrast

def classify(value):
    if value < 0.33: return "low"
    if value < 0.66: return "medium"
    return "high"

# ---------------------------
# Color Utils
# ---------------------------
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def generate_palette(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)

    h_comp = (h + 0.5) % 1.0
    r_c, g_c, b_c = colorsys.hls_to_rgb(h_comp, l, s)
    complementary = rgb_to_hex((int(r_c*255), int(g_c*255), int(b_c*255)))

    h_analog1 = (h + 1/12) % 1.0
    h_analog2 = (h - 1/12) % 1.0
    r1, g1, b1 = colorsys.hls_to_rgb(h_analog1, l, s)
    r2, g2, b2 = colorsys.hls_to_rgb(h_analog2, l, s)
    analogous = [
        rgb_to_hex((int(r1*255), int(g1*255), int(b1*255))),
        rgb_to_hex((int(r2*255), int(g2*255), int(b2*255)))
    ]

    palette = [complementary] + analogous
    return ", ".join(palette)

# ---------------------------
# Color Suggestion Logic
# ---------------------------
def get_color_suggestion(color, brightness, contrast):
    b = classify(brightness)
    c = classify(contrast)

    for item in color_model:
        if (item["dominant_color"].lower() == color.lower() and
            item["brightness"] == b and item["contrast"] == c):
            return item

    return {
        "dominant_color": color,
        "brightness": b,
        "contrast": c,
        "suggested_color_palette": generate_palette(color),
        "suggested_font_style": "Minimal Rounded (auto)"
    }

# ---------------------------
# Font Detection Logic
# ---------------------------
def detect_font_from_text(image, templates_folder="font_templates"):
    text = pytesseract.image_to_string(image).strip()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray) / 255

    if brightness < 0.5:
        group = "dark"
        fallback_fonts = font_model.get("dark", [])
        font_color = "White"
    else:
        group = "bright"
        fallback_fonts = font_model.get("bright", [])
        font_color = "Black"

    if text == "":
        return {
            "detected_text": "(No text detected)",
            "font_color_recommended": font_color,
            "recommended_fonts": fallback_fonts,
        }

    best_matches = []
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for template_path in glob(os.path.join(templates_folder, "*.png")):
        template_img = cv2.imread(template_path, 0)
        if template_img is None:
            continue

        res = cv2.matchTemplate(gray_image, template_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        if max_val > 0.7:
            font_name = os.path.basename(template_path).split(".")[0]
            best_matches.append((font_name, max_val))

    best_matches = sorted(best_matches, key=lambda x: x[1], reverse=True)
    detected_fonts = [name for name, val in best_matches[:5]]

    if not detected_fonts:
        detected_fonts = fallback_fonts

    return {
        "detected_text": text,
        "font_color_recommended": font_color,
        "recommended_fonts": detected_fonts
    }

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    image_path = input("Enter image path: ")
    img = load_image_safe(image_path)

    palette = extract_top_colors(img, k=5)
    brightness, contrast = calculate_brightness_contrast(img)

    print("\n===== COLOR ANALYSIS =====")
    print("Top Colors:", palette)

    for color in palette:
        suggestion = get_color_suggestion(color, brightness, contrast)
        print(f"{color} → {suggestion}")

    font_output = detect_font_from_text(img)
    print("\n===== FONT ANALYSIS =====")
    print("Detected Text:", font_output["detected_text"])
    print("Recommended Font Color:", font_output["font_color_recommended"])
    print("Suggested Fonts:", ", ".join(font_output["recommended_fonts"]))
