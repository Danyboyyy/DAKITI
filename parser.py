import sys
import re
from os import path
import ply.yacc as yacc
from lexer import tokens
from collections import deque
from SemanticCube import semantic_cube
from Cuadruple import *
import utils

vars_table = {} # Variables Table
cuadruples = [] # Cuadrulpes List

# Memory Simulation
memory = ['t' + str(x) for x in range(1, 100)]
idx = 0

# Stacks for building cuadruples
operatorsStack = deque() # Operators stack
operandsStack = deque() # Operands stack
typesStack = deque() # Types stack
jumpsStack = deque() # Jumps stack

# Auxiliary Variables
programName = ''

currentFunction = ''
currentFunctionType = ''

currentVar = ''
currentType = ''
currentArrayTam = 0

numParams = 0
numVars = 0
numTemps = 0
hasReturn = False

countParams = 0
origin = ''

controlVar = 0
finalVar = 0

###### PARSER #####
# PROGRAM
def p_program_1(p):
    '''
    program_1 : PROGRAM VAR_CTE_ID np_program_start SEMI_COLON program_vars program_functions MAIN body_1 END np_program_end
    '''
    utils.displayVarsTable(vars_table)
    utils.displayCuadruples(cuadruples)
    utils.displayStack(operandsStack)
    print('Compiled succesfully!')

def p_program_vars(p):
    '''
    program_vars : vars_1
                 | empty
    '''

def p_program_functions(p):
    '''
    program_functions : functions_1
                      | empty
    '''

# VARIABLES
def p_vars_1(p):
    '''
    vars_1 : VARS vars_2
    '''

def p_vars_2(p):
    '''
    vars_2 : type vars_3
           | empty
    '''

def p_vars_3(p):
    '''
    vars_3 : VAR_CTE_ID np_add_variable COMMA vars_3
           | VAR_CTE_ID np_add_variable SEMI_COLON vars_2
           | VAR_CTE_ID LEFT_BRACK VAR_CTE_INT RIGHT_BRACK np_add_array COMMA vars_3
           | VAR_CTE_ID LEFT_BRACK VAR_CTE_INT RIGHT_BRACK np_add_array SEMI_COLON vars_2
    '''

# FUNCTIONS
def p_functions_1(p):
    '''
    functions_1 :  functions_2 program_functions
    '''

def p_functions_2(p):
    '''
    functions_2 : FUNCTION function_type VAR_CTE_ID np_add_function LEFT_PAR arguments_1 RIGHT_PAR LEFT_KEY program_vars np_add_function_info body_2 return RIGHT_KEY np_end_function
    '''

def p_arguments_1(p):
    '''
    arguments_1 : arguments_2
                | empty
    '''

def p_arguments_2(p):
    '''
    arguments_2 : type VAR_CTE_ID np_function_parameters arguments_3
    '''

def p_arguments_3(p):
    '''
    arguments_3 : COMMA arguments_2
                | empty
    '''

def p_return(p):
    '''
    return : RETURN LEFT_PAR hyper_expression_1 np_return RIGHT_PAR SEMI_COLON
           | empty
    '''

# TYPES
def p_type(p):
    '''
    type : INT np_current_type
         | FLOAT np_current_type
         | BOOL np_current_type
         | STRING np_current_type
    '''

def p_function_type(p):
    '''
    function_type : INT np_current_function_type
                  | FLOAT np_current_function_type
                  | BOOL np_current_function_type
                  | STRING np_current_function_type
                  | VOID np_current_function_type
    '''

# BLOCK OF CODE
def p_body_1(p):
    '''
    body_1 : LEFT_KEY body_2 RIGHT_KEY
    '''

def p_body_2(p):
    '''
    body_2 : statements body_2
           | empty
    '''

# STATEMENTS
def p_statements(p):
    '''
    statements : assignment_1
               | condition_1
               | writting_1
               | function_call_2 np_check_void_function
               | loops
    '''

# ASSIGNMENT
def p_assignment_1(p):
    '''
    assignment_1 : VAR_CTE_ID np_add_id EQUAL np_add_operator hyper_expression_1 np_assignment SEMI_COLON
                 | VAR_CTE_ID LEFT_BRACK hyper_expression_1 RIGHT_BRACK EQUAL np_add_operator hyper_expression_1 SEMI_COLON
    '''

# FUNCTION CALLS
def p_function_call_1(p):
    '''
    function_call_1 : function_call_name LEFT_PAR function_call_arguments_1 np_count_parameters RIGHT_PAR np_function_call_end
    '''

