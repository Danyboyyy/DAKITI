from asyncio import constants
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

# Relevant information
cuadruples = elements[0]
vars_table = elements[1]
constants_table = elements[2]
programName = elements[3]
totalTemps = elements[4]

# Memory
localInts = []
localFloats = []
localBools = []
localStrings = []

globalInts = []
globalFloats = []
globalBools = []
globalStrings = []

constantInts = []
constantFloats = []
constantBools = []
constantStrings = []

tempInts = []
tempFloats = []
tempBools = []
tempStrings = []
tempPointers = []

# Auxiliary variables
current = 0

# Store global vars
for var in vars_table[programName]['vars']:
    if vars_table[programName]['vars'][var]['type'] == 'int':
        if 'size' in vars_table[programName]['vars'][var]:
            for i in range(0, vars_table[programName]['vars'][var]['size']):
                globalInts.append(None)
        else:
            globalInts.append(None)
    if vars_table[programName]['vars'][var]['type'] == 'float':
        if 'size' in vars_table[programName]['vars'][var]:
            for i in range(0, vars_table[programName]['vars'][var]['size']):
                globalInts.append(None)
        else:
            globalFloats.append(None)
    if vars_table[programName]['vars'][var]['type'] == 'bool':
        if 'size' in vars_table[programName]['vars'][var]:
            for i in range(0, vars_table[programName]['vars'][var]['size']):
                globalInts.append(None)
        else:
            globalBools.append(None)
    if vars_table[programName]['vars'][var]['type'] == 'string':
        if 'size' in vars_table[programName]['vars'][var]:
            for i in range(0, vars_table[programName]['vars'][var]['size']):
                globalInts.append(None)
        else:
            globalStrings.append(None)

# Store constants
for type in constants_table:
    for constant in constants_table[type]:
        if type == 'int':
            constantInts.append(constant)
        if type == 'float':
            constantFloats.append(constant)
        if type == 'bool':
            constantBools.append(constant)
        if type == 'string':
            constantStrings.append(constant)

# Store temps
for i in range(0, totalTemps['int']):
    tempInts.append(None)
for i in range(0, totalTemps['float']):
    tempFloats.append(None)
for i in range(0, totalTemps['bool']):
    tempBools.append(None)
for i in range(0, totalTemps['string']):
    tempStrings.append(None)
for i in range(0, totalTemps['pointer']):
    tempPointers.append(None)

# Access value based on the memory address
def getValue(address):
    addressToString = str(address)
    if addressToString[0] == '(' and addressToString[-1] == ')':
        address = getValue(int(addressToString[1:-1]))
    
    if 1000 <= address < 5000: # Local variables
        pass # Not handling local memory yet
    # Global Variables
    elif 5000 <= address < 6000:
        if globalInts[address - 5000] == None:
            utils.showError('Variable does not have a value!')
        return globalInts[address - 5000]
    elif 6000 <= address < 7000:
        if globalFloats[address - 6000] == None:
            utils.showError('Variable does not have a value!')
        return globalFloats[address - 5000]
    elif 7000 <= address < 8000:
        if globalBools[address - 7000] == None:
            utils.showError('Variable does not have a value!')
        return globalBools[address - 7000]
    elif 8000 <= address < 9000:
        if globalStrings[address - 8000] == None:
            utils.showError('Variable does not have a value!')
        return globalStrings[address - 8000]
    # Constants
    elif 9000 <= address < 10000:
        if constantInts[address - 9000] == None:
            utils.showError('Variable does not have a value!')
        return constantInts[address - 9000]
    elif 10000 <= address < 11000:
        if constantFloats[address - 10000] == None:
            utils.showError('Variable does not have a value!')
        return constantFloats[address - 10000]
    elif 11000 <= address < 12000:
        if constantBools[address - 11000] == None:
            utils.showError('Variable does not have a value!')
        return constantBools[address - 11000]
    elif 12000 <= address < 13000:
        if constantStrings[address - 12000] == None:
            utils.showError('Variable does not have a value!')
        return constantStrings[address - 12000]
    # Temp variables
    elif 13000 <= address < 14000:
        if tempInts[address - 13000] == None:
            utils.showError('Variable does not have a value!')
        return tempInts[address - 13000]
    elif 14000 <= address < 15000:
        if tempFloats[address - 14000] == None:
            utils.showError('Variable does not have a value!')
        return tempFloats[address - 14000]
    elif 15000 <= address < 16000:
        if tempBools[address - 15000] == None:
            utils.showError('Variable does not have a value!')
        return tempBools[address - 15000]
    elif 16000 <= address < 17000:
        if tempStrings[address - 16000] == None:
            utils.showError('Variable does not have a value!')
        return tempStrings[address - 16000]
    elif 17000 <= address < 18000:
        if tempPointers[address - 17000] == None:
            utils.showError('Variable does not have a value!')
        return tempPointers[address - 17000]
    else:
        utils.showError('Memory error!')

# Change booleans to lowercase
def changeToLowerCase(res):
    if res == True:
        return 'true'
    elif res == False:
        return 'false'
    else:
        utils.showError('An error ocurred!')

