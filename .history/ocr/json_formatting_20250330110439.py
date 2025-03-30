import os
import json
import re

def clean_number(value):
    """Convert number strings to float or int, removing commas and spaces."""
    if isinstance(value, str):
        value = value.replace(',', '').strip()
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            return value  # Return as-is if conversion fails
    return value

def parse_date(value):
    """Convert date formats like '01-Mar-2017' to '2017-03-01'"""
    try:
        return re.sub(r'(\d{2})-(\w{3})-(\d{4})', lambda m: f"{m.group(3)}-{m.group(2)}-{m.group(1)}", value)
    except:
        return value

def extract_transactions(tables):
    """Extract transactions from table format."""
    transactions = []
    
    for table in tables:
        for row in table:
            if len(row) >= 7:  # Ensure row has at least required columns
                date, ref, value_date, debit, credit, balance, remarks = row[:7]
                
                transaction = {
                    "date": parse_date(date),
                    "reference": ref.strip(),
                    "value_date": parse_date(value_date),
                    "debit": clean_number(debit) if debit else 0,
                    "credit": clean_number(credit) if credit else 0,
                    "balance": clean_number(balance),
                    "remarks": remarks.strip()
                }
                transactions.append(transaction)
    
    return transactions

def process_json(file_path):
    """Process individual JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert key_value_pairs to structured format
    account_info = {k.lower().replace(' ', '_'): clean_number(v) for k, v in data.get("key_value_pairs", {}).items()}
    
    # Extract transactions
    transactions = extract_transactions(data.get("tables", []))
    
    return {
        "account_info": account_info,
        "transactions": transactions
    }

def process_folder(input_folder, output_folder):
    """Process all JSON files in a folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.json'):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            
            processed_data = process_json(input_path)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=4)
            
            print(f"✅ Processed: {file_name}")
input_folder = "D:/TaxGenie_dataset"
output_folder = "D:/TaxGenie_dataset/cleaned_json"
process_folder(input_folder, output_folder)
