#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-16 15:12:00
# @Author  : Tom Hu (webmaster@h1994st.com)
# @Link    : http://h1994st.com
# @Version : 3.1

import os
import sys
import ply.lex as lex
import ply.yacc as yacc

from mklex import *
from mkyacc import *

yacc.yacc()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage : main.py <filename>"
        raise SystemExit
    elif len(sys.argv) == 2:
        inputPath = os.path.realpath(sys.argv[1])
        output = yacc.parse(open(inputPath, 'r').read())

        filename = inputPath.split('/')[-1]
        outputPath = os.path.join(os.getcwd(), 'output_' + filename[:-3] + '.html')
        outputFile = open(outputPath, 'w')
        outputFile.write(output)
        outputFile.close()
