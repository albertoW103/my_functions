#!/bin/python3

#https://matplotlib.org/stable/gallery/text_labels_and_annotations/font_file.html

from pathlib import Path
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm

##################################################3
# font for text:
font_path_for_text = '/home/wilson/Research/github/my_functions/SourceSansPro/SourceSansPro-Regular.ttf'

# first way, determine the font and add to each part of the text:
font_for_text = fm.FontProperties(fname=font_path_for_text, size=14)

# second way, font for all text in a plot:
#font_prop_for_text = FontProperties(fname=font_path_for_text)
#plt.rcParams['font.family'] = font_prop_for_text.get_name()

##################################################
# font for number:
font_path_for_number = '/home/wilson/Research/github/my_functions/YuGothic/YuGothic.ttf'
#font_path_for_number = '/home/wilson/Research/github/my_functions/MoonLess/MoonlessSC-Regular.otf'

# crate the varianble to set font for number:
font_for_numbers = fm.FontProperties(fname=font_path_for_number, size=14)

# define a funtion to set font for all tick on x and y axes:
def set_font_for_numbers(ax):

    # Set font for numbers on x-axis
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_for_numbers)

    # Set font for numbers on y-axis
    for label in ax.get_yticklabels():
        label.set_fontproperties(font_for_numbers)



