import streamlit as st
import preprocessing
import ToDocx
import LayoutParser
import fitz
import datetime
from tqdm import tqdm
import subprocess
import sys
import warnings
warnings.filterwarnings('ignore')


detectron2 = 'git+https://github.com/facebookresearch/detectron2.git'


def install(detectron2):
    subprocess.check_call([sys.executable, "-m", "pip", "install", detectron2])


def ocr(uploaded_file, language, curconfidence, blockconfidence, noise):
    """
    Kindly enter language code prior to text recognition. There are total 12 supported languages.
        The most commonly used are: eng (English), spa (Spanish), fra (French),
        deu (German), hin (Hindi), chi_sim (Simplified Chinese), ukr (Ukrainian), etc.
        Default is English.
        For example, to process PDF in French, run the following command:
        main.py -l fra test.pdf
        Options:
        --curconfidence or -cc option sets confidence level (from 0 to 1) for cursive text detection.
        Default is 0.85.
        --blockconfidende or -bc sets confidence level (from 0 to 1) for text block recognition.
        Default is 0.25.
        --noise is a boolean input option. It will be prompted at start to define preprocessing pipeline.
        Default is n (Image does not contain noise).
    """
    text, pixmaps = extract_text_from_pdf(uploaded_file)

    if len(text) == 0:  # if no text found, proceeding to OCR
        pproces_im_arr = getimage(pixmaps, noise)
        file = getlayout(pproces_im_arr, blockconfidence)
        docx_file = ToDocx.im2dox(file, language, curconfidence)
    else:
        docx_file = ToDocx.txt2dox(text)  # passing collected text directly to file creator
    return docx_file.save('{}.docx'.format(datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")))


def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    pixmaps = []
    print("Processing {} page(s)".format(len(doc)))
    for page_num in tqdm(range(len(doc))):
        page = doc.load_page(page_num)
        text += page.get_text()  # collecting text from digital file
        pix = page.get_pixmap(dpi=300)  # render page to a Pixmap with higher resolution
        pixmaps.append(pix)

    return text, pixmaps


def getimage(pixmaps, noise):
    # calling imported image preprocessing module
    pproces_im_arr = preprocessing.good_image(pixmaps, noise)
    return pproces_im_arr


def getlayout(pproces_im_arr, blockconfidence):
    file = []
    print("Performing text regions detection")
    for page in pproces_im_arr:
        file.append(LayoutParser.layout_parser(page, blockconfidence))
    return file


# Streamlit App
st.title("PDF to DOCX Converter with OCR")
language = st.selectbox(
       'Select language',
       ('eng', 'spa', 'fra', 'deu', 'hin', 'chi_sim', 'ukr', 'ara', 'ron', 'pol', 'tur'))
curconfidence = st.slider(
    "Select a handwritting confidence level",
    0.0, 1.0, 0.05)
blockconfidence = st.slider(
    "Select a layout block type confidence level",
    0.0, 1.0, 0.05)
noise = st.checkbox("Does your image contain noise?")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("Processing file...")
    docx_file = ocr(uploaded_file, language, curconfidence, blockconfidence, noise)

    st.write("Conversion completed.")

    with open(docx_file, "rb") as file:
        btn = st.download_button(
            label="Download DOCX",
            data=file,
            file_name=docx_file,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
