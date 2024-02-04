# 程序和进程

[[toc]]

当运行一个`程序`时，操作系统会创建一个`进程`。它会使用系统资源（如CPU、内存和磁盘空间）和操作系统内核中的数据结构（文件、网络连接、用量统计等）。进程之间是互相隔离的，即一个进程无法访问其他进程的内容，也无法操作其他进程。

操作系统会跟踪所有正在运行的进程，给每个进程一小段运行时间，然后切换到其他进程，这样既可以做到俊平又可以响应用户操作。

标准库`os`模块提供了一些常用的获取系统信息的函数。

## 获取正在运行的Python解释器的进程号、用户ID和用户组ID

```py
$ python3
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
# 获取进程ID
>>> os.getpid()
34294

# 获取组ID
>>> os.getgid()
20

# 获取用户ID
>>> os.getuid()
503
```

## 使用`subprocess`创建进程

`subprocess`允许你创建一个新的进程，连接到它们的`input`/`output`/`error`管道(即标准输入、标准输出、标准错误)，并获取它们的返回码。`subprocess`模块的目录是替换掉旧的模块和方法，如`os.system`和`os.spawn`。

在Python 3.5之后的版本中，官方推荐使用`subprocess.run()`函数来使用`subprocess`模块的功能。

我一般都使用Python 3.6的版本。

### subprocess.run函数运行指定的命令

`subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, env=None)`

参数说明：

- `args`，要执行的shell命令，默认是一个字符串序列，如`['df', '-h']`或者`('df', '-h')`，如果仅使用字符串，如`df -h`，则需要将`shell=True`开关打开。
- `shell`，如果`shell=True`，那么指定的命令将通过`shell`执行。如果我们需要访问某些`shell`的特性，如管道、文件名通配符、环境变量扩展功能，`~`将会指代用户家目录。当然，python本身也提供了许多类似shell的特性的实现，如`glob`、`fnmatch`、`os.walk()`、`os.path.expandvars()`、`os.expanduser()`和`shutil`等。
- `check`，是否进行异常检查，如果`check=true`，并且进程以非零退出代码退出，则将引发`CalledProcessError`异常。 该异常的属性包含参数、退出代码以及`stdout`和`stderr`（如果已捕获）。
- `cwd`，设置子进程的当前工作目录，`cwd=None`表示继承自父进程的。
- `env`，设置子进程的环境变量，`env=None`表示继承自父进程的，指定`env`时，需要使用环境变量的映射关系，如使用字典定义环境变量。
- `timeout`，设置命令超时时间(单位：秒)， `timeout=None`默认不设置超时。如果命令执行时间超时，子进程将被杀死，并弹出`TimeoutExpired`异常。
-  `input`，设置子进程输入参数，需要设置为字节序列(byte sequence)。如果设置了`encoding`/`errors`/`universal_newlines`参数的话，则`input`参数需要设置为字符串，内部的`Popen`对象会自动创建`stdin=PIPE`，此时就不能同时使用`stdin`参数。
-  `stdin`,`stdout`,`stderr`，设置子进程的标准输入、标准输出、标准错误，它们的取值可以是`subprocess.PIPE`、`subprocess.DEVNULL`、一个已经存在的文件描述符、已经打开的文件对象或者`None`。`subprocess.PIPE`表示为子进程创建新的管道，`subprocess.DEVNULL`表示使用`os.devnull`，默认使用的是`None`，表示什么都不做，即不捕获子进程的标准输入、标准输出和标准错误。如果使用`stderr=subprocess.STDOUT`，`stderr`将会合并到`stdout`标准输出里一起输出。 
- `encoding`， 设置编码格式，默认情况下`encoding=None`，此时程序会以二进制模式打开标准输入、标准输出和标准错误；当设置了`encoding`参数时，会以文本模式打开标准输入、标准输出和标准错误。

### subprocess的使用

#### 指定`shell`参数，使用`shell`执行子进程命令

