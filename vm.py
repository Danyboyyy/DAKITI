from collections import deque
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
vmemory = elements[5]

# Auxiliary variables
current = 0
callsStack = deque()
functionsStack = deque()
currentFunction = ''
parameters = []
flag = False

# Store global vars
for var in vars_table[programName]['vars']:
    if vars_table[programName]['vars'][var]['type'] == 'int':
        if 'size' in vars_table[programName]['vars'][var]:
            for i in range(0, vars_table[programName]['vars'][var]['size']):
                vmemory.globalInts.append(None)
        else:
            vmemory.globalInts.append(None)
    if vars_table[programName]['vars'][var]['type'] == 'float':
        if 'size' in vars_table[programName]['vars'][var]:
            for i in range(0, vars_table[programName]['vars'][var]['size']):
                vmemory.globalFloats.append(None)
        else:
            vmemory.globalFloats.append(None)
    if vars_table[programName]['vars'][var]['type'] == 'bool':
        if 'size' in vars_table[programName]['vars'][var]:
            for i in range(0, vars_table[programName]['vars'][var]['size']):
                vmemory.globalBools.append(None)
        else:
            vmemory.globalBools.append(None)
    if vars_table[programName]['vars'][var]['type'] == 'string':
        if 'size' in vars_table[programName]['vars'][var]:
            for i in range(0, vars_table[programName]['vars'][var]['size']):
                vmemory.globalStrings.append(None)
        else:
            vmemory.globalStrings.append(None)

# Store constants
for type in constants_table:
    for constant in constants_table[type]:
        if type == 'int':
            vmemory.constantInts.append(constant)
        if type == 'float':
            vmemory.constantFloats.append(constant)
        if type == 'bool':
            vmemory.constantBools.append(constant)
        if type == 'string':
            vmemory.constantStrings.append(constant)

# Store temps
for i in range(0, totalTemps['int']):
    vmemory.tempInts.append(None)
for i in range(0, totalTemps['float']):
    vmemory.tempFloats.append(None)
for i in range(0, totalTemps['bool']):
    vmemory.tempBools.append(None)
for i in range(0, totalTemps['string']):
    vmemory.tempStrings.append(None)
for i in range(0, totalTemps['pointer']):
    vmemory.tempPointers.append(None)
vmemory.resetTempMemory()
vmemory.resetLocalMemory()

