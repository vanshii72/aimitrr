import pickle

# Updated color model with more common colors and suggestions
color_model = [
    {
        "dominant_color": "#fefefe",
        "brightness": "high",
        "contrast": "low",
        "suggested_color_palette": "Dark Navy, Deep Purple",
        "suggested_font_style": "Minimal Rounded"
    },
    {
        "dominant_color": "#fd8600",
        "brightness": "high",
        "contrast": "medium",
        "suggested_color_palette": "Navy Blue, Deep Purple",
        "suggested_font_style": "Bold Sans Serif"
    },
    {
        "dominant_color": "#b94206",
        "brightness": "medium",
        "contrast": "medium",
        "suggested_color_palette": "Cream, Beige",
        "suggested_font_style": "Serif Modern"
    },
    {
        "dominant_color": "#2a1809",
        "brightness": "low",
        "contrast": "high",
        "suggested_color_palette": "Gold, Beige",
        "suggested_font_style": "Elegant Serif"
    },
    {
        "dominant_color": "#949079",
        "brightness": "medium",
        "contrast": "low",
        "suggested_color_palette": "Dark Green, Olive",
        "suggested_font_style": "Minimal Rounded"
    },
    {
        "dominant_color": "#000000",
        "brightness": "low",
        "contrast": "high",
        "suggested_color_palette": "White, Grey",
        "suggested_font_style": "Bold Sans Serif"
    },
    {
        "dominant_color": "#ffffff",
        "brightness": "high",
        "contrast": "low",
        "suggested_color_palette": "Dark Navy, Deep Purple",
        "suggested_font_style": "Minimal Rounded"
    },
    {
        "dominant_color": "#ff0000",
        "brightness": "high",
        "contrast": "high",
        "suggested_color_palette": "Black, White",
        "suggested_font_style": "Bold Serif"
    },
    {
        "dominant_color": "#00ff00",
        "brightness": "high",
        "contrast": "high",
        "suggested_color_palette": "Black, Dark Green",
        "suggested_font_style": "Minimal Sans"
    },
    {
        "dominant_color": "#0000ff",
        "brightness": "medium",
        "contrast": "high",
        "suggested_color_palette": "White, Light Grey",
        "suggested_font_style": "Bold Sans"
    }
]

# Save to pickle file
with open("tesco_model.pkl", "wb") as f:
    pickle.dump(color_model, f)

print("Updated color model saved as tesco_model.pkl")
