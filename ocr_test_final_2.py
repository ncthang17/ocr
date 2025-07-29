import pytesseract
import easyocr
import cv2
import time
import difflib
import os
from paddleocr import PaddleOCR
import pandas as pd

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Preprocess image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

# Normalize text
def normalize_text(text):
    return ' '.join(text.strip().lower().split())

# Accuracy function
def get_accuracy(gt, pred):
    matcher = difflib.SequenceMatcher(None, normalize_text(gt), normalize_text(pred))
    return round(matcher.ratio() * 100, 2)

# Initialize PaddleOCR instances with adjusted parameters
paddleocr_instances = {
    'en': PaddleOCR(use_angle_cls=True, lang='en', det_db_box_thresh=0.5),
    'korean': PaddleOCR(use_angle_cls=True, lang='korean', det_db_box_thresh=0.5),
    'vi': PaddleOCR(use_angle_cls=True, lang='vi', det_db_box_thresh=0.5)
}

# Image and language data
images = [
    ('english_typed.png', 'eng'),
    ('korean_typed.png', 'kor'),
    ('vietnamese_typed.png', 'vie'),
    ('english_handwritten.png', 'eng'),
    ('korean_handwritten.png', 'kor'),
    ('vietnamese_handwritten.png', 'vie')
]

ground_truths = {
    'english_typed.png': "The quick brown fox jumps over the lazy dog.",
    'korean_typed.png': "빠른 갈색 여우가 게으른 개를 뛰어넘습니다.",
    'vietnamese_typed.png': "Con cáo nâu nhanh nhẹn nhảy qua con chó lười biếng.",
    'english_handwritten.png': "The quick brown fox jumps over the lazy dog.",
    'korean_handwritten.png': "빠른 갈색 여우가 게으른 개를 뛰어넘습니다.",
    'vietnamese_handwritten.png': "Con cáo nâu nhanh nhẹn nhảy qua con chó lười biếng."
}

easyocr_langs = {'eng': ['en'], 'kor': ['ko', 'en'], 'vie': ['vi']}

results = []
for img_name, lang in images:
    print(f"\nProcessing: {img_name} | Language: {lang}")
    img_path = os.path.join('./images', img_name)
    image = cv2.imread(img_path)
    if image is None:
        print(f"Error: Failed to load {img_path}")
        continue
    preprocessed_image = preprocess_image(image)

    # Tesseract
    config = f'--oem 3 --psm 6 -l {lang}'
    start = time.time()
    tesseract_out = pytesseract.image_to_string(preprocessed_image, config=config).strip() or ""
    tesseract_time = time.time() - start
    tesseract_acc = get_accuracy(ground_truths[img_name], tesseract_out)

    # EasyOCR
    easyocr_reader = easyocr.Reader(easyocr_langs[lang], gpu=False)
    start = time.time()
    easyocr_out = ' '.join([x[1] for x in easyocr_reader.readtext(preprocessed_image)]) or ""
    easyocr_time = time.time() - start
    easyocr_acc = get_accuracy(ground_truths[img_name], easyocr_out)

    # PaddleOCR with preprocessing
    temp_image_path = "temp_paddle_image.png"
    cv2.imwrite(temp_image_path, preprocessed_image)
    paddleocr = paddleocr_instances[{'eng': 'en', 'kor': 'korean', 'vie': 'vi'}[lang]]
    start = time.time()
    paddle_result = paddleocr.ocr(temp_image_path)
    print(f"PaddleOCR raw output for {img_name}: {paddle_result}")  # Debug output
    paddle_out = ' '.join([line[1][0] for block in paddle_result for line in block if line and line[1]]) or ""
    paddle_time = time.time() - start
    paddle_acc = get_accuracy(ground_truths[img_name], paddle_out)

    results.append({
        'Image': img_name, 'Lang': lang,
        'Tesseract_Acc': tesseract_acc, 'Tesseract_Sec': round(tesseract_time, 2), 'Tesseract_Output': tesseract_out,
        'EasyOCR_Acc': easyocr_acc, 'EasyOCR_Sec': round(easyocr_time, 2), 'EasyOCR_Output': easyocr_out,
        'PaddleOCR_Acc': paddle_acc, 'PaddleOCR_Sec': round(paddle_time, 2), 'PaddleOCR_Output': paddle_out
    })

# Save and display results
df = pd.DataFrame(results)
output_file = "ocr_results_final_2.csv"
try:
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nResults saved to {output_file}")
except PermissionError as e:
    print(f"Error: Could not save to {output_file}. Permission denied. {e}")
    alt_output_file = os.path.join(os.path.expanduser("~"), "Documents", "ocr_results.csv")
    try:
        df.to_csv(alt_output_file, index=False, encoding='utf-8-sig')
        print(f"Results saved to alternative location: {alt_output_file}")
    except Exception as e2:
        print(f"Error: Could not save to {alt_output_file}. {e2}")
except Exception as e:
    print(f"Error: Failed to save results. {e}")

# Display results with fallback if tabulate is missing
try:
    from tabulate import tabulate
    print(tabulate(df, headers='keys', tablefmt='grid'))
except ModuleNotFoundError:
    print("\nWarning: 'tabulate' module not found. Install it with 'pip install tabulate' for formatted table output.")
    print("Displaying raw DataFrame instead:")
    print(df)