```py
[root@ea4bbe1c189d /]# python3
Python 3.6.7 (default, Dec  5 2018, 15:02:05)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import subprocess
>>> subprocess.
subprocess.CalledProcessError(  subprocess.call(                subprocess.run(
subprocess.CompletedProcess(    subprocess.check_call(          subprocess.select
subprocess.DEVNULL              subprocess.check_output(        subprocess.selectors
subprocess.PIPE                 subprocess.errno                subprocess.signal
subprocess.Popen(               subprocess.getoutput(           subprocess.sys
subprocess.STDOUT               subprocess.getstatusoutput(     subprocess.threading
subprocess.SubprocessError(     subprocess.io                   subprocess.time
subprocess.TimeoutExpired(      subprocess.list2cmdline(        subprocess.warnings
subprocess.builtins             subprocess.os
>>> 

# 运行字符串列表序列命令
>>> subprocess.run(['df', '-h'])
Filesystem      Size  Used Avail Use% Mounted on
overlay          59G  2.8G   53G   5% /
tmpfs            64M     0   64M   0% /dev
tmpfs           995M     0  995M   0% /sys/fs/cgroup
shm              64M     0   64M   0% /dev/shm
/dev/sda1        59G  2.8G   53G   5% /etc/hosts
tmpfs           995M     0  995M   0% /proc/acpi
tmpfs           995M     0  995M   0% /sys/firmware
CompletedProcess(args=['df', '-h'], returncode=0)

# 运行字符串元组序列命令
>>> subprocess.run(('df', '-h'))
Filesystem      Size  Used Avail Use% Mounted on
overlay          59G  2.8G   53G   5% /
tmpfs            64M     0   64M   0% /dev
tmpfs           995M     0  995M   0% /sys/fs/cgroup
shm              64M     0   64M   0% /dev/shm
/dev/sda1        59G  2.8G   53G   5% /etc/hosts
tmpfs           995M     0  995M   0% /proc/acpi
tmpfs           995M     0  995M   0% /sys/firmware
CompletedProcess(args=('df', '-h'), returncode=0)

# 运行字符串命令
>>> subprocess.run('df -h', shell=True)
Filesystem      Size  Used Avail Use% Mounted on
overlay          59G  2.8G   53G   5% /
tmpfs            64M     0   64M   0% /dev
tmpfs           995M     0  995M   0% /sys/fs/cgroup
shm              64M     0   64M   0% /dev/shm
/dev/sda1        59G  2.8G   53G   5% /etc/hosts
tmpfs           995M     0  995M   0% /proc/acpi
tmpfs           995M     0  995M   0% /sys/firmware
CompletedProcess(args='df -h', returncode=0)

# 运行ping命令检查是否可以联网
>>> subprocess.run(['ping', '-c', '3', 'baidu.com'])
PING baidu.com (39.156.69.79) 56(84) bytes of data.
64 bytes from 39.156.69.79 (39.156.69.79): icmp_seq=1 ttl=37 time=40.3 ms
64 bytes from 39.156.69.79 (39.156.69.79): icmp_seq=2 ttl=37 time=26.8 ms
64 bytes from 39.156.69.79 (39.156.69.79): icmp_seq=3 ttl=37 time=27.9 ms

--- baidu.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2008ms
rtt min/avg/max/mdev = 26.839/31.708/40.316/6.107 ms
CompletedProcess(args=['ping', '-c', '3', 'baidu.com'], returncode=0)
```

#### `cwd`指定子进程的工作目录

```py
>>> import subprocess

# 继承父进程，查看当前工作目录
>>> subprocess.run('pwd', shell=True)
/
CompletedProcess(args='pwd', returncode=0)

# 不继承父进程，设置当前工作目录为/etc
>>> subprocess.run('pwd', shell=True, cwd='/etc')
/etc
CompletedProcess(args='pwd', returncode=0)

# 继承父进程，查看当前工作目录下在文件列表
>>> subprocess.run('ls|head', shell=True)
anaconda-post.log
bin
boot
dev
etc
home
lib
lib64
media
mnt
CompletedProcess(args='ls|head', returncode=0)

# 不继承父进程，查看当前工作目录下在文件列表
>>> subprocess.run('ls|head', shell=True, cwd='/etc')
adjtime
adjtime.rpmsave
aliases
alternatives
bash_completion.d
bashrc
binfmt.d
BUILDTIME
centos-release
centos-release-upstream
CompletedProcess(args='ls|head', returncode=0)

>>>
```

