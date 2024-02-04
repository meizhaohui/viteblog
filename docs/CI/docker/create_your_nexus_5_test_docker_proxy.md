# 搭建自己的nexus私有仓库5--测试docker仓库pull和push

[[toc]]

本文档是nexus系列课程第5篇。
- nexus系列课程第1篇，请参考 [搭建自己的nexus私有仓库1--nexus初体验](./create_your_nexus.md)
- nexus系列课程第2篇，请参考 [搭建自己的nexus私有仓库2--创建python pypi代理](./create_your_nexus_2.md)
- nexus系列课程第3篇，请参考 [搭建自己的nexus私有仓库3--创建yum ius代理](./create_your_nexus_3.md)
- nexus系列课程第4篇，请参考 [搭建自己的nexus私有仓库4--创建docker私有仓库](./create_your_nexus_4_docker_proxy.md)


第4篇中，已经使用nexus创建docker代理仓库(proxy)、本地仓库(hosted)和聚合仓库(group)，并尝试通过HTTP方式从代理仓库下载镜像，并且可以正常下载镜像。

本文计划做以下事情：

- 使用HTTP形式，分别测试从代理仓库、本地仓库、聚合仓库下载镜像，构建镜像并上传到私有仓库。
- ~~使用HTTPS形式，配置nginx反向代理，从代理仓库下载镜像，构建镜像并上传到私有仓库。（下一篇再处理。）~~


以下是实验环境：


| 主机 | IP            | 主机名 | 操作系统        | docker版本 | 自定义域名   |
|------|---------------|--------|:----------------|:-----------|:-------------|
| 1    | 192.168.56.11 | nexus  | CentOS 7.6.1810 | 20.10.5    | nexushub.com |
| 2    | 192.168.56.12 | master | CentOS 7.6.1810 | 20.10.5    |              |


## 0. 准备工作

请在主机2以及你的电脑上面配置域名解析：

```sh
[root@master ~]# tail -n 1 /etc/hosts
192.168.56.11 nexushub.com
```

注意，实际操作时，请将`192.168.56.11`替换成你服务器的内网IP或者公网IP，`nexushub.com`替换成你想使用的域名。



## 1. 前情回顾

我们在[搭建自己的nexus私有仓库4--创建docker私有仓库](./create_your_nexus_4_docker_proxy.md) 中是使用的以下命令启动nexus容器：


```sh
[root@nexus ~]# docker run -d --restart always -p 8081:8081 -p 8001-8003:8001-8003  -v /some/dir/nexus-data:/nexus-data --name nexus sonatype/nexus3:3.59.0
8b931229efd4a2749a16342b149901a74674ec5b771591a808baebc744ebcdc4
[root@nexus ~]# docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS                                                      NAMES
8b931229efd4   sonatype/nexus3:3.59.0   "/opt/sonatype/nexus…"   4 seconds ago   Up 3 seconds   0.0.0.0:8001-8003->8001-8003/tcp, 0.0.0.0:8081->8081/tcp   nexus
[root@nexus ~]# netstat -tunlp|grep docker
tcp        0      0 0.0.0.0:8081            0.0.0.0:*               LISTEN      24765/docker-proxy
tcp        0      0 0.0.0.0:8001            0.0.0.0:*               LISTEN      24801/docker-proxy
tcp        0      0 0.0.0.0:8002            0.0.0.0:*               LISTEN      24789/docker-proxy
tcp        0      0 0.0.0.0:8003            0.0.0.0:*               LISTEN      24777/docker-proxy
[root@nexus ~]#
```

可以看到，除了管理端口8081监听了，8001、8002和8003端口也监听了。


## 2. docker仓库规划

在Nexus3中支持3种Docker仓库：

- `hosted`：本地仓库，同Docker官方仓库一样。
- `proxy`：代理仓库，提供代理其他仓库的功能，如我内网只有一台主机能上网，其他主机不能上网，则可以在可以上网的主机上面配置这种代理仓库，然后别的不能上网的主机就可以通过该代理仓库下载docker镜像了。
- `group`：聚合仓库，将多个仓库组合成一个仓库。

我需要配置这三种类型的仓库，现规划如下：


| 仓库类型       | 仓库名称      | HTTP端口号 | HTTPS端口号 | 支持docker操作 |
|----------------|:--------------|------------|-------------|:---------------|
| proxy代理仓库  | docker-proxy  | 8001       | 不设置      | pull           |
| hosted本地仓库 | docker-hosted | 8002       | 不设置      | pull、push      |
| group聚合仓库  | docker-group  | 8003       | 不设置      | pull           |


## 3. 测试docker仓库pull和push


### 3.1 测试docker-proxy代理仓库

#### 3.1.1 测试docker-proxy代理仓库的pull
先修改`/etc/docker/daemon.json`配置：

