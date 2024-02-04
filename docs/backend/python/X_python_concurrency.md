# Python并发

[[toc]]

在计算机中，如果你的程序在等待，通常是因为以下两个原因：

- I/O限制，这个限制很常见，计算机的CPU速度非常快，比计算机内存快几百倍，比硬盘或者网络快几千倍。
- CPU限制，在处理数字运算任务时，比如科学计算或者图形计算，很容易遇到这个限制。

并发相关术语：

- 同步(Synchronous)，一件事情接着一件事情处理。
- 异步(asynchronous)，任务是相互独立的。

当你要用简单的系统和任务来处理现实中的问题时，迟早需要处理并发。

假设你有一个网站，必须给用户很快地返回静态和动态网页，一秒是可以接受的，但是如果展示或者交互需要很长时间，用户就会失去耐心，页面速度加载降低一点就会导致流量大幅下降。

但是，如何处理需要长时间执行的任务呢，如上传文件、改变图片大小或者查询数据库？显然无法用同步的Web客户端代码解决这个问题，因为同步就必然会产生等待。

在一台电脑中，如果你想尽快处理多个任务，就需要让它们互相独立。慢任务不应该阻塞其他任务。

下面我们看一下多任务管理方法：队列。



## 队列

队列有点像列表，从一头添加事物，从另一头取出事物，这种队列被称为`FIFO(先进先出)`， 即`First In First Out`。

假设你正在洗盘子，如果需要完成全部工作，需要洗好每一个盘子、烘干并放好。你有很多种方法来完成这个任务。或许人会先洗好第一个盘子，烘干并把它放好。之后用同样的方法来处理第二个盘子，比此类推。此外，你也可以执行批量操作，先洗好所有的盘子，再烘干所有的盘子，最后把它们都放好。这样做需要你有足够大的水池和烘干机来放置每一步积累的所有盘子。这些都是同步方法--一个工人，一次做一件事。

还有一种方法是再找一个或者两个帮手。如果你是洗盘子的人，可以把洗好的盘子递给烘干盘子的人，他再把烘干的盘子递给放置盘子的人。所有人都在自己的位置工作，这样会比你一个人要快得多。

然而，如果你洗盘子的速度比下一个人烘干的速度快怎么办？要么把湿盘子扔在地上，要么把它们堆在你和下一个之间，或者一直闲着直到下一个人处理完成之前的盘子。如果最后一个人比第二个人还慢，那第二个人要么把盘子扔在地上，要么把它们堆在两个人之间，要么就闲着。你有很多个工人，但总体来说，任务仍然是同步完成的，处理速度和最慢的工人速度是一样的。

俗话说，人多好办事。增加工人可以更快地洗盘子，前提是使用`队列`。

通常来说，队列用来传递消息，消息可以是任意类型的消息。在本例中，我们用队列来管理分布式任务，这种队列也称为`工作队列`或者`任务队列`。水池中的每个盘子都会发给一个闲置的洗盘子的人，他会洗盘子并把盘子传给一个闲置的烘干盘子的人，他会烘干盘子并把盘子传给一个闲置的放盘子的人。这个过程可以是`同步`的(工人等着处理盘子，处理完等着把盘子给下一个人)，也可以是`异步`的(盘子堆在两个工人中间)。只要你有足够多的工人并且他们都能认真工作，完成速度会非常快。

## 进程

你可以用很多方法来实现队列。对单机来说，标准库中的`multiprocessing`模块有一个`Queue`函数。接下来模拟一个洗盘子的人和多个烘干进程（不用担心，会有人放盘子放好）。我们使用一个中间队列`dish_queue`，把下面的代码保存到`dishes.py`中：

```py
# Filename: dishes.py
import multiprocessing as mp


def washer(dishes, output):
    """洗盘子"""
    for dish in dishes:
        print('Washing %s dish' % dish)
        output.put(dish)


def dryer(input):
    """烘干盘子"""
    while True:
        dish = input.get()
        print('Drying %s dish' % dish)
        input.task_done()


def main():
    """构建队列"""
    dish_queue = mp.JoinableQueue()
    dish_proc = mp.Process(target=dryer, args=(dish_queue,))
    dish_proc.daemon = True
    dish_proc.start()

    dishes = ['p1', 'p2', 'p3', 'p4']
    washer(dishes, dish_queue)
    dish_queue.join()


if __name__ == '__main__':
    main()
```

运行这个程序，输出如下：

