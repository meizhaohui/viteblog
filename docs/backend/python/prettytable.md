# 表格美化输出模块prettytable

[[toc]]

本文约32000字。简单使用的话，仅阅读到3.3节 添加字段名和数据 即可。

## 1. 概述

- PrettyTable模块可以用来输出表格，就像excel、mysql查询出来的结果一样，方便查看数据的详情。
- 参考文档：[https://pypi.org/project/prettytable/](https://pypi.org/project/prettytable/)

## 2. 安装

```sh
$ pip install prettytable
Defaulting to user installation because normal site-packages is not writeable
Looking in indexes: https://mirrors.aliyun.com/pypi/simple/
Collecting prettytable
  Downloading https://mirrors.aliyun.com/pypi/packages/7a/cd/bec5850e23eb005c6fe30fe4c26bafd9a07b3d2524771f22a0fa01270078/prettytable-3.7.0-py3-none-any.whl (27 kB)
Collecting wcwidth
  Downloading https://mirrors.aliyun.com/pypi/packages/20/f4/c0584a25144ce20bfcf1aecd041768b8c762c1eb0aa77502a3f0baa83f11/wcwidth-0.2.6-py2.py3-none-any.whl (29 kB)
Installing collected packages: wcwidth, prettytable
Successfully installed prettytable-3.7.0 wcwidth-0.2.6
$ pip list|grep prettytable
prettytable      3.7.0
$
```

## 3. 基本使用

### 3.1 创建表格

```py
$ python
Python 3.9.6 (default, Mar 10 2023, 20:16:38)
[Clang 14.0.3 (clang-1403.0.22.14.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from prettytable import PrettyTable
>>> x = PrettyTable()
>>> x
++
||
++
++
>>>
```

### 3.2 设置表格标题

```py
>>> x.title = 'Table 1  City Info'
```

此时不能直接输出x，输出的话会抛出异常
```py
>>> x
Traceback (most recent call last):
  ...line 1600, in _compute_widths
    widths[-1] += min_width - sum(widths)
IndexError: list index out of range
>>>
```

### 3.3 添加字段名和数据

```py
>>> x.title = 'Table 1  City Info'
>>> x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
>>> x.add_row(["Adelaide", 1295, 1158259, 600.5])
>>> x.add_row(["Brisbane", 5905, 1857594, 1146.4])
>>> x.add_row(["Darwin", 112, 120900, 1714.7])
>>> x.add_row(["Hobart", 1357, 205556, 619.5])
>>> x.add_row(["Sydney", 2058, 4336374, 1214.8])
>>> x.add_row(["Melbourne", 1566, 3806092, 646.9])
>>> x.add_row(["Perth", 5386, 1554769, 869.4])
>>> print(x)
+-------------------------------------------------+
|                Table 1  City Info               |
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
|  Adelaide | 1295 |  1158259   |      600.5      |
|  Brisbane | 5905 |  1857594   |      1146.4     |
|   Darwin  | 112  |   120900   |      1714.7     |
|   Hobart  | 1357 |   205556   |      619.5      |
|   Sydney  | 2058 |  4336374   |      1214.8     |
| Melbourne | 1566 |  3806092   |      646.9      |
|   Perth   | 5386 |  1554769   |      869.4      |
+-----------+------+------------+-----------------+
>>>
```

此时打印`x`时，可以看到输出了一个表格，像从数据库查询的输出结果一样！！


### 3.4 一次添加多行数据

也可以使用`add_rows`一次性添加多行数据到表格中，示例如下：

```py
from prettytable import PrettyTable

x = PrettyTable()
x.title = 'Table 2 City Info'
x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
x.add_rows(
    [
        ["Adelaide", 1295, 1158259, 600.5],
        ["Brisbane", 5905, 1857594, 1146.4],
        ["Darwin", 112, 120900, 1714.7],
        ["Hobart", 1357, 205556, 619.5],
        ["Sydney", 2058, 4336374, 1214.8],
        ["Melbourne", 1566, 3806092, 646.9],
        ["Perth", 5386, 1554769, 869.4],
    ]
)

print(x)
```

运行后，结果如下：

```py
+-------------------------------------------------+
|                Table 2 City Info                |
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
|  Adelaide | 1295 |  1158259   |      600.5      |
|  Brisbane | 5905 |  1857594   |      1146.4     |
|   Darwin  | 112  |   120900   |      1714.7     |
|   Hobart  | 1357 |   205556   |      619.5      |
|   Sydney  | 2058 |  4336374   |      1214.8     |
| Melbourne | 1566 |  3806092   |      646.9      |
|   Perth   | 5386 |  1554769   |      869.4      |
+-----------+------+------------+-----------------+
```

### 3.5 按列添加数据

我们也可以按列的方式一列列的添加数据，此使用使用`add_column`方法，该方法第一个参数是字段名，第二参数是列数据组成的数组或元组。

```py
from prettytable import PrettyTable

x = PrettyTable()
x.title = 'Table 3 City Info'
x.add_column("City name",
["Adelaide","Brisbane","Darwin","Hobart","Sydney","Melbourne","Perth"])
x.add_column("Area", [1295, 5905, 112, 1357, 2058, 1566, 5386])

print(x)
```

运行结果如下：
```py
+-------------------+
| Table 3 City Info |
+-----------+-------+
| City name |  Area |
+-----------+-------+
|  Adelaide |  1295 |
|  Brisbane |  5905 |
|   Darwin  |  112  |
|   Hobart  |  1357 |
|   Sydney  |  2058 |
| Melbourne |  1566 |
|   Perth   |  5386 |
+-----------+-------+
```

可以看到，的确添加了两列数据。

- 注意，只能用`add_column`方法一次添加一列，不能使用`add_columns`一次添加多列，没有该方法。
- 不要混合使用`add_column`和`add_row`,这样有时会让人感觉困惑，更推荐使用`add_row`或`add_rows`一次添加一行或多行数据。

### 3.6 从csv文件读取数据

如我们创建一个`data.csv`文件 [download data.csv](/scripts/python/data.csv) ：
![](/img/Snipaste_2023-04-30_11-34-13.png)

我们也可以使用prettytable读取csv文件中的数据：

```py
from prettytable import from_csv

with open("data.csv") as fp:
    mytable = from_csv(fp)
    mytable.title = '表 4 天气详情'
    print(mytable)

```

运行后，输出如下：
```py
|                   表 4 天气详情                   |
+------+----------+-----------+----------+----------+
| 序号 |   城市   |    日期   | 最低气温 | 最高气温 |
+------+----------+-----------+----------+----------+
|  1   |   北京   | 2023/4/30 |    11    |    25    |
|  2   |   上海   | 2023/4/30 |    15    |    24    |
|  3   |   深圳   | 2023/4/30 |    20    |    26    |
|  4   |  哈尔滨  | 2023/4/30 |    1     |    9     |
|  5   | 呼和浩特 | 2023/4/30 |    7     |    21    |
+------+----------+-----------+----------+----------+
```

输出效果如下图所示：

![](/img/Snipaste_2023-04-30_11-38-37.png)

可以看到，可以正常从csv文件中读取到数据，并输出了表格。唯一美中不足的是，表格中存在中文，文本没有完全对齐。

在Iterm2中控制台输出显示是正常的：
![](/img/Snipaste_2023-04-30_16-37-20.png)

在VSCODE中输出也是正常的！！
![](/img/Snipaste_2023-04-30_16-32-31.png)

详细可参考 [Better display of Chinese #49](https://github.com/jazzband/prettytable/issues/49)

### 3.7 从数据库导入数据

#### 3.7.1 准备数据库数据
我们参考 [https://www.runoob.com/sqlite/sqlite-insert.html](https://www.runoob.com/sqlite/sqlite-insert.html) 创建一个sqlite的表格。

创建db文件：

```sh
$ touch sqlite.db
```

打开db文件:

```sh
$ sqlite3 sqlite.db
```

创建表格：

```sql
sqlite> CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);
```

向表格中插入数据：

```sql
INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (1, 'Paul', 32, 'California', 20000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (2, 'Allen', 25, 'Texas', 15000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (3, 'Teddy', 23, 'Norway', 20000.00 );

```

操作后，检查输出：

![](/img/Snipaste_2023-04-30_12-00-09.png)

#### 3.7.2 导入数据

请看以下示例：

```py
import sqlite3
from prettytable import from_db_cursor

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM COMPANY")
mytable = from_db_cursor(cursor)
mytable.title = 'table 5 database info'
print(mytable)

```

输出结果：

```py
+-----------------------------------------+
|          table 5 database info          |
+----+-------+-----+------------+---------+
| ID |  NAME | AGE |  ADDRESS   |  SALARY |
+----+-------+-----+------------+---------+
| 1  |  Paul |  32 | California | 20000.0 |
| 2  | Allen |  25 |   Texas    | 15000.0 |
| 3  | Teddy |  23 |   Norway   | 20000.0 |
+----+-------+-----+------------+---------+

```


### 3.8 删除数据

- `del_row`：删除某行，允许传入一个整数参数，（从0开始）。
- `del_column`：删除某列，允许传入一个字符串，表示要删除的列的字段名。
- `clear_rows`：删除所有数据，但保留列的字段名。
- `clear`：删除所有数据，包括列的字段名。

我们以3.7节从数据库中读出的数据为例，来删除表格中的数据：

#### 3.8.1 `del_row`删除某行

删除第2行：
```py
import sqlite3
from prettytable import from_db_cursor

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM COMPANY")
mytable = from_db_cursor(cursor)
mytable.title = 'table 5 database info'
print('原始表格输出：')
print(mytable)

print('\n删除某行后的输出：')
mytable.del_row(1)
print(mytable)
```

运行后输出如下：
```sh
原始表格输出：
+-----------------------------------------+
|          table 5 database info          |
+----+-------+-----+------------+---------+
| ID |  NAME | AGE |  ADDRESS   |  SALARY |
+----+-------+-----+------------+---------+
| 1  |  Paul |  32 | California | 20000.0 |
| 2  | Allen |  25 |   Texas    | 15000.0 |
| 3  | Teddy |  23 |   Norway   | 20000.0 |
+----+-------+-----+------------+---------+

删除某行后的输出：
+-----------------------------------------+
|          table 5 database info          |
+----+-------+-----+------------+---------+
| ID |  NAME | AGE |  ADDRESS   |  SALARY |
+----+-------+-----+------------+---------+
| 1  |  Paul |  32 | California | 20000.0 |
| 3  | Teddy |  23 |   Norway   | 20000.0 |
+----+-------+-----+------------+---------+
```

可以看到，ID为2的行（也就是第2行数据）被正常删除了。


#### 3.8.2 `del_column`删除某列

删除`ADDRESS`列：

```py
import sqlite3
from prettytable import from_db_cursor

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM COMPANY")
mytable = from_db_cursor(cursor)
mytable.title = 'table 5 database info'
print('原始表格输出：')
print(mytable)

print('\n删除某列后的输出：')
mytable.del_column('ADDRESS')
print(mytable)
```

运行后，输出如下：

```py
原始表格输出：
+-----------------------------------------+
|          table 5 database info          |
+----+-------+-----+------------+---------+
| ID |  NAME | AGE |  ADDRESS   |  SALARY |
+----+-------+-----+------------+---------+
| 1  |  Paul |  32 | California | 20000.0 |
| 2  | Allen |  25 |   Texas    | 15000.0 |
| 3  | Teddy |  23 |   Norway   | 20000.0 |
+----+-------+-----+------------+---------+

删除某列后的输出：
+----------------------------+
|   table 5 database info    |
+----+-------+-----+---------+
| ID |  NAME | AGE |  SALARY |
+----+-------+-----+---------+
| 1  |  Paul |  32 | 20000.0 |
| 2  | Allen |  25 | 15000.0 |
| 3  | Teddy |  23 | 20000.0 |
+----+-------+-----+---------+
```

可以看到`ADDRESS`列被删除了。

#### 3.8.3 `clear_rows`删除所有数据行

删除所有数据行，但保留字段名：

```py
import sqlite3
from prettytable import from_db_cursor

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM COMPANY")
mytable = from_db_cursor(cursor)
mytable.title = 'table 5 database info'
print('原始表格输出：')
print(mytable)

print('\n清理所有行，但保留字段名后的输出：')
mytable.clear_rows()
print(mytable)
```

运行后，输出如下：

```py
原始表格输出：
+-----------------------------------------+
|          table 5 database info          |
+----+-------+-----+------------+---------+
| ID |  NAME | AGE |  ADDRESS   |  SALARY |
+----+-------+-----+------------+---------+
| 1  |  Paul |  32 | California | 20000.0 |
| 2  | Allen |  25 |   Texas    | 15000.0 |
| 3  | Teddy |  23 |   Norway   | 20000.0 |
+----+-------+-----+------------+---------+

清理所有行，但保留字段名后的输出：
+------------------------------------+
|       table 5 database info        |
+----+------+-----+---------+--------+
| ID | NAME | AGE | ADDRESS | SALARY |
+----+------+-----+---------+--------+
+----+------+-----+---------+--------+
```
可以看到，此时数据行的内容被清空了，仅保留了字段名行。

#### 3.8.4 `clear`删除所有行

```py
import sqlite3
from prettytable import from_db_cursor

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM COMPANY")
mytable = from_db_cursor(cursor)
mytable.title = 'table 5 database info'
print('原始表格输出：')
print(mytable)

print('\n清理所有行，以及字段名后的输出：')
mytable.clear()
```

注意，执行`clear`清理后，不能再打印mytable了，打印的话，会抛出异常`IndexError: list index out of range`。

### 3.9 多语言测试

以下在表格中插入日本地名的中文名称、平假名、英文等。

```py
from prettytable import PrettyTable

x = PrettyTable()
x.title = '表6 多语言测试'
x.field_names = ["序号", "中文名", "平假名", "英文"]
x.add_rows(
    [
        [1, "东京", "とぅきよぅ", "Tokyo"],
        [2, "北海道", "ほっかいどう", "Hokkaido"],
        [3, "横滨", "よこはま", "Yokohama"],
        [4, "名古屋", "なごやし", "Nagoya"],
    ]
)

print(x)
```

运行，输出结果如下：

![](/img/Snipaste_2023-04-30_17-20-40.png)

可以看到，正常输出表格，说明支持中文、日文、英文的表格输出。

### 3.10 设置分界线

- 您可以使用`divider`参数将表划分为不同的部分。这将在设置了此字段的行下的表中添加一条分界线。

#### 3.10.1 每行单独设置分隔线

我们来设置一下，看一下效果。

```py
from prettytable import PrettyTable

x = PrettyTable()
x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
x.add_row(["Adelaide", 1295, 1158259, 600.5])
x.add_row(["Brisbane", 5905, 1857594, 1146.4])
x.add_row(["Darwin", 112, 120900, 1714.7])
x.add_row(["Hobart", 1357, 205556, 619.5], divider=True)
x.add_row(["Melbourne", 1566, 3806092, 646.9])
x.add_row(["Perth", 5386, 1554769, 869.4])
x.add_row(["Sydney", 2058, 4336374, 1214.8])
print(x)
```

运行后，查看输出效果：

![](/img/Snipaste_2023-04-30_18-54-58.png)
可以看到在`City name`为`Hobart`的下一行，多出了一个分割线，将表格分成了上下两部分，就像Excel表格里面的单元格的框线一样。

如果我想每行数据后面都有分隔线，则可以像下面这样做：

在每行数据中都加上`divider=True`参数：

```py
from prettytable import PrettyTable

x = PrettyTable()
x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
x.add_row(["Adelaide", 1295, 1158259, 600.5], divider=True)
x.add_row(["Brisbane", 5905, 1857594, 1146.4], divider=True)
x.add_row(["Darwin", 112, 120900, 1714.7], divider=True)
x.add_row(["Hobart", 1357, 205556, 619.5], divider=True)
x.add_row(["Melbourne", 1566, 3806092, 646.9], divider=True)
x.add_row(["Perth", 5386, 1554769, 869.4], divider=True)
x.add_row(["Sydney", 2058, 4336374, 1214.8], divider=True)
print(x)
```

运行后，输出如下：
```sh
$ python "use_prettytable.py"                                                                                            <<<
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
|  Adelaide | 1295 |  1158259   |      600.5      |
+-----------+------+------------+-----------------+
|  Brisbane | 5905 |  1857594   |      1146.4     |
+-----------+------+------------+-----------------+
|   Darwin  | 112  |   120900   |      1714.7     |
+-----------+------+------------+-----------------+
|   Hobart  | 1357 |   205556   |      619.5      |
+-----------+------+------------+-----------------+
| Melbourne | 1566 |  3806092   |      646.9      |
+-----------+------+------------+-----------------+
|   Perth   | 5386 |  1554769   |      869.4      |
+-----------+------+------------+-----------------+
|   Sydney  | 2058 |  4336374   |      1214.8     |
+-----------+------+------------+-----------------+
$ 
```
可以看到，此时非常像Excel表格，每个单元格都有外边框！！！

#### 3.10.2 默认每行都设置分隔线

我们也可以对`PrettyTable`类的`add_row`方法进行重写！

重写`add_row`方法，并创建表格：

```py
class MyPrettyTable(PrettyTable):
    # *表示位置参数的结束。之后的每个参数只能由关键字指定。这在PEP 3102中定义
    def add_row(self, row, *, default=True) -> None:
        # 调用父类的add_row方法
        super().add_row(row, divider=default)

# 注意，此处调用不是默认的PrettyTable()，而不自定义有MyPrettyTable()
x = MyPrettyTable()
x.title = "表7 设置默认分隔钱"
x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
x.add_row(["Adelaide", 1295, 1158259, 600.5])
x.add_row(["Brisbane", 5905, 1857594, 1146.4])
x.add_row(["Darwin", 112, 120900, 1714.7])
x.add_row(["Hobart", 1357, 205556, 619.5])
x.add_row(["Melbourne", 1566, 3806092, 646.9])
x.add_row(["Perth", 5386, 1554769, 869.4])
x.add_row(["Sydney", 2058, 4336374, 1214.8])
print(x)
```

此时，表格输出与上一节的结果相同！！

输出如下图所示：

![](/img/Snipaste_2023-04-30_19-15-03.png)

其他方法如果也想默认都设置分隔线，则需要对父类方法进行重写，像`from_csv`，则也都需要对父类的`from_csv`方法进行重写。此处忽略。

### 3.11 改变默认样式

可以使用`set_style`方法来改变默认的输出样式。

其参数支持以下内置样式：

- `DEFAULT`, 默认样式，用于撤消您可能所做的任何样式更改。
- `MSWORD_FRIENDLY`, 电子文档模式。
- `PLAIN_COLUMNS`, 一种无边框样式，适用于柱状数据的命令行程序。
- `MARKDOWN`, 遵循 Markdown 语法的样式。
- `ORGMODE`, 适合Org 模式语法的表格样式。
- `SINGLE_BORDER`和`DOUBLE_BORDER`, 使用带有方框图字符的连续单/双边框线的样式，以便在终端上进行更精美的显示。
- `RANDOM`, 随机模式，每一次打印都会在内置的样式中随机选择一个。

以3.6节天气数据为基础，此处参考官方文档修改表格样式。


#### 3.11.1 默认样式

先回顾一下默认样式：

```py
from prettytable import from_csv


with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 8 天气详情 默认样式'
    print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-04-30_22-02-23.png)


#### 3.11.2 电子文档样式

```py
from prettytable import from_csv, MSWORD_FRIENDLY


with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 8 天气详情 电子文档样式'
    x.set_style(MSWORD_FRIENDLY)
    print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-04-30_21-45-13.png)
可以看到，各行都没有横向的分隔线了。


#### 3.11.3 无边框样式

```py
from prettytable import from_csv, PLAIN_COLUMNS


with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 8 天气详情 无边框样式'
    x.set_style(PLAIN_COLUMNS)
    print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-04-30_21-50-17.png)
此时可以看到，表格没有任何边框。

#### 3.11.4  Markdown样式

也可以使用 Markdown 样式：

```py
from prettytable import from_csv, MARKDOWN


with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 8 天气详情 MARKDOWN样式'
    x.set_style(MARKDOWN)
    print(x)
```
运行后效果图如下：

![](/img/Snipaste_2023-04-30_21-54-21.png)
此时生成了MarkDown语法格式的表格输出，我们将字段名和数据行内容复制到此文档中粘贴，显示如下表所示：

| 序号 |   城市   |    日期   | 最低气温 | 最高气温 |
|:----:|:--------:|:---------:|:--------:|:--------:|
|  1   |   北京   | 2023/4/30 |    11    |    25    |
|  2   |   上海   | 2023/4/30 |    15    |    24    |
|  3   |   深圳   | 2023/4/30 |    20    |    26    |
|  4   |  哈尔滨  | 2023/4/30 |    1     |    9     |
|  5   | 呼和浩特 | 2023/4/30 |    7     |    21    |

可以看到，展示了一个完整的表格。

#### 3.11.5 ORG样式

不知道该样式是什么样的，测试看一下。

代码如下：

```py
from prettytable import from_csv, ORGMODE


with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 8 天气详情 ORGMODE样式'
    x.set_style(ORGMODE)
    print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-04-30_21-59-02.png)

可以看到，表格左右两边转角处的`+`十字形没有了，都换成了`|`竖线。其他处与默认模式一样！


#### 3.11.6 连续单、双框线

```py
from prettytable import from_csv, SINGLE_BORDER, DOUBLE_BORDER


with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 8 天气详情 SINGLE_BORDER连续单框线样式'
    x.set_style(SINGLE_BORDER)
    print(x)

    x.title = '表 8 天气详情 DOUBLE_BORDER连续双框线样式'
    x.set_style(DOUBLE_BORDER)
    print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-05-01_11-44-47.png)

此时可以看到，连续单双框线时，表格框线都连接起来了，中间没有中断，这时候的输出更像Excel中的表格。

#### 3.11.7 随机样式

可以使用`x.set_style(RANDOM)`来设置随机样式：

```py
from prettytable import from_csv, RANDOM


with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 8 天气详情 RANDOM随机样式'
    x.set_style(RANDOM)
    print(x)
```

![](/img/Snipaste_2023-05-01_16-31-56.png)
可以看到，运行了4次程序，4次输出的结果都不一样！！


### 3.12 表格对齐处理

- 默认情况下，表格每列都是居中对齐的。
- PrettyTable 实例的 align 属性控制列的对齐，可选的对齐方式有 "l"、"c" 和 "r"，对应是left、center、right靠左对齐、居中对齐和靠右对齐。

#### 3.12.1 默认对齐方式-居中对齐

默认情况下，各列使用居中对齐方式。请看示例：

```py
with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 9 天气详情 默认居中对齐'
    print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-05-01_12-00-10.png)

