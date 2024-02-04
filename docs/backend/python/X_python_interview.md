# Python面试总结

[[toc]]

## Python语言基础

### 1.列出几个常用Python标准库

`os`, `sys`, `string`, `logging`, `time`, `datetime`, `re`, `math`,`threading`

### 2.Python的内建数据类型有哪些

`str`字符串, `list`列表, `tuple`元素, `dict`字典, `set`集合, `int`整型, `float`浮点, `complex`复数(如:`1 + 2j`), `bool`布尔型。

### 3.简述`with`方法打开处理文件帮我我们做了什么

- `with`语句适用于对资源进行访问的场合，确保不管使用过程中是否发生异常都会执行必要的"清理"操作，释放资源，比如文件使用后自动关闭、线程中锁的自动获取和释放等。

- `with`语句即"上下文管理器"，在程序中用来表示代码执行过程中所处的前后环境。

上下文管理器：含有`__enter__`和`__exit__`方法的对象就是上下文管理器。

- `__enter__()`：在执行语句之前，首先执行该方法，通常返回一个实例对象，如果`with`语句有`as`目标，则将对象赋值给`as`目标。
- `__exit__()`：执行语句结束后，自动调用`__exit__()`方法，用户释放资源，若此方法返回布尔值`True`，程序会忽略异常。

使用环境：文件读写、线程锁的自动释放等。

### 4.Python的可变和不可变数据类型

- 可变: `list`列表, `dict`字典, `set`集合
- 不可变：`int`整型, `str`字符串, `tuple`元组


### 5.Python获取当前日期

- 使用`datetime`模块

```py
>>> from datetime import datetime
>>> datetime.now()
datetime.datetime(2020, 5, 16, 8, 26, 59, 83146)
>>> datetime.now().strftime('%Y%m%d_%H%M%S')
'20200516_082739'
```

- 使用`time`模块

```py
>>> import time
>>> time.strftime('%Y%m%d_%H%M%S', time.localtime())
'20200516_083042'
```

### 6.谈谈对Python的了解和其他语言的区别

- python是典型的动态类型强类型语言，强类型语言, 不需要隐式转换。

- 解释性，解释型语言使用解释器将源码逐行解释成机器码并立即执行，不会进行整体性的编译和链接处理，相当于把编译语言中的编译和解释混合到一起同时完成。

- 简洁优雅，面向对象，跨平台。
- Python是动态类型语言，而Java是静态类型语言。

### 7.说说你知道的Python3和Python2之间的区别

- 输出：`print`在python2中是一个输出语句，print后面可以带括号也可以不带；在python3中是一个函数，需要带括号。
- 用户输入：`input`在python2中，用户需要明确自己输入的字符类型，是字符串还是数字或者是布尔型，`raw_input`在python2中用户输入都被当前字符串；在python3中将原来的`input`删除了，然后将`raw_input`改成`input`函数,输出都是字符串类型，自己需要进行类型转换。
- 除法：python3中`/`表示真除，`//`表示取整；python2中`/`带上小数点表示真除，`//`表示取整。
- `xrange`迭代器：python2中可以使用`xrange`或`range`返回迭代器，python3中没有`xrange`，只有`range`。
- 字符串存储：python2以二进制存储，python3以unicode字符串存储。
- 异常捕获不一样，python2中`try except Exception,e:`， python3中`try except Exception as e:`。


### 8.了解`Python`之禅吗

```py
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!

优美胜于丑陋（Python 以编写优美的代码为目标）
明了胜于晦涩（优美的代码应当是明了的，命名规范，风格相似）
简洁胜于复杂（优美的代码应当是简洁的，不要有复杂的内部实现）
复杂胜于凌乱（如果复杂不可避免，那代码间也不能有难懂的关系，要保持接口简洁）
扁平胜于嵌套（优美的代码应当是扁平的，不能有太多的嵌套）
间隔胜于紧凑（优美的代码有适当的间隔，不要奢望一行代码解决问题）
可读性很重要（优美的代码是可读的）
即便假借特例的实用性之名，也不可违背这些规则（这些规则至高无上）
不要包容所有错误，除非你确定需要这样做（精准地捕获异常，不写 except:pass 风格的代码）
当存在多种可能，不要尝试去猜测
而是尽量找一种，最好是唯一一种明显的解决方案（如果不确定，就用穷举法）
虽然这并不容易，因为你不是 Python 之父（这里的 Dutch 是指 Guido ）
做也许好过不做，但不假思索就动手还不如不做（动手之前要细思量）
如果你无法向人描述你的方案，那肯定不是一个好方案；反之亦然（方案测评标准）
命名空间是一种绝妙的理念，我们应当多加利用（倡导与号召）
```


