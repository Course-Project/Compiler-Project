#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-21 11:02:37
# @Author  : Tom Hu (webmaster@h1994st.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import sys
import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN
#
# Lex
# 
tokens = (
    'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
    'CR',
    'WORD', 'SPACE'
    )
# tokens = (
#     'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
#     'SPACE', 'CR',
#     'CHAR',
#     'STAR', 'UNDERLINE', 'CODE', 'MINUS', 'PLUS', 'L_AB', 'R_AB', 'L_RB', 'R_RB', 'L_B', 'R_B', 'SURPRISE'
#     )

# Tokens
t_H1 = r'\#[ ]*'
t_H2 = r'\#\#[ ]*'
t_H3 = r'\#\#\#[ ]*'
t_H4 = r'\#\#\#\#[ ]*'
t_H5 = r'\#\#\#\#\#[ ]*'
t_H6 = r'\#\#\#\#\#\#[ ]*'
t_SPACE = r'[ ]+'


def t_WORD(t):
    r'\w+'
    t.value = str(t.value)
    return t

def t_CR(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
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

def p_state(p):
    '''statement : expression
                 | statement CR expression'''
    if (len(p)==2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = str(p[1]) + str(p[3])

def p_exp_cr(p):
    '''expression : H1 factor
                  | H2 factor
                  | H3 factor
                  | H4 factor
                  | H5 factor
                  | H6 factor'''
    p[1] = filter(lambda x: x != ' ', p[1]) # remove space
    switch = {
        '#': '<h1>' + str(p[2]) + '</h1>',
        '##': '<h2>' + str(p[2]) + '</h2>',
        '###': '<h3>' + str(p[2]) + '</h3>',
        '####': '<h4>' + str(p[2]) + '</h4>',
        '#####': '<h5>' + str(p[2]) + '</h5>',
        '######': '<h6>' + str(p[2]) + '</h6>'
    }
    p[0] = switch[p[1]];

def p_factor_text(p):
    '''factor : WORD
              | WORD SPACE factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + p[2] + p[3]

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
