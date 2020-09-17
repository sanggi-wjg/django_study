from pprint import pprint

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager

print(mpl.matplotlib_fname())

# print(len(font_manager.fontManager.ttflist))
for font in font_manager.fontManager.ttflist:
    #     # print(font)
    print(font.name, font.fname)
#
# print([(f.name, f.fname) for f in font_manager.fontManager.ttflist if 'Nanum' in f.name])

# print(len(font_manager.findSystemFonts(fontpaths = None, fontext = 'ttf')))
# for font in font_manager.findSystemFonts(fontpaths = None, fontext = 'ttf'):
#     print(font)

# print(plt.rcParams['font.family'])
