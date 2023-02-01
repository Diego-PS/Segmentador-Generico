####
from pdf2docx import Converter
# import os

# # # dir_path for input reading and output files & a for loop # # #

path_input = './pdftodocx/input/'
path_output = './pdftodocx/output/'

file = '2fe2018c-094a-41b5-b6b5-f737407c4ad2.pdf'
cv = Converter(path_input+file)
cv.convert(path_output+file+'.docx', start=0, end=None)
cv.close()
print(file)