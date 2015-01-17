#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-16 15:09:02
# @Author  : Tom Hu (webmaster@h1994st.com)
# @Link    : http://h1994st.com
# @Version : 3.1

import os
import sys
import ply.yacc as yacc
import mklex
tokens = mklex.tokens

########
# Yacc #
########
precedence = (
    ('')
    )
names = {}

listStack = []

def p_body(p):
    'body : article'
    print '<html><head><title>Markdown To Html</title></head><body>' + p[1] + '</body></html>'

def p_article(p):
    '''article : block
               | block article'''
    if (len(p)==2):
        p[0] = p[1] 
    elif (len(p) == 3):
        p[0] = str(p[1]) + str(p[2])

# Block
def p_block(p):
    '''block : heading
             | blockquote
             | blockcode
             | paragraph
             | DIVIDER
             | block CR
             | block CR2'''
    p[0] = p[1]

def p_heading(p):
    '''heading : H1 inline
               | H2 inline
               | H3 inline
               | H4 inline
               | H5 inline
               | H6 inline'''
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

def p_blockquote(p):
    '''blockquote : quotelines'''
    p[0] = '<blockquote>%s</blockquote>' % p[1]

def p_quotelines(p):
    '''quotelines : quoteline
                  | quoteline quotelines
                  | quoteline CR2 quotelines'''
    if len(p) == 2:
        p[0] = p[1]
        if p[0] != '':
            p[0] = '<p>%s</p>' % p[0]
    elif len(p) == 3:
        p[0] = str(p[1]) + str(p[2])
    elif len(p) == 4:
        p[0] = ('<p>%s</p>' % p[1]) + r[3]

def p_quoteline(p):
    '''quoteline : BLOCKQUOTE inline
                 | BLOCKQUOTE CR
                 | BLOCKQUOTE CR2'''
    if p[2].find('\n') != -1:
        p[0] = ''
    else:
        p[0] = p[2]

def p_blockcode(p):
    'blockcode : BLOCKCODEOPEN WORD BLOCKCODECLOSE'
    p[0] = '<pre><code>%s</code></pre>' % str(p[2])

def p_paragraph(p):
    'paragraph : inline CR2'
    p[0] = '<p>%s</p>' % p[1]

# def p_list(p):
#     '''list : unorderedlist
#             | orderedlist'''
#     p[0] = p[1]

# def p_unorderedlist(p):
    

# def p_orderedlist(p):
#     d

# def p_listitems(p):
#     '''listitems : listitem
#                  | listitem listitems'''

# def p_listitem(p):
#     '''listitem : LI inline
#                 | LI inline list'''
#     if p[1] == ''

# Inline
def p_inline(p):
    '''inline : plain
              | plain inline
              | strongtext
              | strongtext inline
              | emphasizetext
              | emphasizetext inline
              | code 
              | code inline
              | image
              | image inline
              | link
              | link inline
              | autolink
              | autolink inline
              | inline CR
              | '''
    if len(p) == 3:
        if p[2] == '\n':
            p[2] = ' '
        p[0] = str(p[1]) + str(p[2])
    else:
        p[0] = str(p[1])

def p_plain(p):
    '''plain : WORD
             | WORD SPACE plain'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = str(p[1]) + str(p[2]) + str(p[3])

def p_strongtext(p):
    'strongtext : STRONGOPEN inline STRONGCLOSE'
    p[0] = '<strong>%s</strong>' % p[2]

def p_emphasizetext(p):
    'emphasizetext : EMPHASIZEOPEN inline EMPHASIZECLOSE'
    p[0] = '<i>%s</i>' % p[2]

def p_code(p):
    'code : INLINECODEOPEN inline INLINECODECLOSE'
    p[0] = '<code>%s</code>' % p[2]

def p_image(p):
    'image : SURPRISE L_RB plain R_RB L_SB URL R_RB'
    p[0] = '<img src="%s" alt="%s" />' % (p[6], p[3])

def p_link(p):
    'link : L_RB inline R_RB L_SB URL R_RB'
    p[0] = '<a href="%s">%s</a>' % (p[5], p[2])

def p_autolink(p):
    'autolink : L_AB URL R_AB'
    p[0] = '<a href="%s">%s</a>' % (p[2], p[2])

def p_error(p):
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")



