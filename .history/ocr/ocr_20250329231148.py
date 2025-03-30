import boto3
import json

# 🔹 Manually enter AWS credentials
aws_access_key = "AKIAWOAVSEXOS5QN5CFG"
aws_secret_key = "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"
region = "us-east-1"  # Change if needed

# 🔹 Initialize Textract client
textract = boto3.client(
    "textract",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region
)

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

# 🔹 Example Usage
image_path = "D:/TaxGenie/Bank Statement\27.jpg"  # Change this to your file path

# Call Amazon Textract and get structured data
response = analyze_document(image_path)
formatted_data = format_textract_data(response)

# Print the structured output
print("\n🔹 Extracted Key-Value Pairs:")
print(json.dumps(formatted_data["key_value_pairs"], indent=4))

print("\n🔹 Extracted Tables:")
for i, table in enumerate(formatted_data["tables"]):
    print(f"\nTable {i+1}:")
    for row in table:
        print(row)
