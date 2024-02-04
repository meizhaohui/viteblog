# 日期和时间模块-`calendar`日历模块


[[toc]]

## `calendar`模块

查看`calendar`模块有哪些函数或方法：

```py
$ python                                                                                              
Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)] on win32     
Type "help", "copyright", "credits" or "license" for more information.                                
>>> import calendar                                                                                   
>>> calendar.                                                                                         
calendar.Calendar(            calendar.WEDNESDAY            calendar.month_abbr                       
calendar.EPOCH                calendar.c                    calendar.month_name                       
calendar.FRIDAY               calendar.calendar(            calendar.monthcalendar(                   
calendar.February             calendar.datetime             calendar.monthrange(                      
calendar.HTMLCalendar(        calendar.day_abbr             calendar.prcal(                           
calendar.IllegalMonthError(   calendar.day_name             calendar.prmonth(                         
calendar.IllegalWeekdayError( calendar.different_locale(    calendar.prweek(                          
calendar.January              calendar.error(               calendar.repeat(                          
calendar.LocaleHTMLCalendar(  calendar.firstweekday(        calendar.setfirstweekday(                 
calendar.LocaleTextCalendar(  calendar.format(              calendar.sys                              
calendar.MONDAY               calendar.formatstring(        calendar.timegm(                          
calendar.SATURDAY             calendar.isleap(              calendar.week(                            
calendar.SUNDAY               calendar.leapdays(            calendar.weekday(                         
calendar.THURSDAY             calendar.main(                calendar.weekheader(                      
calendar.TUESDAY              calendar.mdays                                                          
calendar.TextCalendar(        calendar.month(                                                         
>>> calendar.                                                                                         
```

### 周一到周日

看源码可知`(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(7)`，可知周一到周日是以数字0、1、2、3、4、5、6表示的。

```py
>>> calendar.MONDAY       
0                         
                          
>>> calendar.TUESDAY      
1                         
                          
>>> calendar.WEDNESDAY    
2                         
                          
>>> calendar.THURSDAY     
3                         
                          
>>> calendar.FRIDAY       
4                         
                          
>>> calendar.SATURDAY     
5                         
                          
>>> calendar.SUNDAY       
6                         
                          
>>>                       
```

### 每周的第一天

`calendar`默认将周一作为每周的第一天，你可以使用`setfirstweekday(weekday)`和`firstweekday()`来分别设置和获取每周的第一天：


```py
# 获取当前每周第一天
>>> calendar.firstweekday()
0

# 设置每周第一天为周日
>>> calendar.setfirstweekday(6)

# 获取当前每周第一天
>>> calendar.firstweekday()
6

# 设置每周第一天为周日
>>> calendar.setfirstweekday(calendar.SUNDAY)

# 获取当前每周第一天
>>> calendar.firstweekday()
6
```

### 闰年判断

使用`calendar.isleap(year)`判断年份`year`是否为闰年，是闰年时返回`True`，否则返回`False`：

```sh
>>> calendar.isleap?
Signature: calendar.isleap(year)
Docstring: Return True for leap years, False for non-leap years.
File:      d:\programfiles\python368\lib\calendar.py
Type:      function

# 2020年是闰年
>>> calendar.isleap(2020)
True

# 2000年也是闰年
>>> calendar.isleap(2000)
True

>>> calendar.isleap(1900)
False

>>> calendar.isleap(2021)
False
```


### 两个年份之间有多少个闰年

使用`calendar.leapdays(y1, y2)`获取两个年份之间有多少个闰年，包含`y1`年份，不包含`y2`年份，源码中并没有判断`y1`年份必须比`y2`年份小：

```py
>>> calendar.leapdays(1900,2020)
29

>>> calendar.leapdays(1900, 2021)
30

>>> calendar.leapdays(2000, 2020)
5

>>> calendar.leapdays(2000, 2021)
6

>>> calendar.leapdays(2020, 2000)
-5

>>> calendar.leapdays(2019, 2020)
0

>>> calendar.leapdays(2020, 2020)
0

>>> calendar.leapdays(2020, 2021)
1
```


