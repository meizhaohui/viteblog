# 日期和时间模块-`time`时间模块


[[toc]]

## `time`模块

查看`time`模块有哪些函数或方法：

```py
$ python
Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import time
>>> time.
time.altzone         time.clock(          time.daylight        time.gmtime(         time.mktime(         time.perf_counter(   time.sleep(          time.strptime(       time.time(           time.tzname
time.asctime(        time.ctime(          time.get_clock_info( time.localtime(      time.monotonic(      time.process_time(   time.strftime(       time.struct_time(    time.timezone
>>> exit()
```

此模块并非所有平台提供所有功能，因平台而异。

以下是对一些术语和惯例的解释：

- epoch纪元初始时间因平台而异。对于Unix平台，初始时间是`1970,01,01,00:00:00（UTC）`。查看每个操作平台的初始时间可以使用`time.gmtime(0)`函数。
- 在所有POSIX平台上，从初始时间以来的秒数都不包括闰秒。
- 该模块中的函数可能不处理纪元时间以前和遥远未来的日期和时间，未来的分界点对于32位操作系统是2038年。在大多数的UNIX系统中UNIX时间戳存储为32位，这样会引发2038年问题或Y2038。
- 千年虫问题：Python依赖于平台的C库，该库通常没有2000年问题，因为所有日期和时间在内部都以自该纪元以来的秒表示。给定`％y`格式代码时，函数`strptime()`可以解析两位数的年份。解析两位数的年份时，将根据POSIX和ISO C标准进行转换：将值`69-99`映射到`1969-1999`，将值`0-68`映射到`2000-2068`。
- UTC是协调世界时(以前称为格林尼治标准时间，GMT)。缩写UTC不是一个错误，而是英语和法语之间的妥协。
- DST是夏令时，在一年中的某些时候，时区通常会调整一个小时。DST规则是神奇的(由当地法律决定)，每年都在变化。
- 各种实时函数的精度可能低于表示其值或参数的单位所建议的精度。例如。在大多数Unix系统上，时钟每秒仅滴答50或100次。
- 整个世界分为24个时区，每个时区都有自己的本地时间，`UTC`协议世界时与英国伦敦的本地时相同。中国的北京时区位于东八区，领先UTC八个小时。`UTC + 时区差 = 本地时间`， 时区差东为正，西为负。因此，把东八区时区差记为`+0800`。

### 时间元组`struct_time`

`time.struct_time`类，是`gmtime`,`localtime()`和`strptime()`等函数返回的时间值序列的类型。它是具有命名元组接口的对象：可以通过索引和属性名称访问值。 存在以下值：

| 序号 | 属性         |      字段    | 值                          |
|-----|-------------|-------------|----------------------------|
| 0   | `tm_year`   | 4位数年      |  如`2020`                       |
| 1   | `tm_mon`    | 月          |  `1`到`12`                     |
| 2   | `tm_mday`   | 日          |  `1`到`31`                     |
| 3   | `tm_hour`   | 小时         |  `0`到`23`                     |
| 4   | `tm_min`    | 分钟        |   `0`到`59`                     |
| 5   | `tm_sec`    | 秒         | `0`到`61` (60或61是闰秒)       |
| 6   | `tm_wday`   | 一周的第几日  | `0`到`6` (0是周一)               |
| 7   | `tm_yday`   | 一年的第几日  | `1`到`366`             |
| 8   | `tm_isdst`  | 夏令时      |  `-1`, `0`, `1`, 是决定是否为夏令时的标志 |

### `time.asctime([t])`接受时间元组并返回一个可读的形式字符串

`time.asctime([t])`函数将表示由`gmtime()`或`localtime()`返回的时间的元组或`struct_time`转换为以下形式的字符串：`Sun Jun 20 23:21:05 1993`。 如果未提供`t`，则使用`localtime()`返回的当前时间。`asctime()`不使用语言环境信息。

::: tip 说明
`time.asctime([t])`函数返回默认不会加换行符。
:::

```py
>>> import time

>>> time.asctime?
Docstring:
asctime([tuple]) -> string

Convert a time tuple to a string, e.g. 'Sat Jun 06 16:26:11 1998'.
When the time tuple is not present, current time as returned by localtime()
is used.
Type:      builtin_function_or_method

>>> time.asctime()
'Sun May 24 22:37:11 2020'

>>> print('now time is: %s. this is no trailing endline' % time.asctime())
now time is: Wed May 24 22:38:36 2020. this is no trailing endline
```

### `time.clock()`获取处理器时间

`time.clock()`在Unix系统中可以获取处理器时间，在Windows系统中可以返回第一次调用该函数后经过的时间(以秒为单位)的浮点数。从版本3.3开始不推荐使用：此功能的行为取决于平台：请根据您的要求使用`perf_counter()`或`process_time()`来具有明确定义的行为。

```py
>>> time.clock()
1e-07

>>> time.clock()
15.5999267

>>> time.clock()
18.5321979

>>> time.clock()
19.6224457

>>> time.clock()
20.509851

>>> time.clock()
21.280692
```


### `time.localtime([secs])`获取当地时间的时间元组

`time.localtime([secs])`接收时间戳(1970纪元后经过的浮点秒数)并返回当地时间下的时间元组`t`，如果未指定`secs`，则使用`time.time()`获取当前时间。

