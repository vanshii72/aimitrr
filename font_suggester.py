import numpy as np
from colorthief import ColorThief
from PIL import Image

def extract_dominant_color(image_path):
    try:
        color_thief = ColorThief(image_path)
        dominant_color = color_thief.get_color(quality=1)
        return dominant_color
    except:
        return None

def calculate_brightness(rgb):
    r, g, b = rgb
    brightness = (0.299*r + 0.587*g + 0.114*b) / 255
    return brightness

def suggest_font(dominant_color):
    r, g, b = dominant_color
    brightness = calculate_brightness((r, g, b))

    suggestions = {}

    # ------ FONT COLOR BASED ON BACKGROUND ------
    if brightness > 0.6:  
        suggestions["font_color"] = "Black / Dark Gray (#000000 - #333333)"
    else:
        suggestions["font_color"] = "White / Light Gray (#FFFFFF - #DDDDDD)"

    # ------ FONT STYLE BASED ON BACKGROUND ------
    if brightness > 0.75:
        suggestions["font_style"] = "Sans-serif (clean & bold)"
        suggestions["recommended_fonts"] = ["Poppins", "Montserrat", "Open Sans"]
    elif brightness > 0.45:
        suggestions["font_style"] = "Semi-serif / Neutral"
        suggestions["recommended_fonts"] = ["Lato", "Rubik", "Nunito"]
    else:
        suggestions["font_style"] = "Serif or Rounded Fonts"
        suggestions["recommended_fonts"] = ["Merriweather", "Playfair Display", "DM Serif"]

    # ------ FONT WEIGHT ------
    if brightness > 0.7:
        suggestions["font_weight"] = "Bold or Medium"
    else:
        suggestions["font_weight"] = "Regular or Semi-Bold"

    return suggestions

def analyze_image_fonts(image_path):
    dominant_color = extract_dominant_color(image_path)
    if dominant_color is None:
        return {"error": "Unable to read image"}

    suggestions = suggest_font(dominant_color)
    suggestions["dominant_color"] = dominant_color
    suggestions["brightness"] = calculate_brightness(dominant_color)

    return suggestions
