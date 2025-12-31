import cv2
import os

def rotate_image(img, angle):
    """Rotate image based on angle."""
    if angle == 90:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(img, cv2.ROTATE_180)
    elif angle == 360:
        return img.copy()  # No change
    else:
        raise ValueError("Invalid angle selected!")

def main():
    print("===== IMAGE ROTATION TOOL =====")

    image_path = input("Enter image path: ").strip()

    # Check file exists
    if not os.path.exists(image_path):
        print("❌ Error: File not found!")
        return

    # Try loading image
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Error: Unable to read the image! Check file format.")
        return

    # Rotation menu
    print("\nSelect rotation angle:")
    print("1. 90°")
    print("2. 180°")
    print("3. 360°")

    choice = input("Enter choice (1/2/3): ").strip()

    angle_map = {"1": 90, "2": 180, "3": 360}

    if choice not in angle_map:
        print("❌ Invalid choice!")
        return

    angle = angle_map[choice]

    # Rotate image
    rotated_img = rotate_image(img, angle)

    # Auto-generate save name based on original file
    folder = os.path.dirname(image_path)
    base = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(folder, f"{base}_rotated_{angle}.png")

    # Save rotated image
    cv2.imwrite(output_path, rotated_img)

    print(f"\n✅ Image rotated by {angle}° successfully!")
    print(f"📁 Saved as: {output_path}")

if __name__ == "__main__":
    main()
