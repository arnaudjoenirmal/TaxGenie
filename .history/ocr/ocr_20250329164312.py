import pytesseract
import cv2
import os

# 🔹 Set your image path (UPDATE THIS)
image_path = r"D:\TaxGenie\Bank Statement\94.jpg"

# 🔹 Preprocess Image (Grayscale + Binarization)
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)  # Binarization
    return thresh

# 🔹 Extract text from the image
def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)  # Apply preprocessing
    text = pytesseract.image_to_string(processed_image)  # Run OCR
    return text.strip()

# 🔹 Run OCR on the selected image
extracted_text = extract_text_from_image(image_path)

# 🔹 Save extracted text as a .txt file in the same folder
output_text_path = os.path.splitext(image_path)[0] + ".txt"
with open(output_text_path, "w", encoding="utf-8") as f:
    f.write(extracted_text)

print(f"✅ Processed: {image_path} → Extracted text saved in {output_text_path}")