```sh
$ python3 dishes.py
Washing p1 dish
Washing p2 dish
Washing p3 dish
Washing p4 dish
Drying p1 dish
Drying p2 dish
Drying p3 dish
Drying p4 dish
```

这个队列看起来像一个简单的Python迭代器，会生成一系列盘子。这段代码实际上会启动几个独立的进程，先盘子的人和烘干盘子的人会用它们来进行通信。我使用`JoinableQueue`和最后的`join()`方法让洗盘子的人知道，所有的盘子都已经烘干。


增加一些`print`语句，打印一下PID:

```py
# Filename: dishes.py
import os
import multiprocessing as mp


def washer(dishes, output):
    """洗盘子"""
    print('working in washer. PID: %s' % os.getpid())
    for dish in dishes:
        print('Washing %s dish' % dish)
        print('working in washer for before output.put. PID: %s' % os.getpid())
        output.put(dish)
        print('working in washer for after outout.put. PID: %s' % os.getpid())


def dryer(input):
    """烘干盘子"""
    print('working in dryer. PID: %s' % os.getpid())
    while True:
        print('working in dryer. before input.get(). PID: %s' % os.getpid())
        dish = input.get()
        print('working in dryer. after input.get(). PID: %s' % os.getpid())
        print('Drying %s dish' % dish)
        input.task_done()
        print('working in dryer. after input.task_done(). PID: %s' % os.getpid())



def main():
    """构建队列"""
    print('working in main. PID: %s' % os.getpid())
    dish_queue = mp.JoinableQueue()
    dish_proc = mp.Process(target=dryer, args=(dish_queue,))
    dish_proc.daemon = True
    dish_proc.start()

    dishes = ['p1', 'p2', 'p3', 'p4']
    print('working in main. before washer() PID: %s' % os.getpid())
    washer(dishes, dish_queue)
    print('working in main. after washer() PID: %s' % os.getpid())
    print('working in main. before dish_queue.join() PID: %s' % os.getpid())
    dish_queue.join()
    print('working in main. after dish_queue.join() PID: %s' % os.getpid())


if __name__ == '__main__':
    main()
```

再次运行结果如下：

```sh
$ python3 dishes.py
working in main. PID: 24030
working in main. before washer() PID: 24030
working in washer. PID: 24030
Washing p1 dish
working in washer for before output.put. PID: 24030
working in washer for after outout.put. PID: 24030
Washing p2 dish
working in washer for before output.put. PID: 24030
working in washer for after outout.put. PID: 24030
Washing p3 dish
working in washer for before output.put. PID: 24030
working in washer for after outout.put. PID: 24030
Washing p4 dish
working in washer for before output.put. PID: 24030
working in washer for after outout.put. PID: 24030
working in main. after washer() PID: 24030
working in main. before dish_queue.join() PID: 24030
working in dryer. PID: 24031
working in dryer. before input.get(). PID: 24031
working in dryer. after input.get(). PID: 24031
Drying p1 dish
working in dryer. after input.task_done(). PID: 24031
working in dryer. before input.get(). PID: 24031
working in dryer. after input.get(). PID: 24031
Drying p2 dish
working in dryer. after input.task_done(). PID: 24031
working in dryer. before input.get(). PID: 24031
working in dryer. after input.get(). PID: 24031
Drying p3 dish
working in dryer. after input.task_done(). PID: 24031
working in dryer. before input.get(). PID: 24031
working in dryer. after input.get(). PID: 24031
Drying p4 dish
working in dryer. after input.task_done(). PID: 24031
working in dryer. before input.get(). PID: 24031
working in main. after dish_queue.join() PID: 24030
```

可以看到洗盘子使用的进程是`24030`，烘干盘子使用的进程是`24031`，也就是洗盘子和烘干盘子使用独立的进程。

## 线程

线程运行在进程内部，可以访问进程的所有内容。`multiprocessing`模块有一个兄弟模块`threading`，后者用线程来代替进程(实际上，`multiprocessing`是在`threading`之后设计出来的，基于进程来完成各种任务)。我们使用线程来重写上面的进程实例：

```py
import os
import threading


def do_this(what):
    whoami(what)


def whoami(what):
    print('Check PID: %s' % os.getpid())
    print("Thread %s says: %s" % (threading.current_thread(), what))


def main():
    whoami("I'm the main program")
    for i in range(5):
        p = threading.Thread(
            target=do_this,
            args=("I'm function %s" % i,)
        )
        p.start()
        do_this("not in threading")


if __name__ == '__main__':
    main()
```

