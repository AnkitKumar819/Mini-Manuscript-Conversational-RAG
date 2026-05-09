# OCR related logic
# src/ocr.py

import os
import cv2
import easyocr

from tqdm import tqdm

from config import IMAGE_DIR
from config import OCR_OUTPUT_DIR

from utils import create_directory


# ======================================
# INITIALIZE OCR READER
# ======================================

reader = easyocr.Reader(['en'])


# ======================================
# IMAGE PREPROCESSING
# ======================================

def preprocess_image(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Noise reduction
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Binary thresholding
    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh


# ======================================
# OCR EXTRACTION
# ======================================

def extract_text(image_path):

    processed_image = preprocess_image(image_path)

    results = reader.readtext(
        processed_image,
        detail=0
    )

    text = "\n".join(results)

    return text


# ======================================
# MAIN OCR PIPELINE
# ======================================

def run_ocr_pipeline():

    create_directory(OCR_OUTPUT_DIR)

    image_files = sorted(
        os.listdir(IMAGE_DIR)
    )

    for image_file in tqdm(image_files):

        image_path = os.path.join(
            IMAGE_DIR,
            image_file
        )

        extracted_text = extract_text(
            image_path
        )

        output_filename = (
            os.path.splitext(image_file)[0]
            + ".txt"
        )

        output_path = os.path.join(
            OCR_OUTPUT_DIR,
            output_filename
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(extracted_text)

        print(f"Saved: {output_path}")


if __name__ == "__main__":

    run_ocr_pipeline()