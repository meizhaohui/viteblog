# windows批处理的使用

[[toc]]

## 1. 概述

- 命令提示符（CMD）是Windows操作系统中内置的命令行工具，它提供了一种直接与计算机系统进行交互的方式。虽然现代操作系统提供了许多图形化界面和工具，但命令提示符在某些场景下仍然具有重要的作用。比如重复任务的执行，日志的定时删除等操作，都可以借助命令行工具来完成。
-  批处理文件（batch file）包含一系列  DOS命令，通常用于自动执行重复性任务。用户只需双击批处理文件便可执行任务，而无需重复输入相同指令。编写批处理文件非常简单，但难点在于确保一切按顺序执行。编写严谨的批处理文件可以极大程度地节省时间，在应对重复性工作时尤其有效。
-  批处理(Batch)，也称为批处理脚本。顾名思义，批处理就是对某对象进行批量的处理。批处理文件的扩展
   名为bat， 批处理类似于Unix中的Shell脚本。
-  批处理是一种简化的脚本语言，它应用于DOS和Windows系统中，它是由DOS或者Windows系统内嵌的
   命令解释器（通常是CMD.EXE）解释运行。
- 学习批处理，一般从学习批处理命令开始，在命令行进行操作。
- 学会常用命令后，就可以编写批处理脚本，让批处理脚本为我们提供服务。

### 1.1 打开命令行窗口

我使用的windows系统版本是`Windows 10 家庭中文版`：

![](/img/Snipaste_2023-12-02_13-16-58.png)

可以通过多次方式打开命令行窗口。

- 方式1： 通过windows搜索功能，在搜索框直接输入`cmd`搜索，搜索出结果后，点击【打开】或【以管理员身份运行】：

![](/img/Snipaste_2023-12-02_13-18-23.png)

【以管理员身份运行】则可以获取更多的权限。建议通常直接点击【打开】或者直接搜索出结果后按Enter键回车。

![](/img/Snipaste_2023-12-02_13-33-18.png)

这样默认会打开用户的家目录。



- 方式2：在当前目录下的路径栏，输入`cmd`可以打开当前目录下的命令行。

如当前目录是`D:\data\temp`，直接在路径栏输入`cmd`：

![](/img/Snipaste_2023-12-02_13-28-38.png)

此时就可以直接在命令行进入到当前目录。

![](/img/Snipaste_2023-12-02_13-29-51.png)

**推荐使用这种方式，可以快速切换到自己需要处理的工作目录。**



- 方式3： 通过Win+R键，输入`cmd`启动命令行。

![](/img/Snipaste_2023-12-02_13-40-41.png)

这种方式打开的命令行窗口也是处于家目录下。



- 方式4：任务管理器中，依次点击【文件】--【运行新任务】，在打开的输入框处理`cmd`然后回车即可。

![](/img/Snipaste_2023-12-02_13-43-13.png)

这种方式打开的命令行窗口处于`C:\WINDOWS\system32>`目录下。

![](/img/Snipaste_2023-12-02_13-45-07.png)



### 1.2 改变命令行窗口颜色

直接在命令行窗口，在标题处点击鼠标右键，选择【属性】：

![](/img/Snipaste_2023-12-02_13-51-59.png)

选择【屏幕背景】，然后在下面的颜色处，直接点击右侧的白色：

![](/img/Snipaste_2023-12-02_13-53-43.png)

然后选择【屏幕文字】，然后在下面的颜色处，直接点击左侧的黑色，最后点击【确认】：

![](/img/Snipaste_2023-12-02_13-56-33.png)

关闭当前命令行窗口，重新打开一个命令行窗口，可以看到窗口颜色已经发生变化了。

![](/img/Snipaste_2023-12-02_13-57-59.png)



### 1.3 查看帮助信息

通常情况下，可以使用`HELP`来获取帮助信息。

