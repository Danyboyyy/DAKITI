import sys
import re
from os import path
import ply.yacc as yacc
from lexer import tokens
from queue import Queue, LifoQueue

vars_table = {} # Variables Table

currentFunction = ''
currentFunctionType = ''
currentType = ''
currentVar = ''
currentArrayTam = 0

def displayVarsTable():
    for func in vars_table:
        print(func)
        for var in vars_table[func]['vars']:
            print(vars_table[func]['vars'][var]['type'], var)
        print('\n')

def showError(msg):
    print(msg)
    sys.exit()

###### PARSER #####
# PROGRAM
def p_program_1(p):
    '''
    program_1 : PROGRAM VAR_CTE_ID np_program_start SEMI_COLON program_vars program_functions MAIN body_1 END np_program_end
    '''
    print('Compiled succesfully!')
    displayVarsTable()

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
    functions_2 : FUNCTION function_type VAR_CTE_ID np_add_function LEFT_PAR arguments_1 RIGHT_PAR LEFT_KEY program_vars body_2 return RIGHT_KEY
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
    return : RETURN LEFT_PAR hyper_expression_1 RIGHT_PAR SEMI_COLON
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
               | function_call_2
               | loops
    '''

# ASSIGNMENT
def p_assignment_1(p):
    '''
    assignment_1 : VAR_CTE_ID EQUAL hyper_expression_1 SEMI_COLON
                 | VAR_CTE_ID LEFT_BRACK hyper_expression_1 RIGHT_BRACK EQUAL hyper_expression_1 SEMI_COLON
    '''

# FUNCTION CALLS
def p_function_call_1(p):
    '''
    function_call_1 : function_call_name LEFT_PAR function_call_arguments_1 RIGHT_PAR
    '''

def p_function_call_2(p):
    '''
    function_call_2 : function_call_1 SEMI_COLON
    '''

def p_function_call_name(p):
    '''
    function_call_name : VAR_CTE_ID
                       | built_in_functions
    '''

def p_function_call_arguments_1(p):
    '''
    function_call_arguments_1 : function_call_arguments_2
                              | empty
    '''

def p_function_call_arguments_2(p):
    '''
    function_call_arguments_2 : hyper_expression_1 function_call_arguments_3
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
    writting_2 : hyper_expression_1 writting_3
               | VAR_CTE_STRING writting_3
    '''

def p_writting_3(p):
    '''
    writting_3 : COMMA writting_2
               | empty
    '''

# EXPRESSIONS
def p_hyper_expression_1(p):
    '''
    hyper_expression_1 : expression_1 hyper_expression_2
    '''

def p_hyper_expression_2(p):
    '''
    hyper_expression_2 : AND expression_1
                       | OR expression_1
                       | empty
    '''

def p_expression_1(p):
    '''
    expression_1 : exp_1 expression_2
    '''

def p_expression_2(p):
    '''
    expression_2 : GREATER_THAN exp_1
                 | GREATER_E_THAN exp_1
                 | LESS_THAN exp_1
                 | LESS_E_THAN exp_1
                 | NOT_EQUALS exp_1
                 | EQUALS exp_1
                 | empty
    '''

def p_exp_1(p):
    '''
    exp_1 : term_1 exp_2
    '''

def p_exp_2(p):
    '''
    exp_2 : PLUS exp_1
          | MINUS exp_1
          | empty
    '''

def p_term_1(p):
    '''
    term_1 : factor_1 term_2
    '''

def p_term_2(p):
    '''
    term_2 : TIMES term_1
           | DIV term_1
           | MOD term_1
           | empty
    '''

def p_factor_1(p):
    '''
    factor_1 : LEFT_PAR expression_1 RIGHT_PAR
             | factor_2 var_cte
    '''

def p_factor_2(p):
    '''
    factor_2 : PLUS
             | MINUS
             | empty
    '''

# CONDITIONALS
def p_condition_1(p):
    '''
    condition_1 : IF LEFT_PAR hyper_expression_1 RIGHT_PAR body_1 condition_2
    '''

def p_condition_2(p):
    '''
    condition_2 : ELSE condition_1
                | ELSE body_1
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
    while_loop : WHILE LEFT_PAR hyper_expression_1 RIGHT_PAR body_1
    '''

def p_for_loop(p):
    '''
    for_loop : FOR LEFT_PAR VAR_CTE_ID IN RANGE LEFT_PAR VAR_CTE_INT COMMA VAR_CTE_INT RIGHT_PAR RIGHT_PAR body_1
    '''

# CONSTANT VARIABLES
def p_var_cte(p):
    '''
    var_cte : VAR_CTE_ID
            | VAR_CTE_ID LEFT_BRACK hyper_expression_1 RIGHT_BRACK
            | VAR_CTE_INT
            | VAR_CTE_FLOAT
            | TRUE
            | FALSE
            | function_call_1
    '''

# Error handling
def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Empty production
def p_empty(p):
    'empty :'
    pass

##### NEURALGIC POINTS #####
# Starting the program
def p_np_program_start(p):
    'np_program_start :'
    global currentFunction

    program = p[-1]
    currentFunction = program

    vars_table[program] = {'type': 'void', 'vars': {}}

# Ending the program
def p_np_program_end(p):
    'np_program_end :'

# Adding a function to the functions directory
def p_np_add_function(p):
    'np_add_function :'
    global currentFunction, currentFunctionType
    currentFunction = p[-1]
    if currentFunction not in vars_table:
        vars_table[currentFunction] = {'type': currentFunctionType, 'vars': {}}
    else:
        showError('Function already declared!')

# Storing a variable's type
def p_np_current_type(p):
    'np_current_type :'
    global currentType
    currentType = p[-1]

# Storgin a function's type
def p_np_current_function_type(p):
    'np_current_function_type :'
    global currentFunctionType
    currentFunctionType = p[-1]

# Adding a variable to the symbols table
def p_np_add_variable(p):
    'np_add_variable :'
    global currentType, currentVar
    currentVar = p[-1]
    
    if currentVar not in vars_table[currentFunction]['vars']:
        vars_table[currentFunction]['vars'][currentVar] = {'type': currentType}
    else:
        showError('Variable already declared!')

# Adding an array to the symbols table
def p_np_add_array(p):
    'np_add_array :'
    global currentType, currentVar, currentArrayTam
    currentVar = p[-4]
    currentArrayTam = p[-2]

    if currentVar not in vars_table[currentFunction]['vars']:
        vars_table[currentFunction]['vars'][currentVar] = {'type': currentType, 'size': currentArrayTam}
    else:
        showError('Variable already declared!')

# Adding a function's parameters to its symbol table
def p_np_function_parameters(p):
    'np_function_parameters :'
    global currentFunction, currentVar, currentType
    currentVar = p[-1]

    if currentVar not in vars_table[currentFunction]['vars']:
        vars_table[currentFunction]['vars'][currentVar] = {'type': currentType}
    else:
        showError('Variable already declared!')

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
        print(yacc.parse(data))
    except EOFError:
        print("Error, try again!")