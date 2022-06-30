from histogram_handler import HistogramHandler
from histogram_handler import match_histogram
from histogram_handler import save_img

matched_arr = match_histogram("./Source.jpg", "./Reference.jpg")
save_img(matched_arr)

