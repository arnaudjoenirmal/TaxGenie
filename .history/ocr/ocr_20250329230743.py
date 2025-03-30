import json

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
with open("textract_response.json", "r") as f:
    textract_response = json.load(f)  # Load Textract JSON response

formatted_data = format_textract_data(textract_response)

print("\n🔹 Key-Value Pairs:")
print(json.dumps(formatted_data["key_value_pairs"], indent=4))

print("\n🔹 Tables:")
for i, table in enumerate(formatted_data["tables"]):
    print(f"\nTable {i+1}:")
    for row in table:
        print(row)
