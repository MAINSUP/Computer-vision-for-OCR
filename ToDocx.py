from docx import Document
from docx.enum.section import WD_SECTION
import easyocr


def to_dox(file, language):
    document = Document()  # creating Word document instance
    reader = easyocr.Reader([language])  # calling ocr reader
    print("Extracting text to docx file")
    for page in file:
        for segment in page:
            p = document.add_paragraph()  # for each text layout segment, a separate paragraph is created
            result = reader.readtext(segment)  # and filled with predicted text
            for (bbox, text, prob) in result:
                p.add_run(text)
    document.add_section(start_type=WD_SECTION.NEW_PAGE)
    return document
