# Ubuntu初始化配置
[[toc]]

## Ubuntu下一个好用的终端

在终端下输入：


```sh
sudo apt-get install terminator
```

快捷键：

```
shift+ctrl+e      在当前窗口右侧新开一个窗口
shift+ctrl+w      关闭当前活动的窗口
ALT+方向键         实现光标在几个屏中切换
```


## json工具jq的安装

```sh
sudo apt-get install jq
```

## Ubuntu搜狗输入法

参考: https://pinyin.sogou.com/linux/help.php


## WPS

下载： https://www.wps.cn/product/wpslinux


## pycharm

下载: https://www.jetbrains.com/pycharm/download/#section=linux

PyCharm is also available as a snap package. If you’re on Ubuntu 16.04 or later, you can install PyCharm from the command line.

```sh
sudo snap install [pycharm-professional|pycharm-community] --classic
```



## codeblocks

```sh
sudo apt install codeblocks
```

## typora

命令行安装，以下命令都执行即可。


```sh
# or run:
# sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BA300B7755AFCFAE

wget -qO - https://typora.io/linux/public-key.asc | sudo apt-key add -

# add Typora's repository

sudo add-apt-repository 'deb https://typora.io/linux ./'

sudo apt-get update

# install typora

sudo apt-get install typora
```

## atom

```sh
# 首先使用wget获取最新的atom版本。

wget -O atom-amd64.deb https://atom.io/download/deb

# 其次安装gdebi使用：
sudo apt install gdebi-core

# 使用gdebi命令安装atom
sudo gdebi atom-amd64.deb
```

## Foxit Reader 

PDF阅读器安装，https://www.foxitsoftware.cn/pdf-reader/ 下载 安装包。 解压后运行run文件。



## 截图工具

```sh
sudo add-apt-repository ppa:linuxuprising/shutter
sudo apt-get update
sudo apt install shutter
```



## Nefetch

nefetch可以查看系统信息。

```sh
$ sudo add-apt-repository ppa:dawidd0811/neofetch
$ sudo apt-get update
$ sudo apt-get update install neofetch
```

## Unity Tweak 工具

可以尝试新的 GTK 主题、设置桌面热角、自定义图标集、调整 unity 启动器等等。

```sh
$ sudo apt-get install unity-tweak-tool
```

## Guake

```sh
$ sudo apt-get install guake
```