```sh
D:\data\temp> HELP
有关某个命令的详细信息，请键入 HELP 命令名
ASSOC          显示或修改文件扩展名关联。
ATTRIB         显示或更改文件属性。
BREAK          设置或清除扩展式 CTRL+C 检查。
BCDEDIT        设置启动数据库中的属性以控制启动加载。
CACLS          显示或修改文件的访问控制列表(ACL)。
CALL           从另一个批处理程序调用这一个。
CD             显示当前目录的名称或将其更改。
CHCP           显示或设置活动代码页数。
CHDIR          显示当前目录的名称或将其更改。
CHKDSK         检查磁盘并显示状态报告。
CHKNTFS        显示或修改启动时间磁盘检查。
CLS            清除屏幕。
CMD            打开另一个 Windows 命令解释程序窗口。
COLOR          设置默认控制台前景和背景颜色。
COMP           比较两个或两套文件的内容。
COMPACT        显示或更改 NTFS 分区上文件的压缩。
CONVERT        将 FAT 卷转换成 NTFS。你不能转换
               当前驱动器。
COPY           将至少一个文件复制到另一个位置。
DATE           显示或设置日期。
DEL            删除至少一个文件。
DIR            显示一个目录中的文件和子目录。
DISKPART       显示或配置磁盘分区属性。
DOSKEY         编辑命令行、撤回 Windows 命令并
               创建宏。
DRIVERQUERY    显示当前设备驱动程序状态和属性。
ECHO           显示消息，或将命令回显打开或关闭。
ENDLOCAL       结束批文件中环境更改的本地化。
ERASE          删除一个或多个文件。
EXIT           退出 CMD.EXE 程序(命令解释程序)。
FC             比较两个文件或两个文件集并显示
               它们之间的不同。
FIND           在一个或多个文件中搜索一个文本字符串。
FINDSTR        在多个文件中搜索字符串。
FOR            为一组文件中的每个文件运行一个指定的命令。
FORMAT         格式化磁盘，以便用于 Windows。
FSUTIL         显示或配置文件系统属性。
FTYPE          显示或修改在文件扩展名关联中使用的文件
               类型。
GOTO           将 Windows 命令解释程序定向到批处理程序
               中某个带标签的行。
GPRESULT       显示计算机或用户的组策略信息。
GRAFTABL       使 Windows 在图形模式下显示扩展
               字符集。
HELP           提供 Windows 命令的帮助信息。
ICACLS         显示、修改、备份或还原文件和
               目录的 ACL。
IF             在批处理程序中执行有条件的处理操作。
LABEL          创建、更改或删除磁盘的卷标。
MD             创建一个目录。
MKDIR          创建一个目录。
MKLINK         创建符号链接和硬链接
MODE           配置系统设备。
MORE           逐屏显示输出。
MOVE           将一个或多个文件从一个目录移动到另一个
               目录。
OPENFILES      显示远程用户为了文件共享而打开的文件。
PATH           为可执行文件显示或设置搜索路径。
PAUSE          暂停批处理文件的处理并显示消息。
POPD           还原通过 PUSHD 保存的当前目录的上一个
               值。
PRINT          打印一个文本文件。
PROMPT         更改 Windows 命令提示。
PUSHD          保存当前目录，然后对其进行更改。
RD             删除目录。
RECOVER        从损坏的或有缺陷的磁盘中恢复可读信息。
REM            记录批处理文件或 CONFIG.SYS 中的注释(批注)。
REN            重命名文件。
RENAME         重命名文件。
REPLACE        替换文件。
RMDIR          删除目录。
ROBOCOPY       复制文件和目录树的高级实用工具
SET            显示、设置或删除 Windows 环境变量。
SETLOCAL       开始本地化批处理文件中的环境更改。
SC             显示或配置服务(后台进程)。
SCHTASKS       安排在一台计算机上运行命令和程序。
SHIFT          调整批处理文件中可替换参数的位置。
SHUTDOWN       允许通过本地或远程方式正确关闭计算机。
SORT           对输入排序。
START          启动单独的窗口以运行指定的程序或命令。
SUBST          将路径与驱动器号关联。
SYSTEMINFO     显示计算机的特定属性和配置。
TASKLIST       显示包括服务在内的所有当前运行的任务。
TASKKILL       中止或停止正在运行的进程或应用程序。
TIME           显示或设置系统时间。
TITLE          设置 CMD.EXE 会话的窗口标题。
TREE           以图形方式显示驱动程序或路径的目录
               结构。
TYPE           显示文本文件的内容。
VER            显示 Windows 的版本。
VERIFY         告诉 Windows 是否进行验证，以确保文件
               正确写入磁盘。
VOL            显示磁盘卷标和序列号。
XCOPY          复制文件和目录树。
WMIC           在交互式命令 shell 中显示 WMI 信息。

有关工具的详细信息，请参阅联机帮助中的命令行参考。

D:\data\temp>
```

