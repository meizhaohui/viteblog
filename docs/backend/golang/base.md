# Go的基本使用

[[toc]]

本文用于记录学习Golang相关知识点。

Go编程语言中文文档中介绍Go:

- Go编程语言是一个开源项目，它使程序员更具生产力。

- Go语言具有很强的表达能力，它简洁、清晰而高效。得益于其并发机制，用它编写的程序能够非常有效地利用多核与联网的计算机，其新颖的类型系统则使程序结构变得灵活而模块化。Go代码编译成机器码不仅非常迅速，还具有方便的垃圾收集机制和强大的运行时反射机制。 它是一个快速的、静态类型的编译型语言，感觉却像动态类型的解释型语言。


我们可以简单的理解Go语言解决了其他语言并发执行的痛点，像C语言一样的运行效率高，又兼容了Python语言的开发速度快的特点，`Go = C + Python`, Go语言被称为"互联网时代的C"。我们不在概念上过多的纠结，直接来开始使用Go这门编程语言。

## 特别说明

- 本文档中`Golang`简写为`Go`。
- 本文档假定您会使用Linux操作系统的基本命令，如vim、cat、ls等一些工具。
- `Go`学习网站：官方文档[https://golang.google.cn/doc/](https://golang.google.cn/doc/)
- `Go`学习网站：Go编程语言中文文档[https://go-zh.org/doc/](https://go-zh.org/doc/)
- `Go`学习网站：Go语言之旅[https://go-tour-zh.appspot.com/list](https://go-tour-zh.appspot.com/list)
- `Go`学习网站：实效Go编程[https://go-zh.org/doc/effective_go.html](https://go-zh.org/doc/effective_go.html)
- `Go`学习网站：Go编程语言规范[https://go-zh.org/ref/spec](https://go-zh.org/ref/spec)


## 实验环境

本实验使用CentOS7.6作为实验环境。

```sh
[root@hellogitlab ~]# cat /etc/centos-release
CentOS Linux release 7.6.1810 (Core)
```

## 安装和配置GO环境

### 安装Golang

- 使用`yum install go -y`安装Golang。

```sh
[root@hellogitlab ~]# yum install go -y
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package golang.x86_64 0:1.13.1-1.el7 will be updated
--> Processing Dependency: go = 1.13.1-1.el7 for package: golang-bin-1.13.1-1.el7.x86_64
---> Package golang.x86_64 0:1.13.3-1.el7 will be an update
--> Processing Dependency: golang-src = 1.13.3-1.el7 for package: golang-1.13.3-1.el7.x86_64
--> Running transaction check
---> Package golang-bin.x86_64 0:1.13.1-1.el7 will be updated
---> Package golang-bin.x86_64 0:1.13.3-1.el7 will be an update
---> Package golang-src.noarch 0:1.13.1-1.el7 will be updated
---> Package golang-src.noarch 0:1.13.3-1.el7 will be an update
--> Finished Dependency Resolution

Dependencies Resolved

=================================================================================================================================================
 Package                             Arch                            Version                                 Repository                     Size
=================================================================================================================================================
Updating:
 golang                              x86_64                          1.13.3-1.el7                            epel                          694 k
Updating for dependencies:
 golang-bin                          x86_64                          1.13.3-1.el7                            epel                           86 M
 golang-src                          noarch                          1.13.3-1.el7                            epel                          7.1 M

Transaction Summary
=================================================================================================================================================
Upgrade  1 Package (+2 Dependent packages)

Total download size: 93 M
Downloading packages:
epel/7/x86_64/prestodelta                                                                                                 | 1.0 kB  00:00:00     
(1/3): golang-1.13.3-1.el7.x86_64.rpm                                                                                     | 694 kB  00:00:00     
(2/3): golang-src-1.13.3-1.el7.noarch.rpm                                                                                 | 7.1 MB  00:00:00     
(3/3): golang-bin-1.13.3-1.el7.x86_64.rpm                                                                                 |  86 MB  00:00:03     
-------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                             29 MB/s |  93 MB  00:00:03     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Updating   : golang-src-1.13.3-1.el7.noarch                                                                                                1/6 
  Updating   : golang-bin-1.13.3-1.el7.x86_64                                                                                                2/6 
  Updating   : golang-1.13.3-1.el7.x86_64                                                                                                    3/6 
  Cleanup    : golang-bin-1.13.1-1.el7.x86_64                                                                                                4/6 
  Cleanup    : golang-1.13.1-1.el7.x86_64                                                                                                    5/6 
  Cleanup    : golang-src-1.13.1-1.el7.noarch                                                                                                6/6 
  Verifying  : golang-src-1.13.3-1.el7.noarch                                                                                                1/6 
  Verifying  : golang-1.13.3-1.el7.x86_64                                                                                                    2/6 
  Verifying  : golang-bin-1.13.3-1.el7.x86_64                                                                                                3/6 
  Verifying  : golang-1.13.1-1.el7.x86_64                                                                                                    4/6 
  Verifying  : golang-bin-1.13.1-1.el7.x86_64                                                                                                5/6 
  Verifying  : golang-src-1.13.1-1.el7.noarch                                                                                                6/6 

Updated:
  golang.x86_64 0:1.13.3-1.el7                                                                                                                   

Dependency Updated:
  golang-bin.x86_64 0:1.13.3-1.el7                                        golang-src.noarch 0:1.13.3-1.el7                                       

Complete!
```

### 查看Golang版本

```sh
[root@hellogitlab ~]# go version
go version go1.13.3 linux/amd64
```

### 查看`go`命令的帮助信息

```sh
[root@hellogitlab ~]# go
Go is a tool for managing Go source code.

Usage:

        go <command> [arguments]

The commands are:

        bug         start a bug report
        build       compile packages and dependencies
        clean       remove object files and cached files
        doc         show documentation for package or symbol
        env         print Go environment information
        fix         update packages to use new APIs
        fmt         gofmt (reformat) package sources
        generate    generate Go files by processing source
        get         add dependencies to current module and install them
        install     compile and install packages and dependencies
        list        list packages or modules
        mod         module maintenance
        run         compile and run Go program
        test        test packages
        tool        run specified go tool
        version     print Go version
        vet         report likely mistakes in packages

Use "go help <command>" for more information about a command.

Additional help topics:

        buildmode   build modes
        c           calling between Go and C
        cache       build and test caching
        environment environment variables
        filetype    file types
        go.mod      the go.mod file
        gopath      GOPATH environment variable
        gopath-get  legacy GOPATH go get
        goproxy     module proxy protocol
        importpath  import path syntax
        modules     modules, module versions, and more
        module-get  module-aware go get
        module-auth module authentication using go.sum
        module-private module configuration for non-public modules
        packages    package lists and patterns
        testflag    testing flags
        testfunc    testing functions

Use "go help <topic>" for more information about that topic.
```

### go安装信息检查

```sh
# 查看go处于什么位置
[root@hellogitlab ~]# whereis go
go: /usr/bin/go /usr/lib/golang/bin/go
# 查看/usr/bin/go的详细信息，可以看到最终指向了/usr/lib/golang/bin/go
[root@hellogitlab ~]# ls -lah /usr/bin/go
lrwxrwxrwx 1 root root 20 Nov 22 22:36 /usr/bin/go -> /etc/alternatives/go
[root@hellogitlab ~]# ls -lah /etc/alternatives/go
lrwxrwxrwx 1 root root 22 Nov 22 22:36 /etc/alternatives/go -> /usr/lib/golang/bin/go
[root@hellogitlab ~]# ls -lah /usr/lib/golang/bin/go
-rwxr-xr-x 1 root root 15M Nov  3 03:34 /usr/lib/golang/bin/go
# golang的安装目录
[root@hellogitlab ~]# ls -lah /usr/lib/golang/
total 44K
drwxr-xr-x   7 root root 4.0K Nov 22 22:36 .
dr-xr-xr-x. 44 root root 4.0K Nov 20 00:06 ..
drwxr-xr-x   2 root root 4.0K Nov 22 22:36 api
drwxr-xr-x   2 root root 4.0K Nov 22 22:35 bin
-rw-r--r--   1 root root 5.6K Oct 18 06:02 favicon.ico
drwxr-xr-x   3 root root 4.0K Oct 18 06:02 lib
drwxr-xr-x   8 root root 4.0K Nov  3 03:35 pkg
-rw-r--r--   1 root root   26 Oct 18 06:02 robots.txt
drwxr-xr-x  46 root root 4.0K Nov 22 22:35 src
-rw-r--r--   1 root root    8 Oct 18 06:02 VERSION
```

我们后续使用普通账户`meizhaohui`来进行go语言相关命令的操作。

### 配置Go的工作空间

GO代码必须在工作空间内。工作空间是一个目录，其中包含三个子目录：
- `src` 里面每一个子目录，就是一个包。包内是Go的源码文件
- `pkg` 编译后生成的，包的目标文件
- `bin` 生成的可执行文件


使用普通账户`meizhaohui`创建Go的工作空间目录：

```sh
# 查看我是谁
[meizhaohui@hellogitlab ~]$ whoami
meizhaohui
# 查看当前文件夹中的文件
[meizhaohui@hellogitlab ~]$ ls
# 创建工作空间目录
[meizhaohui@hellogitlab ~]$ mkdir -p data/go_data
[meizhaohui@hellogitlab ~]$ ls -lsh data/
total 4.0K
4.0K drwxrwxr-x 2 meizhaohui meizhaohui 4.0K Nov 22 23:02 go_data
# 在工作空间目录下面创建子目录
[meizhaohui@hellogitlab ~]$ mkdir -p data/go_data/{src,bin,pkg}
[meizhaohui@hellogitlab ~]$ ls -lah data/go_data/
total 20K
drwxrwxr-x 5 meizhaohui meizhaohui 4.0K Nov 22 23:10 .
drwxrwxr-x 3 meizhaohui meizhaohui 4.0K Nov 22 23:02 ..
drwxrwxr-x 2 meizhaohui meizhaohui 4.0K Nov 22 23:10 bin
drwxrwxr-x 2 meizhaohui meizhaohui 4.0K Nov 22 23:10 pkg
drwxrwxr-x 2 meizhaohui meizhaohui 4.0K Nov 22 23:10 src
```

### 配置`PATH`、`GOPATH`、`GOROOT`、`GOBIN`等环境变量

在`~/.bashrc`文件中增加以下内容：

```
# Golang environment settings
export GOROOT=/usr/lib/golang # golang install path
export GOPATH=/home/meizhaohui/data/go_data # golang workspace
export GOBIN=${GOPATH}/bin # golang exe files
export PATH=${GOBIN}:${PATH}
```

保存后，`source ~/.bashrc`加载配置文件，并查看以上设置的Go语言的环境变量：

```sh
[meizhaohui@hellogitlab ~]$ source ~/.bashrc
[meizhaohui@hellogitlab ~]$ echo $GOPATH
/home/meizhaohui/data/go_data
[meizhaohui@hellogitlab ~]$ echo $GOBIN
/home/meizhaohui/data/go_data/bin
[meizhaohui@hellogitlab ~]$ echo $GOROOT
/usr/lib/golang
[meizhaohui@hellogitlab ~]$ echo $PATH
/home/meizhaohui/data/go_data/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/meizhaohui/.local/bin:/home/meizhaohui/bin
```

查看到以上信息，说环境变量配置成功。

### 开启Go module和代理

默认情况下，使用go get下载包时会非常慢，需要开启Go module和代理，加快我们包的安装速度。

为了今后中国的Go语言开发者能更好地进行开发，七牛云推出了非营利性项目 goproxy.cn，其目标是为中国和世界上其他地方的 Gopher 们提供一个免费的、可靠的、持续在线的且经过 CDN 加速的模块代理。

参考：
- 干货满满的 Go Modules 和 goproxy.cn [https://github.com/EDDYCJY/blog/blob/master/talk/goproxy-cn.md](https://github.com/EDDYCJY/blog/blob/master/talk/goproxy-cn.md)
- Go module和goproxy 设置[https://luhua.cc/2019/08/23/Go-module-%E5%92%8C-goproxy-%E8%AE%BE%E7%BD%AE/](https://luhua.cc/2019/08/23/Go-module-%E5%92%8C-goproxy-%E8%AE%BE%E7%BD%AE/)

在`~/.bashrc`文件中增加以下内容：

```sh
export GO111MODULE=on
export GOPROXY=https://goproxy.cn
```

保存后，`source ~/.bashrc`加载配置文件，并查看以上设置的Go语言的环境变量：

```sh
[meizhaohui@hellogitlab ~]$ echo $GO111MODULE
on
[meizhaohui@hellogitlab ~]$ echo $GOPROXY 
https://goproxy.cn

# 测试安装包
[meizhaohui@hellogitlab ~]$ go get -v github.com/stamblerre/gocode
```


## 第一个Go程序，你好世界

### 编写Go代码文件
以最经典的`Hello world`程序为例，编写第一个Go代码文件。

我们切换到`$GOPATH/src`目录中，创建第一个Go代码文件。

```sh
[meizhaohui@hellogitlab ~]$ cd $GOPATH/src
[meizhaohui@hellogitlab src]$ pwd
/home/meizhaohui/data/go_data/src
# 使用vim编写hello.go文件，保存后查看内容如下
[meizhaohui@hellogitlab src]$ cat hello.go
package main

import "fmt"

func main() {
    fmt.Println("Hello,World")
}
```

### 编译Go程序`go build`

- 使用`go build filename.go`编译go程序，如`go build hello.go`编译生成可执行文件`hello`。

```sh
[meizhaohui@hellogitlab src]$ go build hello.go 
[meizhaohui@hellogitlab src]$ ls
hello  hello.go
# 运行可执行文件hello
[meizhaohui@hellogitlab src]$ ./hello
Hello,World
```

### 编译并直接运行Go程序`go run`

- 使用`go run filename.go`编译并直接运行go程序，如`go build hello.go`编译时不生成可执行文件，直接显示运行结果。

```sh
[meizhaohui@hellogitlab src]$ trash-put hello
[meizhaohui@hellogitlab src]$ ls
hello.go
[meizhaohui@hellogitlab src]$ go run hello.go
Hello,World
[meizhaohui@hellogitlab src]$ ls
hello.go
```

### 编译并安装`go install`
- 对go源码文件`go install`,会进行编译+链接+生成可执行文件, 会在`$GOBIN`目录下生成可执行文件。

```sh
# 编译并安装
[meizhaohui@hellogitlab src]$ go install hello.go
# 查看当前目录下是否生成可执行文件
[meizhaohui@hellogitlab src]$ ls 
hello.go
# 查看bin目录下是否生成可执行文件
[meizhaohui@hellogitlab src]$ ls $GOBIN
hello
# 查看hello可执行文件的位置
[meizhaohui@hellogitlab src]$ whereis hello
hello: /home/meizhaohui/data/go_data/bin/hello
# 在任何目录执行hello，会打印出世界你好
[meizhaohui@hellogitlab src]$ hello
Hello,World
[meizhaohui@hellogitlab src]$ cd
[meizhaohui@hellogitlab ~]$ hello
Hello,World
```