### 9.了解`docstring`吗

- 文档字符串是一个重要工具，用于解释文档程序，帮助你的程序文档更加简单易懂。
- 我们可以在函数体的第一行使用一对三个单引号或者一对三个双引号来定义文档字符串。 你可以使用`__doc__`调用函数中的文档字符串属性。

如:

```py
>>> import os
>>> os.__doc__
"OS routines for Mac, NT, or Posix depending on what system we're on.\n\nThis exports:\n  - all functions from posix, nt, os2, or ce, e.g. unlink, stat, etc.\n  - os.path is one of the modules posixpath, or ntpath\n  - os.name is 'posix', 'nt', 'os2', 'ce' or 'riscos'\n  - os.curdir is a string representing the current directory ('.' or ':')\n  - os.pardir is a string representing the parent directory ('..' or '::')\n  - os.sep is the (or a most common) pathname separator ('/' or ':' or '\\\\')\n  - os.extsep is the extension separator ('.' or '/')\n  - os.altsep is the alternate pathname separator (None or '/')\n  - os.pathsep is the component separator used in $PATH etc\n  - os.linesep is the line separator in text files ('\\r' or '\\n' or '\\r\\n')\n  - os.defpath is the default search path for executables\n  - os.devnull is the file path of the null device ('/dev/null', etc.)\n\nPrograms that import and use 'os' stand a better chance of being\nportable between different platforms.  Of course, they must then\nonly use functions that are defined by all platforms (e.g., unlink\nand opendir), and leave all pathname manipulation to os.path\n(e.g., split and join).\n"
>>> 
>>> os.name.__doc__
"str(object='') -> string\n\nReturn a nice string representation of the object.\nIf the argument is a string, the return value is the same object."
```

### 10.了解类型注解吗

- 在python中叫做`Function Annotations`函数注解。
- python3中注解用来给参数,返回值,变量的类型加上注解，对代码没影响。
- Python提供了一个工具方便我们测试类型注解的正确性，`pip install mypy ; mypy demo.py`若无错误则无输出。
- Python对注解所做的唯一的事情是，把他们存储在函数的`__annotations__`属性里，仅此而已，Python不做检查，不做强制，不做验证，什么操作都不做。换句话，注解对Python解释器没任何意义。注解只是元数据，可以供IDE、框架和装饰器等工具使用。

比如，下面的计算两个整数的和：

```py
# filename:test.py
def mysum(num1: int, num2: int = 2) -> int:
    """计算两个整数的和"""
    return str(num1 + num2)


r1 = mysum(1, 2)
print(r1)
r2 = mysum('a', 'b')
print(r2)
print(mysum.__annotations__)
```

运行输出结果如下:

```py
3
ab
{'num1': <class 'int'>, 'num2': <class 'int'>, 'return': <class 'int'>}
```

如果我们使用mypy对代码进行检查，检查结果如下：

```sh
mypy test.py
test.py:15: error: Incompatible return value type (got "str", expected "int")
test.py:20: error: Argument 1 to "mysum" has incompatible type "str"; expected "int"
test.py:20: error: Argument 2 to "mysum" has incompatible type "str"; expected "int"
Found 3 errors in 1 file (checked 1 source file)
```
检查发现，本来`mysum`期望返回一个`int`类型的数据(由`-> int`指定),但`return`语句却返回了一个`str`类型的值。
`mysum('a', 'b')`给函数传递了两个字符串类型的参数，实际上`mysum`期望的参数是`int`类型的，因此检查出来了三个异常。


### 11. 列举你知道Python对象的命名规范，例如方法或者类等

- 变量命名：字母数字下划线，不能以数字开头
- `_`受保护的
- `__`私有的
- `__init__`内置方法
- 函数和方法（类中叫做方法，模块中称作函数）。

### 12.列举几个规范Python代码风格的工具

autopep8, pylint, flake8

### 13.一个编码为GBK的字符串S，要将其转成UTF-8编码的字符串，应如何操作