#### `env`设置子进程的环境变量

```py
# 继承父进程，查看当前的环境变量
>>> subprocess.run('env', shell=True)
HOSTNAME=ea4bbe1c189d
TERM=xterm
PIPENV_VENV_IN_PROJECT=1
LC_ALL=en_US.utf8
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env
PWD=/
LANG=en_US.utf8
PIPENV_PYPI_MIRROR=https://mirrors.aliyun.com/pypi/simple
HOME=/root
SHLVL=2
LESSOPEN=||/usr/bin/lesspipe.sh %s
CompletedProcess(args='env', returncode=0)

# 不继承父进程，设置两个环境变量`HOSTNAME`和`LANG`，查看当前的环境变量
>>> subprocess.run('env', shell=True, env={'HOSTNAME': 'hellogitlab.com', 'LANG': 'zh_CN.utf8'})
HOSTNAME=hellogitlab.com
PWD=/
LANG=zh_CN.utf8
SHLVL=1
_=/usr/bin/env
CompletedProcess(args='env', returncode=0)

# 不继承父进程，设置两个环境变量`HOSTNAME`和`LANG`，并使用环境变量
>>> subprocess.run('echo "${HOSTNAME}"', shell=True, env={'HOSTNAME': 'hellogitlab.com', 'LANG': 'zh_CN.utf8'})
hellogitlab.com
CompletedProcess(args='echo "${HOSTNAME}"', returncode=0)
```

#### `timeout`设置命令超时时间

```py
# 不设置命令超时时间，正常执行
>>> subprocess.run('ping -c 3 jd.com', shell=True)
PING jd.com (118.193.98.63) 56(84) bytes of data.
64 bytes from 118.193.98.63 (118.193.98.63): icmp_seq=1 ttl=37 time=32.4 ms
64 bytes from 118.193.98.63 (118.193.98.63): icmp_seq=2 ttl=37 time=60.1 ms
64 bytes from 118.193.98.63 (118.193.98.63): icmp_seq=3 ttl=37 time=30.3 ms

--- jd.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 4100ms
rtt min/avg/max/mdev = 30.337/40.969/60.146/13.587 ms
CompletedProcess(args='ping -c 3 jd.com', returncode=0)

# `timeout`设置命令超时时间这1秒，出现`TimeoutExpired `异常
>>> subprocess.run('ping -c 3 jd.com', shell=True, timeout=1)
PING jd.com (118.193.98.63) 56(84) bytes of data.
64 bytes from 118.193.98.63 (118.193.98.63): icmp_seq=1 ttl=37 time=31.3 ms
---------------------------------------------------------------------------
TimeoutExpired                            Traceback (most recent call last)
/usr/lib64/python3.6/subprocess.py in run(input, timeout, check, *popenargs, **kwargs)
    404         try:
--> 405             stdout, stderr = process.communicate(input, timeout=timeout)
    406         except TimeoutExpired:

/usr/lib64/python3.6/subprocess.py in communicate(self, input, timeout)
    842             try:
--> 843                 stdout, stderr = self._communicate(input, endtime, timeout)
    844             finally:

/usr/lib64/python3.6/subprocess.py in _communicate(self, input, endtime, orig_timeout)
   1539
-> 1540             self.wait(timeout=self._remaining_time(endtime))
   1541

/usr/lib64/python3.6/subprocess.py in wait(self, timeout, endtime)
   1448                     if remaining <= 0:
-> 1449                         raise TimeoutExpired(self.args, timeout)
   1450                     delay = min(delay * 2, remaining, .05)

TimeoutExpired: Command 'ping -c 3 jd.com' timed out after 0.9998177000088617 seconds

During handling of the above exception, another exception occurred:

TimeoutExpired                            Traceback (most recent call last)
<ipython-input-18-b51a07dc1e78> in <module>
----> 1 subprocess.run('ping -c 3 jd.com', shell=True, timeout=1)

/usr/lib64/python3.6/subprocess.py in run(input, timeout, check, *popenargs, **kwargs)
    408             stdout, stderr = process.communicate()
    409             raise TimeoutExpired(process.args, timeout, output=stdout,
--> 410                                  stderr=stderr)
    411         except:
    412             process.kill()

TimeoutExpired: Command 'ping -c 3 jd.com' timed out after 1 seconds
```