### 指定日期为周几

```calendar.weekday(year, month, day)```可以获取指定日期是周几：

```py
# 2020年5月23日是周六
>>> calendar.weekday(2020, 5, 23)
5

# 2020年5月22日是周五
>>> calendar.weekday(2020, 5, 22)
4

>>> calendar.weekday(2020, 5, 21)
3

>>> calendar.weekday(2020, 5, 20)
2

>>> calendar.weekday(2020, 5, 19)
1

>>> calendar.weekday(2020, 5, 18)
0

>>> calendar.weekday(2020, 5, 17)
6

>>> calendar.weekday(1900, 5, 17)
3

# 年份不能是负数或0
>>> calendar.weekday(-1900, 5, 17)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-48-9594fb810542> in <module>
----> 1 calendar.weekday(-1900, 5, 17)

d:\programfiles\python368\lib\calendar.py in weekday(year, month, day)
    114     """Return weekday (0-6 ~ Mon-Sun) for year (1970-...), month (1-12),
    115        day (1-31)."""
--> 116     return datetime.date(year, month, day).weekday()
    117
    118

ValueError: year -1900 is out of range

>>> calendar.weekday(0, 5, 23)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-59-43ee5afa490e> in <module>
----> 1 calendar.weekday(0, 5, 23)

d:\programfiles\python368\lib\calendar.py in weekday(year, month, day)
    114     """Return weekday (0-6 ~ Mon-Sun) for year (1970-...), month (1-12),
    115        day (1-31)."""
--> 116     return datetime.date(year, month, day).weekday()
    117
    118

ValueError: year 0 is out of range
```


### 返回包含英文星期缩写的字符

`calendar.weekheader(n)`可以返回包含英文星期缩写的字符，`n`指定周一至周日英文字符的宽度：
```py
# 因为上面我们设置了每周第一天为周日，所以开始显示是Sun周日
>>> calendar.weekheader(3)
'Sun Mon Tue Wed Thu Fri Sat'

>>> calendar.weekheader(4)
'Sun  Mon  Tue  Wed  Thu  Fri  Sat '

>>> calendar.weekheader(5)
' Sun   Mon   Tue   Wed   Thu   Fri   Sat '

>>> calendar.weekheader(2)
'Su Mo Tu We Th Fr Sa'

>>> calendar.weekheader(1)
'S M T W T F S'

# 重新设置每周第一天为周一
>>> calendar.setfirstweekday(calendar.MONDAY)

# 此时可以看到Mon周一显示在前面
>>> calendar.weekheader(3)
'Mon Tue Wed Thu Fri Sat Sun'

>>> calendar.weekheader(4)
'Mon  Tue  Wed  Thu  Fri  Sat  Sun '

>>> calendar.weekheader(5)
' Mon   Tue   Wed   Thu   Fri   Sat   Sun '

>>> calendar.weekheader(2)
'Mo Tu We Th Fr Sa Su'

>>> calendar.weekheader(1)
'M T W T F S S'
```

### 月份的第一天是周几，月份有多少天

`calendar.monthrange(year, month)`可以返回指定月份的第一天是周几，以及该月的天数。

```py
>>> calendar.monthrange?
Signature: calendar.monthrange(year, month)
Docstring:
Return weekday (0-6 ~ Mon-Sun) and number of days (28-31) for
year, month.
File:      d:\programfiles\python368\lib\calendar.py
Type:      function

# 2020年5月第一天是周五，该月共31天
>>> calendar.monthrange(2020, 5)
(4, 31)

# 2020年4月第一天是周三，该月共30天
>>> calendar.monthrange(2020, 4)
(2, 30)

>>> calendar.monthrange(2020, 3)
(6, 31)

>>> calendar.monthrange(2020, 2)
(5, 29)

>>> calendar.monthrange(2020, 1)
(2, 31)
```

### 指定月份的日历列表

`calendar.monthcalendar(year, month)`可以返回指定月份的列表，每行代表一个星期，该月份以外的日期以0替代，默认以周一作为每周的第一天：