def p_function_call_2(p):
    '''
    function_call_2 : function_call_1 SEMI_COLON
    '''

def p_function_call_name(p):
    '''
    function_call_name : VAR_CTE_ID np_function_call_start
                       | built_in_functions
    '''

def p_function_call_arguments_1(p):
    '''
    function_call_arguments_1 : function_call_arguments_2
                              | empty
    '''

def p_function_call_arguments_2(p):
    '''
    function_call_arguments_2 : hyper_expression_1 np_check_parameter function_call_arguments_3
    '''

def p_function_call_arguments_3(p):
    '''
    function_call_arguments_3 : COMMA function_call_arguments_2
                              | empty
    '''

def p_built_in_functions(p):
    '''
    built_in_functions : PENUP
                       | PENDOWN
                       | FORWARD
                       | BACKWARD
                       | TURNRIGHT
                       | TURNLEFT
                       | DRAWCIRCLE
                       | DRAWRECTANGLE
                       | DRAWARC
    '''

# WRITTING
def p_writting_1(p):
    '''
    writting_1 : PRINT LEFT_PAR writting_2 RIGHT_PAR SEMI_COLON
    '''

def p_writting_2(p):
    '''
    writting_2 : hyper_expression_1 np_writting writting_3
               | VAR_CTE_STRING np_writting_strings writting_3
    '''

def p_writting_3(p):
    '''
    writting_3 : COMMA writting_2
               | empty
    '''

# EXPRESSIONS
def p_hyper_expression_1(p):
    '''
    hyper_expression_1 : expression_1 np_hyper_expression hyper_expression_2
    '''

def p_hyper_expression_2(p):
    '''
    hyper_expression_2 : AND np_add_operator hyper_expression_1
                       | OR np_add_operator hyper_expression_1
                       | empty
    '''

def p_expression_1(p):
    '''
    expression_1 : exp_1 np_expression expression_2
    '''

def p_expression_2(p):
    '''
    expression_2 : GREATER_THAN np_add_operator expression_1
                 | GREATER_E_THAN np_add_operator expression_1
                 | LESS_THAN np_add_operator expression_1
                 | LESS_E_THAN np_add_operator expression_1
                 | NOT_EQUALS np_add_operator expression_1
                 | EQUALS np_add_operator expression_1
                 | empty
    '''

def p_exp_1(p):
    '''
    exp_1 : term_1 np_exp exp_2
    '''

def p_exp_2(p):
    '''
    exp_2 : PLUS np_add_operator exp_1
          | MINUS np_add_operator exp_1
          | empty
    '''

def p_term_1(p):
    '''
    term_1 : factor_1 np_term term_2
    '''

def p_term_2(p):
    '''
    term_2 : TIMES np_add_operator term_1
           | DIV np_add_operator term_1
           | MOD np_add_operator term_1
           | empty
    '''

def p_factor_1(p):
    '''
    factor_1 : LEFT_PAR np_add_bottom hyper_expression_1 RIGHT_PAR np_remove_bottom
             | var_cte
    '''

# CONSTANT VARIABLES
def p_var_cte(p):
    '''
    var_cte : VAR_CTE_ID np_add_id
            | VAR_CTE_ID LEFT_BRACK hyper_expression_1 RIGHT_BRACK
            | VAR_CTE_INT np_add_int
            | VAR_CTE_FLOAT np_add_float
            | TRUE np_add_bool
            | FALSE np_add_bool
            | function_call_1 np_check_non_void_function
    '''

# CONDITIONALS
def p_condition_1(p):
    '''
    condition_1 : IF LEFT_PAR hyper_expression_1 RIGHT_PAR np_if_start body_1 condition_2 np_if_end
    '''

def p_condition_2(p):
    '''
    condition_2 : ELSE np_else IF LEFT_PAR hyper_expression_1 RIGHT_PAR np_if_start body_1 condition_2 np_if_end
                | ELSE np_else body_1
                | empty
    '''

# LOOPS
def p_loops(p):
    '''
    loops : for_loop
          | while_loop
    '''

def p_while_loop(p):
    '''
    while_loop : WHILE np_while_start LEFT_PAR hyper_expression_1 RIGHT_PAR np_while_mid body_1 np_while_end
    '''

def p_for_loop(p):
    '''
    for_loop : FOR LEFT_PAR VAR_CTE_ID np_for_start IN RANGE LEFT_PAR VAR_CTE_INT np_for_range_start COMMA VAR_CTE_INT np_for_range_end RIGHT_PAR RIGHT_PAR body_1 np_for_end
    '''