可以看到，我们直接输入`HELP`就可以查看到帮助信息。



通过以下输出的帮助信息，命令都是使用的大写的，但实际上windows上CMD命令对大小写不敏感，即命令或参数可以用大写或小写字母，但为了与帮助信息保持一致，我后面还是会使用大写形式执行命令。



**由于windows系统自带的命令行工具，使用Ctrl+Shift+C复制命令行输出时，在每一行后面会存在很多空格，粘贴不方便，后面我直接使用MobaXterm来打开命令行工具进行操作。**



比如我要查看`PROMPT`命令的帮助信息，可以这样操作：

```sh
D:\data\temp> HELP PROMPT
更改 cmd.exe 命令提示符。

PROMPT [text]

  text    指定新的命令提示符。

提示符可以由普通字符及下列特殊代码组成:

  $A   & (与号)
  $B   | (坚线)
  $C   ( (左括号)
  $D   当前日期
  $E   转义码(ASCII 码 27)
  $F   ) (右括号)
  $G   > (大于号)
  $H   Backspace (删除前一个字符)
  $L   < (小于号)
  $N   当前驱动器
  $P   当前驱动器及路径
  $Q   = (等号)
  $S     (空格)
  $T   当前时间
  $V   Windows 版本号
  $_   回车换行符
  $$   $ (美元符号)

如果命令扩展被启用，PROMPT 命令会支持下列格式化字符:

  $+   根据 PUSHD 目录堆栈的深度，零个或零个以上加号(+)字符，
       一个推的层一个字符。

  $M   如果当前驱动器不是网络驱动器，显示跟当前驱动器号或
       空字符串有关联的远程名。

D:\data\temp>
```

可以看到，`PROMPT` 命令的帮助信息显示了出来，该命令用于更改 cmd.exe 命令提示符，这正是我需要做的事情。



### 1.4 更改 cmd.exe 命令提示符

上一节，我已经获取`PROMPT` 命令的帮助信息了，我们直接来测试一下。

```sh
D:\data\temp> PROMPT [meizhaohui@windows$S$P]$$$S

[meizhaohui@windows D:\data\temp]$ cmd --version
Microsoft Windows [版本 10.0.19045.3693]
(c) Microsoft Corporation。保留所有权利。

Clink v1.5.18.dd581e
Copyright (c) 2012-2018 Martin Ridgers
Portions Copyright (c) 2020-2023 Christopher Antos
https://github.com/chrisant996/clink

[meizhaohui@windows D:\data\temp]$
```

![](/img/Snipaste_2023-12-02_15-35-05.png)

这时候命令提示符就与Linux上面的命令提示符非常像了。



如果仅想命令提示符是`$ `，则可以按如下方式设置：

```sh
PROMPT $$$S
```





## 2. 常用CMD命令

### 2.1 ECHO显示消息

查看`ECHO`命令帮助信息：

