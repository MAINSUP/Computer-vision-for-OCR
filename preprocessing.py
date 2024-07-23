import numpy as np
from PIL import Image
from scipy.ndimage import rotate
import cv2
from stqdm import stqdm
import warnings
warnings.filterwarnings('ignore')


def good_image(pixmaps, noise):
    pproces_im_arr = []
    delta = 1
    limit = 5
    angles = np.arange(-limit, limit + delta, delta)
    print("Checking page alignment and removing any noise")

    for num, pix in stqdm(enumerate(pixmaps)):  # iterate through the pages
        print("Processing page {}".format(num+1))
        scores = []
        img = Image.frombytes(mode='RGB', size=[pix.width, pix.height], data=pix.samples)  # getting original image
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
        im_data = (bin_img * 255).round().astype(np.uint8)
        center = (wd // 2, ht // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)

        if noise == "y":
            rotated = cv2.warpAffine(im_data, M, (wd, ht), flags=cv2.INTER_CUBIC,  # rotate image to the best angle
                                     borderMode=cv2.BORDER_REPLICATE)
            ret, mask = cv2.threshold(rotated, 0, 255, cv2.THRESH_BINARY_INV)
            dst = cv2.fastNlMeansDenoising(mask, None, 20, 20, 15)   # performing denoising
            kernel = np.array([[10, -1, 5],
                              [-1, -1, -1],
                              [5, -1, 10]])  # sharpening image according to kernel matrix
            sharp_img = cv2.filter2D(src=dst, ddepth=-1, kernel=kernel)  # manually tuned coefficient matrix
            img = cv2.cvtColor(sharp_img, cv2.COLOR_GRAY2BGR)
            # do adaptive threshold on gray image
            thresh = cv2.adaptiveThreshold(sharp_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 25)
            # make background of input white where thresh is white
            result = img.copy()
            result[thresh == 255] = (255, 255, 255)
            pproces_im_arr.append(result)

        else:
            image = np.array(img)[:, :, ::-1].copy()
            result = cv2.warpAffine(image, M, (wd, ht))  # rotate original image to the best angle
            pproces_im_arr.append(result)
    return pproces_im_arr


def find_score(arr, angle):  # utility function to return array of skewness scores
    data = rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score