# Error handling
def p_error(p):
    print(f'Syntax error at {p.value!r}')
    sys.exit()

# Empty production
def p_empty(p):
    'empty :'
    pass

##### NEURALGIC POINTS #####
# Starting the program
def p_np_program_start(p):
    'np_program_start :'
    global currentFunction, programName

    programName = p[-1]
    currentFunction = programName

    vars_table[programName] = {'type': 'void', 'vars': {}, 'params': {}, 'cuadruple': len(cuadruples), 'noVars': 0, 'noParams': 0, 'noTemps': 0}

    cuadruples.append(Cuadruple('GOTO', None, None, 'main'))

# Ending the program
def p_np_program_end(p):
    'np_program_end :'
    pass

# Adding a function to the functions directory
def p_np_add_function(p):
    'np_add_function :'
    global currentFunction, currentFunctionType, numVars, numTemps, hasReturn

    numVars = 0
    numTemps = 0
    hasReturn = False
    currentFunction = p[-1]
    if currentFunction not in vars_table:
        vars_table[currentFunction] = {'type': currentFunctionType, 'vars': {}, 'params': {}, 'cuadruple': len(cuadruples), 'noVars': 0, 'noParams': 0, 'noTemps': 0}

        if currentFunctionType != 'void':
            if currentFunction not in vars_table[programName]['vars']:
                vars_table[programName]['vars'][currentFunction] = {'type': currentFunctionType}
            else:
                utils.showError(f'Name \'{currentFunction}\' has already been used for a variable!')
    else:
        utils.showError(f'Function \'{currentFunction}\' has already been declared!')

# Ending a function
def p_np_end_function(p):
    'np_end_function :'
    global cuadruples, vars_table, numTemps, currentFunction, currentFunctionType, hasReturn

    if currentFunctionType == 'void' and hasReturn:
        utils.showError(f'Functions of type \'void\' must not have a return statement!')
    if currentFunctionType != 'void' and not hasReturn:
        utils.showError(f'Functions of type other than \'void\' must have a return statement!')
    
    cuadruples.append(Cuadruple('ENDFUNC', None, None, None))
    vars_table[currentFunction]['noTemps'] = numTemps
    hasReturn = False


# Adding a function's parameters to its symbol table
def p_np_function_parameters(p):
    'np_function_parameters :'
    global currentFunction, currentVar, currentType, numParams

    currentVar = p[-1]

    if currentVar not in vars_table[currentFunction]['vars']:
        vars_table[currentFunction]['vars'][currentVar] = {'type': currentType}

        if len(vars_table[currentFunction]['params']) == 0:
            numParams = 0
        
        vars_table[currentFunction]['params'][numParams] = currentType

        numParams += 1
    else:
        utils.showError(f'Variable \'{currentVar}\' has already been declared!')

# Adding relevant information to the function's directory
def p_np_add_function_info(p):
    'np_add_function_info :'
    global vars_table, numParams, numVars

    vars_table[currentFunction]['noParams'] = len(vars_table[currentFunction]['params'])
    vars_table[currentFunction]['noVars'] = numVars

# Returns in functions
def p_np_return(p):
    'np_return :'
    global hasReturn, cuadruples, operandsStack, typesStack, currentFunctionType

    hasReturn = True
    returnValue = operandsStack.pop()
    returnType = typesStack.pop()

    if returnType == currentFunctionType:
        cuadruples.append(Cuadruple('RETURN', None, None, returnValue))
    else:
        utils.showError(f'Return value \'{returnValue}\' of type \'{returnType}\' is not the same type as \'{currentFunctionType}\'!')
    
# Generate era cuadruple
def p_np_function_call_start(p):
    'np_function_call_start :'
    global countParams, currentFunction, operandsStack, origin

    calledFunction = p[-1]

    if calledFunction in vars_table:
        countParams = 0
        origin = currentFunction
        currentFunction = calledFunction
        operandsStack.append('(')
        cuadruples.append(Cuadruple('ERA', None, None, calledFunction))
    else:
        utils.showError(f'Function \'{currentFunction}\' has not been defined!')