#### 3.12.2 一次设置所有列的对齐方式

```py
x.align = "r"
print(x)
```

可以使用以上代码将表格所有列都设置为右对齐。我们来测试一下：

```py
from prettytable import from_csv

with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 9 天气详情 所有列右对齐'
    x.align = 'r'
    print(x)

    x.title = '表 9 天气详情 所有列左对齐'
    x.align = 'l'
    print(x)

    x.title = '表 9 天气详情 所有列居中对齐'
    x.align = 'c'
    print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-05-01_12-05-45.png)

#### 3.12.3 单独控制每列对齐方式

通常情况下，我们需要单独控制每列的对齐方式，比如，有的列内容比较长，则不适合居中对齐，此时设置左对齐看起来更舒服。

```py
from prettytable import from_csv

with open("data.csv") as fp:
    x = from_csv(fp)
    x.title = '表 9 天气详情 每列单独控制对齐方式'
    x.align["序号"] = 'r'
    x.align["城市"] = 'l'
    x.align["日期"] = 'c'
    x.align["最低气温"] = 'r'
    x.align["最高气温"] = 'r'
    print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-05-01_14-46-32.png)
可以看到`序号`、`最低气温`、`最高气温`三列是右对齐，`城市`列是左对齐，`日期`列是居中对齐。这样每列的对齐方式就单独控制了！！