```py
import chardet

gbk_str = '这是中文字符'.encode('gbk')
print(gbk_str)
print(gbk_str.decode('gbk'))

utf8_str = gbk_str.decode('gbk').encode('utf-8')
print(utf8_str)
print(utf8_str.decode())
print(utf8_str.decode('utf-8'))

print(chardet.detect(gbk_str))
print(chardet.detect(utf8_str))
```

输出结果如下:

```py
b'\xd5\xe2\xca\xc7\xd6\xd0\xce\xc4\xd7\xd6\xb7\xfb'
这是中文字符
b'\xe8\xbf\x99\xe6\x98\xaf\xe4\xb8\xad\xe6\x96\x87\xe5\xad\x97\xe7\xac\xa6'
这是中文字符
这是中文字符
{'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}
{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
```


### 14.用正则切分字符串去除非符号(除字母，数字，下划线外其他的字符)

```py
>>> import re
>>> string = "hello, python!! good!"
>>> re.compile('\W').split(string)
['hello', '', 'python', '', '', 'good', '']
>>> [ item for item in re.compile('\W').split(string) if item != '']
['hello', 'python', 'good']
```


### 15.单引号、双引号、三引号的区别

- 在不需要转义的时候，单引号和双引号无区别。
- 三引号主要用于包裹文档字符串或者多行字符串。

### 16.[[1,2],[3,4],[5,6]]一行代码展开该列表，得出[1,2,3,4,5,6]

```py
>>> question_list =  [[1,2],[3,4],[5,6]]
>>> [item for inside in question_list for item in inside]
[1, 2, 3, 4, 5, 6]
```

### 17.哪些不能作为字典的健

- 字典中的键是不可变类型，可变类型`list`和`dict`不能作为字典键。
- 一个对象能不能作为字典的`key`，就取决于其有没有`__hash__`方法，没有`__hash__`方法不能作为字典的键。


### 18.如何交换字典 {"A"：1,"B"：2}的键和值

```py
>>> demo_dic = {'A':1, 'B':2}         
>>> demo_dic   
{'A': 1, 'B': 2}                      
>>> result_dict = {v:k for k,v in demo_dic.items()}          
>>> result_dict
{1: 'A', 2: 'B'}                      
```

### 19.对生成器类型的对象实现切片功能

```py
>>> import itertools               
>>> itertools.islice(range(10),5, 10)                     
<itertools.islice object at 0x000002E379903A48>           
>>> for i in itertools.islice(range(10),5, 10):           
...     print(i)                   
...         
5           
6           
7           
8           
9           
```


### 20.关于list tuple `copy`和`deepcopy`的区别是什么


tuple是不可变的：

```py
>>> a = (1, 2, 3, [4, 5, 6, 7], 8)
>>> id(a)
3176020056640
>>> a[3] = 3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> a[3][3] = 9
>>> a
(1, 2, 3, [4, 5, 6, 9], 8)
```

- 列表是可变数据类型，数据的值可以修改的; 这里只是修改了元祖子对象的值，而不是修改了元祖的值。
- 修改可变类型的值不会改变内存id，因此元祖的引用还是没有发生变化。可以这么理解，只要不修改元祖中值的内存id，那么就可以进行"修改元祖"操作扩展，

面试官可能会问到：元祖是否可以被修改

答：元祖是不可变数据类型，因此不能修改元祖中的值，但是如果元组中有可变数据类型，那么可以修改可变数据类型中的值，修改可变数据类型的值并不会使其内存id发生变化，所以元祖中元素中的内存id也没有改变，因此就做到了"修改元祖"操作。

list:

```
>>> a = [1, 2, [3, 4]]
>>> b = a
>>> c = a[:]
>>> d = a.co
a.copy(  a.count(
>>> d = a.copy()
>>> import copy
>>> a.
a.append(  a.copy(a.extend(  a.insert(  a.remove(  a.sort(
a.clear(   a.count(   a.index(   a.pop( a.reverse(
>>> e = copy.d
copy.deepcopy(copy.dispatch_table
>>> e = copy.deepcopy(a)
>>> b
[1, 2, [3, 4]]
>>> c
[1, 2, [3, 4]]
>>> d
[1, 2, [3, 4]]
>>> e
[1, 2, [3, 4]]

# 查看id值，只有a和b是同一指向
>>> id(a)
3176020060488
>>> id(b)
3176020060488
>>> id(c)
3176020165768
>>> id(d)
3176020149256
>>> id(e)
3176020265160


# 对a追加数据，只有b跟着变化
>>> a.append(5)
>>> a
[1, 2, [3, 4], 5]
>>> b
[1, 2, [3, 4], 5]
>>> c
[1, 2, [3, 4]]
>>> d
[1, 2, [3, 4]]
>>> e
[1, 2, [3, 4]]
>>>

# 对列表中的子元素列表进行修改，只有deepcopy的值没有更新
>>> a[2][1] = -3
>>> a
[1, 2, [3, -3], 5]
>>> b
[1, 2, [3, -3], 5]
>>> c
[1, 2, [3, -3]]
>>> d
[1, 2, [3, -3]]
>>> e
[1, 2, [3, 4]]
>>>

# 最后检查id值，都没有变化
>>> id(a)
3176020060488
>>> id(b)
3176020060488
>>> id(c)
3176020165768
>>> id(d)
3176020149256
>>> id(e)
3176020265160
>>>
```

