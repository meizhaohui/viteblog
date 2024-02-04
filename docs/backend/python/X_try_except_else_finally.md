# 异常

[[toc]]

本节介绍Python的异常。

## 异常的定义


- 异常是一个事件，该事件会在程序执行时发生，影响程序的正常执行。
- 一般情况下，在Python无法正常处理程序时就会发生一个异常。
- 异常是Python对象，表示一个错误。
- 当Python脚本发生异常时，我们需要捕获处理它，否则程序会终止运行。
- 当你执行可能出错的代码时，需要适当的异常处理程序用于阻止潜在的错误发生。
- 在异常可能发生的地方添加异常处理程序，对于用户明确错误是一种好办法。


## 常见的异常


- `ZeroDivisionError`除零异常

```python
In [1]: 1/0
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)
<ipython-input-1-9e1622b385b6> in <module>
----> 1 1/0

ZeroDivisionError: division by zero
```

- `AttributeError`属性异常

```python
In [2]: import os                                                               

In [3]: os.name                                                                 
Out[3]: 'posix'

In [4]: os.Name                                                                 
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-4-edb55bc87dba> in <module>
----> 1 os.Name

AttributeError: module 'os' has no attribute 'Name'
```

- `ImportError`导入异常

```python
In [5]: import maths                                                                                                                   
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
<ipython-input-8-6e25cba24411> in <module>
----> 1 import maths

ImportError: No module named 'maths'

In [6]: import math     
```

- `IndexError`索引异常

```python
In [7]: list1=['a','b']

In [8]: list1[3]
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
<ipython-input-8-831b15cbf272> in <module>
----> 1 list1[3]

IndexError: list index out of range
```
   
- `SyntaxError`语法异常

```python
In [9]: print 'hello'
  File "<ipython-input-9-5a1ef41e7057>", line 1
    print 'hello'
                ^
SyntaxError: Missing parentheses in call to 'print'
```

- `IndentationError`缩进异常

```python
In [10]: a = 1                                                                                                                         

In [11]: if a > 0: 
    ...:     print(a) 
    ...:   print(a + 1)                                                                                                                
  File "<tokenize>", line 3
    print(a + 1)
    ^
IndentationError: unindent does not match any outer indentation level
```

## 内置异常


Python所有的错误都是从`BaseException`类派生的，内置异常见如下:

```python
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
           
## 异常处理语法


异常处理语法如下:

```python
try:
    <statements>        #运行try语句块，并试图捕获异常
except <ExceptionErrorName1>:
    <statements>        #如果ExceptionErrorName1异常发现，那么执行该语句块。
except (ExceptionErrorName2,ExceptionErrorName3):
    <statements>        #如果元组内的任意异常发生，那么捕获它
except <ExceptionErrorName4> as <variable>:
    <statements>        #如果ExceptionErrorName4异常发生，那么进入该语句块，并把异常实例命名为variable
except:
    <statements>        #发生了以上所有列出的异常之外的异常
else:
<statements>            #如果没有异常发生，那么执行该语句块
finally:
    <statement>         #无论是否有异常发生，均会执行该语句块
```
说明:

- `else`和`finally`是可选的，可能会有0个或多个`except`，但是，如果出现一个`else`的话，必须有至少一个`except`。
- 不管你如何指定异常，异常总是通过实例对象来识别，并且大多数时候在任意给定的时刻激活。一旦异常在程序中某处由一条`except`子句捕获，它就死掉了，除非由另一个`raise`语句或错误重新引发它。
- 在`try`中的代码如果发生异常，则会被捕获，然后执行`except`中的代码，否则跳过`except`块代码，此时执行`else`语句块。
- 无论异常是否发生`finally`语句块的代码一定会执行。
- 在对异常进行处理时，建议`except`后面接具体的异常名称，不要直接使用`except`不接任何异常名去处理异常，因为`except`适用于任何异常类型，你可以使用一个`except`去捕获所有的异常，但这样的处理方式会比较泛化。
- 可以使用`as`将异常名称赋值给变量，再输出存储在变量中的异常信息。
  
## 异常处理示例


- 示例1

处理除零异常:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt1(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')

expt1(4,0)
```

