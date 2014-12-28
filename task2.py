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
    'UNDERLINEOPEN', 'UNDERLINECLOSE',
    'CODEOPEN', 'CODECLOSE', 'PLUS',
    'L_AB', 'R_AB', 'L_SB', 'R_SB','L_RB', 'R_RB',
    'URL', 'ORDERLIST', 'UNORDERLIST'
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

t_ANY_ignore = '\t'

def t_URL(t):
    r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    t.value = str(t.value)
    return t

def t_STAR(t):
    r'[ ]*\n+[ ]*(\*[ ]*){3,}'
    return t

def t_ORDERLIST(t):
    r'[ ]*\n+\d+\.[ ]'
    t.value = 'order'
    return t

def t_UNORDERLIST(t):
    r'[ ]*\n+(\*|\+)[ ]'
    t.value = 'unorder'
    return t

def t_PLUS(t):
    r'\+'
    t.value = str(t.value)
    return t

def t_L_AB(t):
    r'\<'
    t.value = str(t.value)
    return t

def t_R_AB(t):
    r'\>'
    t.value = str(t.value)
    return t
def t_L_SB(t):
    r'\['
    t.value = str(t.value)
    return t
def t_R_SB(t):
    r'\]'
    t.value = str(t.value)
    return t
def t_L_RB(t):
    r'\('
    t.value = str(t.value)
    return t
def t_R_RB(t):
    r'\)'
    t.value = str(t.value)
    return t

def t_CODEOPEN(t):
    r'\`'
    t.lexer.push_state('close')
    t.value = str(t.value)
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

def t_close_CODECLOSE(t):
    r'\`'
    t.lexer.pop_state()
    t.value = str(t.value)
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
    r'[a-zA-Z0-9,\':\.\/]'
    t.value = str(t.value)
    return t

def t_ANY_CR(t):
    r'[ ]*\n+'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.begin('INITIAL')
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
    ('')
    )
names = {}

def p_body(p):
    'body : statement'
    print '<html><head><title>MarkdownToHtml</title></head><body>' + p[1] + '</body></html>'

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
        # print p[1]
        # for i in range(1,str(p[1]).count("\n")): 
        #     p[0] = p[0] + '<br>'
    elif (len(p) == 3): 
        p[0] = p[1]

        # for i in range(1,str(p[2]).count("\n")):
        #     p[0] = p[0] + '<br>'

# def p_state_ulol(p):
#     '''statement : list
#                  | statement list'''
#     if len(p)==2:


def p_state_devide(p):
    '''statement : divider
                 | statement divider'''
    if (len(p)==2):
        p[0] = '<hr/>'
    elif (len(p) == 3):
        p[0] = str(p[1]) + '<hr/>'

def p_exo_list(p):
    '''expression : list'''
    p[0] = p[1]

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
 
def p_list_ol(p):
    '''list : olistitem
            | olistitem list'''
    if len(p) == 2:
        p[0] = '<ol>' + str(p[1]) + '</ol>'
    else:
        p[0] = '<ol>' + str(p[1]) + str(p[2])[4:-5] + '</ol>'

def p_list_ul(p):
    '''list : ulistitem
            | ulistitem list'''
    if len(p) == 2:
        p[0] = '<ul>' + str(p[1]) + '</ul>'
    else:
        p[0] = '<ul>' + str(p[1]) + str(p[2])[4:-5] + '</ul>'


def p_olistitem_li(p):
    '''olistitem : ORDERLIST
                 | ORDERLIST factor'''
    if len(p) == 2:
        p[0] = '<li></li>'
    else:
        p[0] = '<li>' + str(p[2]) + '</li>'

def p_ulistitem_li(p):
    '''ulistitem : UNORDERLIST
                 | UNORDERLIST factor'''
    if len(p) == 2:
        p[0] = '<li></li>'
    else:
        p[0] = '<li>' + str(p[2]) + '</li>'


def p_factor_text(p):
    '''factor : str
              | factor SPACE factor
              | factor factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + p[2] + p[3]
    elif len(p) == 3:
        p[0] = p[1] + p[2]

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

def p_factor_code(p):
    '''factor : CODEOPEN factor CODECLOSE
              | CODEOPEN factor CODECLOSE str'''
    if len(p) == 4:
        p[0] = '<code>' + str(p[2]) + '</code>'
    else:
        p[0] = '<code>' + str(p[2]) + '</code>' + str(p[4])

def p_factor_simplelink(p):
    '''factor : L_AB URL R_AB
              | L_AB URL R_AB str'''
    if len(p) == 4:
        p[0] = '<a href="' + str(p[2]) +'">' + str(p[2]) + '</a>'
    else:
        p[0] = '<a href="' + str(p[2]) +'">' + str(p[2]) + '</a>' + str(p[4])

def p_factor_link(p):
    '''factor : L_SB factor R_SB L_RB URL R_RB
              | L_SB factor R_SB L_RB URL R_RB str'''
    if len(p) == 7:
        p[0] = '<a href="' + str(p[5]) +'">' + str(p[2]) + '</a>'
    else:
        p[0] = '<a href="' + str(p[5]) +'">' + str(p[2]) + '</a>' + str(p[7])

def p_factor_symbol(p):
    '''factor : R_AB
              | R_AB str
              | L_AB
              | L_AB str
              | R_SB
              | R_SB str
              | L_SB
              | L_SB str
              | R_RB
              | R_RB str
              | L_RB
              | L_RB str'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]


def p_str_char(p):
    '''str : CHAR
           | CHAR str
           | URL
           | URL str
           | CODEOPEN
           | CODEOPEN str
           | PLUS 
           | PLUS str
           | STAROPEN
           | STAROPEN str'''
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