### 3.13 排序

为了演示排序的效果，我们补充天气数据，并进行数据的排序。

以下是默认情况下，不进行排序的代码：

```py
from prettytable import PrettyTable

x = PrettyTable()
x.title = '表 10 天气详情 默认排序'
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(
    [
        [1, '北京', '2023/4/30', 11, 25],
        [2, '上海', '2023/4/30', 15, 24],
        [3, '深圳', '2023/4/30', 20, 26],
        [4, '哈尔滨', '2023/4/30', 1, 9],
        [5, '呼和浩特', '2023/4/30', 7, 21],
        [6, '北京', '2023/5/1', 16, 27],
        [7, '上海', '2023/5/1', 17, 29],
        [8, '深圳', '2023/5/1', 29, 29],
        [9, '哈尔滨', '2023/5/1', 9, 19],
        [10, '呼和浩特', '2023/5/1', 9, 25]
    ]

)
print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-05-03_10-37-43.png)
#### 3.13.1 按指定字段名升序排序

在上一节代码的基础上，进行一些修改，按`最低气温`升序排序：

```py
x.title = '表 10 天气详情 按最低气温 升序排序'
x.sortby = '最低气温'
print(x)
```

使用`x.sortby = '最低气温'`按`最低气温`升序排序。

运行后效果图如下：

![](/img/Snipaste_2023-05-03_11-16-32.png)

#### 3.13.2 按指定字段名降序排序

在上一节代码的基础上，进行一些修改，按`最低气温`降序排序：

```py
x.title = '表 10 天气详情 按最低气温 降序排序'
x.sortby = '最低气温'
x.reversesort = True
print(x)
```

默认情况下，排序是使用的升序排序，要想降序排序，则需要使用`x.reversesort = True`。

运行后效果图如下：

![](/img/Snipaste_2023-05-03_11-19-28.png)

可以看到，最低气温的确是按从大到小降序排序的。

#### 3.13.3 按多个字段进行排序

说明：本节是先对原始数据进行排序，然后直接将数据打印出来的。并没有用`x.sortby = '最低气温'`这样的方式进行排序。

为了演示排序效果，我们对天气数据进行扩充。多增加一些数据。

```py
from prettytable import PrettyTable

