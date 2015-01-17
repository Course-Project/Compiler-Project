# Test04

## Heading

# h1
## h2
### h3
#### h4
##### h5
###### h6

## Divider

---

= =    =

    *          **

## Strong

__strong__

**strong**

## Italic

_italic_

*italic*

## Inline code

`Inline code, look at here`

## Blockcode

```nohighlight
#include <stdio.h>

int main() {
    printf("test");
}
```

C with `highlight.js`

```c
#include <stdio.h>

int main() {
    printf("test");
}
```

```nohighlight
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

Python with `highlight.js`

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

## Link

[h1994st](http://h1994st.com)

## Autolink

<http://h1994st.com>

<https://highlightjs.org/>

## List

* list1
* list1
* list1

- list2
- list2
- list2

* list3
- list3
- list3

1. list4
2. list4
5. list4

## Nested list

* list1
	* list11
	* list11
		1. list111
		2. list111

## Image

![Test](http://a1.att.hudong.com/24/64/01300001178110130097643491565.jpg)

## Blockquote

> test for blockquote
>
> test for blockquote

## Autoemail link

<h1994st@gmail.com>

<h1994st@qq.com>

<webmaster@h1994st.com>



