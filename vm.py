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

# Memory
localVars_memory = {}
globalVars_memory = {}
tempVars_memory = {}
constants_memory = {}

# Auxiliary variables
current = 0

# Store global vars
for var in vars_table[programName]['vars']:
    globalVars_memory[vars_table[programName]['vars'][var]['memory']] = None

# Store constants
for type in constants_table:
    for constant in constants_table[type]:
        constants_memory[constants_table[type][constant]['memory']] = constant

def addTempToMemory(address, res):
    global tempVars_memory

    tempVars_memory[address] = res

# def setLocalMemory(functionName):
#     global localVars_memory, tempVars_memory

#     localVars_memory.clear()
#     tempVars_memory.clear()
    
#     for var in vars_table[functionName]['vars']:
#         localVars_memory[vars_table[functionName]['vars'][var]['memory']] = None

# Access value based on the memory address
def getValue(address):
    if 1000 <= address < 5000: # Local variables
        pass # Not handling local memory yet
    elif 5000 <= address < 9000: # Global Variables
        if globalVars_memory[address] == None:
            utils.showError('Variable does not have a value!')

        return globalVars_memory[address]
    elif 9000 <= address < 13000: # Constants
        if constants_memory[address] == None:
            utils.showError('Variable does not have a value!')

        return constants_memory[address]
    elif 13000 <= address < 17000: # Temp variables
        if tempVars_memory[address] == None:
            utils.showError('Variable does not have a value!')

        return tempVars_memory[address]
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
        if 13000 <= res < 17000:
            tempVars_memory[res] = getValue(op1) + getValue(op2)
        else:
            globalVars_memory[res] = getValue(op1) + getValue(op2)
    elif operator == '-':
        if 13000 <= res < 17000:
            tempVars_memory[res] = getValue(op1) - getValue(op2)
        else:
            globalVars_memory[res] = getValue(op1) - getValue(op2)
    elif operator == '*':
        if 13000 <= res < 17000:
            tempVars_memory[res] = getValue(op1) * getValue(op2)
        else:
            globalVars_memory[res] = getValue(op1) * getValue(op2)
    elif operator == '/':
        if op2 == '0':
            utils.showError('Cannot perform a division by 0!')

        if 13000 <= res < 17000:
            tempVars_memory[res] = getValue(op1) / getValue(op2)
        else:
            globalVars_memory[res] = getValue(op1) / getValue(op2)
    elif operator == '%':
        if 13000 <= res < 17000:
            tempVars_memory[res] = getValue(op1) % getValue(op2)
        else:
            globalVars_memory[res] = getValue(op1) % getValue(op2)
    elif operator == '<':
        if 13000 <= res < 17000:
            tempVars_memory[res] = changeToLowerCase(getValue(op1) < getValue(op2))
        else:
            globalVars_memory[res] = changeToLowerCase(getValue(op1) < getValue(op2))
    elif operator == '<=':
        if 13000 <= res < 17000:
            tempVars_memory[res] = changeToLowerCase(getValue(op1) <= getValue(op2))
        else:
            globalVars_memory[res] = changeToLowerCase(getValue(op1) <= getValue(op2))
    elif operator == '>':
        if 13000 <= res < 17000:
            tempVars_memory[res] = changeToLowerCase(getValue(op1) > getValue(op2))
        else:
            globalVars_memory[res] = changeToLowerCase(getValue(op1) > getValue(op2))
    elif operator == '>=':
        if 13000 <= res < 17000:
            tempVars_memory[res] = changeToLowerCase(getValue(op1) >= getValue(op2))
        else:
            globalVars_memory[res] = changeToLowerCase(getValue(op1) >= getValue(op2))
    elif operator == '==':
        if 13000 <= res < 17000:
            if 15000 <= op1 < 16000 and 15000 <= op2 < 16000:
                tempVars_memory[res] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            else:
                tempVars_memory[res] = changeToLowerCase(getValue(op1) == getValue(op2))
        else:
            if (2000 <= op1 < 3000 or 6000 <= op1 < 7000 or 10000 <= op1 < 11000) and (2000 <= op2 < 3000 or 6000 <= op2 < 7000 or 10000 <= op2 < 11000):
                globalVars_memory[res] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            else:
                globalVars_memory[res] = changeToLowerCase(getValue(op1) == getValue(op2))
    elif operator == '<>':
        if 13000 <= res < 17000:
            if 15000 <= op1 < 16000 and 15000 <= op2 < 16000:
                tempVars_memory[res] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            else:
                tempVars_memory[res] = changeToLowerCase(getValue(op1) != getValue(op2))
        else:
            if (2000 <= op1 < 3000 or 6000 <= op1 < 7000 or 10000 <= op1 < 11000) and (2000 <= op2 < 3000 or 6000 <= op2 < 7000 or 10000 <= op2 < 11000):
                globalVars_memory[res] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            else:
                globalVars_memory[res] = changeToLowerCase(getValue(op1) != getValue(op2))
    elif operator == '&&':
        if 13000 <= res < 17000:
            tempVars_memory[res] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        else:
            globalVars_memory[res] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
    elif operator == '||':
        if 13000 <= res < 17000:
            tempVars_memory[res] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        else:
            globalVars_memory[res] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
    elif operator == '=':
        if 13000 <= res < 17000:
            tempVars_memory[res] = getValue(op1)
        else:
            globalVars_memory[res] = getValue(op1)
    elif operator == 'PRINT':
        print(getValue(res))
    elif operator == 'GOTO':
        current = res
        continue
    elif operator == 'GOTOF':
        if getValue(op1) == 'false':
            current = res
            continue
    
    current += 1