rows = [
    [1, '北京', '2023/4/30', 11, 25],
    [2, '上海', '2023/4/30', 15, 24],
    [3, '深圳', '2023/4/30', 20, 26],
    [4, '哈尔滨', '2023/4/30', 1, 9],
    [5, '呼和浩特', '2023/4/30', 7, 21],
    [6, '北京', '2023/5/1', 16, 27],
    [7, '上海', '2023/5/1', 17, 29],
    [8, '深圳', '2023/5/1', 20, 29],
    [9, '哈尔滨', '2023/5/1', 9, 19],
    [10, '呼和浩特', '2023/5/1', 9, 25]
]
# 对rows进行排序,先按照第4列排序，再按照第5列升序排序
rows.sort(key=lambda r: (r[3], r[4]))

x = PrettyTable()
print('先按最低气温升序，再按最高气温升序排序')
x.title = '表 10 天气详情 多列排序'
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-05-05_23-23-37.png)
可以看到，`最低气温`列是从小到大升序排序的，然后当`最低气温`相同时，`最高气温`是按升序排序的。如`最低气温`为9时，`最高气温`是19在上、25在下，`最低气温`为20时，`最高气温`是26在上、29在下，说明也按`最高气温`升序排序了。


修改代码，先按最低气温升序，再按最高气温降序排序：

