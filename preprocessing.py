import numpy as np
from PIL import Image
from scipy.ndimage import rotate
import cv2
import pymupdf


def good_image(filename):
    doc = pymupdf.open(filename)  # open pdf document
    orig_im_arr = []
    pproces_im_arr = []
    delta = 1
    limit = 5
    angles = np.arange(-limit, limit + delta, delta)
    print("Checking page alignment and removing any noise")

    for page in doc:  # iterate through the pages
        scores = []
        pix = page.get_pixmap(dpi=300)  # render page to an image
        # pix.save("page-%i.png" % page.number)  # store image as a PNG
        pix.tobytes()
        img = Image.frombytes(mode='RGB', size=[pix.width, pix.height], data=pix.samples)  # getting original image
        orig_im_arr.append(img)
        wd, ht = img.size
        pix8 = np.array(img.convert('1').getdata(), np.uint8)  # converting to binary image
        bin_img = 1 - (pix8.reshape((ht, wd)) / 255.0)         # for use with scipy interpolation module
        for angle in angles:
            hist, score = find_score(bin_img, angle)
            scores.append(score)
        best_score = max(scores)  # getting best score
        best_angle = angles[scores.index(best_score)]
        print('Best skewness correction angle: {}'.format(best_angle))
        # correct skew
        image = np.array(img)[:, :, ::-1].copy()
        center = (wd // 2, ht // 2)
        rotmat = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        rotated = cv2.warpAffine(image, rotmat, (wd, ht), flags=cv2.INTER_CUBIC,  # rotate image to the best angle
                                 borderMode=cv2.BORDER_REPLICATE)
        dst = cv2.fastNlMeansDenoising(rotated, None, 20, 70, 15)   # performing denoising
        kernel = np.array([[0, -2, 0],
                           [-1, 6, -1],
                           [0, -1, 0]])                              # sharpening image according to
        sharp_img = cv2.filter2D(src=dst, ddepth=-1, kernel=kernel)  # manually tuned coefficient matrix
        pproces_im_arr.append(sharp_img)
    return orig_im_arr, pproces_im_arr


def find_score(arr, angle):  # utility function to return array of skewness scores
    data = rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score