- `copy`仅拷贝对象本身，而不拷贝对象中引用的其它对象。
- `deepcopy`除拷贝对象本身，而且拷贝对象中引用的其它对象，可以理解为`deepcopy`复制后与原来的对象就没有关联。


### 21.代码中经常遇到的`*args`,`**kwargs`含义及用法

- `args`是`arguments`的缩写，表示位置参数。
- `kwargs`是`keyword arguments`的缩写，表示关键字参数。
- 一个函数如果定义了`*args`表示该函数可以接收多个(可变)位置参数。
- 一个函数如果定义了`**kwargs`表示该函数可以接收多个(可变)关键字参数。

看下面的示例:

```py
def print_args_kwargs(*args, **kwargs):
    print('args:', args, 'type(args):', type(args))
    for value in args:
        print("positional argument:", value)
    print('kwargs:', kwargs, 'type(kwargs):', type(kwargs))
    for key in kwargs:
        print("keyword argument:\t{}:{}".format(key, kwargs[key]))


print_args_kwargs(1, 2, 3, 'a', 'b', key1='num1', key2='num2')

# 输出：
# args: (1, 2, 3, 'a', 'b') type(args): <class 'tuple'>
# positional argument: 1
# positional argument: 2
# positional argument: 3
# positional argument: a
# positional argument: b
# kwargs: {'key1': 'num1', 'key2': 'num2'} type(kwargs): <class 'dict'>
# keyword argument:	key1:num1
# keyword argument:	key2:num2
```

### 22.Python中会有函数或成员变量包含单下划线前缀和结尾，和双下划线前缀结尾，区别是什么

- 下划线开头的命名方式被常用于模块中，在一个模块中以单下划线开头的变量和方法会被默认划入模块内部范围。
- 当使用`from my_module import *`导入时，单下划线开头的变量和方法是**不会被导入**的。但使用`import my_module`导入的话，仍然可以用`my_module._var`这样的形式访问属性或方法。
- 双下划线开头和结尾的是一些python的"魔术"对象,`class A`中定义的属性`__cont`，这样的变量获取时需要用`A._A__cont`，即使用`__`定义变量可以将名称重整，以保护私有特性，如`__name`。实际上名称被重整为`_ClassName__name`这样的。


### 23.`json`序列化时，可以处理的数据类型有哪些？如何定制支持`datetime`类型

- `json`序列化时，可以处理列表、元组、字典、字符、数值、布尔和`None`。
- 有两种方式定制`datetime`类型，一种是将`datetime`类型转换成字符串再进行序列化；另外一种方式是扩展json的编码方式，继承`json.JSONEncoder`类，可以参考[模块-json模块](./X_json_module.html)

### 24.`json`序列化时，默认遇到中文会转换成`unicode`，如果想要保留中文怎么办

序列化时增加`ensure_ascii=False`参数。

```py
>>> str1 = '中文字符'
>>> json.dumps(str1)
'"\\u4e2d\\u6587\\u5b57\\u7b26"'
>>> json.dumps(str1, ensure_ascii=True)
'"\\u4e2d\\u6587\\u5b57\\u7b26"'
>>> json.dumps(str1, ensure_ascii=False)
'"中文字符"'
```

### 25.python字典和`json`字符串相互转化方法

```py
#导包
import json

#json字符串转换成字典
json.loads(json_str)

#字典转换成json字符串
json.dumps(dict)
```

### 26.如果当前的日期为 20190530，要求写一个函数输出 N 天后的日期，(比如 N 为 2，则输出 20190601)

