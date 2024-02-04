# 搭建简易的HTTP服务

[[toc]]

通过Python自带的模块，可以快速搭建简易的HTTP服务，达达到共享目录的目的。

首先创建一个共享目录：

```sh
# mkdir ~/fastweb
# cd ~/fastweb
```

在目录中创建一些文件或目录，查看文件夹中包含哪些文件：

```sh
# pwd
/root/fastweb
# tree
.
├── backup
│   └── index.html
├── favicon.ico
└── index.html.bak

1 directory, 3 files
```



## 1. Python 2建立HTTP服务

通常Linux服务器都自带了Python 2，我们可以直接使用`SimpleHTTPServer`模块来启动一个HTTP服务。

- `python -m SimpleHTTPServer`,不带端口号，默认监听`8000`端口号。

```sh
# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
```

此时，访问页面 [http://master.hellogitlab.com:8000/](http://master.hellogitlab.com:8000/)：

![](/img/Snipaste_2022-09-05_22-29-21.png) 

可以看到，页面中列出了我们需要共享的文件夹中的文件和文件，我们点击文件就可以下载对应的文件了，这样就可以达到快速共享文件。

如果想停止正在运行有HTTP服务，只需要按`Ctrl + C`取消即可。



- `python -m SimpleHTTPServer 8765`, 指定端口号，此时会监听`8765`端口号。

```sh
# python -m SimpleHTTPServer 8765
Serving HTTP on 0.0.0.0 port 8765 ...
```

此时，访问页面 [http://master.hellogitlab.com:8765/](http://master.hellogitlab.com:8765/)

![](/img/Snipaste_2022-09-05_22-34-24.png)

此时，在后台也可以看到日志信息：

```sh
# python -m SimpleHTTPServer 8765
Serving HTTP on 0.0.0.0 port 8765 ...
171.113.232.78 - - [05/Sep/2022 22:33:27] "GET / HTTP/1.1" 200 -
```

 

## 2. Python 3建立HTTP服务

当你安装了Python 3时，也可以使用Python 3来建立HTTP服务，在Python 3中使用`http.server`模块来建立HTTP服务:

```sh
# 不指定端口号，使用默认8000端口
# python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...

# 指定端口号
# python3 -m http.server 8765
Serving HTTP on 0.0.0.0 port 8765 (http://0.0.0.0:8765/) ...
```

此时，同样也可以通过在浏览器中访问相应的链接，来获取共享文件数据。



## 3. 共享文件夹中有`index.html`文件

当共享文件夹中有`index.html`文件时，会以该文件作为首页：

```sh
# mv index.html.bak index.html
# python3 -m http.server 8765
Serving HTTP on 0.0.0.0 port 8765 (http://0.0.0.0:8765/) ...
```

此时，访问页面 [http://master.hellogitlab.com:8765/](http://master.hellogitlab.com:8765/) 看到的效果如下图所示：

![](/img/Snipaste_2022-09-05_22-42-05.png)

可以看到，此时并没有直接共享文件夹。

查看`index.html`文件内容：

```sh
# cat index.html
<html>
  <head>
    <meta charset="utf-8">
    <link rel="icon" href="favicon.ico">
  </head>
  <body>
   fast web
  </body>
</html>
#
```

 

## 4. 设置快捷命令

当我们经常要使用文件夹共享时，可以设置一个快捷命令，方便自己快速共享。

在`~/.bashrc`中加入以下内容，并使用`source ~/.bashrc`使配置生效：

```sh
alias fastweb2='python -m SimpleHTTPServer'
alias fastweb3='python3 -m http.server'
```

此时，随意使用`fastweb2`或`fastweb3`都可以启动HTTP服务。

```sh
# source ~/.bashrc

# 使用Python 2启动HTTP服务，注意按Ctrl + C取消运行
# fastweb2 8765
Serving HTTP on 0.0.0.0 port 8765 ..

# 使用Python 3启动HTTP服务
# fastweb3 8765
Serving HTTP on 0.0.0.0 port 8765 (http://0.0.0.0:8765/) ...
```

