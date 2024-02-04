# 成为真正的Python开发者

[[toc]]

Python开发者，用英文表示时为`Pythonista`，参考[我不认识Pythoner这种开发者](https://zhuanlan.zhihu.com/p/26832983).

> 那正确的词应该是什么？
>
> 备选答案有：Pythonista、Pythoneer、Pythonist
>
> Pythoneer：使用python语言开发程序的人。
>
> Pythonista：顾名思义表示「Python支持者」，更表示资深的，对代码质量和品味有要求的开发者，这种执念也就是所谓「Pythonic」。这也是为什么称自己为Pythonista的人最多的原因了。
>
> Pythonist：-ist这种后缀表示职业中有一定的信念，有专家角度，如scientist、physicist、chemist，还给人严肃且不活泼的感觉，所以用的人很少。
>
>  **所以正确的用法，请大家大声的和我念一遍：Pythonista！！**



本章节选自丁嘉瑞等译的《Python语言及其应用》一书。

## 关于编程

学会享受编程的乐趣！

编程有很多领域，如计算机图形学、操作系统、商业应用、科学等等等。

编程中数字能力并不是很重要，更重要的是要具备逻辑思考能力！

编程中要有耐心，尤其是寻找代码中的Bug的时候！



## 寻找Python代码

当你需要开发功能时，最快的解决方法是借鉴别人写的代码。你可以从这些渠道获取代码。

- Python官方文档， [https://docs.python.org/3/](https://docs.python.org/3/)，你可以在这里找到很多有用的东西！
- Python包索引PyPi，[https://pypi.org/](https://pypi.org/)，你可以在这个网站上面直接搜索你要的包，或者使用pip搜索！
- GitHub仓库，[https://github.com/search?q=python](https://github.com/search?q=python), 在这里你可以查看到所有跟Python相关的开源代码。



## 安装包

有3种方式安装Python包：

- 推荐使用`pip`，你可以使用`pip`安装绝大多数Python包。
  - 安装最新版， `pip install packagename`，如`pip install flask`。
  - 安装指定版，`pip install packagename==xxx`，如`pip install flask==1.1.2`。
  - 指定最小版本，`pip install packagename>=xxx`，如`pip install flask>=0.9.0`。
  - 通过requirements.txt文件安装，`pip install -r requirements.txt`。
- 有时可以使用操作系统自带的包管理工具，如`yum`、`homebrew`等。
- 从源码安装。
  - 这种方式一般是先下载源码，然后源码是压缩文件，则需要先解压。
  - 在包含`setup.py`文件的目录中运行`python setup.py install`安装！



## 集成开发环境

- Python命令行

```python
$ python3
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.name
'posix'
>>>
```

- ipython

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import os

>>> os?
Type:        module
String form: <module 'os' from '/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/os.py'>
File:        /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/os.py
Docstring:
OS routines for NT or Posix depending on what system we're on.

This exports:
  - all functions from posix or nt, e.g. unlink, stat, etc.
  - os.path is either posixpath or ntpath
  - os.name is either 'posix' or 'nt'
  - os.curdir is a string representing the current directory (always '.')
  - os.pardir is a string representing the parent directory (always '..')
  - os.sep is the (or a most common) pathname separator ('/' or '\\')
  - os.extsep is the extension separator (always '.')
  - os.altsep is the alternate pathname separator (None or '/')
  - os.pathsep is the component separator used in $PATH etc
  - os.linesep is the line separator in text files ('\r' or '\n' or '\r\n')
  - os.defpath is the default search path for executables
  - os.devnull is the file path of the null device ('/dev/null', etc.)

Programs that import and use 'os' stand a better chance of being
portable between different platforms.  Of course, they must then
only use functions that are defined by all platforms (e.g., unlink
and opendir), and leave all pathname manipulation to os.path
(e.g., split and join).

>>>
```

- PyCharm,开发Python项目时适合使用PyCharm！社区版是免费的！



## 命名和文档

- 文档可以包括注释和文档字符串，也可以把信息记录在变量名、函数名、模块名和类名中。

- Python没有常量，但是使用大写字母和下划线来表示常量名。
- 

可以参考Google的Python编码规范或者PEP8格式规范建议！

- Google Python Style Guide [https://google.github.io/styleguide/pyguide.html](https://google.github.io/styleguide/pyguide.html)
- Google python编码规范中文版 [https://www.runoob.com/w3cnote/google-python-styleguide.html](https://www.runoob.com/w3cnote/google-python-styleguide.html)
- PEP8 [https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)

## 测试代码

### 代码检查

我们可以使用pylint、Flake8、pyright等工具对Python代码进行代码检查，可以参考[代码检查](https://hellogitlab.com/backend/python/X_Python_style_and_static_check.html) 。

这部分主要是代码风格检查和静态检查等。

### 使用`unittest`进行代码测试

我们已经通过了代码风格检查，下面该真正地测试程序逻辑了！

最好先编写独立的测试程序，在提交代码到源码控制系统之前确保通过所有测试。写测试看起来是一件很麻烦的事情，但是它们真的能帮助你更快地发现问题。尤其是回归测试（破坏之前还能正常工作的代码）。工程师们已经从惨痛的经历中领悟到一个真理：即使是很小的看起来没有任何问题的改动，也可能出问题。如果看那些优秀的Python包就会发现，它们大都有测试集。

标准库中有两个测试包，unittest和doctest。

首先我们介绍unittest测试包。假设我们编写了一个单词首字母转大写的模块，第一版直接使用标准字符串函数`capitalize()`，之后会看到许多意料之外的结果，把下面的代码保存为cap.py:

```python
def just_do_it(text):
    return text.capitalize()
```

好，我们跟踪书上的示例，一步步的来做。

测试就是先确定输入对应的期望输出(本例期望的输出是输入文本的首字母大写版本)，然后把输入传入需要测试的函数，并检查返回值和期望输出是否相同。期望输出被称为`断言`。因此在`unittest`中，可以使用`assert`断言开头的方法来检查返回的结果。比如下面代码中的`assertEqual`方法。

把下面的代码保存为test_cap.py:

```python
import unittest

import cap


class TestCap(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_one_word(self):
        text = 'duck'
        result = cap.just_do_it(text)
        self.assertEqual(result, 'Duck')

    def test_multiple_words(self):
        text = 'a veritable flock of ducks'
        result = cap.just_do_it(text)
        self.assertEqual(result, 'A Veritable Flock Of Ducks')


if __name__ == '__main__':
    unittest.main()

```

查看文件内容：

```sh
$ cat cap.py 
def just_do_it(text):
    return text.capitalize()%                                                                                                                                             $ cat test_cap.py 
import unittest

import cap


class TestCap(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_one_word(self):
        text = 'duck'
        result = cap.just_do_it(text)
        self.assertEqual(result, 'Duck')

    def test_multiple_words(self):
        text = 'a veritable flock of ducks'
        result = cap.just_do_it(text)
        self.assertEqual(result, 'A Veritable Flock Of Ducks')


if __name__ == '__main__':
    unittest.main()
```

`setUp()`和`tearDown()`方法是在每个测试方法执行之前/后执行的函数，它们通常用来分配和回收测试需要的外部资源，比如数据库连接或者一些测试数据。在本例中，我们的测试方法已经足够进行测试，因此不需要再定义`setUp()`和`tearDown()`，但是放一个空方法也没有关系，我们测试的核心是函数`test_one_word()`和`test_multiple_words()`,它们会运行我们定义的`just_do_it()`函数，传入不同的输出并检查返回值是否和期望输出一样！

我们运行一下脚本，它会调用那两个测试方法：

```sh
$ python3 test_cap.py
F.
======================================================================
FAIL: test_multiple_words (__main__.TestCap)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_cap.py", line 21, in test_multiple_words
    self.assertEqual(result, 'A Veritable Flock Of Ducks')
AssertionError: 'A veritable flock of ducks' != 'A Veritable Flock Of Ducks'
- A veritable flock of ducks
?   ^         ^     ^  ^
+ A Veritable Flock Of Ducks
?   ^         ^     ^  ^


----------------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (failures=1)
$ 
```

看起来第一个测试`test_one_word`通过了，但是第二个`test_multiple_words`失败了。上箭头(^)指出了字符串不相同的地方！

为什么多个单词会失败？可以阅读字符串的capitalize函数文档来寻找线索，它只会把第一个单词的第一个字母转换成大定，或许我们应该先阅读文档。

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> str1='duck'

>>> str1.capitalize?
Docstring:
S.capitalize() -> str

Return a capitalized version of S, i.e. make the first character
have upper case and the rest lower case.
Type:      builtin_function_or_method

>>>
```

为了修复这个问题，我们需要改进代码！

我们可以使用`title()`函数，我们把`cap.py`中的`capitalize()`替换成`title()`：

```python
def just_do_it(text):
    # return text.capitalize()
    return text.title()
```

```sh
$ cat cap.py 
def just_do_it(text):
    # return text.capitalize()
    return text.title()
```

我们再次运行测试，看看结果如何：

```sh
$ python3 test_cap.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

这时两个测试都运行通过了，看起来没问题了。不过，其实还是有问题的，我们还需要在`test_cap.py`中添加另一个方法，修改后内容如下：

```python
import unittest

import cap


class TestCap(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_one_word(self):
        """测试单个单词的情况"""
        text = 'duck'
        result = cap.just_do_it(text)
        self.assertEqual(result, 'Duck')

    def test_multiple_words(self):
        """测试多个单词的情况"""
        text = 'a veritable flock of ducks'
        result = cap.just_do_it(text)
        self.assertEqual(result, 'A Veritable Flock Of Ducks')

    def test_words_with_apostrophes(self):
        """测试带撇号的情况"""
        text = "I'm fresh out of ideas"
        result = cap.just_do_it(text)
        self.assertEqual(result, "I'm Fresh Out Of Ideas")


if __name__ == '__main__':
    unittest.main()

```

我们再次运行测试：

```sh
$ python3 test_cap.py
..F
======================================================================
FAIL: test_words_with_apostrophes (__main__.TestCap)
测试带撇号的情况
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_cap.py", line 29, in test_words_with_apostrophes
    self.assertEqual(result, "I'm Fresh Out Of Ideas")
AssertionError: "I'M Fresh Out Of Ideas" != "I'm Fresh Out Of Ideas"
- I'M Fresh Out Of Ideas
?   ^
+ I'm Fresh Out Of Ideas
?   ^


----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=1)
$ 
```

函数把`I'm`中的`m`大写了，查看官方文档也可以看到它默认不处理撇号：

> The algorithm uses a simple language-independent definition of a word as groups of consecutive letters. The definition works in many contexts but it means that apostrophes in contractions and possessives form word boundaries, which may not be the desired result:
>
> ```python
> >>> "they're bill's friends from the UK".title()
> "They'Re Bill'S Friends From The Uk"
> ```

我们应该好好读一下官方文档！

在标准库`string`文档[https://docs.python.org/3/library/string.html#string.capwords](https://docs.python.org/3/library/string.html#string.capwords)的底部有另一个函数，一个名为`capwords()`的辅助函数：

> string.`capwords`(*s*, *sep=None*)
>
> Split the argument into words using [`str.split()`](https://docs.python.org/3/library/stdtypes.html#str.split), capitalize each word using [`str.capitalize()`](https://docs.python.org/3/library/stdtypes.html#str.capitalize), and join the capitalized words using [`str.join()`](https://docs.python.org/3/library/stdtypes.html#str.join). If the optional second argument *sep* is absent or `None`, runs of whitespace characters are replaced by a single space and leading and trailing whitespace are removed, otherwise *sep* is used to split and join the words.

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import string

>>> string.capwords?
Signature: string.capwords(s, sep=None)
Docstring:
capwords(s [,sep]) -> string

Split the argument into words using split, capitalize each
word using capitalize, and join the capitalized words using
join.  If the optional second argument sep is absent or None,
runs of whitespace characters are replaced by a single space
and leading and trailing whitespace are removed, otherwise
sep is used to split and join the words.
File:      /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/string.py
Type:      function

>>> string.capwords("I'm lilei")
"I'm Lilei"
```

初步测试发现使用这个函数好像是对的！

我们试试这个，将cap.py文件修改一下：

```python
from string import capwords
def just_do_it(text):
    # return text.capitalize()
    # return text.title()
    return capwords(text)

```

然后我们再运行一下测试：

```sh
$ python3 test_cap.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
$ 
```

终于3个测试都通过了！但是，这个时候还是有问题，我们向`test_cap.py`中再增加一个测试：

```python
import unittest

import cap


class TestCap(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_one_word(self):
        """测试单个单词的情况"""
        text = 'duck'
        result = cap.just_do_it(text)
        self.assertEqual(result, 'Duck')

    def test_multiple_words(self):
        """测试多个单词的情况"""
        text = 'a veritable flock of ducks'
        result = cap.just_do_it(text)
        self.assertEqual(result, 'A Veritable Flock Of Ducks')

    def test_words_with_apostrophes(self):
        """测试带撇号的情况"""
        text = "I'm fresh out of ideas"
        result = cap.just_do_it(text)
        self.assertEqual(result, "I'm Fresh Out Of Ideas")

    def test_words_with_quotes(self):
        """测试带引号的情况"""
        text = "\"You're despicable,\" said Daffy Duck"
        result = cap.just_do_it(text)
        self.assertEqual(result, "\"You're Despicable,\" Said Daffy Duck")


if __name__ == '__main__':
    unittest.main()

```

此时再测试：

```sh
$ python3 test_cap.py
...F
======================================================================
FAIL: test_words_with_quotes (__main__.TestCap)
测试带引号的情况
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_cap.py", line 35, in test_words_with_quotes
    self.assertEqual(result, "\"You're Despicable,\" Said Daffy Duck")
AssertionError: '"you\'re Despicable," Said Daffy Duck' != '"You\'re Despicable," Said Daffy Duck'
- "you're Despicable," Said Daffy Duck
?  ^
+ "You're Despicable," Said Daffy Duck
?  ^


----------------------------------------------------------------------
Ran 4 tests in 0.001s

FAILED (failures=1)
$ 
```

可以看到第一个双引号并没有被目前为止最好用的函数`capwords`正常处理。它试着把`"`转成大写，并把其他内容转成小写`You're`，此外，字符串中其余部分应该保持不变。

做测试的人可以发现实些边界条件，但是开发者在面对自己的代码时通常有盲区！

`unittest`提供了数量不多但非常有用的断言，你可以用它们检查值、确保类能够匹配、判断是否触发错误，等等！



### 使用`doctest`进行代码测试

我们也可以使用标准库中的`doctest`进行代码测试，可参考[https://docs.python.org/3/library/doctest.html](https://docs.python.org/3/library/doctest.html)。

使用这个包可以将测试写到文档字符串中，也可以起到文档的作用。它看起来有点像交互式解释器，字符`>>>`后面是一个函数调用，下一行是执行结果。你可以在交互式解释器中运行测试并把结果粘贴到测试文件中。

我们修改一下`cap.py`文件(暂时不考虑带引号的情况)。

修改后的`cap.py`内容如下：

```python
from string import capwords


def just_do_it(text):
    """
    >>> just_do_it('duck')
    'Duck'
    >>> just_do_it('a veritable flock of ducks')
    'A Veritable Flock Of Ducks'
    >>> just_do_it("I'm fresh out of ideas")
    "I'm Fresh Out Of Ideas"
    """
    return capwords(text)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

```

运行时，如果测试全部通过不会产生任何输出：

```sh
$ python3 cap.py  
```

加上冗余选项(`-v`)，会输出比较详细的测试结果：

```sh
$ python3 cap.py -v
Trying:
    just_do_it('duck')
Expecting:
    'Duck'
ok
Trying:
    just_do_it('a veritable flock of ducks')
Expecting:
    'A Veritable Flock Of Ducks'
ok
Trying:
    just_do_it("I'm fresh out of ideas")
Expecting:
    "I'm Fresh Out Of Ideas"
ok
1 items had no tests:
    __main__
1 items passed all tests:
   3 tests in __main__.just_do_it
3 tests in 2 items.
3 passed and 0 failed.
Test passed.
$ 
```

如果我们将第一个测试中的`'Duck'`写错，看看输出会怎样，如`'Duck'`改成`'DUCK'`。

```sh
$ python3 cap.py -v
Trying:
    just_do_it('duck')
Expecting:
    'DUCK'
**********************************************************************
File "cap.py", line 6, in __main__.just_do_it
Failed example:
    just_do_it('duck')
Expected:
    'DUCK'
Got:
    'Duck'
Trying:
    just_do_it('a veritable flock of ducks')
Expecting:
    'A Veritable Flock Of Ducks'
ok
Trying:
    just_do_it("I'm fresh out of ideas")
Expecting:
    "I'm Fresh Out Of Ideas"
ok
1 items had no tests:
    __main__
**********************************************************************
1 items had failures:
   1 of   3 in __main__.just_do_it
3 tests in 2 items.
2 passed and 1 failed.
***Test Failed*** 1 failures.
$ 
```

此时可以看到测试失败！

### 使用`nose`进行测试

也可以使用第三方包`nose`进行代码测试。安装包：

```sh
$ pip install nose
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting nose
  Downloading http://mirrors.aliyun.com/pypi/packages/15/d8/dd071918c040f50fa1cf80da16423af51ff8ce4a0f2399b7bf8de45ac3d9/nose-1.3.7-py3-none-any.whl (154 kB)
     |████████████████████████████████| 154 kB 4.2 MB/s
Installing collected packages: nose
Successfully installed nose-1.3.7
```

参考 [https://nose.readthedocs.io/en/latest/](https://nose.readthedocs.io/en/latest/)



我们修改一下之前的`test_cap.py`并保存为`test_cap_nose.py`:

```python
from nose.tools import eq_

import cap


def test_one_word():
    """测试单个单词的情况"""
    text = 'duck'
    result = cap.just_do_it(text)
    eq_(result, 'Duck')


def test_multiple_words():
    """测试多个单词的情况"""
    text = 'a veritable flock of ducks'
    result = cap.just_do_it(text)
    eq_(result, 'A Veritable Flock Of Ducks')


def test_words_with_apostrophes():
    """测试带撇号的情况"""
    text = "I'm fresh out of ideas"
    result = cap.just_do_it(text)
    eq_(result, "I'm Fresh Out Of Ideas")


def test_words_with_quotes():
    """测试带引号的情况"""
    text = "\"You're despicable,\" said Daffy Duck"
    result = cap.just_do_it(text)
    eq_(result, "\"You're Despicable,\" Said Daffy Duck")

```

运行测试：

```sh
$ nosetests --version
nosetests version 1.3.7
$ nosetests test_cap_nose.py 
...F
======================================================================
FAIL: 测试带引号的情况
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/nose/case.py", line 198, in runTest
    self.test(*self.arg)
  File "test_cap_nose.py", line 31, in test_words_with_quotes
    eq_(result, "\"You're Despicable,\" Said Daffy Duck")
AssertionError: '"you\'re Despicable," Said Daffy Duck' != '"You\'re Despicable," Said Daffy Duck'

----------------------------------------------------------------------
Ran 4 tests in 0.002s

FAILED (failures=1)
$ 
```

这和我们使用`unitest`进行测试得到的错误是一样的！

但是在`nose`官网我们可以看到`nose`很久没有人维护了：

> Nose has been in maintenance mode for the past several years and will likely cease without a new person/team to take over maintainership. New projects should consider using [Nose2](https://github.com/nose-devs/nose2), [py.test](http://pytest.org/), or just plain unittest/unittest2.

新的项目推荐使用 `nose2`、 `pytest`等进行代码测试。

我们看一下`nose2`。

官方文档链接 [https://docs.nose2.io/en/latest/](https://docs.nose2.io/en/latest/)。

> `nose2` is the successor to `nose`.
>
> It’s `unittest` with plugins.
>
> `nose2` is a new project and does not support all of the features of `nose`. See [differences](https://nose2.readthedocs.io/en/latest/differences.html) for a thorough rundown.
>
> nose2’s purpose is to extend `unittest` to make testing nicer and easier to understand.
>
> nose2 vs pytest
>
> `nose2` may or may not be a good fit for your project.
>
> If you are new to python testing, we encourage you to also consider [pytest](http://pytest.readthedocs.io/en/latest/), a popular testing framework.



`nose2`继承自`nose`，但是又与`nose`不完全相同，`nose2`是`unittest`单元测试模块的插件，能够扩展单元测试，使测试更好更容易理解。

`nose2`有可能适合或不适合你的项目。如果你不熟悉python测试，建议考虑使用`pytest`测试框架。

我们安装一下`nose2`包：

```sh
$ pip install nose2
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting nose2
  Downloading http://mirrors.aliyun.com/pypi/packages/b9/ad/27561695e863f5df064f1715864afb3ebe723a6e19e875eca85570e0a7cd/nose2-0.9.2-py2.py3-none-any.whl (137 kB)
     |████████████████████████████████| 137 kB 1.2 MB/s
Requirement already satisfied: six>=1.7 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from nose2) (1.14.0)
Requirement already satisfied: coverage>=4.4.1 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from nose2) (5.0.4)
Installing collected packages: nose2
Successfully installed nose2-0.9.2

$ nose2 --help
usage: nose2 [-s START_DIR] [-t TOP_LEVEL_DIRECTORY] [--config [CONFIG]]
             [--no-user-config] [--no-plugins] [--plugin PLUGINS]
             [--exclude-plugin EXCLUDE_PLUGINS] [--verbosity VERBOSITY]
             [--verbose] [--quiet] [--log-level LOG_LEVEL] [-B]
             [--coverage PATH] [--coverage-report TYPE]
             [--coverage-config FILE] [-C] [-D] [-F] [--log-capture]
             [--pretty-assert] [-h]
             [testNames [testNames ...]]

positional arguments:
  testNames

optional arguments:
  -s START_DIR, --start-dir START_DIR
                        Directory to start discovery ('.' default)
  -t TOP_LEVEL_DIRECTORY, --top-level-directory TOP_LEVEL_DIRECTORY, --project-directory TOP_LEVEL_DIRECTORY
                        Top level directory of project (defaults to start dir)
  --config [CONFIG], -c [CONFIG]
                        Config files to load, if they exist. ('unittest.cfg'
                        and 'nose2.cfg' in start directory default)
  --no-user-config      Do not load user config files
  --no-plugins          Do not load any plugins. Warning: nose2 does not do
                        anything if no plugins are loaded
  --plugin PLUGINS      Load this plugin module.
  --exclude-plugin EXCLUDE_PLUGINS
                        Do not load this plugin module
  --verbosity VERBOSITY
                        Set starting verbosity level (int). Applies before -v
                        and -q
  --verbose, -v         Print test case names and statuses. Use multiple '-v's
                        for higher verbosity.
  --quiet, -q           Reduce verbosity. Multiple '-q's result in lower
                        verbosity.
  --log-level LOG_LEVEL
                        Set logging level for message logged to console.
  -h, --help            Show this help message and exit

plugin arguments:
  Command-line arguments added by plugins:

  -B, --output-buffer   Enable output buffer
  --coverage PATH       Measure coverage for filesystem path (multi-allowed)
  --coverage-report TYPE
                        Generate selected reports, available types: term,
                        term-missing, annotate, html, xml (multi-allowed)
  --coverage-config FILE
                        Config file for coverage, default: .coveragerc
  -C, --with-coverage   Turn on coverage reporting
  -D, --debugger        Enter pdb on test fail or error
  -F, --fail-fast       Stop the test run after the first error or failure
  --log-capture         Enable log capture
  --pretty-assert       Add pretty output for "assert" statements
$
```

看官方示例，`nose2`可以直接对`unittest`编写的单元测试进行测试：

```sh
$ nose2 -v
test_multiple_words (test_cap.TestCap)
测试多个单词的情况 ... ok
test_one_word (test_cap.TestCap)
测试单个单词的情况 ... ok
test_words_with_apostrophes (test_cap.TestCap)
测试带撇号的情况 ... ok
test_words_with_quotes (test_cap.TestCap)
测试带引号的情况 ... FAIL
test_cap_nose.transplant_class.<locals>.C (test_multiple_words)
测试多个单词的情况 ... ok
test_cap_nose.transplant_class.<locals>.C (test_one_word)
测试单个单词的情况 ... ok
test_cap_nose.transplant_class.<locals>.C (test_words_with_apostrophes)
测试带撇号的情况 ... ok
test_cap_nose.transplant_class.<locals>.C (test_words_with_quotes)
测试带引号的情况 ... FAIL

======================================================================
FAIL: test_words_with_quotes (test_cap.TestCap)
测试带引号的情况
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_cap.py", line 35, in test_words_with_quotes
    self.assertEqual(result, "\"You're Despicable,\" Said Daffy Duck")
AssertionError: '"you\'re Despicable," Said Daffy Duck' != '"You\'re Despicable," Said Daffy Duck'
- "you're Despicable," Said Daffy Duck
?  ^
+ "You're Despicable," Said Daffy Duck
?  ^


======================================================================
FAIL: test_cap_nose.transplant_class.<locals>.C (test_words_with_quotes)
测试带引号的情况
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_cap_nose.py", line 31, in test_words_with_quotes
    eq_(result, "\"You're Despicable,\" Said Daffy Duck")
AssertionError: '"you\'re Despicable," Said Daffy Duck' != '"You\'re Despicable," Said Daffy Duck'

----------------------------------------------------------------------
Ran 8 tests in 0.001s

FAILED (failures=2)
$ 
```

可以看到`nose2`直接运行了我们前面编写的两个测试文件。并且显示出了异常的位置。



### 使用`pytest`测试代码

`pytest`框架使编写小型测试变得容易，并且可以扩展以支持应用程序和库的复杂功能测试。

`pytest`官方文档 [https://docs.pytest.org/en/latest/](https://docs.pytest.org/en/latest/)。

安装包：

```sh
$ pip install pytest
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Requirement already satisfied: pytest in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (5.4.1)
Requirement already satisfied: more-itertools>=4.0.0 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from pytest) (8.2.0)
Requirement already satisfied: packaging in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from pytest) (20.3)
Requirement already satisfied: attrs>=17.4.0 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from pytest) (19.3.0)
Requirement already satisfied: py>=1.5.0 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from pytest) (1.8.1)
Requirement already satisfied: pluggy<1.0,>=0.12 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from pytest) (0.13.1)
Requirement already satisfied: importlib-metadata>=0.12; python_version < "3.8" in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from pytest) (1.5.2)
Requirement already satisfied: wcwidth in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from pytest) (0.1.8)
Requirement already satisfied: six in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from packaging->pytest) (1.14.0)
Requirement already satisfied: pyparsing>=2.0.2 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from packaging->pytest) (2.4.6)
Requirement already satisfied: zipp>=0.5 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from importlib-metadata>=0.12; python_version < "3.8"->pytest) (3.1.0)
$
```

如果你安装后，使用`pytest --version`查看版本，如果不是最新版本，可以在pypi网站 [https://pypi.org/project/pytest/#files](https://pypi.org/project/pytest/#files)  上面下载最新的版本的源代码进行安装。

查看`pytest`版本：

```sh
$ pytest --version
pytest 6.0.1
```

我们编写`pytest`的测试代码`test_cap_pytest.py`:

```python
import cap


def test_one_word():
    """测试单个单词的情况"""
    text = 'duck'
    result = cap.just_do_it(text)
    assert result == 'Duck'


def test_multiple_words():
    """测试多个单词的情况"""
    text = 'a veritable flock of ducks'
    result = cap.just_do_it(text)
    assert result == 'A Veritable Flock Of Ducks'


def test_words_with_apostrophes():
    """测试带撇号的情况"""
    text = "I'm fresh out of ideas"
    result = cap.just_do_it(text)
    assert result == "I'm Fresh Out Of Ideas"


def test_words_with_quotes():
    """测试带引号的情况"""
    text = "\"You're despicable,\" said Daffy Duck"
    result = cap.just_do_it(text)
    assert result == "\"You're Despicable,\" Said Daffy Duck"

```

然后我们运行测试：

```sh
$ pytest test_cap_pytest.py 
/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pytest-6.0.1-py3.6.egg/_pytest/compat.py:340: PytestDeprecationWarning: The TerminalReporter.writer attribute is deprecated, use TerminalReporter._tw instead at your own risk.
See https://docs.pytest.org/en/stable/deprecations.html#terminalreporter-writer for more information.
  return getattr(object, name, default)
=============================== test session starts ===============================
platform darwin -- Python 3.6.8, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
rootdir: ~
plugins: xonsh-0.9.15
collected 4 items                                                                 

test_cap_pytest.py ...F                                                     [100%]

==================================== FAILURES =====================================
_____________________________ test_words_with_quotes ______________________________

    def test_words_with_quotes():
        """测试带引号的情况"""
        text = "\"You're despicable,\" said Daffy Duck"
        result = cap.just_do_it(text)
>       assert result == "\"You're Despicable,\" Said Daffy Duck"
E       assert '"you\'re Des...id Daffy Duck' == '"You\'re Des...id Daffy Duck'
E         - "You're Despicable," Said Daffy Duck
E         ?  ^
E         + "you're Despicable," Said Daffy Duck
E         ?  ^

test_cap_pytest.py:29: AssertionError
============================= short test summary info =============================
FAILED test_cap_pytest.py::test_words_with_quotes - assert '"you\'re Des...id Da...
=========================== 1 failed, 3 passed in 0.13s ===========================
$
```

可以看到`pytest`只需要使用`assert`断言来进行测试即可。更详细的例子请参考官方文档 [https://docs.pytest.org/en/latest/](https://docs.pytest.org/en/latest/)。



## 持续集成

当你的团队每天会产生很多代码时，就需要在出现改动时进行自动测试。你可以让源码控制系统，在提交代码时进行自动化的测试。这样每个人都知道是谁破坏了构建并消失在叫饭的人群中。

你可以了解一下以下系统：

- Jenkins [https://www.jenkins.io/](https://www.jenkins.io/)  Jenkins是一个开源软件项目，是基于Java开发的一种持续集成工具，用于监控持续重复的工作，旨在提供一个开放易用的软件平台，使软件的持续集成变成可能。
- Travis-ci [https://travis-ci.org/](https://travis-ci.org/) Travis CI 是目前新兴的开源持续集成构建项目，它与jenkins，GO的很明显的区别在于采用yaml格式，简洁清新独树一帜。目前大多数的github项目都已经移入到Travis CI的构建队列中，据说Travis CI每天运行超过4000次完整构建。对开源项目是免费的！



## 调试Python代码

> 调试的难度是写代码的两倍。以此类推，如果你绞尽脑汁编写巧妙的代码，那你一定无法调试它。   ——Brian Kernighan

测试在先，测试越完善，之后需要修复的bug越少。不过，bug总是无法避免的，发现bug就要去修复它。之前就说过，Python中最简单的调试方法就是打印字符串。`var()`是非常有用的一个函数，可以提取本地变量的值，包括函数参数。

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> def func(*args, **kwargs):
...     print(vars())
...

>>> func(1, 2, 3)
{'kwargs': {}, 'args': (1, 2, 3)}

>>> func(['a', 'b', 'argh'])
{'kwargs': {}, 'args': (['a', 'b', 'argh'],)}

>>> func(['a', 'b', 'c'], key='test')
{'kwargs': {'key': 'test'}, 'args': (['a', 'b', 'c'],)}
```

书中也提到使用装饰器来调试代码，但感觉有点麻烦。

我常用的调试方法包括：

- 使用`print`打印变量。
- 使用`logging`模块( [https://docs.python.org/3.6/library/logging.html](https://docs.python.org/3.6/library/logging.html) )保存日志到文件中，查看日志调试。

一般来说，编写简单代码时就用`print`足够了，但如果是在生产环境下的代码，建议使用`logging`模块保存日志到文件，便于异常时调试。

## 使用pdb调试代码

上面的技能很有用，但仍然无法代替真正的调试器。大多数IDE都带有调试器，有各种各样的特性和用户界面（PyCharm非常不错，你可以试一下！）。这里，我们介绍标准的Python调试器`pdb`，参考 [https://docs.python.org/3/library/pdb.html](https://docs.python.org/3/library/pdb.html)

`pdb`是Python Debugger。



我们简单的使用一下`pdb`模块来调试代码。

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

# 定义一个函数，打印某个未定义的变量
>>> def test():
...     print(i)
...

>>> import pdb

# 调试代码
>>> pdb.run('')
> <string>(1)<module>()
(Pdb) test()
*** NameError: name 'i' is not defined
(Pdb) ?

Documented commands (type help <topic>):
========================================
EOF    c          d        h         list      q        rv       undisplay
a      cl         debug    help      ll        quit     s        unt
alias  clear      disable  ignore    longlist  r        source   until
args   commands   display  interact  n         restart  step     up
b      condition  down     j         next      return   tbreak   w
break  cont       enable   jump      p         retval   u        whatis
bt     continue   exit     l         pp        run      unalias  where

Miscellaneous help topics:
==========================
exec  pdb

(Pdb)

# 获取帮助信息
(Pdb) help s
s(tep)
        Execute the current line, stop at the first possible occasion
        (either in a function that is called or in the current
        function).
(Pdb) help n
n(ext)
        Continue execution until the next line in the current function
        is reached or it returns.
(Pdb)
(Pdb) help b
b(reak) [ ([filename:]lineno | function) [, condition] ]
        Without argument, list all breaks.

        With a line number argument, set a break at this line in the
        current file.  With a function name, set a break at the first
        executable line of that function.  If a second argument is
        present, it is a string specifying an expression which must
        evaluate to true before the breakpoint is honored.

        The line number may be prefixed with a filename and a colon,
        to specify a breakpoint in another file (probably one that
        hasn't been loaded yet).  The file is searched for on
        sys.path; the .py suffix may be omitted.
(Pdb) exit
>>>                                                  
```

可以看到调试时就可以知道变量`i`是未定义的。

- `s`是单步执行，会进入到函数内部并继续单步执行。
- `n`也可以单步执行，但不会进入函数，如果遇到一个函数，`n`会执行整个函数并前进到下一行代码。
- 不确定问题在哪时使用`s`，确定问题不在函数中时使用`n`，函数很长时尤其有用。
- `b`可以在指定行设置断点。
- `c`继续。

此处仅简单的使用一下`pdb`，详细可了解官方文档 [https://docs.python.org/3/library/pdb.html](https://docs.python.org/3/library/pdb.html) 。

## 记录错误日志

有时候，你需要使用比`print()`更高端的工具来记录日志。日志通常是系统中的一个文件，用于持续记录信息。信息中通常会包含很多有用的内容，比如时间戳或者运行程序的用户的名字。通常来说，日志每天会被放置(重命名)并压缩，这样它们就不会占用太多磁盘空间。如果程序出错，你可以查看对应的日志文件来了解发生了什么。异常信息非常重要，因为它们会告诉你出错的行数和原因。

使用标准库`logging`模块来记录日志，参考 [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html) 。

下面是`logging`模块的简单使用。

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import logging as logger

>>> logger.debug('testing')

>>> logger.info('info')

>>> logger.warning('Booming')
WARNING:root:Booming

>>> logger.error('Error')
ERROR:root:Error

>>> logger.critical('Critical')
CRITICAL:root:Critical

>>>
```

将日志保存到文件中：

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import logging

>>> logging.basicConfig(level='INFO', filename='log.txt')

>>> logger = logging.getLogger('mylog')

>>> logger.debug('debug log')

>>> logger.info('info log')

>>> logger.warning('warning log')
```

查看文件`log.txt`内容：

```sh
$ cat log.txt
DEBUG:mylog:debug log
INFO:mylog:info log
WARNING:mylog:warning log
```



具体使用可参考官方文档 [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html) 。

或者参考 [Python logging模块-记录错误日志](./X_logging.html)。



## 优化代码

一般来说，Python代码已经足够快了，直到它不够快的那一时刻之前。大多数情况下，你都可以使用更好的算法或者数据结构来加速，关键是知道把这些技巧用在哪里。即使经验丰富的程序员也常常会犯错误，你需要像裁缝一样耐心，在裁剪之前认真测量。

### 测量时间

可以使用`time`模块或`timeit`模块来测试你的代码运行的时间。

- 使用`time`模块时，在代码运行前获取一下时间戳，然后再运行你的代码，然后再次获取时间戳，最后用两个时间戳相减就获取到你的代码运行时间了。

我们把代码保存到`time1.py`中，注意，不要保存到`time.py`文件中。

```python
# filename: time1.py

from time import time

before = time()
num = 5
num *= 2
after = time()
print(after - before)
```

然后多次运行它：

```sh
$ python3 time1.py 
9.5367431640625e-07
$ python3 time1.py
1.1920928955078125e-06
$ python3 time1.py
1.1920928955078125e-06
$ python3 time1.py
1.1920928955078125e-06
$ python3 time1.py
9.5367431640625e-07
$ python3 time1.py
1.1920928955078125e-06
$ python3 time1.py
1.1920928955078125e-06
$ python3 time1.py
7.152557373046875e-07
$ 
```

可以看到运行时间很短。

- 使用`timeit`模块更简单，其中的`timeit`函数会运行你的测试代码count次，并打印结果。具体可参考 [日期和时间模块-`timeit`程序运行时间统计模块](./X_time_and_date_module_timeit.html)， `timeit()`的调用形式为`timeit(code, number)`。

```python
# filename: timeit1.py

from timeit import timeit

print(timeit('num = 5; num *=2', number=1))
```

现在我们运行`timeit1.py`:

```sh
$ python3 timeit1.py
1.5389960026368499e-06
$ python3 timeit1.py
8.919887477532029e-07
$ python3 timeit1.py
9.880022844299674e-07
$ python3 timeit1.py
9.450013749301434e-07
$ python3 timeit1.py
1.1269876267760992e-06
$ python3 timeit1.py
8.680071914568543e-07
```





### 算法和数据结构

Python之禅提到，应该有一种，最好只有一种，明显的解决办法。不幸的是，有时候并没有那么明显，你需要比较各种方案。举例来说，如果要构建一个列表，使用`for`循环好还是列表解析好？我们如何定义更好？是更快、更容易理解、占用内存更好还是更具Python风格？

我们在下面的示例中，使用不同的方式构建列表，比较速度、可读性和Python风格。



`time_lists.py`源码如下：

```python
# filename: time_lists.py

from timeit import timeit


def make_list_1():
    result = []
    for value in range(1000):
        result.append(value)
    return result


def make_list_2():
    result = [value for value in range(1000)]
    return result


print('make_list_1 takes', timeit(make_list_1, number=1000), 'seconds')
print('make_list_2 takes', timeit(make_list_2, number=1000), 'seconds')
```

代码中我们创建一个列表，向列表中添加1000个元素，使用`timeit`分别调用1000次。我们运行一下程序：

```sh
$ python3 time_lists.py
make_list_1 takes 0.10264219999953639 seconds
make_list_2 takes 0.04438292399936472 seconds
```

可以看到列表解析至少比用`append()`添加元素快两倍。

- 通常来说，列表解析要比手动添加快，可以使用这个方法来加速你的代码。

### Cython、NumPy和C扩展

如果你已经尽了最大的努力仍然无法达到想要的速度，还有一些方法可以选择。

Cpython混合了Python和C，它的设计目的是把带有性能注释的Python代码翻译成C代码。这些注释非常简单，比如声明一些变量，函数参数或者函数返回值的类型。对于科学上的数字运算循环来说，添加这些注释之后会让程序快很多，速度能达到之前的1000倍。可以在Cpython wiki查看文档和示例。

- Cython官网 [https://cython.org/](https://cython.org/)
- Cython官方文档 [https://cython.readthedocs.io/en/latest/](https://cython.readthedocs.io/en/latest/)
- Cython wiki [https://github.com/cython/cython/wiki](https://github.com/cython/cython/wiki)

NumPy是Python的一个数学库，它是用C语言编写的，运行速度很快。

- NumPy官网 [https://numpy.org/](https://numpy.org/)
- NumPy官方文档 [https://numpy.org/doc/stable/](https://numpy.org/doc/stable/)

为了提高性能并且方便使用，Python的很多代码和标准库都是用C写成并用Python进行封装。这些钩子可以直接在你的程序中使用，如果你熟悉C和Python并且真的想提高程序性能，可以写一个C扩展，这样做难度很大但是效果很好。

### PyPy

Java刚出现时，速度非常的慢，Sun投入了大量的资金来优化Java的解释器和底层的Java虚拟机（JVM）。Python不属于任何人，因此没有投入这么多努力来提高它的速度。你使用的很可能是标准的Python实现。它是由C写成，通常被称为CPython，注意，与Cython不一样！

和PHP/Perl甚至Java一样，Python并不会被编译成机器语言，而是被翻译成中间语言(通常被称为字节码)，然后在虚拟机解释执行。

PyPy是一个新出现的Python解释器，实现了许多Java中的加速技术。它的基准测试显示PyPy几乎完全超越了CPython，平均快6倍，最高快20倍，它支持Python2和Python3，你可以下载并用它代替CPython。PyPy在不断的改进。

- PyPy官网 [https://www.pypy.org/](https://www.pypy.org/)
- PyPy官方文档 [https://doc.pypy.org/en/latest/index.html](https://doc.pypy.org/en/latest/index.html)

> "If you want your code to run faster, you should probably just use PyPy."
>                                       -- Guido van Rossum (creator of Python)



## 源码控制

如果你和其他开发者在一个团队工作，源码控制就变得极其重要！

比较好用的版本控制系统：

- `Git`
- `Subversion`

两个版本控制系统都有很多命令，此处忽略不提。



## Python的艺术

人们会在不同的场合、不同的领域借助Python进行一些探索。

### 2D图形

几乎所有的计算机编程语言或多或少都会被应用到图形处理中。出于效率考虑，大多都会使用C或C++编写平台软件，也会用Python来扩展其功能。

标准库中有图形相关的库并不多：

- imghdr, 这个模块用于检测图片文件的文件格式。
- colorsys， 这个模块用于在不同的颜色系统间进行转换。 

为了在Python中对图片进行更高级的处理，我们需要安装一些第三方包。

#### PIL和Pillow

PIL是Python 图片库(Python Image Library)，并不属于Python的标准库，无法使用pip安装。有人创建了一个友好的项目分支Pillow,其向后兼容PIL,并且文档更加规范。

- Pillow官网地址 [https://python-pillow.org/](https://python-pillow.org/)

- Pillow Pypi [https://pypi.org/project/Pillow/](https://pypi.org/project/Pillow/)
- Pillow官方文档 [https://pillow.readthedocs.io/en/stable/](https://pillow.readthedocs.io/en/stable/)

安装：

```sh
$ pip install pillow
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting pillow
  Downloading http://mirrors.aliyun.com/pypi/packages/04/8f/c42f534b73680f501858a8c7171705a55c7347c86419b74fa585370c8306/Pillow-7.2.0-cp36-cp36m-macosx_10_10_x86_64.whl (2.2 MB)
     |████████████████████████████████| 2.2 MB 8.6 MB/s 
Installing collected packages: pillow
Successfully installed pillow-7.2.0
```



简单的使用：

```sh
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> from PIL import Image                                                       

>>> img = Image.open('image.png')                                            

>>> img.format                                                                  
'JPEG'

>>> img.size                                                                    
(408, 612)

>>> img.mode                                                                    
'RGB'
```

可以参考官方文档查看更多示例。

### 图形用户界面

GUI是图形用户界面，虽然包括图形这个词，但它的重点更在于用户界面(展示数据用的小控件、输入的方法、菜单、按钮以及包含所有这些的窗口等)上。Tkinter是内置的图形用户界面库，它的功能不多，但可以在所有平台上创建符合接近原生界面的窗口和控件。

- GUI编程FAQ页面 [https://docs.python.org/3/faq/gui.html](https://docs.python.org/3/faq/gui.html)
- GUI Programming in Python [https://wiki.python.org/moin/GuiProgramming](https://wiki.python.org/moin/GuiProgramming)



下面是一个极简的Tkinter程序，它可以在新建窗口中显示图片：

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import tkinter

>>> from PIL import Image, ImageTk

>>> main = tkinter.Tk()

>>> img = Image.open('image.jpg')

>>> tkimg = ImageTk.PhotoImage(img)

>>> tkinter.Label(main, image=tkimg).pack()

>>> main.mainloop()
```

想要关闭窗口的话只需要点击图片上方的关闭按钮或者关闭Python解释器即可。



#### Qt

Qt是一款专业级GUI及应用工具包。Qt有两个主要的Python库版本，PySide(免费)和PyQt（开发的代码必须要开源，商用的话需要买许可license）。



Pyside2支持Qt5,Pyside不支持Qt5,因此需要支持Qt5以上版本的话，需要使用`pip install PySide2`来安装Pyside2.

- Pyside2 pypi [https://pypi.org/project/PySide2/](https://pypi.org/project/PySide2/)
- Qt for python 文档 [https://doc.qt.io/qtforpython/](https://doc.qt.io/qtforpython/)



### 3D图形与动画

如果你喜欢探索Python,喜欢3D、动画、多媒体以及游戏的话，应该试试Panda3D，它开源免费。

- Panda3D网站 [https://www.panda3d.org/](https://www.panda3d.org/)
- Panda3d pypi [https://pypi.org/project/Panda3D/](https://pypi.org/project/Panda3D/)
- 文档 [https://docs.panda3d.org/1.10/python/index](https://docs.panda3d.org/1.10/python/index)

- 安装方法 `pip install Panda3D`

简单使用，使用Panda3d加载草木风景：

```python
from direct.showbase.ShowBase import ShowBase


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)


app = MyApp()
app.run()
```

运行程序会显示出风景3d图。



使用下面的程序，可以看到大熊猫在草地上原地行走：

```python
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()
```

更多请参考官方示例。



### 平面图、曲线图和可视化

Python是目前绘制平面图、曲线图以及进行数据可视化的最佳解决方法。它在科学研究中尤其受到欢迎。

#### matplotlib

Matplotlib是一个综合库，用于在Python中创建静态、动画和交互式可视化。

- 官网 [https://matplotlib.org/](https://matplotlib.org/)
- 官方文档 [https://matplotlib.org/users/index.html](https://matplotlib.org/users/index.html)
- matplotlib运行在服务器端。

安装：

```sh
$ pip install matplotlib
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting matplotlib
  Downloading http://mirrors.aliyun.com/pypi/packages/bc/05/38de828456fe962885c2577d5519fcec50f8e1537a3b58839eccff34eb38/matplotlib-3.3.1-cp36-cp36m-macosx_10_9_x86_64.whl (8.5 MB)
     |████████████████████████████████| 8.5 MB 6.6 MB/s
Collecting cycler>=0.10
  Downloading http://mirrors.aliyun.com/pypi/packages/f7/d2/e07d3ebb2bd7af696440ce7e754c59dd546ffe1bbe732c8ab68b9c834e61/cycler-0.10.0-py2.py3-none-any.whl (6.5 kB)
Requirement already satisfied: pyparsing!=2.0.4,!=2.1.2,!=2.1.6,>=2.0.3 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from matplotlib) (2.4.6)
Requirement already satisfied: python-dateutil>=2.1 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from matplotlib) (2.8.1)
Collecting kiwisolver>=1.0.1
  Downloading http://mirrors.aliyun.com/pypi/packages/06/b2/f7e88efd6323df9ae604f1ff35c629f266d4f424f2a244a7e1d5560c5d96/kiwisolver-1.2.0-cp36-cp36m-macosx_10_9_x86_64.whl (60 kB)
     |████████████████████████████████| 60 kB 6.4 MB/s
Collecting certifi>=2020.06.20
  Downloading http://mirrors.aliyun.com/pypi/packages/5e/c4/6c4fe722df5343c33226f0b4e0bb042e4dc13483228b4718baf286f86d87/certifi-2020.6.20-py2.py3-none-any.whl (156 kB)
     |████████████████████████████████| 156 kB 11.6 MB/s
Requirement already satisfied: pillow>=6.2.0 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from matplotlib) (7.2.0)
Collecting numpy>=1.15
  Downloading http://mirrors.aliyun.com/pypi/packages/28/be/b354ebde8ae4e46972cb9ee6ac6e7c178adffcc6d52e5e20b1b9077be056/numpy-1.19.1-cp36-cp36m-macosx_10_9_x86_64.whl (15.3 MB)
     |████████████████████████████████| 15.3 MB 11.9 MB/s
Requirement already satisfied: six in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from cycler>=0.10->matplotlib) (1.14.0)
Installing collected packages: cycler, kiwisolver, certifi, numpy, matplotlib
  Attempting uninstall: certifi
    Found existing installation: certifi 2020.4.5.1
    Uninstalling certifi-2020.4.5.1:
      Successfully uninstalled certifi-2020.4.5.1
Successfully installed certifi-2020.6.20 cycler-0.10.0 kiwisolver-1.2.0 matplotlib-3.3.1 numpy-1.19.1
$
```

示例，可以参考官方文档 [https://matplotlib.org/tutorials/introductory/usage.html#usage-guide](https://matplotlib.org/tutorials/introductory/usage.html#usage-guide)

#### bokeh

bokeh能有效地将python与JavaScript结合起来。它致力于大数据集的快速可视化。

- 官网 [https://bokeh.org/](https://bokeh.org/)
- 官方文档 [https://docs.bokeh.org/en/latest/docs/user_guide/quickstart.html#userguide-quickstart](https://docs.bokeh.org/en/latest/docs/user_guide/quickstart.html#userguide-quickstart)
- bokeh主要在浏览器上运行，它可以充分利用最近客户端能力的提升。
- 安装`pip install bokeh`。

```python
from bokeh.plotting import figure, output_file, show

# prepare some data
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

# output to static HTML file
output_file("lines.html")

# create a new plot with a title and axis labels
p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

# add a line renderer with legend and line thickness
p.line(x, y, legend_label="Temp.", line_width=2)

# show the results
show(p)
```

当你运行以上代码，将会自动打开浏览器，并访问`lines.html`页面，页面中有绘制的图像。

更多请参考官方示例。





