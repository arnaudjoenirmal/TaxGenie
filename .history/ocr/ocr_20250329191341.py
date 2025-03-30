# import pytesseract
# import cv2
# import os
# import re
# import numpy as np
# from PIL import Image

# # 🔹 Set path to your dataset
# image_path = r"D:\TaxGenie\Bank Statement\11.jpg"

# # 🔹 Preprocess Image (Grayscale + Noise Reduction + Thresholding + Deskewing)
# def preprocess_image(image_path):
#     if not os.path.exists(image_path):
#         print(f"❌ Error: Image not found at {image_path}")
#         return None
    
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if image is None:
#         print(f"❌ Error: Unable to read image {image_path}")
#         return None
    
#     # 🔹 Apply Noise Reduction
#     image = cv2.GaussianBlur(image, (3, 3), 0)
#     image = cv2.bilateralFilter(image, 9, 75, 75)
    
#     # 🔹 Deskew Image
#     image = deskew_image(image)

#     # 🔹 Adaptive Thresholding
#     image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                   cv2.THRESH_BINARY, 11, 2)

#     return image

# # 🔹 Deskew Image
# def deskew_image(image):
#     coords = np.column_stack(np.where(image > 0))
#     angle = cv2.minAreaRect(coords)[-1]
#     if angle < -45:
#         angle = -(90 + angle)
#     else:
#         angle = -angle
    
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
#     return rotated

# # 🔹 Extract text from the image
# def extract_text_from_image(image_path):
#     processed_image = preprocess_image(image_path)
#     if processed_image is None:
#         return ""
    
#     pil_image = Image.fromarray(processed_image)
#     custom_config = "--oem 3 --psm 6"
#     text = pytesseract.image_to_string(pil_image, config=custom_config)
#     return clean_text(text)

# # 🔹 Clean OCR Text (Post-processing)
# def clean_text(text):
#     text = re.sub(r"[^\w\s.,:-]", "", text)  # Remove unwanted symbols
#     text = re.sub(r"\s+", " ", text)  # Remove extra spaces
#     return text.strip()

# # 🔹 Run OCR on the selected image
# extracted_text = extract_text_from_image(image_path)

# # 🔹 Save extracted text as a .txt file in the same folder
# if extracted_text:
#     output_text_path = os.path.splitext(image_path)[0] + ".txt"
#     with open(output_text_path, "w", encoding="utf-8") as f:
#         f.write(extracted_text)
#     print(f"✅ Processed: {image_path} → Extracted text saved in {output_text_path}")
# else:
#     print(f"⚠️ No text extracted from {image_path}")