```py
>>> time.localtime()
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=26, tm_hour=8, tm_min=6, tm_sec=13, tm_wday=1, tm_yday=147, tm_isdst=0)

>>> time.localtime(time.time())
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=26, tm_hour=8, tm_min=6, tm_sec=45, tm_wday=1, tm_yday=147, tm_isdst=0)

>>> time.localtime(0)
time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=8, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=1, tm_isdst=0)
```

可以发现当`time.localtime(0)`时,`tm_hour=8`,这是因为参数0表示距离纪元的时间秒数，而本地时间为东8区，因此当UTC时间为0时，东8区的时间是8点。

### `time.ctime([secs])`将时间秒数转换成本地时间

`time.ctime([secs])`将自纪元以来的秒数转换为代表本地时间的字符串。等阶于`time.asctime(time.localtime())`:

```py
>>> time.ctime()
'Tue May 26 08:18:22 2020'

>>> time.asctime(time.localtime())
'Tue May 26 08:18:49 2020'
```


### `time.time()`获取纪元以来的时间秒数

`time.time()`获取纪元以来的时间秒数，可以通过`time.gmtime(0)`获取纪元开始时间。

```py
>>> time.time?
Docstring:
time() -> floating point number

Return the current time in seconds since the Epoch.
Fractions of a second may be present if the system clock provides them.
Type:      builtin_function_or_method

>>> time.time()
1590452682.4995768

>>> time.gmtime(0)
time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=1, tm_isdst=0)
```

### `time.gmtime([secs])`获取时间戳的时间元组

```py
>>> time.gmtime?
Docstring:
gmtime([seconds]) -> (tm_year, tm_mon, tm_mday, tm_hour, tm_min,
                       tm_sec, tm_wday, tm_yday, tm_isdst)

Convert seconds since the Epoch to a time tuple expressing UTC (a.k.a.
GMT).  When 'seconds' is not passed in, convert the current time instead.

If the platform supports the tm_gmtoff and tm_zone, they are available as
attributes only.
Type:      builtin_function_or_method

>>> time.gmtime()
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=26, tm_hour=0, tm_min=28, tm_sec=15, tm_wday=1, tm_yday=147, tm_isdst=
)

>>> time.gmtime(60)
time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=1, tm_sec=0, tm_wday=3, tm_yday=1, tm_isdst=0)

>>> time.gmtime(3600)
time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=1, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=1, tm_isdst=0)

>>> time.gmtime(36000)
time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=10, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=1, tm_isdst=0)

>>>
```

### `time.mktime(t)`将时间元组转换成时间戳

```py
>>> time.mktime?
Docstring:
mktime(tuple) -> floating point number

Convert a time tuple in local time to seconds since the Epoch.
Note that mktime(gmtime(0)) will not generally return zero for most
time zones; instead the returned value will either be equal to that
of the timezone or altzone attributes on the time module.
Type:      builtin_function_or_method

>>> time.localtime()
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=21, tm_min=58, tm_sec=18, tm_wday=2, tm_yday=148, tm_isdst=0)

>>> time.gmtime()
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=13, tm_min=58, tm_sec=23, tm_wday=2, tm_yday=148, tm_isdst=0)

>>> time.time()
1590587909.801845

>>> time.mktime(time.localtime())
1590587921.0

>>> time.mktime(time.localtime())
1590587926.0

>>>
```

### `time.sleep(seconds)`让程序暂停执行

```py
>>> time.sleep?
Docstring:
sleep(seconds)

Delay execution for a given number of seconds.  The argument may be
a floating point number for subsecond precision.
Type:      builtin_function_or_method

>>> time.sleep(2)

>>> for i in range(3):
...     print(time.localtime())
...     time.sleep(2)
...     print(time.localtime())
...
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=22, tm_min=2, tm_sec=51, tm_wday=2, tm_yday=148, tm_isdst=0)
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=22, tm_min=2, tm_sec=53, tm_wday=2, tm_yday=148, tm_isdst=0)
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=22, tm_min=2, tm_sec=53, tm_wday=2, tm_yday=148, tm_isdst=0)
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=22, tm_min=2, tm_sec=55, tm_wday=2, tm_yday=148, tm_isdst=0)
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=22, tm_min=2, tm_sec=55, tm_wday=2, tm_yday=148, tm_isdst=0)
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=22, tm_min=2, tm_sec=57, tm_wday=2, tm_yday=148, tm_isdst=0)

>>>
```
可以看出在`for`语句中，每次循环时中间都会暂停2秒再执行下一次循环。

### `time.strftime`将时间元组转换成指定格式的字符串

常用的格式化符号可见下面的帮助信息（注：后面的中文是我加上去的）：

