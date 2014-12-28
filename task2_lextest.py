import sys
import ply.lex as lex

#Lex 

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
    'UNDERLINEOPEN','UNDERLINECLOSE',
    'CODE', 'POINT', 'PLUS',
    'L_AB', 'R_AB', 'L_SB', 'R_SB','L_RB', 'R_RB',
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
t_CODE = r'\`'
t_POINT = r'\.'
t_PLUS = r'\+'
t_L_AB = r'\<'
t_R_AB = r'\>'
t_L_SB = r'\['
t_R_SB = r'\]'
t_L_RB = r'\('
t_R_RB = r'\)'


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
    r'[a-zA-Z0-9,\'./:]+'
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

# Test it out
data = '''
# forrest gump

## OPENING

**hello**, **my name is forrest**, `forrest gump`. do you want chocolate, i could eat about a million and a half of these. my mama always said, life was like a box of __chocolates__. you never know what you are going to get.

## SHOES

these must be  **comfortable shoes**, i bet you cloud walk all day in _shoes_ like that and not feel a thing.i wish i have [shoes](http://www.taobao.com/) like that. 
	
my `mama` always said there's an awful lot you can tell about a person by their shoes.where they're gone, where they've *been*.

## REVIEWS

<http://www.github.com/guoylyy/>

* i like this film.

---
<http://www.github.com/guoylyy/>

1. i wish jenny can marry with gump early.

===

<http://www.github.com/guoylyy/>

+ i wish jenny can marry with gump early.

* * *

'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