# Validate that the parameters type match
def p_np_check_parameter(p):
    'np_check_parameter :'
    global countParams, currentFunction, typesStack, operandsStack, vars_table
    
    parameters = vars_table[currentFunction]['params']
    if countParams in parameters:
        argumentType = typesStack.pop()
        argument = operandsStack.pop()
        paramType = vars_table[currentFunction]['params'][countParams]

        if paramType == argumentType:
            cuadruples.append(Cuadruple('PARAM', argument, None, 'ARGUMENT#'+str(countParams + 1)))
        else:
            utils.showError(f'Argument #{countParams + 1} must be of type \'{paramType}\'')
    else:
        utils.showError(f'Function expected {len(parameters)} parameters and received {countParams + 1}')

    countParams += 1

# Verifiy that the number of parameters match
def p_np_count_parameters(p):
    'np_count_parameters :'
    global vars_table, countParams
    parameters = vars_table[currentFunction]['params']

    if len(parameters) != countParams:
        utils.showError(f'Function expected {len(parameters)} parameters and received {countParams}')

# Generate gosub cuadruple
def p_np_function_call_end(p):
    'np_function_call_end :'
    global cuadruples, currentFunction, operandsStack, vars_table
    cuadruples.append(Cuadruple('GOSUB', None, None, currentFunction))
    operandsStack.pop()

    operandsStack.append(currentFunction)
    typesStack.append(vars_table[currentFunction]['type'])
    
# Check usage of void functions
def p_np_check_void_function(p):
    'np_check_void_function :'
    global vars_table, currentFunction, origin

    if vars_table[currentFunction]['type'] != 'void':
        utils.showError(f'A non void function must be assigned to a variable or used in an expression!')
    
    currentFunction = origin

# Check usage of non void functions
def p_np_check_non_void_function(p):
    'np_check_non_void_function :'
    global vars_table, currentFunction, origin

    if vars_table[currentFunction]['type'] == 'void':
        utils.showError(f'A void function cannot be assigned to a variable or used in an expression!')
    
    currentFunction = origin

# Storing a function's type
def p_np_current_function_type(p):
    'np_current_function_type :'
    global currentFunctionType

    currentFunctionType = p[-1]

# Adding a variable to the symbols table
def p_np_add_variable(p):
    'np_add_variable :'
    global currentType, currentVar, numVars

    currentVar = p[-1]
    
    if currentVar not in vars_table[currentFunction]['vars']:
        vars_table[currentFunction]['vars'][currentVar] = {'type': currentType}
        numVars += 1
    else:
        utils.showError(f'Variable \'{currentVar}\' has already been declared!')

# Adding an array to the symbols table
def p_np_add_array(p):
    'np_add_array :'
    global currentType, currentVar, currentArrayTam

    currentVar = p[-4]
    currentArrayTam = p[-2]

    if currentVar not in vars_table[currentFunction]['vars']:
        vars_table[currentFunction]['vars'][currentVar] = {'type': currentType, 'size': currentArrayTam}
    else:
        utils.showError(f'Variable \'{currentVar}\' has already been declared!')

# Storing a variable's type
def p_np_current_type(p):
    'np_current_type :'
    global currentType

    currentType = p[-1]

# Adding operator to the operators stack
def p_np_add_operator(p):
    'np_add_operator :'
    global operatorsStack

    operator = p[-1]
    operatorsStack.append(operator)

# Add fake bottom
def p_np_add_bottom(p):
    'np_add_bottom :'
    global operatorsStack

    operator = p[-1]
    operatorsStack.append(operator)

# Removing fake bottom
def p_np_remove_bottom(p):
    'np_remove_bottom :'
    global operatorsStack

    operatorsStack.pop()

# Add id to the operands stack and type to the types stack
def p_np_add_id(p):
    'np_add_id :'
    global currentFunction, programName
    
    operand = p[-1]

    if operand in vars_table[currentFunction]['vars']:
        operandsStack.append(operand)
        typesStack.append(vars_table[currentFunction]['vars'][operand]['type'])
    elif operand in vars_table[programName]['vars']:
        operandsStack.append(operand)
        typesStack.append(vars_table[programName]['vars'][operand]['type'])
    else:
        utils.showError(f'Variable \'{operand}\' has not been declared!')

# Add int to the operands stack and type to the types stack
def p_np_add_int(p):
    'np_add_int :'
    global operandsStack, typesStack

    operand = p[-1]

    operandsStack.append(operand)
    typesStack.append('int')

# Add flaot to the operands stack and type to the types stack
def p_np_add_float(p):
    'np_add_float :'
    global operandsStack, typesStack

    operand = p[-1]

    operandsStack.append(operand)
    typesStack.append('float')

