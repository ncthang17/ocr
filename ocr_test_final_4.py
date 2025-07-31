import pytesseract
import easyocr
import cv2
import time
import difflib
import os
import pandas as pd
from paddleocr import PaddleOCR
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ==== Preprocessing ====
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

# ==== Accuracy ====
def normalize_text(text):
    return ' '.join(text.strip().lower().split())

def get_accuracy(gt, pred):
    matcher = difflib.SequenceMatcher(None, normalize_text(gt), normalize_text(pred))
    return round(matcher.ratio() * 100, 2)

# ==== Language Mapping ====
lang_map = {
    'eng': {'tess': 'eng', 'easy': ['en'], 'paddle': 'en'},
    'kor': {'tess': 'kor', 'easy': ['ko', 'en'], 'paddle': 'korean'},
    'vie': {'tess': 'vie', 'easy': ['vi'], 'paddle': 'vi'}
}

# ==== OCR Initializations ====
easyocr_readers = {k: easyocr.Reader(v['easy'], gpu=False) for k, v in lang_map.items()}
paddleocr_instances = {v['paddle']: PaddleOCR(use_angle_cls=True, lang=v['paddle'], det_db_box_thresh=0.5) for v in lang_map.values()}

# Doctr and TrOCR models (load once)
doctr_model = ocr_predictor(pretrained=True)

trocr_processors = {
    'printed': TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed'),
    'handwritten': TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
}
trocr_models = {
    'printed': VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed'),
    'handwritten': VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
}

# ==== OCR Functions ====
def run_doctr(image_path):
    start = time.time()
    doc = DocumentFile.from_images(image_path)
    result = doctr_model(doc)
    text = result.render()
    elapsed = time.time() - start
    return text, elapsed

def run_trocr(image_path, model_type='handwritten'):
    processor = trocr_processors[model_type]
    model = trocr_models[model_type]
    image = Image.open(image_path).convert("RGB")

    start = time.time()
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    elapsed = time.time() - start
    return text, elapsed

# ==== Data ====
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

# ==== Run OCRs and Collect Results ====
results = []
for img_name, lang in images:
    print(f"\n🔍 Processing: {img_name} | Language: {lang}")
    img_path = os.path.join('./images', img_name)
    image = cv2.imread(img_path)
    if image is None:
        print(f"❌ Could not load {img_path}")
        continue

    pre_img = preprocess_image(image)

    # --- Tesseract ---
    config = f'--oem 3 --psm 6 -l {lang_map[lang]["tess"]}'
    start = time.time()
    tesseract_out = pytesseract.image_to_string(pre_img, config=config).strip() or ""
    tesseract_time = time.time() - start
    tesseract_acc = get_accuracy(ground_truths[img_name], tesseract_out)

    # --- EasyOCR ---
    easyocr_reader = easyocr_readers[lang]
    start = time.time()
    easyocr_out = ' '.join([x[1] for x in easyocr_reader.readtext(pre_img)]) or ""
    easyocr_time = time.time() - start
    easyocr_acc = get_accuracy(ground_truths[img_name], easyocr_out)

    # --- PaddleOCR ---
    paddleocr = paddleocr_instances[lang_map[lang]['paddle']]
    start = time.time()
    paddle_result = paddleocr.ocr(image)
    paddle_time = time.time() - start
    try:
        paddle_out = ' '.join([line[1][0] for block in paddle_result for line in block if line and len(line) > 1]) or ""
    except Exception as e:
        print(f"⚠️ PaddleOCR parsing error: {e}")
        paddle_out = ""
    paddle_acc = get_accuracy(ground_truths[img_name], paddle_out)

    # --- Doctr ---
    try:
        doctr_out, doctr_time = run_doctr(img_path)
        doctr_acc = get_accuracy(ground_truths[img_name], doctr_out)
    except Exception as e:
        doctr_out = f"❌ Doctr Error: {e}"
        doctr_time = 0
        doctr_acc = 0

    # --- TrOCR ---
    trocr_model_type = 'printed' if 'typed' in img_name else 'handwritten'
    try:
        trocr_out, trocr_time = run_trocr(img_path, trocr_model_type)
        trocr_acc = get_accuracy(ground_truths[img_name], trocr_out)
    except Exception as e:
        trocr_out = f"❌ TrOCR Error: {e}"
        trocr_time = 0
        trocr_acc = 0

    # Print summary for this image
    print(f"Tesseract: Acc {tesseract_acc}%, Time {round(tesseract_time,2)}s")
    print(f"EasyOCR: Acc {easyocr_acc}%, Time {round(easyocr_time,2)}s")
    print(f"PaddleOCR: Acc {paddle_acc}%, Time {round(paddle_time,2)}s")
    print(f"Doctr: Acc {doctr_acc}%, Time {round(doctr_time,2)}s")
    print(f"TrOCR ({trocr_model_type}): Acc {trocr_acc}%, Time {round(trocr_time,2)}s")

    # Save results
    results.append({
        'Image': img_name,
        'Lang': lang,
        'Tesseract_Acc': tesseract_acc, 'Tesseract_Sec': round(tesseract_time, 2), 'Tesseract_Output': tesseract_out,
        'EasyOCR_Acc': easyocr_acc, 'EasyOCR_Sec': round(easyocr_time, 2), 'EasyOCR_Output': easyocr_out,
        'PaddleOCR_Acc': paddle_acc, 'PaddleOCR_Sec': round(paddle_time, 2), 'PaddleOCR_Output': paddle_out,
        'Doctr_Acc': doctr_acc, 'Doctr_Sec': round(doctr_time, 2), 'Doctr_Output': doctr_out,
        'TrOCR_Acc': trocr_acc, 'TrOCR_Sec': round(trocr_time, 2), 'TrOCR_Output': trocr_out
    })

# ==== Save CSV ====
df = pd.DataFrame(results)
output_file = "ocr_results_all.csv"
try:
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n📁 Results saved to {output_file}")
except Exception as e:
    print(f"❌ Failed to save CSV: {e}")

# ==== Optional: Display summary with tabulate ====
try:
    from tabulate import tabulate
    print(tabulate(df, headers='keys', tablefmt='grid'))
except ImportError:
    print("\nInstall 'tabulate' for better table display:\n  pip install tabulate")
    print(df)