```sh
[meizhaohui@windows D:\data\temp]$ HELP ECHO
显示消息，或者启用或关闭命令回显。

  ECHO [ON | OFF]
  ECHO [message]

若要显示当前回显设置，请键入不带参数的 ECHO。

[meizhaohui@windows D:\data\temp]$
```

查看命令回显状态：

```sh
[meizhaohui@windows D:\data\temp]$ ECHO
ECHO 处于打开状态。
```

可以看到ECHO回显处于打开状态。



输出消息，按惯例，输出`hello, world`。

```sh
[meizhaohui@windows D:\data\temp]$ ECHO hello world
hello world

[meizhaohui@windows D:\data\temp]$ ECHO "hello world"
"hello world"

```

可以看到，`ECHO`后面的message消息默认不需要用引号包裹起来，用引号包裹时，引号也会原样输出。





### 2.2 目录与文件管理命令

#### 2.2.1 CD切换目录

查看帮助信息：

```sh
[meizhaohui@windows D:\data\temp]$ HELP CD
显示当前目录名或改变当前目录。

CHDIR [/D] [drive:][path]
CHDIR [..]
CD [/D] [drive:][path]
CD [..]

  ..   指定要改成父目录。

键入 CD drive: 显示指定驱动器中的当前目录。
不带参数只键入 CD，则显示当前驱动器和目录。

使用 /D 开关，除了改变驱动器的当前目录之外，
还可改变当前驱动器。

如果命令扩展被启用，CHDIR 会如下改变:

当前的目录字符串会被转换成使用磁盘名上的大小写。所以，
如果磁盘上的大小写如此，CD C:\TEMP 会将当前目录设为
C:\Temp。

CHDIR 命令不把空格当作分隔符，因此有可能将目录名改为一个
带有空格但不带有引号的子目录名。例如:

     cd \winnt\profiles\username\programs\start menu

与下列相同:

     cd "\winnt\profiles\username\programs\start menu"

在扩展停用的情况下，你必须键入以上命令。

[meizhaohui@windows D:\data\temp]$
```

可以看到，`CD`与`CHDIR`等价，可以认为`CD`是`CHDIR`的快捷命令。

```sh
# 查看当前目录
[meizhaohui@windows D:\data\temp]$ CD
D:\data\temp

# 切换到上一级目录
[meizhaohui@windows D:\data\temp]$ CD ..

# 切换回上一次的目录
[meizhaohui@windows D:\data]$ CD -

# 切换目录时改变驱动器
[meizhaohui@windows D:\data\temp]$ CD /D C:\Windows\System32\

# 再次查看当前目录，可以看到已经变成 C:\Windows\System32
[meizhaohui@windows C:\Windows\System32]$ CD
C:\Windows\System32

[meizhaohui@windows C:\Windows\System32]$
```

**通常不建议在系统自带的目录进行测试，万一操作失误，就损失巨大。**



将工作目录切换回`D:\data\temp`：

```sh
[meizhaohui@windows C:\Windows\System32]$ CD /D D:\data\temp

[meizhaohui@windows D:\data\temp]$
```



#### 2.2.2 DIR显示目录中的文件和子目录列表

可以使用`DIR`命令显示目录中的文件和子目录列表，查看帮助信息：

