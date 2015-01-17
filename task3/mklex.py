#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-16 13:16:18
# @Author  : Tom Hu (webmaster@h1994st.com)
# @Link    : http://h1994st.com
# @Version : 3.1

import os
import sys
import ply.lex as lex
from ply.lex import TOKEN

#######
# Lex #
#######
states = (
    ('blockcode','exclusive'),
    ('strong','exclusive'),
    ('emphasize','exclusive'),
    ('inlinecode','exclusive')
    )

tokens = (
    'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
    'DIVIDER',
    'SPACE', 'CR', 'CR2', 'TAB',
    'URL', 'EMAIL',
    'STRONGOPEN', 'STRONGCLOSE',
    'EMPHASIZEOPEN', 'EMPHASIZECLOSE',
    'INLINECODEOPEN', 'INLINECODECLOSE',
    'SURPRISE',
    'BLOCKQUOTE',
    'L_SB', 'R_SB',
    'L_RB', 'R_RB',
    'L_AB', 'R_AB',
    'ULI', 'OLI',
    'WORD',
    'BLOCKCODEOPEN', 'BLOCKCODECLOSE'
    )

char = r'([a-zA-Z0-9,\'":\.\/])'
star = r'(\*)'
underline = r'(\_)'
minus = r'(\-)'
plus = r'(\+)'
numberIndex = r'([1-9][0-9]*\.)'
blockcode = r'(\`\`\`)'
tab = r'(\t)'

word = char + r'+'
code = r'[0-9a-zA-Z\*\&\^\%\$\#\@\!\~\-\=\+_\[\]\{\}\;\:\'\"\/\.\,\<\>\|\\\s\(\)]+'

doubleStar = star + r'{2}'
doubleUnderline = underline + r'{2}'

lineDivider = r'([ ]*(\-[ ]*){3,}\n)'
equalDivider = r'([ ]*(\=[ ]*){3,}\n)'
starDivider = r'([ ]*(\*[ ]*){3,}\n)'
divider = lineDivider + r'|' + equalDivider + r'|' + starDivider

blockcodeopen = blockcode + r'(' + word + r')*\n'
blockcodeclose = blockcode + r'(\n)?'

strong = doubleStar + r'|' + doubleUnderline
emphasize = star + r'|' + underline

uli = tab + r'*' + r'(' + star + r'|' + plus + r'|' + minus + r')[ ]+'
oli = numberIndex + r'[ ]+'

# Token rules
t_H1 = r'\#[ ]*'
t_H2 = r'\#\#[ ]*'
t_H3 = r'\#\#\#[ ]*'
t_H4 = r'\#\#\#\#[ ]*'
t_H5 = r'\#\#\#\#\#[ ]*'
t_H6 = r'\#\#\#\#\#\#[ ]*'
t_ANY_SPACE = r'[ ]+'

t_SURPRISE = r'\!'
t_L_SB = r'\['
t_R_SB = r'\]'
t_L_RB = r'\('
t_R_RB = r'\)'

# Ignore rules
t_ignore = ''
t_blockcode_ignore = ''
t_strong_ignore = ''
t_emphasize_ignore = ''
t_inlinecode_ignore = ''

def t_L_AB(t):
    r'\<'
    t.lexer.isLeftAB = True
    return t

def t_R_AB(t):
    r'\>'
    if not t.lexer.isLeftAB:
        t.type = 'BLOCKQUOTE'
    t.lexer.isLeftAB = False
    return t

@TOKEN(divider)
def t_DIVIDER(t):
    t.lexer.lineno += t.value.count("\n")
    return t

@TOKEN(uli)
def t_ULI(t):
    t.value = t.value[:t.value.rfind('\t') + 1] + 'ul'
    return t

@TOKEN(oli)
def t_OLI(t):
    t.value = t.value[:t.value.rfind('\t') + 1] + 'ol'
    return t

@TOKEN(tab)
def t_TAB(t):
    pass
    # return t

def t_URL(t):
    r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    t.value = str(t.value)
    return t

def t_EMAIL(t):
    r'(\w)+(\.\w+)*@(\w)+((\.\w+)+)'
    t.value = str(t.value)
    return t

@TOKEN(word)
def t_strong_emphasize_inlinecode_INITIAL_WORD(t):
    # print '(lineno: %d, lexpos: %d, type: %s, value: %s)' % (t.lineno, t.lexpos, t.type, t.value)
    return t

# Blockcode close
@TOKEN(blockcodeclose)
def t_blockcode_BLOCKCODECLOSE(t):
    t.lexer.lineno += t.value.count("\n")
    t.lexer.pop_state()
    return t

@TOKEN(code)
def t_blockcode_WORD(t):
    t.lexer.lineno += t.value.count("\n")
    return t

# Blockcode open
@TOKEN(blockcodeopen)
def t_BLOCKCODEOPEN(t):
    t.lexer.lineno += t.value.count("\n")
    t.lexer.push_state('blockcode')
    return t

# Inlinecode close
def t_inlinecode_INLINECODE(t):
    r'\`'
    if len(t.lexer.symbolStack) > 0 and t.lexer.symbolStack[-1] == t.value:
        t.type = 'INLINECODECLOSE'
        t.lexer.symbolStack.pop()
        t.lexer.pop_state()
        return t

# Emphasize close
@TOKEN(emphasize)
def t_emphasize_EMPHASIZE(t):
    if len(t.lexer.symbolStack) > 0 and t.lexer.symbolStack[-1] == t.value:
        t.type = 'EMPHASIZECLOSE'
        t.lexer.symbolStack.pop()
        t.lexer.pop_state()
        return t

# Strong close
@TOKEN(strong)
def t_strong_STRONG(t):
    if len(t.lexer.symbolStack) > 0 and t.lexer.symbolStack[-1] == t.value:
        t.type = 'STRONGCLOSE'
        t.lexer.symbolStack.pop()
        t.lexer.pop_state()
        return t

# Strong open
@TOKEN(strong)
def t_emphasize_inlinecode_INITIAL_STRONG(t):
    t.type = 'STRONGOPEN'
    t.lexer.symbolStack.append(t.value)
    t.lexer.push_state('strong')
    return t

# Emphasize open
@TOKEN(emphasize)
def t_strong_inlinecode_INITIAL_EMPHASIZE(t):
    t.type = 'EMPHASIZEOPEN'
    t.lexer.symbolStack.append(t.value)
    t.lexer.push_state('emphasize')
    return t

# Inlinecode open
def t_strong_emphasize_INITIAL_INLINECODE(t):
    r'\`'
    t.type = 'INLINECODEOPEN'
    t.lexer.symbolStack.append(t.value)
    t.lexer.push_state('inlinecode')
    return t

def t_blockcode_CR(t):
    r'[ ]*\n+'
    if t.value.count('\n') >= 2:
        t.type = 'CR2'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_strong_emphasize_inlinecode_CR(t):
    r'[ ]*\n+'
    if t.value.count('\n') >= 2:
        t.type = 'CR2'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.begin('INITIAL') # Go back
    return t

def t_INITIAL_CR(t):
    r'[ ]*\n*\t*[ ]*\n+'
    if t.value.count('\n') >= 2:
        t.type = 'CR2'
    t.lexer.lineno += t.value.count("\n")
    return t

# Error handling
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
lexer.symbolStack = []
lexer.isLeftAB = False

def mklex_run(filename):
    lexer.input(open(filename).read())
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage : mklex.py <filename>"
        raise SystemExit 

    if len(sys.argv) == 2:
        print 'Filename: ' + sys.argv[1]
        mklex_run(sys.argv[1])
