import pytesseract
import cv2
import os
from PIL import Image

# 🔹 Set your image path (UPDATE THIS)
image_path = r"D:\TaxGenie\Bank \53.jpg"

# 🔹 Preprocess Image (Grayscale + Binarization)
def preprocess_image(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found at {image_path}")
        return None  # Return None if file is missing

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    if image is None:  # ❌ Image failed to load
        print(f"❌ Error: Unable to read image {image_path}")
        return None

    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)  # Binarization
    return thresh

# 🔹 Extract text from the image
def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)  # Preprocess image
    
    if processed_image is None:  # ❌ Image loading failed
        return ""

    pil_image = Image.fromarray(processed_image)  # ✅ Convert NumPy array to PIL Image
    text = pytesseract.image_to_string(pil_image)  # ✅ Now it works!
    return text.strip()

# 🔹 Run OCR on the selected image
extracted_text = extract_text_from_image(image_path)

# 🔹 Save extracted text as a .txt file in the same folder
if extracted_text:  # Only save if text was extracted
    output_text_path = os.path.splitext(image_path)[0] + ".txt"
    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    print(f"✅ Processed: {image_path} → Extracted text saved in {output_text_path}")
else:
    print(f"⚠️ No text extracted from {image_path}")
