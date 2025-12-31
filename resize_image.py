import cv2
import os

def resize_image(input_path, output_path, width=None, height=None):
    """
    Resize an image while keeping aspect ratio if only width or height is given.
    """
    if not os.path.exists(input_path):
        print("❌ Input image not found!")
        return

    img = cv2.imread(input_path)
    if img is None:
        print("❌ Error loading image!")
        return

    h, w = img.shape[:2]

    # If both width and height are given → direct resize
    if width and height:
        new_size = (width, height)
        resized = cv2.resize(img, new_size)
    
    # Resize based on width only → keep aspect ratio
    elif width:
        ratio = width / w
        height = int(h * ratio)
        resized = cv2.resize(img, (width, height))

    # Resize based on height only → keep aspect ratio
    elif height:
        ratio = height / h
        width = int(w * ratio)
        resized = cv2.resize(img, (width, height))
    
    else:
        print("❌ Provide at least width or height!")
        return

    cv2.imwrite(output_path, resized)
    print(f"✅ Image resized successfully!")
    print(f"📁 Saved at: {output_path}")


# ----------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------

if __name__ == "__main__":
    image_path = input("Enter image path: ").strip()
    save_path = input("Enter output image name (with .jpg/.png): ").strip()

    print("\nChoose Resize Option:")
    print("1️⃣ Resize by Width")
    print("2️⃣ Resize by Height")
    print("3️⃣ Resize by Width & Height (custom)")
    choice = input("\nEnter choice (1/2/3): ")

    if choice == "1":
        width = int(input("Enter new width (px): "))
        resize_image(image_path, save_path, width=width)

    elif choice == "2":
        height = int(input("Enter new height (px): "))
        resize_image(image_path, save_path, height=height)

    elif choice == "3":
        width = int(input("Enter width: "))
        height = int(input("Enter height: "))
        resize_image(image_path, save_path, width=width, height=height)

    else:
        print("❌ Invalid choice!")
