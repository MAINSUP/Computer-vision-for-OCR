import click
import preprocessing
import ToDocx
import LayoutParser
# import matplotlib.pyplot as plt
import datetime
import warnings
warnings.filterwarnings('ignore')


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--language", "-l", multiple=False, default="en")
@click.argument('filename', type=click.Path(exists=True))  # defining wrapper argument as name of the file
def ocr(filename, language):
    """
    Kindly enter language code prior to text recognition. There are total 80 supported languages.
        The most commonly used are: en (English), es (Spanish), fr (French),
        de (German), hi (Hindi), ch_sim (Simplified Chinese), uk (Ukrainian), etc.
        Default is English.
        For example, to process PDF in French, run the following command:
        main.py -l es test.pdf
    """
    pproces_im_arr = getimage(filename)
    file = getlayout(pproces_im_arr)
    docx_file = ToDocx.to_dox(file, language)
    return docx_file.save('{}.docx'.format(datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")))


def getimage(filename):
    orig_im_arr, pproces_im_arr = preprocessing.good_image(filename)  # calling imported image preprocessing module
    # plt.subplot(211), plt.imshow(orig_im_arr[0])
    # plt.subplot(212), plt.imshow(pproces_im_arr[0])
    # plt.suptitle('Image preprocessing', fontsize=10)
    # plt.show()  # visualisation of the 1st page of test file.
    return pproces_im_arr


def getlayout(pproces_im_arr):
    file = []
    print("Performing text regions detections")
    for page in pproces_im_arr:
        textim_arr = LayoutParser.layout_parser(page)
        file.append(textim_arr)
    return file


if __name__ == '__main__':
    ocr()