#### `input`设置子进程输入参数
```py
# 给子进程指定输入参数，查找数字
>>> subprocess.run('grep --color=auto "[0-9]\{1,\}" $1', input=b"abcd", shell=True)
CompletedProcess(args='grep --color=auto "[0-9]\\{1,\\}" $1', returncode=1)

# 给子进程指定输入参数，查找数字
>>> subprocess.run('grep --color=auto "[0-9]\{1,\}" $1', input=b"1234", shell=True)
1234
CompletedProcess(args='grep --color=auto "[0-9]\\{1,\\}" $1', returncode=0)

# 给子进程指定输入参数，查找小写字母
>>> subprocess.run('grep --color=auto "[a-z]\{1,\}" $1', input=b"abcd", shell=True)
abcd
CompletedProcess(args='grep --color=auto "[a-z]\\{1,\\}" $1', returncode=0)
```

#### 设置子进程的标准输出

```py
# 不捕获标准输出，查看python3的版本信息
>>> subprocess.run(['python3', '-V'])
Python 3.6.7
CompletedProcess(args=['python3', '-V'], returncode=0)

# 捕获标准输出，查看python3的版本信息
>>> subprocess.run(['python3', '-V'], stdout=subprocess.PIPE)
CompletedProcess(args=['python3', '-V'], returncode=0, stdout=b'Python 3.6.7\n')

# 捕获标准输出，查看python3的版本信息，将结果保存到变量cmd_result中
>>> cmd_result=subprocess.run(['python3', '-V'], stdout=subprocess.PIPE)

# 查看cmd_result的值
>>> cmd_result
CompletedProcess(args=['python3', '-V'], returncode=0, stdout=b'Python 3.6.7\n')

# 获取标准输出信息
>>> cmd_result.stdout
b'Python 3.6.7\n'
```

#### 设置子进程的标准输出和标准错误

默认不会捕获子进程的标准输出和标准错误。

```py
[root@ea4bbe1c189d /]# ipython
Python 3.6.7 (default, Dec  5 2018, 15:02:05)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.5.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import subprocess

# 默认不会捕获标准输出和标准错误
# 不设置小数点位数，计算5除以2
>>> subprocess.run('echo "5/2"|bc', shell=True)
2
CompletedProcess(args='echo "5/2"|bc', returncode=0)

# 默认不会捕获标准输出和标准错误
# 设置小数点位数为1，计算5除以2
>>> subprocess.run('echo "scale=1; 5/2"|bc', shell=True)
2.5
CompletedProcess(args='echo "scale=1; 5/2"|bc', returncode=0)

# 捕获标准输出和标准错误
# 设置小数点位数为1，计算5除以2
# 此时没有异常，子进程的标准错误为空
>>> subprocess.run('echo "scale=1; 5/2"|bc', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
CompletedProcess(args='echo "scale=1; 5/2"|bc', returncode=0, stdout=b'2.5\n', stderr=b'')



# 不捕获标准输出和标准错误
# 设置小数点位数为1，计算5除以0，提示除0异常
>>> subprocess.run('echo "scale=1; 5/0"|bc', shell=True)
Runtime error (func=(main), adr=9): Divide by zero
CompletedProcess(args='echo "scale=1; 5/0"|bc', returncode=0)


# 捕获标准输出和标准错误
# 设置小数点位数为1，计算5除以0，
# 因为0不能作为除数，此时会抛出异常，子进程的标准为空，子进程的标准错误获取到了异常
>>> subprocess.run('echo "scale=1; 5/0"|bc', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
CompletedProcess(args='echo "scale=1; 5/0"|bc', returncode=0, stdout=b'', stderr=b'Runtime error (func=(main), adr=9): Divide by zero\n')


# 获取运行子进程后的结果
>>> divide_result = subprocess.run('echo "scale=1; 5/0"|bc', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 显示结果
>>> divide_result
CompletedProcess(args='echo "scale=1; 5/0"|bc', returncode=0, stdout=b'', stderr=b'Runtime error (func=(main), adr=9): Divide by zero\n')

# 打印获取到的标准输出结果，因为有异常，标准输出无错误
>>> divide_result.stdout
b''

# 打印获取到的标准错误结果
>>> divide_result.stderr
b'Runtime error (func=(main), adr=9): Divide by zero\n'
```

