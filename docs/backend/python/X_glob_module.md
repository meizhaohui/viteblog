# 模块-glob模块


[[toc]]

## glob模块基本介绍


- `glob`是python自带的一个操作文件的相关模块。
-  `glob`模块使用Unix Shell的规则来匹配文件或文件夹目录，而不是更复杂的正则表达式。
-  `*`星号会匹配任意名称（re正则中是`.*`）。
-  `?`问号会匹配一个字符。
-  `[abc]`会匹配字符`a`、`b`和`c`。
-  `[!abc]`会匹配除了字符`a`、`b`和`c`之外的所有字符。


```py
[root@ea4bbe1c189d /]# python3
Python 3.6.7 (default, Dec  5 2018, 15:02:05)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import glob
>>> glob.
glob.escape(            glob.glob0(             glob.iglob(             glob.os
glob.fnmatch            glob.glob1(             glob.magic_check        glob.re
glob.glob(              glob.has_magic(         glob.magic_check_bytes
```


## glob的使用

```py
[root@ea4bbe1c189d /]# python3
Python 3.6.7 (default, Dec  5 2018, 15:02:05)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import glob
>>> import os
```

### 查看根目录下面存在的目录或文件

```py
>>> os.listdir()
['home', 'sbin', 'sys', 'lib', 'media', 'etc', 'srv', 'usr', 'tmp', 'mnt', 'lib64', 'run', 'proc', 'dev', 'var', 'opt', 'anaconda-post.log', 'bin', 'root', '.dockerenv', 'boot']
```

### 获取以`lib`开头的文件和目录

```py
>>> glob.glob('lib*')
['lib', 'lib64']
```

### 获取以`bin`结尾的文件和目录

```py
>>> glob.glob('*bin')
['sbin', 'bin']
```

### 获取所有名称为5个字符的文件和目录

```py
>>> glob.glob('?????')
['media', 'lib64']
```

### 获取所有名称为3个字符的文件和目录

```py
>>> glob.glob('???')
['sys', 'lib', 'etc', 'srv', 'usr', 'tmp', 'mnt', 'run', 'dev', 'var', 'opt', 'bin']
```

### 获取所有名称以指定字符开头的文件和目录

```py
# 以a开头的文件或目录
>>> glob.glob('[a]*')
['anaconda-post.log']
# 以a或者b开头的文件或目录
>>> glob.glob('[ab]*')
['anaconda-post.log', 'bin', 'boot']
# 以a或者b或者c开头的文件或目录
>>> glob.glob('[abc]*')
['anaconda-post.log', 'bin', 'boot']
# 以a或者b或者c或者d开头的文件或目录
>>> glob.glob('[abcd]*')
['dev', 'anaconda-post.log', 'bin', 'boot']
```

### 获取所有名称不是以指定字符开头的文件和目录

```py
# 不是以a或者b或者d开头的文件或目录
>>> glob.glob('[!abd]*')
['home', 'sbin', 'sys', 'lib', 'media', 'etc', 'srv', 'usr', 'tmp', 'mnt', 'lib64', 'run', 'proc', 'var', 'opt', 'root']
# 不是以a或者b或者d或者e开头的文件或目录
>>> glob.glob('[!abde]*')
['home', 'sbin', 'sys', 'lib', 'media', 'srv', 'usr', 'tmp', 'mnt', 'lib64', 'run', 'proc', 'var', 'opt', 'root']
# 不是以a或者b或者d或者e或者h开头的文件或目录
>>> glob.glob('[!abdeh]*')
['sbin', 'sys', 'lib', 'media', 'srv', 'usr', 'tmp', 'mnt', 'lib64', 'run', 'proc', 'var', 'opt', 'root']
# 不是以a或者b或者d或者e或者h或者l开头的文件或目录
>>> glob.glob('[!abdehl]*')
['sbin', 'sys', 'media', 'srv', 'usr', 'tmp', 'mnt', 'run', 'proc', 'var', 'opt', 'root']
# 不是以a或者b或者d或者e或者h或者l或者r开头的文件或目录
>>> glob.glob('[!abdehlr]*')
['sbin', 'sys', 'media', 'srv', 'usr', 'tmp', 'mnt', 'proc', 'var', 'opt']
# 不是以a或者b或者d或者e或者h或者l或者r或者s开头的文件或目录
>>> glob.glob('[!abdehlrs]*')
['media', 'usr', 'tmp', 'mnt', 'proc', 'var', 'opt']
```

### 获取所有名称以指定字符开头或结尾的文件和目录

```py
# 获取以o或者t开头，并且以p或者t结尾的文件和目录
>>> glob.glob('[ot]*[pt]')
['tmp', 'opt']
```

### 匹配以数字结尾的文件和目录

```py
>>> glob.glob('*[0-9]')
['lib64']
```

### 匹配以点号开头的隐藏的文件和目录

```py
>>> glob.glob('.*')
['.dockerenv']
>>> glob.glob('*')
['home', 'sbin', 'sys', 'lib', 'media', 'etc', 'srv', 'usr', 'tmp', 'mnt', 'lib64', 'run', 'proc', 'dev', 'var', 'opt', 'anaconda-post.log', 'bin', 'root', 'boot']
```

::: tip 注意
直接使用星号不能匹配到隐藏文件！
:::


### 使用`glob.iglob`迭代器

返回迭代器(`iterator`)，一次产生一个匹配结果，不需要存储所有的匹配值。

```py
>>> for file in glob.iglob('*'):
...     print(file)
...
home
sbin
sys
lib
media
etc
srv
usr
tmp
mnt
lib64
run
proc
dev
var
opt
anaconda-post.log
bin
root
boot
```


### 查找shell脚本文件

```py
# 查找所有的.sh脚本
>>> glob.glob('./*/*.sh')
['./bin/setup-nsssysinit.sh', './bin/lesspipe.sh', './root/centos7_start_config.sh']
```

### 查找python脚本文件

```py
>>> glob.glob('./*/*.py')
[]
```

### 查找配置文件

```py
>>> glob.glob('./*/*.conf')
['./etc/dracut.conf', './etc/yum.conf', './etc/ld.so.conf', './etc/libuser.conf', './etc/libaudit.conf', './etc/krb5.conf', './etc/vconsole.conf', './etc/host.conf', './etc/nsswitch.conf', './etc/locale.conf', './etc/resolv.conf', './etc/rsyncd.conf', './etc/safe-rm.conf', './etc/sysctl.conf']
```

### 递归查找文件

通过指定`recursive=True`可以进行递归查找，模式`**`将匹配任何文件以及零个或多个目录，子目录和目录的符号链接。

```py
>>> for conf in glob.iglob('./tmp/**', recursive=True):
...     print(conf)
...
./tmp/
./tmp/yum.log
./tmp/ks-script-eC059Y
>>> for conf in glob.iglob('./home/**', recursive=True):
...     print(conf)
...
./home/
>>> for conf in glob.iglob('./etc/**', recursive=True):
...     print(conf)
...
./etc/
./etc/profile
./etc/DIR_COLORS.lightbgcolor
./etc/yum.repos.d
...省略
```

::: warning 注意
在大型目录树中使用`**`模式可能会花费大量时间。此时建议使用`glob.iglob`的形式返回迭代器。
:::

参考：

- [glob — Unix style pathname pattern expansion](https://docs.python.org/3.8/library/glob.html#module-glob)
