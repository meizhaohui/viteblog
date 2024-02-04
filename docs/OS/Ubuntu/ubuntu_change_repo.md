# 更改ubuntu国内镜像源

[[toc]]



我们使用docker运行一个ubuntu容器。

```sh
# 启动容器
# docker run --privileged --name ubuntu -it  -d ubuntu /bin/bash
4144e8c22fff58da621d0f39ebef81e890472839e3a868248b53aad0d461ba25
# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
4144e8c22fff        ubuntu              "/bin/bash"         2 seconds ago       Up 1 second                             ubuntu

# 进入到容器
#  docker exec -it  4144e8c22fff /bin/bash
root@4144e8c22fff:/# 
```

我们使用阿里云的镜像站，可以参考[https://developer.aliyun.com/mirror/ubuntu?spm=a2c6h.13651102.0.0.3e221b11TcPF5H](https://developer.aliyun.com/mirror/ubuntu?spm=a2c6h.13651102.0.0.3e221b11TcPF5H)


###  查看ubuntu版本信息

```sh
root@4144e8c22fff:/# cat /etc/issue
Ubuntu 20.04 LTS \n \l
```

即当前版本是`Ubuntu 20.04`。

### 查看默认配置`/etc/apt/sources.list`


```sh
root@4144e8c22fff:/# cat /etc/apt/sources.list
# See http://help.ubuntu.com/community/UpgradeNotes for how to upgrade to
# newer versions of the distribution.
deb http://archive.ubuntu.com/ubuntu/ focal main restricted
# deb-src http://archive.ubuntu.com/ubuntu/ focal main restricted

## Major bug fix updates produced after the final release of the
## distribution.
deb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted
# deb-src http://archive.ubuntu.com/ubuntu/ focal-updates main restricted

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team. Also, please note that software in universe WILL NOT receive any
## review or updates from the Ubuntu security team.
deb http://archive.ubuntu.com/ubuntu/ focal universe
# deb-src http://archive.ubuntu.com/ubuntu/ focal universe
deb http://archive.ubuntu.com/ubuntu/ focal-updates universe
# deb-src http://archive.ubuntu.com/ubuntu/ focal-updates universe

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team, and may not be under a free licence. Please satisfy yourself as to
## your rights to use the software. Also, please note that software in
## multiverse WILL NOT receive any review or updates from the Ubuntu
## security team.
deb http://archive.ubuntu.com/ubuntu/ focal multiverse
# deb-src http://archive.ubuntu.com/ubuntu/ focal multiverse
deb http://archive.ubuntu.com/ubuntu/ focal-updates multiverse
# deb-src http://archive.ubuntu.com/ubuntu/ focal-updates multiverse

## N.B. software from this repository may not have been tested as
## extensively as that contained in the main release, although it includes
## newer versions of some applications which may provide useful features.
## Also, please note that software in backports WILL NOT receive any review
## or updates from the Ubuntu security team.
deb http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse
# deb-src http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse

## Uncomment the following two lines to add software from Canonical's
## 'partner' repository.
## This software is not part of Ubuntu, but is offered by Canonical and the
## respective vendors as a service to Ubuntu users.
# deb http://archive.canonical.com/ubuntu focal partner
# deb-src http://archive.canonical.com/ubuntu focal partner

deb http://security.ubuntu.com/ubuntu/ focal-security main restricted
# deb-src http://security.ubuntu.com/ubuntu/ focal-security main restricted
deb http://security.ubuntu.com/ubuntu/ focal-security universe
# deb-src http://security.ubuntu.com/ubuntu/ focal-security universe
deb http://security.ubuntu.com/ubuntu/ focal-security multiverse
# deb-src http://security.ubuntu.com/ubuntu/ focal-security multiverse
```

实质是起作用的配置行内容：

```sh
root@4144e8c22fff:/# cat /etc/apt/sources.list|grep -v '^#'|awk NF
deb http://archive.ubuntu.com/ubuntu/ focal main restricted
deb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted
deb http://archive.ubuntu.com/ubuntu/ focal universe
deb http://archive.ubuntu.com/ubuntu/ focal-updates universe
deb http://archive.ubuntu.com/ubuntu/ focal multiverse
deb http://archive.ubuntu.com/ubuntu/ focal-updates multiverse
deb http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ focal-security main restricted
deb http://security.ubuntu.com/ubuntu/ focal-security universe
deb http://security.ubuntu.com/ubuntu/ focal-security multiverse
```

### 修改配置文件

备份配置文件：

```sh
root@4144e8c22fff:/# cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

在配置文件中写入阿里云的镜像源内容：

```
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
```

写入命令：

```sh
cat > /etc/apt/sources.list << EOF
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
EOF
```

```sh
root@4144e8c22fff:/# cat > /etc/apt/sources.list << EOF
> deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
> deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
>
> deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
> deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
>
> deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
> deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
>
> deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
> deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
>
> deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
> deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
> EOF
```


修改后的内容如下：

```sh
root@4144e8c22fff:/# cat /etc/apt/sources.list
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
root@4144e8c22fff:/#
```

### 更新

```sh
root@4144e8c22fff:/# apt-get update
Get:1 http://mirrors.aliyun.com/ubuntu focal InRelease [265 kB]
Get:2 http://mirrors.aliyun.com/ubuntu focal-security InRelease [101 kB]
Get:3 http://mirrors.aliyun.com/ubuntu focal-updates InRelease [97.0 kB]
Get:4 http://mirrors.aliyun.com/ubuntu focal-proposed InRelease [265 kB]
Get:5 http://mirrors.aliyun.com/ubuntu focal-backports InRelease [89.2 kB]
Get:6 http://mirrors.aliyun.com/ubuntu focal/restricted Sources [7198 B]
Get:7 http://mirrors.aliyun.com/ubuntu focal/main Sources [1079 kB]
Get:8 http://mirrors.aliyun.com/ubuntu focal/multiverse Sources [208 kB]
Get:9 http://mirrors.aliyun.com/ubuntu focal/universe Sources [12.3 MB]
Get:10 http://mirrors.aliyun.com/ubuntu focal/restricted amd64 Packages [33.4 kB]
Get:11 http://mirrors.aliyun.com/ubuntu focal/main amd64 Packages [1275 kB]
Get:12 http://mirrors.aliyun.com/ubuntu focal/multiverse amd64 Packages [177 kB]
Get:13 http://mirrors.aliyun.com/ubuntu focal/universe amd64 Packages [11.3 MB]
Get:14 http://mirrors.aliyun.com/ubuntu focal-security/universe Sources [1020 B]
Get:15 http://mirrors.aliyun.com/ubuntu focal-security/main Sources [6585 B]
Get:16 http://mirrors.aliyun.com/ubuntu focal-security/restricted Sources [880 B]
Get:17 http://mirrors.aliyun.com/ubuntu focal-security/restricted amd64 Packages [2843 B]
Get:18 http://mirrors.aliyun.com/ubuntu focal-security/universe amd64 Packages [2298 B]
Get:19 http://mirrors.aliyun.com/ubuntu focal-security/main amd64 Packages [22.9 kB]
Get:20 http://mirrors.aliyun.com/ubuntu focal-updates/main Sources [9740 B]
Get:21 http://mirrors.aliyun.com/ubuntu focal-updates/universe Sources [1020 B]
Get:22 http://mirrors.aliyun.com/ubuntu focal-updates/restricted Sources [880 B]
Get:23 http://mirrors.aliyun.com/ubuntu focal-updates/main amd64 Packages [30.1 kB]
Get:24 http://mirrors.aliyun.com/ubuntu focal-updates/universe amd64 Packages [5652 B]
Get:25 http://mirrors.aliyun.com/ubuntu focal-updates/restricted amd64 Packages [2843 B]
Get:26 http://mirrors.aliyun.com/ubuntu focal-proposed/universe Sources [8699 B]
Get:27 http://mirrors.aliyun.com/ubuntu focal-proposed/restricted Sources [1181 B]
Get:28 http://mirrors.aliyun.com/ubuntu focal-proposed/main Sources [20.5 kB]
Get:29 http://mirrors.aliyun.com/ubuntu focal-proposed/main amd64 Packages [69.1 kB]
Get:30 http://mirrors.aliyun.com/ubuntu focal-proposed/restricted amd64 Packages [3190 B]
Get:31 http://mirrors.aliyun.com/ubuntu focal-proposed/universe amd64 Packages [41.8 kB]
Fetched 27.5 MB in 6s (4742 kB/s)
Reading package lists... Done
```