####  ` stderr=subprocess.STDOUT`设置子进程的标准错误合并到标准输出中

我们接着上面的示例进行除0计算。

```py

# 将子进程的标准错误合并到标准输出中
>>> divide_result = subprocess.run('echo "scale=1; 5/0"|bc', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# 显示计算结果
>>> divide_result
CompletedProcess(args='echo "scale=1; 5/0"|bc', returncode=0, stdout=b'Runtime error (func=(main), adr=9): Divide by zero\n')

# 打印标准输出结果
>>> divide_result.stdout
b'Runtime error (func=(main), adr=9): Divide by zero\n'

# 尝试打印标准错误，此时没有输出
>>> divide_result.stderr
```

#### 通过文件名柄设置标准错误和标准输出

```py
# 通过文件句柄获取标准异常
>>> with open('/tmp/stderr.log', 'ab') as ferr, open('/tmp/stdout.log', 'ab') as fout:
...     subprocess.run('echo "5/0"|bc', shell=True, stderr=ferr.fileno(), stdout=fout.fileno())
...
```

其中，`ferr.fileno()`和`fout.fileno()`表示一个整型的文件描述符。

此时查看`/tmp/stderr.log`文件的内容：

```sh
[root@ea4bbe1c189d /]# cat /tmp/stderr.log
Runtime error (func=(main), adr=5): Divide by zero
```

```py
# 通过文件句柄获取标准输出
>>> with open('/tmp/stderr.log', 'ab') as ferr, open('/tmp/stdout.log', 'ab') as fout:
...     subprocess.run('python3 -V', shell=True, stderr=ferr.fileno(), stdout=fout.fileno())
...
```

此时查看`/tmp/stdout.log`文件的内容：

```sh
[root@ea4bbe1c189d /]# cat /tmp/stdout.log
Python 3.6.7
```


也可以这样：

```py
>>> with open('/tmp/stderr.log', 'ab') as ferr, open('/tmp/stdout.log', 'ab') as fout:
...     subprocess.run('ping -c 3 baidu.com', shell=True, stderr=ferr, stdout=fout)
...

>>> with open('/tmp/stderr.log', 'ab') as ferr, open('/tmp/stdout.log', 'ab') as fout:
...     subprocess.run('command-not-exist', shell=True, stderr=ferr, stdout=fout)
...
```

此时再查看stderr.log和stdout.log文件内容：

```sh

[root@ea4bbe1c189d tmp]# cat stdout.log
Python 3.6.7
PING baidu.com (39.156.69.79) 56(84) bytes of data.
64 bytes from 39.156.69.79 (39.156.69.79): icmp_seq=1 ttl=37 time=30.3 ms
64 bytes from 39.156.69.79 (39.156.69.79): icmp_seq=2 ttl=37 time=27.9 ms
64 bytes from 39.156.69.79 (39.156.69.79): icmp_seq=3 ttl=37 time=27.5 ms

--- baidu.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 27.540/28.613/30.323/1.237 ms

[root@ea4bbe1c189d tmp]# cat stderr.log
Runtime error (func=(main), adr=5): Divide by zero
/bin/sh: command-not-exist: command not found
```

可以看到标准输出和标准错误都可以正常写入到文件中。


#### 将输出从二进制字符转换成字符串

```py
>>> subprocess.run('command-not-exist', shell=True, stderr=subprocess.PIPE)
CompletedProcess(args='command-not-exist', returncode=127, stderr=b'/bin/sh: command-not-exist: command not found\n')

>>> cmd_result = subprocess.run('command-not-exist', shell=True, stderr=subprocess.PIPE)

>>> cmd_result.stderr
b'/bin/sh: command-not-exist: command not found\n'

>>> print(cmd_result.stderr)
b'/bin/sh: command-not-exist: command not found\n'

>>> print(cmd_result.stderr.decode())
/bin/sh: command-not-exist: command not found
```

