# 日期和时间模块-`arrow`日期时间模块

[[toc]]

## 简介

官方介绍如下：

> **Arrow** is a Python library that offers a sensible and human-friendly approach to creating, manipulating, formatting and  converting dates, times and timestamps. It implements and updates the  datetime type, plugging gaps in functionality and providing an  intelligent module API that supports many common creation scenarios.  Simply put, it helps you work with dates and times with fewer imports  and a lot less code.
>
> Arrow is named after the [arrow of time](https://en.wikipedia.org/wiki/Arrow_of_time) and is heavily inspired by [moment.js](https://github.com/moment/moment) and [requests](https://github.com/psf/requests).

即：Arrow是一个Python库，它提供了一种明智且人性化的方法来创建、处理、格式化和转换日期、时间和时间戳。 它实现并更新了日期时间类型，填补了功能上的空白，并提供了支持许多常见创建方案的智能模块API。 简而言之，它可以帮助您以更少的导入和更少的代码来处理日期和时间。

Arrow以(Arrow of time)时间之箭命名，灵感来自moment.js和requests模块。

## 为什么在内置模块上使用Arrow？

Python的标准库和其他一些底层模块具有几乎完整的日期，时间和时区功能，但是从可用性的角度来看，效果并不理想：

 太多模块：`datetime`，`time`，`calendar`，`dateutil`，`pytz`等。

 类型太多：`date`，`time`，`datetime`，`tzinfo`，`timedelta`，`relativedelta`等。

 时区和时间戳转换是冗长不方便的。

 时区朴素(即无时区信息)是常态。

 功能上的差距：ISO 8601解析，时间跨度，人性化等。

## 安装

```sh
$ pip install arrow
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting arrow
  Downloading http://mirrors.aliyun.com/pypi/packages/99/b5/1f1c5ef3156f7b514c58613fe56e5670dc56374ab744bd1eb653c95e16b5/arrow-0.15.6-py2.py3-none-any.whl (47 kB)
     |████████████████████████████████| 47 kB 2.1 MB/s
Requirement already satisfied: python-dateutil in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from arrow) (2.8.1)
Requirement already satisfied: six>=1.5 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from python-dateutil->arrow) (1.14.0)
Installing collected packages: arrow
Successfully installed arrow-0.15.6
```

查看`arrow`模块有哪些函数或方法：

```py
$ python3
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import arrow
>>> arrow.
arrow.api           arrow.ArrowFactory( arrow.formatter     arrow.now(          arrow.utcnow(
arrow.arrow         arrow.constants     arrow.get(          arrow.parser        arrow.util
arrow.Arrow(        arrow.factory       arrow.locales       arrow.ParserError(
>>> exit()
```

## 快速生成日期、时间字符串

```py
$ python3
Python 3.9.6 (default, Mar 10 2023, 20:16:38)
[Clang 14.0.3 (clang-1403.0.22.14.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import arrow
>>> now = arrow.now()
>>> now
<Arrow [2023-04-19T23:25:46.647980+08:00]>
>>> now.format(arrow.FORMAT_ATOM)
'2023-04-19 23:25:46+08:00'
>>> arrow.FORMAT_ATOM
'YYYY-MM-DD HH:mm:ssZZ'

# 快速生成日期字符串
>>> now.format('YYYYMMDD')
'20230419'

# 快速生成日期时间字符串
>>> now.format('YYYY年MM月DD日 HH:mm:ss')
'2023年04月19日 23:25:46'
>>> exit()
```

## 时区图

![时区图](/img/timezone.gif)

注：图中的GMT是指格林威治标准时间，也就是UTC标准时间，可参考[格林威治标准时间](http://www.shijian.cc/shiqu/184/) 。

## 创建

### 通过now或utcnow创建时间对象

创建现在时间更加简单！

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import arrow

>>> arrow.now?
Signature: arrow.now(tz=None)
Docstring:
Returns an :class:`Arrow <arrow.arrow.Arrow>` object, representing "now" in the given
timezone.

:param tz: (optional) A :ref:`timezone expression <tz-expr>`.  Defaults to local time.

Usage::

    >>> import arrow
    >>> arrow.now()
    <Arrow [2013-05-07T22:19:11.363410-07:00]>

    >>> arrow.now('US/Pacific')
    <Arrow [2013-05-07T22:19:15.251821-07:00]>

    >>> arrow.now('+02:00')
    <Arrow [2013-05-08T07:19:25.618646+02:00]>

    >>> arrow.now('local')
    <Arrow [2013-05-07T22:19:39.130059-07:00]>
File:      /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/arrow/api.py
Type:      function

>>>

# UTC标准时间
>>> arrow.utcnow()
<Arrow [2020-07-17T14:18:37.599051+00:00]>

# 自动判断本地时区，当前为北京时间
>>> arrow.now()
<Arrow [2020-07-17T22:18:42.111606+08:00]>

# 美国东部时间，加上时区参数字符串表示对应时区的当前时间
>>> arrow.now('US/Eastern')
<Arrow [2020-07-17T10:20:13.932694-04:00]>

>>>
# 西四区的时间
>>> arrow.now('-04:00')
<Arrow [2020-07-17T10:26:59.082865-04:00]>

# 中时区的时间，即UTC标准时间
>>> arrow.now('00:00')
<Arrow [2020-07-17T14:27:05.627601+00:00]>

# 东八区的时间
>>> arrow.now('08:00')
<Arrow [2020-07-17T22:27:09.674684+08:00]>

# 东八区的时间
>>> arrow.now('+08:00')
<Arrow [2020-07-17T22:27:14.788227+08:00]>
```

### 通过时间戳创建时间对象

通过时间戳创建时间对象时，时间戳支持`int`和`float`类型。

```python
# 获取当前标准时间
>>> now = arrow.utcnow()

>>> now
<Arrow [2020-07-17T14:45:11.070688+00:00]>

# 将标准时间转换成时间戳
>>> now.timestamp
1594997111

# 获取arrow.get的帮助信息，可以看到帮助信息非常多，最后按q退出帮助信息查看界面
>>> arrow.get?
Signature: arrow.get(*args, **kwargs)
Docstring:
Returns an :class:`Arrow <arrow.arrow.Arrow>` object based on flexible inputs.

:param locale: (optional) a ``str`` specifying a locale for the parser. Defaults to
    'en_us'.
:param tzinfo: (optional) a :ref:`timezone expression <tz-expr>` or tzinfo object.
    Replaces the timezone unless using an input form that is explicitly UTC or specifies
    the timezone in a positional argument. Defaults to UTC.

Usage::

    >>> import arrow

**No inputs** to get current UTC time::

    >>> arrow.get()
    <Arrow [2013-05-08T05:51:43.316458+00:00]>

**None** to also get current UTC time::

    >>> arrow.get(None)
    <Arrow [2013-05-08T05:51:49.016458+00:00]>

**One** :class:`Arrow <arrow.arrow.Arrow>` object, to get a copy.

    >>> arw = arrow.utcnow()
    >>> arrow.get(arw)
    <Arrow [2013-10-23T15:21:54.354846+00:00]>

**One** ``float`` or ``int``, convertible to a floating-point timestamp, to get
that timestamp in UTC::

    >>> arrow.get(1367992474.293378)
    <Arrow [2013-05-08T05:54:34.293378+00:00]>

    >>> arrow.get(1367992474)
    <Arrow [2013-05-08T05:54:34+00:00]>

**One** ISO 8601-formatted ``str``, to parse it::

    >>> arrow.get('2013-09-29T01:26:43.830580')
    <Arrow [2013-09-29T01:26:43.830580+00:00]>

**One** ISO 8601-formatted ``str``, in basic format, to parse it::

    >>> arrow.get('20160413T133656.456289')
    <Arrow [2016-04-13T13:36:56.456289+00:00]>

**One** ``tzinfo``, to get the current time **converted** to that timezone::

    >>> arrow.get(tz.tzlocal())
    <Arrow [2013-05-07T22:57:28.484717-07:00]>

**One** naive ``datetime``, to get that datetime in UTC::

    >>> arrow.get(datetime(2013, 5, 5))
    <Arrow [2013-05-05T00:00:00+00:00]>

**One** aware ``datetime``, to get that datetime::

    >>> arrow.get(datetime(2013, 5, 5, tzinfo=tz.tzlocal()))
    <Arrow [2013-05-05T00:00:00-07:00]>

**One** naive ``date``, to get that date in UTC::

    >>> arrow.get(date(2013, 5, 5))
    <Arrow [2013-05-05T00:00:00+00:00]>

**One** time.struct time::

    >>> arrow.get(gmtime(0))
    <Arrow [1970-01-01T00:00:00+00:00]>

**One** iso calendar ``tuple``, to get that week date in UTC::

    >>> arrow.get((2013, 18, 7))
    <Arrow [2013-05-05T00:00:00+00:00]>

**Two** arguments, a naive or aware ``datetime``, and a replacement
:ref:`timezone expression <tz-expr>`::

    >>> arrow.get(datetime(2013, 5, 5), 'US/Pacific')
    <Arrow [2013-05-05T00:00:00-07:00]>

**Two** arguments, a naive ``date``, and a replacement
:ref:`timezone expression <tz-expr>`::

    >>> arrow.get(date(2013, 5, 5), 'US/Pacific')
    <Arrow [2013-05-05T00:00:00-07:00]>

**Two** arguments, both ``str``, to parse the first according to the format of the second::

    >>> arrow.get('2013-05-05 12:30:45 America/Chicago', 'YYYY-MM-DD HH:mm:ss ZZZ')
    <Arrow [2013-05-05T12:30:45-05:00]>

**Two** arguments, first a ``str`` to parse and second a ``list`` of formats to try::

    >>> arrow.get('2013-05-05 12:30:45', ['MM/DD/YYYY', 'YYYY-MM-DD HH:mm:ss'])
    <Arrow [2013-05-05T12:30:45+00:00]>

**Three or more** arguments, as for the constructor of a ``datetime``::

    >>> arrow.get(2013, 5, 5, 12, 30, 45)
    <Arrow [2013-05-05T12:30:45+00:00]>
File:      /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/arrow/api.py
Type:      function
(END)
    
# 通过时间戳获取时间对象    
>>> arrow.get(1594997111)
<Arrow [2020-07-17T14:45:11+00:00]>

>>> arrow.get(1594997112)
<Arrow [2020-07-17T14:45:12+00:00]>

>>> arrow.get(1594997113)
<Arrow [2020-07-17T14:45:13+00:00]>

>>> arrow.get(1594997113.4343)
<Arrow [2020-07-17T14:45:13.434300+00:00]>
```

### 通过无时区/有时区信息的datetime或者指定时区

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import arrow

>>> from datetime import datetime

>>> from dateutil import tz

>>> arrow.get(datetime.utcnow())
<Arrow [2020-07-18T12:21:17.701713+00:00]>

>>> arrow.get(datetime(2020, 7, 18), 'US/Eastern')
<Arrow [2020-07-18T00:00:00-04:00]>

>>> arrow.get(datetime(2020, 7, 18), tz.gettz('US/Eastern'))
<Arrow [2020-07-18T00:00:00-04:00]>

>>> arrow.get(datetime.now(tz.gettz('US/Eastern')))
<Arrow [2020-07-18T08:23:01.146618-04:00]>

>>>
```

### 通过解析时间字符串

```python
>>> arrow.get('2020-07-18 20:24:45', 'YYYY-MM-DD HH:mm:ss')
<Arrow [2020-07-18T20:24:45+00:00]>
```

### 在字符串中搜索时间对象

```python
>>> arrow.get('June was born in May 1980', 'MMMM YYYY')
<Arrow [1980-05-01T00:00:00+00:00]>
```

### 在不使用格式字符串的情况下，可以识别和解析一些符合ISO 8601的字符串

```python
>>> arrow.get('2013-09-30T15:34:00.000-07:00')
<Arrow [2013-09-30T15:34:00-07:00]>

>>> arrow.get('2020-07-19T20:28:00.000-08:00')
<Arrow [2020-07-19T20:28:00-08:00]>
```

### 直接实例化

Arrow对象也可以直接实例化，只需要传入类似`datetime`对象一样的参数即可。

```python
>>> arrow.get(2020,7,18,20,29,30)
<Arrow [2020-07-18T20:29:30+00:00]>

>>> arrow.get(2020,7,18)
<Arrow [2020-07-18T00:00:00+00:00]>

>>> arrow.Arrow(2020,7,18)
<Arrow [2020-07-18T00:00:00+00:00]>

>>> arrow.Arrow(2020,7,18,20,29,30)
<Arrow [2020-07-18T20:29:30+00:00]>
```

## 获取属性

### `datetime`对象

获取`datetime`属性：

```python
# 获取当前UTC标准时间
>>> a = arrow.utcnow()

>>> a
<Arrow [2020-07-18T13:19:35.632796+00:00]>

获取datetime属性，返回datetime对象
>>> a.datetime
datetime.datetime(2020, 7, 18, 13, 19, 35, 632796, tzinfo=tzutc())
```

### `timestamp`时间戳

获取`timestamp`时间戳：

```python
>>> a.timestamp
1595078375
```

### 无时区`datetime`对象和`tzinfo`

可以通过`naive`属性获取无时区`datetime`对象，`tzinfo`属性获取tzinfo信息。

```python
# 无时区`datetime`对象
>>> a.naive
datetime.datetime(2020, 7, 18, 13, 19, 35, 632796)

# 时区信息
>>> a.tzinfo
tzutc()
```

### datetime年月月等信息

```python
# 年
>>> a.year
2020

# 月
>>> a.month
7

# 日
>>> a.day
18

# 小时
>>> a.hour
13

# 分钟
>>> a.minute
19

# 秒
>>> a.second
35

# 微秒
>>> a.microsecond
632796
```

### 调用datetime的功能返回属性值

```python
# 获取日期信息
>>> a.date()
datetime.date(2020, 7, 18)

# 获取时间信息
>>> a.time()
datetime.time(13, 19, 35, 632796)
```

## Replace替换或Shift移位

你可以像datetime一样，对arrow对象进行替换和修改。注意，替换或移位时不会对原来的对象进行修改，只会生成一个新的对象。

```python
# 查年Arrow对象
>>> a
<Arrow [2020-07-18T13:19:35.632796+00:00]>

# 查看replace方法的帮助信息
>>> a.replace?
Signature: a.replace(**kwargs)
Docstring:
Returns a new :class:`Arrow <arrow.arrow.Arrow>` object with attributes updated
according to inputs.

Use property names to set their value absolutely::

    >>> import arrow
    >>> arw = arrow.utcnow()
    >>> arw
    <Arrow [2013-05-11T22:27:34.787885+00:00]>
    >>> arw.replace(year=2014, month=6)
    <Arrow [2014-06-11T22:27:34.787885+00:00]>

You can also replace the timezone without conversion, using a
:ref:`timezone expression <tz-expr>`::

    >>> arw.replace(tzinfo=tz.tzlocal())
    <Arrow [2013-05-11T22:27:34.787885-07:00]>
File:      /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/arrow/arrow.py
Type:      method

# 进行替换，生成一个新的Arrow对象
# 对年月日小时分钟秒和微秒都可以进行替换
>>> a.replace(year=2021,month=8,day=9,hour=19,minute=25,second=15,microsecond=1234)
<Arrow [2021-08-09T19:25:15.001234+00:00]>

# 查看原来的Arrow对象，并没有更新
>>> a
<Arrow [2020-07-18T13:19:35.632796+00:00]>

# 也可以对时区进行替换，可以直接以时区数字表示，也可以用英文方式表示
# 替换成西四区
>>> a.replace(tzinfo='-04:00')
<Arrow [2020-07-18T13:19:35.632796-04:00]>

# 替换成东八区
>>> a.replace(tzinfo='+08:00')
<Arrow [2020-07-18T13:19:35.632796+08:00]>

# 也可以直接使用timezone信息代替
>>> a.replace(tzinfo='US/Eastern')
<Arrow [2020-07-18T13:19:35.632796-04:00]>

>>> a.replace(tzinfo='US/eastErn')
<Arrow [2020-07-18T13:19:35.632796-04:00]>

>>> a.replace(tzinfo='us/eastErn')
<Arrow [2020-07-18T13:19:35.632796-04:00]>

>>> a.replace(tzinfo='Asia/Shanghai')
<Arrow [2020-07-18T13:19:35.632796+08:00]>
```

或者直接使用`shift`来向前或向后改变属性：

```python
>>> a.shift?
Signature: a.shift(**kwargs)
Docstring:
Returns a new :class:`Arrow <arrow.arrow.Arrow>` object with attributes updated
according to inputs.

Use pluralized property names to relatively shift their current value:

>>> import arrow
>>> arw = arrow.utcnow()
>>> arw
<Arrow [2013-05-11T22:27:34.787885+00:00]>
>>> arw.shift(years=1, months=-1)
<Arrow [2014-04-11T22:27:34.787885+00:00]>

Day-of-the-week relative shifting can use either Python's weekday numbers
(Monday = 0, Tuesday = 1 .. Sunday = 6) or using dateutil.relativedelta's
day instances (MO, TU .. SU).  When using weekday numbers, the returned
date will always be greater than or equal to the starting date.

Using the above code (which is a Saturday) and asking it to shift to Saturday:

>>> arw.shift(weekday=5)
<Arrow [2013-05-11T22:27:34.787885+00:00]>

While asking for a Monday:

>>> arw.shift(weekday=0)
<Arrow [2013-05-13T22:27:34.787885+00:00]>
File:      /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/arrow/arrow.py
Type:      method

>>> a
<Arrow [2020-07-18T13:19:35.632796+00:00]>


# 差一个月一年后的日期
>>> a.shift(years=+1, months=-1)
<Arrow [2021-06-18T13:19:35.632796+00:00]>

# 一年又一个月后的日期
>>> a.shift(years=+1, months=+1)
<Arrow [2021-08-18T13:19:35.632796+00:00]>

# 一年前一个月后的日期
>>> a.shift(years=-1, months=+1)
<Arrow [2019-08-18T13:19:35.632796+00:00]>

# 两天后的日期
>>> a.shift(days=+2)
<Arrow [2020-07-20T13:19:35.632796+00:00]>

# 两天前的日期
>>> a.shift(days=-2)
<Arrow [2020-07-16T13:19:35.632796+00:00]>

# 周一的日期
>>> a.shift(weekday=0)
<Arrow [2020-07-20T13:19:35.632796+00:00]>

# 周二的日期
>>> a.shift(weekday=1)
<Arrow [2020-07-21T13:19:35.632796+00:00]>

# 周三的日期
>>> a.shift(weekday=2)
<Arrow [2020-07-22T13:19:35.632796+00:00]>

# 周四的日期
>>> a.shift(weekday=3)
<Arrow [2020-07-23T13:19:35.632796+00:00]>

# 周五的日期
>>> a.shift(weekday=4)
<Arrow [2020-07-24T13:19:35.632796+00:00]>

# 周六的日期，就是今天！！！
>>> a.shift(weekday=5)
<Arrow [2020-07-18T13:19:35.632796+00:00]>

# 周日的日期，明天！
>>> a.shift(weekday=6)
<Arrow [2020-07-19T13:19:35.632796+00:00]>
```

## 格式化

可以使用format方法进对arrow对象进行格式化。

```python
>>> a.format?
Signature: a.format(fmt='YYYY-MM-DD HH:mm:ssZZ', locale='en_us')
Docstring:
Returns a string representation of the :class:`Arrow <arrow.arrow.Arrow>` object,
formatted according to a format string.

:param fmt: the format string.

Usage::

    >>> arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')
    '2013-05-09 03:56:47 -00:00'

    >>> arrow.utcnow().format('X')
    '1368071882'

    >>> arrow.utcnow().format('MMMM DD, YYYY')
    'May 09, 2013'

    >>> arrow.utcnow().format()
    '2013-05-09 03:56:47 -00:00'
File:      /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/arrow/arrow.py
Type:      method
  

>>> a.format()
'2020-07-18 13:19:35+00:00'

>>> a.format('YYYY-MM-DD HH:mm:ss ZZ')
'2020-07-18 13:19:35 +00:00'

>>> a.format('X')
'1595078375'

>>> a.format('MMMM DD, YYYY')
'July 18, 2020'

>>> a.format('MMM DD, YYYY')
'Jul 18, 2020'

>>> a.format('MM DD, YYYY')
'07 18, 2020'
```

## 时区转换

可以很好地将UTC标准时间转换成其他时区的时间：

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> from dateutil import tz

>>> import arrow

>>> utcnow = arrow.utcnow()

# UTC标准时间
>>> utcnow
<Arrow [2020-07-20T12:06:49.508271+00:00]>

# 转换成美国东部时区时间
>>> utcnow.to('US/Eastern')
<Arrow [2020-07-20T08:06:49.508271-04:00]>

# 转换成中国时间
>>> utcnow.to('Asia/Shanghai')
<Arrow [2020-07-20T20:06:49.508271+08:00]>

# 也可以通过tz.gettz来指定时区
>>> utcnow.to(tz.gettz('Asia/Shanghai'))
<Arrow [2020-07-20T20:06:49.508271+08:00]>

>>> utcnow.to(tz.gettz('US/Eastern'))
<Arrow [2020-07-20T08:06:49.508271-04:00]>

>>> tz.gettz('Asia/Shanghai')
tzfile('/usr/share/zoneinfo/Asia/Shanghai')

>>> tz.gettz('US/Eastern')
tzfile('/usr/share/zoneinfo/US/Eastern')
```

也可以使用一些速记方式：

```python
# 转化成本地时间
>>> utcnow.to('local')
<Arrow [2020-07-20T20:06:49.508271+08:00]>

# 转换成UTC标准时间
>>> utcnow.to('local').to('utc')
<Arrow [2020-07-20T12:06:49.508271+00:00]>
```

## 人性化设置

时间的相对关系更加人性化：

```python
# 过去的时间
# 6秒前
>>> past = arrow.utcnow().shift(seconds=-6)

>>> past.humanize()
'just now'

# 6分钟前
>>> past = arrow.utcnow().shift(minutes=-6)

>>> past.humanize()
'6 minutes ago'

# 1小时前
>>> past = arrow.utcnow().shift(hours=-1)

>>> past
<Arrow [2020-07-20T12:32:57.575819+00:00]>

>>> past.humanize()
'an hour ago'

# 两小时前
>>> past = arrow.utcnow().shift(hours=-2)

>>> past.humanize()
'2 hours ago'

# 三小时前
>>> past = arrow.utcnow().shift(hours=-3)

>>> past.humanize()
'3 hours ago'

# 1天前
>>> past = arrow.utcnow().shift(days=-1)

>>> past.humanize()
'a day ago'

# 两天前
>>> past = arrow.utcnow().shift(days=-2)

>>> past.humanize()
'2 days ago'

# 31天前，程序自动考虑为1个月前
>>> past = arrow.utcnow().shift(days=-31)

>>> past.humanize()
'a month ago'

# 30天前，程序自动考虑为1个月前
>>> past = arrow.utcnow().shift(days=-30)

>>> past.humanize()
'a month ago'

# 1年1个月前
>>> past = arrow.utcnow().shift(years=-1, days=-30)

>>> past.humanize()
'a year ago'

# 未来的时间
# 五分钟后
>>> future = arrow.utcnow().shift(minutes=6)

>>> future.humanize()
'in 5 minutes'

>>> future.humanize(locale='zh')
'5分钟后'

# 2小时后
>>> future = arrow.utcnow().shift(hours=3)

>>> future.humanize()
'in 2 hours'

# 切换语言
>>> future.humanize(locale='zh')
'2小时后'

# 2天后
>>> future = arrow.utcnow().shift(days=3)

>>> future.humanize()
'in 2 days'

>>> future.humanize(locale='zh')
'2天后'

# 6个月后
>>> future = arrow.utcnow().shift(months=6)

>>> future.humanize()
'in 6 months'

>>> future.humanize(locale='zh')
'6个月后'

# 11个月后
>>> future = arrow.utcnow().shift(years=1, days=-30)

>>> future.humanize()
'in 11 months'

>>> future.humanize(locale='zh')
'11个月后'


# 法语的11个月后
>>> future.humanize(locale='fr')
'dans 11 mois'

# 日语的11个月后
>>> future.humanize(locale='ja')
'11ヶ月後'

# 韩语的11个月后
>>> future.humanize(locale='ko')
'11개월 후'

# 德语的11个月后
>>> future.humanize(locale='de')
'in 11 Monaten'
```

查看所有支持的语言：

```python
>>> from arrow.locales import _locales

>>> _locales
{'af': arrow.locales.AfrikaansLocale,
 'af_nl': arrow.locales.AfrikaansLocale,
 'ar_tn': arrow.locales.AlgeriaTunisiaArabicLocale,
 'ar_dz': arrow.locales.AlgeriaTunisiaArabicLocale,
 'ar': arrow.locales.ArabicLocale,
 'ar_ae': arrow.locales.ArabicLocale,
 'ar_bh': arrow.locales.ArabicLocale,
 'ar_dj': arrow.locales.ArabicLocale,
 'ar_eg': arrow.locales.ArabicLocale,
 'ar_eh': arrow.locales.ArabicLocale,
 'ar_er': arrow.locales.ArabicLocale,
 'ar_km': arrow.locales.ArabicLocale,
 'ar_kw': arrow.locales.ArabicLocale,
 'ar_ly': arrow.locales.ArabicLocale,
 'ar_om': arrow.locales.ArabicLocale,
 'ar_qa': arrow.locales.ArabicLocale,
 'ar_sa': arrow.locales.ArabicLocale,
 'ar_sd': arrow.locales.ArabicLocale,
 'ar_so': arrow.locales.ArabicLocale,
 'ar_ss': arrow.locales.ArabicLocale,
 'ar_td': arrow.locales.ArabicLocale,
 'ar_ye': arrow.locales.ArabicLocale,
 'de_at': arrow.locales.AustrianLocale,
 'az': arrow.locales.AzerbaijaniLocale,
 'az_az': arrow.locales.AzerbaijaniLocale,
 'eu': arrow.locales.BasqueLocale,
 'eu_eu': arrow.locales.BasqueLocale,
 'be': arrow.locales.BelarusianLocale,
 'be_by': arrow.locales.BelarusianLocale,
 'bn': arrow.locales.BengaliLocale,
 'bn_bd': arrow.locales.BengaliLocale,
 'bn_in': arrow.locales.BengaliLocale,
 'pt_br': arrow.locales.BrazilianPortugueseLocale,
 'bg': arrow.locales.BulgarianLocale,
 'bg_bg': arrow.locales.BulgarianLocale,
 'ca': arrow.locales.CatalanLocale,
 'ca_es': arrow.locales.CatalanLocale,
 'ca_ad': arrow.locales.CatalanLocale,
 'ca_fr': arrow.locales.CatalanLocale,
 'ca_it': arrow.locales.CatalanLocale,
 'zh': arrow.locales.ChineseCNLocale,
 'zh_cn': arrow.locales.ChineseCNLocale,
 'zh_tw': arrow.locales.ChineseTWLocale,
 'cs': arrow.locales.CzechLocale,
 'cs_cz': arrow.locales.CzechLocale,
 'da': arrow.locales.DanishLocale,
 'da_dk': arrow.locales.DanishLocale,
 'nl': arrow.locales.DutchLocale,
 'nl_nl': arrow.locales.DutchLocale,
 'en': arrow.locales.EnglishLocale,
 'en_us': arrow.locales.EnglishLocale,
 'en_gb': arrow.locales.EnglishLocale,
 'en_au': arrow.locales.EnglishLocale,
 'en_be': arrow.locales.EnglishLocale,
 'en_jp': arrow.locales.EnglishLocale,
 'en_za': arrow.locales.EnglishLocale,
 'en_ca': arrow.locales.EnglishLocale,
 'en_ph': arrow.locales.EnglishLocale,
 'eo': arrow.locales.EsperantoLocale,
 'eo_xx': arrow.locales.EsperantoLocale,
 'ee': arrow.locales.EstonianLocale,
 'et': arrow.locales.EstonianLocale,
 'fa': arrow.locales.FarsiLocale,
 'fa_ir': arrow.locales.FarsiLocale,
 'fi': arrow.locales.FinnishLocale,
 'fi_fi': arrow.locales.FinnishLocale,
 'fr': arrow.locales.FrenchLocale,
 'fr_fr': arrow.locales.FrenchLocale,
 'de': arrow.locales.GermanLocale,
 'de_de': arrow.locales.GermanLocale,
 'el': arrow.locales.GreekLocale,
 'el_gr': arrow.locales.GreekLocale,
 'he': arrow.locales.HebrewLocale,
 'he_il': arrow.locales.HebrewLocale,
 'hi': arrow.locales.HindiLocale,
 'zh_hk': arrow.locales.HongKongLocale,
 'hu': arrow.locales.HungarianLocale,
 'hu_hu': arrow.locales.HungarianLocale,
 'is': arrow.locales.IcelandicLocale,
 'is_is': arrow.locales.IcelandicLocale,
 'id': arrow.locales.IndonesianLocale,
 'id_id': arrow.locales.IndonesianLocale,
 'it': arrow.locales.ItalianLocale,
 'it_it': arrow.locales.ItalianLocale,
 'ja': arrow.locales.JapaneseLocale,
 'ja_jp': arrow.locales.JapaneseLocale,
 'ko': arrow.locales.KoreanLocale,
 'ko_kr': arrow.locales.KoreanLocale,
 'ar_iq': arrow.locales.LevantArabicLocale,
 'ar_jo': arrow.locales.LevantArabicLocale,
 'ar_lb': arrow.locales.LevantArabicLocale,
 'ar_ps': arrow.locales.LevantArabicLocale,
 'ar_sy': arrow.locales.LevantArabicLocale,
 'mk': arrow.locales.MacedonianLocale,
 'mk_mk': arrow.locales.MacedonianLocale,
 'ml': arrow.locales.MalayalamLocale,
 'mr': arrow.locales.MarathiLocale,
 'ar_mr': arrow.locales.MauritaniaArabicLocale,
 'ar_ma': arrow.locales.MoroccoArabicLocale,
 'ne': arrow.locales.NepaliLocale,
 'ne_np': arrow.locales.NepaliLocale,
 'nn': arrow.locales.NewNorwegianLocale,
 'nn_no': arrow.locales.NewNorwegianLocale,
 'nb': arrow.locales.NorwegianLocale,
 'nb_no': arrow.locales.NorwegianLocale,
 'pl': arrow.locales.PolishLocale,
 'pl_pl': arrow.locales.PolishLocale,
 'pt': arrow.locales.PortugueseLocale,
 'pt_pt': arrow.locales.PortugueseLocale,
 'ro': arrow.locales.RomanianLocale,
 'ro_ro': arrow.locales.RomanianLocale,
 'rm': arrow.locales.RomanshLocale,
 'rm_ch': arrow.locales.RomanshLocale,
 'ru': arrow.locales.RussianLocale,
 'ru_ru': arrow.locales.RussianLocale,
 'sk': arrow.locales.SlovakLocale,
 'sk_sk': arrow.locales.SlovakLocale,
 'sl': arrow.locales.SlovenianLocale,
 'sl_si': arrow.locales.SlovenianLocale,
 'es': arrow.locales.SpanishLocale,
 'es_es': arrow.locales.SpanishLocale,
 'sv': arrow.locales.SwedishLocale,
 'sv_se': arrow.locales.SwedishLocale,
 'de_ch': arrow.locales.SwissLocale,
 'tl': arrow.locales.TagalogLocale,
 'tl_ph': arrow.locales.TagalogLocale,
 'th': arrow.locales.ThaiLocale,
 'th_th': arrow.locales.ThaiLocale,
 'tr': arrow.locales.TurkishLocale,
 'tr_tr': arrow.locales.TurkishLocale,
 'ua': arrow.locales.UkrainianLocale,
 'uk_ua': arrow.locales.UkrainianLocale,
 'vi': arrow.locales.VietnameseLocale,
 'vi_vn': arrow.locales.VietnameseLocale}

>>>
```

## Range范围或Span跨度

获取时间跨度：

```python
>>> utcnow
<Arrow [2020-07-20T12:06:49.508271+00:00]>

>>> utcnow.span('hour')
(<Arrow [2020-07-20T12:00:00+00:00]>,
 <Arrow [2020-07-20T12:59:59.999999+00:00]>)

>>> utcnow.span('minute')
(<Arrow [2020-07-20T12:06:00+00:00]>,
 <Arrow [2020-07-20T12:06:59.999999+00:00]>)

>>> utcnow.span('second')
(<Arrow [2020-07-20T12:06:49+00:00]>,
 <Arrow [2020-07-20T12:06:49.999999+00:00]>)

>>> utcnow.span('day')
(<Arrow [2020-07-20T00:00:00+00:00]>,
 <Arrow [2020-07-20T23:59:59.999999+00:00]>)

>>> utcnow.span('month')
(<Arrow [2020-07-01T00:00:00+00:00]>,
 <Arrow [2020-07-31T23:59:59.999999+00:00]>)

>>> utcnow.span('year')
(<Arrow [2020-01-01T00:00:00+00:00]>,
 <Arrow [2020-12-31T23:59:59.999999+00:00]>)
```

时间向上或向下取值：

```python
# 现在时间
>>> utcnow
<Arrow [2020-07-20T12:06:49.508271+00:00]>

# 向下取值
>>> utcnow.floor('hour')
<Arrow [2020-07-20T12:00:00+00:00]>

# 向上取值
>>> utcnow.ceil('hour')
<Arrow [2020-07-20T12:59:59.999999+00:00]>

# 向上取值
>>> utcnow.ceil('minute')
<Arrow [2020-07-20T12:06:59.999999+00:00]>

# 向下取值
>>> utcnow.floor('minute')
<Arrow [2020-07-20T12:06:00+00:00]>

# 向下取值
>>> utcnow.floor('day')
<Arrow [2020-07-20T00:00:00+00:00]>

# 向上取值
>>> utcnow.ceil('day')
<Arrow [2020-07-20T23:59:59.999999+00:00]>
```

你也可以获取指定时间区域的时间跨度：

```python
>>> yesterday = utcnow.shift(days=-1)

>>> yesterday
<Arrow [2020-07-19T12:06:49.508271+00:00]>

>>> for r in arrow.Arrow.span_range('hour', yesterday, utcnow):
...     print(r)
...
(<Arrow [2020-07-19T12:00:00+00:00]>, <Arrow [2020-07-19T12:59:59.999999+00:00]>)
(<Arrow [2020-07-19T13:00:00+00:00]>, <Arrow [2020-07-19T13:59:59.999999+00:00]>)
(<Arrow [2020-07-19T14:00:00+00:00]>, <Arrow [2020-07-19T14:59:59.999999+00:00]>)
(<Arrow [2020-07-19T15:00:00+00:00]>, <Arrow [2020-07-19T15:59:59.999999+00:00]>)
(<Arrow [2020-07-19T16:00:00+00:00]>, <Arrow [2020-07-19T16:59:59.999999+00:00]>)
(<Arrow [2020-07-19T17:00:00+00:00]>, <Arrow [2020-07-19T17:59:59.999999+00:00]>)
(<Arrow [2020-07-19T18:00:00+00:00]>, <Arrow [2020-07-19T18:59:59.999999+00:00]>)
(<Arrow [2020-07-19T19:00:00+00:00]>, <Arrow [2020-07-19T19:59:59.999999+00:00]>)
(<Arrow [2020-07-19T20:00:00+00:00]>, <Arrow [2020-07-19T20:59:59.999999+00:00]>)
(<Arrow [2020-07-19T21:00:00+00:00]>, <Arrow [2020-07-19T21:59:59.999999+00:00]>)
(<Arrow [2020-07-19T22:00:00+00:00]>, <Arrow [2020-07-19T22:59:59.999999+00:00]>)
(<Arrow [2020-07-19T23:00:00+00:00]>, <Arrow [2020-07-19T23:59:59.999999+00:00]>)
(<Arrow [2020-07-20T00:00:00+00:00]>, <Arrow [2020-07-20T00:59:59.999999+00:00]>)
(<Arrow [2020-07-20T01:00:00+00:00]>, <Arrow [2020-07-20T01:59:59.999999+00:00]>)
(<Arrow [2020-07-20T02:00:00+00:00]>, <Arrow [2020-07-20T02:59:59.999999+00:00]>)
(<Arrow [2020-07-20T03:00:00+00:00]>, <Arrow [2020-07-20T03:59:59.999999+00:00]>)
(<Arrow [2020-07-20T04:00:00+00:00]>, <Arrow [2020-07-20T04:59:59.999999+00:00]>)
(<Arrow [2020-07-20T05:00:00+00:00]>, <Arrow [2020-07-20T05:59:59.999999+00:00]>)
(<Arrow [2020-07-20T06:00:00+00:00]>, <Arrow [2020-07-20T06:59:59.999999+00:00]>)
(<Arrow [2020-07-20T07:00:00+00:00]>, <Arrow [2020-07-20T07:59:59.999999+00:00]>)
(<Arrow [2020-07-20T08:00:00+00:00]>, <Arrow [2020-07-20T08:59:59.999999+00:00]>)
(<Arrow [2020-07-20T09:00:00+00:00]>, <Arrow [2020-07-20T09:59:59.999999+00:00]>)
(<Arrow [2020-07-20T10:00:00+00:00]>, <Arrow [2020-07-20T10:59:59.999999+00:00]>)
(<Arrow [2020-07-20T11:00:00+00:00]>, <Arrow [2020-07-20T11:59:59.999999+00:00]>)
(<Arrow [2020-07-20T12:00:00+00:00]>, <Arrow [2020-07-20T12:59:59.999999+00:00]>)

>>>
```

或者仅遍历一段时间：

```python
>>> yesterday = utcnow.shift(days=-1)

>>> yesterday
<Arrow [2020-07-19T12:06:49.508271+00:00]>

>>> for r in arrow.Arrow.range('hour', yesterday, utcnow):
...     print(repr(r))
...
<Arrow [2020-07-19T12:06:49.508271+00:00]>
<Arrow [2020-07-19T13:06:49.508271+00:00]>
<Arrow [2020-07-19T14:06:49.508271+00:00]>
<Arrow [2020-07-19T15:06:49.508271+00:00]>
<Arrow [2020-07-19T16:06:49.508271+00:00]>
<Arrow [2020-07-19T17:06:49.508271+00:00]>
<Arrow [2020-07-19T18:06:49.508271+00:00]>
<Arrow [2020-07-19T19:06:49.508271+00:00]>
<Arrow [2020-07-19T20:06:49.508271+00:00]>
<Arrow [2020-07-19T21:06:49.508271+00:00]>
<Arrow [2020-07-19T22:06:49.508271+00:00]>
<Arrow [2020-07-19T23:06:49.508271+00:00]>
<Arrow [2020-07-20T00:06:49.508271+00:00]>
<Arrow [2020-07-20T01:06:49.508271+00:00]>
<Arrow [2020-07-20T02:06:49.508271+00:00]>
<Arrow [2020-07-20T03:06:49.508271+00:00]>
<Arrow [2020-07-20T04:06:49.508271+00:00]>
<Arrow [2020-07-20T05:06:49.508271+00:00]>
<Arrow [2020-07-20T06:06:49.508271+00:00]>
<Arrow [2020-07-20T07:06:49.508271+00:00]>
<Arrow [2020-07-20T08:06:49.508271+00:00]>
<Arrow [2020-07-20T09:06:49.508271+00:00]>
<Arrow [2020-07-20T10:06:49.508271+00:00]>
<Arrow [2020-07-20T11:06:49.508271+00:00]>
<Arrow [2020-07-20T12:06:49.508271+00:00]>

>>>
```



## 工厂模式

使用工厂模式将Arrow的模块API应用于自定义的Arrow衍生类型。 首先，编写您的自定义类，以及相应的方法，然后获取并使用工厂函数。

如下面的定义的`CustomArrow`类继承自`Arrow`类，并在其中定义了一个`days_till_xmas`方法。通过`ArrowFactory(CustomArrow)`构建一个工厂对象，然后再生成一个Arrow时间对象，最后调用自定义的`days_till_xmas`方法！

在pycham中测试：

```python
from arrow import Arrow, ArrowFactory


class CustomArrow(Arrow):
    """使用arrow模块的工厂模式进行自定义模块功能开发"""

    def days_till_xmas(self):
        """距离圣诞节的天数"""
        xmas = Arrow(self.year, 12, 25)
        if self > xmas:
            xmas = xmas.shift(years=1)

        return (xmas - self).days


def main():
    """测试使用工厂模块的函数"""
    factory = ArrowFactory(CustomArrow)
    custom = factory.utcnow()
    print(custom)
    print(custom.days_till_xmas())
    

if __name__ == '__main__':
    main()

# output:
# 2020-07-20T14:27:53.958652+00:00
# 157
```

在ipython中测试：

```python
>>> from arrow import Arrow, ArrowFactory
...
...
... class CustomArrow(Arrow):
...     """使用arrow模块的工厂模式进行自定义模块功能开发"""
...
...     def days_till_xmas(self):
...         """距离圣诞节的天数"""
...         xmas = Arrow(self.year, 12, 25)
...         if self > xmas:
...             xmas = xmas.shift(years=1)
...
...         return (xmas - self).days
...

>>> factory = ArrowFactory(CustomArrow)

>>> custom = factory.utcnow()

>>> custom
<CustomArrow [2020-07-20T14:30:46.109427+00:00]>

>>> custom.days_till_xmas()
157

>>>
```

## 支持的令牌

使用以下标记进行解析和格式化。 请注意，它们与strptime的令牌不同：

|                                        | Token令牌 | Output输出                                                   |
| -------------------------------------- | --------- | ------------------------------------------------------------ |
| **Year年**                             | YYYY      | 2000, 2001, 2002 … 2012, 2013                                |
|                                        | YY        | 00, 01, 02 … 12, 13                                          |
| **Month月**                            | MMMM      | January, February, March … [1](https://arrow.readthedocs.io/en/latest/#t1) |
|                                        | MMM       | Jan, Feb, Mar … [1](https://arrow.readthedocs.io/en/latest/#t1) |
|                                        | MM        | 01, 02, 03 … 11, 12                                          |
|                                        | M         | 1, 2, 3 … 11, 12                                             |
| **Day of Year年中的某一天**            | DDDD      | 001, 002, 003 … 364, 365                                     |
|                                        | DDD       | 1, 2, 3 … 364, 365                                           |
| **Day of Month月中的某一天**           | DD        | 01, 02, 03 … 30, 31                                          |
|                                        | D         | 1, 2, 3 … 30, 31                                             |
|                                        | Do        | 1st, 2nd, 3rd … 30th, 31st                                   |
| **Day of Week周中的某一天**            | dddd      | Monday, Tuesday, Wednesday … [2](https://arrow.readthedocs.io/en/latest/#t2) |
|                                        | ddd       | Mon, Tue, Wed … [2](https://arrow.readthedocs.io/en/latest/#t2) |
|                                        | d         | 1, 2, 3 … 6, 7                                               |
| **ISO week date**                      | W         | 2011-W05-4, 2019-W17                                         |
| **Hour小时**                           | HH        | 00, 01, 02 … 23, 24                                          |
|                                        | H         | 0, 1, 2 … 23, 24                                             |
|                                        | hh        | 01, 02, 03 … 11, 12                                          |
|                                        | h         | 1, 2, 3 … 11, 12                                             |
| **AM / PM上午与下午**                  | A         | AM, PM, am, pm [1](https://arrow.readthedocs.io/en/latest/#t1) |
|                                        | a         | am, pm [1](https://arrow.readthedocs.io/en/latest/#t1)       |
| **Minute分钟**                         | mm        | 00, 01, 02 … 58, 59                                          |
|                                        | m         | 0, 1, 2 … 58, 59                                             |
| **Second秒**                           | ss        | 00, 01, 02 … 58, 59                                          |
|                                        | s         | 0, 1, 2 … 58, 59                                             |
| **Sub-second**                         | S…        | 0, 02, 003, 000006, 123123123123… [3](https://arrow.readthedocs.io/en/latest/#t3) |
| **Timezone时区**                       | ZZZ       | Asia/Baku, Europe/Warsaw, GMT … [4](https://arrow.readthedocs.io/en/latest/#t4) |
|                                        | ZZ        | -07:00, -06:00 … +06:00, +07:00, +08, Z                      |
|                                        | Z         | -0700, -0600 … +0600, +0700, +08, Z                          |
| **Seconds Timestamp秒时间戳**          | X         | 1381685817, 1381685817.915482 … [5](https://arrow.readthedocs.io/en/latest/#t5) |
| **ms or µs Timestamp毫秒与微秒时间戳** | x         | 1569980330813, 1569980330813221                              |

Footnotes脚注说明：

- 1([1](https://arrow.readthedocs.io/en/latest/#id1),[2](https://arrow.readthedocs.io/en/latest/#id2),[3](https://arrow.readthedocs.io/en/latest/#id5),[4](https://arrow.readthedocs.io/en/latest/#id6)) localization support for parsing and formatting
- 2([1](https://arrow.readthedocs.io/en/latest/#id3),[2](https://arrow.readthedocs.io/en/latest/#id4)) localization support only for formatting
- [3 ](https://arrow.readthedocs.io/en/latest/#id7) the result is truncated to microseconds, with [half-to-even rounding](https://en.wikipedia.org/wiki/IEEE_floating_point#Roundings_to_nearest).
- [4](https://arrow.readthedocs.io/en/latest/#id8)  timezone names from [tz database](https://www.iana.org/time-zones) provided via dateutil package
- [5](https://arrow.readthedocs.io/en/latest/#id9)  this token cannot be used for parsing timestamps out of natural language strings due to compatibility reasons



## 内置格式化

有几种格式标准作为内置令牌提供。看下面的示例。

可以通过以下方式查看arrow的版本信息：

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import arrow

>>> arrow.__version__
'0.15.8'
```



注意，内置格式化是在0.15.7版本引入的，如果你的arrow版本相对较低的话，可以使用以下命令升级arrow版本：

```sh
$ pip install -U arrow
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting arrow
  Downloading http://mirrors.aliyun.com/pypi/packages/40/2a/9dd6a391e7813b9908b4dcaec7df0f2d365cfc0f071799f2ae5147707923/arrow-0.15.8-py2.py3-none-any.whl (49 kB)
     |████████████████████████████████| 49 kB 4.3 MB/s
Requirement already satisfied, skipping upgrade: python-dateutil in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from arrow) (2.8.1)
Requirement already satisfied, skipping upgrade: six>=1.5 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from python-dateutil->arrow) (1.14.0)
Installing collected packages: arrow
  Attempting uninstall: arrow
    Found existing installation: arrow 0.15.6
    Uninstalling arrow-0.15.6:
      Successfully uninstalled arrow-0.15.6
Successfully installed arrow-0.15.8
```

[可以在这里看到提交修改信息](https://github.com/arrow-py/arrow/commit/22acd93050aa23147c9122f143a3069dc7f5b89f#diff-98102a005603dcf5eb33f3152fe5099e)，定义的几个内置格式化常量为：

```python
FORMAT_ATOM = "YYYY-MM-DD HH:mm:ssZZ"
FORMAT_COOKIE = "dddd, DD-MMM-YYYY HH:mm:ss ZZZ"
FORMAT_RFC822 = "ddd, DD MMM YY HH:mm:ss Z"
FORMAT_RFC850 = "dddd, DD-MMM-YY HH:mm:ss ZZZ"
FORMAT_RFC1036 = "ddd, DD MMM YY HH:mm:ss Z"
FORMAT_RFC1123 = "ddd, DD MMM YYYY HH:mm:ss Z"
FORMAT_RFC2822 = "ddd, DD MMM YYYY HH:mm:ss Z"
FORMAT_RFC3339 = "YYYY-MM-DD HH:mm:ssZZ"
FORMAT_RSS = "ddd, DD MMM YYYY HH:mm:ss Z"
FORMAT_W3C = "YYYY-MM-DD HH:mm:ssZZ"
```

我们来试一下，这些内置的格式化输出。

```python
# UTC标准时间
>>> now = arrow.utcnow()

>>> now
<Arrow [2020-07-25T09:53:41.904664+00:00]>

>>> now.format(arrow.FORMAT_ATOM)
'2020-07-25 09:53:41+00:00'

>>> now.format(arrow.FORMAT_COOKIE)
'Saturday, 25-Jul-2020 09:53:41 UTC'

>>> now.format(arrow.FORMAT_RFC822)
'Sat, 25 Jul 20 09:53:41 +0000'

>>> now.format(arrow.FORMAT_RFC850)
'Saturday, 25-Jul-20 09:53:41 UTC'

>>> now.format(arrow.FORMAT_RFC1036)
'Sat, 25 Jul 20 09:53:41 +0000'

>>> now.format(arrow.FORMAT_RFC1123)
'Sat, 25 Jul 2020 09:53:41 +0000'

>>> now.format(arrow.FORMAT_RFC2822)
'Sat, 25 Jul 2020 09:53:41 +0000'

>>> now.format(arrow.FORMAT_RFC3339)
'2020-07-25 09:53:41+00:00'

>>> now.format(arrow.FORMAT_RSS)
'Sat, 25 Jul 2020 09:53:41 +0000'

>>> now.format(arrow.FORMAT_W3C)
'2020-07-25 09:53:41+00:00'
```

我们可以选择一种自己看得顺眼的格式作为自己使用的格式化输出。



## 格式转义Escaping Format 

在解析和格式化时，可以将格式字符串中的标记，短语和正则表达式转义，方法是将它们括在方括号`[]`内。

### 解析或格式化

任何令牌或者格式化字符可以像下面这种方式进行转义。

```python
>>> fmt = "YYYY-MM-DD h [h] m"

>>> arw = arrow.get("2018-03-09 8 h 40", fmt)

>>> arw.format(fmt)
'2018-03-09 8 h 40'



>>> fmt = "YYYY-MM-DD h [hello] m"

>>> arw = arrow.get("2018-03-09 8 hello 40", fmt)

>>> arw
<Arrow [2018-03-09T08:40:00+00:00]>

>>> arw.format(fmt)
'2018-03-09 8 hello 40'


>>> fmt = "YYYY-MM-DD h [hello world] m"

>>> arw = arrow.get("2018-03-09 8 hello world 40", fmt)

>>> arw
<Arrow [2018-03-09T08:40:00+00:00]>

>>> arw.format(fmt)
'2018-03-09 8 hello world 40'
```

这对于解析不同语言环境（例如法语）中的日期很有用，在这种语言中，通常将时间字符串的格式设置为“8 h 40”而不是“ 8:40”。

### 正则表达式转义

您也可以通过将正则表达式括在方括号中来对它们进行转义。在以下示例中，我们使用正则表达式`\s+`来匹配任意数量的空白字符。如果您不能提前知道令牌之间的空格数（例如在日志文件中），这将很有用。

```python
>>> fmt = r"ddd[\s+]MMM[\s+]DD[\s+]HH:mm:ss[\s+]YYYY"

>>> arrow.get("Mon Sep 08 16:41:45 2014", fmt)
<Arrow [2014-09-08T16:41:45+00:00]>

>>> arrow.get("Mon    Sep    08 16:41:45 2014", fmt)
<Arrow [2014-09-08T16:41:45+00:00]>

>>> arrow.get("Mon \tSep 08   16:41:45     2014", fmt)
<Arrow [2014-09-08T16:41:45+00:00]>

>>> arrow.get("Mon Sep 08   16:41:45   2014", fmt)
<Arrow [2014-09-08T16:41:45+00:00]>
```

### 标点符号转义

日期格式可能在下面的列表中的任何一个标点符号两侧`, . ; : ? ! "  ' [ ] { } ( ) < >`

```python
>>> arrow.get("Tomorrow (2019-10-31) is Halloween!", "YYYY-MM-DD")
<Arrow [2019-10-31T00:00:00+00:00]>

>>> arrow.get("Halloween is on 2019.10.31.", "YYYY.MM.DD")
<Arrow [2019-10-31T00:00:00+00:00]>

>>> arrow.get("It's Halloween tomorrow (2019/10/31)", "YYYY/MM/DD")
<Arrow [2019-10-31T00:00:00+00:00]>

>>> arrow.get("It's Halloween tomorrow 2019/10/31", "YYYY/MM/DD")
<Arrow [2019-10-31T00:00:00+00:00]>

# Raises exception because there are multiple punctuation marks following the date
>>> arrow.get("It's Halloween tomorrow (2019-10-31)!", "YYYY-MM-DD")
---------------------------------------------------------------------------
ParserMatchError: Failed to match 'YYYY-MM-DD' when parsing 'It's Halloween tomorrow (2019-10-31)!'

>>>
```

## Arrow模块的API

官方文档中提供了详细的api文档，具体可参考[https://arrow.readthedocs.io/en/stable/#api-guide](https://arrow.readthedocs.io/en/stable/#api-guide)。



在github上面可以看到该模块最近也有更新，说明比较活跃！通过本文中的一些示例可以看到，使用arrow模块处理日期时间相关的操作非常的方法，后续可以使用这个模块作为代码中日期的默认的处理方式！



参考：

- [https://pypi.org/project/arrow/](https://pypi.org/project/arrow/)
- [https://github.com/crsmithdev/arrow/](https://github.com/crsmithdev/arrow/)
- [https://arrow.readthedocs.io/en/latest/](https://arrow.readthedocs.io/en/latest/)