```py
from prettytable import PrettyTable

rows = [
    [1, '北京', '2023/4/30', 11, 25],
    [2, '上海', '2023/4/30', 15, 24],
    [3, '深圳', '2023/4/30', 20, 26],
    [4, '哈尔滨', '2023/4/30', 1, 9],
    [5, '呼和浩特', '2023/4/30', 7, 21],
    [6, '北京', '2023/5/1', 16, 27],
    [7, '上海', '2023/5/1', 17, 29],
    [8, '深圳', '2023/5/1', 20, 29],
    [9, '哈尔滨', '2023/5/1', 9, 19],
    [10, '呼和浩特', '2023/5/1', 9, 25]
]

# 对rows进行排序,先按照第4列排序，再按照第5列降序排序
rows.sort(key=lambda r: (r[3], -r[4]))


x = PrettyTable()
print('先按最低气温升序，再按最高气温降序排序')
x.title = '表 10 天气详情 多列排序'
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-05-05_23-32-59.png)

可以看到，`最低气温`列是从小到大升序排序的，然后当`最低气温`相同时，`最高气温`是按升序排序的。如`最低气温`为9时，`最高气温`是25在上、19在下，`最低气温`为20时，`最高气温`是29在上、26在下，说明按`最高气温`降序排序了。

### 3.14 输出格式化字符串

我们可以使用`get_string`、`get_csv_string`、`get_html_string`、`get_json_string`输出特殊格式的字符串，然后输出导文件中。

- `get_string`，原样输出表格对应的字符串。
- `get_csv_string`，输出csv类型字符串。
- `get_html_string`，输出html格式的字符串。
- `get_json_string`，输出json格式的字符串。

#### 3.14.1 get_string原样输出表格

get_string可以原样输出表格对应的字符串，请看以下示例：

```py
from prettytable import PrettyTable

