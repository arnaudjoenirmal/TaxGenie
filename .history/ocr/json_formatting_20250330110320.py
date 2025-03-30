import os
import json
import re
from datetime import datetime

def clean_number(value):
    """Convert number strings to floats, handle errors."""
    if isinstance(value, (int, float)):
        return value
    value = value.replace(',', '').replace(' ', '')  # Remove commas & spaces
    try:
        return float(value)
    except ValueError:
        return value  # Return original if conversion fails

def clean_date(date_str):
    """Convert various date formats to YYYY-MM-DD."""
    try:
        return datetime.strptime(date_str, "%d/%b/%Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%d-%b-%Y").strftime("%Y-%m-%d")
        except ValueError:
            return date_str  # Return original if conversion fails

def extract_transactions(tables):
    """Extract transactions from tables."""
    transactions = []
    
    for table in tables:
        if not table or len(table) < 2:
            continue  # Skip empty tables
        
        headers = table[0]  # First row is headers
        for row in table[1:]:  # Remaining rows are transactions
            if len(row) < len(headers):
                continue  # Skip incomplete rows
            
            transaction = {}
            for i, header in enumerate(headers):
                key = re.sub(r'[^a-zA-Z0-9_]', '_', header.strip().lower())  # Clean header names
                value = row[i].strip()
                
                if 'date' in key:
                    value = clean_date(value)
                elif 'debit' in key or 'credit' in key or 'balance' in key:
                    value = clean_number(value)
                
                transaction[key] = value
            
            transactions.append(transaction)
    
    return transactions

def process_json(file_path):
    """Process a single JSON file and format it properly."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract key-value pairs into account_info
    account_info = {re.sub(r'[^a-zA-Z0-9_]', '_', k.strip().lower()): clean_number(v.strip()) if isinstance(v, str) else v
                    for k, v in data.get("key_value_pairs", {}).items()}
    
    # Extract transactions from tables
    transactions = extract_transactions(data.get("tables", []))
    
    return {"account_info": account_info, "transactions": transactions}

def process_folder(input_folder, output_folder):
    """Process all JSON files in a folder and save them in another."""
    os.makedirs(output_folder, exist_ok=True)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            
            try:
                cleaned_json = process_json(input_path)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(cleaned_json, f, indent=4)
                print(f'✅ Processed: {file_name}')
            except Exception as e:
                print(f'❌ Error processing {file_name}: {e}')



input_folder = "D:/TaxGenie_dataset"
output_folder = "D:/TaxGenie_dataset/cleaned_json"
process_folder(input_folder, output_folder)