```sh
[meizhaohui@windows D:\data\temp]$ HELP DIR
显示目录中的文件和子目录列表。

DIR [drive:][path][filename] [/A[[:]attributes]] [/B] [/C] [/D] [/L] [/N]
  [/O[[:]sortorder]] [/P] [/Q] [/R] [/S] [/T[[:]timefield]] [/W] [/X] [/4]

  [drive:][path][filename]
              指定要列出的驱动器、目录和/或文件。

  /A          显示具有指定属性的文件。
  属性         D  目录                R  只读文件
               H  隐藏文件            A  准备存档的文件
               S  系统文件            I  无内容索引文件
               L  重新分析点          O  脱机文件
               -  表示“否”的前缀
  /B          使用空格式(没有标题信息或摘要)。
  /C          在文件大小中显示千位数分隔符。这是默认值。用 /-C 来
              禁用分隔符显示。
  /D          跟宽式相同，但文件是按栏分类列出的。
  /L          用小写。
  /N          新的长列表格式，其中文件名在最右边。
  /O          用分类顺序列出文件。
  排列顺序     N  按名称(字母顺序)     S  按大小(从小到大)
               E  按扩展名(字母顺序)   D  按日期/时间(从先到后)
               G  组目录优先           -  反转顺序的前缀
  /P          在每个信息屏幕后暂停。
  /Q          显示文件所有者。
  /R          显示文件的备用数据流。
  /S          显示指定目录和所有子目录中的文件。
  /T          控制显示或用来分类的时间字符域
  时间段      C  创建时间
              A  上次访问时间
              W  上次写入的时间
  /W          用宽列表格式。
  /X          显示为非 8dot3 文件名产生的短名称。格式是 /N 的格式，
              短名称插在长名称前面。如果没有短名称，在其位置则
              显示空白。
  /4          以四位数字显示年份

可以在 DIRCMD 环境变量中预先设定开关。通过添加前缀 - (破折号)
来替代预先设定的开关。例如，/-W。

[meizhaohui@windows D:\data\temp]$
```

注意，`/N`与`X`与长短名称有关，此处不详细介绍。

> 8.3命名规则
>
> DOS下命名文件名的一种规格：主文件名是小于等于8个英文字符，扩展名为特定的某3个英文字符，他们之间必须用“.”连接起来，构成一个完整的文件名。
>
>  若同一文件夹有相似的名称，末端的数值则会自动递增。 
>
>  该模式只允许文件名存在1个“.”符号，不能创建包含超过1个“.”符号的文件夹或文件。 

测试一下：

```sh
[meizhaohui@windows D:\data\temp]$ DIR
 驱动器 D 中的卷是 LENOVO
 卷的序列号是 9EA4-2025

 D:\data\temp 的目录

2023/12/02  13:04    <DIR>          .
2023/12/02  13:04    <DIR>          ..
               0 个文件              0 字节
               2 个目录 22,973,845,504 可用字节

[meizhaohui@windows D:\data\temp]$
```

可以看到，当前目录下0个文件，0字节。由于该目录没有文件，我们切换到别的目录来验证`DIR`命令。



切换目录到`C:\Program Files (x86)\Microsoft\Edge\Application`。

由于`CHDIR` 命令不把空格当作分隔符，直接切换目录：

```sh
[meizhaohui@windows D:\data\temp]$ CD /D C:\Program Files (x86)\Microsoft\Edge\Application

[meizhaohui@windows C:\Program Files (x86)\Microsoft\Edge\Application]$
```

查看当前目录中的文件和子目录列表信息：

```sh
[meizhaohui@windows C:\Program Files (x86)\Microsoft\Edge\Application]$ DIR
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  4,015,476,736 可用字节

[meizhaohui@windows C:\Program Files (x86)\Microsoft\Edge\Application]$
```

该目录实际情况：

![](/img/Snipaste_2023-12-02_16-56-27.png)

可以看到，`DIR`命令默认会将当前目录`.`和父目录`..`算作两个目录，然后再与当前目录下存在的真实目录相加，得到目录数量。

##### 2.2.2.1 /A 依据文件属性显示文件

```
  /A          显示具有指定属性的文件。
  属性         D  目录                R  只读文件
               H  隐藏文件            A  准备存档的文件
               S  系统文件            I  无内容索引文件
               L  重新分析点          O  脱机文件
               -  表示“否”的前缀
```

需要用`/A`参数，带一个属性值。

- 只显示目录

```sh
[meizhaohui@windows C:\Program Files (x86)\Microsoft\Edge\Application]$ DIR /AD
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/25  11:17    <DIR>          SetupMetrics
               0 个文件              0 字节
               4 个目录  8,400,134,144 可用字节
```

