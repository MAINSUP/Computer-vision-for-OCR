import streamlit as st
import preprocessing
import ToDocx
import LayoutParser
import fitz
import datetime
from stqdm import stqdm
import warnings
warnings.filterwarnings('ignore')


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
    for page_num in stqdm(range(len(doc))):
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
       ('eng', 'spa', 'fra', 'deu', 'ukr', 'ara', 'ron', 'pol', 'tur'))
curconfidence = st.slider(
    "Select a handwritting confidence level",
    min_value=0.0, max_value=1.0, value=0.85, step=0.05)
blockconfidence = st.slider(
    "Select a layout block type confidence level",
    min_value=0.0, max_value=1.0, value=0.25, step=0.05)
# noise = st.checkbox("Does your image contain noise?")
on = st.toggle("Does your image contain noise?")
if on:
    noise = "y"
else:
    noise = "n"

uploaded_files = st.file_uploader("Upload a PDF file", type="pdf", accept_multiple_files=True)
document_list = []
if uploaded_files is not None:
    for num, loaded_file in enumerate(uploaded_files):
        st.write("Processing file...")
        docx_file = ocr(loaded_file, language, curconfidence, blockconfidence, noise)
        document_list.append(datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p"))
        docx_file.save('{}.docx'.format(document_list[0]))
        st.write("Conversion completed.")

for file_name in document_list:
    with open(file_name, "rb") as file:
        btn = st.download_button(
            label="Download DOCX",
            data=file,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