```py
>>> calendar.monthcalendar(2020, 5)
[[0, 0, 0, 0, 1, 2, 3],
 [4, 5, 6, 7, 8, 9, 10],
 [11, 12, 13, 14, 15, 16, 17],
 [18, 19, 20, 21, 22, 23, 24],
 [25, 26, 27, 28, 29, 30, 31]]

>>> calendar.monthcalendar(2020, 4)
[[0, 0, 1, 2, 3, 4, 5],
 [6, 7, 8, 9, 10, 11, 12],
 [13, 14, 15, 16, 17, 18, 19],
 [20, 21, 22, 23, 24, 25, 26],
 [27, 28, 29, 30, 0, 0, 0]]

>>> calendar.monthcalendar(2020, 3)
[[0, 0, 0, 0, 0, 0, 1],
 [2, 3, 4, 5, 6, 7, 8],
 [9, 10, 11, 12, 13, 14, 15],
 [16, 17, 18, 19, 20, 21, 22],
 [23, 24, 25, 26, 27, 28, 29],
 [30, 31, 0, 0, 0, 0, 0]]

>>> calendar.monthcalendar(2020, 2)
[[0, 0, 0, 0, 0, 1, 2],
 [3, 4, 5, 6, 7, 8, 9],
 [10, 11, 12, 13, 14, 15, 16],
 [17, 18, 19, 20, 21, 22, 23],
 [24, 25, 26, 27, 28, 29, 0]]

>>> calendar.monthcalendar(2020, 1)
[[0, 0, 1, 2, 3, 4, 5],
 [6, 7, 8, 9, 10, 11, 12],
 [13, 14, 15, 16, 17, 18, 19],
 [20, 21, 22, 23, 24, 25, 26],
 [27, 28, 29, 30, 31, 0, 0]]
```


### 打印指定月份的日历

`calendar.prmonth(theyear, themonth, w=0, l=0)`可以打印指定月份的日历，`w`指定星期字符的宽度，默认为0，内部限制至少为2; `l`指定两周之间换几行，默认值为0，内部限制至少换1行，实验可以发现`l`参数保持默认比较好，看起来比较紧凑：

```py
>>> calendar.prmonth?
Signature: calendar.prmonth(theyear, themonth, w=0, l=0)
Docstring: Print a month's calendar.
File:      d:\programfiles\python368\lib\calendar.py
Type:      method

# 默认星期字符宽度为2
>>> calendar.prmonth(2020, 5)
      May 2020
Mo Tu We Th Fr Sa Su
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31

>>> calendar.prmonth(2020, 4)
     April 2020
Mo Tu We Th Fr Sa Su
       1  2  3  4  5
 6  7  8  9 10 11 12
13 14 15 16 17 18 19
20 21 22 23 24 25 26
27 28 29 30

>>> calendar.prmonth(2020, 3)
     March 2020
Mo Tu We Th Fr Sa Su
                   1
 2  3  4  5  6  7  8
 9 10 11 12 13 14 15
16 17 18 19 20 21 22
23 24 25 26 27 28 29
30 31

# 设置星期字符宽度为3
>>> calendar.prmonth(2020, 5, w=3)
          May 2020
Mon Tue Wed Thu Fri Sat Sun
                  1   2   3
  4   5   6   7   8   9  10
 11  12  13  14  15  16  17
 18  19  20  21  22  23  24
 25  26  27  28  29  30  31

# 设置星期字符宽度为4
>>> calendar.prmonth(2020, 5, w=4)
             May 2020
Mon  Tue  Wed  Thu  Fri  Sat  Sun
                      1    2    3
  4    5    6    7    8    9   10
 11   12   13   14   15   16   17
 18   19   20   21   22   23   24
 25   26   27   28   29   30   31

# 设置星期字符宽度为2
>>> calendar.prmonth(2020, 5, w=2)
      May 2020
Mo Tu We Th Fr Sa Su
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31

# 设置星期字符宽度为1时，不起作用，还是保持为宽度为2
>>> calendar.prmonth(2020, 5, w=1)
      May 2020
Mo Tu We Th Fr Sa Su
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31

# 设置两周之间换1行
>>> calendar.prmonth(2020, 5, l=1)
      May 2020
Mo Tu We Th Fr Sa Su
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31

# 设置两周之间换2行
>>> calendar.prmonth(2020, 5, l=2)
      May 2020

Mo Tu We Th Fr Sa Su

             1  2  3

 4  5  6  7  8  9 10

11 12 13 14 15 16 17

18 19 20 21 22 23 24

25 26 27 28 29 30 31

# 设置两周之间换3行
>>> calendar.prmonth(2020, 5, l=3)
      May 2020


Mo Tu We Th Fr Sa Su


             1  2  3


 4  5  6  7  8  9 10


11 12 13 14 15 16 17


18 19 20 21 22 23 24


25 26 27 28 29 30 31



>>>
```

