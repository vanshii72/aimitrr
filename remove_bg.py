import os
from rembg import remove
from PIL import Image

# ------------------------------------------------------------
# SAFE IMAGE LOADER
# ------------------------------------------------------------
def load_image_safe(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    try:
        return Image.open(path)
    except:
        raise ValueError("Unable to open the image. File may be corrupted.")


# ------------------------------------------------------------
# REMOVE BACKGROUND FUNCTION
# ------------------------------------------------------------
def remove_background(input_path, output_path=None):
    """
    Removes background using rembg and saves the output.
    """

    # Load the image safely
    img = load_image_safe(input_path)

    # Remove background
    output = remove(img)

    # Generate output path if not provided
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = base + "_noBG.png"

    # Save result
    output.save(output_path)

    return output_path


# ------------------------------------------------------------
# MAIN (User Input)
# ------------------------------------------------------------
if __name__ == "__main__":

    # Ask user for image path
    image_path = input("Enter the image path: ").strip()

    try:
        print("\n⏳ Removing background...")
        result_path = remove_background(image_path)
        print("✅ Background removed successfully!")
        print("📌 Saved at:", result_path)
    except Exception as e:
        print("❌ Error:", e)