```py
>>> time.strftime?
Docstring:
strftime(format[, tuple]) -> string

Convert a time tuple to a string according to a format specification.
See the library reference manual for formatting codes. When the time tuple
is not present, current time as returned by localtime() is used.

Commonly used format codes:

%Y  Year with century as a decimal number.  4位年份，如2020
%m  Month as a decimal number [01,12]. 月份，如05
%d  Day of the month as a decimal number [01,31]. 日期，如06
%H  Hour (24-hour clock) as a decimal number [00,23]. 24小时制小时数，如07
%M  Minute as a decimal number [00,59]. 分钟数，如08
%S  Second as a decimal number [00,61]. 秒数，如09
%z  Time zone offset from UTC. 时区偏差
%a  Locale's abbreviated weekday name. 本地简化星期名称
%A  Locale's full weekday name. 本地完整星期名称
%b  Locale's abbreviated month name. 简化月份名称
%B  Locale's full month name. 完整月份名称
%c  Locale's appropriate date and time representation. 本地相应的日期表示和时间表示
%I  Hour (12-hour clock) as a decimal number [01,12]. 12小时制小时数
%p  Locale's equivalent of either AM or PM. 上午或下午表示符

Other codes may be available on your platform.  See documentation for
the C library strftime function.
Type:      builtin_function_or_method

# 按4位年2位月2位日 2位时2位分2位秒输出当前时间
>>> time.strftime('%Y%m%d %H%M%S', time.localtime())
'20200527 221453'

>>> time.strftime('%Y%m%d %H%M%S', time.localtime())
'20200527 221455'

>>> time.strftime('%Y%m%d %H%M%S', time.localtime())
'20200527 221458'

>>> time.strftime('%Y%m%d %H%M%S', time.localtime())
'20200527 221500'

>>> time.strftime('%Y%m%d %H%M%S', time.localtime())
'20200527 221501'

>>> time.strftime('%Y%m%d %H%M%S', time.localtime())
'20200527 221503'

# 时间格式中加入其他元素
>>> time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime())
'2020年05月27日 22:19:10'

>>> time.strftime('%Y年%m月%d日 %H:%M:%S')
'2020年05月27日 22:21:50'

# 输出时间偏差和星期简写
>>> time.strftime('%Y年%m月%d日 %H:%M:%S %z %a')
'2020年05月27日 22:29:24 +0800 Wed'

# 输出时间偏差和星期全称
>>> time.strftime('%Y年%m月%d日 %H:%M:%S %z %A')
'2020年05月27日 22:29:33 +0800 Wednesday'


>>> time.strftime('%Y %B %d', time.gmtime(1))
'1970 January 01'

>>> time.strftime('%Y %b %d', time.gmtime(1))
'1970 Jan 01'

>>> time.strftime('%c', time.gmtime(1))
'Thu Jan  1 00:00:01 1970'

>>> time.strftime('%c')
'Wed May 27 22:35:20 2020'

>>> time.strftime('%c', time.gmtime(123456789))
'Thu Nov 29 21:33:09 1973'

# 数据太大，无法存储
>>> time.strftime('%c', time.gmtime(1234567891011121314))
---------------------------------------------------------------------------
OSError                                   Traceback (most recent call last)
<ipython-input-83-13fec9b44855> in <module>
----> 1 time.strftime('%c', time.gmtime(1234567891011121314))

OSError: [Errno 84] Value too large to be stored in data type

>>> time.strftime('%c', time.gmtime(12345678910111213))
'Tue Sep  2 08:40:13 391220960'

>>> time.strftime('%c', time.gmtime(123456789101112))
'Wed Nov 28 00:05:12 3914159'

>>> time.strftime('%c', time.gmtime(1234567891011))
'Wed Nov 25 05:16:51 41091'

>>> time.strftime('%c', time.gmtime(12345678910))
'Tue Mar 21 19:15:10 2361'

>>> time.strftime('%c', time.gmtime(123456789))
'Thu Nov 29 21:33:09 1973'

>>> time.strftime('%c', time.localtime())
'Wed May 27 22:39:01 2020'

>>>
```


### `time.strptime`将时间字符串按指定格式解析成时间元组

 `time.strptime(string, format)`将时间字符串按指定格式解析成时间元组,注意时间字符串在前，时间格式化参数在后。
 
```py
>>> time.strptime?
Docstring:
strptime(string, format) -> struct_time

Parse a string to a time tuple according to a format specification.
See the library reference manual for formatting codes (same as
strftime()).

Commonly used format codes:

%Y  Year with century as a decimal number.
%m  Month as a decimal number [01,12].
%d  Day of the month as a decimal number [01,31].
%H  Hour (24-hour clock) as a decimal number [00,23].
%M  Minute as a decimal number [00,59].
%S  Second as a decimal number [00,61].
%z  Time zone offset from UTC.
%a  Locale's abbreviated weekday name.
%A  Locale's full weekday name.
%b  Locale's abbreviated month name.
%B  Locale's full month name.
%c  Locale's appropriate date and time representation.
%I  Hour (12-hour clock) as a decimal number [01,12].
%p  Locale's equivalent of either AM or PM.

Other codes may be available on your platform.  See documentation for
the C library strftime function.
Type:      builtin_function_or_method

>>> time.strptime('20200527 224734', '%Y%m%d %H%M%S')
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=22, tm_min=47, tm_sec=34, tm_wday=2, tm_yday=148, tm_isdst=-1)

# 给的时间字符串与格式化字符串需要对应，不对应匹配则会抛出异常
>>> time.strptime('20200527 224734', '%Y年%m月%d日 %H:%M:%S')
--出现异常...
ValueError: time data '20200527 224734' does not match format '%Y年%m月%d日 %H:%M:%S'

>>> time.strptime('2020年05月27日 22:47:34', '%Y年%m月%d日 %H:%M:%S')
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=27, tm_hour=22, tm_min=47, tm_sec=34, tm_wday=2, tm_yday=148, tm_isdst=-1)

>>>
```



### `time.perf_counter()`计算程序运行时间

官方文档介绍如下：

