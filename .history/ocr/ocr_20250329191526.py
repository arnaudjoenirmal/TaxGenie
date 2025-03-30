import pytesseract
import cv2
import numpy as np
from PIL import Image

# Load the uploaded image
image_path = "/mnt/data/image.png"
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply noise reduction and thresholding
gray = cv2.GaussianBlur(gray, (3, 3), 0)
gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             cv2.THRESH_BINARY, 11, 2)

# Convert image to PIL format for OCR
pil_image = Image.fromarray(gray)

# Perform OCR
custom_config = "--oem 3 --psm 6"
extracted_text = pytesseract.image_to_string(pil_image, config=custom_config)

# Output extracted text
extracted_text
