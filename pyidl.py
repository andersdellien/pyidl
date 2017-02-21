import sys
import ply.lex as lex
import os

class_name = os.path.splitext(sys.argv[1])[0]

states = (
   ('comment','exclusive'),
)

reserved = {
    'const' : 'CONST',
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

def t_comment_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_comment_error(t):
    print("Illegal character in comment '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

import ply.yacc as yacc

def p_idl(p):
   'idl : statement_list'

def p_statement_list(p):
   '''statement_list : statement statement_list
                     | '''
def p_statement(p):
   '''statement : statement_include
                | statement_declaration
                | statement_enum_declaration
                | statement_struct_declaration'''

def p_qualified_name(p):
    '''qualified_name : NAME \'.\' qualified_name
                      | NAME'''
    p[0] = p[1]

def p_struct_name(p):
    'struct_name : NAME'
    p[0] = p[1]

def p_struct_declaration(p):
    'statement_struct_declaration : STRUCT struct_name \'{\' struct_item_list \'}\''
    struct_name = p[2].replace(class_name, "").replace("Path", "")
    if (struct_name != ""):
        print ('struct %s' % (struct_name))
        print ('{')
        for s in p[4]:
            print ('  %s %s;' % (s[0], s[1]))
        print ('}')
    p[0] = p[2]

def p_struct_item_list(p):
    '''struct_item_list : struct_item struct_item_list
                        | '''
    if (len(p) > 1):
        if (p[2] == None):
            p[0] = [p[1]]
        else:
            p[2].append(p[1])
            p[0] = list(p[2])

def p_struct_item(p):
    'struct_item : NUMBER \':\' OPTIONAL type qualified_name opt_assignment struct_item_terminator'
    p[0] = (p[4], p[5])

def p_struct_item_terminator(p):
    '''struct_item_terminator : \',\'
                              | \';\'
                              | '''

def p_opt_assignment(p):
    '''opt_assignment : \'=\' qualified_name
                      | \'=\' NUMBER
                      | '''

def p_type(p):
    '''type : qualified_name
            | LIST \'<\' NAME \'>\' '''
    p[0] = p[1]

def p_enum_item(p):
    'enum_item : NAME opt_assignment'

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

def p_constexpr(p):
    '''constexpr : NUMBER
                 | STRINGLITERAL'''

def p_statement_declaration(p):
    'statement_declaration : CONST NAME NAME \'=\' constexpr opt_semicolon'
    function_name = p[3].replace(class_name, "").replace("Path", "")
    if (function_name == "OutputRoleConfigureCommand"):
        print ("void %s(OutputRoleConfigure outputRoleConfigure);" % function_name)
    elif (function_name != "Prefix" and function_name != "Name"):
        print ("void %s();" % function_name)

def p_opt_semicolon(p):
    '''opt_semicolon : \';\'
                     | '''

def p_error(p):
    print("Syntax error")

parser = yacc.yacc()
parser.parse(open(sys.argv[1], 'r').read())
