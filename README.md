# 🧠 OCR Benchmark: Tesseract vs EasyOCR vs PaddleOCR

This project benchmarks three OCR libraries: **Tesseract**, **EasyOCR**, and **PaddleOCR** across three languages (**English**, **Korean**, **Vietnamese**) and two input types (**typed** and **handwritten**).

---

## 📌 Objective

The goal of this project is to evaluate and compare OCR performance using the following criteria:

- ✅ **Accuracy**: Based on how closely the OCR output matches the ground truth.
- ⏱️ **Execution time**: Time taken to process each image.
- 🌐 **Language support**: Includes Korean, Vietnamese, and English.
- 🐤 **Text type**: Both typed and handwritten.

---

## ⚙️ Setup Instructions

### 🖥️ Requirements

Install required Python packages:

```bash
pip install pytesseract easyocr paddleocr opencv-python pandas tabulate
```

Also install Tesseract OCR manually:

- Windows: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

If needed, set Tesseract path in your Python script:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 🧠 Code Explanation

### 📋 File Structure

```
ocr-comparison-benchmark/
├── images/                  # Input test images
├── ocr_results_final_2.csv  # Output results
├── ocr_test_final_2.py      # Main benchmarking script
└── README.md                # This documentation file
```

### 🔄 How It Works

1. **Preprocessing**:

   - Converts image to grayscale.
   - Applies binarization if needed.

2. **OCR Engines**:

   - Tesseract via `pytesseract`
   - EasyOCR via `easyocr.Reader`
   - PaddleOCR via `PaddleOCR`

3. **Evaluation**:

   - Uses `difflib.SequenceMatcher` to compare OCR output with ground truth.
   - Measures execution time for each OCR engine.

4. **Output**:

   - Saves results into `ocr_results_final_2.csv`.
   - Optionally prints result table via `tabulate` (if installed).

---

## 📊 Result File (ocr\_results\_final\_2.csv) Explanation

Each row in the CSV represents one test image and its OCR results:

| Column             | Meaning                                |
| ------------------ | -------------------------------------- |
| `Image`            | Image file name                        |
| `Lang`             | Language code: `eng`, `kor`, `vie`     |
| `Tesseract_Acc`    | Accuracy (%) from Tesseract            |
| `Tesseract_Sec`    | Execution time (seconds) for Tesseract |
| `Tesseract_Output` | Raw OCR text by Tesseract              |
| `EasyOCR_Acc`      | Accuracy (%) from EasyOCR              |
| `EasyOCR_Sec`      | Execution time for EasyOCR             |
| `EasyOCR_Output`   | Raw OCR text by EasyOCR                |
| `PaddleOCR_Acc`    | Accuracy (%) from PaddleOCR            |
| `PaddleOCR_Sec`    | Execution time for PaddleOCR           |
| `PaddleOCR_Output` | Raw OCR text by PaddleOCR              |

---

## 📄 Sample Interpretations (from CSV)

  - Tesseract: achieved higher accuracy and faster speed than the others for typed English, Korean and Vietnamese. Handwritten in three languages is still a challenge.
  - EasyOCR: performed well in typed writing. Handwritten in three languages is still a challenge. Surprisingly, performed quite well in Korean, compared to Tesseract and PaddleOCR.
  - PaddleOCR: failed to extract properly in both typed and handwritten writing.
    
---

## 📂 Notes

- Handwritten text is more difficult for all engines.
- You can expand this benchmark by:
  - Adding more languages
  - Using different OCR engines
  - Tuning preprocessing techniques
    




