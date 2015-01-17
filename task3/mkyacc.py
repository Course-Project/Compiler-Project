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
    print '<!DOCTYPE html><html><head><link rel="stylesheet" href="./GitHub2.css"><link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css"><title>Markdown To Html</title></head><body>' + p[1] + '</body><script src="http://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/highlight.min.js"></script><script>hljs.initHighlightingOnLoad();</script></html>'

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
             | paragraph
             | divider
             | listall
             | blockcode
             | blockquote
             | block CR
             | block CR2'''
    p[0] = p[1]

def p_divider(p):
    'divider : DIVIDER'
    p[0] = '<hr>'

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

def p_paragraph(p):
    'paragraph : inline CR2'
    p[0] = '<p>%s</p>' % p[1]

def p_list(p):
    '''list : li
            | li list'''
    cat = listStack[-1][1]
    if len(p) == 2:
        p[0] = '<%s>%s</%s>' % (cat, p[1], cat)
    else:
        if len(listStack) >= 2:
            if listStack[-1][0] != listStack[-2][0]:
                p[0] = '<%s>%s</%s>' % (cat, str(p[1]) + str(p[2]), cat)
            else:
                p[0] = '<%s>%s</%s>' % (cat, str(p[1]) + str(p[2])[4:-5], cat)
            listStack.pop()

def p_li(p):
    '''li : OLI inline CR
          | OLI inline CR2
          | ULI inline CR
          | ULI inline CR2'''
    p[0] = '<li>%s</li>' % p[2]
    listStack.append((p[1].count('\t'), p[1][p[1].rfind('\t') + 1:]))

def p_listall(p):
    'listall : list'
    p[0] = p[1]
    listStack = []

def p_blockcode(p):
    'blockcode : BLOCKCODEOPEN WORD BLOCKCODECLOSE'
    codeStyle = filter(lambda x: x != '\n', p[1][3:]) # remove Enter
    p[0] = '<pre><code class="%s">%s</code></pre>' % (codeStyle, str(p[2]))

def p_blockquote(p):
    '''blockquote : quoteline
                  | quoteline blockquote'''
    if len(p) == 2:
        p[0] = '<blockquote>%s</blockquote>' % p[1]
    elif len(p) == 3:
        if str(p[2])[12:-13] == '':
            p[0] = '<blockquote><p>%s</p></blockquote>' % str(p[1])
        else:
            p[0] = '<blockquote>%s</blockquote>' % (str(p[1]) + str(p[2])[12:-13])

def p_quoteline(p):
    '''quoteline : quotestart CR
                 | quotestart CR2
                 | quotestart inline CR
                 | quotestart inline CR2'''
    if len(p) == 3:
        p[0] = ''
    else:
        if p[3].count('\n') < 2:
            p[0] = p[2]
        else:
            p[0] = '<p>%s</p>' % p[2]

def p_quotestart(p):
    '''quotestart : BLOCKQUOTE
                  | BLOCKQUOTE SPACE'''
    p[0] = p[1]

# Inline
def p_strongtext(p):
    'strongtext : STRONGOPEN inline STRONGCLOSE'
    p[0] = '<strong>%s</strong>' % p[2]

def p_emphasizetext(p):
    'emphasizetext : EMPHASIZEOPEN inline EMPHASIZECLOSE'
    p[0] = '<i>%s</i>' % p[2]

def p_inlinecode(p):
    'inlinecode : INLINECODEOPEN inline INLINECODECLOSE'
    p[0] = '<code>%s</code>' % p[2]

def p_image(p):
    'image : SURPRISE L_SB WORD R_SB L_RB URL R_RB'
    p[0] = '<img src="%s" alt="%s" />' % (p[6], p[3])

def p_link(p):
    'link : L_SB inline R_SB L_RB URL R_RB'
    p[0] = '<a href="%s">%s</a>' % (p[5], p[2])

def p_autolink(p):
    'autolink : L_AB URL R_AB'
    p[0] = '<a href="%s">%s</a>' % (p[2], p[2])

def p_one(p):
    '''one : WORD
           | strongtext
           | emphasizetext
           | inlinecode
           | image
           | link
           | autolink'''
    p[0] = p[1]

def p_inline(p):
    '''inline : one
              | one inline
              | one SPACE inline'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = str(p[1]) + str(p[2])
    elif len(p) == 4:
        p[0] = str(p[1]) + ' ' + str(p[3])

def p_error(p):
    print p
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")



