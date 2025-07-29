# 🧠 OCR Benchmark: Tesseract vs EasyOCR vs PaddleOCR

This project compares the performance of three open-source Optical Character Recognition (OCR) libraries: **Tesseract**, **EasyOCR**, and **PaddleOCR** across **three languages** (English, Korean, Vietnamese) and **two input types** (typed and handwritten text).

---

## 📌 Objective

To evaluate OCR performance based on:
- ✅ **Accuracy** (compared with ground truth)
- ⏱️ **Execution time**
- 🌐 **Language support** (Korean, Vietnamese, English)
- 🔤 **Text type** (typed vs. handwritten)

---

## ⚙️ Setup Instructions

### 🖥️ Requirements

Install required libraries:

```bash
pip install pytesseract easyocr paddleocr opencv-python pandas tabulate

Also install:

Tesseract OCR: https://github.com/tesseract-ocr/tesseract

(Optional) Set Tesseract path in your script:

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

🧠 Code Explanation
📝 Structure
images/                  # Test images
ocr_results_final_2.csv  # Output result file
ocr_test_final_2.py                  # Benchmarking script
README.md

🔄 How It Works
Preprocessing: Converts image to grayscale and binarizes it.

OCR Engines:

Tesseract via pytesseract

EasyOCR via easyocr.Reader

PaddleOCR via PaddleOCR

Comparison:

Normalizes OCR output and ground truth

Uses difflib.SequenceMatcher to calculate accuracy

Measures time taken by each OCR engine

Output:

Saves results into ocr_results_final_2.csv

Optionally displays in terminal using tabulate



