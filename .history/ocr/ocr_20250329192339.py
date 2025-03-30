import pytesseract
import cv2
import os
import numpy as np
from PIL import Image

# 🔹 Set Image Path
image_path = r"/mnt/data/image.png"

# 🔹 Preprocess Image (Grayscale + Noise Reduction + Morphological Transformations)
def preprocess_image(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found at {image_path}")
        return None
    
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"❌ Error: Unable to read image {image_path}")
        return None
    
    # 🔹 Noise Reduction
    image = cv2.GaussianBlur(image, (3, 3), 0)
    
    # 🔹 Apply Thresholding
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 🔹 Morphological Transformations (Improves OCR Accuracy)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

    return image

# 🔹 Extract structured text from image
def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)
    if processed_image is None:
        return ""
    
    pil_image = Image.fromarray(processed_image)
    
    # ✅ Use `--psm 4` for table-like structures
    custom_config = "--oem 3 --psm 4"
    
    # Perform OCR and extract as structured text
    text_data = pytesseract.image_to_string(pil_image, config=custom_config)

    return clean_text(text_data)

# 🔹 Clean & Format Extracted Text
def clean_text(text):
    text = text.replace("\n", "\n ")  # Add spacing
    text = text.replace("|", " | ")  # Normalize table-like format
    text = "\n".join(line.strip() for line in text.split("\n") if line.strip())  # Remove empty lines
    return text.strip()

# 🔹 Run OCR
extracted_text = extract_text_from_image(image_path)

# 🔹 Save Extracted Text
if extracted_text:
    output_text_path = os.path.splitext(image_path)[0] + ".txt"
    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    print(f"✅ Processed: {image_path} → Extracted text saved in {output_text_path}")
    print("\n📝 Extracted Text:\n")
    print(extracted_text)  # Print formatted output
else:
    print(f"⚠️ No text extracted from {image_path}")