可以看到，只显示出来了目录，未显示`msedge.exe`之类的文件。



- 只显示文件

你可以使用`-`前缀标记，用来不显示某些属性。如不显示文件夹，只显示文件，则可以用如下命令：

```sh
[meizhaohui@windows C:\Program Files (x86)\Microsoft\Edge\Application]$ DIR /A-D
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
               5 个文件      6,510,009 字节
               0 个目录  8,406,904,832 可用字节
```



您可以使用冒号将开关与其可选代码分隔开，而不是像我们在示例中那样将主开关和字母代码挤在一起。就像下面这样，这会使代码更容易解析，使用冒号将开关与其可选代码分隔开是可选的。

```sh
[meizhaohui@windows C:\Program Files (x86)\Microsoft\Edge\Application]$ DIR /A:D
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/25  11:17    <DIR>          SetupMetrics
               0 个文件              0 字节
               4 个目录  8,402,055,168 可用字节

[meizhaohui@windows C:\Program Files (x86)\Microsoft\Edge\Application]$ DIR /A:-D
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
               5 个文件      6,510,009 字节
               0 个目录  8,402,055,168 可用字节
```



当文件路径非常长时，使用以上命令提示符，会占用很长的位置，为了让测试更加简单，我们设置命令行提示符为`$ `。

```sh
[meizhaohui@windows C:\Program Files (x86)\Microsoft\Edge\Application]$ PROMPT $$$S

$ DIR /A:-D
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
               5 个文件      6,510,009 字节
               0 个目录  8,401,969,152 可用字节

$
```

改变命令提示符后，我们只用关注命令本身，不用过多关注命令提示符了。



##### 2.2.2.2 /B 仅显示目录和文件名称

`/B`参数会删除所有多余的信息，只显示当前目录中文件夹和文件的名称。

```sh
$ DIR /B
114.0.1823.58
delegatedWebFeatures.sccd
msedge.exe
msedge.VisualElementsManifest.xml
msedge_proxy.exe
pwahelper.exe
SetupMetrics

```

可以看到只显示了当前目录中文件夹和文件的名称，没有显示`.`点目录和`..`父目录，也没有显示文件大小和时间戳等属性。

这有时候会比较有用，便于轮询文件夹。



##### 2.2.2.3 /C 在文件大小中显示千位数分隔符

`/C`参数会在文件大小中显示千位数分隔符。这是默认值。可以用`/-C` 来禁用分隔符显示。

如果我们不想显示千位数分隔符，则可以如下操作：

```sh
# 只显示文件，默认情况下，会显示千位数分隔符， 如`18,112`
$ DIR /A:-D
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
               5 个文件      6,510,009 字节
               0 个目录  8,387,518,464 可用字节

# 只显示文件，关闭千位数分隔符显示， `18,112`会显示为`18112`
$ DIR /A:-D /-C
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/22  08:01             18112 delegatedWebFeatures.sccd
2023/06/22  15:07           4113856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08           1198016 msedge_proxy.exe
2023/06/22  15:08           1179584 pwahelper.exe
               5 个文件        6510009 字节
               0 个目录     8387518464 可用字节

$
```



##### 2.2.2.4 /L 用小写显示文件名

`/L`参数会将文件夹或文件名称转换成小写显示。

```sh
# 默认方式显示，包含大写的文件名还是大写，如`SetupMetrics`
$ DIR
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  8,384,532,480 可用字节

# 开启小写方式显示，包含大写的文件名也会显示成小写，如`SetupMetrics`现在显示为`setupmetrics`
$ DIR /L
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/22  08:01            18,112 delegatedwebfeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.visualelementsmanifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/25  11:17    <DIR>          setupmetrics
               5 个文件      6,510,009 字节
               4 个目录  8,384,516,096 可用字节

$
```



##### 2.2.2.5 /O 按指定属性分类排序

`/O`参数会对文件按指定属性分类进行排序。

