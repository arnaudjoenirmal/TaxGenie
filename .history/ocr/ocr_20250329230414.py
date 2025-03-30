import boto3

# 🔹 Manually enter AWS credentials
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

def extract_text_from_image(image_path):
    """Extracts text from an image or document using Amazon Textract."""
    with open(image_path, "rb") as file:
        img_bytes = file.read()

    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': img_bytes})

    extracted_text = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':  # Get line-by-line text
            extracted_text.append(block['Text'])

    return "\n".join(extracted_text)

# 🔹 Example Usage
image_path = "document.jpg"  # Change this to your file path
text = extract_text_from_image(image_path)

print("\nExtracted Text:\n", text)
