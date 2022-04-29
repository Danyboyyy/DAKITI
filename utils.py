import sys

def showError(msg):
    print(msg)
    sys.exit()

def displayVarsTable(vars_table):
    for func in vars_table:
        print(func)
        for var in vars_table[func]['vars']:
            print(vars_table[func]['vars'][var]['type'], var)
        print('\n')

def displayCuadruples(cuadruples):
    idx = 1
    for c in cuadruples:
        print(f'{idx}: {c.operator}, {c.op1}, {c.op2}, {c.res}')
        idx += 1

def displayCuadruple(c):
    print(f'{c.operator}, {c.op1}, {c.op2}, {c.res}')

def displayStack(stack):
    for el in stack:
        print(el)
    print('************************')