可指定的属性包含：
- N  按Name名称(字母顺序)     
- S  按Size大小(从小到大)
- E  按Extension扩展名(字母顺序) 
- D  按Date日期/时间(从先到后)
- G  Group组目录优先
- `-`  反转顺序的前缀



**按名称顺序排序：**

```sh
$ DIR
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  7,810,658,304 可用字节

$ DIR /O:N
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  7,810,592,768 可用字节

$
```

可以看到，直接使用`DIR`与使用`DIR /O:N`输出的结果是一样，说明`DIR`默认就是按名称排序的。



**按文件大小排序：**

```sh
# 搂文件大小排序，从小到大
$ DIR /O:S
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/25  11:17    <DIR>          SetupMetrics
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:07         4,113,856 msedge.exe
               5 个文件      6,510,009 字节
               4 个目录  7,810,256,896 可用字节

# 搂文件大小排序，从大到小
$ DIR /O:-S
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/22  15:07         4,113,856 msedge.exe
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/25  08:45    <DIR>          ..
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  7,810,256,896 可用字节

$
```



**按扩展名排序：**

```sh
# 按扩展名排序，可以看到相同扩展名的文件会上下挨着的
$ DIR /O:E
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  11:17    <DIR>          SetupMetrics
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
               5 个文件      6,510,009 字节
               4 个目录  7,809,757,184 可用字节

$ DIR /O:-E
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  7,809,757,184 可用字节

$
```



**按日期排序：**

```sh
# 按日期排序，文件时间越久越靠前
$ DIR /O:D
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  7,809,122,304 可用字节

$ DIR /O:-D
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  11:17    <DIR>          SetupMetrics
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
               5 个文件      6,510,009 字节
               4 个目录  7,809,122,304 可用字节

$
```



**按组排序：**

```sh
# 按组排序，先显示文件夹，再显示文件
$ DIR /O:G
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/25  11:17    <DIR>          SetupMetrics
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
               5 个文件      6,510,009 字节
               4 个目录  7,807,901,696 可用字节

# 按组反序，先显示文件，再显示文件夹
$ DIR /O:-G
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/25  08:45    <DIR>          ..
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  8,190,418,944 可用字节

$
```

##### 2.2.2.6 /P 分页显示

`/P`参数会在每个信息屏幕后暂停，也就是分页显示。当一个文件夹有成千上万个文件时，使用`/P`开关可以一页一页的显示有哪些文件。你可测试一下。



当你配合`/S`参数一起递归查看文件夹时，这个开关更有用。



##### 2.2.2.7 /S 递归查找

`/S`参数会显示指定目录和所有子目录中的文件。当不使用`/P`参数时，`DIR`命令会一股脑地把该文件夹下所有文件和文件夹都显示出来，像刷屏一样输出。使用`/P`参数就会一页一页输出。



##### 2.2.2.8 /T 按时间属性显示

`/T`参数会根据文件的时间属性不同来显示。可包含以下属性参数：

- `C`，创建时间(was Created)。
- `A`，上次访问时间(last Accessed)。
- `W`，上次写入的时间(last Written)，默认使用这个属性。

查看默认的上次写入时间属性：

```sh
$ DIR
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  8,185,208,832 可用字节

$ DIR /T:W
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/06/25  08:45    <DIR>          .
2023/06/25  08:45    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2023/06/22  08:01            18,112 delegatedWebFeatures.sccd
2023/06/22  15:07         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/22  15:08         1,198,016 msedge_proxy.exe
2023/06/22  15:08         1,179,584 pwahelper.exe
2023/06/25  11:17    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  8,185,208,832 可用字节

$
```

可以看到`DIR`与`DIR /T:W`输出结果是一样的！ 可以看到这些文件，大部分都是2023年6月最后写入数据的。



查看创建时间：