> Return the value (in fractional seconds) of a performance counter, i.e. a clock with the highest available resolution to measure a short duration. It does include time elapsed during sleep and is system-wide. The reference point of the returned value is undefined, so that only the difference between the results of consecutive calls is valid.
    
 即：`time.perf_counter()`返回性能计数器的值（以分数秒为单位），即具有最高可用分辨率的时钟，以测量较短的持续时间。 它包含整个系统的睡眠时间。 返回值的参考点是不确定的，因此仅连续调用的结果之间的差有效。  
    
```py
>>> time.perf_counter?
Docstring:
perf_counter() -> float

Performance counter for benchmarking.
Type:      builtin_function_or_method
>>> def timeit(n):
...     start = time.perf_counter()
...     sum = 0
...     for i in range(n):
...         sum += i
...     time.sleep(n)
...     end = time.perf_counter()
...     print(start, end, end - start)
...

>>> timeit(3)
16912.547074853 16915.552290544 3.005215691002377

>>> timeit(10)
16927.02270078 16937.027870937 10.005170157000975
```
可以看到，当`n`值不同时，程序执行的时间不同，当`n`为3时，执行时间为`3.005215691002377`,当`n`为10时，执行时间为`10.005170157000975`,而这其中包含`time.sleep(n)`程序暂停的时间。

 time.process_time()计算程序(不含睡眠时间)的运行时间

官方文档介绍如下：

> Return the value (in fractional seconds) of the sum of the system and user CPU time of the current process. It does not include time elapsed during sleep. It is process-wide by definition. The reference point of the returned value is undefined, so that only the difference between the results of consecutive calls is valid.

即：返回当前进程的系统和用户CPU时间之和的值（以秒为单位）。 它不包括睡眠期间经过的时间。 根据定义，它是整个过程的。 返回值的参考点是不确定的，因此仅连续调用的结果之间的差有效。

```py
>>> time.process_time?
Docstring:
process_time() -> float

Process time for profiling: sum of the kernel and user-space CPU time.
Type:      builtin_function_or_method

>>> def timeit(n):
...     start = time.process_time()
...     sum = 0
...     for i in range(n):
...         sum += i
...     time.sleep(n)
...     end = time.process_time()
...     print(start, end, end - start)
...

>>> timeit(3)
21.771753 21.772565 0.0008119999999998129

>>> timeit(10)
21.81368 21.81468 0.0009999999999976694
```
可以发现此时并没有考虑程序暂停时所花费的时间。

计算程序的运行时间可以用`timeit`模块，后续补充。

### `time.get_clock_info(name)`获取指定时间类型的时钟信息

获取有关指定时钟的信息作为名称空间对象。 支持的时钟名称和读取其值的相应功能是：

- 'clock': `time.clock()`
- 'monotonic': `time.monotonic()`
- 'perf_counter': `time.perf_counter()`
- 'process_time': `time.process_time()`
- 'time': `time.time()`

```py
>>> time.get_clock_info?
Docstring:
get_clock_info(name: str) -> dict

Get information of the specified clock.
Type:      builtin_function_or_method

>>> time.get_clock_info('clock')
namespace(adjustable=False, implementation='clock()', monotonic=True, resolution=1e-06)

>>> time.get_clock_info('time')
namespace(adjustable=True, implementation='gettimeofday()', monotonic=False, resolution=1e-06)

>>> time.get_clock_info('monotonic')
namespace(adjustable=False, implementation='mach_absolute_time()', monotonic=True, resolution=1e-09)

>>> time.get_clock_info('perf_counter')
namespace(adjustable=False, implementation='mach_absolute_time()', monotonic=True, resolution=1e-09)

>>> time.get_clock_info('process_time')
namespace(adjustable=False, implementation='getrusage(RUSAGE_SELF)', monotonic=True, resolution=1e-06)
```

### `time.monotonic()`返回一个只增加的时钟

```py
>>> time.monotonic?
Docstring:
monotonic() -> float

Monotonic clock, cannot go backward.
Type:      builtin_function_or_method

>>> time.monotonic()
19785.01834342

>>> time.monotonic()
19786.86552583

>>> time.monotonic()
19787.973120366
```

### Timezone Constants时区常量

 - `time altzone`函数返回格林威治西部的夏令时地区的偏移秒数,如果该地区在格林威治东部会返回负值(如西欧，包括英国)。对夏令时启用地区才能使用。
 - `time.daylight`如果夏令时被定义，则该值为非零。
 - `time.timezone`属性是当地时区（未启动夏令时）距离格林威治的偏移秒数（美洲>0；大部分欧洲，亚洲，非洲 <= 0）。
 - `time.tzname`属性是包含两个字符串的元组：第一是当地非夏令时区的名称，第二个是当地的夏令时区的名称，如果没有设置夏令时区则第二个字符串不能使用。
 - 以上几个时区常量值与`time.tzset()`设置的时区相关，不同时区时它们的值会不一样。

```py
>>> time.altzone
-28800

>>> time.daylight
0

>>> time.timezone
-28800

>>> time.tzname
('CST', 'CST')
```

### 修改时区

查看所有的时区：

