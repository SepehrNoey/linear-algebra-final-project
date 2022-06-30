import numpy as np
from PIL import Image


class Pixel:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x_y(self):
        return self.__x, self.__y


class HistogramHandler:
    def __init__(self, img_path=None, img_arr=None, channel_arr=None, make_cdf=True):
        if img_path is not None:
            self.__img_path = img_path
            self.__img = Image.open(img_path)
            self.__img_arr = np.array(self.__img)
        elif img_arr is not None:
            self.__img_arr = img_arr
        elif channel_arr is not None:
            self.__channel_arr = channel_arr

        self.__multi_channel = True if self.__img_arr.shape[2] > 1 else False
        # now defining cdf histogram arrays
        self.__gray_cdf = np.zeros((1, 256))
        self.__red_cdf = np.zeros((1, 256))
        self.__green_cdf = np.zeros((1, 256))
        self.__blue_cdf = np.zeros((1, 256))
        if make_cdf:
            cdfs, self.__values2pixels_list = get_img_cdfs(self.__img_arr)
            if self.__multi_channel:
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

    def set__gray_cdf(self, gray_cdf):
        self.__gray_cdf = gray_cdf

    def set__red_cdf(self, red_cdf):
        self.__red_cdf = red_cdf

    def set__green_cdf(self, green_cdf):
        self.__green_cdf = green_cdf

    def set__blue_cdf(self, blue_cdf):
        self.__blue_cdf = blue_cdf

    def is_multichannel(self):
        return self.__multi_channel

    def get__img(self):
        return self.__img

    def get_number_of_channels(self):
        return self.__img_arr.shape[2]

    def get_cdf_with_index(self, index):
        if index == 0:
            return self.__gray_cdf
        elif index == 1:
            return self.__red_cdf
        elif index == 2:
            return self.__green_cdf
        else:
            return self.__blue_cdf

    def get_channel_img_arr(self, index):
        if index == 0 or index == 1:
            return self.__img_arr[:, :, 0]
        elif index == 2:
            return self.__img_arr[:, :, 1]
        else:
            return self.__img_arr[:, :, 2]

    def get_channel_values2pixels_dict(self, index):
        if index == 0 or index == 1:
            return self.__values2pixels_list[0]
        elif index == 2:
            return self.__values2pixels_list[1]
        else:
            return self.__values2pixels_list[2]


def make_channel_hist_arr(channel_arr: np.ndarray):
    hist_arr = np.zeros((1, 256))
    values2pixels = {}
    for i in range(channel_arr.shape[0]):
        for j in range(channel_arr.shape[1]):
            hist_arr[0, channel_arr[i, j]] += 1
            if channel_arr[i, j] in values2pixels.keys():
                values2pixels.get(channel_arr[i, j]).append(Pixel(i, j))
            else:
                values2pixels[channel_arr[i, j]] = [Pixel(i, j)]
    return hist_arr, values2pixels


def make_cdf_hist(hist_arr: np.ndarray):
    cdf = np.zeros((1, 256))
    cdf[0, 0] = hist_arr[0, 0]
    for j in range(1, 256):
        cdf[0, j] = cdf[0, j - 1] + hist_arr[0, j]
    return cdf


def get_img_cdfs(img_arr):
    cdf_list = []
    values2pixels_list = []
    for i in range(img_arr.shape[2]):
        hist_arr, values2pixels = make_channel_hist_arr(img_arr[:, :, i])
        cdf_list.append(make_cdf_hist(hist_arr))
        values2pixels_list.append(values2pixels)

    return cdf_list, values2pixels_list


def map_channel(src_cdf, ref_cdf, src_channel_img_arr, src_chan_val2pixels_dict):
    mapped_img_channel_arr = np.copy(src_channel_img_arr)
    for i in range(256):
        new_val = __map_value2new_value(src_cdf[0, i], ref_cdf)
        replace_value(mapped_img_channel_arr, src_chan_val2pixels_dict, i, new_val)

    return mapped_img_channel_arr


def replace_value(src_channel_img_arr, channel_values2pixels_dict, old_val, new_val):
    lst = channel_values2pixels_dict.get(old_val)
    for p in lst:
        i, j = p.get_x_y()
        src_channel_img_arr[i, j] = new_val


def __map_value2new_value(val, rf_cdf):
    nearest_val = 0
    at_least_one_change = False
    at_least_one_failure_after_change = False
    for i in range(256):
        if at_least_one_change and at_least_one_failure_after_change:
            break

        if abs(rf_cdf[0, i] - val) <= abs(rf_cdf[0, nearest_val] - val):
            at_least_one_change = True
            nearest_val = i
        elif at_least_one_change:
            at_least_one_failure_after_change = True

    return nearest_val


def rgb2gray(color_img):
    return color_img.convert('L')


def match_histogram(src_path, ref_path):
    src_handler = HistogramHandler(img_path=src_path)
    ref_handler = HistogramHandler(img_path=ref_path)

    if (not src_handler.is_multichannel()) and ref_handler.is_multichannel():
        print("Not implemented yet!")
    elif (not ref_handler.is_multichannel()) and src_handler.is_multichannel():  # makes src single channel too
        single_channeled = rgb2gray(src_handler.get__img())
        src_handler = HistogramHandler(img_arr=single_channeled)

    if src_handler.get_number_of_channels() == ref_handler.get_number_of_channels():
        channels = []
        if src_handler.get_number_of_channels() == 1:  # single channel
            channels.append(map_channel(src_handler.get_cdf_with_index(0), ref_handler.get_cdf_with_index(0),
                                        src_handler.get_channel_img_arr(0),
                                        src_handler.get_channel_values2pixels_dict(0)))
        else:  # multichannel
            for j in range(1, src_handler.get_number_of_channels() + 1):
                channels.append(map_channel(src_handler.get_cdf_with_index(j), ref_handler.get_cdf_with_index(j),
                                            src_handler.get_channel_img_arr(j),
                                            src_handler.get_channel_values2pixels_dict(j)))

        # now channel(s) are mapped, so we can create the matched image
        cnct_channels = channels[0]
        for j in range(1, len(channels)):
            cnct_channels = np.dstack((cnct_channels, channels[j]))
            # cnct_channels = np.concatenate(cnct_channels[:, :, j - 1], channels[:, :, j], axis=1)

        return cnct_channels

    else:
        print("Can't handle these type images!")


def save_img(img_arr):
    img = Image.fromarray(img_arr)
    img.save("./matched_img.jpg")
