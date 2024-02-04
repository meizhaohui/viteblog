# 日期和时间模块-`fleming`时区模块

[[toc]]

## 介绍

> This package contains Fleming, which contains a set of routines for doing datetime manipulation. Named after Sandford Fleming, the father of worldwide standard timezones, this package is meant to aid datetime manipulations with regards to timezones.
>
> Fleming addresses some of the common difficulties with timezones and datetime objects, such as performing arithmetic and datetime truncation across a Daylight Savings Time border. It also provides utilities for generating date ranges and getting unix times with respect to timezones.

即：该软件包包含Fleming，其中包含一组用于执行日期时间操作的例程。 该软件包以全球标准时区之父桑福德·弗莱明（Sandford Fleming）的名字命名，旨在帮助对时区进行日期时间操纵。

弗莱明（Fleming）解决了时区和日期时间对象的一些常见困难，例如跨夏令时边界执行算术和日期时间截断。 它还提供了用于生成日期范围和获取相对于时区的Unix时间的实用程序。

Fleming接受pytz时区对象作为参数，并且假定用户对pytz有基本的了解。 如果你不了解pytz模块，可以参考[模块-日期和时间模块之pytz时区模块](./X_time_and_date_module_pytz.html)了解有关pytz的更多信息。

## 安装

```sh
$ pip install fleming
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting fleming
  Downloading http://mirrors.aliyun.com/pypi/packages/c0/8c/42972e31f78e54dcd7fe74677439e03037b2ba11af994d65324791a27fe4/fleming-0.5.0-py2.py3-none-any.whl (9.7 kB)
Requirement already satisfied: python-dateutil>=2.2 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from fleming) (2.8.1)
Requirement already satisfied: pytz>=2013.9 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from fleming) (2020.1)
Requirement already satisfied: six>=1.5 in /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages (from python-dateutil>=2.2->fleming) (1.14.0)
Installing collected packages: fleming
Successfully installed fleming-0.5.0
```

查看`fleming`模块有哪些函数或方法：

```py
$ python
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import fleming
>>> fleming.
fleming.add_timedelta( fleming.convert_to_tz( fleming.floor(         fleming.unix_time(
fleming.ceil(          fleming.fleming        fleming.intervals(
>>> exit()
```

## 功能概述

下面是此软件包中每个功能的简要说明。 之后，将对功能进行更详细的说明和高级用法。 单击功能名称以转到其详细说明。

- `convert_to_tz`：将日期时间对象转换为指定时区的时间对象。
- `add_timedelta`：将一个timedelta添加到datetime对象。
- `floor`：将日期时间对象向下舍入到上一个时间间隔。
- `ceil`：将日期时间对象四舍五入到下一个时间间隔。
- `interval`：以给定的时间间隔获取时间范围。
- `unix_time`：返回日期时间对象的unix时间戳。



## `convert_to_tz`将日期时间对象转换指定时区的时间对象

` fleming.convert_to_tz(dt, tz, return_naive=False)` 将一个`datetime`对象转换成另一个时区的`datetime`对象。

参数说明：

- `dt`，datetime对象，如果datetime对象没有时区设置，则默认以UTC作为其时区。
- `tz`，pytz模块的timezone对象，即需要转换到哪个时区去。
- `return_naive=False`是否转换成`naive datetime object`即是否转换成无时区的datetime对象，默认是不转换，即保留时区信息。

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

# 导入模块
>>> from datetime import datetime

>>> from fleming import convert_to_tz

>>> from pytz import UTC, timezone

>>> datetime?
Init signature: datetime(self, /, *args, **kwargs)
Docstring:
datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints.
File:           /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/datetime.py
Type:           type
Subclasses:

# 构建标准UTC标准时间datetime对象
>>> dt_utc =  datetime(2020,7,15,12,45,20, tzinfo=UTC)

>>> dt_utc
datetime.datetime(2020, 7, 15, 12, 45, 20, tzinfo=<UTC>)

