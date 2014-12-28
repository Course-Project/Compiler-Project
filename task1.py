#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-21 11:02:37
# @Author  : Hu Yonghao
# @Version : 1.0

import sys
import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN
#
# Lex
# 
states = (
    ('close','exclusive'),
    )

tokens = (
    'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
    'SPACE', 'CR',
    'CHAR',
    'STAR',  'MINUS' ,'EQUAL',
    'DOUBLESTAROPEN','DOUBLESTARCLOSE',
    'DOUBLEUNDERLINEOPEN','DOUBLEUNDERLINECLOSE',
    'STAROPEN','STARCLOSE',
    'UNDERLINEOPEN','UNDERLINECLOSE'
    )

# Tokens
t_H1 = r'\#[ ]*'
t_H2 = r'\#\#[ ]*'
t_H3 = r'\#\#\#[ ]*'
t_H4 = r'\#\#\#\#[ ]*'
t_H5 = r'\#\#\#\#\#[ ]*'
t_H6 = r'\#\#\#\#\#\#[ ]*'
t_ANY_SPACE = r'[ ]+'
t_MINUS = r'[ ]*(\-[ ]*){3,}'
t_EQUAL = r'[ ]*(\=[ ]*){3,}'

def t_STAR(t):
    r'[ ]*(\*[ ]*){3,}'
    return t

def t_DOUBLEUNDERLINEOPEN(t):
    r'\_\_'
    t.lexer.push_state('close')
    return t

def t_UNDERLINEOPEN(t):
    r'\_'
    t.lexer.push_state('close')
    return t

def t_DOUBLESTAROPEN(t):
    r'\*\*'
    t.lexer.push_state('close')
    return t

def t_STAROPEN(t):
    r'\*'
    t.lexer.push_state('close')
    return t

def t_close_DOUBLESTARCLOSE(t):
    r'\*\*'
    t.lexer.pop_state()
    return t

def t_close_STARCLOSE(t):
    r'\*'
    t.lexer.pop_state()
    return t

def t_close_DOUBLEUNDERLINECLOSE(t):
    r'\_\_'
    t.lexer.pop_state()
    return t

def t_close_UNDERLINECLOSE(t):
    r'\_'
    t.lexer.pop_state()
    return t

def t_ANY_CHAR(t):
    r'[a-zA-Z0-9,\'.]+'
    t.value = str(t.value)
    return t

def t_CR(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def mklex_run(filename):
    lexer.input(open(filename).read())
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok

#
# Yacc
#
precedence = (
    )
names = {}

def p_body(p):
    'body : statement'
    print '<html><head><title>Test</title></head><body>' + p[1] + '</body></html>'

def p_state_text(p):
    '''statement : expression
                 | statement expression'''
    if (len(p)==2):
        p[0] = p[1] 
    elif (len(p) == 3):
        p[0] = str(p[1]) + str(p[2])

def p_state_newline(p):
    '''statement : CR
                 | statement CR''' 

    if (len(p)==2):
        p[0] = p[0]
        # for i in range(1,str(p[1]).count("\n")): 
        #     p[0] = p[0] + '<br>'
    elif (len(p) == 3): 
        p[0] = p[1]
        # for i in range(1,str(p[2]).count("\n")):
        #     p[0] = p[0] + '<br>'

def p_state_devide(p):
    '''statement : divider
                 | statement divider'''
    if (len(p)==2):
        p[0] = '<hr/>'
    elif (len(p) == 3):
        p[0] = p[1] + '<hr/>'

def p_exp_cr(p):
    '''expression : H1 factor
                  | H2 factor
                  | H3 factor
                  | H4 factor
                  | H5 factor
                  | H6 factor
                  | factor'''
    if(len(p)==3):
        p[1] = filter(lambda x: x != ' ', p[1]) # remove space
        switch = {
            '#': '<h1>' + str(p[2]) + '</h1>',
            '##': '<h2>' + str(p[2]) + '</h2>',
            '###': '<h3>' + str(p[2]) + '</h3>',
            '####': '<h4>' + str(p[2]) + '</h4>',
            '#####': '<h5>' + str(p[2]) + '</h5>',
            '######': '<h6>' + str(p[2]) + '</h6>'
        }
        p[0] = switch[p[1]]
    elif (len(p) == 2):
        p[0] = '<p>' + str(p[1]) + '</p>' 
    

def p_factor_text(p):
    '''factor : str
              | factor SPACE factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + p[2] + p[3]

def p_factor_blod(p):
    '''factor : DOUBLESTAROPEN factor DOUBLESTARCLOSE
              | DOUBLEUNDERLINEOPEN factor DOUBLEUNDERLINECLOSE
              | DOUBLESTAROPEN factor DOUBLESTARCLOSE str
              | DOUBLEUNDERLINEOPEN factor DOUBLEUNDERLINECLOSE str'''  
    if len(p) == 4:
        p[0] = '<strong>' + str(p[2]) + '</strong>'
    else:
        p[0] = '<strong>' + str(p[2]) + '</strong>' + str(p[4])

def p_factor_italic(p):
    '''factor : STAROPEN factor STARCLOSE
              | UNDERLINEOPEN factor UNDERLINECLOSE
              | STAROPEN factor STARCLOSE str
              | UNDERLINEOPEN factor UNDERLINECLOSE str'''
    if len(p) == 4:
        p[0] = '<i>' + str(p[2]) + '</i>'
    else:
        p[0] = '<i>' + str(p[2]) + '</i>' + str(p[4])
    

def p_str_char(p):
    '''str : CHAR
            | CHAR str'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]

def p_divider(p):
    '''divider : EQUAL 
               | MINUS 
               | STAR '''
    if len(p) == 3:
        p[0] = p[1] + p[2]

def p_error(p):
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")

yacc.yacc()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "usage : mkrun.py [-lex|run] inputfilename"
        raise SystemExit 

    if len(sys.argv) == 3:
        if sys.argv[1] == '-lex':
            mklex_run(sys.argv[2])
        elif sys.argv[1] == '-run':
            yacc.parse(open(sys.argv[2]).read())