# Access value based on the memory address
def getValue(address):
    addressToString = str(address)
    if addressToString[0] == '(' and addressToString[-1] == ')':
        address = getValue(int(addressToString[1:-1]))
    
    # Local variables
    if 1000 <= address < 2000:
        if vmemory.localIntsStack[-1][address - 1000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.localIntsStack[-1][address - 1000]
    elif 2000 <= address < 3000:
        if vmemory.localFloatsStack[-1][address - 2000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.localFloatsStack[-1][address - 2000]
    elif 3000 <= address < 4000:
        if vmemory.localBoolsStack[-1][address - 3000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.localBoolsStack[-1][address - 3000]
    elif 4000 <= address < 5000:
        if vmemory.localStringsStack[-1][address - 4000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.localStringsStack[-1][address - 4000]
    # Global Variables
    elif 5000 <= address < 6000:
        if vmemory.globalInts[address - 5000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.globalInts[address - 5000]
    elif 6000 <= address < 7000:
        if vmemory.globalFloats[address - 6000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.globalFloats[address - 5000]
    elif 7000 <= address < 8000:
        if vmemory.globalBools[address - 7000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.globalBools[address - 7000]
    elif 8000 <= address < 9000:
        if vmemory.globalStrings[address - 8000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.globalStrings[address - 8000]
    # Constants
    elif 9000 <= address < 10000:
        if vmemory.constantInts[address - 9000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.constantInts[address - 9000]
    elif 10000 <= address < 11000:
        if vmemory.constantFloats[address - 10000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.constantFloats[address - 10000]
    elif 11000 <= address < 12000:
        if vmemory.constantBools[address - 11000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.constantBools[address - 11000]
    elif 12000 <= address < 13000:
        if vmemory.constantStrings[address - 12000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.constantStrings[address - 12000]
    # Temp variables
    elif 13000 <= address < 14000:
        if vmemory.tempIntsStack[-1][address - 13000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.tempIntsStack[-1][address - 13000]
    elif 14000 <= address < 15000:
        if vmemory.tempFloatsStack[-1][address - 14000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.tempFloatsStack[-1][address - 14000]
    elif 15000 <= address < 16000:
        if vmemory.tempBoolsStack[-1][address - 15000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.tempBoolsStack[-1][address - 15000]
    elif 16000 <= address < 17000:
        if vmemory.tempStringsStack[-1][address - 16000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.tempStringsStack[-1][address - 16000]
    elif 17000 <= address < 18000:
        if vmemory.tempPointersStack[-1][address - 17000] == None:
            utils.showError('Variable does not have a value!')
        return vmemory.tempPointersStack[-1][address - 17000]
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
        utils.showError('An error ocurred!')

utils.displayCuadruples(cuadruples)
utils.displayVarsTable(vars_table)
print(vars_table)

while current < len(cuadruples):
    operator = cuadruples[current].operator
    op1 = cuadruples[current].op1
    op2 = cuadruples[current].op2
    res = cuadruples[current].res

    if operator == '+':
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = getValue(op1) + getValue(op2)
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = getValue(op1) + getValue(op2)
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = getValue(op1) + getValue(op2)
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = getValue(op1) + getValue(op2)
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = getValue(op1) + getValue(op2)
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = getValue(op1) + getValue(op2)
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = getValue(op1) + getValue(op2)
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = getValue(op1) + getValue(op2)
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = getValue(op1) + getValue(op2)
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = getValue(op1) + getValue(op2)
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = getValue(op1) + getValue(op2)
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = getValue(op1) + getValue(op2)
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = getValue(op1) + getValue(op2)
    elif operator == '-':
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = getValue(op1) - getValue(op2)
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = getValue(op1) - getValue(op2)
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = getValue(op1) - getValue(op2)
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = getValue(op1) - getValue(op2)
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = getValue(op1) - getValue(op2)
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = getValue(op1) - getValue(op2)
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = getValue(op1) - getValue(op2)
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = getValue(op1) - getValue(op2)
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = getValue(op1) - getValue(op2)
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = getValue(op1) - getValue(op2)
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = getValue(op1) - getValue(op2)
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = getValue(op1) - getValue(op2)
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = getValue(op1) - getValue(op2)
    elif operator == '*':
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = getValue(op1) * getValue(op2)
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = getValue(op1) * getValue(op2)
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = getValue(op1) * getValue(op2)
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = getValue(op1) * getValue(op2)
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = getValue(op1) * getValue(op2)
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = getValue(op1) * getValue(op2)
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = getValue(op1) * getValue(op2)
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = getValue(op1) * getValue(op2)
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = getValue(op1) * getValue(op2)
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = getValue(op1) * getValue(op2)
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = getValue(op1) * getValue(op2)
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = getValue(op1) * getValue(op2)
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = getValue(op1) * getValue(op2)
    elif operator == '/':
        if getValue(op2) == 0:
            utils.showError('Cannot perform a division by 0!')

        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = getValue(op1) / getValue(op2)
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = getValue(op1) / getValue(op2)
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = getValue(op1) / getValue(op2)
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = getValue(op1) / getValue(op2)
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = getValue(op1) / getValue(op2)
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = getValue(op1) / getValue(op2)
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = getValue(op1) / getValue(op2)
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = getValue(op1) / getValue(op2)
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = getValue(op1) / getValue(op2)
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = getValue(op1) / getValue(op2)
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = getValue(op1) / getValue(op2)
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = getValue(op1) / getValue(op2)
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = getValue(op1) / getValue(op2)
    elif operator == '%':
        if getValue(op2) == 0:
            utils.showError('Cannot perform a division by 0!')
        
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = getValue(op1) % getValue(op2)
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = getValue(op1) % getValue(op2)
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = getValue(op1) % getValue(op2)
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = getValue(op1) % getValue(op2)
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = getValue(op1) % getValue(op2)
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = getValue(op1) % getValue(op2)
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = getValue(op1) % getValue(op2)
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = getValue(op1) % getValue(op2)
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = getValue(op1) % getValue(op2)
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = getValue(op1) % getValue(op2)
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = getValue(op1) % getValue(op2)
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = getValue(op1) % getValue(op2)
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = getValue(op1) % getValue(op2)
    elif operator == '<':
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(getValue(op1) < getValue(op2))
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(getValue(op1) < getValue(op2))
    elif operator == '<=':
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(getValue(op1) <= getValue(op2))
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(getValue(op1) <= getValue(op2))
    elif operator == '>':
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(getValue(op1) > getValue(op2))
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(getValue(op1) > getValue(op2))
    elif operator == '>=':
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(getValue(op1) >= getValue(op2))
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(getValue(op1) >= getValue(op2))
    elif operator == '==':
        operatorToString1 = str(op1)
        operatorToString2 = str(op2)
        if operatorToString1[0] == '(' and operatorToString1[-1] == ')':
            op1 = getValue(int(operatorToString1[1:-1]))
        if operatorToString2[0] == '(' and operatorToString2[-1] == ')':
            op2 = getValue(int(operatorToString2[1:-1]))

        if ((3000 <= op1 < 4000 or 7000 <= op1 < 8000 or 11000 <= op1 < 12000 or 15000 <= op1 < 16000) and (3000 <= op2 < 4000 or 7000 <= op2 < 8000 or 11000 <= op2 < 12000 or 15000 <= op2 < 16000)):
            if 1000 <= res < 2000:
                vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 2000 <= res < 3000:
                vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 3000 <= res < 4000:
                vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 4000 <= res < 5000:
                vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 5000 <= res < 6000:
                vmemory.globalInts[res - 5000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 6000 <= res < 7000:
                vmemory.globalFloats[res - 6000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 7000 <= res < 8000:
                vmemory.globalBools[res - 7000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 8000 <= res < 9000:
                vmemory.globalStrings[res - 8000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 13000 <= res < 14000:
                vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 14000 <= res < 15000:
                vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 15000 <= res < 16000:
                vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 16000 <= res < 17000:
                vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
            elif 17000 <= res < 18000:
                vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(changeToUpperCase(getValue(op1)) == changeToUpperCase(getValue(op2)))
        else:
            if 1000 <= res < 2000:
                vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 2000 <= res < 3000:
                vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 3000 <= res < 4000:
                vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 4000 <= res < 5000:
                vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 5000 <= res < 6000:
                vmemory.globalInts[res - 5000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 6000 <= res < 7000:
                vmemory.globalFloats[res - 6000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 7000 <= res < 8000:
                vmemory.globalBools[res - 7000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 8000 <= res < 9000:
                vmemory.globalStrings[res - 8000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 13000 <= res < 14000:
                vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 14000 <= res < 15000:
                vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 15000 <= res < 16000:
                vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 16000 <= res < 17000:
                vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(getValue(op1) == getValue(op2))
            elif 17000 <= res < 18000:
                vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(getValue(op1) == getValue(op2))
    elif operator == '<>':
        operatorToString1 = str(op1)
        operatorToString2 = str(op2)
        if operatorToString1[0] == '(' and operatorToString1[-1] == ')':
            op1 = getValue(int(operatorToString1[1:-1]))
        if operatorToString2[0] == '(' and operatorToString2[-1] == ')':
            op2 = getValue(int(operatorToString2[1:-1]))

        if ((3000 <= op1 < 4000 or 7000 <= op1 < 8000 or 11000 <= op1 < 12000 or 15000 <= op1 < 16000) and (3000 <= op2 < 4000 or 7000 <= op2 < 8000 or 11000 <= op2 < 12000 or 15000 <= op2 < 16000)):
            if 1000 <= res < 2000:
                vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 2000 <= res < 3000:
                vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 3000 <= res < 4000:
                vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 4000 <= res < 5000:
                vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 5000 <= res < 6000:
                vmemory.globalInts[res - 5000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 6000 <= res < 7000:
                vmemory.globalFloats[res - 6000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 7000 <= res < 8000:
                vmemory.globalBools[res - 7000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 8000 <= res < 9000:
                vmemory.globalStrings[res - 8000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 13000 <= res < 14000:
                vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 14000 <= res < 15000:
                vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 15000 <= res < 16000:
                vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 16000 <= res < 17000:
                vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
            elif 17000 <= res < 18000:
                vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(changeToUpperCase(getValue(op1)) != changeToUpperCase(getValue(op2)))
        else:
            if 1000 <= res < 2000:
                vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 2000 <= res < 3000:
                vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 3000 <= res < 4000:
                vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 4000 <= res < 5000:
                vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 5000 <= res < 6000:
                vmemory.globalInts[res - 5000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 6000 <= res < 7000:
                vmemory.globalFloats[res - 6000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 7000 <= res < 8000:
                vmemory.globalBools[res - 7000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 8000 <= res < 9000:
                vmemory.globalStrings[res - 8000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 13000 <= res < 14000:
                vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 14000 <= res < 15000:
                vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 15000 <= res < 16000:
                vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 16000 <= res < 17000:
                vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(getValue(op1) != getValue(op2))
            elif 17000 <= res < 18000:
                vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(getValue(op1) != getValue(op2))
    elif operator == '&&':
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(changeToUpperCase(getValue(op1)) and changeToUpperCase(getValue(op2)))
    elif operator == '||':
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 14000 <= res < 15000:
            vmemory.tempFloatsStack[-1][res - 14000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = changeToLowerCase(changeToUpperCase(getValue(op1)) or changeToUpperCase(getValue(op2)))
    elif operator == '=':
        resToString = str(res)
        if resToString[0] == '(' and resToString[-1] == ')':
            res = getValue(int(resToString[1:-1]))
        if 1000 <= res < 2000:
            vmemory.localIntsStack[-1][res - 1000] = getValue(op1)
        elif 2000 <= res < 3000:
            vmemory.localFloatsStack[-1][res - 2000] = getValue(op1)
        elif 3000 <= res < 4000:
            vmemory.localBoolsStack[-1][res - 3000] = getValue(op1)
        elif 4000 <= res < 5000:
            vmemory.localStringsStack[-1][res - 4000] = getValue(op1)
        elif 5000 <= res < 6000:
            vmemory.globalInts[res - 5000] = getValue(op1)
        elif 6000 <= res < 7000:
            vmemory.globalFloats[res - 6000] = getValue(op1)
        elif 7000 <= res < 8000:
            vmemory.globalBools[res - 7000] = getValue(op1)
        elif 8000 <= res < 9000:
            vmemory.globalStrings[res - 8000] = getValue(op1)
        elif 13000 <= res < 14000:
            vmemory.tempIntsStack[-1][res - 13000] = getValue(op1)
        elif 14000 <= res < 15000:
            vmemory.tempFloats[res - 14000] = getValue(op1)
        elif 15000 <= res < 16000:
            vmemory.tempBoolsStack[-1][res - 15000] = getValue(op1)
        elif 16000 <= res < 17000:
            vmemory.tempStringsStack[-1][res - 16000] = getValue(op1)
        elif 17000 <= res < 18000:
            vmemory.tempPointersStack[-1][res - 17000] = getValue(op1)
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
        currentFunction = res
        
        for i in range(0, vars_table[currentFunction]['noVars']['int'] + vars_table[currentFunction]['noParams']['int']):
            vmemory.localInts.append(None)
        for i in range(0, vars_table[currentFunction]['noVars']['float'] + vars_table[currentFunction]['noParams']['float']):
            vmemory.localFloats.append(None)
        for i in range(0, vars_table[currentFunction]['noVars']['bool'] + vars_table[currentFunction]['noParams']['bool']):
            vmemory.localBools.append(None)
        for i in range(0, vars_table[currentFunction]['noVars']['string'] + vars_table[currentFunction]['noParams']['string']):
            vmemory.localStrings.append(None)
        
        for i in range(0, vars_table[currentFunction]['noTemps']['int']):
            vmemory.tempInts.append(None)
        for i in range(0, vars_table[currentFunction]['noTemps']['float']):
            vmemory.tempFloats.append(None)
        for i in range(0, vars_table[currentFunction]['noTemps']['bool']):
            vmemory.tempBools.append(None)
        for i in range(0, vars_table[currentFunction]['noTemps']['string']):
            vmemory.tempStrings.append(None)
        for i in range(0, vars_table[currentFunction]['noTemps']['pointer']):
            vmemory.tempPointers.append(None)

        parameters = list(vars_table[currentFunction]['vars'])

    elif operator == 'PARAM':
        parameter = op1
        idx = int(res[-1]) - 1
       
        if (len(parameters) > 0):
            if 1000 <= parameter < 2000 or 5000 <= parameter < 6000 or 9000 <= parameter < 10000 or 13000 <= parameter < 14000:
                vmemory.localInts[vars_table[currentFunction]['vars'][parameters[idx]]['memory'] - 1000] = getValue(parameter)
            if 2000 <= parameter < 3000 or 6000 <= parameter < 7000 or 10000 <= parameter < 11000 or 14000 <= parameter < 15000:
                vmemory.localFloats[vars_table[currentFunction]['vars'][parameters[idx]]['memory'] - 2000] = getValue(parameter)
            if 3000 <= parameter < 4000 or 7000 <= parameter < 8000 or 11000 <= parameter < 12000 or 15000 <= parameter < 16000:
                vmemory.localBools[vars_table[currentFunction]['vars'][parameters[idx]]['memory'] - 3000] = getValue(parameter)
            if 4000 <= parameter < 5000 or 8000 <= parameter < 9000 or 12000 <= parameter < 13000 or 16000 <= parameter < 17000:
                vmemory.localStrings[vars_table[currentFunction]['vars'][parameters[idx]]['memory'] - 4000] = getValue(parameter)

    elif operator == 'GOSUB':
        destination = res
        
        callsStack.append(current)
        functionsStack.append(currentFunction)
        currentFunction = destination

        vmemory.resetLocalMemory()
        vmemory.resetTempMemory()
        
        current = vars_table[destination]['cuadruple']
        continue
    elif operator == 'RETURN':
        currentFunctionType = vars_table[currentFunction]['type']
       
        memoryPos = 0
        if currentFunctionType != 'void':
            memoryPos = vars_table[programName]['vars'][currentFunction]['memory']

        if res != None:
            if currentFunctionType == 'int':
                vmemory.globalInts[memoryPos - 5000] = getValue(res)
            elif currentFunctionType =='float':
                vmemory.globalFloats[memoryPos - 6000] = getValue(res)
            elif currentFunctionType == 'bool':
                vmemory.globalBools[memoryPos - 7000] = getValue(res)
            elif currentFunctionType == 'string':
                vmemory.globalStrings[memoryPos - 8000] = getValue(res)

        vmemory.localIntsStack.pop()
        vmemory.localFloatsStack.pop()
        vmemory.localBoolsStack.pop()
        vmemory.localStringsStack.pop()

        vmemory.tempIntsStack.pop()
        vmemory.tempFloatsStack.pop()
        vmemory.tempBoolsStack.pop()
        vmemory.tempStringsStack.pop()
        vmemory.tempPointersStack.pop()

        current = callsStack.pop() + 1
        currentFunction = functionsStack.pop()
        continue
    elif operator == 'ENDFUNC':
        vmemory.localIntsStack.pop()
        vmemory.localFloatsStack.pop()
        vmemory.localBoolsStack.pop()
        vmemory.localStringsStack.pop()

        vmemory.tempIntsStack.pop()
        vmemory.tempFloatsStack.pop()
        vmemory.tempBoolsStack.pop()
        vmemory.tempStringsStack.pop()
        vmemory.tempPointersStack.pop()
        
        current = callsStack.pop() + 1
        currentFunction = functionsStack.pop()
        continue

    
    current += 1