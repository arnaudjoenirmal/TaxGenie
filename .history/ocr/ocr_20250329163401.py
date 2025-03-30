import pytesseract
import cv2
import numpy as np
import os
from PIL import Image
from pdf2image import convert_from_path
import glob

# 🔹 Preprocess Image (Grayscale + Noise Removal + Binarization)
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    image = cv2.GaussianBlur(image, (5, 5), 0)  # Reduce noise
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)  # Binarization
    return thresh

# 🔹 Extract text from Image
def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)  # Preprocess image
    text = pytesseract.image_to_string(processed_image)  # Run OCR
    return text.strip()

# 🔹 Extract text from PDF
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)  # Convert PDF pages to images
    full_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)  # OCR directly on image
        full_text += text + "\n"
    return full_text.strip()

# 🔹 Process all images & PDFs in a folder
input_folder = "/content/drive/MyDrive/ocr_dataset"  # Update with your path
output_base_folder = "/content/drive/MyDrive/ocr_output"

if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

for file_path in glob.glob(f"{input_folder}/*"):
    filename = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename
    output_folder = os.path.join(output_base_folder, f"{filename}_processed")  # Create output folder
    os.makedirs(output_folder, exist_ok=True)

    if file_path.lower().endswith((".jpg", ".png", ".jpeg")):
        extracted_text = extract_text_from_image(file_path)
    elif file_path.lower().endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    else:
        continue  # Skip unsupported files

    # Save only the extracted text file
    output_text_path = os.path.join(output_folder, f"{filename}.txt")
    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"✅ Processed: {file_path} → Extracted text saved in {output_text_path}")