可以看到正常情况下，`cmd_result.stderr`的值是一个二进制字符串，使用`cmd_result.stderr.decode())`转换后，成为正常的字符串。

#### 标准输出编码处理

# 默认以UTF-8编码格式进行编码
```py
>>> subprocess.run('echo "中文字符"', shell=True, stdout=subprocess.PIPE)
CompletedProcess(args='echo "中文字符"', returncode=0, stdout=b'\xe4\xb8\xad\xe6\x96\x87\xe5\xad\x97\xe7\xac\xa6\n')

>>> cmd_result = subprocess.run('echo "中文字符"', shell=True, stdout=subprocess.PIPE)

# 输出是十六进制码
>>> cmd_result.stdout
b'\xe4\xb8\xad\xe6\x96\x87\xe5\xad\x97\xe7\xac\xa6\n'

>>> print(cmd_result.stdout)
b'\xe4\xb8\xad\xe6\x96\x87\xe5\xad\x97\xe7\xac\xa6\n'

# 重新解码
>>> print(cmd_result.stdout.decode())
中文字符


# 按UTF-8编码解码
>>> print(cmd_result.stdout.decode('UTF-8'))
中文字符

# 按GBK编码解码失败
>>> print(cmd_result.stdout.decode('GBK'))
---------------------------------------------------------------------------
UnicodeDecodeError                        Traceback (most recent call last)
<ipython-input-31-81e4c0032353> in <module>
----> 1 print(cmd_result.stdout.decode('GBK'))

UnicodeDecodeError: 'gbk' codec can't decode byte 0xad in position 2: illegal multibyte sequence

>>>
```

#### 设置编码格式为UTF-8

```py
>>> subprocess.run('echo "中文字符"', shell=True, stdout=subprocess.PIPE)
CompletedProcess(args='echo "中文字符"', returncode=0, stdout=b'\xe4\xb8\xad\xe6\x96\x87\xe5\xad\x97\xe7\xac\xa6\n')

>>> subprocess.run('echo "中文字符"', shell=True, stdout=subprocess.PIPE, encoding='UTF-8')
CompletedProcess(args='echo "中文字符"', returncode=0, stdout='中文字符\n')
```

此时可以看出使用`encoding='UTF-8'`设置后，输出的`stdout`的值发生了变化，不是二进制结果了！此时不需要解码就可以直接获取到标准输出的中文字符：

```py
 cmd_result = subprocess.run('echo "中文字符"', shell=True, stdout=subprocess.PIPE, encoding='UTF-8')

>>> cmd_result
CompletedProcess(args='echo "中文字符"', returncode=0, stdout='中文字符\n')

>>> cmd_result.stdout
'中文字符\n'

>>> print(cmd_result.stdout)
中文字符
```

#### 检查子进程的运行状态是否正常

当子进程退出码非零时，说明子进程退出异常！

正常退出示例：

```py
 cmd_result = subprocess.run('echo "中文字符"', shell=True, stdout=subprocess.PIPE, encoding='UTF-8')

>>> cmd_result
CompletedProcess(args='echo "中文字符"', returncode=0, stdout='中文字符\n')

>>> cmd_result.check_returncode?
Signature: cmd_result.check_returncode()
Docstring: Raise CalledProcessError if the exit code is non-zero.
File:      /usr/lib64/python3.6/subprocess.py
Type:      method

>>> cmd_result.returncode
0

# 检查退出码是否非0
>>> cmd_result.check_returncode()

>>>
```

异常退出：

```py
>>> cmd_result = subprocess.run('exit 2', shell=True)

>>> cmd_result
CompletedProcess(args='exit 2', returncode=2)

>>> cmd_result.returncode
2

>>> cmd_result.check_returncode()
---------------------------------------------------------------------------
CalledProcessError                        Traceback (most recent call last)
<ipython-input-64-b3b88562ebc7> in <module>
----> 1 cmd_result.check_returncode()

/usr/lib64/python3.6/subprocess.py in check_returncode(self)
    367         if self.returncode:
    368             raise CalledProcessError(self.returncode, self.args, self.stdout,
--> 369                                      self.stderr)
    370
    371

CalledProcessError: Command 'exit 2' returned non-zero exit status 2.

>>>
```
当检查到异常退出时，`check_returncode()`方法会抛出`CalledProcessError`异常。