运行后得到以下输出：

```sh
Check PID: 25206
Thread <_MainThread(MainThread, started 140734900350400)> says: I'm the main program
Check PID: 25206
Thread <Thread(Thread-1, started 123145383030784)> says: I'm function 0
Check PID: 25206
Thread <_MainThread(MainThread, started 140734900350400)> says: not in threading
Check PID: 25206
Check PID: 25206
Thread <_MainThread(MainThread, started 140734900350400)> says: not in threading
Thread <Thread(Thread-2, started 123145383030784)> says: I'm function 1
Check PID: 25206
Thread <Thread(Thread-3, started 123145388285952)> says: I'm function 2
Check PID: 25206
Thread <_MainThread(MainThread, started 140734900350400)> says: not in threading
Check PID: 25206
Thread <Thread(Thread-4, started 123145383030784)> says: I'm function 3
Check PID: 25206
Thread <_MainThread(MainThread, started 140734900350400)> says: not in threading
Check PID: 25206
Thread <Thread(Thread-5, started 123145383030784)> says: I'm function 4
Check PID: 25206
Thread <_MainThread(MainThread, started 140734900350400)> says: not in threading
```

使用线程重定盘子示例：

```py
# Filename: dishes.py
import os
import threading, queue
import time


def washer(dishes, dish_queue):
    """洗盘子"""
    print('working in washer. PID: %s' % os.getpid())
    for dish in dishes:
        print('Washing %s dish' % dish)
        print('working in washer for before dish_queue.put. PID: %s' % os.getpid())
        time.sleep(2)
        dish_queue.put(dish)
        print('working in washer for after dish_queue.put. PID: %s' % os.getpid())


def dryer(dish_queue):
    """烘干盘子"""
    print('working in dryer. PID: %s' % os.getpid())
    while True:
        print('working in dryer. before dish_queue.get(). PID: %s' % os.getpid())
        dish = dish_queue.get()
        time.sleep(3)
        print('working in dryer. after dish_queue.get(). PID: %s' % os.getpid())
        print('Drying %s dish' % dish)
        dish_queue.task_done()
        print('working in dryer. after dish_queue.task_done(). PID: %s' % os.getpid())


def main():
    """构建队列"""
    print('working in main. PID: %s' % os.getpid())
    dish_queue = queue.Queue()
    for n in range(5):
        dryer_thread = threading.Thread(target=dryer, args=(dish_queue,))
        dryer_thread.start()

    dishes = ['p1', 'p2', 'p3', 'p4']
    print('working in main. before washer() PID: %s' % os.getpid())
    washer(dishes, dish_queue)
    print('working in main. after washer() PID: %s' % os.getpid())
    print('working in main. before dish_queue.join() PID: %s' % os.getpid())
    dish_queue.join()
    print('working in main. after dish_queue.join() PID: %s' % os.getpid())


if __name__ == '__main__':
    main()
```

运行后得到以下输出：

```sh
$ python3 dishes.py
working in main. PID: 25556
working in dryer. PID: 25556
working in dryer. before dish_queue.get(). PID: 25556
working in dryer. PID: 25556
working in dryer. before dish_queue.get(). PID: 25556
working in dryer. PID: 25556
working in dryer. before dish_queue.get(). PID: 25556
working in dryer. PID: 25556
working in dryer. before dish_queue.get(). PID: 25556
working in dryer. PID: 25556
working in dryer. before dish_queue.get(). PID: 25556
working in main. before washer() PID: 25556
working in washer. PID: 25556
Washing p1 dish
working in washer for before dish_queue.put. PID: 25556
working in washer for after dish_queue.put. PID: 25556
Washing p2 dish
working in washer for before dish_queue.put. PID: 25556
working in washer for after dish_queue.put. PID: 25556
Washing p3 dish
working in washer for before dish_queue.put. PID: 25556
working in dryer. after dish_queue.get(). PID: 25556
Drying p1 dish
working in dryer. after dish_queue.task_done(). PID: 25556
working in dryer. before dish_queue.get(). PID: 25556
working in washer for after dish_queue.put. PID: 25556
Washing p4 dish
working in washer for before dish_queue.put. PID: 25556
working in dryer. after dish_queue.get(). PID: 25556
Drying p2 dish
working in dryer. after dish_queue.task_done(). PID: 25556
working in dryer. before dish_queue.get(). PID: 25556
working in washer for after dish_queue.put. PID: 25556
working in main. after washer() PID: 25556
working in main. before dish_queue.join() PID: 25556
working in dryer. after dish_queue.get(). PID: 25556
Drying p3 dish
working in dryer. after dish_queue.task_done(). PID: 25556
working in dryer. before dish_queue.get(). PID: 25556
working in dryer. after dish_queue.get(). PID: 25556
Drying p4 dish
working in dryer. after dish_queue.task_done(). PID: 25556
working in dryer. before dish_queue.get(). PID: 25556
working in main. after dish_queue.join() PID: 25556
```