rows = [
    [1, '北京', '2023/4/30', 11, 25],
    [2, '上海', '2023/4/30', 15, 24],
    [3, '深圳', '2023/4/30', 20, 26],
    [4, '哈尔滨', '2023/4/30', 1, 9],
    [5, '呼和浩特', '2023/4/30', 7, 21],
]

x = PrettyTable()
x.title = '表 11 天气详情 输出格式化字符串'
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)
print(type(x))
out_str = x.get_string()
print(out_str)
print(type(out_str))
```

运行后效果图如下：

![](/img/Snipaste_2023-05-05_23-51-18.png)
可以看到，`out_str`的类型是`str`字符串类型，其输出的效果与`print(x)`的效果一样。

下面我改一下代码，将格式化的字符写入到文件：

```py
from prettytable import PrettyTable

rows = [
    [1, '北京', '2023/4/30', 11, 25],
    [2, '上海', '2023/4/30', 15, 24],
    [3, '深圳', '2023/4/30', 20, 26],
    [4, '哈尔滨', '2023/4/30', 1, 9],
    [5, '呼和浩特', '2023/4/30', 7, 21],
]

x = PrettyTable()
x.title = '表 11 天气详情 输出格式化字符串'
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)
out_str = x.get_string()

with open('default.txt', mode='w') as f:
    f.write(f'{out_str}\n')