# Add bool to the operands stack and type to the types stack
def p_np_add_bool(p):
    'np_add_bool :'
    global operandsStack, typesStack

    operand = p[-1]

    operandsStack.append(operand)
    typesStack.append('bool')

# Handle hyper expressions
def p_np_hyper_expression(p):
    'np_hyper_expression :'
    global operatorsStack, operandsStack, typesStack, currentFunction, memory, idx, cuadruples, numTemps

    if (operatorsStack):
        operator = operatorsStack[-1]
        if operator == '&&' or operator == '||':
            right = operandsStack.pop()
            left = operandsStack.pop()
            rightType = typesStack.pop()
            leftType = typesStack.pop()
            operator = operatorsStack.pop()
            resultType = semantic_cube[leftType][rightType][operator]

            if resultType == 'error':
                utils.showError(f'Cannot perform \'{operator}\' with \'{leftType}\' and \'{rightType}\' as operands!')
            else:
                cuadruples.append(Cuadruple(operator, left, right, memory[idx]))
                operandsStack.append(memory[idx])
                typesStack.append(resultType)
                idx += 1
                numTemps += 1

# Handle expressions
def p_np_expression(p):
    'np_expression :'
    global operatorsStack, operandsStack, typesStack, currentFunction, memory, idx, cuadruples, numTemps

    if (operatorsStack):
        operator = operatorsStack[-1]
        if operator == '>' or operator == '>=' or operator == '<' or operator == '<=' or operator == '==' or operator == '<>':
            right = operandsStack.pop()
            left = operandsStack.pop()
            rightType = typesStack.pop()
            leftType = typesStack.pop()
            operator = operatorsStack.pop()
            resultType = semantic_cube[leftType][rightType][operator]

            if resultType == 'error':
                utils.showError(f'Cannot perform \'{operator}\' with \'{leftType}\' and \'{rightType}\' as operands!')
            else:
                cuadruples.append(Cuadruple(operator, left, right, memory[idx]))
                operandsStack.append(memory[idx])
                typesStack.append(resultType)
                idx += 1
                numTemps += 1

# Handle exps
def p_np_exp(p):
    'np_exp :'
    global operatorsStack, operandsStack, typesStack, currentFunction, memory, idx, cuadruples, numTemps

    if (operatorsStack):
        operator = operatorsStack[-1]
        if operator == '+' or operator == '-':
            right = operandsStack.pop()
            left = operandsStack.pop()
            rightType = typesStack.pop()
            leftType = typesStack.pop()
            operator = operatorsStack.pop()
            resultType = semantic_cube[leftType][rightType][operator]

            if resultType == 'error':
                utils.showError(f'Cannot perform \'{operator}\' with \'{leftType}\' and \'{rightType}\' as operands!')
            else:
                cuadruples.append(Cuadruple(operator, left, right, memory[idx]))
                operandsStack.append(memory[idx])
                typesStack.append(resultType)
                idx += 1
                numTemps += 1

# Handle terms
def p_np_term(p):
    'np_term :'
    global operatorsStack, operandsStack, typesStack, currentFunction, memory, idx, cuadruples, numTemps

    if (operatorsStack):
        operator = operatorsStack[-1]
        if operator == '*' or operator == '/' or operator == '%':
            right = operandsStack.pop()
            left = operandsStack.pop()
            rightType = typesStack.pop()
            leftType = typesStack.pop()
            operator = operatorsStack.pop()
            resultType = semantic_cube[leftType][rightType][operator]

            if resultType == 'error':
                utils.showError(f'Cannot perform \'{operator}\' with \'{leftType}\' and \'{rightType}\' as operands!')
            else:
                cuadruples.append(Cuadruple(operator, left, right, memory[idx]))
                operandsStack.append(memory[idx])
                typesStack.append(resultType)
                idx += 1
                numTemps += 1

# Handle assignments
def p_np_assignment(p):
    'np_assignment :'
    global operatorsStack, operandsStack, typesStack, cuadruples

    left = operandsStack.pop()
    right = operandsStack.pop()
    leftType = typesStack.pop()
    rightType = typesStack.pop()
    operator = operatorsStack.pop()

    if leftType != rightType:
        utils.showError(f'Cannot assign a(n) \'{leftType}\' to a(n) \'{rightType}\'!')
    else:
        cuadruples.append(Cuadruple(operator, left, None, right))

# Handle writting expressions
def p_np_writting(p):
    'np_writting :'
    global operandsStack, cuadruples
    operand = operandsStack[-1]
    cuadruples.append(Cuadruple('print', None, None, operand))
   
