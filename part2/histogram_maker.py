import numpy as np
from PIL import Image


class HistogramHandler:
    def __init__(self, img_path=None, img_arr=None, channel_arr=None, is_color=False, make_cdf=True):
        if img_path is not None:
            self.__img_path = img_path
            self.__img = Image.open(img_path)
            self.__img_arr = np.array(self.__img)
        elif img_arr is not None:
            self.__img_arr = img_arr
        elif channel_arr is not None:
            self.__channel_arr = channel_arr

        self.__color = is_color
        # now defining cdf histogram arrays
        self.__gray_cdf = np.zeros((1, 256))
        self.__red_cdf = np.zeros((1, 256))
        self.__green_cdf = np.zeros((1, 256))
        self.__blue_cdf = np.zeros((1, 256))
        if make_cdf:
            cdfs = get_img_cdfs(img_arr)
            if is_color:
                self.__red_cdf = cdfs[0]
                self.__green_cdf = cdfs[1]
                self.__blue_cdf = cdfs[2]
            else:
                self.__gray_cdf = cdfs[0]

    def get__gray_cdf(self):
        return self.__gray_cdf

    def get__red_cdf(self):
        return self.__red_cdf

    def get__green_cdf(self):
        return self.__green_cdf

    def get__blue__cdf(self):
        return self.__blue_cdf

    def is_colorful(self):
        return self.__color

    def set__gray_cdf(self, gray_cdf):
        self.__gray_cdf = gray_cdf

    def set__red_cdf(self, red_cdf):
        self.__red_cdf = red_cdf

    def set__green_cdf(self, green_cdf):
        self.__green_cdf = green_cdf

    def set__blue_cdf(self, blue_cdf):
        self.__blue_cdf = blue_cdf


def make_channel_hist_arr(channel_arr: np.ndarray):
    hist_arr = np.zeros((1, 256))
    for i in range(channel_arr.shape[0]):
        for j in range(channel_arr.shape[1]):
            hist_arr[0, channel_arr[i, j]] += 1
    return hist_arr


def make_cdf_hist(hist_arr: np.ndarray):
    cdf = np.zeros((1, 256))
    cdf[0, 0] = hist_arr[0, 0]
    for j in range(1, 256):
        cdf[0, j] = cdf[0, j - 1] + hist_arr[0, j]
    return cdf


def get_img_cdfs(img_arr):
    cdf_list = []
    for i in range(img_arr.shape[2]):
        cdf_list.append(make_cdf_hist(make_channel_hist_arr(img_arr[:, :, i])))

    return cdf_list


def map_channel(src_cdf, ref_cdf, src_channel_img_arr):
    mapped_img_channel_arr = np.copy(src_channel_img_arr)
    for i in range(256):
        new_val = __map_value2new_value(src_cdf[0, i], ref_cdf)
        replace_value(mapped_img_channel_arr, i, new_val)

    return mapped_img_channel_arr


def replace_value(src_channel_img_arr, old_val, new_val):
    for i in range(src_channel_img_arr.shape[0]):
        for j in range(src_channel_img_arr.shape[1]):
            if src_channel_img_arr[i, j] == old_val:
                src_channel_img_arr[i, j] = new_val


def __map_value2new_value(val, ref_cdf):
    nearest_val = 0
    for i in range(256):
        if abs(ref_cdf[0, i] - val) < abs(ref_cdf[0, nearest_val] - val):
            nearest_val = i

    return nearest_val


def rgb2gray(color_img):
    return color_img.convert('L')

# def print(self):
#     plt.bar(range(256), self.red_cdf.reshape((256, )), color='red')
#     print("here")
