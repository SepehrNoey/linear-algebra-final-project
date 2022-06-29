import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

class HistogramMaker:
    def __init__(self, img_path, colorful: bool):
        self.img_path = img_path
        self.img = Image.open(img_path)
        self.img_arr = np.array(self.img)
        self.colorful = colorful
        # now defining cdf histogram arrays
        self.gray_cdf = np.zeros((1, 256))
        self.red_cdf = np.zeros((1, 256))
        self.green_cdf = np.zeros((1, 256))
        self.blue_cdf = np.zeros((1, 256))
        self.__make_cdf_histogram_array()

    def __make_cdf_histogram_array(self):
        if not self.colorful:
            hist_arr = np.zeros((1, 256))
            for i in range(self.img_arr.shape[0]):
                for j in range(self.img_arr.shape[1]):
                    hist_arr[0, self.img_arr[i, j]] += 1

            self.gray_cdf[0] = hist_arr[0]
            for i in range(1, 256):
                self.gray_cdf[i] = self.gray_cdf[i - 1] + hist_arr[i]

        else:
            red_hist_arr = np.zeros((1, 256))
            green_hist_arr = np.zeros((1, 256))
            blue_hist_arr = np.zeros((1, 256))
            for i in range(self.img_arr.shape[0]):
                for j in range(self.img_arr.shape[1]):
                    red_hist_arr[0, self.img_arr[i, j]] += 1
                    green_hist_arr[0, self.img_arr[i, j]] += 1
                    blue_hist_arr[0, self.img_arr[i, j]] += 1

            self.red_cdf[0] = red_hist_arr[0]
            self.green_cdf[0] = green_hist_arr[0]
            self.blue_cdf[0] = blue_hist_arr[0]
            for i in range(1, 256):
                self.red_cdf[0, i] = self.red_cdf[0, i - 1] + red_hist_arr[0, i]
                self.green_cdf[0, i] = self.green_cdf[0, i - 1] + green_hist_arr[0, i]
                self.blue_cdf[0, i] = self.blue_cdf[0, i - 1] + blue_hist_arr[0, i]







    # def print(self):
    #     plt.bar(range(256), self.red_cdf.reshape((256, )), color='red')
    #     print("here")