```sh
$ DIR /T:C
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2022/12/21  20:05    <DIR>          .
2022/12/21  20:05    <DIR>          ..
2023/06/25  08:45    <DIR>          114.0.1823.58
2022/12/21  20:05            18,112 delegatedWebFeatures.sccd
2022/12/21  20:05         4,113,856 msedge.exe
2022/12/21  20:05               441 msedge.VisualElementsManifest.xml
2022/12/21  20:05         1,198,016 msedge_proxy.exe
2022/12/21  20:05         1,179,584 pwahelper.exe
2022/12/21  20:05    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  8,185,032,704 可用字节

$
```

可以看到这些文件大部分2022年就创建了。



查看上次访问时间：

```sh
$ DIR /T:A
 驱动器 C 中的卷是 Windows
 卷的序列号是 B4E0-3657

 C:\Program Files (x86)\Microsoft\Edge\Application 的目录

2023/11/19  08:26    <DIR>          .
2023/11/19  08:26    <DIR>          ..
2023/11/19  08:26    <DIR>          114.0.1823.58
2023/06/25  08:45            18,112 delegatedWebFeatures.sccd
2023/11/19  08:26         4,113,856 msedge.exe
2023/06/25  08:45               441 msedge.VisualElementsManifest.xml
2023/06/25  08:45         1,198,016 msedge_proxy.exe
2023/06/25  08:45         1,179,584 pwahelper.exe
2023/07/11  15:23    <DIR>          SetupMetrics
               5 个文件      6,510,009 字节
               4 个目录  8,184,672,256 可用字节

$
```

可以看到，访问时间又不一样！



##### 2.2.2.9 递归查找文件

`/S`参数会显示指定目录和所有子目录中的文件，而`/B`参数会仅显示目录和文件的名称。

如果我们要查找当前目录下所有`.exe`可执行文件，可以这样搜索：

```sh
$ DIR *.exe /S /B
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
C:\Program Files (x86)\Microsoft\Edge\Application\msedge_proxy.exe
C:\Program Files (x86)\Microsoft\Edge\Application\pwahelper.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\cookie_exporter.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\elevation_service.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\identity_helper.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\msedge.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\msedgewebview2.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\msedge_proxy.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\msedge_pwa_launcher.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\notification_click_helper.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\notification_helper.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\pwahelper.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\BHO\ie_to_edge_stub.exe
C:\Program Files (x86)\Microsoft\Edge\Application\114.0.1823.58\Installer\setup.exe
```

这样，就查找出了`C:\Program Files (x86)\Microsoft\Edge\Application`目录下的所有`.exe`可执行文件。



使用`DIR`搜索结果：

![](/img/Snipaste_2023-12-03_22-39-52.png)



使用everything搜索结果：



![](/img/Snipaste_2023-12-03_22-40-34.png)

可以看到，搜索结果数量是一致的。



#### 2.2.3 MKDIR/MD创建文件夹

查看帮助信息：

```sh
$ HELP MKDIR
创建目录。

MKDIR [drive:]path
MD [drive:]path

如果命令扩展被启用，MKDIR 会如下改变:

如果需要，MKDIR 会在路径中创建中级目录。例如: 假设 \a 不
存在，那么:

    mkdir \a\b\c\d

与:

    mkdir \a
    chdir \a
    mkdir b
    chdir b
    mkdir c
    chdir c
    mkdir d

相同。如果扩展被停用，则需要键入 mkdir \a\b\c\d。
```

查看当前目录中的文件列表信息：

```sh
# 查看当前目录下的文件列表信息，可以看到没有子文件
$ DIR /B
```

在当前目录下创建多级目录：
```sh
$ MKDIR A\B\C\D
```

再次查看当前目录下的文件列表信息：
```sh
$ DIR /S /B
D:\data\temp\A
D:\data\temp\A\B
D:\data\temp\A\B\C
D:\data\temp\A\B\C\D
```

可以看到，多级目录创建成功了。



参考：

- [How to Use the DIR Command in Windows](https://www.howtogeek.com/363639/how-to-use-the-dir-command-in-windows/)


