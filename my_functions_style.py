#!/bin/python3

#https://matplotlib.org/stable/gallery/text_labels_and_annotations/font_file.html

from pathlib import Path
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import os
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

##################################################3
# font for text:
font_path_for_text = '/home/wilson/Research/github/my_functions/SourceSansPro/SourceSansPro-Regular.ttf'

# first way, determine the font and add to each part of the text:
font_for_text = fm.FontProperties(fname=font_path_for_text, size=12)

# second way, font for all text in a plot:
#font_prop_for_text = FontProperties(fname=font_path_for_text)
#plt.rcParams['font.family'] = font_prop_for_text.get_name()

# font for number:
font_path_for_number = '/home/wilson/Research/github/my_functions/YuGothic/YuGothic.ttf'
#font_path_for_number = '/home/wilson/Research/github/my_functions/MoonLess/MoonlessSC-Regular.otf'

# crate the varianble to set font for number:
font_for_numbers = fm.FontProperties(fname=font_path_for_number, size=12)


####################################################################################################
# define a funtion to set font for all tick on x and y axes:
def set_font_for_numbers(ax, font_for_numbers):

    # Set font for numbers on x-axis
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_for_numbers)

    # Set font for numbers on y-axis
    for label in ax.get_yticklabels():
        label.set_fontproperties(font_for_numbers)



def style_ticks_plot(ax, x_mayor_tick):
    '''
    Description of this function:

    ax: subplot ax
    x_mayor_tick: add mayor ticks every set value on x
    #y_mayor_tick: add mayor ticks every set value on y
    
    The functions provides 6 mayor ticks values on y axe with 1 minor tick between 2 mayor ticks 
    '''
    
    # set tick values on x: mayor and minor
    ax.xaxis.set_major_locator(mtick.MultipleLocator(x_mayor_tick)) # mayor tick on x
    x_minor_tick = x_mayor_tick*0.5                                 # set x_minor_tick value
    ax.xaxis.set_minor_locator(mtick.MultipleLocator(x_minor_tick)) # minor tick on x

    # set tick values on y: mayor and minor
    #ax.yaxis.set_major_locator(mtick.MultipleLocator(y_mayor_tick)) # mayor tick on y
    #y_minor_tick = y_mayor_tick*0.5                                 # set y_minor_tick value
    #ax.yaxis.set_minor_locator(mtick.MultipleLocator(y_minor_tick)) # minor tick on y

    # set amount of ticks on y axe:
    n_mayor_yticks=6
    n_minor_yticks=2
    ax.yaxis.set_major_locator(mtick.MaxNLocator(n_mayor_yticks))
    ax.yaxis.set_minor_locator(AutoMinorLocator(n_minor_yticks))
    
    # set specific format on x and y axes:
    #ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1e"))

def save_file(fig, output_file):
    '''
    Description of this function:

    fig: this must be add on figure
    output_file: name of the output file
    
    The function save a figure with personal format and trim it
    '''
    fig.savefig(output_file, transparent=True, format="png", dpi=200)
    os.system('convert -trim {} {}'.format(output_file, output_file))


def set_plotstyle(plt, ax):
    '''
    Description of this function:
    plt: it must be added
    ax: for subplot ax
    This script set a personal style for plots on mathplotlib:
    - font: serif
    - fontsize: 15 for title, xlabel, ylabel
    - aspect ration 1
    - fontsize for legend: 10
    - layout plot
    '''
    # search font 'serif'
    serif_fonts = [font for font in fm.fontManager.ttflist if 'serif' in font.name.lower()]
    
    if serif_fonts:
        # get first font serif
        serif_font = serif_fonts[0].name
        
        # set fontsize on axes legends
        fontsize=12 # fontsize
        ax.set_title(ax.get_title(), fontname=serif_font, fontsize=fontsize)
        ax.set_xlabel(ax.get_xlabel(), fontname=serif_font, fontsize=fontsize)
        ax.set_ylabel(ax.get_ylabel(), fontname=serif_font, fontsize=fontsize)
            
        # set aspect ratio 1
        ax.set_box_aspect(1)
        
        # Set fontsize for tick labels on both axes
        fonstsize_ticks_labels=10
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(serif_font)
            label.set_fontsize(fonstsize_ticks_labels)  # You can adjust this fontsize as needed

        # set other elements on legends
        fontsize_legend=10
        legend = ax.legend(loc='best', fontsize=fontsize_legend, frameon=False)
        for text in legend.get_texts():
            text.set_fontname(serif_font)

        # layout graps on figure
        #plt.tight_layout()