可以看出使用线程运行该程序时，并没有新的进程产生，全部使用的是`PID: 25556`。

`multiprocessing`和`threading`的区别之一就是`threading`没有`terminate()`函数，很难终止一个正在运行的线程，因为这可能会引起代码和时空连续性上的各种问题。(不懂:cry:)

线程可能会很危险。就像C或C++这类语言中的手动内存管理一样，线程可能会引起很难寻找和处理的bug，要使用线程，程序中的所有代码以及程序使用的所有外部库中的代码必须是线程安全的。在之前的示例代码中，线程之间没有共享任何全局变量，因此可以在没有副作用的情况下独立运行。

下面这些关于线程的幽灵故事是直接复制的《python语言及其应用》的。

假设你是一个幽灵星中的超自然现象调查员，幽灵在大厅中漫游，但是它们互相之间并不能感知到对方。此外，幽灵可以在任何时间浏览、添加、删除或者移动房间中的任意物品。

你一边看着令人惊讶的仪表读数，一边穿过整个房间。突然，你发现几秒钟之前刚看到的烛台不见了。

房间中的物品就像程序中的变量，幽灵是进程(房间)中的线程。如果幽灵只会浏览房间中的物品，就没有任何问题。就像线程只会读取常量或者变量中的值，但是不会修改它们。

然而，有些看不见的东西会抓住你的手电筒，往你的脖子上吹冷风，在大理石楼梯上一步一步地走，或者点燃壁炉。真正精明的幽灵甚至会在你看不到的房间中捣乱。

尽管你有很高端的设备，要找出是谁在什么时候做了什么改动仍然非常困难。

如果你使用进程来代替线程，那就像有很多个房子但是每个房子里只有一个(活)人。如果你把白兰地放在壁炉前，一个小时后它还会在那儿。或许会蒸发一些，但是位置不变。

没有全局变量时，线程是非常有用并且安全的。通常来说，如果需要等待I/O操作完成，那么使用线程可以节省很多时间。在这种情况下，线程不会因为数据打架。因为每个线程使用的是完全独立的变量。

但是线程有时候确实需要修改全局变量。实际上，使用多线程的一个常见目的就是把需要处理的数据进行划分，这就不可避免地需要修改数据。

常见的安全共享数据的方法是让线程在修改变量之前加软件锁🔒，这样在进行修改时其他线程都会等待。这就像在有幽灵的房子中有一个抓幽灵敢死队帮你看门。需要注意的是，千万别忘了解锁。此外，锁可以嵌套，就像你还有另一个抓幽灵敢死队来看同一个房间或者同一个房子。锁的用户非常传统但是要想用对非常困难。

在Python中，线程不能加速受CPU限制的任务，原因是标准Python系统中使用了全局解释器锁(GIL),GIL的作用是避免Python解释器中的线程问题，但是实际上会让多线程程序运行速度比对应的单线程版本甚至是多进程版本更慢。

总而言之，对于Python建议如下:

- 使用线程来解决I/O限制问题。
- 使用进程、网络或者事件下处理CPU限制问题。

## 绿色线程和gevent

如你所见，开发者通常会把程序中运行速度慢的部分划分为多个线程或者进程从而加快速度。Apache Web服务器就是一个典型的例子。

另一种方法是基于事件编程(Event-driven programming)。一个基于事件的程序会运行一个核心事件循环。分配所有任务，然后重复这个循环。Nginx Web服务器就是基于事件的设计，通常来说比Apache快。

gevent就是一个基于事件的很棒的库，你只需要写普通的代码，gevent会神奇的地它们转换成协程。协程就像可以互相通信的生成器，它们会记录自己的位置。gevent可以修改许多Python的标准对象，比如socket,从而使用它自己的机制来代替阻塞。协程无法处理C写成的Python扩展代码，比如一些数据库驱动程序。

### 安装gevent

使用pip安装gevent：