#### 将异常重定向到空设备文件`DEVNULL`

可以使用`subprocess.DEVNULL`定义空设备文件，如果将标准输出或者标准错误重定向到空设备文件`/dev/null`，实质上想当于不捕获标准输出或标准错误，因为任何写入到空设备文件中的内容都不会显示，就像黑洞一样。

```py
>>> cmd_result = subprocess.run('echo "5/0"|bc', shell=True)
Runtime error (func=(main), adr=5): Divide by zero

# 查看不获取标准错误时的输出信息
>>> cmd_result
CompletedProcess(args='echo "5/0"|bc', returncode=0)

>>> cmd_result = subprocess.run('echo "5/0"|bc', shell=True, stderr=subprocess.PIPE)

# 查看获取标准错误时的输出信息
>>> cmd_result
CompletedProcess(args='echo "5/0"|bc', returncode=0, stderr=b'Runtime error (func=(main), adr=5): Divide by zero\n')

# 捕获标准错误，但是重定向到空设备文件中去
>>> cmd_result = subprocess.run('echo "5/0"|bc', shell=True, stderr=subprocess.DEVNULL)

# 查看输出错误，可以看到此时程序并没有返回`stderr`的值信息，说明标准错误信息并没有捕获
>>> cmd_result
CompletedProcess(args='echo "5/0"|bc', returncode=0)
```

#### `subprocess.Popen`类

`class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, encoding=None, errors=None)`