def set_plotstyle_without_legend(plt, ax):
    '''
    Description of this function:
    plt: it must be added
    ax: for subplot ax
    This script set a personal style for plots on mathplotlib:
    - font: serif
    - fontsize: 15 for title, xlabel, ylabel
    - aspect ration 1
    - fontsize for legend: 10
    - layout plot
    '''
    # search font 'serif'
    serif_fonts = [font for font in fm.fontManager.ttflist if 'serif' in font.name.lower()]
    
    if serif_fonts:
        # get first font serif
        serif_font = serif_fonts[0].name
        
        # set font for elements on figure
        fontsize=15 # fontsize
        ax.set_title(ax.get_title(), fontname=serif_font, fontsize=fontsize)
        ax.set_xlabel(ax.get_xlabel(), fontname=serif_font, fontsize=fontsize)
        ax.set_ylabel(ax.get_ylabel(), fontname=serif_font, fontsize=fontsize)

        # set aspect ratio 1
        ax.set_box_aspect(1)
        
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(serif_font)

        # set other elements on legends
        #fontsize_legend=10
        #legend = ax.legend(loc='best', fontsize=fontsize_legend, frameon=False)
        #for text in legend.get_texts():
        #    text.set_fontname(serif_font)

        # layout graps on figure
        #plt.tight_layout()



def add_text(ax, text, location, offset=(0, 0), fontsize=12, fontprop='DejaVu Sans'):
    '''
    Add text to the specified location on the given axes.

    Parameters:
        ax (matplotlib.axes.Axes): The axes object to which text will be added.
        text (str): The text content to be added.
        location (str): The location where the text should be placed ('upper left', 'upper right', 'lower left', 'lower right', 'center', 'right', 'left', 'upper', 'lower', or 'custom').
        offset (tuple): Offset for custom positioning (default is (0, 0)).
        fontsize (int): Font size of the text (default is 12).
    '''
    
    if location == 'upper left':
        ax.text(0.05 + offset[0], 0.95 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop)
    elif location == 'upper right':
        ax.text(0.95 + offset[0], 0.95 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop, horizontalalignment='right')
    elif location == 'lower left':
        ax.text(0.05 + offset[0], 0.05 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop)
    elif location == 'lower right':
        ax.text(0.95 + offset[0], 0.05 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop, horizontalalignment='right')
    elif location == 'center':
        ax.text(0.5 + offset[0], 0.5 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop, horizontalalignment='center', verticalalignment='center')
    elif location == 'right':
        ax.text(0.95 + offset[0], 0.5 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop, horizontalalignment='right', verticalalignment='center')
    elif location == 'left':
        ax.text(0.05 + offset[0], 0.5 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop, verticalalignment='center')
    elif location == 'upper':
        ax.text(0.5 + offset[0], 0.95 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop, horizontalalignment='center')
    elif location == 'lower':
        ax.text(0.5 + offset[0], 0.05 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop, horizontalalignment='center')
    elif location == 'custom':
        ax.text(offset[0], offset[1], text, transform=ax.transAxes, fontsize=fontsize, fontproperties=fontprop)
    else:
        raise ValueError("Invalid location. Supported locations: 'upper left', 'upper right', 'lower left', 'lower right', 'center', 'right', 'left', 'upper', 'lower', or 'custom'.")



def save_file(fig, output_file):
    '''
    this function save a figure with personal format and trim it
    put always fig
    put the filename
    '''
    fig.savefig(output_file, transparent=True, format="png", dpi=200)
    os.system('convert -trim {} {}'.format(output_file, output_file))



def set_plotstyle(plt, ax):
    '''
    This script set a personal style for plots on mathplotlib
    - font: serif
    - fontsize: 15 for title, xlabel, ylabel
    - aspect ration 1
    - fontsize for legend: 10
    - layout plot
    '''
    # Buscar una fuente serif
    serif_fonts = [font for font in fm.fontManager.ttflist if 'serif' in font.name.lower()]
    
    if serif_fonts:
        # Tomar la primera fuente serif encontrada
        serif_font = serif_fonts[0].name
        
        # Establecer la fuente para varios elementos del gráfico
        ax.set_title(ax.get_title(), fontname=serif_font, fontsize=15)
        ax.set_xlabel(ax.get_xlabel(), fontname=serif_font, fontsize=15)
        ax.set_ylabel(ax.get_ylabel(), fontname=serif_font, fontsize=15)
        ax.set_box_aspect(1)
        
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(serif_font)

        # Configurar la fuente y otros parámetros de la leyenda
        legend = ax.legend(loc='best', fontsize=10, frameon=False)
        for text in legend.get_texts():
            text.set_fontname(serif_font)

        plt.tight_layout()
        
        

def style_ticks_plot(ax, x_mayor_tick):
    '''
    x_mayor_tick: add mayor ticks every set value on x
    y_mayor_tick: add mayor ticks every set value on y  
    '''
    # set tick values on x: mayor and minor
    ax.xaxis.set_major_locator(mtick.MultipleLocator(x_mayor_tick))   # mayor tick on x
    x_minor_tick = x_mayor_tick*0.5
    ax.xaxis.set_minor_locator(mtick.MultipleLocator(x_minor_tick))   # minor tick on x

    # set tick values on y: mayor and minor
    #ax.yaxis.set_major_locator(mtick.MultipleLocator(y_mayor_tick)) # mayor tick on y
    #y_minor_tick = y_mayor_tick*0.5
    #ax.yaxis.set_minor_locator(mtick.MultipleLocator(y_minor_tick)) # minor tick on y

    # set amount of tick on y axe:
    ax.yaxis.set_major_locator(mtick.MaxNLocator(6))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    
    # format:
    #ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1e"))
        