# Handle writting string
def p_np_writting_strings(p):
    'np_writting_strings :'
    global cuadruples
    string = p[-1]
    cuadruples.append(Cuadruple('print', None, None, string))

# Handle conditionals
def p_np_if_start(p):
    'np_if_start :'
    global cuadruples, typesStack, operandsStack, jumpsStack

    type = typesStack[-1]
    result = operandsStack[-1]

    if (type != 'bool'):
        utils.showError('Expression must return a bool!')

    cuadruples.append(Cuadruple('GOTOF', result, None, 0))
    jumpsStack.append(len(cuadruples) - 1)

def p_np_else(p):
    'np_else :'
    global cuadruples, jumpsStack

    cuadruples.append(Cuadruple('GOTO', None, None, 0))
    jump = jumpsStack.pop()
    jumpsStack.append(len(cuadruples) - 1)
    cuadruples[jump].res = len(cuadruples)

def p_np_if_end(p):
    'np_if_end :'
    global cuadruples, jumpsStack

    jump = jumpsStack.pop()
    cuadruples[jump].res = len(cuadruples)
    
# Handle while loop
def p_np_while_start(p):
    'np_while_start :'
    global cuadruples, jumpsStack

    jumpsStack.append(len(cuadruples))

def p_np_while_mid(p):
    'np_while_mid :'
    global cuadruples, typesStack, operandsStack, jumpsStack

    type = typesStack[-1]
    result = operandsStack[-1]

    if (type != 'bool'):
        utils.showError('Expression must return a bool!')

    cuadruples.append(Cuadruple('GOTOF', result, None, 0))
    jumpsStack.append(len(cuadruples) - 1)

def p_np_while_end(p):
    'np_while_end :'
    end = jumpsStack.pop()
    start = jumpsStack.pop()

    cuadruples.append(Cuadruple('GOTO', None, None, start))
    cuadruples[end].res = len(cuadruples)

# Handle for loop
def p_np_for_start(p):
    'np_for_start :'
    global currentFunction, programName, operandsStack, typesStack

    operand = p[-1]

    if operand in vars_table[currentFunction]['vars']:
        if vars_table[programName]['vars'][operand]['type'] == 'int':
            operandsStack.append(operand)
            typesStack.append('int')
        else:
            utils.showError(f'Variable \'{operand}\' must be an int!')
    elif operand in vars_table[programName]['vars']:
        if vars_table[programName]['vars'][operand]['type'] == 'int':
            operandsStack.append(operand)
            typesStack.append('int')
        else:
            utils.showError(f'Variable \'{operand}\' must be an int!')
    else:
        utils.showError(f'Variable \'{operand}\' has not been declared!')        
    

def p_np_for_range_start(p):
    'np_for_range_start :'
    global cuadruples, operandsStack, controlVar, numTemps

    start = p[-1]
    controlVar = start
    var = operandsStack[-1]

    cuadruples.append(Cuadruple('=', start, None, var))
    cuadruples.append(Cuadruple('=', var, None, 'VC'))

def p_np_for_range_end(p):
    'np_for_range_end :'
    global cuadruples, operandsStack, jumpsStack, controlVar, finalVar, memory, idx, numTemps

    end = p[-1]
    finalVar = end
    aux = memory[idx]

    cuadruples.append(Cuadruple('=', end, None, 'VF'))
    cuadruples.append(Cuadruple('<', 'VC', 'VF', aux))
    jumpsStack.append(len(cuadruples) - 1)
    cuadruples.append(Cuadruple('GOTOF', aux, None, 0))
    jumpsStack.append(len(cuadruples) - 1)

    idx += 1
    numTemps += 1
    

def p_np_for_end(p):
    'np_for_end :'
    global cuadruples, operandsStack, jumpsStack, memory, idx

    aux = memory[idx]

    cuadruples.append(Cuadruple('+', 'VC', 1, aux))
    cuadruples.append(Cuadruple('=', aux, None, 'VC'))
    cuadruples.append(Cuadruple('=', aux, None, operandsStack[-1]))

    end = jumpsStack.pop()
    ret = jumpsStack.pop()

    cuadruples.append(Cuadruple('GOTO', None, None, ret))
    cuadruples[end].res = len(cuadruples)

yacc.yacc()

##### PROGRAM EXECUTION #####
if __name__ == '__main__':
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

        yacc.parse(data)
    except EOFError:
        print("Error, try again!")