### 返回指定月份的多行文本字符串

`calendar.month(theyear, themonth, w=0, l=0)`可以返回指定月份的多行文本字符串，与`calendar.prmonth(theyear, themonth, w=0, l=0)`设置类似，可以理解为`calendar.prmonth`将`calendar.month`的返回值打印出来了：

```py
>>> calendar.month(2020, 5)
'      May 2020\nMo Tu We Th Fr Sa Su\n             1  2  3\n 4  5  6  7  8  9 10\n11 12 13 14 15 16 17\n18 19 20 21 22
23 24\n25 26 27 28 29 30 31\n'

>>> calendar.month(2020, 5, w=3)
'          May 2020\nMon Tue Wed Thu Fri Sat Sun\n                  1   2   3\n  4   5   6   7   8   9  10\n 11  12  13
 14  15  16  17\n 18  19  20  21  22  23  24\n 25  26  27  28  29  30  31\n'

>>> calendar.month(2020, 5, l=2)
'      May 2020\n\nMo Tu We Th Fr Sa Su\n\n             1  2  3\n\n 4  5  6  7  8  9 10\n\n11 12 13 14 15 16 17\n\n18 19
 20 21 22 23 24\n\n25 26 27 28 29 30 31\n\n'

>>> print(calendar.month(2020, 5, l=2))
      May 2020

Mo Tu We Th Fr Sa Su

             1  2  3

 4  5  6  7  8  9 10

11 12 13 14 15 16 17

18 19 20 21 22 23 24

25 26 27 28 29 30 31



>>>
```

### 打印指定年份的日历

`calendar.prcal(year, w=0, l=0, c=6, m=3)`打印指定年份的日历，`w`指定星期宽度，`l`指定换行，与上面的`prmonth`配置相同，`c`指定两列月份之间的空隔距离，`m`指定日历中显示几列月份