```py
import sys
from datetime import datetime, timedelta


def after_num_days(daytime: str, num: int) -> str:
    """计算给定日期后num天的日期"""
    try:
        old_day = datetime.strptime(daytime, "%Y%m%d").date()
    except Exception as e:
        print(e)
        sys.exit(1)

    offset = timedelta(days=num)
    new_day = (old_day + offset).strftime("%Y%m%d")
    print("%s天后的日期为%s" % (num, new_day))
    return new_day


after_num_days('20200501', -2)
after_num_days('20200512', 3)
after_num_days('20200228', 1)
after_num_days('20190530', 2)
after_num_days('20200230', 1)

# 输出：
# -2天后的日期为20200429
# 3天后的日期为20200515
# 1天后的日期为20200229
# 2天后的日期为20190601
# day is out of range for month
```

### 27.函数装饰器有什么作用？请列举说明

- 装饰器就是拓展原来函数功能的一种函数，这个函数的返回值也是一个函数。
- 装饰器其实就是一个闭包，把一个函数当作参数然后返回一个替代版参数。
- 使用装饰器的好处是在不用更改原函数的代码前提下给函数增加新的功能。
- 装饰器可以扩展原函数的日志，预处理工作，清理工作，性能测试，时间测试，事务处理，缓存，权限校验等等功能。
- 装饰器会丢失原函数的元信息，需要使用`functools`包的`wraps`装饰器来消除这种弊端。
- 多层装饰器时，先执行靠近`def`定义处(内层)的装饰器，再执行上层(外层)的装饰器。


### 28.`__call__`

可以调用的对象: 一个特殊的魔术方法可以让类的实例的行为表现的像函数一样。

```py
class Entity:
'''调用实体来改变实体的位置。'''
    
    def __init__(self, size, x, y):
        self.x, self.y = x, y
        self.size = size
    
    def __call__(self, x, y):
        '''改变实体的位置'''
        self.x, self.y = x, y

e = Entity(1, 2, 3) // 创建实例
e(4, 5) //实例可以象函数那样执行，并传入x y值，修改对象的x y
```


### 29.如何判断一个对象是函数还是方法

- 在类外声明`def`为函数。
- 类中声明`def`：使用类调用为函数，使用实例化对象调用为方法。

可以使用`isinstance()`判断:

```py
from types import MethodType, FunctionType


class Work(object):
    def show(self):
        print("执行show方法")


work = Work()
print(Work.show)
print(work.show)
print(isinstance(Work.show, FunctionType))
print(isinstance(work.show, MethodType))

# 输出：
# <function Work.show at 0x0000014F6A946D90>
# <bound method Work.show of <__main__.Work object at 0x0000014F536DA4E0>>
# True
# True
```

### 30.python实现接口

- 接口只是定义了一些方法，而没有去实现，多用于程序设计时，只是设计需要有什么样的功能，但是并没有实现任何功能，这些功能需要被另一个类（B）继承后，由类B去实现其中的某个功能或全部功能。
- 遵循：开放封闭原则，依赖导致原则，接口隔离原则，继承多态。
- 编程思想：为子类做规范； 归一化设计：几个类都实现了相同的方法。
- 抽象类：最好单继承，且可以简单的实现功能，接口类：可以多继承，且最好不实现具体功能。
- 在python中接口由抽象类和抽象方法去实现，接口是不能被实例化的，只能被别的类继承去实现相应的功能。
- 个人觉得接口在python中并没有那么重要，因为如果要继承接口，需要把其中的每个方法全部实现，否则会报编译错误，还不如直接定义一个class，其中的方法实现全部为`pass`，让子类重写这些函数。
- 方法一：用抽象类和抽象函数实现方法（适用于单继承）;方法二：用普通类定义接口（推荐）。

### 31.Python 中的反射了解么

- 在Python中，能够通过一个对象，找出其`type`、`class`、`attribute`或`method`的能力，称为反射或自省。
- 具有反射能力的函数有`type()`,`isinstance()`,`callable()`,`dir()`,`getattr()`等。

### 32.metaclass or type
https://www.liaoxuefeng.com/wiki/897692888725344/923030550637312

### 33.Python中递归的最大次数1000,怎么改

```py
>>> import sys           
>>> sys.getr             
sys.getrecursionlimit( sys.getrefcount(         
>>> sys.getrecursionlimit()                     
1000                     
>>> sys.setrecursionlimit(1500)                 
>>> sys.getrecursionlimit()                     
1500                     
>>>                      
```

