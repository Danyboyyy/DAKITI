from Cuadruple import Cuadruple
from parser import cuadruples
from os import path
import sys
import re
import parser
import utils

try:
    if not len(sys.argv) == 2:
        sys.exit("Try running the following command: python parser.py name_of_file.dak")

    file = sys.argv[1]

    if not re.match("(.*?)\.(dak)$", file):
        sys.exit("File should be a .dak file!")

    if not path.isfile(file):
        sys.exit("Cannot find the file!" + file)

    ifFile = open(file, 'r')
    data = ifFile.read()
    ifFile.close()

    elements = parser.run(data)
except EOFError:
    print("Error, try again!")

cuadruples = elements[0]
vars_table = elements[1]
constants_table = elements[2]
programName = elements[3]

for cuadruple in cuadruples:
    operator = cuadruple.operator
    
    