```
运行程序，并在控制台查看输入的文件`default.txt`，效果图如下：

![](/img/Snipaste_2023-05-05_23-58-27.png)
可以看到，查看文件`default.txt`的内容，与`print(x)`的输出效果是一样的。

#### 3.14.2 输出其他格式字符串

```py
with open('out.html', mode='w') as f:
    out_str = x.get_html_string()
    f.write(f'{out_str}\n')

with open('out.json', mode='w') as f:
    # 此处需要指定ensure_ascii=False，否则中文乱码
    out_str = x.get_json_string(ensure_ascii=False)
    f.write(f'{out_str}\n')

with open('out.csv', mode='w') as f:
    out_str = x.get_csv_string()
    f.write(f'{out_str}\n')
```

在上一节的基础上，我们分别输出html、json、csv格式的文件，运行后效果图如下：

![](/img/Snipaste_2023-05-06_00-10-58.png)

![](/img/Snipaste_2023-05-06_00-16-11.png)

![](/img/Snipaste_2023-05-06_00-16-40.png)

### 3.15 更高级的样式配置

PrettyTable有许多样式选项，用于控制表格显示的各个方面。您可以自由地将这些选项中的每一个单独设置为您喜欢的任何选项。`set_style`方法会为你自动处理相关设置。

简单的改变表格样式可以参考 3.11节 改变默认样式。

以下是官方文档中给的的参数列表：

> The options are these:
> 
> - border - A boolean option (must be True or False). Controls whether a border is drawn inside and around the table.
> - preserve_internal_border - A boolean option (must be True or False). Controls whether borders are still drawn within the table even when border=False.
> - header - A boolean option (must be True or False). Controls whether the first row of the table is a header showing the names of all the fields.
> - hrules - Controls printing of horizontal rules after rows. Allowed values: FRAME, HEADER, ALL, NONE - note that these are variables defined inside the prettytable module so make sure you import them or use prettytable.FRAME etc.
> - vrules - Controls printing of vertical rules between columns. Allowed values: FRAME, ALL, NONE.
> - int_format - A string which controls the way integer data is printed. This works like: print("%<int_format>d" % data)
> - float_format - A string which controls the way floating point data is printed. This works like: print("%<float_format>f" % data)
> - custom_format - A Dictionary of field and callable. This allows you to set any format you want pf.custom_format["my_col_int"] = ()lambda f, v: f"{v:,}". The type of the callable if callable[[str, Any], str]
> - padding_width - Number of spaces on either side of column data (only used if left and right paddings are None).
> - left_padding_width - Number of spaces on left-hand side of column data.
> - right_padding_width - Number of spaces on right-hand side of column data.
> - vertical_char - Single character string used to draw vertical lines. Default is |.
> - horizontal_char - Single character string used to draw horizontal lines. Default is -.
> - _horizontal_align_char - single character string used to indicate column alignment in horizontal lines. Default is : for Markdown, otherwise None.
> - junction_char - Single character string used to draw line junctions. Default is +.
> - top_junction_char - single character string used to draw top line junctions. Default is junction_char.
> - bottom_junction_char - single character string used to draw bottom line junctions. Default is junction_char.
> - right_junction_char - single character string used to draw right line junctions. Default is junction_char.
> - left_junction_char - single character string used to draw left line junctions. Default is junction_char.
> - top_right_junction_char - single character string used to draw top-right line junctions. Default is junction_char.
> - top_left_junction_char - single character string used to draw top-left line junctions. Default is junction_char.
> - bottom_right_junction_char - single character string used to draw bottom-right line junctions. Default is junction_char
> - bottom_left_junction_char - single character string used to draw bottom-left line junctions. Default is junction_char.

我们编写一个设置高级样式的示例：

```py
from prettytable import PrettyTable, ALL, FRAME, HEADER, NONE

rows = [
    [1, '北京', '2023/4/30', 11, 25],
    [2, '上海', '2023/4/30', 15, 24],
    [3, '深圳', '2023/4/30', 20, 26],
    [4, '哈尔滨', '2023/4/30', 1, 9],
    [5, '呼和浩特', '2023/4/30', 7, 21],
]

x = PrettyTable()
x.title = '表 12 天气详情 默认样式'
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)
x.title = '表 12 天气详情 高级样式设置'
# 设置列数据左侧的空格数
x.left_padding_width = 4
# 设置列数据右侧的空格数
x.right_padding_width = 4
# 设置绘制垂直线的单个字符串
x.vertical_char = '$'
# 设置绘制水平线的单个字符串
x.horizontal_char = '='
# 设置整数数据打印方式的字符串, 整数设置宽为3，不够3位左侧补0
x.int_format = '03'
# 控制行后水平方向的打印
# ALL全部打印
# FRAME打印头部行、字段行、最后行下面的水平线
# HEADER 只打印头部
# NONE 不打印
x.hrules = ALL
print(x)

