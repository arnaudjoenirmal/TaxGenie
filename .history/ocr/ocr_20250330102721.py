import boto3
import json
import os
import csv
import logging
import time

# 🔹 Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 AWS Credentials (Use IAM Roles or environment variables in production!)
aws_access_key = "YOUR_AWS_ACCESS_KEY"
aws_secret_key = "YOUR_AWS_SECRET_KEY"
region = "us-east-1"

# 🔹 Initialize Textract Client
try:
    textract = boto3.client(
        "textract",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )
    logging.info("✅ AWS Textract client initialized successfully.")
except Exception as e:
    logging.error(f"❌ AWS Textract Initialization Error: {e}")
    exit(1)

# 🔹 Paths
input_folder = "D:/TaxGenie/Bank Statement/"
output_folder = "D:/TaxGenie_dataset/"
os.makedirs(output_folder, exist_ok=True)

def analyze_document(image_path):
    """Extracts structured data (forms & tables) from an image."""
    try:
        with open(image_path, "rb") as file:
            img_bytes = file.read()

        response = textract.analyze_document(
            Document={'Bytes': img_bytes},
            FeatureTypes=["FORMS", "TABLES"]
        )
        return response
    except Exception as e:
        logging.error(f"❌ Textract Error for {image_path}: {e}")
        return None

def start_pdf_analysis(pdf_path):
    """Starts asynchronous processing for PDFs using Textract."""
    try:
        with open(pdf_path, "rb") as file:
            pdf_bytes = file.read()

        response = textract.start_document_analysis(
            DocumentLocation={'Bytes': pdf_bytes},
            FeatureTypes=["FORMS", "TABLES"]
        )
        return response["JobId"]
    except Exception as e:
        logging.error(f"❌ Error starting PDF analysis: {e}")
        return None

def check_textract_status(job_id):
    """Polls AWS Textract until processing is complete."""
    while True:
        response = textract.get_document_analysis(JobId=job_id)
        status = response["JobStatus"]
        if status in ["SUCCEEDED", "FAILED"]:
            return response if status == "SUCCEEDED" else None
        logging.info("⏳ Waiting for Textract to complete...")
        time.sleep(5)

def format_textract_data(response):
    """Formats Textract response into structured JSON format."""
    key_value_pairs = {}
    tables = []
    block_map = {block["Id"]: block for block in response.get("Blocks", [])}
    
    for block in response.get("Blocks", []):
        if block["BlockType"] == "KEY_VALUE_SET" and "KEY" in block["EntityTypes"]:
            key_text = get_text_from_block(block, block_map)
            value_text = get_text_from_block(find_value_block(block, block_map), block_map)
            if key_text:
                key_value_pairs[key_text] = value_text
    
        if block["BlockType"] == "TABLE":
            table = []
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    row = [get_text_from_block(block_map.get(cell_id), block_map) for cell_id in relationship["Ids"]]
                    if row:
                        table.append(row)
            if table:
                tables.append(table)
    
    return {"key_value_pairs": key_value_pairs, "tables": tables}

def get_text_from_block(block, block_map):
    """Extracts text from a Textract block."""
    if not block or "Relationships" not in block:
        return ""
    return " ".join(block_map.get(child_id, {}).get("Text", "") for rel in block["Relationships"] if rel["Type"] == "CHILD" for child_id in rel["Ids"]).strip()

def find_value_block(key_block, block_map):
    """Finds the corresponding value block for a key block."""
    for relationship in key_block.get("Relationships", []):
        if relationship["Type"] == "VALUE":
            return block_map.get(relationship["Ids"][0])
    return None

def save_to_json(data, filename):
    """Saves extracted data to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        logging.info(f"✅ Saved JSON: {filename}")
    except Exception as e:
        logging.error(f"❌ Error saving JSON {filename}: {e}")

def save_to_csv(data, filename):
    """Saves extracted data to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Key", "Value"])
            for key, value in data["key_value_pairs"].items():
                writer.writerow([key, value])
            for i, table in enumerate(data["tables"]):
                writer.writerow([])
                writer.writerow([f"Table {i+1}"])
                writer.writerows(table)
        logging.info(f"✅ Saved CSV: {filename}")
    except Exception as e:
        logging.error(f"❌ Error saving CSV {filename}: {e}")

# 🔹 Process all files in the folder
for file_name in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file_name)
    ext = file_name.lower().split(".")[-1]
    
    response = None
    if ext in ["jpg", "png"]:
        logging.info(f"📄 Processing image: {file_name}...")
        response = analyze_document(file_path)
    elif ext == "pdf":
        logging.info(f"📄 Processing PDF: {file_name}...")
        job_id = start_pdf_analysis(file_path)
        response = check_textract_status(job_id) if job_id else None
    else:
        logging.warning(f"⚠️ Skipping unsupported file: {file_name}")
        continue
    
    if response:
        formatted_data = format_textract_data(response)
        save_to_json(formatted_data, os.path.join(output_folder, f"{file_name}.json"))
        save_to_csv(formatted_data, os.path.join(output_folder, f"{file_name}.csv"))

logging.info(f"\n🎉 All valid files processed & saved in: {output_folder}")
