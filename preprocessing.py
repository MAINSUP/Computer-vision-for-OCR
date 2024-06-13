import numpy as np
from PIL import Image
from scipy.ndimage import interpolation as inter
import cv2
import pymupdf


def good_image(filename):
    doc = pymupdf.open(filename)  # open pdf document
    orig_im_arr = []
    proces_im_arr = []
    delta = 1
    limit = 5
    angles = np.arange(-limit, limit + delta, delta)

    for page in doc:  # iterate through the pages
        scores = []
        pix = page.get_pixmap()  # render page to an image
        # pix.save("page-%i.png" % page.number)  # store image as a PNG
        pix.tobytes()
        img = Image.frombytes(mode='RGB', size=[pix.width, pix.height], data=pix.samples)  # getting original image
        orig_im_arr.append(img)
        wd, ht = img.size
        nppix = np.array(img.convert('1').getdata(), np.uint8)  # converting to binary image
        bin_img = 1 - (nppix.reshape((ht, wd)) / 255.0)         # for use with scipy interpolation module
        for angle in angles:
            hist, score = find_score(bin_img, angle)
            scores.append(score)
        best_score = max(scores)  # getting best score
        best_angle = angles[scores.index(best_score)]
        print('Best skewness correction angle: {}'.format(best_angle))
        # correct skew
        bin_img = inter.rotate(bin_img, best_angle, reshape=False, order=0)  # rotate image to the best angle
        # skew_img = Image.fromarray((255 * bin_img).astype("uint8")).convert("RGB")
        cu8_img = (bin_img * 255).round().astype(np.uint8)  # converting image to CU8 format for use with CV2
        dst = cv2.fastNlMeansDenoising(cu8_img, None, 20, 70, 15)   # performing denoising
        kernel = np.array([[0, -2, 0],
                           [-1, 6, -1],
                           [0, -1, 0]])                              # sharping image according to
        sharp_img = cv2.filter2D(src=dst, ddepth=-1, kernel=kernel)  # manually tuned coefficient matrix
        proces_im_arr.append(sharp_img)
    return orig_im_arr, proces_im_arr


def find_score(arr, angle):  # utility function to return array of skewness scores
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score
