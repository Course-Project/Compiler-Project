# Test04

## Blockcode with `highlight.js`

```c
#include <stdio.h>

int main() {
    printf("test");
}
```

```python
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

    if len(sys.argv) == 2:
        yacc.parse(open(sys.argv[1]).read())
```

## Autoemail link

<h1994st@gmail.com>

<h1994st@qq.com>

<webmaster@h1994st.com>



