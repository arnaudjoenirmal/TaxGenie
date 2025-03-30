import boto3
import json
import os
import csv

# 🔹 AWS Credentials
aws_access_key = "YOUR_AWS_ACCESS_KEY"
aws_secret_key = "YOUR_AWS_SECRET_KEY"
region = "us-east-1"  # Change if needed

# 🔹 Initialize Textract client
textract = boto3.client(
    "textract",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region
)

# 🔹 Paths
input_folder = "D:/TaxGenie/Bank Statement/"  # Folder containing images
output_folder = "D:/TaxGenie/Processed/"  # Folder to save CSV/TXT files
os.makedirs(output_folder, exist_ok=True)  # Create output folder if not exists

def analyze_document(image_path):
    """Extracts structured data (forms & tables) from an image or PDF."""
    with open(image_path, "rb") as file:
        img_bytes = file.read()

    response = textract.analyze_document(
        Document={'Bytes': img_bytes},
        FeatureTypes=["FORMS", "TABLES"]  # Extracts labeled key-value pairs & tables
    )
    return response

def format_textract_data(response):
    """Formats Textract response into structured key-value pairs and tables."""
    key_value_pairs = {}
    tables = []
    block_map = {block["Id"]: block for block in response["Blocks"]}

    # Extract key-value pairs (Forms)
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if "KEY" in block["EntityTypes"]:
                key_text = get_text_from_block(block, block_map)
                value_block = find_value_block(block, block_map)
                value_text = get_text_from_block(value_block, block_map)
                if key_text:
                    key_value_pairs[key_text] = value_text

    # Extract tables
    for block in response["Blocks"]:
        if block["BlockType"] == "TABLE":
            table = []
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    row = []
                    for cell_id in relationship["Ids"]:
                        cell = block_map[cell_id]
                        if cell["BlockType"] == "CELL":
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
                    text += block_map[child_id].get("Text", "") + " "
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
    with open(filename, "w", encoding="utf-8") as file:
        file.write("🔹 Key-Value Pairs:\n")
        for key, value in data["key_value_pairs"].items():
            file.write(f"{key}: {value}\n")

        file.write("\n🔹 Tables:\n")
        for i, table in enumerate(data["tables"]):
            file.write(f"\nTable {i+1}:\n")
            for row in table:
                file.write("\t".join(row) + "\n")

def save_to_csv(data, filename):
    """Saves extracted data to a CSV file."""
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

# 🔹 Process all files in the folder
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".pdf")):  # Only process supported formats
        file_path = os.path.join(input_folder, file_name)
        print(f"📄 Processing: {file_name}...")

        response = analyze_document(file_path)
        formatted_data = format_textract_data(response)

        # Output file names
        base_name = os.path.splitext(file_name)[0]
        txt_output = os.path.join(output_folder, f"{base_name}.txt")
        csv_output = os.path.join(output_folder, f"{base_name}.csv")

        # Save data
        save_to_text(formatted_data, txt_output)
        save_to_csv(formatted_data, csv_output)

        print(f"✅ Saved: {txt_output}, {csv_output}")

print("\n🎉 All files processed and saved in", output_folder)
