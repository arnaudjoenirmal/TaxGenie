import boto3
import json
import os
import csv
import logging
from PIL import Image
import pdf2image

# 🔹 Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 AWS Credentials
aws_access_key = "AKIAWOAVSEXOS5QN5CFG"
aws_secret_key = "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"
region = "us-east-1"

# 🔹 Initialize Textract client
try:
    textract = boto3.client(
        "textract",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )
    logging.info("✅ AWS Textract client initialized successfully.")
except Exception as e:
    logging.error(f"❌ Error initializing AWS Textract: {e}")
    exit(1)

# 🔹 Paths
input_folder = "D:/TaxGenie/Bank Statement/"  # Input folder
output_folder = "D:/TaxGenie/Processed/"  # Output folder
os.makedirs(output_folder, exist_ok=True)

def convert_pdf_to_images(pdf_path):
    """Converts a PDF to images (JPEG) for Textract processing."""
    try:
        images = pdf2image.convert_from_path(pdf_path)
        image_paths = []
        for i, image in enumerate(images):
            img_path = f"{pdf_path}_page_{i+1}.jpg"
            image.save(img_path, "JPEG")
            image_paths.append(img_path)
        logging.info(f"🔄 Converted PDF to {len(image_paths)} images.")
        return image_paths
    except Exception as e:
        logging.error(f"❌ Error converting PDF {pdf_path}: {e}")
        return []

def analyze_document(image_path):
    """Extracts structured data (forms & tables) from an image or PDF."""
    try:
        with open(image_path, "rb") as file:
            img_bytes = file.read()

        response = textract.analyze_document(
            Document={'Bytes': img_bytes},
            FeatureTypes=["FORMS", "TABLES"]
        )
        return response
    except textract.exceptions.UnsupportedDocumentException:
        logging.warning(f"❌ Unsupported format: {image_path} (Skipping...)")
        return None
    except Exception as e:
        logging.error(f"❌ Textract API error for {image_path}: {e}")
        return None

def format_textract_data(response):
    """Formats Textract response into structured key-value pairs and tables."""
    key_value_pairs = {}
    tables = []
    block_map = {block["Id"]: block for block in response.get("Blocks", [])}

    # Extract key-value pairs (Forms)
    for block in response.get("Blocks", []):
        if block["BlockType"] == "KEY_VALUE_SET":
            if "KEY" in block["EntityTypes"]:
                key_text = get_text_from_block(block, block_map)
                value_block = find_value_block(block, block_map)
                value_text = get_text_from_block(value_block, block_map)
                if key_text:
                    key_value_pairs[key_text] = value_text

    # Extract tables
    for block in response.get("Blocks", []):
        if block["BlockType"] == "TABLE":
            table = []
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    row = []
                    for cell_id in relationship["Ids"]:
                        cell = block_map.get(cell_id)
                        if cell and cell["BlockType"] == "CELL":
                            row.append(get_text_from_block(cell, block_map))
                    if row:
                        table.append(row)
            if table:
                tables.append(table)

    return {"key_value_pairs": key_value_pairs, "tables": tables}

def get_text_from_block(block, block_map):
    """Extracts text from a Textract block."""
    text = ""
    if "Relationships" in block:
        for relationship in block["Relationships"]:
            if relationship["Type"] == "CHILD":
                for child_id in relationship["Ids"]:
                    text += block_map.get(child_id, {}).get("Text", "") + " "
    return text.strip()

def find_value_block(key_block, block_map):
    """Finds the corresponding value block for a key block."""
    for relationship in key_block.get("Relationships", []):
        if relationship["Type"] == "VALUE":
            for value_id in relationship["Ids"]:
                return block_map.get(value_id)
    return None

def save_to_text(data, filename):
    """Saves extracted text to a .txt file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("🔹 Key-Value Pairs:\n")
            for key, value in data["key_value_pairs"].items():
                file.write(f"{key}: {value}\n")

            file.write("\n🔹 Tables:\n")
            for i, table in enumerate(data["tables"]):
                file.write(f"\nTable {i+1}:\n")
                for row in table:
                    file.write("\t".join(row) + "\n")
        logging.info(f"✅ Saved TXT: {filename}")
    except Exception as e:
        logging.error(f"❌ Error saving TXT {filename}: {e}")

def save_to_csv(data, filename):
    """Saves extracted data to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write key-value pairs
            writer.writerow(["Key", "Value"])
            for key, value in data["key_value_pairs"].items():
                writer.writerow([key, value])

            # Write tables
            for i, table in enumerate(data["tables"]):
                writer.writerow([])  # Empty line for separation
                writer.writerow([f"Table {i+1}"])
                for row in table:
                    writer.writerow(row)

        logging.info(f"✅ Saved CSV: {filename}")
    except Exception as e:
        logging.error(f"❌ Error saving CSV {filename}: {e}")

# 🔹 Process all files in the folder
for file_name in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file_name)
    ext = file_name.lower().split(".")[-1]

    # Convert PDFs to images
    if ext == "pdf":
        logging.info(f"🔄 Converting PDF: {file_name}...")
        image_paths = convert_pdf_to_images(file_path)
    else:
        image_paths = [file_path]

    # Process each image
    for img_path in image_paths:
        logging.info(f"📄 Processing: {img_path}...")
        response = analyze_document(img_path)

        if response:
            formatted_data = format_textract_data(response)

            # Output file names
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            txt_output = os.path.join(output_folder, f"{base_name}.txt")
            csv_output = os.path.join(output_folder, f"{base_name}.csv")

            # Save data
            save_to_text(formatted_data, txt_output)
            save_to_csv(formatted_data, csv_output)
        else:
            logging.warning(f"⚠️ Skipped: {img_path}")

logging.info("\n🎉 All valid files processed & saved in: " + output_folder)