```sh
$ pip install gevent
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting gevent
  Downloading http://mirrors.aliyun.com/pypi/packages/fc/ad/c907f92d34c33ce0c088705dc4675b0a9d22caeb078bf4cb5d9c66329f6e/gevent-20.5.2-cp36-cp36m-macosx_10_15_x86_64.whl (1.8 MB)
     |████████████████████████████████| 1.8 MB 1.4 MB/s
Collecting greenlet>=0.4.14; platform_python_implementation == "CPython"
  Downloading http://mirrors.aliyun.com/pypi/packages/f8/e8/b30ae23b45f69aa3f024b46064c0ac8e5fcb4f22ace0dca8d6f9c8bbe5e7/greenlet-0.4.15.tar.gz (59 kB)
     |████████████████████████████████| 59 kB 10.6 MB/s
Requirement already satisfied: setuptools in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from gevent) (40.6.2)
Collecting zope.event
  Downloading http://mirrors.aliyun.com/pypi/packages/c5/96/361edb421a077a4c208b4a5c212737d78ae03ce67fbbcd01621c49f332d1/zope.event-4.4-py2.py3-none-any.whl (7.6 kB)
Collecting zope.interface
  Downloading http://mirrors.aliyun.com/pypi/packages/ba/6f/03bcd3038d9f2ed6ec7253a775e45c376ab9382bc2cd17cc7c5dab05e477/zope.interface-5.1.0-cp36-cp36m-macosx_10_6_intel.whl (203 kB)
     |████████████████████████████████| 203 kB 9.4 MB/s
Installing collected packages: greenlet, zope.event, zope.interface, gevent
    Running setup.py install for greenlet ... done
Successfully installed gevent-20.5.2 greenlet-0.4.15 zope.event-4.4 zope.interface-5.1.0
```

### gevent示例

```py
# Filename: use_gevent.py
import gevent
from gevent import socket

hosts = [
    'www.baidu.com',
    'www.jd.com',
    'www.zhihu.com'
]
jobs = [gevent.spawn(socket.gethostbyname, host) for host in hosts]
gevent.joinall(jobs, timeout=5)
for job in jobs:
    print(job.value)
```

运行以上程序，输出如下：

```sh
$ python3 use_gevent.py
180.101.49.41
60.174.240.3
125.78.252.83
```

可以看到以上程序运行后，可以很快的打印出结果，几乎没有等待。

通过`gethostbyname()`可以通过主机名获取主机名对应的IP地址，`for`循环中的调用可以异步执行，因为使用的是`gevent`版本的`gethostbyname()`。

`gevent.spawn()`会为每个`gevent.socket.gethostbyname`创建一个绿色线程(也叫做微线程)。

绿色线程和普通线程的区别是前者不会阻塞。如果遇到会阻塞普通线程的情况，gevent会把控制权切换到另一个绿色线程。

`gevent.joinall()`会等待所有的任务完成。最后输出获得的所有IP地址。

除了使用`gevent`版本的`socket`之外，也可以使用`猴子补丁(monkey-patching)`函数。这个函数会修改标准模块，比如`socket`，直接让它们使用绿色线程而不是调用`gevent`版本。如果想在整个程序中应用`gevent`，这种方法非常有用，即使那些你无法直接接触到的代码也会改变。

在程序的开头添加下面的代码:

```py
from gevent import monkey
monkey.patch_socket()
```

这会把程序中所有的普通`socket`都修改成`gevent`版本，即使是标准库也不例外。这个改动只对Python代码有效，对C写成的库无效。

我们使用猴子方法修改上面的示例：

```py
import socket
from gevent import monkey, spawn, joinall

monkey.patch_socket()
hosts = [
    'www.baidu.com',
    'www.jd.com',
    'www.zhihu.com'
]
jobs = [spawn(socket.gethostbyname, host) for host in hosts]
joinall(jobs, timeout=5)
for job in jobs
    print(job)
    print(job.value)
```

运行输出如下:

```sh
<Greenlet at 0x106bbd748: _run>
14.215.177.39
<Greenlet at 0x106bbd848: _run>
60.174.240.3
<Greenlet at 0x106bbd948: _run>
59.63.235.238
```

可以看到每一个子job都是`Greenlet`绿色线程。

另一个函数会给更多的标准库模块打上补丁：

```py
from gevent import monkey
monkey.patch_all()
```

在程序开头加上以上代码可以让你的程序充分利用`gevent`带来的速度提升。

