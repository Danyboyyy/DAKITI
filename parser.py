import sys
import ply.yacc as yacc
from lexer import tokens

# Grammar rules

# PROGRAM
def p_program_1(p):
    '''
    program_1 : PROGRAM VAR_CTE_ID SEMI_COLON program_vars program_functions MAIN body_1 END
    '''
    print('Compiled succesfully!')

def p_program_vars(p):
    '''
    program_vars : vars_1
                 | empty
    '''

def p_program_functions(p):
    '''
    program_functions : functions
                      | empty
    '''

# VARS
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
    vars_3 : VAR_CTE_ID COMMA vars_3
           | VAR_CTE_ID SEMI_COLON vars_2
           | VAR_CTE_ID LEFT_BRACK VAR_CTE_INT RIGHT_BRACK SEMI_COLON vars_2
    '''

# FUNCTIONS
def p_functions(p):
    '''
    functions : functions_t program_functions
              | functions_v program_functions
    '''

def p_functions_t(p):
    '''
    functions_t : FUNCTION type VAR_CTE_ID LEFT_PAR arguments_1 RIGHT_PAR LEFT_KEY program_vars statements return RIGHT_KEY
    '''

def p_functions_v(p):
    '''
    functions_v : FUNCTION VOID VAR_CTE_ID LEFT_PAR arguments_1 RIGHT_PAR LEFT_KEY program_vars statements RIGHT_KEY
    '''

def p_arguments_1(p):
    '''
    arguments_1 : arguments_2
                | empty
    '''

def p_arguments_2(p):
    '''
    arguments_2 : type VAR_CTE_ID arguments_3
    '''

def p_arguments_3(p):
    '''
    arguments_3 : COMMA arguments_2
                | empty
    '''

def p_return(p):
    '''
    return : RETURN LEFT_PAR hyper_expression_1 RIGHT_PAR SEMI_COLON
    '''

# TYPE
def p_type(p):
    '''
    type : INT
         | FLOAT
         | BOOL
         | STRING
    '''

# BLOQUE
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

# FUNCTION CALL
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

# WRITTIG
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

# EXPRESSION
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

# EXP
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

# TERM
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

# FACTOR
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

# CONDITION
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
    for_loop : FOR LEFT_PAR VAR_CTE_ID IN RANGE LEFT_PAR VAR_CTE_FLOAT COMMA VAR_CTE_FLOAT RIGHT_PAR RIGHT_PAR body_1
    '''

# VAR_CTE
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

# def p_var_cte_aux_1(p):
#     '''
#     var_cte_aux_1 : VAR_CTE_ID vars_5
#     '''

# Error handling
def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Empty
def p_empty(p):
    'empty :'
    pass

yacc.yacc()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]

        try:
            ifFile = open(file, 'r')
            data = ifFile.read()
            ifFile.close()
            print(yacc.parse(data))
        except:
            print("Error opening the file!")
    else:
        print("Try running the following command: python parser.py name_of_file.txt")