import click
import preprocessing
import ToDocx
import LayoutParser
import fitz
import datetime
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--language", "-l", multiple=False, default="eng")
@click.option("--curconfidence", "-cc", multiple=False, default=0.85)
@click.option("--blockconfidence", "-bc", multiple=False, default=0.25)
@click.option('--noise', prompt='Does your picture(s) contain noise, y/n?', default="n")
@click.argument('filename', type=click.Path(exists=True))  # defining wrapper argument as name of the file
def ocr(filename, language, curconfidence, blockconfidence, noise):
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
    text, pixmaps = extract_text_from_pdf(filename)

    if len(text) == 0:  # if no text found, proceeding to OCR
        pproces_im_arr = getimage(pixmaps, noise)
        file = getlayout(pproces_im_arr, blockconfidence)
        docx_file = ToDocx.im2dox(file, language, curconfidence)
    else:
        docx_file = ToDocx.txt2dox(text)  # passing collected text directly to file creator
    return docx_file.save('{}.docx'.format(datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")))


def extract_text_from_pdf(filename):
    doc = fitz.open(filename)
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


if __name__ == '__main__':
    ocr()