运行:

```python
meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py 
程序出现异常，异常信息：被除数为0
```

以上程序，我们已经获取到了除零异常`ZeroDivisionError`,感觉自己处理得很完美。假如我们将`expt1(4,0)`改为`expt1(4,'')`,然后再运行看看会发生什么。

运行:

```python
[meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py 
Traceback (most recent call last):
  File "try_except_else_finally.py", line 10, in <module>
    expt1(4,'')
  File "try_except_else_finally.py", line 5, in expt1
    c = a/b
TypeError: unsupported operand type(s) for /: 'int' and 'str'
```

怎么又出现了一个`TypeError`类型异常，但我们却没有捕获到，上面提示不能在int类型和字符串类型之间做除法运算。看来我们要补上这个异常的处理，获取到这个异常。

- 示例2

我们改一个这个脚本文件:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt2(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
    except TypeError:
        print('程序出现异常，异常信息：参数a和b类型不同,仅支持float或int类型')

expt2(4,'')
```

运行:

```python
[meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py
程序出现异常，异常信息：参数a或b的类型不支持，仅支持float或int类型
```

我们看一下能不能捕获除零异常:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt2(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
    except TypeError:
        print('程序出现异常，异常信息：参数a和b类型不同,仅支持float或int类型')

expt2(4,0)
```

运行:

```python
[meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py
程序出现异常，异常信息：被除数为0
```

可以看出除零异常和类型异常都能正常的捕获到。

- 示例3

联合`else`和`finally`一起使用，修改脚本文件:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt3(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
    except TypeError:
        print('程序出现异常，异常信息：参数a或b的类型不支持，仅支持float或int类型')
    else:
        print('No exception')
    finally:
        print('always display')
expt3(4, 2)
```

运行:

```python
[meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py 
the value is:2.0
No exception
always display
```

没有异常正常运行，打印出4/2的值为2.0,因为没有异常，`except`语句不会被执行，但`else`语句会被执行，所有会打印出"`No exception`"，另外`finally`语句一直会被执行，所以"`always display`"会被打印出来。

## 异常中的`return`语句


如果在异常处理时指定`return`语句，会出现什么效果。

- 没有异常,且没有设置`return`

示例4:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt4(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
        # return 'try'
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
        # return 'exceptZero'
    except TypeError:
        print('程序出现异常，异常信息：参数a或b的类型不支持，仅支持float或int类型')
        # return 'exceptType'
    else:
        print('No exception')
        # return 'else'
    finally:
        print('always display')
        # return 'finally'

if __name__ == '__main__':
    return_string = expt4(4, 2)
    print('return_string:{}'.format(return_string))
```

运行:

```python
meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py
the value is:2.0
No exception
always display
return_string:None
```

因为没有指定`return`语句，返回的是隐式返回值`None`。

- 没有异常,且`try`中设置`return`

示例5:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt4(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
        return 'try'
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
        # return 'exceptZero'
    except TypeError:
        print('程序出现异常，异常信息：参数a或b的类型不支持，仅支持float或int类型')
        # return 'exceptType'
    else:
        print('No exception')
        # return 'else'
    finally:
        print('always display')
        # return 'finally'

if __name__ == '__main__':
    return_string = expt4(4, 2)
    print('return_string:{}'.format(return_string))
```
运行:

```python
meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py
the value is:2.0
No exception
return_string:try
```

仅在`try`中有`return`时，没有异常的情况下，会返回`try`中的返回值"`try`"。

- 没有异常，在`try`,`except`,`else`,`finally`中都有`return`语句

示例6:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt4(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
        return 'try'
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
        return 'exceptZero'
    except TypeError:
        print('程序出现异常，异常信息：参数a或b的类型不支持，仅支持float或int类型')
        return 'exceptType'
    else:
        print('No exception')
        return 'else'
    finally:
        print('always display')
        return 'finally'

if __name__ == '__main__':
    return_string = expt4(4, 2)
    print('return_string:{}'.format(return_string))
```

运行:

```python
meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py
the value is:2.0
always display
return_string:finally
```

没有异常，在`try`,`except`,`else`,`finally`中都有`return`语句时，会返回`finally`中的返回值"`finally`"，并且`except`,`else`语句不会被执行,`try`中的`return`语句不起作用。

- 没有异常，在`except`,`else`,`finally`中有`return`语句

示例7:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt4(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
        # return 'try'
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
        return 'exceptZero'
    except TypeError:
        print('程序出现异常，异常信息：参数a或b的类型不支持，仅支持float或int类型')
        return 'exceptType'
    else:
        print('No exception')
        return 'else'
    finally:
        print('always display')
        return 'finally'

if __name__ == '__main__':
    return_string = expt4(4, 2)
    print('return_string:{}'.format(return_string))
```

运行:

```python
meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py
the value is:2.0
No exception
always display
return_string:finally
```

此时，没有异常，`except`被忽略，`else`语句被执行，打印出"`No exception`"，但最后的返回值还是`finally`语句中的返回值"`finally`"。

- 没有异常，在`except`,`else`中有`return`语句

示例8:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt4(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
        # return 'try'
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
        return 'exceptZero'
    except TypeError:
        print('程序出现异常，异常信息：参数a或b的类型不支持，仅支持float或int类型')
        return 'exceptType'
    else:
        print('No exception')
        return 'else'
    finally:
        print('always display')
        # return 'finally'

if __name__ == '__main__':
    return_string = expt4(4, 2)
    print('return_string:{}'.format(return_string))
```


运行:

```python
meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py
the value is:2.0
No exception
always display
return_string:else
```

没有异常，在`except`和`else`中有`return`时，会将`return`中的返回值"`else`"作为函数的返回值。

- 有异常，在`try`,`except`,`else`,`finally`中都有`return`语句

示例9:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt4(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
        return 'try'
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
        return 'exceptZero'
    except TypeError:
        print('程序出现异常，异常信息：参数a或b的类型不支持，仅支持float或int类型')
        return 'exceptType'
    else:
        print('No exception')
        return 'else'
    finally:
        print('always display')
        return 'finally'

if __name__ == '__main__':
    return_string = expt4(4, 0)
    print('return_string:{}'.format(return_string))
```

运行:

```python
meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py
程序出现异常，异常信息：被除数为0
always display
return_string:finally
```

有异常，`else`不会被执行，`except`语句会执行，由于最后`finally`有`return`语句，最后返回值是`finally`语句中的"`finally`"。

- 有异常，在`try`,`except`,`else`中都有`return`语句

示例10:

```python
# Filename: try_except_else_finally.py
# Author: meizhaohui
def expt4(a, b):
    try:
        c = a/b
        print('the value is:{}'.format(c))
        return 'try'
    except ZeroDivisionError:
        print('程序出现异常，异常信息：被除数为0')
        return 'exceptZero'
    except TypeError:
        print('程序出现异常，异常信息：参数a或b的类型不支持，仅支持float或int类型')
        return 'exceptType'
    else:
        print('No exception')
        return 'else'
    finally:
        print('always display')
        # return 'finally'

if __name__ == '__main__':
    return_string = expt4(4, 0)
    print('return_string:{}'.format(return_string))
```

运行:

```python
meizhaohui@localhost python_scripts]$ python3 try_except_else_finally.py
程序出现异常，异常信息：被除数为0
always display
return_string:exceptZero
```

有异常，由于`finally`语句没有`return`语句，`try`有异常，不会执行`try`代码块中的`return`语句，执行`except`语句，返回值是除零异常中的"`exceptZero`"。

总结：

1. `try`中有`return`语句时，会阻止`else`语句的执行，并不影响`finally`语句的执行。
1. `try`中没有`return`语句时，如果`try`中没有异常，`except`语句会被跳过，执行`else`语句。
1. 在含有`return`的情况下，并不会阻碍`finally`语句的执行。
1. 在`try`和`finally`中都有`return`时，无论有没有异常，`finally`语句会修改最后的返回值。
1. 在`finally`中没有`return`语句时，`try`,except,`else`中有`return`语句，没有异常时，`else`中返回值作为最终返回值;有异常时，`except`中返回值作为最终返回值。
1. 如果没有异常发生，`try`中有`return` 语句，这个时候`else`块中的代码是没有办法执行到的，但是`finally`语句中如果有`return`语句会修改最终的返回值，我个人理解的是`try`中`return`语句先将要返回的值放在某个CPU寄存器，然后运行`finally`语句的时候修改了这个寄存器的值，最后在返回到`try`中的`return`语句返回修改后的值。
1. 如果有异常发生，`try`中的`return`语句肯定是执行不到，在捕获异常的`except`语句中，如果存在`return`语句，那么也要先执行`finally`的代码，`finally`里面的代码会修改最终的返回值，然后在从`except`块的`return`语句返回最终修改的返回值， 和第5条一致。

以上总结可以看在使用`try`进行异常捕获处理时，`return`语句的处理相当麻烦。总结以下三点:

- 不要在`try`,`except`,`else`里面写返回值，如果没有`finally`语句，就在最后面写`return`语句，或者将`return`语句写在`finally`中。
- `try`,`except`,`else`里面是做某事，不处理返回值。
- 在`try`中的代码尽可能的少，减少异常出现的可能性。

## `raise`手动抛出异常


使用`raise`语句手动抛出异常：

- `raise ExceptionErrorName`   # 抛出ExceptionErrorName异常
- `raise ExceptionErrorName('info') `  # 抛出ExceptionErrorName异常,提供额外的异常信息info

示例:

```python
In [1]: raise NameError
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-1-42b67b2fc75d> in <module>
----> 1 raise NameError

NameError:

In [2]: raise NameError('名称异常')
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-2-daa6ee1852fc> in <module>
----> 1 raise NameError('名称异常')

NameError: 名称异常

In [3]: raise ZeroDivisionError('除零异常')
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)
<ipython-input-3-02e66f4d0766> in <module>
----> 1 raise ZeroDivisionError('除零异常')

ZeroDivisionError: 除零异常
```

## 自定义异常


- 用户可以自己定义一个Python中没有涉及的异常。
- 自定义异常必须直接或间接的继承`Exception`类。
- 自定义异常按照命名规范以"`Error`"结尾，显式地告诉用户这是异常。
- 自定义异常只能使用`raise`方式手动抛出。

我们定义一个网络异常的自定义异常:

```python
# Filename: networkerror.py
# Author: meizhaohui

class NetworkError(RuntimeError):
    def __init__(self, host):
        self._host = host

    def __str__(self):
        return 'Unknow host:{}'.format(self._host)

if __name__ == '__main__':
    try:
        raise NetworkError('python.org')
    except NetworkError as e:
        print('NetworkError: %s' % e)
```

运行:

```python
[meizhaohui@localhost python_scripts]$ python3 networkerror.py
NetworkError: Unknow host:python.org
```

说明：

- 自定义异常类`NetworkError`继承`RuntimeError`,而从内置异常图中可以看`RuntimeError`继承`Exception`，因此`NetworkError`是间接继承`Exception`类的。
- 使用`raise`手动抛出`NetworkError`异常，并在`except`中捕获，并打印出异常的信息。


参考文献:

1. [Python异常处理](http://www.runoob.com/python/python-exceptions.html)
1. [Built-in Exceptions](https://docs.python.org/3.6/library/exceptions.html?highlight=exception)
1. [Python异常及处理方法总结](https://blog.csdn.net/polyhedronx/article/details/81589196)
1. [Python中的异常处理](https://www.cnblogs.com/jessonluo/p/4743574.html)
1. [Python——异常](https://blog.csdn.net/qq_41573234/article/details/82466313)
1. [python的try finally (还真不简单)](https://www.cnblogs.com/xuanmanstein/p/8080629.html)
1. [python try except else finally 执行顺序详细分析](https://www.2cto.com/kf/201405/304975.html)