```sh
[root@master ~]# cd /etc/docker/

# 备份
[root@master docker]# cp -p daemon.json daemon.json.20240124.bak

# 修改配置文件
[root@master docker]# vi daemon.json

# 查看配置文件内容
[root@master docker]# cat daemon.json
{
    "insecure-registries":[
        "nexushub.com:8001"
    ],
    "registry-mirrors":[
        "http://nexushub.com:8001"
    ],
    "data-root": "/data/docker"
}
[root@master docker]#
```

注意，跟nexushub.com相关的是我新加的。


重启docker服务：

```sh
[root@master ~]# systemctl restart docker
```

再次查看docker信息：

```sh
[root@master ~]# docker info|tail -n 7
 Insecure Registries:
  nexushub.com:8001
  127.0.0.0/8
 Registry Mirrors:
  http://nexushub.com:8001/
 Live Restore Enabled: false

[root@master ~]#
```

可以看到，现在只使用docker-proxy代理仓库进行加速。

然后下载镜像：
```sh
# 下载alpine镜像指定版本
[root@master ~]# docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
[root@master ~]# docker pull alpine:3.19
3.19: Pulling from library/alpine
661ff4d9561e: Pull complete
Digest: sha256:51b67269f354137895d43f3b3d810bfacd3945438e94dc5ac55fdac340352f48
Status: Downloaded newer image for alpine:3.19
docker.io/library/alpine:3.19
[root@master ~]# date
Wed Jan 24 21:37:13 CST 2024
[root@master ~]#
```

可以看到，能够正常下载。

![](/img/Snipaste_2024-01-24_21-38-45.png)
并且在Browse浏览器界面也可以看到刚才下载的镜像信息，对应的alpine镜像版本是3.19，所使用的仓库，容器仓库Containing repo是`docker-proxy`代理仓库。

#### 3.1.2 测试docker-proxy代理仓库的push

