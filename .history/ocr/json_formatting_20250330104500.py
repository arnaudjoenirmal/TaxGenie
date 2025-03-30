import json
import os
import re
from datetime import datetime

# Folders
input_folder = ""  # Change this to your actual input folder path
output_folder = ""

os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

def clean_date(date_str):
    """Convert various date formats to YYYY-MM-DD"""
    patterns = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d"]
    for pattern in patterns:
        try:
            return datetime.strptime(date_str, pattern).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None  # Return None if date format is unknown

def clean_amount(amount):
    """Convert string amounts to float, remove commas, and handle currency symbols"""
    if not amount or amount == ".":
        return None
    match = re.search(r"[-+]?\d{1,3}(?:,\d{3})*(?:\.\d+)?", amount.replace("$", ""))
    return float(match.group().replace(",", "")) if match else None

def standardize_json(file_path):
    """Read and clean JSON data"""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Standardized field mapping
    field_mapping = {
        "Balance on June 1:": "opening_balance",
        "Balance on June 30:": "closing_balance",
        "Total money in:": "total_deposits",
        "Total money out:": "total_withdrawals",
        "Account Number:": "account_number",
        "Account Name:": "account_name",
        "Account Type:": "account_type",
        "Statement Period:": "statement_period"
    }

    cleaned_data = {
        "account_info": {},
        "transactions": []
    }

    # Process key-value pairs
    for key, value in data.get("key_value_pairs", {}).items():
        standard_key = field_mapping.get(key, key.lower().replace(" ", "_").replace(":", ""))
        cleaned_data["account_info"][standard_key] = clean_amount(value) if "balance" in standard_key or "money" in standard_key else value

    # Extract transactions
    for table in data.get("tables", []):
        for row in table:
            if len(row) >= 4:
                date = clean_date(row[0])
                transaction = {
                    "date": date,
                    "description": row[1] if len(row) > 1 else "",
                    "withdrawal": clean_amount(row[2]) if len(row) > 2 else None,
                    "deposit": clean_amount(row[3]) if len(row) > 3 else None,
                    "balance": clean_amount(row[4]) if len(row) > 4 else None
                }
                if date:
                    cleaned_data["transactions"].append(transaction)

    return cleaned_data

# Process only JSON files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):  # Ignore CSV and other formats
        file_path = os.path.join(input_folder, filename)
        cleaned_json = standardize_json(file_path)

        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_json, f, indent=4)

        print(f"✅ Processed: {filename}")

print("\n🎉 JSON Processing Complete! All cleaned files saved in:", output_folder)
