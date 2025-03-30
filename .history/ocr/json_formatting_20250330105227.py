import json
import os
import re
from datetime import datetime

input_folder = "D:\TaxGenie_dataset"
output_folder = "D:\TaxGenie_dataset\cleaned"
os.makedirs(output_folder, exist_ok=True)

def clean_key(key):
    """Format key to lowercase, replace special chars with underscores, and remove trailing underscores."""
    key = key.lower().strip().replace(" ", "_").replace("/", "_").replace("-", "_")
    key = re.sub(r"_+", "_", key)  # Replace multiple underscores with a single one
    return key.rstrip("_")  # Remove trailing underscores

def clean_value(value):
    """Convert numeric values and clean strings."""
    if isinstance(value, str):
        value = value.strip()
        # Convert to float if it looks like a number
        if re.match(r"^\d{1,3}(,\d{3})*(\.\d+)?$", value):  
            return float(value.replace(",", ""))
    return value

def clean_date(date_str):
    """Convert various date formats to YYYY-MM-DD"""
    try:
        return datetime.strptime(date_str, "%d/%b/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # Return original if format is unknown

def process_json(file_path):
    """Read and clean JSON data."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    cleaned_data = {"account_info": {}, "transactions": []}

    # Process account info
    for key, value in data.get("key_value_pairs", {}).items():
        clean_k = clean_key(key)
        clean_v = clean_value(value)

        # Format date fields
        if "date" in clean_k or "period" in clean_k:
            clean_v = clean_date(clean_v)

        if clean_k and clean_v != "":
            cleaned_data["account_info"][clean_k] = clean_v

    # Process transactions
    if "tables" in data and len(data["tables"]) > 0:
        transaction_table = data["tables"][0]  # Assuming first table is transactions
        headers = [clean_key(h) for h in transaction_table[0]]  # Process headers

        for row in transaction_table[1:]:
            transaction = {headers[i]: clean_value(row[i]) for i in range(len(headers))}
            cleaned_data["transactions"].append(transaction)

    return cleaned_data

# Process JSON files
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)
        cleaned_json = process_json(file_path)

        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_json, f, indent=4)

        print(f"✅ Processed: {filename}")

print("\n🎉 JSON Cleaning Complete! Saved in:", output_folder)
