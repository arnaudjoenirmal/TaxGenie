import json
from datetime import datetime

def clean_date(date_str):
    """Convert date from 'DD/Mon/YYYY' to 'YYYY-MM-DD'"""
    try:
        return datetime.strptime(date_str, "%d-%b-%Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # Return as is if conversion fails

def clean_amount(amount):
    """Convert amount to float, handling empty values."""
    if amount and isinstance(amount, str):
        return float(amount.replace(",", ""))
    return 0.0

def extract_transactions(json_data):
    """Extracts transaction data from JSON and formats it correctly."""
    transactions = []
    
    if "tables" in json_data and json_data["tables"]:
        table_data = json_data["tables"][0]  # Extract first table
        
        if len(table_data) > 1:
            headers = table_data[0]  # First row contains column headers
            
            for row in table_data[1:]:  # Iterate through data rows
                transaction = dict(zip(headers, row))  # Map headers to row values
                
                # Format values
                transaction["Trans Date"] = clean_date(transaction.get("Trans Date", ""))
                transaction["Value Date"] = clean_date(transaction.get("Value Date", ""))
                transaction["Debit"] = clean_amount(transaction.get("Debit"))
                transaction["Credit"] = clean_amount(transaction.get("Credit"))
                transaction["Balance"] = clean_amount(transaction.get("Balance"))
                
                transactions.append(transaction)
    
    return transactions

def format_json(file_path):
    """Reads, formats, and writes a JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Extract account information
    account_info = {k.lower().replace(" ", "_"): v for k, v in data.get("key_value_pairs", {}).items()}
    
    # Extract and format transactions
    transactions = extract_transactions(data)
    
    # Build the final formatted JSON
    formatted_json = {
        "account_info": account_info,
        "transactions": transactions
    }
    
    # Save formatted JSON
    output_path = file_path.replace(".json", "_formatted.json")
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(formatted_json, outfile, indent=4)
    
    print(f"✅ Processed and saved: {output_path}")
    return formatted_json

# Example Usage
if __name__ == "__main__":
    file_path = "D:\\TaxGenie\\ocr\\88.jpg.json"  # Update with actual file path
    formatted_data = format_json(file_path)