```py
>>> pytz.all_timezones
['Africa/Abidjan',
 'Africa/Accra',
 'Africa/Addis_Ababa',
 'Africa/Algiers',
 'Africa/Asmara',
 'Africa/Asmera',
 'Africa/Bamako',
 'Africa/Bangui',
 'Africa/Banjul',
 'Africa/Bissau',
 'Africa/Blantyre',
 'Africa/Brazzaville',
 'Africa/Bujumbura',
 'Africa/Cairo',
 'Africa/Casablanca',
 'Africa/Ceuta',
 'Africa/Conakry',
 'Africa/Dakar',
 'Africa/Dar_es_Salaam',
 'Africa/Djibouti',
 'Africa/Douala',
 'Africa/El_Aaiun',
 'Africa/Freetown',
 'Africa/Gaborone',
 'Africa/Harare',
 'Africa/Johannesburg',
 'Africa/Juba',
 'Africa/Kampala',
 'Africa/Khartoum',
 'Africa/Kigali',
 'Africa/Kinshasa',
 'Africa/Lagos',
 'Africa/Libreville',
 'Africa/Lome',
 'Africa/Luanda',
 'Africa/Lubumbashi',
 'Africa/Lusaka',
 'Africa/Malabo',
 'Africa/Maputo',
 'Africa/Maseru',
 'Africa/Mbabane',
 'Africa/Mogadishu',
 'Africa/Monrovia',
 'Africa/Nairobi',
 'Africa/Ndjamena',
 'Africa/Niamey',
 'Africa/Nouakchott',
 'Africa/Ouagadougou',
 'Africa/Porto-Novo',
 'Africa/Sao_Tome',
 'Africa/Timbuktu',
 'Africa/Tripoli',
 'Africa/Tunis',
 'Africa/Windhoek',
 'America/Adak',
 'America/Anchorage',
 'America/Anguilla',
 'America/Antigua',
 'America/Araguaina',
 'America/Argentina/Buenos_Aires',
 'America/Argentina/Catamarca',
 'America/Argentina/ComodRivadavia',
 'America/Argentina/Cordoba',
 'America/Argentina/Jujuy',
 'America/Argentina/La_Rioja',
 'America/Argentina/Mendoza',
 'America/Argentina/Rio_Gallegos',
 'America/Argentina/Salta',
 'America/Argentina/San_Juan',
 'America/Argentina/San_Luis',
 'America/Argentina/Tucuman',
 'America/Argentina/Ushuaia',
 'America/Aruba',
 'America/Asuncion',
 'America/Atikokan',
 'America/Atka',
 'America/Bahia',
 'America/Bahia_Banderas',
 'America/Barbados',
 'America/Belem',
 'America/Belize',
 'America/Blanc-Sablon',
 'America/Boa_Vista',
 'America/Bogota',
 'America/Boise',
 'America/Buenos_Aires',
 'America/Cambridge_Bay',
 'America/Campo_Grande',
 'America/Cancun',
 'America/Caracas',
 'America/Catamarca',
 'America/Cayenne',
 'America/Cayman',
 'America/Chicago',
 'America/Chihuahua',
 'America/Coral_Harbour',
 'America/Cordoba',
 'America/Costa_Rica',
 'America/Creston',
 'America/Cuiaba',
 'America/Curacao',
 'America/Danmarkshavn',
 'America/Dawson',
 'America/Dawson_Creek',
 'America/Denver',
 'America/Detroit',
 'America/Dominica',
 'America/Edmonton',
 'America/Eirunepe',
 'America/El_Salvador',
 'America/Ensenada',
 'America/Fort_Nelson',
 'America/Fort_Wayne',
 'America/Fortaleza',
 'America/Glace_Bay',
 'America/Godthab',
 'America/Goose_Bay',
 'America/Grand_Turk',
 'America/Grenada',
 'America/Guadeloupe',
 'America/Guatemala',
 'America/Guayaquil',
 'America/Guyana',
 'America/Halifax',
 'America/Havana',
 'America/Hermosillo',
 'America/Indiana/Indianapolis',
 'America/Indiana/Knox',
 'America/Indiana/Marengo',
 'America/Indiana/Petersburg',
 'America/Indiana/Tell_City',
 'America/Indiana/Vevay',
 'America/Indiana/Vincennes',
 'America/Indiana/Winamac',
 'America/Indianapolis',
 'America/Inuvik',
 'America/Iqaluit',
 'America/Jamaica',
 'America/Jujuy',
 'America/Juneau',
 'America/Kentucky/Louisville',
 'America/Kentucky/Monticello',
 'America/Knox_IN',
 'America/Kralendijk',
 'America/La_Paz',
 'America/Lima',
 'America/Los_Angeles',
 'America/Louisville',
 'America/Lower_Princes',
 'America/Maceio',
 'America/Managua',
 'America/Manaus',
 'America/Marigot',
 'America/Martinique',
 'America/Matamoros',
 'America/Mazatlan',
 'America/Mendoza',
 'America/Menominee',
 'America/Merida',
 'America/Metlakatla',
 'America/Mexico_City',
 'America/Miquelon',
 'America/Moncton',
 'America/Monterrey',
 'America/Montevideo',
 'America/Montreal',
 'America/Montserrat',
 'America/Nassau',
 'America/New_York',
 'America/Nipigon',
 'America/Nome',
 'America/Noronha',
 'America/North_Dakota/Beulah',
 'America/North_Dakota/Center',
 'America/North_Dakota/New_Salem',
 'America/Nuuk',
 'America/Ojinaga',
 'America/Panama',
 'America/Pangnirtung',
 'America/Paramaribo',
 'America/Phoenix',
 'America/Port-au-Prince',
 'America/Port_of_Spain',
 'America/Porto_Acre',
 'America/Porto_Velho',
 'America/Puerto_Rico',
 'America/Punta_Arenas',
 'America/Rainy_River',
 'America/Rankin_Inlet',
 'America/Recife',
 'America/Regina',
 'America/Resolute',
 'America/Rio_Branco',
 'America/Rosario',
 'America/Santa_Isabel',
 'America/Santarem',
 'America/Santiago',
 'America/Santo_Domingo',
 'America/Sao_Paulo',
 'America/Scoresbysund',
 'America/Shiprock',
 'America/Sitka',
 'America/St_Barthelemy',
 'America/St_Johns',
 'America/St_Kitts',
 'America/St_Lucia',
 'America/St_Thomas',
 'America/St_Vincent',
 'America/Swift_Current',
 'America/Tegucigalpa',
 'America/Thule',
 'America/Thunder_Bay',
 'America/Tijuana',
 'America/Toronto',
 'America/Tortola',
 'America/Vancouver',
 'America/Virgin',
 'America/Whitehorse',
 'America/Winnipeg',
 'America/Yakutat',
 'America/Yellowknife',
 'Antarctica/Casey',
 'Antarctica/Davis',
 'Antarctica/DumontDUrville',
 'Antarctica/Macquarie',
 'Antarctica/Mawson',
 'Antarctica/McMurdo',
 'Antarctica/Palmer',
 'Antarctica/Rothera',
 'Antarctica/South_Pole',
 'Antarctica/Syowa',
 'Antarctica/Troll',
 'Antarctica/Vostok',
 'Arctic/Longyearbyen',
 'Asia/Aden',
 'Asia/Almaty',
 'Asia/Amman',
 'Asia/Anadyr',
 'Asia/Aqtau',
 'Asia/Aqtobe',
 'Asia/Ashgabat',
 'Asia/Ashkhabad',
 'Asia/Atyrau',
 'Asia/Baghdad',
 'Asia/Bahrain',
 'Asia/Baku',
 'Asia/Bangkok',
 'Asia/Barnaul',
 'Asia/Beirut',
 'Asia/Bishkek',
 'Asia/Brunei',
 'Asia/Calcutta',
 'Asia/Chita',
 'Asia/Choibalsan',
 'Asia/Chongqing',
 'Asia/Chungking',
 'Asia/Colombo',
 'Asia/Dacca',
 'Asia/Damascus',
 'Asia/Dhaka',
 'Asia/Dili',
 'Asia/Dubai',
 'Asia/Dushanbe',
 'Asia/Famagusta',
 'Asia/Gaza',
 'Asia/Harbin',
 'Asia/Hebron',
 'Asia/Ho_Chi_Minh',
 'Asia/Hong_Kong',
 'Asia/Hovd',
 'Asia/Irkutsk',
 'Asia/Istanbul',
 'Asia/Jakarta',
 'Asia/Jayapura',
 'Asia/Jerusalem',
 'Asia/Kabul',
 'Asia/Kamchatka',
 'Asia/Karachi',
 'Asia/Kashgar',
 'Asia/Kathmandu',
 'Asia/Katmandu',
 'Asia/Khandyga',
 'Asia/Kolkata',
 'Asia/Krasnoyarsk',
 'Asia/Kuala_Lumpur',
 'Asia/Kuching',
 'Asia/Kuwait',
 'Asia/Macao',
 'Asia/Macau',
 'Asia/Magadan',
 'Asia/Makassar',
 'Asia/Manila',
 'Asia/Muscat',
 'Asia/Nicosia',
 'Asia/Novokuznetsk',
 'Asia/Novosibirsk',
 'Asia/Omsk',
 'Asia/Oral',
 'Asia/Phnom_Penh',
 'Asia/Pontianak',
 'Asia/Pyongyang',
 'Asia/Qatar',
 'Asia/Qostanay',
 'Asia/Qyzylorda',
 'Asia/Rangoon',
 'Asia/Riyadh',
 'Asia/Saigon',
 'Asia/Sakhalin',
 'Asia/Samarkand',
 'Asia/Seoul',
 'Asia/Shanghai',
 'Asia/Singapore',
 'Asia/Srednekolymsk',
 'Asia/Taipei',
 'Asia/Tashkent',
 'Asia/Tbilisi',
 'Asia/Tehran',
 'Asia/Tel_Aviv',
 'Asia/Thimbu',
 'Asia/Thimphu',
 'Asia/Tokyo',
 'Asia/Tomsk',
 'Asia/Ujung_Pandang',
 'Asia/Ulaanbaatar',
 'Asia/Ulan_Bator',
 'Asia/Urumqi',
 'Asia/Ust-Nera',
 'Asia/Vientiane',
 'Asia/Vladivostok',
 'Asia/Yakutsk',
 'Asia/Yangon',
 'Asia/Yekaterinburg',
 'Asia/Yerevan',
 'Atlantic/Azores',
 'Atlantic/Bermuda',
 'Atlantic/Canary',
 'Atlantic/Cape_Verde',
 'Atlantic/Faeroe',
 'Atlantic/Faroe',
 'Atlantic/Jan_Mayen',
 'Atlantic/Madeira',
 'Atlantic/Reykjavik',
 'Atlantic/South_Georgia',
 'Atlantic/St_Helena',
 'Atlantic/Stanley',
 'Australia/ACT',
 'Australia/Adelaide',
 'Australia/Brisbane',
 'Australia/Broken_Hill',
 'Australia/Canberra',
 'Australia/Currie',
 'Australia/Darwin',
 'Australia/Eucla',
 'Australia/Hobart',
 'Australia/LHI',
 'Australia/Lindeman',
 'Australia/Lord_Howe',
 'Australia/Melbourne',
 'Australia/NSW',
 'Australia/North',
 'Australia/Perth',
 'Australia/Queensland',
 'Australia/South',
 'Australia/Sydney',
 'Australia/Tasmania',
 'Australia/Victoria',
 'Australia/West',
 'Australia/Yancowinna',
 'Brazil/Acre',
 'Brazil/DeNoronha',
 'Brazil/East',
 'Brazil/West',
 'CET',
 'CST6CDT',
 'Canada/Atlantic',
 'Canada/Central',
 'Canada/Eastern',
 'Canada/Mountain',
 'Canada/Newfoundland',
 'Canada/Pacific',
 'Canada/Saskatchewan',
 'Canada/Yukon',
 'Chile/Continental',
 'Chile/EasterIsland',
 'Cuba',
 'EET',
 'EST',
 'EST5EDT',
 'Egypt',
 'Eire',
 'Etc/GMT',
 'Etc/GMT+0',
 'Etc/GMT+1',
 'Etc/GMT+10',
 'Etc/GMT+11',
 'Etc/GMT+12',
 'Etc/GMT+2',
 'Etc/GMT+3',
 'Etc/GMT+4',
 'Etc/GMT+5',
 'Etc/GMT+6',
 'Etc/GMT+7',
 'Etc/GMT+8',
 'Etc/GMT+9',
 'Etc/GMT-0',
 'Etc/GMT-1',
 'Etc/GMT-10',
 'Etc/GMT-11',
 'Etc/GMT-12',
 'Etc/GMT-13',
 'Etc/GMT-14',
 'Etc/GMT-2',
 'Etc/GMT-3',
 'Etc/GMT-4',
 'Etc/GMT-5',
 'Etc/GMT-6',
 'Etc/GMT-7',
 'Etc/GMT-8',
 'Etc/GMT-9',
 'Etc/GMT0',
 'Etc/Greenwich',
 'Etc/UCT',
 'Etc/UTC',
 'Etc/Universal',
 'Etc/Zulu',
 'Europe/Amsterdam',
 'Europe/Andorra',
 'Europe/Astrakhan',
 'Europe/Athens',
 'Europe/Belfast',
 'Europe/Belgrade',
 'Europe/Berlin',
 'Europe/Bratislava',
 'Europe/Brussels',
 'Europe/Bucharest',
 'Europe/Budapest',
 'Europe/Busingen',
 'Europe/Chisinau',
 'Europe/Copenhagen',
 'Europe/Dublin',
 'Europe/Gibraltar',
 'Europe/Guernsey',
 'Europe/Helsinki',
 'Europe/Isle_of_Man',
 'Europe/Istanbul',
 'Europe/Jersey',
 'Europe/Kaliningrad',
 'Europe/Kiev',
 'Europe/Kirov',
 'Europe/Lisbon',
 'Europe/Ljubljana',
 'Europe/London',
 'Europe/Luxembourg',
 'Europe/Madrid',
 'Europe/Malta',
 'Europe/Mariehamn',
 'Europe/Minsk',
 'Europe/Monaco',
 'Europe/Moscow',
 'Europe/Nicosia',
 'Europe/Oslo',
 'Europe/Paris',
 'Europe/Podgorica',
 'Europe/Prague',
 'Europe/Riga',
 'Europe/Rome',
 'Europe/Samara',
 'Europe/San_Marino',
 'Europe/Sarajevo',
 'Europe/Saratov',
 'Europe/Simferopol',
 'Europe/Skopje',
 'Europe/Sofia',
 'Europe/Stockholm',
 'Europe/Tallinn',
 'Europe/Tirane',
 'Europe/Tiraspol',
 'Europe/Ulyanovsk',
 'Europe/Uzhgorod',
 'Europe/Vaduz',
 'Europe/Vatican',
 'Europe/Vienna',
 'Europe/Vilnius',
 'Europe/Volgograd',
 'Europe/Warsaw',
 'Europe/Zagreb',
 'Europe/Zaporozhye',
 'Europe/Zurich',
 'GB',
 'GB-Eire',
 'GMT',
 'GMT+0',
 'GMT-0',
 'GMT0',
 'Greenwich',
 'HST',
 'Hongkong',
 'Iceland',
 'Indian/Antananarivo',
 'Indian/Chagos',
 'Indian/Christmas',
 'Indian/Cocos',
 'Indian/Comoro',
 'Indian/Kerguelen',
 'Indian/Mahe',
 'Indian/Maldives',
 'Indian/Mauritius',
 'Indian/Mayotte',
 'Indian/Reunion',
 'Iran',
 'Israel',
 'Jamaica',
 'Japan',
 'Kwajalein',
 'Libya',
 'MET',
 'MST',
 'MST7MDT',
 'Mexico/BajaNorte',
 'Mexico/BajaSur',
 'Mexico/General',
 'NZ',
 'NZ-CHAT',
 'Navajo',
 'PRC',
 'PST8PDT',
 'Pacific/Apia',
 'Pacific/Auckland',
 'Pacific/Bougainville',
 'Pacific/Chatham',
 'Pacific/Chuuk',
 'Pacific/Easter',
 'Pacific/Efate',
 'Pacific/Enderbury',
 'Pacific/Fakaofo',
 'Pacific/Fiji',
 'Pacific/Funafuti',
 'Pacific/Galapagos',
 'Pacific/Gambier',
 'Pacific/Guadalcanal',
 'Pacific/Guam',
 'Pacific/Honolulu',
 'Pacific/Johnston',
 'Pacific/Kiritimati',
 'Pacific/Kosrae',
 'Pacific/Kwajalein',
 'Pacific/Majuro',
 'Pacific/Marquesas',
 'Pacific/Midway',
 'Pacific/Nauru',
 'Pacific/Niue',
 'Pacific/Norfolk',
 'Pacific/Noumea',
 'Pacific/Pago_Pago',
 'Pacific/Palau',
 'Pacific/Pitcairn',
 'Pacific/Pohnpei',
 'Pacific/Ponape',
 'Pacific/Port_Moresby',
 'Pacific/Rarotonga',
 'Pacific/Saipan',
 'Pacific/Samoa',
 'Pacific/Tahiti',
 'Pacific/Tarawa',
 'Pacific/Tongatapu',
 'Pacific/Truk',
 'Pacific/Wake',
 'Pacific/Wallis',
 'Pacific/Yap',
 'Poland',
 'Portugal',
 'ROC',
 'ROK',
 'Singapore',
 'Turkey',
 'UCT',
 'US/Alaska',
 'US/Aleutian',
 'US/Arizona',
 'US/Central',
 'US/East-Indiana',
 'US/Eastern',
 'US/Hawaii',
 'US/Indiana-Starke',
 'US/Michigan',
 'US/Mountain',
 'US/Pacific',
 'US/Samoa',
 'UTC',
 'Universal',
 'W-SU',
 'WET',
 'Zulu']
```

