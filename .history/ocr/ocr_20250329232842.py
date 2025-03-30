from PIL import Image
import pdf2image
import boto3
import json
import os
import csv

# 🔹 AWS Credentials
aws_access_key = "YOUR_AWS_ACCESS_KEY"
aws_secret_key = "YOUR_AWS_SECRET_KEY"
region = "us-east-1"

# 🔹 Initialize Textract client
textract = boto3.client(
    "textract",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region
)

# 🔹 Paths
input_folder = "D:/TaxGenie/Bank Statement/"  # Input folder
output_folder = "D:/TaxGenie/Processed/"  # Output folder
os.makedirs(output_folder, exist_ok=True)

def convert_pdf_to_images(pdf_path):
    """Converts PDF to images (JPEG)"""
    images = pdf2image.convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        img_path = f"{pdf_path}_page_{i+1}.jpg"
        image.save(img_path, "JPEG")
        image_paths.append(img_path)
    return image_paths

def analyze_document(image_path):
    """Extracts structured data from an image using AWS Textract."""
    with open(image_path, "rb") as file:
        img_bytes = file.read()

    try:
        response = textract.analyze_document(
            Document={'Bytes': img_bytes},
            FeatureTypes=["FORMS", "TABLES"]
        )
        return response
    except textract.exceptions.UnsupportedDocumentException:
        print(f"❌ Unsupported format: {image_path} (Skipping...)")
        return None

# 🔹 Process all files in the folder
for file_name in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file_name)
    ext = file_name.lower().split(".")[-1]

    # Convert PDFs to images
    if ext == "pdf":
        print(f"🔄 Converting PDF: {file_name}...")
        image_paths = convert_pdf_to_images(file_path)
    else:
        image_paths = [file_path]

    # Process each image
    for img_path in image_paths:
        print(f"📄 Processing: {img_path}...")
        response = analyze_document(img_path)
        if response:
            print(f"✅ Successfully processed: {img_path}")
        else:
            print(f"⚠️ Skipped: {img_path}")

print("\n🎉 All valid files processed!")
