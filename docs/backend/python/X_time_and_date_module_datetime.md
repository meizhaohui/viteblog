# 日期和时间模块-`datetime`日期时间模块


[[toc]]



查看`datetime`模块有哪些函数或方法：

```py
$ python
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import datetime
>>> datetime.
datetime.date(         datetime.datetime_CAPI datetime.MINYEAR       datetime.time(         datetime.timezone(
datetime.datetime(     datetime.MAXYEAR       datetime.sys           datetime.timedelta(    datetime.tzinfo(
>>> exit()
```

似乎看起来`datetime`模块没有多少函数或方法，我们一个个的了解一下。

参考：

- [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
- [https://docs.python.org/zh-cn/3/library/datetime.html](https://docs.python.org/zh-cn/3/library/datetime.html)



`datetime`模块提供用于处理日期和时间的类。

在支持日期时间数学运算的同时，实现的关注点更着重于如何能够更有效地解析其属性用于格式化输出和数据操作。

## 常量

`date`和`datetime`对象允许的最小、最大年份，最小年份为1，最大年份为9999。
```py
>>> datetime.MINYEAR
1
>>> datetime.MAXYEAR
9999
```

### 有效的类型

- `class datetime.date`理想化的日期类。
- `class datetime.time`理想化的时间类。
- `class datetime.datetime`理想化日期和时间的结合。
- `class datetime.timedelta`时间间隔。
-  `class datetime.tzinfo`抽象类，给date或time类提供自定义的时间调整概念。
- `class datetime.timezone`时区设置，是tzinfo类的子类。


## 通用的特征属性

`date`, `datetime`, `time`和`timezone`类型共享这些通用特性:

- 这些类型的对象都是不可变的。
- 这些类型的对象是可哈希的，这意味着它们可被作为字典的键。
- 这些类型的对象支持通过 pickle 模块进行高效的封存。

## `datetime.date`日期类

初步使用date类：

```py
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> import datetime

>>> datetime.date?
Init signature: datetime.date(self, /, *args, **kwargs)
Docstring:      date(year, month, day) --> date object
File:           /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/datetime.py
Type:           type
Subclasses:     datetime

>>> datetime.date()
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-3-76bd6ecec42c> in <module>
----> 1 datetime.date()

TypeError: Required argument 'year' (pos 1) not found
```

可以看到`datetime.date`类实例化时需要提供year, month, day三个参数。

参数说明如下：

- 所有参数都是必须的。
- 参数都需要为integer整数。

- `MINYEAR <= year <= MAXYEAR`
- `1 <= month <= 12`
- `1 <= day <= number of days in the given month and year`

我们来实现化一个`datetime.date`类对象。

正常实例化：

```python
>>> datetime.date(2020, 6, 25)
datetime.date(2020, 6, 25)

>>> ndate = datetime.date(2020, 6, 25)

>>> ndate
datetime.date(2020, 6, 25)
```

检查异常：



### 整型检查

```python
>>> datetime.date(2020.3, 6, 25)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-12-378e9f0dc353> in <module>
----> 1 datetime.date(2020.3, 6, 25)

TypeError: integer argument expected, got float

>>> datetime.date(2020, 6.3, 25)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-13-7f03f9cdb50c> in <module>
----> 1 datetime.date(2020, 6.3, 25)

TypeError: integer argument expected, got float

>>> datetime.date(2020, 6, 25.3)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-15-b1a4edea2412> in <module>
----> 1 datetime.date(2020, 6, 25.3)

TypeError: integer argument expected, got float
```

可以发现输入小数后实例化会报`TypeError`异常。



### 值异常检查

```python
>>> datetime.date(9999, 6, 25)
datetime.date(9999, 6, 25)

>>> datetime.date(10000, 6, 25)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-18-254ebe0a2d38> in <module>
----> 1 datetime.date(10000, 6, 25)

ValueError: year 10000 is out of range

>>> datetime.date(0, 6, 25)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-19-5753139fb256> in <module>
----> 1 datetime.date(0, 6, 25)

ValueError: year 0 is out of range

>>> datetime.date(-0, 6, 25)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-20-1c1ea584a919> in <module>
----> 1 datetime.date(-0, 6, 25)

ValueError: year 0 is out of range

>>> datetime.date(-2020, 6, 25)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-21-5def12532dda> in <module>
----> 1 datetime.date(-2020, 6, 25)

ValueError: year -2020 is out of range
```

可以发现输入年份不在[0, 9999]区间时，实例化会报`ValueError`异常。

查看源码可知实例化时会使用`year, month, day = _check_date_fields(year, month, day)`对年月日参数进行有效性检查。

### `datetime.date`类的方法和属性

查看`datetime.date`类的方法和属性：

```python
>>> ndate.
           ctime()         fromtimestamp() isoweekday()    month           strftime()      toordinal()
           day             isocalendar()   max             replace()       timetuple()     weekday()
           fromordinal()   isoformat()     min             resolution      today()         year
```

- 查看实例的年月日属性

```python
>>> ndate
datetime.date(2020, 6, 25)

# 年份
>>> ndate.year
2020

# 月份
>>> ndate.month
6

# 日期
>>> ndate.day
25
```

- 查看类属性

```python
# 最小的日期
>>> ndate.min
datetime.date(1, 1, 1)

# 最大的日期
>>> ndate.max
datetime.date(9999, 12, 31)

# 两个日期对象的最小间隔
>>> ndate.resolution
datetime.timedelta(1)
```

- 查看类方法

```python
# 返回当前的本地日期，相当于datetime.date.fromtimestamp(time.time())
>>> datetime.date.today()
datetime.date(2020, 6, 25)

>>> import time

# 返回时间戳对应的date对象
>>> datetime.date.fromtimestamp(time.time())
datetime.date(2020, 6, 25)
```

- 实例的方法

`date.replace(year=self.year, month=self.month, day=self.day)`返回一个具有同样值的日期，除非通过任何关键字参数给出了某些形参的新值。

```python
>>> ndate
datetime.date(2020, 6, 25)

>>> ndate.replace(day=26)
datetime.date(2020, 6, 26)

>>> ndate
datetime.date(2020, 6, 25)

>>> ndate.replace(year=2021, month=5, day=1)
datetime.date(2021, 5, 1)

>>> ndate
datetime.date(2020, 6, 25)
```

可以看到使用`replace`方法替换时，只是返回一个新的`date`类对象，不会改变原来的实例。



`date.timetuple()` 返回一个 time.struct_time时间元组。



```python
>>> ndate.timetuple()
time.struct_time(tm_year=2020, tm_mon=6, tm_mday=25, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=177, tm_isdst=-1)
```



`date.weekday()`返回当前日期是星期几，0代表周一，6代表周日。

```python
# 2020年6月25日是周四
>>> ndate.weekday()
3
```

`date.isoweekday()`返回当前日期是星期几，1代表周一，7代表周日。

```python
# 2020年6月25日是周四
>>> ndate.isoweekday()
4
```

`date.isocalendar()`返回当前日期对应的日历元组` (ISO year, ISO week number, ISO weekday)`。

```python
# 2020年6月25日的年份是2020年，是该年的第26周，周四
>>> ndate.isocalendar()
(2020, 26, 4)
```

`date.isoformat()`返回一个以 ISO 8601 格式`YYYY-MM-DD`来表示日期的字符串。与`date.__str__()`等价。

```python
>>> ndate.isoformat()
'2020-06-25'

>>> ndate.__str__()
'2020-06-25'
```

可以看到此时日期字符串是四位数字的年份-两位数字的月份-两位数字的日期。

`date.ctime()`返回一个表示日期的字符串。

```python
>>> ndate.ctime()
'Thu Jun 25 00:00:00 2020'
```

`date.strftime(format)`返回一个由显式格式字符串所指明的代表日期的字符串。与`date.__format__(format)`等价。

```python
>>> ndate.strftime('%Y%m%d')
'20200625'

>>> ndate.strftime('%Y-%m-%d')
'2020-06-25'

>>> ndate.strftime('%Y年%m月%d日')
'2020年06月25日'

>>> ndate.strftime('%Y %b %d')
'2020 Jun 25'

>>> ndate.__format__('%Y %b %d')
'2020 Jun 25'

>>> ndate.__format__('%Y-%m-%d')
'2020-06-25'

>>> ndate.__format__('%Y年%m月%d日')
'2020年06月25日'
```

## `datetime.time`时间类

`class datetime.time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)`时间对象，所有参数可选。



参数取值说明：

  - `0 <= hour < 24`,
  - `0 <= minute < 60`,
  - `0 <= second < 60`,
  - `0 <= microsecond < 1000000`,
  - `fold in [0, 1]`.

查看帮助信息并实例化对象：

```python
>>> datetime.time?
Init signature: datetime.time(self, /, *args, **kwargs)
Docstring:
time([hour[, minute[, second[, microsecond[, tzinfo]]]]]) --> a time object

All arguments are optional. tzinfo may be None, or an instance of
a tzinfo subclass. The remaining arguments may be ints.
File:           /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/datetime.py
Type:           type
Subclasses:

>>> ntime = datetime.time(6,48,5)

>>> ntime
datetime.time(6, 48, 5)

>>> ntime.
ntime.dst(        ntime.isoformat(  ntime.min         ntime.resolution  ntime.tzinfo
ntime.fold        ntime.max         ntime.minute      ntime.second      ntime.tzname(
ntime.hour        ntime.microsecond ntime.replace(    ntime.strftime(   ntime.utcoffset(
```

### `datetime.time`类方法

```python
# 最小时间
>>> datetime.time.min
datetime.time(0, 0)

# 最大时间
>>> datetime.time.max
datetime.time(23, 59, 59, 999999)

# 时间对象的最小间隔,注意，time对象不支持算术运算！
>>> datetime.time.resolution
datetime.timedelta(0, 0, 1)

# 可以看到进行time类算术运算会出现异常
>>> datetime.time.max - datetime.time.min
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-281-c9a8c1713e41> in <module>
----> 1 datetime.time.max - datetime.time.min

TypeError: unsupported operand type(s) for -: 'datetime.time' and 'datetime.time'
```

### `datetime.time`类实例属性

```python
>>> ntime.
ntime.dst(        ntime.isoformat(  ntime.min         ntime.resolution  ntime.tzinfo
ntime.fold        ntime.max         ntime.minute      ntime.second      ntime.tzname(
ntime.hour        ntime.microsecond ntime.replace(    ntime.strftime(   ntime.utcoffset(

# 获取时间对象小时值
>>> ntime.hour
6

# 获取时间对象分钟值
>>> ntime.minute
48

# 获取时间对象秒值
>>> ntime.second
5

# 获取时间对象微秒值
>>> ntime.microsecond
0
  
# 获取tzinfo参数传递的值，没有指定tzinfo时，返回None
>>> ntime.tzinfo

# 取值范围是 [0, 1]。 用于在重复的时间段中消除边界时间歧义，对于中国没有夏令时似乎没有实际意义，不用理会
>>> ntime.fold
0
```

`datetime.time`对象支持`time`与`time`之间的比较：

```python
>>> atime = datetime.time(6, 48, 5)

>>> btime = datetime.time(19, 53, 6)

>>> atime < btime
True

>>> atime == btime
False

>>> atime != btime
True
```

布尔运算时，`datetime.time`时间对象永远认为是`True`真值。

```python
>>> bool(ntime)
True
```

### `datetime.time`类实例方法



`time.replace(hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, * fold=0)`时间对象替换，返回新的`time`对象。

```python
>>> ntime.replace?
Docstring: Return time with new specified fields.
Type:      builtin_function_or_method

>>> ntime
datetime.time(6, 48, 5)

>>> ntime.replace(7,3,6)
datetime.time(7, 3, 6)

>>> ntime
datetime.time(6, 48, 5)
```

`time.isoformat(timespec='auto')`返回表示为 ISO 8601 格式之一的时间字符串。

```python
>>> ntime.isoformat?
Docstring:
Return string in ISO 8601 format, [HH[:MM[:SS[.mmm[uuu]]]]][+HH:MM].

timespec specifies what components of the time to include.
Type:      builtin_function_or_method

>>> ntime.isoformat()
'06:48:05'

# 自动设置格式，等价于'seconds'，返回HH:MM:SS格式
>>> ntime.isoformat(timespec='auto')
'06:48:05'

# 返回小时
>>> ntime.isoformat(timespec='hours')
'06'

# 返回小时和分钟
>>> ntime.isoformat(timespec='minutes')
'06:48'

# 返回小时、分钟和秒数
>>> ntime.isoformat(timespec='seconds')
'06:48:05'

# 返回小时、分钟和秒数，秒数精确到毫秒
>>> ntime.isoformat(timespec='milliseconds')
'06:48:05.000'

# 返回小时、分钟和秒数，秒数精确到微秒
>>> ntime.isoformat(timespec='microseconds')
'06:48:05.000000'
```

`time.__str__()`对于`time`时间对象`t`，`str(t)`与`t.isoformat()`等价。返回标准时间字符串。

```python
>>> str(ntime)
'06:48:05'

>>> ntime.isoformat()
'06:48:05'

>>> ntime.__str__()
'06:48:05'
```

`time.strftime(format)`按指定格式格式化时间对象。具体的格式化标志请参考[https://docs.python.org/3.6/library/datetime.html#strftime-strptime-behavior](https://docs.python.org/3.6/library/datetime.html#strftime-strptime-behavior)。

```python
>>> ntime.strftime('%H%M%S')
'064805'

>>> ntime.strftime('%H:%M:%S')
'06:48:05'

>>> ntime.strftime('%H:%M:%S %p')
'06:48:05 AM'


time.__format__(format)与time.strftime(format)等价
>>> ntime.__format__('%H:%M:%S')
'06:48:05'
```

另外三个方法`time.utcoffset()`、`time.dst()`、`time.tzname()`与`tzinfo`相关，如果`datetime.time`对象没有设置tzinfo,则返回值为`None`。

```python
>>> ntime.utcoffset()

>>> ntime.dst()

>>> ntime.tzname()
```



## `datetime.datetime`日期时间类

`datetime.datetime`对象是包含来自`datetime.time`对象和`datetime.date`对象的所有信息的单一对象。

与`datetime.date`对象一样，`datetime.datetime`假定当前的格列高利历(Gregorian calendar)向前后两个方向无限延伸；与`datetime.time`对象一样，`datetime.datetime`假定假定每一天恰好有 3600*24 秒。

 `class datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)`*year*, *month* 和 *day* 参数是必须的。 *tzinfo* 可以是 `None` 或者是一个 [`tzinfo`](https://docs.python.org/zh-cn/3/library/datetime.html#datetime.tzinfo)子类的实例。 其余的参数必须是在下面范围内的整数：

- `MINYEAR <= year <= MAXYEAR`,
- `1 <= month <= 12`,
- `1 <= day <= 指定年月的天数`,
- `0 <= hour < 24`,
- `0 <= minute < 60`,
- `0 <= second < 60`,
- `0 <= microsecond < 1000000`,
- `fold in [0, 1]`.

如果参数不在这些范围内，则抛出 [`ValueError`](https://docs.python.org/zh-cn/3/library/exceptions.html#ValueError) 异常。



### `datetime.datetime`类方法

```python
>>> datetime.datetime?
Init signature: datetime.datetime(self, /, *args, **kwargs)
Docstring:
datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints.
File:           /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/datetime.py
Type:           type
Subclasses:

# 返回表示当前地方时的datetime对象，其中tzinfo为None
>>> datetime.datetime.today?
Docstring: Current date or datetime:  same as self.__class__.fromtimestamp(time.time()).
Type:      builtin_function_or_method

>>> datetime.datetime.today()
datetime.datetime(2020, 6, 30, 7, 28, 8, 46004)


# 返回当前地方时的日期和时间，如果tz参数未指定，则与today()类方法等价。如果 tz 不为 None，它必须是 tzinfo 子类的一个实例，并且当前日期和时间将被转换到 tz 时区。
>>> datetime.datetime.now?
Signature: datetime.datetime.now(tz=None)
Docstring:
Returns new datetime object representing current time local to tz.

  tz
    Timezone object.

If no tz is specified, uses local timezone.
Type:      builtin_function_or_method
  
>>> datetime.datetime.now()
datetime.datetime(2020, 6, 30, 7, 28, 27, 965728)


# 返回表示当前 UTC 时间的 date 和 time，其中 tzinfo 为 None
>>> datetime.datetime.utcnow?
Docstring: Return a new datetime representing UTC day and time.
Type:      builtin_function_or_method
  
>>> datetime.datetime.utcnow()
datetime.datetime(2020, 6, 29, 23, 28, 46, 771171)

# 返回时间戳timestamp对应的本地日期和时间,如果指定tz，则其必须是tzinfo子类
>>> datetime.datetime.fromtimestamp?
Docstring: timestamp[, tz] -> tz's local time from POSIX timestamp.
Type:      builtin_function_or_method

>>> import time

>>> datetime.datetime.fromtimestamp(time.time())
datetime.datetime(2020, 6, 30, 7, 55, 54, 336472)

>>> time.time()
1593474958.3385558

# 返回时间戳timestamp对应的UTC日期和时间
>>> datetime.datetime.utcfromtimestamp?
Docstring: Construct a naive UTC datetime from a POSIX timestamp.
Type:      builtin_function_or_method

>>> datetime.datetime.utcfromtimestamp(time.time())
datetime.datetime(2020, 6, 30, 0, 6, 44, 530452)


# 返回对应于预期格列高利历序号的 datetime，其中公元 1 年 1 月 1 日的序号为 1。结果的 hour, minute, second 和 microsecond 值均为 0，并且 tzinfo 值为 None。
>>> datetime.datetime.fromordinal?
Docstring: int -> date corresponding to a proleptic Gregorian ordinal.
Type:      builtin_function_or_method

# 格列高利历序号1对应的日期
>>> datetime.datetime.fromordinal(1)
datetime.datetime(1, 1, 1, 0, 0)

# 格列高利历序号2对应的日期
>>> datetime.datetime.fromordinal(2)
datetime.datetime(1, 1, 2, 0, 0)

>>> datetime.datetime.fromordinal(30)
datetime.datetime(1, 1, 30, 0, 0)

>>> datetime.datetime.fromordinal(31)
datetime.datetime(1, 1, 31, 0, 0)

>>> datetime.datetime.fromordinal(32)
datetime.datetime(1, 2, 1, 0, 0)

>>> datetime.datetime.fromordinal(365)
datetime.datetime(1, 12, 31, 0, 0)

# 从公元 1 年 1 月 1 日到现在已经经过了737606天呢！# 格列高利历序号737606对应的日期是今天2020年6月30日
>>> datetime.datetime.fromordinal(737606)
datetime.datetime(2020, 6, 30, 0, 0)

# 最大的日期不能超过9999年12月31日
>>> datetime.datetime.max
datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)

# 也就是最大的格列高得历序号为3652059，超过这个值就会引发ValueError异常
>>> datetime.datetime.max.toordinal()
3652059

>>> datetime.datetime.fromordinal(datetime.datetime.max.toordinal() + 1)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-177-8452070d41ee> in <module>
----> 1 datetime.datetime.fromordinal(datetime.datetime.max.toordinal() + 1)

ValueError: year 10000 is out of range
  
  
>>> ndate
datetime.date(2020, 6, 25)

>>> ntime
datetime.time(6, 48, 5)

# 返回一个新的 datetime 对象，对象的日期部分等于给定的 date 对象的值，而其时间部分等于给定的 time 对象的值。
# combine是结合、合并的意思 
>>> datetime.datetime.combine?
Docstring: date, time -> datetime with same date and time fields
Type:      builtin_function_or_method
  
>>> datetime.datetime.combine(ndate, ntime)
datetime.datetime(2020, 6, 25, 6, 48, 5)


# 返回一个对应于 string，根据 format 进行解析得到的 datetime 对象。即将日期时间字符串转换成datetime对象
>>> datetime.datetime.strptime?
Docstring: string, format -> new datetime parsed from a string (like time.strptime()).
Type:      builtin_function_or_method

>>> datetime.datetime.strptime('2020-06-30 20:30:32', '%Y-%m-%d %H:%M:%S')
datetime.datetime(2020, 6, 30, 20, 30, 32)
```



### `datetime.datetime`类属性

```python
# 最早可以表示的日期时间
>>> datetime.datetime.min
datetime.datetime(1, 1, 1, 0, 0)

# 最晚可以表示的日期时间
>>> datetime.datetime.max
datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)

# 两个datetime对象之间的最小间隔
>>> datetime.datetime.resolution
datetime.timedelta(0, 0, 1)
```

### `datetime.datetime`实例属性

查看`datetime.datetime`实例的所有属性和方法：

```python
>>> ndatetime = datetime.datetime.today()
>>> ndatetime.
ndatetime.astimezone(       ndatetime.isocalendar(      ndatetime.resolution        ndatetime.tzinfo
ndatetime.combine(          ndatetime.isoformat(        ndatetime.second            ndatetime.tzname(
ndatetime.ctime(            ndatetime.isoweekday(       ndatetime.strftime(         ndatetime.utcfromtimestamp(
ndatetime.date(             ndatetime.max               ndatetime.strptime(         ndatetime.utcnow(
ndatetime.day               ndatetime.microsecond       ndatetime.time(             ndatetime.utcoffset(
ndatetime.dst(              ndatetime.min               ndatetime.timestamp(        ndatetime.utctimetuple(
ndatetime.fold              ndatetime.minute            ndatetime.timetuple(        ndatetime.weekday(
ndatetime.fromordinal(      ndatetime.month             ndatetime.timetz(           ndatetime.year
ndatetime.fromtimestamp(    ndatetime.now(              ndatetime.today(
ndatetime.hour              ndatetime.replace(          ndatetime.toordinal(
>>> 
```

`datetime.datetime`实例属性：

```python
>>> datetime.datetime.today()
datetime.datetime(2020, 6, 30, 20, 54, 51, 974744)

>>> ndatetime = datetime.datetime.today()

>>> ndatetime
datetime.datetime(2020, 6, 30, 20, 55, 14, 377464)

# 年
>>> ndatetime.year
2020

# 月
>>> ndatetime.month
6

# 日
>>> ndatetime.day
30

# 小时
>>> ndatetime.hour
20

# 分钟
>>> ndatetime.minute
55

# 秒
>>> ndatetime.second
14

# 微秒
>>> ndatetime.microsecond
377464

# 作为 tzinfo 参数被传给 datetime 构造器的对象，如果没有传入值则为 None
>>> ndatetime.tzinfo

# 取值范围是 [0, 1]。 用于在重复的时间段中消除边界时间歧义。
>>> ndatetime.fold
0
```



### `datetime.datetime`实例方法

- `datetime.date()`返回date日期对象:

```python
# 返回具有同样 year, month 和 day 值的 date 对象。
>>> ndatetime.date()
datetime.date(2020, 6, 30)
```

- `datetime.time()`返回time时间对象：

```python
# 返回具有同样 hour, minute, second, microsecond 和 fold 值的 time 对象。 tzinfo 值为 None。
>>> ndatetime.time()
datetime.time(20, 55, 14, 377464)
```

- `datetime.timetz()`返回具有同样 hour, minute, second, microsecond, fold 和 tzinfo 属性性的 time 对象。

```python
# 返回具有同样 hour, minute, second, microsecond, fold 和 tzinfo 属性性的 time 对象。
>>> ndatetime.timetz()
datetime.time(20, 55, 14, 377464)
```

- `datetime.timetuple()`返回时间元组

```python
# 返回一个 time.struct_time时间元组，即 time.localtime() 所返回的类型。
>>> ndatetime.timetuple()
time.struct_time(tm_year=2020, tm_mon=6, tm_mday=30, tm_hour=20, tm_min=55, tm_sec=14, tm_wday=1, tm_yday=182, tm_isdst=-1)
```

- `datetime.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, * fold=0)`返回一个具有同样属性值的 datetime，除非通过任何关键字参数为某些属性指定了新值。 请注意可以通过指定 `tzinfo=None` 来从一个感知型 datetime 创建一个简单型 datetime 而不必转换日期和时间数据。

```python
>>> ndatetime
datetime.datetime(2020, 6, 30, 20, 55, 14, 377464)

>>> ndatetime.replace?
Docstring: Return datetime with new specified fields.
Type:      builtin_function_or_method

# 返回新的datetime对象
>>> ndatetime.replace(month=7, day=1, hour=7, minute=16, second=30)
datetime.datetime(2020, 7, 1, 7, 16, 30, 377464)

# ndatetime实例并没有发生变化
>>> ndatetime
datetime.datetime(2020, 6, 30, 20, 55, 14, 377464)
```

- `datetime.astimezone(tz=None)`返回一个具有新的 [`tzinfo`](https://docs.python.org/zh-cn/3/library/datetime.html#datetime.datetime.tzinfo) 属性 *tz* 的 [`datetime`](https://docs.python.org/zh-cn/3/library/datetime.html#datetime.datetime) 对象，并会调整日期和时间数据使得结果对应的 UTC 时间与 *self* 相同，但为 *tz* 时区的本地时间。

```python
>>> ndatetime.astimezone?
Docstring: tz -> convert to local time in new timezone tz
Type:      builtin_function_or_method

>>> ndatetime.astimezone()
datetime.datetime(2020, 6, 30, 20, 55, 14, 377464, tzinfo=datetime.timezone(datetime.timedelta(0, 28800), 'CST'))
```

- `datetime.utcoffset`如果 [`tzinfo`](https://docs.python.org/zh-cn/3/library/datetime.html#datetime.datetime.tzinfo) 为 `None`，则返回 `None`，否则返回 `self.tzinfo.utcoffset(self)`。

```python
>>> ndatetime.utcoffset?
Docstring: Return self.tzinfo.utcoffset(self).
Type:      builtin_function_or_method

>>> ndatetime.utcoffset()
```

- `datetime.dst()`如果 [`tzinfo`](https://docs.python.org/zh-cn/3/library/datetime.html#datetime.datetime.tzinfo) 为 `None`，则返回 `None`，否则返回 `self.tzinfo.dst(self)`。

```python
>>> ndatetime.dst?
Docstring: Return self.tzinfo.dst(self).
Type:      builtin_function_or_method

>>> ndatetime.dst()
```

- `datetime.tzname()`如果 tzinfo 为`None`，则返回`None`，否则返回 `self.tzinfo.tzname(self)`。

```python
>>> ndatetime.tzname?
Docstring: Return self.tzinfo.tzname(self).
Type:      builtin_function_or_method

>>> ndatetime.tzname()
```

- `datetime.utftimetuple()`返回UTC形式的时间元组。

```python
>>> ndatetime.utctimetuple?
Docstring: Return UTC time tuple, compatible with time.localtime().
Type:      builtin_function_or_method

>>> ndatetime.utctimetuple()
time.struct_time(tm_year=2020, tm_mon=6, tm_mday=30, tm_hour=20, tm_min=55, tm_sec=14, tm_wday=1, tm_yday=182, tm_isdst=0)
```

- `datetime.toordinal()`返回日期的预期格列高利历序号。 与 `self.date().toordinal()` 相同。

```python
>>> ndatetime.toordinal?
Docstring: Return proleptic Gregorian ordinal.  January 1 of year 1 is day 1.
Type:      builtin_function_or_method

# 返回日期的格列高利序号
>>> ndatetime.toordinal()
737606

# 从公元 1 年 1 月 1 日到现在已经经过了737606天呢！# 格列高利历序号737606对应的日期是今天2020年6月30日
>>> datetime.datetime.fromordinal(737606)
datetime.datetime(2020, 6, 30, 0, 0)
```

- `datetime.timestamp()`返回日期时间对象对应的时间戳。

```python
>>> ndatetime.timestamp?
Docstring: Return POSIX timestamp as float.
Type:      builtin_function_or_method

>>> ndatetime.timestamp()
1593521714.377464
```

- `datetime.weekday()`返回日期时间对象是星期几。0代表周一，1代表周二，6代码周日。

```python
>>> ndatetime.weekday?
Docstring:
Return the day of the week represented by the date.
Monday == 0 ... Sunday == 6
Type:      builtin_function_or_method

>>> ndatetime.weekday()
1
```

- `datetime.isoweekday()`返回日期时间对象是星期几。1代表周一，2代表周二，7代码周日。

```python
>>> ndatetime.isoweekday?
Docstring:
Return the day of the week represented by the date.
Monday == 1 ... Sunday == 7
Type:      builtin_function_or_method

>>> ndatetime.isoweekday()
2
```

- `datetime.isocalendar()`返回一个 3 元组 (ISO 年份, ISO 周序号, ISO 周日期)。 等同于 self.date().isocalendar()。

```python
>>> ndatetime.isocalendar?
Docstring: Return a 3-tuple containing ISO year, week number, and weekday.
Type:      builtin_function_or_method

>>> ndatetime.isocalendar()
(2020, 27, 2)
```

- ` datetime.isoformat(sep='T', timespec='auto')`返回一个以 ISO 8601 格式表示的日期和时间字符串

```python
>>> ndatetime.isoformat?
Docstring:
[sep] -> string in ISO 8601 format, YYYY-MM-DDT[HH[:MM[:SS[.mmm[uuu]]]]][+HH:MM].
sep is used to separate the year from the time, and defaults to 'T'.
timespec specifies what components of the time to include (allowed values are 'auto', 'hours', 'minutes', 'seconds', 'milliseconds', and 'microseconds').
Type:      builtin_function_or_method

>>> ndatetime.isoformat()
'2020-06-30T20:55:14.377464'

>>> ndatetime.isoformat(timespec='minutes')
'2020-06-30T20:55'

>>> ndatetime.isoformat(timespec='seconds')
'2020-06-30T20:55:14'
```

- `datetime.__str__()`等价于`datetime.isoformat(sep=' '`)。

```python
>>> ndatetime.__str__()
'2020-06-30 20:55:14.377464'
```

-  `datetime.ctime()`返回一个表示日期和时间的字符串。d.ctime() 等效于:`time.ctime(time.mktime(d.timetuple()))`。

```python
>>> ndatetime.ctime?
Docstring: Return ctime() style string.
Type:      builtin_function_or_method

>>> ndatetime.ctime()
'Tue Jun 30 20:55:14 2020'

>>> import time

>>> ndatetime.timetuple()
time.struct_time(tm_year=2020, tm_mon=6, tm_mday=30, tm_hour=20, tm_min=55, tm_sec=14, tm_wday=1, tm_yday=182, tm_isdst=-1)

>>> time.mktime(ndatetime.timetuple())
1593521714.0

>>> time.ctime(time.mktime(ndatetime.timetuple()))
'Tue Jun 30 20:55:14 2020'
```

- `datetime.strftime(format)`返回一个由显式格式字符串所指明的代表日期和时间的字符串。

```python
>>> ndatetime.strftime?
Docstring: format -> strftime() style string.
Type:      builtin_function_or_method
  
>>> ndatetime.strftime('%Y%m%d')
'20200630'

>>> ndatetime.strftime('%Y年%m月%d日')
'2020年06月30日'

>>> ndatetime.strftime('%H:%M:%S')
'20:55:14'

>>> ndatetime.strftime('%Y%m%d %H:%M:%S')
'20200630 20:55:14'

>>> ndatetime.strftime('%Y年%m月%d日%H:%M:%S')
'2020年06月30日20:55:14'
```

- `datetime.__format__(format)`与 datetime.strftime() 相同。 此方法使得为 datetime 对象指定以 格式化字符串字面值 表示的格式化字符串以及使用 str.format() 进行格式化成为可能。`str.format()`可参考[https://docs.python.org/zh-cn/3/library/string.html#format-examples](https://docs.python.org/zh-cn/3/library/string.html#format-examples)。

```python
>>> ndatetime.__format__('%Y年%m月%d日%H:%M:%S')
'2020年06月30日20:55:14'

>>> '{:%Y年%m月%d日}'.format(ndatetime)
'2020年06月30日'

>>> '{:%Y年%m月%d日%H:%M:%S}'.format(ndatetime)
'2020年06月30日20:55:14'


>>> 'The {1} is {0:%d}, the {2} is {0:%B}, the {3} is {0:%I:%M%p}.'.format(ndatetime, "day", "month", "time")
'The day is 30, the month is June, the time is 08:55PM.'
```



## `datetime.timedelta`时间间隔类

` class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)`表示两个 date 对象或者 time 对象,或者 datetime 对象之间的时间间隔，精确到微秒。

```python
>>> datetime.timedelta?
Init signature: datetime.timedelta(self, /, *args, **kwargs)
Docstring:
Difference between two datetime values.

timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

All arguments are optional and default to 0.
Arguments may be integers or floats, and may be positive or negative.
File:           /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/datetime.py
Type:           type
Subclasses:
```

所有参数都是可选的并且默认为 `0`。 这些参数可以是整数或者浮点数，也可以是正数或者负数。

只有 *days*, *seconds* 和 *microseconds* 会存储在内部。 参数单位的换算规则如下：

- 1毫秒会转换成1000微秒。
- 1分钟会转换成60秒。
- 1小时会转换成3600秒。
- 1星期会转换成7天。

并且 days, seconds, microseconds 会经标准化处理以保证表达方式的唯一性，即：

- `0 <= microseconds < 1000000`
- `0 <= seconds < 3600*24` (一天的秒数)
- `-999999999 <= days <= 999999999`

示例：

```python
# 如何对 days, seconds 和 microseconds 以外的任意参数执行“合并”操作并标准化为以上三个结果属性
>>> from datetime import timedelta
... delta = timedelta(
...     days=50,
...     seconds=27,
...     microseconds=10,
...     milliseconds=29000,
...     minutes=5,
...     hours=8,
...     weeks=2
... )

>>> delta
datetime.timedelta(64, 29156, 10)
```



### 对日期、时间对象进行算术运算操作

- 对datetime.date对象进行算术运算操作

```python
>>> ndate
datetime.date(2020, 6, 25)

>>> d1 = ndate

>>> d2 = datetime.date.today()

>>> d2
datetime.date(2020, 7, 2)

>>> d2 - d1
datetime.timedelta(7)

>>> delta = d2 - d1

>>> delta
datetime.timedelta(7)

>>> d1 < d2
True

>>> d1 > d2
False

>>> d1 + delta
datetime.date(2020, 7, 2)

>>> d1 + delta == d2
True

>>> d2 + delta
datetime.date(2020, 7, 9)

>>> d2 - delta
datetime.date(2020, 6, 25)

>>> d2 - delta == d1
True
```

- 对datetime.time对象进行算术运算操作

datetime.time对象不支持算术运算操作，进行相关操作会提示异常。

```python
>>> datetime.time.max
datetime.time(23, 59, 59, 999999)

>>> datetime.time.min
datetime.time(0, 0)

>>> datetime.time.max - datetime.time.min
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-327-c9a8c1713e41> in <module>
----> 1 datetime.time.max - datetime.time.min

TypeError: unsupported operand type(s) for -: 'datetime.time' and 'datetime.time'

# 可以进行逻辑运行
>>> datetime.time.max > datetime.time.min
True
```

- 对datetime.datetime对象进行算术运算操作

```python
# 对datetime.datetime对象进行算术运算操作
>>> ndatetime
datetime.datetime(2020, 6, 30, 20, 55, 14, 377464)

>>> d1 = ndatetime

>>> d2 = datetime.datetime.today()

>>> d1 < d2
True

>>> d2 > d1
True

>>> d2 - d1
datetime.timedelta(1, 39023, 96117)

>>> delta1 = d2 - d1

>>> delta1
datetime.timedelta(1, 39023, 96117)

>>> d1 + delta1
datetime.datetime(2020, 7, 2, 7, 45, 37, 473581)

>>> d1 + delta1 == d2
True

>>> d2 + delta1
datetime.datetime(2020, 7, 3, 18, 36, 0, 569698)

>>> d2 - delta1 == d1
True
```



### `datetime.timedelta`类属性

```python
# 最小的timedelta对象
>>> datetime.timedelta.min
datetime.timedelta(-999999999)

# 最大的timedelta对象
>>> datetime.timedelta.max
datetime.timedelta(999999999, 86399, 999999)

# 两个timedelta对象的最小间隔
>>> datetime.timedelta.resolution
datetime.timedelta(0, 0, 1)
```

需要注意的是，因为标准化的缘故，`timedelta.max` > `-timedelta.min`，`-timedelta.max` 不可以表示一个 [`timedelta`](https://docs.python.org/zh-cn/3/library/datetime.html#datetime.timedelta) 类对象。

```python
# 将timedelta.max取负时会出现OverflowError异常
>>> -datetime.timedelta.max
---------------------------------------------------------------------------
OverflowError                             Traceback (most recent call last)
<ipython-input-333-ba8c83a6c9ef> in <module>
----> 1 -datetime.timedelta.max

OverflowError: days=-1000000000; must have magnitude <= 999999999

>>> -datetime.timedelta.min
datetime.timedelta(999999999)

>>> datetime.timedelta.max > -datetime.timedelta.min
True
```



### `datetime.timedelta`类实例方法

`timedelta.total_secounds()`返回时间间隔包含多少秒。

```python
>>> year = timedelta(days=365)

>>> year.total_seconds?
Docstring: Total seconds in the duration.
Type:      builtin_function_or_method

# 一年有多少秒
>>> year.total_seconds()
31536000.0

>>> minute = timedelta(minutes=1)

>>> minute
datetime.timedelta(0, 60)

1分钟有60秒
>>> minute.total_seconds()
60.0

>>> hour = timedelta(hours=1)

# 1小时有3600秒
>>> hour.total_seconds()
3600.0

>>> day = timedelta(days=1)

# 1天有86400秒
>>> day.total_seconds()
86400.0
```

`datetime`模块中还有`tzinfo`子类，以及`tzinfo`子类的子类`timezone`，使用相对麻烦，在此不提了！总的来说，`datetime`模块并没有想象的那么简单，其中的各个子类还是比较复杂的。在实际编程中，经常使用`datetime`模块来生成当前时间对应的字符串。

```python
>>> import datetime 

>>> ndatetime = datetime.datetime.today()

>>> ndatetime
datetime.datetime(2020, 7, 5, 11, 44, 37, 182216)

# 生成当前时间对应的时间字符串
>>> ndatetime.strftime('%Y年%m月%d日%H:%M:%S')
'2020年07月05日11:44:37'

# 生成文件名
>>> filename = ndatetime.strftime('%Y%m%d_%H%M%S.txt')

>>> filename
'20200705_114437.txt'

# 创建文件并写入数据
>>> with open(filename,'w', encoding='utf-8') as f:
...     f.write(ndatetime.strftime('%Y年%m月%d日%H:%M:%S'))
...
```



