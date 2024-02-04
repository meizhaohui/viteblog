
# linux下安装htop

[[toc]]

`htop`是Linux系统中的一个互动的进程查看器。

## 下载源文件


htop下载地址：[http://hisham.hm/htop/index.php?page=downloads#binaries](http://hisham.hm/htop/index.php?page=downloads#binaries)

## 添加镜像源

参考： [https://fedoraproject.org/wiki/EPEL](https://fedoraproject.org/wiki/EPEL)
```sh
# yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
```

## 安装htop

```sh
# yum install htop -y
```


## 使用htop

```sh
# 查看htop版本信息
[meizhaohui@localhost ~]$ htop --version
htop 2.2.0 - (C) 2004-2019 Hisham Muhammad
Released under the GNU GPL.

# 查看htop帮助信息
[meizhaohui@localhost ~]$ htop --help
htop 2.2.0 - (C) 2004-2019 Hisham Muhammad
Released under the GNU GPL.

-C --no-color               Use a monochrome color scheme
-d --delay=DELAY            Set the delay between updates, in tenths of seconds
-h --help                   Print this help screen
-s --sort-key=COLUMN        Sort by COLUMN (try --sort-key=help for a list)
-t --tree                   Show the tree view by default
-u --user=USERNAME          Show only processes of a given user
-p --pid=PID,[,PID,PID...]  Show only the given PIDs
-v --version                Print version info

Long options may be passed with a single dash.

Press F1 inside htop for online help.
See 'man htop' for more information.
[meizhaohui@localhost ~]$
```

htop查看进程示例：

![htop_graph.gif](/img/htop_graph.gif)
