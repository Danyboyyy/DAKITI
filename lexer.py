import ply.lex as lex

# Tokens
tokens = ('PROGRAM', 'FUNCTION', 'RETURN', 'INT', 'FLOAT', 'BOOL', 'STRING', 'IF', 'ELSE', 'PRINT', 'MAIN',
          'VARS', 'VAR_CTE_ID', 'VAR_CTE_INT', 'VAR_CTE_FLOAT', 'VAR_CTE_STRING', 'TRUE', 'FALSE',
          'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD', 'LESS_THAN', 'LESS_E_THAN', 'GREATER_THAN', 'GREATER_E_THAN',
          'EQUAL', 'EQUALS', 'NOT_EQUALS', 'AND', 'OR', 'LEFT_PAR', 'RIGHT_PAR', 'LEFT_KEY', 'RIGHT_KEY', 'LEFT_BRACK', 'RIGHT_BRACK',
          'WHILE', 'FOR', 'IN', 'RANGE', 'VOID', 'COMMA', 'SEMI_COLON', 'END',
          'PENUP', 'PENDOWN', 'FORWARD', 'BACKWARD', 'TURNLEFT', 'TURNRIGHT', 'DRAWCIRCLE', 'DRAWRECTANGLE', 'DRAWARC')

# Ignored characters
t_ignore = ' \t'

# Reserved words 
reserved = {
    'program': 'PROGRAM',
    'vars': 'VARS',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'main': 'MAIN',
    'void': 'VOID',
    'int': 'INT',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'string': 'STRING',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'range': 'RANGE',
    'print': 'PRINT',
    'end': 'END',
    'penUp': 'PENUP',
    'penDown': 'PENDOWN',
    'forward': 'FORWARD',
    'backward': 'BACKWARD',
    'turnRight': 'TURNRIGHT',
    'turnLeft': 'TURNLEFT',
    'drawCircle': 'DRAWCIRCLE',
    'drawRectangle': 'DRAWRECTANGLE',
    'drawArc': 'DRAWARC'
}

# Regular expressions
t_VAR_CTE_STRING = r'"(.*?)"'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'
t_EQUAL = r'\='
t_LESS_THAN = r'\<'
t_LESS_E_THAN = r'\<\='
t_GREATER_THAN = r'\>'
t_GREATER_E_THAN = r'\>\='
t_EQUALS = r'\=\='
t_NOT_EQUALS = r'\<\>'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_LEFT_PAR = r'\('
t_RIGHT_PAR = r'\)'
t_LEFT_KEY = r'\{'
t_RIGHT_KEY = r'\}'
t_LEFT_BRACK = r'\['
t_RIGHT_BRACK = r'\]'
t_COMMA = r'\,'
t_SEMI_COLON = r'\;'

# Function regular expressions
def t_VAR_CTE_ID(t):
    r'([a-z][a-zA-Z0-9]*)'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t
    
def t_VAR_CTE_FLOAT(t):
    r'[-]?[0-9]+([.][0-9]+)'
    t.value = float(t.value)
    return t

def t_VAR_CTE_INT(t):
    r'[-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lex.lex()