```py
>>> calendar.prcal?
Signature: calendar.prcal(theyear, w=0, l=0, c=6, m=3)
Docstring: Print a year's calendar.
File:      d:\programfiles\python368\lib\calendar.py
Type:      method

# 默认显示三列月份，两个月份之间空6格
>>> calendar.prcal(2020)
                                  2020

      January                   February                   March
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
       1  2  3  4  5                      1  2                         1
 6  7  8  9 10 11 12       3  4  5  6  7  8  9       2  3  4  5  6  7  8
13 14 15 16 17 18 19      10 11 12 13 14 15 16       9 10 11 12 13 14 15
20 21 22 23 24 25 26      17 18 19 20 21 22 23      16 17 18 19 20 21 22
27 28 29 30 31            24 25 26 27 28 29         23 24 25 26 27 28 29
                                                    30 31

       April                      May                       June
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
       1  2  3  4  5                   1  2  3       1  2  3  4  5  6  7
 6  7  8  9 10 11 12       4  5  6  7  8  9 10       8  9 10 11 12 13 14
13 14 15 16 17 18 19      11 12 13 14 15 16 17      15 16 17 18 19 20 21
20 21 22 23 24 25 26      18 19 20 21 22 23 24      22 23 24 25 26 27 28
27 28 29 30               25 26 27 28 29 30 31      29 30

        July                     August                  September
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
       1  2  3  4  5                      1  2          1  2  3  4  5  6
 6  7  8  9 10 11 12       3  4  5  6  7  8  9       7  8  9 10 11 12 13
13 14 15 16 17 18 19      10 11 12 13 14 15 16      14 15 16 17 18 19 20
20 21 22 23 24 25 26      17 18 19 20 21 22 23      21 22 23 24 25 26 27
27 28 29 30 31            24 25 26 27 28 29 30      28 29 30
                          31

      October                   November                  December
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
          1  2  3  4                         1          1  2  3  4  5  6
 5  6  7  8  9 10 11       2  3  4  5  6  7  8       7  8  9 10 11 12 13
12 13 14 15 16 17 18       9 10 11 12 13 14 15      14 15 16 17 18 19 20
19 20 21 22 23 24 25      16 17 18 19 20 21 22      21 22 23 24 25 26 27
26 27 28 29 30 31         23 24 25 26 27 28 29      28 29 30 31
                          30

# 设置月份之间空3格，按4列显示月份
>>> calendar.prcal(2020, c=3, m=4)
                                           2020

      January                February                March                  April
Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su
       1  2  3  4  5                   1  2                      1          1  2  3  4  5
 6  7  8  9 10 11 12    3  4  5  6  7  8  9    2  3  4  5  6  7  8    6  7  8  9 10 11 12
13 14 15 16 17 18 19   10 11 12 13 14 15 16    9 10 11 12 13 14 15   13 14 15 16 17 18 19
20 21 22 23 24 25 26   17 18 19 20 21 22 23   16 17 18 19 20 21 22   20 21 22 23 24 25 26
27 28 29 30 31         24 25 26 27 28 29      23 24 25 26 27 28 29   27 28 29 30
                                              30 31

        May                    June                   July                  August
Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su
             1  2  3    1  2  3  4  5  6  7          1  2  3  4  5                   1  2
 4  5  6  7  8  9 10    8  9 10 11 12 13 14    6  7  8  9 10 11 12    3  4  5  6  7  8  9
11 12 13 14 15 16 17   15 16 17 18 19 20 21   13 14 15 16 17 18 19   10 11 12 13 14 15 16
18 19 20 21 22 23 24   22 23 24 25 26 27 28   20 21 22 23 24 25 26   17 18 19 20 21 22 23
25 26 27 28 29 30 31   29 30                  27 28 29 30 31         24 25 26 27 28 29 30
                                                                     31

     September               October                November               December
Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su
    1  2  3  4  5  6             1  2  3  4                      1       1  2  3  4  5  6
 7  8  9 10 11 12 13    5  6  7  8  9 10 11    2  3  4  5  6  7  8    7  8  9 10 11 12 13
14 15 16 17 18 19 20   12 13 14 15 16 17 18    9 10 11 12 13 14 15   14 15 16 17 18 19 20
21 22 23 24 25 26 27   19 20 21 22 23 24 25   16 17 18 19 20 21 22   21 22 23 24 25 26 27
28 29 30               26 27 28 29 30 31      23 24 25 26 27 28 29   28 29 30 31
                                              30


>>>
```

### 返回年份日历的多行文本字符串

`calendar.calendar(year, w=2, l=1, c=6, m=3)`可以返回年份日历的多行文本字符串，参数与`calendar.prcal(year, w=0, l=0, c=6, m=3)`相同。