设置`TZ`环境变量，并使用`time.tzset()`使时间转换规则生效

官方文档中介绍`time.tzset()`如下：
> `time.tzset()` Resets the time conversion rules used by the library routines. The environment variable TZ specifies how this is done. 
> 
>  Availability: Unix.
> 
> Note: Although in many cases, changing the TZ environment variable may affect the output of functions like localtime() without calling tzset(), this behavior should not be relied on.The TZ environment variable should contain no whitespace.

即：
> 通过设置环境变量`TZ`来重置库程序使用的时间转换规则。 
> 
> 可用性：Unix。
> 
> 注意: 尽管在很多情况下，更改`TZ`环境变量可能会影响诸如`localtime()`之类的函数的输出而无需调用`tzset()`，但不应依赖此行为。
>
> TZ环境变量不应包含空格。


也就是说，我们在更改`TZ`环境变量后，应该使用`time.tzset()`使时区切换生效。

```py
>>> time.tzset?
Docstring:
tzset()

Initialize, or reinitialize, the local timezone to the value stored in
os.environ['TZ']. The TZ environment variable should be specified in
standard Unix timezone format as documented in the tzset man page
(eg. 'US/Eastern', 'Europe/Amsterdam'). Unknown timezones will silently
fall back to UTC. If the TZ environment variable is not set, the local
timezone is set to the systems best guess of wallclock time.
Changing the TZ environment variable without calling tzset *may* change
the local timezone used by methods such as localtime, but this behaviour
should not be relied on.
Type:      builtin_function_or_method

>>> import os

# 设置TZ环境变量
>>> os.environ['TZ'] = 'UTC'

# 重新设置时区为标准时区
>>> time.tzset()

>>> time.altzone
0

>>> time.daylight
0

>>> time.timezone
0

# 查看当前时区属性
>>> time.tzname
('UTC', 'UTC')

# 因为时区设置为UTC标准时区，可以发现此时tm_hour比北京时间小8
>>> time.localtime()
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=28, tm_hour=14, tm_min=5, tm_sec=9, tm_wday=3, tm_yday=149, tm_isdst=0)

>>> time.strftime('%Y年%m月%d日 %H:%M:%S %z')
'2020年05月28日 14:06:26 +0000'


# 重新设置时区
>>> os.environ['TZ'] = 'US/Hawaii'

>>> time.strftime('%Y年%m月%d日 %H:%M:%S %z')
'2020年05月28日 04:09:42 -1000'

# 使时区规则生效
>>> time.tzset()

>>> time.altzone
36000

>>> time.daylight
0

>>> time.timezone
36000

>>> time.tzname
('HST', 'HST')

# 再次查看时间
>>> time.strftime('%Y年%m月%d日 %H:%M:%S %z')
'2020年05月28日 04:10:22 -1000'

>>> time.localtime()
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=28, tm_hour=4, tm_min=10, tm_sec=28, tm_wday=3, tm_yday=149, tm_isdst=0)
```

参考：
- [Python time.tzsets 代码实例 https://www.kutu66.com//Python-Module-Examples/article_59589](https://www.kutu66.com//Python-Module-Examples/article_59589)
- [time — Time access and conversions https://docs.python.org/3.6/library/time.html](https://docs.python.org/3.6/library/time.html)

