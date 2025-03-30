import os
import json
from datetime import datetime

def clean_date(date_str):
    if isinstance(date_str, str):
        try:
            return datetime.strptime(date_str, "%d/%b/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return date_str  # Return as is if format is unexpected
    return date_str  # Return as is if not a string

def process_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Process account info
    account_info = {}
    for key, value in data.get("key_value_pairs", {}).items():
        cleaned_key = key.lower().replace(" ", "_").replace("/", "_").replace(":", "").strip()
        if "date" in cleaned_key:
            value = clean_date(value)
        elif value.replace(',', '').replace('.', '').isdigit():
            value = float(value.replace(',', ''))  # Convert numbers to float
        account_info[cleaned_key] = value
    
    # Process transactions
    transactions = []
    for table in data.get("tables", []):
        if table and isinstance(table, list) and len(table) > 1:
            headers = table[0]
            for row in table[1:]:
                transaction = {headers[i].lower().replace(" ", "_"): clean_date(row[i]) if "date" in headers[i].lower() else row[i] for i in range(len(headers))}
                transactions.append(transaction)
    
    # New structured data
    cleaned_data = {"account_info": account_info, "transactions": transactions}
    return cleaned_data

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            
            cleaned_json = process_json(input_path)
            
            with open(output_path, 'w', encoding='utf-8') as output_file:
                json.dump(cleaned_json, output_file, indent=4)
            
            print(f"✅ Processed: {file_name}")

# Example usage
input_folder = "D:/TaxGenie_dataset"  # Update with your actual input folder
output_folder = "D:/TaxGenie_dataset/cleaned_json"  # Update with your desired output folder
process_folder(input_folder, output_folder)