# Change booleans to upperCase
def changeToUpperCase(res):
    if res == 'true':
        return True
    elif res == 'false':
        return False
    else:
        utils.showError('An error ocurredasdfasdf!')

while current < len(cuadruples):
    operator = cuadruples[current].operator
    op1 = cuadruples[current].op1
    op2 = cuadruples[current].op2
    res = cuadruples[current].res

    if operator == '+':
        if 5000 <= res < 6000:
            globalInts[res - 5000] = getValue(op1) + getValue(op2)
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = getValue(op1) + getValue(op2)
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = getValue(op1) + getValue(op2)
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = getValue(op1) + getValue(op2)
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = getValue(op1) + getValue(op2)
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = getValue(op1) + getValue(op2)
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = getValue(op1) + getValue(op2)
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = getValue(op1) + getValue(op2)
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = getValue(op1) + getValue(op2)
    elif operator == '-':
        if 5000 <= res < 6000:
            globalInts[res - 5000] = getValue(op1) - getValue(op2)
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = getValue(op1) - getValue(op2)
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = getValue(op1) - getValue(op2)
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = getValue(op1) - getValue(op2)
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = getValue(op1) - getValue(op2)
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = getValue(op1) - getValue(op2)
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = getValue(op1) - getValue(op2)
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = getValue(op1) - getValue(op2)
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = getValue(op1) - getValue(op2)
    elif operator == '*':
        if 5000 <= res < 6000:
            globalInts[res - 5000] = getValue(op1) * getValue(op2)
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = getValue(op1) * getValue(op2)
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = getValue(op1) * getValue(op2)
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = getValue(op1) * getValue(op2)
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = getValue(op1) * getValue(op2)
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = getValue(op1) * getValue(op2)
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = getValue(op1) * getValue(op2)
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = getValue(op1) * getValue(op2)
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = getValue(op1) * getValue(op2)
    elif operator == '/':
        if getValue(op2) == 0:
            utils.showError('Cannot perform a division by 0!')

        if 5000 <= res < 6000:
            globalInts[res - 5000] = getValue(op1) / getValue(op2)
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = getValue(op1) / getValue(op2)
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = getValue(op1) / getValue(op2)
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = getValue(op1) / getValue(op2)
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = getValue(op1) / getValue(op2)
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = getValue(op1) / getValue(op2)
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = getValue(op1) / getValue(op2)
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = getValue(op1) / getValue(op2)
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = getValue(op1) / getValue(op2)
    elif operator == '%':
        if getValue(op2) == 0:
            utils.showError('Cannot perform a division by 0!')
            
        if 5000 <= res < 6000:
            globalInts[res - 5000] = getValue(op1) % getValue(op2)
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = getValue(op1) % getValue(op2)
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = getValue(op1) % getValue(op2)
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = getValue(op1) % getValue(op2)
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = getValue(op1) % getValue(op2)
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = getValue(op1) % getValue(op2)
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = getValue(op1) % getValue(op2)
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = getValue(op1) % getValue(op2)
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = getValue(op1) % getValue(op2)
    elif operator == '<':
        if 5000 <= res < 6000:
            globalInts[res - 5000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = changeToLowerCase(getValue(op1) < getValue(op2))
    elif operator == '<=':
        if 5000 <= res < 6000:
            globalInts[res - 5000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = changeToLowerCase(getValue(op1) <= getValue(op2))
    elif operator == '>':
        if 5000 <= res < 6000:
            globalInts[res - 5000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = changeToLowerCase(getValue(op1) > getValue(op2))
    elif operator == '>=':
        if 5000 <= res < 6000:
            globalInts[res - 5000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = changeToLowerCase(getValue(op1) >= getValue(op2))
    elif operator == '==':
        if 13000 <= res < 17000:
            if 15000 <= op1 < 16000 and 15000 <= op2 < 16000:
                if 13000 <= res < 14000:
                    tempInts[res - 13000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
                elif 14000 <= res < 15000:
                    tempFloats[res - 14000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
                elif 15000 <= res < 16000:
                    tempBools[res - 15000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
                elif 16000 <= res < 17000:
                    tempStrings[res - 16000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
                elif 17000 <= res < 18000:
                    tempPointers[res - 17000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            else:
                if 13000 <= res < 14000:
                    tempInts[res - 13000] = changeToLowerCase(getValue(op1) == getValue(op2))
                elif 14000 <= res < 15000:
                    tempFloats[res - 14000] = changeToLowerCase(getValue(op1) == getValue(op2))
                elif 15000 <= res < 16000:
                    tempBools[res - 15000] = changeToLowerCase(getValue(op1) == getValue(op2))
                elif 16000 <= res < 17000:
                    tempStrings[res - 16000] = changeToLowerCase(getValue(op1) == getValue(op2))
                elif 17000 <= res < 18000:
                    tempPointers[res - 17000] = changeToLowerCase(getValue(op1) == getValue(op2))
        else:
            if (3000 <= op1 < 4000 or 7000 <= op1 < 8000 or 11000 <= op1 < 12000) and (3000 <= op2 < 4000 or 7000 <= op2 < 8000 or 11000 <= op2 < 12000):
                if 5000 <= res < 6000:
                    globalInts[res - 5000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
                elif 6000 <= res < 7000:
                    globalFloats[res - 6000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
                elif 7000 <= res < 8000:
                    globalBools[res - 7000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
                elif 8000 <= res < 9000:
                    globalStrings[res - 8000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            else:
                if 5000 <= res < 6000:
                    globalInts[res - 5000] = changeToLowerCase(getValue(op1) == getValue(op2))
                elif 6000 <= res < 7000:
                    globalFloats[res - 6000] = changeToLowerCase(getValue(op1) == getValue(op2))
                elif 7000 <= res < 8000:
                    globalBools[res - 7000] = changeToLowerCase(getValue(op1) == getValue(op2))
                elif 8000 <= res < 9000:
                    globalStrings[res - 8000] = changeToLowerCase(getValue(op1) == getValue(op2))
    elif operator == '<>':
        if 13000 <= res < 17000:
            if 15000 <= op1 < 16000 and 15000 <= op2 < 16000:
                if 13000 <= res < 14000:
                    tempInts[res - 13000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
                elif 14000 <= res < 15000:
                    tempFloats[res - 14000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
                elif 15000 <= res < 16000:
                    tempBools[res - 15000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
                elif 16000 <= res < 17000:
                    tempStrings[res - 16000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
                elif 17000 <= res < 18000:
                    tempPointers[res - 17000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            else:
                if 13000 <= res < 14000:
                    tempInts[res - 13000] = changeToLowerCase(getValue(op1) != getValue(op2))
                elif 14000 <= res < 15000:
                    tempFloats[res - 14000] = changeToLowerCase(getValue(op1) != getValue(op2))
                elif 15000 <= res < 16000:
                    tempBools[res - 15000] = changeToLowerCase(getValue(op1) != getValue(op2))
                elif 16000 <= res < 17000:
                    tempStrings[res - 16000] = changeToLowerCase(getValue(op1) != getValue(op2))
                elif 17000 <= res < 18000:
                    tempPointers[res - 17000] = changeToLowerCase(getValue(op1) != getValue(op2))
        else:
            if (3000 <= op1 < 4000 or 7000 <= op1 < 8000 or 11000 <= op1 < 12000) and (3000 <= op2 < 4000 or 7000 <= op2 < 8000 or 11000 <= op2 < 12000):
                if 5000 <= res < 6000:
                    globalInts[res - 5000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
                elif 6000 <= res < 7000:
                    globalFloats[res - 6000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
                elif 7000 <= res < 8000:
                    globalBools[res - 7000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
                elif 8000 <= res < 9000:
                    globalStrings[res - 8000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            else:
                if 5000 <= res < 6000:
                    globalInts[res - 5000] = changeToLowerCase(getValue(op1) != getValue(op2))
                elif 6000 <= res < 7000:
                    globalFloats[res - 6000] = changeToLowerCase(getValue(op1) != getValue(op2))
                elif 7000 <= res < 8000:
                    globalBools[res - 7000] = changeToLowerCase(getValue(op1) != getValue(op2))
                elif 8000 <= res < 9000:
                    globalStrings[res - 8000] = changeToLowerCase(getValue(op1) != getValue(op2))
    elif operator == '&&':
        if 5000 <= res < 6000:
            globalInts[res - 5000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
    elif operator == '||':
        if 5000 <= res < 6000:
            globalInts[res - 5000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
    elif operator == '=':
        resToString = str(res)
        if resToString[0] == '(' and resToString[-1] == ')':
            res = getValue(int(resToString[1:-1]))

        if 5000 <= res < 6000:
            globalInts[res - 5000] = getValue(op1)
        elif 6000 <= res < 7000:
            globalFloats[res - 6000] = getValue(op1)
        elif 7000 <= res < 8000:
            globalBools[res - 7000] = getValue(op1)
        elif 8000 <= res < 9000:
            globalStrings[res - 8000] = getValue(op1)
        elif 13000 <= res < 14000:
            tempInts[res - 13000] = getValue(op1)
        elif 14000 <= res < 15000:
            tempFloats[res - 14000] = getValue(op1)
        elif 15000 <= res < 16000:
            tempBools[res - 15000] = getValue(op1)
        elif 16000 <= res < 17000:
            tempStrings[res - 16000] = getValue(op1)
        elif 17000 <= res < 18000:
            tempPointers[res - 17000] = getValue(op1)
    elif operator == 'PRINT':
        print(getValue(res))
    elif operator == 'GOTO':
        current = res
        continue
    elif operator == 'GOTOF':
        if getValue(op1) == 'false':
            current = res
            continue
    elif operator == 'VERIFY':
        if getValue(op1) < getValue(op2) or getValue(op1) >= getValue(res):
            utils.showError('Index out of bounds!')
    elif operator == 'ERA':
        pass
    elif operator == 'PARAM':
        pass
    elif operator == 'GOSUB':
        pass
    elif operator == 'ENDFUNC':
        pass

    
    current += 1