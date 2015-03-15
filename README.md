Compiler-Project
================

Course Project for the Principles of Compiler

[Python Lex Yacc手册](http://www.pchou.info/open-source/2014/01/18/52da47204d4cb.html)

## 项目基本功能

本项目主要实现了 Markdown 的解析，能够正确解析的 Markdown 语法最要有：

* 标题 h1 到 h6
* 分隔符
* 斜体
* 粗体
* 代码段(inline code)
* 块级代码(block code)
* 超链接
* 自动链接
* 无序列表
* 有序列表
* 嵌套列表
* 图片
* 引用

## 扩展功能

同时，我们还实现了一些 markdown 本身不具备的功能：

### 代码着色

主要使用了 `highlight.js` 库，在解析块级代码的时候对代码进行着色处理

* 使用的库链接：<https://highlightjs.org/>

我们还实现了一些 test 文件中没有涵盖的语法：

### 自动邮件链接

和自动链接一样，将Email也做成了自动链接，这在Markdown标准中有，但是 test 文件中没有

如下格式：

```
<xxx@xxx.xxx>
```

将会被转为：

```
<a href="mailto:xxx@xxx.xxx">xxx@xxx.xxx</a>
```

## 测试文件

测试文件位于项目目录 `data` 下，共五个文件：

* test01.md - 包含标题、分隔符、斜体、粗体
* test02.md - 包含代码段、超链接、自动链接、列表
* test03.md - 包含图片、引用、嵌套列表、代码块
* test04.md - 包含代码块、代码高亮、自动链接、自动邮件链接
* test05.md - 包含所有实现的功能

## 测试方法：

```bash
$ python main.py <filename>
```

将会输出一个名为`output_<filename>.html`的文件，浏览器打开即可

## 项目特别说明

`highlight.js` 库相关的文件需要网络，务必联网测试

## 小组成员贡献说明

### [胡圣托](https://github.com/h1994st) 1252960（组长)

主要工作：test03.md所涵盖的语法

贡献率：33.3%

### [王笑盈](https://github.com/wangxiaoying) 1252885

主要工作：test02.md所涵盖的语法

贡献率：33.3%

### [胡永豪](https://github.com/ForeverHYH) 1253004

主要工作：test01.md所涵盖的语法

贡献率：33.3%