实际上`subprocess.run()`函数是调用底层的`subprocess.Popen`类，你可以用 `subprocess.Popen`类做更多复杂的事情，可以参考[https://docs.python.org/3.6/library/subprocess.html#popen-constructor](https://docs.python.org/3.6/library/subprocess.html#popen-constructor)。

由于官方告诉我们大部分时间我们使用`subprocess.run()`函数就足够了，我这边就不详细介绍 `subprocess.Popen`类呢。

### `subprocess`的安全问题

虽然我们可以在`subprocess.run()`中使用`shell=True`参数，让我们可以执行shell命令，但此时我们需要关注一下安全问题，官方有以下说明：

> 17.5.2. Security Considerations

> Unlike some other popen functions, this implementation will never implicitly call a system shell. This means that all characters, including shell metacharacters, can safely be passed to child processes. If the shell is invoked explicitly, via shell=True, it is the application’s responsibility to ensure that all whitespace and metacharacters are quoted appropriately to avoid shell injection vulnerabilities.

> When using shell=True, the shlex.quote() function can be used to properly escape whitespace and shell metacharacters in strings that are going to be used to construct shell commands.

即：

- 如果通过`shell=True`显式调用了shell，则应用程序有责任确保所有空白和元字符都被正确引用，以避免shell注入漏洞。
- 当使用`shell=True`时，`shlex.quote()`函数可用于正确地转义将用于构造Shell命令的字符串中的空格和Shell元字符。

`shlex`中给出了一个不安全的示例：

```py
>>> filename = 'somefile; rm -rf ~'
>>> command = 'ls -l {}'.format(filename)
>>> print(command)  # executed by a shell: boom!
ls -l somefile; rm -rf ~
```

此时我们如果使用shell执行上面`command`命令，那么家目录将会被完全删除！！！非常危险！！！

而使用`shlex.quote()`将需要执行的命令进行转义，解决上面的安全问题：

```py
>>> command = 'ls -l {}'.format(quote(filename))
>>> print(command)
ls -l 'somefile; rm -rf ~'
>>> remote_command = 'ssh home {}'.format(quote(command))
>>> print(remote_command)
ssh home 'ls -l '"'"'somefile; rm -rf ~'"'"''
```

我们来依照上面的例子做一个实验，看看使用`shlex.quote()`和不使用`shlex.quote()`执行shell命令时产生什么样的效果。

::: danger 危险
我们的测试都是在docker容器中进行，请不要在生产环境或者你有重要数据的电脑上执行。
:::

我们首先备份一下`/tmp`目录：

```sh
[root@ea4bbe1c189d /]# cp -r tmp tmpbak

[root@ea4bbe1c189d /]# ls /tmpbak/
anaconda-post.log  ks-script-eC059Y  stderr.log  stdin.log  stdout.log  yum.log
```

下面我在`ipython`中执行shell命令：

```py
>>> import subprocess

>>> import shlex

>>> shlex.quote?
Signature: shlex.quote(s)
Docstring: Return a shell-escaped version of the string *s*.
File:      /usr/lib64/python3.6/shlex.py
Type:      function



>>> cmd = 'ls /tmp/stderr.log; rm -rf /tmpbak'

>>> shlex.quote(cmd)
"'ls /tmp/stderr.log; rm -rf /tmpbak'"

>>> subprocess.run(shlex.quote(cmd), shell=True)
/bin/sh: ls /tmp/stderr.log; rm -rf /tmpbak: No such file or directory
CompletedProcess(args="'ls /tmp/stderr.log; rm -rf /tmpbak'", returncode=127)
```

此时查看根目录下面的文件列表：

```sh
[root@ea4bbe1c189d /]# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  tmpbak  usr  var
```

可以看到`tmpbak`目录仍然存在！

可以看到，此时虽然原始命令`'ls /tmp/stderr.log; rm -rf /tmpbak'`如果按shell方式执行的话会执行两条命令，会将/tmpbak删除，使用了`shlex.quote()`转义后，将命令当成了一条命令，执行子进程异常退出，不会删除/tmpbak文件夹。

我们再尝试一下不使用`shlex.quote()`会是什么效果：

```py
>>> subprocess.run(cmd, shell=True)
/tmp/stderr.log
CompletedProcess(args='ls /tmp/stderr.log; rm -rf /tmpbak', returncode=0)
```

此时程序正常执行，退出码为0，这时候查看根目录下面的文件列表：

```sh
[root@ea4bbe1c189d /]# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

可以看到，此时根目录下面已经没有`tmpbak`目录了，说明`tmpbak`目录已经被删除了！如果将`rm -rf /tmpbak`换成`rm -rf /`,执行命令的话，此时就是灾难呢。

所以我们尽量在执行`subprocess.run()`时使用`shell=False`，并且使用列表或元组指定子进程命令参数。


## 使用`multiprocessing`创建进程

我们可以使用`multiprocessing`模块在一个程序中创建多个进程。

看下面的示例：

```py
# filename: use_multiprocessing.py
import os
import multiprocessing


def do_this(what):
    whoami(what)


def whoami(what):
    print("Process %s says: %s" % (os.getpid(), what))


def main():
    whoami("I'm the main program")
    for i in range(5):
        p = multiprocessing.Process(
            target=do_this,
            args=("I'm function %s" % i,)
        )
        p.start()
        do_this("not in multiprocessing")


if __name__ == '__main__':
    main()

# Output:
# Process 3415 says: I'm the main program
# Process 3415 says: not in multiprocessing
# Process 3415 says: not in multiprocessing
# Process 3416 says: I'm function 0
# Process 3415 says: not in multiprocessing
# Process 3417 says: I'm function 1
# Process 3415 says: not in multiprocessing
# Process 3418 says: I'm function 2
# Process 3415 says: not in multiprocessing
# Process 3419 says: I'm function 3
# Process 3420 says: I'm function 4
```

可以看到，主函数运行时，进程ID为3415，并最先打印出`I'm the main program`,此时虽然紧接着使用`multiprocessing.Process()`函数创建一个新进程来运行`do_this()`函数，正常来说，如果不使用多进程的话，应该代码段在前的先执行，在后的后执行，由于此时需要开辟新进程，主进程中仍然可以继续执行其他操作，因此`not in multiprocessing`被先执行了，后来再执行子进程输出`I'm function 0`之类的。

`mutiprocessing`多进程使用相对麻烦，后续详细了解后再补充。

参考：

- [subprocess — Subprocess management](https://docs.python.org/3.6/library/subprocess.html#popen-constructor)
- [运维那点事-Python模块：subprocess](https://www.ywnds.com/?p=15074)
- [刘江的博客-subprocess](https://www.liujiangblog.com/course/python/55)
- [https://docs.python.org/3.6/library/shlex.html#shlex.quote](https://docs.python.org/3.6/library/shlex.html#shlex.quote)

