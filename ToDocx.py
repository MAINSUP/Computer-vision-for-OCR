from docx import Document
from docx.enum.section import WD_SECTION
# #*#import easyocr
# #*#import torch
import pytesseract
import TextStyle
from docx.shared import Pt
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
tessdata_dir_config = "--tessdata-dir 'C:\\Program Files \\Tesseract-OCR\\tessdata\\"


def im2dox(file, language, confidence):
    document = Document()  # creating Word document instance
    # #*# torch.cuda.empty_cache()
    # #*# reader = easyocr.Reader([language], gpu=False)  # calling ocr reader

    print("Extracting text to docx file")
    for ref, page in enumerate(file):
        print("Reading page {}".format(ref+1))
        for segment in tqdm(page):
            p = document.add_paragraph()  # for each text layout segment, a separate paragraph is created
            # #*#result = reader.readtext(segment)  # and filled with predicted text
            result = pytesseract.image_to_string(segment, lang=language, config='--psm 6')
            font_style = TextStyle.text_style(segment, confidence)
            if font_style != 'Cursive':
                # #*#for (bbox, text, prob) in result:
                for text in result:
                    run = p.add_run(text)
                    run.font.size = Pt(14)
            else:
                # #*#for (bbox, text, prob) in result:
                for text in result:
                    run = p.add_run(text)
                    run.font.name = 'Brush Script MT'       # writing cursive font text
                    run.font.size = Pt(14)

    document.add_section(start_type=WD_SECTION.NEW_PAGE)
    return document


def txt2dox(text):
    document = Document()  # creating Word document instance
    p = document.add_paragraph()
    p.add_run(text)    # writing standard font text
    return document

# #*# for use with easyocr lib