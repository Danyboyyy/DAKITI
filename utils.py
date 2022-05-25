import sys

def showError(msg):
    print(msg)
    sys.exit()

def displayVarsTable(vars_table):
    for func in vars_table:
        print('Function name: ', func)
        for var in vars_table[func]['vars']:
            print(vars_table[func]['vars'][var]['type'], var, vars_table[func]['vars'][var]['memory'])
        print('Starts at cudaruple: ', vars_table[func]['cuadruple'])
        print('No of params: ', vars_table[func]['noParams'])
        print('No of vars: ', vars_table[func]['noVars'])
        print('No of temps: ', vars_table[func]['noTemps'])
        print('\n')

def displayConstantsTable(constants_table):
    for type in constants_table:
        print('Type: ', type)
        for var in constants_table[type]:
            print(var, constants_table[type][var]['memory'])

def displayMemory(memory):
    for address in memory:
        print(address, memory[address])

def displayCuadruples(cuadruples):
    idx = 0
    for c in cuadruples:
        print(f'{idx}: {c.operator}, {c.op1}, {c.op2}, {c.res}')
        idx += 1

def displayCuadruple(c):
    print(f'{c.operator}, {c.op1}, {c.op2}, {c.res}')

def displayStack(stack):
    for el in stack:
        print(el)
    print('************************')