```py
import socket
from gevent import monkey, spawn, joinall

monkey.patch_all()
hosts = [
    'www.baidu.com',
    'www.jd.com',
    'www.zhihu.com'
]
jobs = [spawn(socket.gethostbyname, host) for host in hosts]
joinall(jobs, timeout=5)
for job in jobs:
    print(job)
    print(job.value)
```

我们再次运行，输出如下：

```sh
<Greenlet at 0x106d9b548: _run>
14.215.177.39
<Greenlet at 0x106d9b648: _run>
60.174.240.3
<Greenlet at 0x106d9b748: _run>
218.75.176.215
```

使用`gevent`还有一个潜在的危险。对于基于事件的系统来说，执行的每段代码都应该尽可能快，尽管不会阻塞，执行复杂任务的代码还是会很慢。

猴子补丁的理念对于很多人来说并不容易接受。但是，很多大型网站都在使用`gevent`，对网站来说有明显的加速作用。就像一个外表精美的药丸💊一样，要用正确的方式使用`gevent`。

另外两个流行的事件驱动框架是`tornado`和`gunicorn`。它们都使用了底层事件处理和高速Web服务器。如果你想使用传统的Web服务器(比如Apache)来构建高速网站，这两个框架非常值得一看。


## twisted

twisted是一个异步事件驱动的网络框架。你可以把函数关联到事件(比如数据接收或者连接关闭)上，当事件发生时这些函数会被调用。这种设计被称为`回调(callback)`。如果你以前用过JavaScript，那一定不会陌生。对于有些开发者来说，基于回调的代码在应用规模变大之后会很难维护。

Twisted支持许多常见的传输及应用层协议，包括TCP、UDP、SSL/TLS、HTP、IMAP、SSH、IRC以及FTP。就像Python一样，Twisted也具有`内置电池(batteries-included)`的特点。Twisted对于其支持的所有协议都带有客户端和服务器实现，同时附带有基于命令行的工具，使得配置和部署产品级的Twisted应用变得非常方便。

后续补充twisted相关示例和详情。


## asyncio

asyncio模块在python 3.4中首次出现。它提供了一种能用的事件循环，可以兼容twisted/gevent和其他异步方法。目标是提供一种标准、简洁、高性能的异步API。

参考：[https://docs.python.org/3.6/library/asyncio.html](https://docs.python.org/3.6/library/asyncio.html)


##  Redis实现队列

我们之前的洗盘子示例代码，无论使用的是进程还是线程，都运行在一台机器上。下面我们使用另一种方法来实际队列。让它可以既支持单机又支持网络。有时候用了进程和线程，单机仍然无法满足需求。本章的目的就是帮助你从一个盒子(单机)过滤到多个并发的盒子。

要运行本章的示例，需要安装Redis服务器和它的Python模块，安装方法可参考：[redis的安装](./X_database.html#redis的安装),在参考链接中Redis的角色是数据库，而这里指的是它的并发特性。

可以使用Redis列表来快速创建一个队列。

下面是示例，后续待补！！！

## 队列之上

加入的功能越多，流水线就越有可能出问题。如果需要给一个宴会洗盘子，工人数量是否足够呢？如果烘干工人喝多了怎么办？如果水槽堵了怎么办？如担心啊！

如何应对这一切呢？幸运的是，有三种技术可供你使用：

- 触发并忘记。只传递内容，江不关心结果，即使没人处理。这就是"把盘子扔地上"方法。
- 请求-响应。对于每一个盘子，流水线上的清洗工人需要收到烘干工人的确认，烘干工人需要收到放置工人的确认。
- 背压或者节流。适用于上游工人速度比下游工作快的情况。

在真实系统中，你必须保证工人的速度能够满足需求，否则就会听到盘子摔碎的声音。你可以把就任务添加到一个等待列表中，一些工人进程会从中弹出最后一个消息并把它添加到工作列表中。消息处理完成后会从工作列表中移除并被添加到完成列表。这样就可以知道哪些任务失败或者占用了太长的时间。你可以自己使用redis来完成这些功能，或者使用其他人已经写好并通过测试的系统。以下有一些基于Python队列的包添加了这种额外的控制层(有些使用的是Redis):

- celery。 这个包非常值得一看，它可以同步或者异步执行分布式任务。使用了我们之前介绍的方法multiprocessing、gevent等。
- thoonk。 这个包基于Redis构建，可以创建任务队列并实现发布-订阅。
- rq。 这是一个处理任务队列的python库，也是基于Redis。
- Queues。 这个网站(http://queues.io/)介绍了队列化软件，其中有些基于Python开发的。