### 34.列举5个Python中的异常类型以及其含义

Python所有的错误都是从`BaseException`类派生的，内置异常见如下:

```py
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning
```


### 35.w、a+、wb 文件写入模式的区别

- `r`: 读取文件，若文件不存在则会报错
- `w`: 写入文件，若文件不存在则会先创建再写入，会覆盖原文件
- `a`: 写入文件，若文件不存在则会先创建再写入，但不会覆盖原文件，而是追加在文件末尾
- `rb`,`wb`：分别于r,w类似，用于读写二进制文件
- `r+`: 可读、可写，文件不存在也会报错，写操作时会覆盖
- `w+`: 可读，可写，文件不存在先创建，会覆盖
- `a+`：可读、可写，文件不存在先创建，不会覆盖，追加在末尾


### 36.举例`sort`和`sorted`的区别

- 使用`sort()`方法对`list`排序会修改`list`本身,不会返回新`list`，`sort()`不能对`dict`字典进行排序。
- `sorted`方法对可迭代的序列排序生成新的序列，对`dict`排序默认会按照`dict`的`key`值进行排序，最后返回的结果是一个对`key`值排序好的`list`。
- `sorted`对`tuple`,`dict`依然有效，而`sort`不行。

```py
>>> l1 = [2,3,1]     
>>> l1.              
l1.append(  l1.copy(    l1.extend(  l1.insert(  l1.remove(  l1.sort(
l1.clear(   l1.count(   l1.index(   l1.pop(     l1.reverse(        
>>> l1.sort()        
>>> l1               
[1, 2, 3]            
>>> t1= (1,3,2)      
>>> t1.              
t1.count( t1.index(  
>>> dict1={'a':1,'aa':2,'b':3}
>>> dict1.           
dict1.clear(      dict1.fromkeys(   dict1.items(      dict1.pop(        dict1.setdefault( dict1.values(
dict1.copy(       dict1.get(        dict1.keys(       dict1.popitem(    dict1.update(     
>>> sorted(dict1)    
['a', 'aa', 'b']     
>>> sorted(t1)       
[1, 2, 3]            
>>>                  
>>> t2=[2,4,1,3]    
>>> sorted(t2)
[1, 2, 3, 4]        
>>> t2              
[2, 4, 1, 3]        
```


### 37.在`requests`模块中，`requests.content`和`requests.text`什么区别

- `.content`中间存的是字节码, `.text`存的是`.content`编码后的字符串。
- 操作方式就是，如果想取得文本就用`.text`，如果想获取图片，就用`.content`。


### 38.python新式类和经典类的区别

- Python 2.x中默认都是经典类，只有显式继承了object才是新式类。
- python 3.x中默认都是新式类,经典类被移除，不必显式的继承object。

### 39.字符串的操作题目


全字母短句`PANGRAM`是包含所有英文字母的句子，比如：`A QUICK BROWN FOX JUMPS OVER THE LAZY DOG`. 定义并实现一个方法`get_missing_letter`, 传入一个字符串采纳数，返回参数字符串变成一个`PANGRAM`中所缺失的字符。应该忽略传入字符串参数中的大小写，返回应该都是小写字符并按字母顺序排序（请忽略所有非`ACSII`字符）。

说明：

- 全字母句是指包含有字母表中所有字母并且言之成义的句子。全字母句被用于显示字体和测试打字机。
- 英语中最知名的全字母句是“The quick brown fox jumps over the lazy dog（敏捷的棕色狐狸跳过懒狗身上）”。

**下面示例是用来解释，双引号不需要考虑:**

(0)输入: "A quick brown fox jumps over the lazy dog"

返回： ""

(1)输入: "A slow yellow fox crawls under the proactive dog"

返回: "bjkmqz"

(2)输入: "Lions, and tigers, and bears, oh my!"

返回: "cfjkpquvwxz"

(3)输入: ""

返回："abcdefghijklmnopqrstuvwxyz"



