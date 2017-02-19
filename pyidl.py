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

import ply.yacc as yacc

def p_idl(p):
   '''idl : statement_include
          | statement_declaration
          | statement_enum_declaration'''

def p_enum_item(p):
    'enum_item : NAME \'=\' NUMBER' 

def p_enum_item_list(p):
    'enum_item_list : enum_item enum_item_list_tail'

def p_enum_item_list_tail(p):
    '''enum_item_list_tail : \',\' enum_item_list
                           | \',\'
                           | '''

def p_statement_enum_declaration(p):
    'statement_enum_declaration : ENUM NAME \'{\' enum_item_list \'}\''

def p_statement_include(p):
    'statement_include : INCLUDE STRINGLITERAL'
    print (p[1:])

def p_constexpr(p):
    '''constexpr : NUMBER
                 | STRINGLITERAL'''

def p_statement_declaration(p):
    'statement_declaration : CONST NAME NAME \'=\' constexpr \';\''
    print (p[1:])

def p_error(p):
    print("Syntax error")

parser = yacc.yacc()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