参考 [https://hub-stage.docker.com/_/alpine](https://hub-stage.docker.com/_/alpine) 来构建一个本地镜像，并尝试push到仓库中。

创建构建mysql镜像的文件夹和Dockerfile文件：
```sh
[root@master ~]# mkdir mysql
[root@master ~]# cd mysql/
[root@master mysql]# vi Dockerfile
[root@master mysql]# cat Dockerfile
FROM alpine:3.9
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk add --update mysql-client \
    && rm -rf /var/cache/apk/*
ENTRYPOINT ["mysql"]

[root@master mysql]#
```
参考： [Alpine 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/alpine/) 

使用`sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories` 加速alpine软件包安装。

构建镜像：

```sh
[root@master mysql]# docker build --tag mysql-client:proxy .
Sending build context to Docker daemon  2.048kB
Step 1/3 : FROM alpine:3.9
3.9: Pulling from library/alpine
31603596830f: Pull complete
Digest: sha256:414e0518bb9228d35e4cd5165567fb91d26c6a214e9c95899e1e056fcd349011
Status: Downloaded newer image for alpine:3.9
 ---> 78a2ce922f86
Step 2/3 : RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories     && apk add --update mysql-client     && rm -rf /var/cache/apk/*
 ---> Running in 2108c31c0b42
fetch http://mirrors.tuna.tsinghua.edu.cn/alpine/v3.9/main/x86_64/APKINDEX.tar.gz
fetch http://mirrors.tuna.tsinghua.edu.cn/alpine/v3.9/community/x86_64/APKINDEX.tar.gz
(1/8) Installing mariadb-common (10.3.25-r0)
(2/8) Installing ncurses-terminfo-base (6.1_p20190105-r0)
(3/8) Installing ncurses-terminfo (6.1_p20190105-r0)
(4/8) Installing ncurses-libs (6.1_p20190105-r0)
(5/8) Installing libgcc (8.3.0-r0)
(6/8) Installing libstdc++ (8.3.0-r0)
(7/8) Installing mariadb-client (10.3.25-r0)
(8/8) Installing mysql-client (10.3.25-r0)
Executing busybox-1.29.3-r10.trigger
OK: 45 MiB in 22 packages
Removing intermediate container 2108c31c0b42
 ---> 12f6f9a7c8b9
Step 3/3 : ENTRYPOINT ["mysql"]
 ---> Running in 2de87bfa1035
Removing intermediate container 2de87bfa1035
 ---> f326dd608a3f
Successfully built f326dd608a3f
Successfully tagged mysql-client:proxy
[root@master mysql]#
```

查看镜像：

```sh
[root@master ~]# docker images
REPOSITORY     TAG       IMAGE ID       CREATED         SIZE
mysql-client   proxy     f326dd608a3f   8 minutes ago   41.1MB
alpine         3.19      f8c20f8bbcb6   6 weeks ago     7.38MB
alpine         3.9       78a2ce922f86   3 years ago     5.55MB
[root@master ~]#
```
重新打标签并上传镜像：

```sh
重新打标签
[root@master ~]# docker tag mysql-client:proxy nexushub.com:8001/mysql-client:proxy
[root@master ~]# docker images
REPOSITORY                       TAG       IMAGE ID       CREATED          SIZE
mysql-client                     proxy     f326dd608a3f   16 minutes ago   41.1MB
nexushub.com:8001/mysql-client   proxy     f326dd608a3f   16 minutes ago   41.1MB
alpine                           3.19      f8c20f8bbcb6   6 weeks ago      7.38MB
alpine                           3.9       78a2ce922f86   3 years ago      5.55MB

# 登陆
[root@master ~]# docker login http://nexushub.com:8001
Username: admin
Password:
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

# 上传
[root@master ~]# docker push nexushub.com:8001/mysql-client:proxy
The push refers to repository [nexushub.com:8001/mysql-client]
55af1c19d0db: Preparing
89ae5c4ee501: Preparing
error parsing HTTP 404 response body: invalid character '<' looking for beginning of value: "\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <title>404 - Sonatype Nexus Repository</title>\n  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>\n\n\n  <link rel=\"icon\" type=\"image/png\" href=\"../../../../../../static/rapture/resources/safari-favicon-32x32.png?3.59.0-01\" sizes=\"32x32\">\n  <link rel=\"mask-icon\" href=\"../../../../../../static/rapture/resources/favicon-white.svg?3.59.0-01\" color=\"#00bb6c\">\n  <link rel=\"icon\" type=\"image/png\" href=\"../../../../../../static/rapture/resources/favicon.svg?3.59.0-01\" sizes=\"16x16\">\n\n  <link rel=\"stylesheet\" type=\"text/css\" href=\"../../../../../../static/css/nexus-content.css?3.59.0-01\"/>\n</head>\n<body>\n<div class=\"nexus-header\">\n  <a href=\"../../../../../..\">\n    <div class=\"product-logo\">\n      <img src=\"../../../../../../static/rapture/resources/nxrm-reverse-icon.png?3.59.0-01\" alt=\"Product logo\"/>\n    </div>\n    <div class=\"product-id\">\n      <div class=\"product-id__line-1\">\n        <span class=\"product-name\">Sonatype Nexus Repository</span>\n      </div>\n      <div class=\"product-id__line-2\">\n        <span class=\"product-spec\">OSS 3.59.0-01</span>\n      </div>\n    </div>\n  </a>\n</div>\n\n<div class=\"nexus-body\">\n  <div class=\"content-header\">\n    <img src=\"../../../../../../static/rapture/resources/icons/x32/exclamation.png?3.59.0-01\" alt=\"Exclamation point\" aria-role=\"presentation\"/>\n    <span class=\"title\">Error 404</span>\n    <span class=\"description\">Not Found</span>\n  </div>\n  <div class=\"content-body\">\n    <div class=\"content-section\">\n      Not Found\n    </div>\n  </div>\n</div>\n</body>\n</html>\n\n"
[root@master ~]#

```

此处，我们不管构建的镜像能不能正常运行，只看镜像能不能正常push上传，可以看到上传镜像失败了。


#### 3.1.3 测试docker-proxy代理仓库的search功能

可以使用`docker search`搜索镜像：

```sh
[root@master ~]# docker search alpine
NAME                               DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
alpine                             A minimal Docker image based on Alpine Linux…   10627     [OK]
alpinelinux/unbound                                                                11
alpinelinux/docker-cli             Simple and lightweight Alpine Linux image wi…   10
alpinelinux/ansible                Ansible in docker                               9
grafana/alpine                     Alpine Linux with ca-certificates package in…   7
alpinelinux/gitlab-runner-helper   Helper image container gitlab-runner-helper …   6
alpinelinux/gitlab-runner          Alpine Linux gitlab-runner (supports more ar…   5
alpinelinux/alpine-gitlab-ci       Build Alpine Linux packages with Gitlab CI      3
alpinelinux/golang                 Build container for golang based on Alpine L…   2
alpinelinux/docker-compose         docker-compose image based on Alpine Linux      2
alpinelinux/rsyncd                                                                 2
alpinelinux/darkhttpd                                                              2
kasmweb/alpine-317-desktop         Alpine 3.17 desktop for Kasm Workspaces         1
alpinelinux/package-builder        Container to build packages for a repository    1
alpinelinux/apkbuild-lint-tools    Tools for linting APKBUILD files in a CI env…   0
alpinelinux/alpine-docker-gitlab   Gitlab running on Alpine Linux                  0
alpinelinux/docker-abuild          Dockerised abuild                               0
alpinelinux/build-base             Base image suitable for building packages wi…   0
alpinelinux/alpine-www             The Alpine Linux public website (www.alpinel…   0
alpinelinux/turbo-paste            Alpine Linux paste service                      0
alpinelinux/mqtt-exec                                                              0
alpinelinux/alpine-drone-ci        Build Alpine Linux packages with drone CI       0
alpinelinux/git-mirror-syncd                                                       0
alpinelinux/mirror-status                                                          0
alpinelinux/docker-alpine                                                          0
[root@master ~]#
```

可以看到，代理仓库支持搜索功能。


### 3.2 测试docker-hosted本地仓库

像上一节一样修改`/etc/docker/daemon.json`配置文件，并重启docker服务：

```sh
[root@master ~]# cat /etc/docker/daemon.json
{
    "insecure-registries":[
        "nexushub.com:8002"
    ],
    "registry-mirrors":[
        "http://nexushub.com:8002"
    ],
    "data-root": "/data/docker"
}
[root@master ~]# systemctl restart docker
[root@master ~]# docker info|tail -n 6
  nexushub.com:8002
  127.0.0.0/8
 Registry Mirrors:
  http://nexushub.com:8002/
 Live Restore Enabled: false

[root@master ~]#
```

#### 3.2.1 测试docker-hosted本地仓库的pull

当我修改了docker的代理仓库地址时，发现拉取镜像不那么好使了，为了确认docker到底有没有走我们的代理，可以使用`tcpdump`命令抓包。

在执行下载镜像前，使用以下命令开始抓包：

```sh
[root@master ~]# tcpdump -w docker.pcap
tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
```

此时，`tcpdump`命令开始抓包。

我们重开一个命令行窗口，执行`docker pull`下载镜像，为了与之前下载的镜像不一样，使用`docker pull alpine:3.17`命令下载不一样版本标签的镜像：

```sh
[root@master ~]# date
Fri Jan 26 21:29:29 CST 2024
[root@master ~]# docker pull alpine:3.17
3.17: Pulling from library/alpine
1207c741d8c9: Pull complete
error pulling image configuration: Get https://registry-1.docker.io/v2/library/alpine/blobs/sha256:7997ad530b088ce1ef0b5e4a705600db0e62a2fd399e3639722b81ebe596d67d: net/http: TLS handshake timeout
[root@master ~]#
```

此时，可以发现docker去官方仓库下载镜像，出现异常了。



在`tcpdump`窗口，按`Ctrl+C`停止抓包。然后查看抓包内容，并进行过滤：

```sh
[root@master ~]# tcpdump -r docker.pcap |grep docker
reading from file docker.pcap, link-type EN10MB (Ethernet)
21:29:30.981844 IP master.39801 > 183.60.83.19.domain: 39211+ AAAA? registry-1.docker.io. (38)
21:29:30.981891 IP master.41196 > 183.60.83.19.domain: 35656+ A? registry-1.docker.io. (38)
21:29:32.494813 IP master.58750 > 183.60.83.19.domain: 21063+ A? auth.docker.io. (32)
21:29:32.494813 IP master.57133 > 183.60.83.19.domain: 50872+ AAAA? auth.docker.io. (32)
21:29:34.629189 IP master.35928 > 183.60.83.19.domain: 2521+ A? registry-1.docker.io. (38)
21:29:34.629189 IP master.44917 > 183.60.83.19.domain: 60493+ AAAA? registry-1.docker.io. (38)
21:29:42.004018 IP master.39689 > 183.60.83.19.domain: 40605+ AAAA? registry-1.docker.io. (38)
21:29:42.004069 IP master.50498 > 183.60.83.19.domain: 43681+ A? registry-1.docker.io. (38)
21:29:45.811099 IP master.37113 > 183.60.83.19.domain: 58786+ AAAA? registry-1.docker.io. (38)
21:29:45.811101 IP master.42227 > 183.60.83.19.domain: 23235+ A? registry-1.docker.io. (38)
21:29:47.842681 IP master.59306 > 183.60.83.19.domain: 1282+ AAAA? registry-1.docker.io. (38)
21:29:47.842712 IP master.41541 > 183.60.83.19.domain: 19428+ A? registry-1.docker.io. (38)
21:29:49.329197 IP master.38550 > 183.60.83.19.domain: 56599+ AAAA? production.cloudflare.docker.com. (50)
21:29:49.329197 IP master.54597 > 183.60.83.19.domain: 44289+ A? production.cloudflare.docker.com. (50)
[root@master ~]# tcpdump -r docker.pcap |grep nexushub
reading from file docker.pcap, link-type EN10MB (Ethernet)
21:29:30.928183 IP master.47456 > nexushub.com.teradataordbms: Flags [S], seq 4140786466, win 29200, options [mss 1460,sackOK,TS val 7389275 ecr 0,nop,wscale 7], length 0
21:29:30.932360 IP nexushub.com.teradataordbms > master.47456: Flags [S.], seq 653420215, ack 4140786467, win 28960, options [mss 1424,sackOK,TS val 1094546779 ecr 7389275,nop,wscale 7], length 0
21:29:30.932394 IP master.47456 > nexushub.com.teradataordbms: Flags [.], ack 1, win 229, options [nop,nop,TS val 7389279 ecr 1094546779], length 0
21:29:30.932480 IP master.47456 > nexushub.com.teradataordbms: Flags [P.], seq 1:252, ack 1, win 229, options [nop,nop,TS val 7389279 ecr 1094546779], length 251
21:29:30.937268 IP nexushub.com.teradataordbms > master.47456: Flags [.], ack 252, win 235, options [nop,nop,TS val 1094546784 ecr 7389279], length 0
21:29:30.939085 IP nexushub.com.teradataordbms > master.47456: Flags [P.], seq 1:634, ack 252, win 235, options [nop,nop,TS val 1094546786 ecr 7389279], length 633
21:29:30.939095 IP master.47456 > nexushub.com.teradataordbms: Flags [.], ack 634, win 239, options [nop,nop,TS val 7389286 ecr 1094546786], length 0
21:29:30.939098 IP nexushub.com.teradataordbms > master.47456: Flags [F.], seq 634, ack 252, win 235, options [nop,nop,TS val 1094546786 ecr 7389279], length 0
21:29:30.939189 IP master.47456 > nexushub.com.teradataordbms: Flags [F.], seq 252, ack 635, win 239, options [nop,nop,TS val 7389286 ecr 1094546786], length 0
21:29:30.940119 IP master.47458 > nexushub.com.teradataordbms: Flags [S], seq 1817288869, win 29200, options [mss 1460,sackOK,TS val 7389287 ecr 0,nop,wscale 7], length 0
21:29:30.943971 IP nexushub.com.teradataordbms > master.47456: Flags [.], ack 253, win 235, options [nop,nop,TS val 1094546790 ecr 7389286], length 0
21:29:30.945032 IP nexushub.com.teradataordbms > master.47458: Flags [S.], seq 4064665969, ack 1817288870, win 28960, options [mss 1424,sackOK,TS val 1094546792 ecr 7389287,nop,wscale 7], length 0
21:29:30.945049 IP master.47458 > nexushub.com.teradataordbms: Flags [.], ack 1, win 229, options [nop,nop,TS val 7389292 ecr 1094546792], length 0
21:29:30.945142 IP master.47458 > nexushub.com.teradataordbms: Flags [P.], seq 1:354, ack 1, win 229, options [nop,nop,TS val 7389292 ecr 1094546792], length 353
21:29:30.949228 IP nexushub.com.teradataordbms > master.47458: Flags [.], ack 354, win 235, options [nop,nop,TS val 1094546796 ecr 7389292], length 0
21:29:30.950788 IP nexushub.com.teradataordbms > master.47458: Flags [P.], seq 1:411, ack 354, win 235, options [nop,nop,TS val 1094546797 ecr 7389292], length 410
21:29:30.950806 IP master.47458 > nexushub.com.teradataordbms: Flags [.], ack 411, win 237, options [nop,nop,TS val 7389298 ecr 1094546797], length 0
21:29:30.950811 IP nexushub.com.teradataordbms > master.47458: Flags [F.], seq 411, ack 354, win 235, options [nop,nop,TS val 1094546797 ecr 7389292], length 0
21:29:30.950889 IP master.47458 > nexushub.com.teradataordbms: Flags [F.], seq 354, ack 412, win 237, options [nop,nop,TS val 7389298 ecr 1094546797], length 0
21:29:30.951037 IP master.47460 > nexushub.com.teradataordbms: Flags [S], seq 1864346844, win 29200, options [mss 1460,sackOK,TS val 7389298 ecr 0,nop,wscale 7], length 0
21:29:30.954957 IP nexushub.com.teradataordbms > master.47458: Flags [.], ack 355, win 235, options [nop,nop,TS val 1094546801 ecr 7389298], length 0
21:29:30.955927 IP nexushub.com.teradataordbms > master.47460: Flags [S.], seq 632883591, ack 1864346845, win 28960, options [mss 1424,sackOK,TS val 1094546802 ecr 7389298,nop,wscale 7], length 0
21:29:30.955946 IP master.47460 > nexushub.com.teradataordbms: Flags [.], ack 1, win 229, options [nop,nop,TS val 7389303 ecr 1094546802], length 0
21:29:30.956041 IP master.47460 > nexushub.com.teradataordbms: Flags [P.], seq 1:654, ack 1, win 229, options [nop,nop,TS val 7389303 ecr 1094546802], length 653
21:29:30.960143 IP nexushub.com.teradataordbms > master.47460: Flags [.], ack 654, win 237, options [nop,nop,TS val 1094546807 ecr 7389303], length 0
21:29:30.963244 IP nexushub.com.teradataordbms > master.47460: Flags [P.], seq 1:406, ack 654, win 237, options [nop,nop,TS val 1094546810 ecr 7389303], length 405
21:29:30.963254 IP master.47460 > nexushub.com.teradataordbms: Flags [.], ack 406, win 237, options [nop,nop,TS val 7389310 ecr 1094546810], length 0
21:29:30.963256 IP nexushub.com.teradataordbms > master.47460: Flags [F.], seq 406, ack 654, win 237, options [nop,nop,TS val 1094546810 ecr 7389303], length 0
21:29:30.963329 IP master.47460 > nexushub.com.teradataordbms: Flags [F.], seq 654, ack 407, win 237, options [nop,nop,TS val 7389310 ecr 1094546810], length 0
21:29:30.963486 IP master.47462 > nexushub.com.teradataordbms: Flags [S], seq 3505736660, win 29200, options [mss 1460,sackOK,TS val 7389310 ecr 0,nop,wscale 7], length 0
21:29:30.967399 IP nexushub.com.teradataordbms > master.47460: Flags [.], ack 655, win 237, options [nop,nop,TS val 1094546814 ecr 7389310], length 0
21:29:30.968399 IP nexushub.com.teradataordbms > master.47462: Flags [S.], seq 1793806116, ack 3505736661, win 28960, options [mss 1424,sackOK,TS val 1094546815 ecr 7389310,nop,wscale 7], length 0
21:29:30.968413 IP master.47462 > nexushub.com.teradataordbms: Flags [.], ack 1, win 229, options [nop,nop,TS val 7389315 ecr 1094546815], length 0
21:29:30.968520 IP master.47462 > nexushub.com.teradataordbms: Flags [P.], seq 1:676, ack 1, win 229, options [nop,nop,TS val 7389315 ecr 1094546815], length 675
21:29:30.972658 IP nexushub.com.teradataordbms > master.47462: Flags [.], ack 676, win 237, options [nop,nop,TS val 1094546819 ecr 7389315], length 0
21:29:30.981318 IP nexushub.com.teradataordbms > master.47462: Flags [P.], seq 1:527, ack 676, win 237, options [nop,nop,TS val 1094546828 ecr 7389315], length 526
21:29:30.981353 IP master.47462 > nexushub.com.teradataordbms: Flags [.], ack 527, win 237, options [nop,nop,TS val 7389328 ecr 1094546828], length 0
21:29:30.981358 IP nexushub.com.teradataordbms > master.47462: Flags [F.], seq 527, ack 676, win 237, options [nop,nop,TS val 1094546828 ecr 7389315], length 0
21:29:30.981462 IP master.47462 > nexushub.com.teradataordbms: Flags [F.], seq 676, ack 528, win 237, options [nop,nop,TS val 7389328 ecr 1094546828], length 0
21:29:30.985551 IP nexushub.com.teradataordbms > master.47462: Flags [.], ack 677, win 237, options [nop,nop,TS val 1094546832 ecr 7389328], length 0
[root@master ~]#
```

![](/img/Snipaste_2024-01-26_21-39-25.png)



可以看到，docker先从代理nexushub.com拉取镜像，发现没有拉取到，又从docker官方镜像仓库去拉取，由于从国内访问docker官方镜像仓库很慢，导致镜像下载失败了。说明通过本地仓库代理去拉取官方镜像是不通的。



#### 3.2.2 测试docker-hosted本地仓库的push

给3.1节自己创建的本地镜像，重新打个标签：

```sh
# 打标签
[root@master ~]# docker tag mysql-client:proxy nexushub.com:8002/mysql-client:hosted

# 查看本地镜像
[root@master ~]# docker images|grep mysql
nexushub.com:8002/mysql-client   hosted    f326dd608a3f   2 days ago    41.1MB
mysql-client                     proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8001/mysql-client   proxy     f326dd608a3f   2 days ago    41.1MB
[root@master ~]#
```



尝试push推送到本地仓库：

```sh
# 第一次登陆时，需要输入用户名和密码
[root@master ~]# docker login http://nexushub.com:8002
Username: admin
Password:
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
[root@master ~]#

# 再次登陆的话，就会用之前保存的认证信息
[root@master ~]# docker login http://nexushub.com:8002
Authenticating with existing credentials...
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

# 尝试推送本地镜像到nexushub.com本地仓库
[root@master ~]# docker push nexushub.com:8002/mysql-client:hosted
The push refers to repository [nexushub.com:8002/mysql-client]
55af1c19d0db: Pushed
89ae5c4ee501: Pushed
hosted: digest: sha256:55ff0eed604c1ed42c18455a1ac3ba6fbd10a44cc7e6b489bb48d2e6a4d5ad01 size: 739
[root@master ~]#
```

可以看到，正常推送到远程仓库了。



此时，在Nexus Browse浏览器中，可以看到docker-hosted仓库中已经有blob对象数据了：

![](/img/Snipaste_2024-01-26_21-53-43.png)



此时，尝试pull拉取刚才上传的镜像：



```sh
# 直接拉取，此时会docker官方镜像仓库拉取镜像
# 因为这个镜像是在我们自己的nexushub.com本地仓库，并不在官方镜像仓库
# 可以看到拉取失败
[root@master ~]# docker pull mysql-client:hosted
Error response from daemon: Get https://registry-1.docker.io/v2/: net/http: request canceled (Client.Timeout exceeded while awaiting headers)

# 查看当前存在哪些镜像
[root@master ~]# docker images
REPOSITORY                       TAG       IMAGE ID       CREATED       SIZE
mysql-client                     proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8001/mysql-client   proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8002/mysql-client   hosted    f326dd608a3f   2 days ago    41.1MB
alpine                           3.19      f8c20f8bbcb6   7 weeks ago   7.38MB
alpine                           3.9       78a2ce922f86   3 years ago   5.55MB

# 将我们刚才本地打标签的镜像删除掉
[root@master ~]# docker rmi nexushub.com:8002/mysql-client:hosted
Untagged: nexushub.com:8002/mysql-client:hosted
Untagged: nexushub.com:8002/mysql-client@sha256:55ff0eed604c1ed42c18455a1ac3ba6fbd10a44cc7e6b489bb48d2e6a4d5ad01

# 查看当前存在哪些镜像
[root@master ~]# docker images
REPOSITORY                       TAG       IMAGE ID       CREATED       SIZE
mysql-client                     proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8001/mysql-client   proxy     f326dd608a3f   2 days ago    41.1MB
alpine                           3.19      f8c20f8bbcb6   7 weeks ago   7.38MB
alpine                           3.9       78a2ce922f86   3 years ago   5.55MB


# 带上域名，再次从nexushub.com本地仓库拉取镜像
# 可以看到，正常拉取下来镜像
[root@master ~]# docker pull nexushub.com:8002/mysql-client:hosted
hosted: Pulling from mysql-client
Digest: sha256:55ff0eed604c1ed42c18455a1ac3ba6fbd10a44cc7e6b489bb48d2e6a4d5ad01
Status: Downloaded newer image for nexushub.com:8002/mysql-client:hosted
nexushub.com:8002/mysql-client:hosted

# 再次查看镜像信息
# 可以看到，新下载的镜像ID也是f326dd608a3f，与之前我们本地创建的镜像的ID是一样的
[root@master ~]# docker images
REPOSITORY                       TAG       IMAGE ID       CREATED       SIZE
mysql-client                     proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8001/mysql-client   proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8002/mysql-client   hosted    f326dd608a3f   2 days ago    41.1MB
alpine                           3.19      f8c20f8bbcb6   7 weeks ago   7.38MB
alpine                           3.9       78a2ce922f86   3 years ago   5.55MB
[root@master ~]#
```

通过以上实验，可以看到在docker中配置`docker-hosted`作为加速源，只能正常`pull`  nexus本地仓库中存在的镜像，并且可以`push`推送镜像到nexus本地仓库中。



### 3.3 测试docker-group聚合仓库
像上一节一样修改`/etc/docker/daemon.json`配置文件，并重启docker服务：

```sh
[root@master ~]# cat /etc/docker/daemon.json
{
    "insecure-registries":[
        "nexushub.com:8003"
    ],
    "registry-mirrors":[
        "http://nexushub.com:8003"
    ],
    "data-root": "/data/docker"
}
[root@master ~]# systemctl restart docker
[root@master ~]# docker info|tail -n 6
  nexushub.com:8003
  127.0.0.0/8
 Registry Mirrors:
  http://nexushub.com:8003/
 Live Restore Enabled: false

[root@master ~]#
```

#### 3.3.1 测试docker-group聚合仓库的pull



##### 3.3.1.1 拉取docker官方仓库中的镜像

拉取代理仓库中不存在的镜像：

```sh
# 查看本地镜像
[root@master ~]# docker images
REPOSITORY                       TAG       IMAGE ID       CREATED       SIZE
mysql-client                     proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8001/mysql-client   proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8002/mysql-client   hosted    f326dd608a3f   2 days ago    41.1MB
alpine                           3.19      f8c20f8bbcb6   7 weeks ago   7.38MB
alpine                           3.9       78a2ce922f86   3 years ago   5.55MB

# 拉取新版本的镜像
# 可以看到，很快就拉取下来了
[root@master ~]# docker pull alpine:3.16
3.16: Pulling from library/alpine
070eb51debd9: Pull complete
Digest: sha256:e4cdb7d47b06ba0a062ad2a97a7d154967c8f83934594d9f2bd3efa89292996b
Status: Downloaded newer image for alpine:3.16
docker.io/library/alpine:3.16

# 再次查看本地镜像
[root@master ~]# docker images
REPOSITORY                       TAG       IMAGE ID       CREATED       SIZE
mysql-client                     proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8001/mysql-client   proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8002/mysql-client   hosted    f326dd608a3f   2 days ago    41.1MB
alpine                           3.19      f8c20f8bbcb6   7 weeks ago   7.38MB
alpine                           3.16      e525c930fe75   8 weeks ago   5.54MB
alpine                           3.9       78a2ce922f86   3 years ago   5.55MB
[root@master ~]#
```

在Nexus Browse浏览器中，可以看到docker-group仓库中已经有blob对象数据了:

![](/img/Snipaste_2024-01-26_22-21-56.png)

该仓库中包含了docker-proxy代理仓库下载的镜像。



##### 3.3.1.2 拉取nexus-hosted仓库中的镜像

我们上一节手动上传了一个镜像到nexus-hosted本地仓库中，我们尝试下载这个镜像：

```sh
[root@master ~]# docker pull nexushub.com:8003/mysql-client:hosted
hosted: Pulling from mysql-client
Digest: sha256:55ff0eed604c1ed42c18455a1ac3ba6fbd10a44cc7e6b489bb48d2e6a4d5ad01
Status: Downloaded newer image for nexushub.com:8003/mysql-client:hosted
nexushub.com:8003/mysql-client:hosted
[root@master ~]# docker images
REPOSITORY                       TAG       IMAGE ID       CREATED       SIZE
mysql-client                     proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8001/mysql-client   proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8002/mysql-client   hosted    f326dd608a3f   2 days ago    41.1MB
nexushub.com:8003/mysql-client   hosted    f326dd608a3f   2 days ago    41.1MB
alpine                           3.19      f8c20f8bbcb6   7 weeks ago   7.38MB
alpine                           3.16      e525c930fe75   8 weeks ago   5.54MB
alpine                           3.9       78a2ce922f86   3 years ago   5.55MB
[root@master ~]#
```

可以看到，此时使用的`8003`端口代理，同样能拉取`mysql-client:hosted`镜像下来。



通过以下两次拉取镜像可以看到，使用`docker-group`聚合仓库，可以拉取docker官方镜像和自己上传到`docker-hosted`仓库中的私有镜像。



#### 3.3.2 测试docker-group聚合仓库的push



像3.2节一样，打镜像标签，登陆远程仓库，然后执行push推送：

```sh
# 登陆聚合仓库
[root@master ~]# docker login http://nexushub.com:8003
Username: admin
Password:
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

# 重新打标签
[root@master ~]# docker tag mysql-client:proxy nexushub.com:8003/mysql-client:group

# 查看本地镜像
[root@master ~]# docker images
REPOSITORY                       TAG       IMAGE ID       CREATED       SIZE
nexushub.com:8001/mysql-client   proxy     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8002/mysql-client   hosted    f326dd608a3f   2 days ago    41.1MB
nexushub.com:8003/mysql-client   group     f326dd608a3f   2 days ago    41.1MB
nexushub.com:8003/mysql-client   hosted    f326dd608a3f   2 days ago    41.1MB
mysql-client                     proxy     f326dd608a3f   2 days ago    41.1MB
alpine                           3.19      f8c20f8bbcb6   7 weeks ago   7.38MB
alpine                           3.16      e525c930fe75   8 weeks ago   5.54MB
alpine                           3.9       78a2ce922f86   3 years ago   5.55MB

# 尝试推送到远程仓库
[root@master ~]# docker push nexushub.com:8003/mysql-client:group
The push refers to repository [nexushub.com:8003/mysql-client]
55af1c19d0db: Layer already exists
89ae5c4ee501: Layer already exists
denied: Deploying to groups is a PRO-licensed feature. See https://links.sonatype.com/product-nexus-repository
[root@master ~]#
```

可以看到，提示异常"denied: Deploying to groups is a PRO-licensed feature. See https://links.sonatype.com/product-nexus-repository" 权限拒绝，部署到组需要PRO许可。

即要专业版才让朝聚合仓库里面推送镜像，我们简单看下官方的报价：

![](/img/Snipaste_2024-01-26_22-41-01.png)

即，如果你有50个用户，那一个用户一个月要127美元！按 2024-01-26 的汇率，每个月约要911.39元。

看看免费版和专业版的区别：

![](/img/Snipaste_2024-01-26_22-43-15.png)

可以看到，免费版不支持高可用、不支持朝NPM仓库和docker聚合仓库推送。我自己测试，不想花钱。



通过以上几节验证，可以知道三种类型的仓库支持的docker镜像正如规划时的一样：


| 仓库类型       | 仓库名称      | HTTP端口号 | HTTPS端口号 | 支持docker操作 |
| -------------- | :------------ | ---------- | ----------- | :------------- |
| proxy代理仓库  | docker-proxy  | 8001       | 不设置      | pull           |
| hosted本地仓库 | docker-hosted | 8002       | 不设置      | pull、push     |
| group聚合仓库  | docker-group  | 8003       | 不设置      | pull           |







