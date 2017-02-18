import ply.lex as lex

states = (
   ('comment','exclusive'),
)

reserved = {
    'const' : 'CONST',
    'string' : 'STRING',
    'include' : 'INCLUDE',
    'enum' : 'ENUM',
    'struct' : 'STRUCT',
    'optional' : 'OPTIONAL',
    'list' : 'LIST'
}

literals = [ ':', ';', '=', '{', '}', ',', '<', '>', '.' ]

tokens = [
    'NAME','NUMBER', 'STRINGLITERAL', 'COMMENT'
    ] + list(reserved.values())

# Tokens

t_STRINGLITERAL = r'\".*\"'

def t_COMMENT(t):
    r'\/\/.*'
    pass

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(),'NAME')
    return t

def t_NUMBER(t):
    r'(0x)?\d+'
    if (t.value.count("0x") == 1):
        t.value = int(t.value, 16)
    else:
        t.value = int(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_comment_end(t):
    r'\*/'
    t.lexer.begin('INITIAL')

def t_comment_COMMENT(t):
    r'.'
    pass

def t_begin_comment(t):
    r'/\*'
    t.lexer.begin('comment')

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_comment_error(t):
    print("Illlegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

while True:
    try:
        s = raw_input('lex > ')   # use input() on Python 3
    except EOFError:
        break
    lexer.input(s)
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)
