import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os
import matplotlib.font_manager as fm
import matplotlib.ticker as mtick
from matplotlib import rcParams, cycler

# my functions:
# style flag indicates function to style on plots
# for estyle use:
# plt.style.use("seaborn-bright")

# call my functions for style:
# style_ticks_plot(ax, 1)
# set_plotstyle(plt, ax)

#####################################################################
# import this to run my_funtions.py:
# import sys
# sys.path.append('/home/wilson/Research/styles_and_functions/')
# from my_functions import *
#####################################################################

'''
# format (Origin):
# https://stackoverflow.com/questions/59222659/making-pythons-matplotlib-graphics-look-like-graphics-created-using-originpro
rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 12
rcParams['axes.linewidth'] = 1.1
rcParams['axes.labelpad'] = 10.0
plot_color_cycle = cycler('color', ['FE0000', '0000FE', '008001', 'FD8000', '8c564b', 
                                    'e377c2', '7f7f7f', 'bcbd22', '17becf'])
rcParams['axes.prop_cycle'] = plot_color_cycle
rcParams['axes.xmargin'] = 0
rcParams['axes.ymargin'] = 0
rcParams.update({"figure.figsize" : (6.4,4.8),
                 "figure.subplot.left" : 0.177, "figure.subplot.right" : 0.946,
                 "figure.subplot.bottom" : 0.156, "figure.subplot.top" : 0.965,
                 "axes.autolimit_mode" : "round_numbers",
                 "xtick.major.size"     : 7,
                 "xtick.minor.size"     : 3.5,
                 "xtick.major.width"    : 1.1,
                 "xtick.minor.width"    : 1.1,
                 "xtick.major.pad"      : 5,
                 "xtick.minor.visible" : True,
                 "ytick.major.size"     : 7,
                 "ytick.minor.size"     : 3.5,
                 "ytick.major.width"    : 1.1,
                 "ytick.minor.width"    : 1.1,
                 "ytick.major.pad"      : 5,
                 "ytick.minor.visible" : True,
                 "lines.markersize" : 10,
                 "lines.markerfacecolor" : "none",
                 "lines.markeredgewidth"  : 0.8})
'''


def molec2mg_(mw):
    mw = mw   # molecular weitght in g/mol
    avogadro = 6.023*(10**23) # avogadro number in molecules/mol
    m_to_nm = 1*(10**9) # nm/m
    g_to_mg = 1000      # mg/g
    factor = (g_to_mg*mw*m_to_nm)/(avogadro)
    return factor


def gamma_molec_to_mg_m2(gamma1, mw):
    '''
    Parameters:
        gamma1: gamma in molecules/nm^2
        mw: molecular weight in g/mol
    Return:
        gamma2: gamma in mg/m^2
    '''
    avogadro = 6.023*(10**23) # avogadro number in molecules by mol
    m2nm = 1/(1*(10**9)**2)   # conversion factor from m^2 to nm^2
    g2mg = 1/1000             # conversion factor from g to mg
    gamma2 = (gamma1 * mw)/(avogadro * m2nm * g2mg)
    return gamma2


def convert_1dx_xxx(text):
    """
    Converts, for example 1d6 string into 1*10**-6 M float

    Args:
        text (str): 1d6 string 

    Returns:
        float: 1*10**-6

    Raises:
        ValueError: If the input string does not follow the '1dx' format or if 'x' is not an integer.
    """
    base = float(text.split('d')[0])    # base
    exponent = int(text.split('d')[1])  # exponent
    
    cprot = base * 10 **(-exponent)     # float data
    
    return cprot


def mw_from_sequence(sequence):
    """
    Calculate the molecular weight (MW) of a protein or peptide sequence.

    Parameters:
        sequence (str): A string representing the sequence of amino acids.

    Returns:
        float: The calculated molecular weight in g/mol.
    """
    # Defines a dictionary that maps the 20 common amino acids to their atomic masses
    atomic_weights = {
        'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
        'Q': 146.2, 'E': 147.1, 'G': 75.1, 'H': 155.2, 'I': 131.2,
        'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
        'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
    }
    # from https://www.thermofisher.com/

    # Calculate the molecular weight by summing the atomic weights of the amino acids
    mw = sum(atomic_weights.get(aminoacid, 0) for aminoacid in sequence)
    return mw






def get_xyz1(filename, skiprows=2):
    block = []
    # open a file:
    with open(filename, "r") as file:
        # save all lines:
        lines = file.readlines()
        # skip first two lines:
        lines = lines[skiprows:]

        # create a list if lists:
        for line in lines:
            line_xyz = line.strip().split("\t")
            line_xyz[1] = float(line_xyz[1])
            line_xyz[2] = float(line_xyz[2])
            line_xyz[3] = float(line_xyz[3])
            block.append(line_xyz)
    return block

def get_xyz2(filename):
    blocks = []
    current_block = []
    with open(filename, 'r') as file:
        ### skip rows with rare numbers:
        lines = []
        for line in file:
            value_to_test = len(line.split())
            if value_to_test == 1:  
                continue
            else:
                lines.append(line)

        ### save blocks of data by spacing
        for line in lines:
            value_to_test = line.strip()
            if value_to_test == '':   # if empty line is found, then block is save into block list 
                if current_block: # save non empty block
                    blocks.append(current_block) # append block into a block list
                current_block = []               # inicialize a new block
            else:   # append lines into current block:
                line_xyz = line.strip().split()
                line_xyz[1] = float(line_xyz[1])
                line_xyz[2] = float(line_xyz[2])
                line_xyz[3] = float(line_xyz[3]) 
                current_block.append(line_xyz)
        return blocks

def a_to_nm(block):
    for element in block:
        element[1] = round(element[1]/10,4)
        element[2] = round(element[2]/10,4)
        element[3] = round(element[3]/10,4)
    return block
    
   

def molec_to_mg(mw):
    mw = mw   # molecular weitght in g by mol
    avogadro = 6.023*(10**23) # avogadro number in molecules by mol
    m_to_nm = 1*(10**9) # nm by m
    g_to_mg = 1000      # mg by g
    factor = (g_to_mg*mw*m_to_nm)/(avogadro)
    return factor
