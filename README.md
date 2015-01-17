Compiler-Project
================

Course Project for the Principles of Compiler

[Python Lex Yacc手册](http://www.pchou.info/open-source/2014/01/18/52da47204d4cb.html)

## Usage

```bash
$ python md2html.py -run <input_file>
$ python md2html.py -run ./data/Lv0.md     # example
```

## Task

#### Task 1 ([Hu Yonghao](https://github.com/ForeverHYH))

- h1 ~ h6
- devider
- italic
- strong

#### Task 2 ([Wang Xiaoying](https://github.com/wangxiaoying))

- inline code
- link
- autolink
- unorderd list
- ordered list

#### Task 3 ([Hu Shengtuo](https://github.com/h1994st))

- image
- quote
- nesting list
- code block

## Design

article := article block | ε

block := p
       | h1
       | h2
       | h3
       | h4
       | h5
       | h6
       | blockquote
       | ol
       | ul
       | pre code
       | hr

inline := inline strong
       | inline inlinecode
       | inline italic
       | inline autolink
       | inline link
       | inline plain
       | inline image
       | ε

h1 := # inline
h2 := ## inline
h3 := ### inline
h4 := #### inline
h5 := ##### inline
h6 := ###### inline

blockquote := > inline | > inline \n{2,} blockquote

ul := li | li \n
