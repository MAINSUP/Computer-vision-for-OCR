#importing necessary libraries
import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import time
from IPython.display import display
import streamlit as st

st.title("Image to Text App") # Setting title of the app window
#defining image processing function
def ocr(item):
    model = ocr_predictor("db_resnet50", "crnn_vgg16_bn", pretrained=True)
    result = model(item)
    json_output = result.export()
    return result, json_output

# Uploading an image file
uploaded_file = st.file_uploader(
    "Choose a File", type=["jpg", "jpeg", "png", "pdf"]
)

st.write("#### Or Put an URL")
url = st.text_input("Please type an URL:")

if st.button("Show The URL"):
    st.write("Typed URL:", url)
    start_time = time.time()

    single_img_doc = DocumentFile.from_url(url)
    result, json_output = ocr(single_img_doc)
    display(result, json_output)
#defining switch cases to call the ocr function
elif uploaded_file is not None:
    # start timer
    start_time = time.time()

    if uploaded_file.type == "application/pdf":
        pdf = uploaded_file.read()
        single_img_doc = DocumentFile.from_pdf(pdf)
    else:
        image = uploaded_file.read()
        single_img_doc = DocumentFile.from_images(image)

    result, json_output = ocr(single_img_doc)
    display(result, json_output) #displaying prediction result in the terminal window