```py
>>> calendar.calendar(2020)
'                                  2020\n\n      January                   February                   March\nMo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su\n       1  2  3  4  5
              1  2                         1\n 6  7  8  9 10 11 12       3  4  5  6  7  8  9       2  3  4  5  6  7  8\n13 14 15 16 17 18 19      10 11 12 13 14 15 16       9 10 11 12 13 14 15\n20 21 22 23 24 25 26      17 18 19 20 21 22 23      16 17 18 19 20 21 22\n27 28 29 30 31            24 25 26 27 28 29         23 24 25 26 27 28 29\n                                                    30 31\n\n       April
               May                       June\nMo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su\n       1  2  3  4  5                   1  2  3       1  2  3  4  5  6  7\n 6  7  8  9 10 11 12       4  5  6  7  8  9 10       8  9 10 11 12 13 14\n13 14 15 16 17 18 19      11 12 13 14 15 16 17      15 16 17 18 19 20 21\n20 21 22 23 24 25 26      18 19 20 21 22 23 24      22 23 24 25 26 27 28\n27 28 29 30               25 26 27 28 29 30 31      29 30\n\n        July                     August                  September\nMo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su\n       1  2
3  4  5                      1  2          1  2  3  4  5  6\n 6  7  8  9 10 11 12       3  4  5  6  7  8  9       7  8  9 10 11 12 13\n13 14 15 16 17 18 19      10 11 12 13 14 15 16      14 15 16 17 18 19 20\n20 21 22 23 24 25 26      17 18 19 20 21 22 23      21 22 23 24 25 26 27\n27 28 29 30 31            24 25 26 27 28 29 30      28 29 30\n                          31\n\n      October                   November
             December\nMo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su\n          1  2  3  4                         1          1  2  3  4  5  6\n 5  6  7  8  9 10 11       2  3  4  5  6
  7  8       7  8  9 10 11 12 13\n12 13 14 15 16 17 18       9 10 11 12 13 14 15      14 15 16 17 18 19 20\n19 20 21 22 23 24 25      16 17 18 19 20 21 22      21 22 23 24 25 26 27\n26 27 28 29 30 31         23 24 25 26 27 28 29      28 29 30 31\n                          30\n'
```


### 获取时间戳值

`calendar.timegm(tuple)`是一个不相关但很方便的函数，`tuple`参数可以是由`time.gmtime()`函数返回的时间元组，返回相应的Unix时间戳值。实际上，`time.gmtime()`和`calendar.timegm()`功能正好相反。

```py
>>> calendar.timegm?
Signature: calendar.timegm(tuple)
Docstring: Unrelated but handy function to calculate Unix timestamp from GMT.
File:      d:\programfiles\python368\lib\calendar.py
Type:      function

>>> calendar.timegm((2020 ,2, 3, 12, 12, 20))
1580731940

>>> import time

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
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=23, tm_hour=9, tm_min=16, tm_sec=24, tm_wday=5, tm_yday=144, tm_isdst=0)

>>> calendar.timegm(time.gmtime())
1590225405

>>> calendar.timegm(time.gmtime())
1590225416

>>> type(time.gmtime())
time.struct_time

>>> time.gmtime(calendar.timegm(time.gmtime()))
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=23, tm_hour=9, tm_min=18, tm_sec=3, tm_wday=5, tm_yday=144, tm_isdst=0)

>>> time.gmtime(calendar.timegm(time.gmtime()))
time.struct_time(tm_year=2020, tm_mon=5, tm_mday=23, tm_hour=9, tm_min=18, tm_sec=29, tm_wday=5, tm_yday=144, tm_isdst=0)
```

### `calendar`日历模块的数据属性

- `calendar.day_name`: 当前语言环境下星期(每周的第一天到最后一天)组成的数组。
- `calendar.day_abbr`: 当前语言环境下星期(每周的第一天到最后一天)缩写组成的数组。
- `calendar.month_name`: 当前语言环境下一年中月份组成的数组，长度为13，第一个元素为空，是为了让`January`作为`1`号元素，与实际约定保持一致。
- `calendar.month_abbr`: 当前语言环境下一年中月份缩写组成的数组，长度为13，第一个元素为空，是为了让`January`作为`1`号元素，与实际约定保持一致。

