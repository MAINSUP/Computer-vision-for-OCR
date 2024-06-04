import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import time
from IPython.display import display
import cv2
import PIL
import fitz
import tensorflow
import streamlit as st

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from glob import glob
import matplotlib.pyplot as plt
import matplotlib.image as implt
from IPython.display import clear_output as cls

import tensorflow as tf
import tensorflow.data as tfd
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

st.title("Image to Text App")


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
    display(result, json_output)