# 🧠 OCR 벤치마크: Tesseract vs EasyOCR vs PaddleOCR

이 프로젝트는 세 가지 OCR 라이브러리인 **Tesseract**, **EasyOCR**, **PaddleOCR**를 **영어**, **한국어**, **베트남어** 세 언어와 **타이핑** 및 **손글씨** 두 가지 입력 유형에서 벤치마크합니다.

---

## 📌 목적

이 프로젝트의 목표는 다음 기준에 따라 OCR 성능을 평가 및 비교하는 것입니다:

- ✅ **정확도**: OCR 출력이 실제 정답과 얼마나 유사한지 기반
- ⏱️ **실행 시간**: 각 이미지를 처리하는 데 걸린 시간
- 🌐 **언어 지원**: 한국어, 베트남어, 영어 포함
- 🐤 **텍스트 유형**: 타이핑된 텍스트 및 손글씨

---

## ⚙️ 설치 방법

### 🖥️ 요구사항

다음 파이썬 패키지를 설치하세요:

```bash
pip install pytesseract easyocr paddleocr opencv-python pandas tabulate
```

그리고 Tesseract OCR을 수동으로 설치하세요:

- Windows: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

필요한 경우, 파이썬 스크립트에서 Tesseract 경로를 지정하세요:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 🧠 코드 설명

### 📋 파일 구조

```
ocr-comparison-benchmark/
├── images/                  # 입력 테스트 이미지
├── ocr_results_final_2.csv  # 출력 결과 파일
├── ocr_test_final_2.py      # 메인 벤치마크 스크립트
└── README.md                # 이 설명 파일
```

### 🔄 작동 방식

1. **전처리**:

   - 이미지를 그레이스케일로 변환
   - 필요한 경우 이진화 적용

2. **OCR 엔진**:

   - Tesseract (pytesseract 이용)
   - EasyOCR (`easyocr.Reader` 이용)
   - PaddleOCR (`PaddleOCR` 이용)

3. **평가**:

   - `difflib.SequenceMatcher`를 사용하여 OCR 결과와 실제 정답을 비교
   - 각 OCR 엔진의 실행 시간 측정

4. **결과 출력**:

   - 결과를 `ocr_results_final_2.csv` 파일에 저장
   - `tabulate` 설치 시, 결과 표로 출력 가능

---

## 📊 결과 파일 (ocr_results_final_2.csv) 설명

각 행은 하나의 테스트 이미지와 그에 대한 OCR 결과를 나타냅니다:

| 열 이름              | 의미                                           |
|---------------------|----------------------------------------------|
| `Image`             | 이미지 파일 이름                               |
| `Lang`              | 언어 코드: `eng`, `kor`, `vie`                |
| `Tesseract_Acc`     | Tesseract의 정확도 (%)                         |
| `Tesseract_Sec`     | Tesseract 처리 시간 (초)                        |
| `Tesseract_Output`  | Tesseract의 원시 OCR 텍스트                    |
| `EasyOCR_Acc`       | EasyOCR의 정확도 (%)                           |
| `EasyOCR_Sec`       | EasyOCR 처리 시간 (초)                          |
| `EasyOCR_Output`    | EasyOCR의 원시 OCR 텍스트                      |
| `PaddleOCR_Acc`     | PaddleOCR의 정확도 (%)                         |
| `PaddleOCR_Sec`     | PaddleOCR 처리 시간 (초)                        |
| `PaddleOCR_Output`  | PaddleOCR의 원시 OCR 텍스트                    |

---

## 📄 예시 해석

- Tesseract: 영어, 한국어, 베트남어 타이핑된 텍스트에서 높은 정확도와 빠른 속도를 보여줌. 손글씨는 여전히 어려움.
- EasyOCR: 타이핑된 텍스트에서 좋은 성능. 손글씨는 세 언어 모두에서 여전히 어려움. 특히 한국어에서 다른 엔진보다 좋은 성능.
- PaddleOCR: 타이핑과 손글씨 모두에서 추출 성능이 낮음.

---

## 📂 참고사항

- 손글씨는 모든 엔진에서 어려운 과제입니다.
- 다음과 같은 방식으로 벤치마크를 확장할 수 있습니다:
  - 더 많은 언어 추가
  - 다양한 OCR 엔진 사용
  - 전처리 기술 튜닝

--

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
    




