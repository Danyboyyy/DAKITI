import sys
import ply.yacc as yacc
from lexer import tokens

# Grammar rules

# PROGRAMA
def p_programa_1(p):
    '''
    programa_1 : PROGRAM VAR_CTE_ID SEMI_COLON programa_2 bloque_1
    '''

def p_programa_2(p):
    '''
    programa_2 : vars_1
               | empty
    '''

# VARS
def p_vars_1(p):
    '''
    vars_1 : VAR vars_2
    '''

def p_vars_2(p):
    '''
    vars_2 : vars_3 COLON tipo SEMI_COLON vars_4
    '''

def p_vars_3(p):
    '''
    vars_3 : VAR_CTE_ID vars_5
    '''

def p_vars_4(p):
    '''
    vars_4 : vars_2
           | empty
    '''

def p_vars_5(p):
    '''
    vars_5 : COMMA vars_3
           | empty
    '''

# TIPO
def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
    '''

# BLOQUE
def p_bloque_1(p):
    '''
    bloque_1 : LEFT_KEY bloque_2 RIGHT_KEY
    '''

def p_bloque_2(p):
    '''
    bloque_2 : estatuto bloque_2
             | empty
    '''

# ESTATUTO
def p_estatuto(p):
    '''
    estatuto : asignacion
             | condicion_1
             | escritura_1
    '''

# ASIGNACION
def p_asignacion(p):
    '''
    asignacion : VAR_CTE_ID EQUAL expresion_1 SEMI_COLON
    '''

# ESCRITURA
def p_escritura_1(p):
    '''
    escritura_1 : PRINT LEFT_PAR escritura_2 RIGHT_PAR SEMI_COLON
    '''

def p_escritura_2(p):
    '''
    escritura_2 : expresion_1 escritura_3
                | VAR_CTE_STRING escritura_3
    '''

def p_escritura_3(p):
    '''
    escritura_3 : COMMA escritura_2
                | empty
    '''

# EXPRESION
def p_expresion_1(p):
    '''
    expresion_1 : exp_1 expresion_2
    '''

def p_expresion_2(p):
    '''
    expresion_2 : GREATER_THAN exp_1
                | LESS_THAN exp_1
                | NOT_EQUAL exp_1
                | empty
    '''

# EXP
def p_exp_1(p):
    '''
    exp_1 : termino_1 exp_2
    '''

def p_exp_2(p):
    '''
    exp_2 : PLUS exp_1
          | MINUS exp_1
          | empty
    '''

# TERMINO
def p_termino_1(p):
    '''
    termino_1 : factor_1 termino_2
    '''

def p_termino_2(p):
    '''
    termino_2 : TIMES termino_1
              | DIV termino_1
              | empty
    '''

# FACTOR
def p_factor_1(p):
    '''
    factor_1 : LEFT_PAR expresion_1 RIGHT_PAR
             | factor_2 var_cte
    '''

def p_factor_2(p):
    '''
    factor_2 : PLUS
             | MINUS
             | empty
    '''

# CONDICION
def p_condicion_1(p):
    '''
    condicion_1 : IF LEFT_PAR expresion_1 RIGHT_PAR bloque_1 condicion_2 SEMI_COLON
    '''

def p_condicion_2(p):
    '''
    condicion_2 : ELSE bloque_1
                | empty
    '''

# VAR_CTE
def p_var_cte(p):
    '''
    var_cte : VAR_CTE_ID
            | VAR_CTE_INT
            | VAR_CTE_FLOAT
    '''

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