```py
>>> calendar.day_name?
Type:        _localized_day
String form: <calendar._localized_day object at 0x000002C809329710>
Length:      7
File:        d:\programfiles\python368\lib\calendar.py
Docstring:   <no docstring>

>>> calendar.day_name
<calendar._localized_day at 0x2c809329710>

>>> calendar.day_abbr
<calendar._localized_day at 0x2c809329748>

>>> print(calendar.day_abbr)
<calendar._localized_day object at 0x000002C809329748>

>>> print(calendar.month_name)
<calendar._localized_month object at 0x000002C809329780>

>>> print(calendar.month_name[0])


>>> calendar.month_name[0]
''

>>> calendar.month_name[1]
'January'

>>> calendar.month_name[2]
'February'

>>> calendar.month_name[3]
'March'

>>> calendar.month_name[4]
'April'

>>> [i for i in calendar.day_name]
['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

>>> [i for i in calendar.day_abbr]
['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

>>> [i for i in calendar.month_name]
['',
 'January',
 'February',
 'March',
 'April',
 'May',
 'June',
 'July',
 'August',
 'September',
 'October',
 'November',
 'December']

>>> [i for i in calendar.month_abbr]
['',
 'Jan',
 'Feb',
 'Mar',
 'Apr',
 'May',
 'Jun',
 'Jul',
 'Aug',
 'Sep',
 'Oct',
 'Nov',
 'Dec']
```

### 设置locale本地化后获取日历模块数据属性

```py
>>> import locale

>>> locale?
Type:        module
String form: <module 'locale' from 'd:\\programfiles\\python368\\lib\\locale.py'>
File:        d:\programfiles\python368\lib\locale.py
Docstring:
Locale support module.

The module provides low-level access to the C lib's locale APIs and adds high
level number formatting APIs as well as a locale aliasing engine to complement
these.

The aliasing engine includes support for many commonly used locale names and
maps them to values suitable for passing to the C lib's setlocale() function. It
also includes default encodings for all supported locale names.

>>> locale.getlocale()
(None, None)

# 获取当前默认环境，当设置locale使用默认值时，此值会被采用为默认值。
>>> locale.getdefaultlocale()
('zh_CN', 'cp65001')

>>> locale.LC_ALL
0

>>> locale.getlocale()
(None, None)

# 设置为中文环境
>>> locale.setlocale(locale.LC_ALL, '')
'Chinese (Simplified)_China.utf8'

>>> locale.getlocale()
('Chinese (Simplified)_China', 'utf8')

>>> [i for i in calendar.day_name]
['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

>>> [i for i in calendar.day_abbr]
['周一', '周二', '周三', '周四', '周五', '周六', '周日']

>>> [i for i in calendar.month_name]
['', '一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']

>>> [i for i in calendar.month_abbr]
['', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

# 重新设置为英文环境
>>> locale.setlocale(locale.LC_ALL, 'C')
'C'

>>> locale.getlocale()
(None, None)

>>> [i for i in calendar.month_abbr]
['',
 'Jan',
 'Feb',
 'Mar',
 'Apr',
 'May',
 'Jun',
 'Jul',
 'Aug',
 'Sep',
 'Oct',
 'Nov',
 'Dec']

>>> [i for i in calendar.day_name]
['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

>>> [i for i in calendar.day_abbr]
['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

>>> [i for i in calendar.month_name]
['',
 'January',
 'February',
 'March',
 'April',
 'May',
 'June',
 'July',
 'August',
 'September',
 'October',
 'November',
 'December']

>>> [i for i in calendar.month_abbr]
['',
 'Jan',
 'Feb',
 'Mar',
 'Apr',
 'May',
 'Jun',
 'Jul',
 'Aug',
 'Sep',
 'Oct',
 'Nov',
 'Dec']

>>>
```
可以发现获取日历模块的数据属性时，根据当前语言环境不同，获取的结果是不一样的，相应的使用`calendar`模块其他函数或方法获取到的结果也可能会受语言环境影响，请注意此问题。

`calendar`模块中还定义了`calendar.Calendar`类，`calendar.TextCalendar`类，`calendar.HTMLCalendar`类，`calendar.LocaleTextCalendar`类以及`calendar.LocaleHTMLCalendar`类，此处不展开。详细可参考[https://docs.python.org/3.6/library/calendar.html](https://docs.python.org/3.6/library/calendar.html)

