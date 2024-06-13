import click
import preprocessing
import matplotlib.pyplot as plt


@click.command()
@click.argument('filename', type=click.Path(exists=True))  # defining wrapper argument as name of the file
def getimage(filename):
    orig_im_arr, proces_im_arr = preprocessing.good_image(filename)  # calling imported image preprocessing module
    plt.subplot(221), plt.imshow(orig_im_arr[0])
    plt.subplot(222), plt.imshow(proces_im_arr[0])
    plt.subplot(223), plt.imshow(orig_im_arr[1])
    plt.subplot(224), plt.imshow(proces_im_arr[1])
    plt.suptitle('Image preprocessing', fontsize=10)
    plt.show()  # visualisation is adopted to two page test file.


if __name__ == '__main__':
    getimage()