```

运行程序，效果图如下：

![](/img/Snipaste_2023-05-06_18-09-53.png)
可以看到，我们设置的几个属性都起作用了。如`x.int_format = '03'`设置整数数据打印方式的字符串, 整数设置宽为3，不够3位左侧补0，可以看到`序号`、`最低气温`、`最高气温`三列中的数字都不够三位，左侧都补了0。

你可以根据自己喜好设置不同的表格样式。

### 3.16 改变表格颜色

- prettytable可以使用ANSI颜色码来控制表格的输出颜色。
- 使用时，只需要使用`ColorTable`代替`PrettyTable`即可，

如：

```py
-from prettytable import PrettyTable
+from prettytable.colortable import ColorTable
```

- `ColorTable`的使用与`PrettyTable`相同，只是额外增加了一些参数，你可以设置自定义主题。

如：

```py
from prettytable.colortable import ColorTable, Themes

x = ColorTable(theme=Themes.OCEAN)

print(x)
```

这种是使用prettytable自带的`OCEAN`海洋主题。

查看源码知道主题定义如下：

```py
class Themes:
    DEFAULT = Theme()
    OCEAN = Theme(
        default_color="96",
        vertical_color="34",
        horizontal_color="34",
        junction_color="36",
    )
```

我们可以自定义主题，类似`OCEAN`海洋主题设置不同的颜色值即可。

维基百科上面详细介绍了 [ANSI转义序列 https://zh.wikipedia.org/wiki/ANSI%E8%BD%AC%E4%B9%89%E5%BA%8F%E5%88%97](https://zh.wikipedia.org/wiki/ANSI%E8%BD%AC%E4%B9%89%E5%BA%8F%E5%88%97)

其中有详细的颜色表！

![](/img/Snipaste_2023-05-06_22-16-46.png)

我们在自定义主题设置时，可以随意使用上表中的前景色代码或背景色代码。

我们按官方示例进行尝试一下：

```py
from prettytable.colortable import ColorTable, Themes, Theme

rows = [
    [1, '北京', '2023/4/30', 11, 25],
    [2, '上海', '2023/4/30', 15, 24],
    [3, '深圳', '2023/4/30', 20, 26],
    [4, '哈尔滨', '2023/4/30', 1, 9],
    [5, '呼和浩特', '2023/4/30', 7, 21],
]

x = ColorTable(theme=Themes.OCEAN)
x.title = '表 13 天气详情 改变表格颜色'
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)
```

运行后效果图如下：

![](/img/Snipaste_2023-05-06_22-25-42.png)
此时，可以看到，由于添加了表格标题，标题内容有点移位，不在表格正上方。为了测试颜色效果，我们不配置表格标题再测试。

```py
from prettytable.colortable import ColorTable, Themes, Theme

rows = [
    [1, '北京', '2023/4/30', 11, 25],
    [2, '上海', '2023/4/30', 15, 24],
    [3, '深圳', '2023/4/30', 20, 26],
    [4, '哈尔滨', '2023/4/30', 1, 9],
    [5, '呼和浩特', '2023/4/30', 7, 21],
]

# 使用海洋主题
x = ColorTable(theme=Themes.OCEAN)
print('\n表 13 天气详情 使用系统自带海洋主题 改变表格颜色')
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)

# 自定义主题
MYTHEME = Theme(
    default_color="31",  # 默认使用红色前景色
    vertical_color="44",  # 垂直线使用蓝色背景色
    horizontal_color="33", # 水平线使用黄色前景色
    junction_color="97",  # 连接线使用亮白色前景色
)

x = ColorTable(theme=MYTHEME)
print('\n表 13 天气详情 使用自定义主题 改变表格颜色')
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)
```

运行程序，效果图如下：

![](/img/Snipaste_2023-05-06_22-34-13.png)

可以看到，设置的前景色和背景色都起作用了！说明我们创建的自定义主题的配置方法是对的！

### 3.17 复制表格

有时候，你如果只想复制表格中的某些行，可以使用切片的方式获取子表。

在上一节的基础上，我们直接来获取子表信息：

```py
y = x[1:3]
print('\n获取第2和第3行子表')
print(y)
print('\n\n获取第1和第3行子表')
z = x[0:4:2]
print(z)
```

运行程序，效果图如下：

![](/img/Snipaste_2023-05-06_23-09-07.png)
可以看到，的确获取到了两个子表。


**以上就是prettytable模块的全部用法了。本文档结束！！！**



参考：

- pypi prettytable [https://pypi.org/project/prettytable/](https://pypi.org/project/prettytable/)
- 中文对齐 [Better display of Chinese #49](https://github.com/jazzband/prettytable/issues/49)
- 自定义样式 [Python中prettytable库](https://blog.csdn.net/qq_62789540/article/details/126039567)
- [PEP 3102 – Keyword-Only Arguments](https://peps.python.org/pep-3102/)
- [python-格式化输出表格+中英文对齐](https://www.cnblogs.com/luoxian1011/p/16582325.html)