```py
import re
import string


def get_missing_letter(check_string):
    """返回缺失的字符"""
    exist_ascii = set(re.findall('[a-z]', check_string.lower()))
    all_ascii = set(string.ascii_lowercase)
    missing_letter = sorted(all_ascii - exist_ascii)
    return ''.join(missing_letter)


print(get_missing_letter('A quick brown fox jumps over the lazy dog'))
print(get_missing_letter('A slow yellow fox crawls under the proactive dog'))
print(get_missing_letter('Lions, and tigers, and bears, oh my!'))
print(get_missing_letter(''))

# 输出：
# 
# bjkmqz
# cfjkpquvwxz
# abcdefghijklmnopqrstuvwxyz
```

### 40.可变类型和不可变类型

- 可变类型有`list`,`dict`,不可变类型有`str`，`int`, `float`, `complex`,`tuple`。
- 当进行修改操作时，可变类型传递的是内存中的地址，也就是说，直接修改内存中的值，并没有开辟新的内存。
- 不可变类型被改变时，并没有改变原内存地址中的值，而是开辟一块新的内存，将原地址中的值复制过去，对这块新开辟的内存中的值进行操作。

### 41.`is`和`==`有什么区别

- `is`：比较的是两个对象的`id`值是否相等，也就是比较俩对象是否为同一个实例对象。是否指向同一个内存地址。
- `==`：比较的两个对象的内容/值是否相等，默认会调用对象的`eq()`方法。

### 42.求出列表所有奇数并构造新列表

```py
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
res = [i for i in a if i % 2 == 1]
print(res)
```

### 43.用一行python代码写出1+2+3+10248

```py
from functools import reduce

# 1.使用sum内置求和函数
num = sum([1, 2, 3, 10248])
print(num)

# 2.reduce 函数
num1 = reduce(lambda x, y: x + y, [1, 2, 3, 10248])
print(num1)
```


### 44.Python中变量的作用域？（变量查找顺序)

- Python 在查找"名称"时，是按照 LEGB 规则查找的：`Local-->Enclosed-->Global-->Built in`。
- `Local`: 指的就是函数或者类的方法内部。
- `Enclosed`: 指的是嵌套函数（一个函数包裹另一个函数，闭包）。
- `Global`: 指的是模块中的全局变量。
- `Built in`: 指的是 Python 为自己保留的特殊名称。

可参考以下示例:

```py
str = "global"


def out():
    # str = "out"

    def inner():
        # str="inner"
        print(str)

    inner()


out()
```

### 45.字符串 `"123"` 转换成 `123`，不使用内置api，例如 `int()`

```py
# 方法1，利用str函数
def atoi(s):
    """整数字符串转整数"""
    num = 0
    for v in s:
        for j in range(10):
            if v == str(j):
                num = num * 10 + j
    return num

#方法2： 利用ord函数
def atoi(s):
    """整数字符串转整数"""
    num = 0
    for v in s:
        num = num * 10 + ord(v) - ord('0')
    return num
```

### 46.Given an array of integers

给定一个整数数组和一个目标值，找出数组中和为目标值的两个数。你可以假设每个输入只对应一种答案，且同样的元素不能被重复利用。示例:给定nums = [2,7,11,15],target=9 因为 nums[0]+nums[1] = 2+7 =9,所以返回[0,1]。

```py
def two_sum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    for i in nums:
        if target - i in nums and i is not target - i:
            return [nums.index(i), nums.index(target - i)]


print(two_sum([2, 7, 11, 15], 9))
```


### 47.有一个jsonline格式的文件file.txt大小约为10K

```py
def get_lines():
    with open('file.txt','rb') as f:
        return f.readlines()

if __name__ == '__main__':
    for e in get_lines():
        process(e) # 处理每一行数据
```

现在要处理一个大小为10G的文件，但是内存只有4G，如果在只修改`get_lines`函数而其他代码保持不变的情况下，应该如何实现？需要考虑的问题都有那些

```py
def get_lines():
    with open('file.txt','rb') as f:
        for i in f:
            yield i
```

要考虑的问题有：内存只有4G无法一次性读入10G文件，需要分批读入，分批读入数据要记录每次读入数据的位置。分批每次读取数据的大小，太小会在读取操作花费过多时间。
[https://stackoverflow.com/questions/30294146/python-fastest-way-to-process-large-file](https://stackoverflow.com/questions/30294146/python-fastest-way-to-process-large-file)

### 48.返回该文件夹中所有文件的路径

递归遍历目录树，生成目录树下所有文件的路径信息:

```py
def walkdir(path):
    import os
    for root, dirs, files in os.walk(path, followlinks=False):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))

walkdir("D:\\data\\vueblog\\myblog\\docs\\backend")
```