>>> print(dt_utc)
2020-07-15 12:45:20+00:00
      
# 创建中国时区对象
>>> china_timezone = timezone('Asia/Shanghai')

>>> china_timezone
<DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>

# 将标准时间datetime对象转换到亚洲/上海时区来，得到中国的时间
>>> dt_local = convert_to_tz(dt_utc, china_timezone)

# 可以看到，正常转换成中国的时间，中国的时间比标准时间早8个小时
>>> dt_local
datetime.datetime(2020, 7, 15, 20, 45, 20, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

# 打印时间，最后带时区信息
>>> print(dt_local)
2020-07-15 20:45:20+08:00
      
# 注意，转换时对原来的datetime对象不会产生影响，只会产生一个新的对象
>>> dt_utc
datetime.datetime(2020, 7, 15, 12, 45, 20, tzinfo=<UTC>)
```

我们再定义一个时区，将UTC标准时间对象转换成不带时区对象的datetime对象：

```python
# 创建美国东部时区
>>> eastern = timezone('US/Eastern')

>>> eastern
<DstTzInfo 'US/Eastern' LMT-1 day, 19:04:00 STD>

# 将UTC标准时间转换成美国东部时区时间对象，并且不带时区信息
>>> dt_eastern = convert_to_tz(dt_utc, eastern, return_naive=True)

# 可以看到，正常转换成美国东部的时间，美国东部时间比标准时间晚4个小时，此时datetime对象中已经没有时区信息
>>> dt_eastern
datetime.datetime(2020, 7, 15, 8, 45, 20)

# 打印时间，最后没有时区信息
>>> print(dt_eastern)
2020-07-15 08:45:20

# 注意，转换时对原来的datetime对象不会产生影响，只会产生一个新的对象
>>> dt_utc
datetime.datetime(2020, 7, 15, 12, 45, 20, tzinfo=<UTC>)
```

这个时间，再不应该对转换后的时间再进行转换，转换过程中有可能得到的结果不是你想要的！



我们尝试再进一步转换：

```python
# 将中国的本地时间转换成美国东部时间
>>> local_2_eastern = convert_to_tz(dt_local, eastern)

# 因为dt_local中带有时区信息，所以此时转换到美国东部时间时，转换结果正常，得到早上8:45的时间，与上面的dt_eastern时间是一样的
>>> local_2_eastern
datetime.datetime(2020, 7, 15, 8, 45, 20, tzinfo=<DstTzInfo 'US/Eastern' EDT-1 day, 20:00:00 DST>)

# 打印美国东部时间，此时结果是正确的！
>>> print(local_2_eastern)
2020-07-15 08:45:20-04:00

# 将美国东部时间转换成中国时间，此时因为dt_eastern并没有时区信息，得到的结果是16:45，而不是20:45，可以发现此处错误了！
# 原因：因为dt_eastern并没有带时区信息，所以conver_to_tz函数将dt_eastern当做了UTC标准时间，并没有把它当前美国东部(-04:00)时区时间，dt_eastern时间是早上8:45，按照中国时间比UTC标准时间早8小时计算，转换后中国时间就是16:45，也就是下面的结果，而实际上现在中国是20:45，也就是中间相差了4小时呢！！！
>>> eastern_2_local = convert_to_tz(dt_eastern, china_timezone)

# 这是一个错误的结果！
>>> eastern_2_local
datetime.datetime(2020, 7, 15, 16, 45, 20, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

>>>
```

总结，**无论什么时间，只要涉及到时间对象的转换，一定通过UTC标准时间进行计算！！对UTC标准时间进行时区转换再得到最好要的结果！**



## `add_timedelta`给datetime对象增加时间增量

`fleming.add_timedelta(dt, td, within_tz=None)`给datetime对象增加时间增量。

参数说明：

- `dt`，datetime对象，如果datetime对象没有时区设置，则默认以UTC作为其时区。
- `td`，timedelta对象，需要添加的时间增量。
- `within_tz`，pytz模块的timezone对象，如果指定该参数，则dt将在日期时间算术之前转换为该时区，然后再转换回其原始时区。

```python
>>> from datetime import timedelta

>>> from fleming import add_timedelta

# UTC标准时间,为2020年7月15日
>>> dt_utc
datetime.datetime(2020, 7, 15, 12, 45, 20, tzinfo=<UTC>)

# 在UTC标准时间的基础上增加两周，变成了2020年7月29日，此时时间对象仍然是UTC标准时间对象
>>> dt_delta1 = add_timedelta(dt_utc, timedelta(weeks=2))

# 通过UTC进行时间增量处理，得到的结果是正确的
>>> dt_delta1
datetime.datetime(2020, 7, 29, 12, 45, 20, tzinfo=<UTC>)

# 指定的转换过程中需要使用的时区，会先将dt_utc转换成美国东部时间，再增加两周，再将美国东部时间转换成UTC标准时间，此时转换的结果也是正确的
>>> dt_delta2 = add_timedelta(dt_utc, timedelta(weeks=2), within_tz=eastern)

>>> dt_delta2
datetime.datetime(2020, 7, 29, 12, 45, 20, tzinfo=<UTC>)

# 将中国本地时间加两周，最终的结果也是对的
>>> dt_delta3 = add_timedelta(dt_local, timedelta(weeks=2), within_tz=eastern)

>>> dt_delta3
datetime.datetime(2020, 7, 29, 20, 45, 20, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

>>>
```

## `floor`向下取最近的时间边界值

`fleming.floor(dt, within_tz=None, year=None, month=None, week=None, day=None, hour=None, minute=None, second=None, microsecond=None, extra_td_if_floor=None)`向下取最近的时间边界值。将日期时间四舍五入到最接近的时间间隔。 可用的时间间隔是年`year`，月`month`，周`week`，日`day`，小时`hour`，分钟`minute`，秒`second`和微秒`microsecond`。

参数中需要注意的是`week`参数，代码周，只能是1或默认的`None`，指定`week`时则`year`和`month`参数不生效。

```python
$ ipython
Python 3.6.8 (v3.6.8:3c6b436a57, Dec 24 2018, 02:10:22)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

>>> from datetime import datetime

>>> from pytz import timezone, UTC

>>> from fleming import floor, convert_to_tz

>>> today = datetime.today()

# 本地时间，不带时区信息
>>> today
datetime.datetime(2020, 7, 15, 22, 15, 33, 460350)

# 本地时间，带时区信息
>> dt_local = today.replace(tzinfo=timezone('Asia/Shanghai'))

# 本地时间，带时区信息
>>> dt_local
datetime.datetime(2020, 7, 15, 22, 15, 33, 460350, tzinfo=<DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>)

# 将本地时间转换成UTC标准时间
>>> dt_utc = convert_to_tz(dt_local, UTC)

# UTC标准时间
>>> dt_utc
datetime.datetime(2020, 7, 15, 14, 9, 33, 460350, tzinfo=<UTC>)

>>>
```

### 对无时区时间对象进行处理

对年和月间隔的处理：

```python
>>> floor(today, year=1)
datetime.datetime(2020, 1, 1, 0, 0)

>>> floor(today, year=2)
datetime.datetime(2020, 1, 1, 0, 0)

>>> floor(today, year=3)
datetime.datetime(2019, 1, 1, 0, 0)

>>> floor(today, year=4)
datetime.datetime(2020, 1, 1, 0, 0)

>>> floor(today, year=5)
datetime.datetime(2020, 1, 1, 0, 0)

>>> floor(today, year=6)
datetime.datetime(2016, 1, 1, 0, 0)

>>> floor(today, year=7)
datetime.datetime(2016, 1, 1, 0, 0)

>>> floor(today, year=8)
datetime.datetime(2016, 1, 1, 0, 0)

>>> floor(today, year=9)
datetime.datetime(2016, 1, 1, 0, 0)

>>> floor(today, year=10)
datetime.datetime(2020, 1, 1, 0, 0)

>>> floor(today, year=11)
datetime.datetime(2013, 1, 1, 0, 0)

>>> for i in range(1, 50):
...     print('floor(today,year=%s) = %s' % (i, floor(today, year=i)))
...
floor(today,year=1) = 2020-01-01 00:00:00
floor(today,year=2) = 2020-01-01 00:00:00
floor(today,year=3) = 2019-01-01 00:00:00
floor(today,year=4) = 2020-01-01 00:00:00
floor(today,year=5) = 2020-01-01 00:00:00
floor(today,year=6) = 2016-01-01 00:00:00
floor(today,year=7) = 2016-01-01 00:00:00
floor(today,year=8) = 2016-01-01 00:00:00
floor(today,year=9) = 2016-01-01 00:00:00
floor(today,year=10) = 2020-01-01 00:00:00
floor(today,year=11) = 2013-01-01 00:00:00
floor(today,year=12) = 2016-01-01 00:00:00
floor(today,year=13) = 2015-01-01 00:00:00
floor(today,year=14) = 2016-01-01 00:00:00
floor(today,year=15) = 2010-01-01 00:00:00
floor(today,year=16) = 2016-01-01 00:00:00
floor(today,year=17) = 2006-01-01 00:00:00
floor(today,year=18) = 2016-01-01 00:00:00
floor(today,year=19) = 2014-01-01 00:00:00
floor(today,year=20) = 2020-01-01 00:00:00
floor(today,year=21) = 2016-01-01 00:00:00
floor(today,year=22) = 2002-01-01 00:00:00
floor(today,year=23) = 2001-01-01 00:00:00
floor(today,year=24) = 2016-01-01 00:00:00
floor(today,year=25) = 2000-01-01 00:00:00
floor(today,year=26) = 2002-01-01 00:00:00
floor(today,year=27) = 1998-01-01 00:00:00
floor(today,year=28) = 2016-01-01 00:00:00
floor(today,year=29) = 2001-01-01 00:00:00
floor(today,year=30) = 2010-01-01 00:00:00
floor(today,year=31) = 2015-01-01 00:00:00
floor(today,year=32) = 2016-01-01 00:00:00
floor(today,year=33) = 2013-01-01 00:00:00
floor(today,year=34) = 2006-01-01 00:00:00
floor(today,year=35) = 1995-01-01 00:00:00
floor(today,year=36) = 2016-01-01 00:00:00
floor(today,year=37) = 1998-01-01 00:00:00
floor(today,year=38) = 2014-01-01 00:00:00
floor(today,year=39) = 1989-01-01 00:00:00
floor(today,year=40) = 2000-01-01 00:00:00
floor(today,year=41) = 2009-01-01 00:00:00
floor(today,year=42) = 2016-01-01 00:00:00
floor(today,year=43) = 1978-01-01 00:00:00
floor(today,year=44) = 1980-01-01 00:00:00
floor(today,year=45) = 1980-01-01 00:00:00
floor(today,year=46) = 1978-01-01 00:00:00
floor(today,year=47) = 1974-01-01 00:00:00
floor(today,year=48) = 2016-01-01 00:00:00
floor(today,year=49) = 2009-01-01 00:00:00

>>>
```

你发现的什么规律吗？当`year`值从1到49时，floor得到的值有什么规律？我完成没有发现，输出完成与预期不一样！:cry: 搞不懂！我猜后面的`ceil`方法也可能有类似的问题，我决定放弃这个模块的学习。Bye! 你如果想再深入的学习，可参考[https://fleming.readthedocs.io/en/develop/index.html](https://fleming.readthedocs.io/en/develop/index.html)。



参考：

- [https://pypi.org/project/fleming/](https://pypi.org/project/fleming/)
- [https://github.com/ambitioninc/fleming](https://github.com/ambitioninc/fleming)
- [https://fleming.readthedocs.io/en/develop/index.html](https://fleming.readthedocs.io/en/develop/index.html)



