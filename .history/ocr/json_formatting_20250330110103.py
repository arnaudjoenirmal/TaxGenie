import os
import json
import glob
from datetime import datetime

def clean_key(key):
    return key.lower().replace(" ", "_").replace("-", "_").replace("/", "_").replace("*", "").replace(".", "").strip("_:")

def clean_value(value):
    if isinstance(value, str):
        value = value.strip()
        
        if any(char.isdigit() for char in value):  # Only process numbers
            value = value.replace(",", "").replace(" ", "")  # Remove spaces & commas
            
            try:
                if "." in value:
                    return float(value)  # Convert to float
                return int(value)  # Convert to int
            except ValueError:
                pass  # If conversion fails, keep it as string
        
        # Convert date formats
        try:
            return datetime.strptime(value, "%d/%b/%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass
    return value  # Return cleaned value

def process_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    cleaned_data = {"account_info": {}, "transactions": []}
    
    if "key_value_pairs" in data:
        for key, value in data["key_value_pairs"].items():
            cleaned_key = clean_key(key)
            cleaned_value = clean_value(value)
            cleaned_data["account_info"][cleaned_key] = cleaned_value
    
    if "tables" in data:
        for table in data["tables"]:
            headers = table[0]  # First row is headers
            for row in table[1:]:  # Remaining rows are data
                transaction = {}
                for i, cell in enumerate(row):
                    if i < len(headers):
                        transaction[clean_key(headers[i])] = clean_value(cell)
                if transaction:
                    cleaned_data["transactions"].append(transaction)
    
    return cleaned_data

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_path in glob.glob(os.path.join(input_folder, "*.json")):
        try:
            cleaned_json = process_json(file_path)
            output_file = os.path.join(output_folder, os.path.basename(file_path))
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(cleaned_json, f, indent=4)
            print(f"✅ Processed: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"❌ Error processing {os.path.basename(file_path)}: {e}")

# Change these paths accordingly
input_folder = "D:/TaxGenie_dataset"
output_folder = "D:/TaxGenie/ocr/processed_json"
process_folder(input_folder, output_folder)
