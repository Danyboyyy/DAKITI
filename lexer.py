import ply.lex as lex

# Tokens
tokens = ('PROGRAM', 'INT', 'FLOAT', 'IF', 'ELSE', 'PRINT', 'VAR',
          'VAR_CTE_ID', 'VAR_CTE_INT', 'VAR_CTE_FLOAT', 'VAR_CTE_STRING',
          'PLUS', 'MINUS', 'TIMES', 'DIV', 'LESS_THAN', 'GREATER_THAN',
          'EQUAL', 'NOT_EQUAL', 'LEFT_PAR', 'RIGHT_PAR', 'LEFT_KEY',
          'RIGHT_KEY', 'COMMA', 'COLON', 'SEMI_COLON')

# Ignored characters
t_ignore = ' \t'

# Reserved words 
reserved = {
    'program': 'PROGRAM',
    'int': 'INT',
    'float': 'FLOAT',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT',
    'var': 'VAR'
}

# Regular expressions
t_VAR_CTE_STRING = r'"(.*?)"'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIV = r'\/'
t_LESS_THAN = r'\<'
t_GREATER_THAN = r'\>'
t_EQUAL = r'\='
t_NOT_EQUAL = r'\<\>'
t_LEFT_PAR = r'\('
t_RIGHT_PAR = r'\)'
t_LEFT_KEY = r'\{'
t_RIGHT_KEY = r'\}'
t_COMMA = r'\,'
t_COLON = r'\:'
t_SEMI_COLON = r'\;'

# Function regular expressions
def t_VAR_CTE_ID(t):
    r'[A-za-z]([A-za-z]|[0-9])*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t
    
def t_VAR_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_VAR_CTE_FLOAT(t):
    r'([0-9]*[.])?[0-9]+'
    t.value = float(t.value)
    return t

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lex.lex()