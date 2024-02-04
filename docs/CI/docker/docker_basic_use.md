# docker的基本使用

[[toc]]

## 安装docker

如果你配置了`Homebrew`工具的话，使用`brew cask install docker`就可以快速安装docker桌面工具。

或者从docker官网[https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)下载安装包安装。

## 查看docker版本信息

```sh
$ docker version
Client: Docker Engine - Community
 Version:           19.03.5
 API version:       1.40
 Go version:        go1.12.12
 Git commit:        633a0ea
 Built:             Wed Nov 13 07:22:34 2019
 OS/Arch:           darwin/amd64
 Experimental:      true

Server: Docker Engine - Community
 Engine:
  Version:          19.03.5
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.12
  Git commit:       633a0ea
  Built:            Wed Nov 13 07:29:19 2019
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v1.2.10
  GitCommit:        b34a5c8af56e510852c35414db4c1f4fa6172339
 runc:
  Version:          1.0.0-rc8+dev
  GitCommit:        3e425f80a8c931f88e6d94a8c831b9d5aa481657
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
```

## 配置docker国内镜像

从docker官网上面下载镜像时，由于网络原因，下载速度非常慢，还有可能下载失败，因此安装完docker后就应马上配置docker的国内镜像站。

可以参考[Docker 镜像加速](https://www.runoob.com/docker/docker-mirror-acceleration.html) 配置docker的国内镜像。

在任务栏点击`Docker Desktop`应用图标，打开`Perferences`个人设置，切换到`Docker Engine`标签页，可以看到默认的配置：

![docker_setting_default](/img/docker_setting_default.png)

我们在这个配置文件中添加镜像的配置，配置内容如下：

```
{
  "debug": true,
  "experimental": false,
  "registry-mirrors":["https://docker.mirrors.ustc.edu.cn","https://hub-mirror.c.163.com","http://f1361db2.m.daocloud.io"]
}
```

![docker_add_registry_mirrors](/img/docker_add_registry_mirrors.png) 

添加完成后，点击「Apple & Restart」应用并重启后，再看看docker的镜像信息：

```sh
$ docker info                                                                                                                                                                 [21:35:47]
Client:
 Debug Mode: false

Server:
 Containers: 1
  Running: 0
  Paused: 0
  Stopped: 1
 Images: 1
 Server Version: 19.03.5
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Native Overlay Diff: true
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
 Swarm: inactive
 Runtimes: runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: b34a5c8af56e510852c35414db4c1f4fa6172339
 runc version: 3e425f80a8c931f88e6d94a8c831b9d5aa481657
 init version: fec3683
 Security Options:
  seccomp
   Profile: default
 Kernel Version: 4.19.76-linuxkit
 Operating System: Docker Desktop
 OSType: linux
 Architecture: x86_64
 CPUs: 4
 Total Memory: 1.943GiB
 Name: docker-desktop
 ID: N5AI:K2A5:6S6U:QOC2:2ZIZ:ASKA:ER7V:BNOO:5ETC:LFXJ:LETZ:JDD5
 Docker Root Dir: /var/lib/docker
 Debug Mode: true
  File Descriptors: 34
  Goroutines: 50
  System Time: 2020-04-04T13:35:53.638116731Z
  EventsListeners: 3
 HTTP Proxy: gateway.docker.internal:3128
 HTTPS Proxy: gateway.docker.internal:3129
 Registry: https://index.docker.io/v1/
 Labels:
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Registry Mirrors:
  https://docker.mirrors.ustc.edu.cn/
  https://hub-mirror.c.163.com/
  http://f1361db2.m.daocloud.io/
 Live Restore Enabled: false
 Product License: Community Engine
```

可以看到`Registry Mirrors`处已经显示了三个国内的镜像站地址，说明已经生效了。

:::tip 提示
你也可以直接修改docker的配置文件，配置文件位置为`~/.docker/daemon.json `。

```sh
$ cat ~/.docker/daemon.json
{"debug":true,"experimental":false,"registry-mirrors":["https://docker.mirrors.ustc.edu.cn","https://hub-mirror.c.163.com","http://f1361db2.m.daocloud.io"]}
```

在Linux系统上面对应的配置文件为`/etc/docker/daemon.json`。
:::

配置了国内镜像站后，你后续使用`docker pull`下载docker镜像时，可以明显发现速度快多了。

## 搜索docker镜像

```sh
# 搜索镜像时的帮助信息
$ docker search --help

Usage:	docker search [OPTIONS] TERM

Search the Docker Hub for images

Options:
  -f, --filter filter   Filter output based on conditions provided
      --format string   Pretty-print search using a Go template
      --limit int       Max number of search results (default 25)
      --no-trunc        Don't truncate output
  
# 搜索hello-world镜像，限制只列出1个搜索结果     
$ docker search hello-world --limit 1
NAME                DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
hello-world         Hello World! (an example of minimal Dockeriz…   1139                [OK]
```


## 下载docker镜像

```sh
$ docker pull hello-world
Using default tag: latest
latest: Pulling from library/hello-world
1b930d010525: Pull complete
Digest: sha256:fc6a51919cfeb2e6763f62b6d9e8815acbf7cd2e476ea353743570610737b752
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest
```

## 查看docker镜像信息

```sh
$ docker images
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
hello-world            latest              fce289e99eb9        14 months ago       1.84kB
```

## 查看docker容器信息

```sh
$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS                      PORTS               NAMES
c8f5724b95f0        hello-world            "/hello"            2 minutes ago       Exited (0) 2 minutes ago                        great_goodall
21ad63cdd8fb        meizhaohui/meicentos   "/bin/bash"         11 minutes ago      Exited (0) 10 minutes ago                       pensive_mclaren
```

## 运行docker容器

```sh
$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

按以上步骤，我们可以下载meizhaohui/meicentos镜像，下载完成后，查看镜像信息如下：

```sh
$  docker images
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
meizhaohui/meicentos   latest              e64cd9abd46d        10 months ago       710MB
hello-world            latest              fce289e99eb9        14 months ago       1.84kB
```

## 停止docker容器

```sh
# docker stop 容器ID
$ docker stop c8f5724b95f0
c8f5724b95f0
```

## 删除docker容器

```sh
# docker rm 容器ID
$ docker rm 6861c0c9dc73
6861c0c9dc73
```

## 查看所有的docker容器

```sh
$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS                     PORTS               NAMES
21ad63cdd8fb        meizhaohui/meicentos   "/bin/bash"         9 minutes ago       Exited (0) 8 minutes ago                       pensive_mclaren
```


## 删除docker镜像

若要删除镜像，先要停止并删除容器

```sh
$ docker rmi --help

Usage:	docker rmi [OPTIONS] IMAGE [IMAGE...]

Remove one or more images

Options:
  -f, --force      Force removal of the image
      --no-prune   Do not delete untagged parents

# 查看当前存在的镜像
$ docker images
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
meizhaohui/meicentos   latest              e64cd9abd46d        10 months ago       710MB
hello-world            latest              fce289e99eb9        14 months ago       1.84kB

# 删除镜像
$ docker rmi fce289e99eb9
Untagged: hello-world:latest
Untagged: hello-world@sha256:fc6a51919cfeb2e6763f62b6d9e8815acbf7cd2e476ea353743570610737b752
Deleted: sha256:fce289e99eb9bca977dae136fbe2a82b6b7d4c372474c9235adc1741675f587e
Deleted: sha256:af0b15c8625bb1938f1d7b17081031f649fd14e6b233688eea3c5483994a66a3

# 再次查看本地镜像情况
$ docker images
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
meizhaohui/meicentos   latest              e64cd9abd46d        10 months ago       710MB
```
## docker的运行

docker的运行主要使用`docker run`命令运行，但有很多参数。

- 查看`docker run`的帮助信息

```sh
$ docker run --help

Usage:	docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

Run a command in a new container

Options:
      --add-host list                  Add a custom host-to-IP mapping (host:ip)
  -a, --attach list                    Attach to STDIN, STDOUT or STDERR
      --blkio-weight uint16            Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0)
      --blkio-weight-device list       Block IO weight (relative device weight) (default [])
      --cap-add list                   Add Linux capabilities
      --cap-drop list                  Drop Linux capabilities
      --cgroup-parent string           Optional parent cgroup for the container
      --cidfile string                 Write the container ID to the file
      --cpu-period int                 Limit CPU CFS (Completely Fair Scheduler) period
      --cpu-quota int                  Limit CPU CFS (Completely Fair Scheduler) quota
      --cpu-rt-period int              Limit CPU real-time period in microseconds
      --cpu-rt-runtime int             Limit CPU real-time runtime in microseconds
  -c, --cpu-shares int                 CPU shares (relative weight)
      --cpus decimal                   Number of CPUs
      --cpuset-cpus string             CPUs in which to allow execution (0-3, 0,1)
      --cpuset-mems string             MEMs in which to allow execution (0-3, 0,1)
  -d, --detach                         Run container in background and print container ID
      --detach-keys string             Override the key sequence for detaching a container
      --device list                    Add a host device to the container
      --device-cgroup-rule list        Add a rule to the cgroup allowed devices list
      --device-read-bps list           Limit read rate (bytes per second) from a device (default [])
      --device-read-iops list          Limit read rate (IO per second) from a device (default [])
      --device-write-bps list          Limit write rate (bytes per second) to a device (default [])
      --device-write-iops list         Limit write rate (IO per second) to a device (default [])
      --disable-content-trust          Skip image verification (default true)
      --dns list                       Set custom DNS servers
      --dns-option list                Set DNS options
      --dns-search list                Set custom DNS search domains
      --domainname string              Container NIS domain name
      --entrypoint string              Overwrite the default ENTRYPOINT of the image
  -e, --env list                       Set environment variables
      --env-file list                  Read in a file of environment variables
      --expose list                    Expose a port or a range of ports
      --gpus gpu-request               GPU devices to add to the container ('all' to pass all GPUs)
      --group-add list                 Add additional groups to join
      --health-cmd string              Command to run to check health
      --health-interval duration       Time between running the check (ms|s|m|h) (default 0s)
      --health-retries int             Consecutive failures needed to report unhealthy
      --health-start-period duration   Start period for the container to initialize before starting health-retries countdown
                                       (ms|s|m|h) (default 0s)
      --health-timeout duration        Maximum time to allow one check to run (ms|s|m|h) (default 0s)
      --help                           Print usage
  -h, --hostname string                Container host name
      --init                           Run an init inside the container that forwards signals and reaps processes
  -i, --interactive                    Keep STDIN open even if not attached
      --ip string                      IPv4 address (e.g., 172.30.100.104)
      --ip6 string                     IPv6 address (e.g., 2001:db8::33)
      --ipc string                     IPC mode to use
      --isolation string               Container isolation technology
      --kernel-memory bytes            Kernel memory limit
  -l, --label list                     Set meta data on a container
      --label-file list                Read in a line delimited file of labels
      --link list                      Add link to another container
      --link-local-ip list             Container IPv4/IPv6 link-local addresses
      --log-driver string              Logging driver for the container
      --log-opt list                   Log driver options
      --mac-address string             Container MAC address (e.g., 92:d0:c6:0a:29:33)
  -m, --memory bytes                   Memory limit
      --memory-reservation bytes       Memory soft limit
      --memory-swap bytes              Swap limit equal to memory plus swap: '-1' to enable unlimited swap
      --memory-swappiness int          Tune container memory swappiness (0 to 100) (default -1)
      --mount mount                    Attach a filesystem mount to the container
      --name string                    Assign a name to the container
      --network network                Connect a container to a network
      --network-alias list             Add network-scoped alias for the container
      --no-healthcheck                 Disable any container-specified HEALTHCHECK
      --oom-kill-disable               Disable OOM Killer
      --oom-score-adj int              Tune host's OOM preferences (-1000 to 1000)
      --pid string                     PID namespace to use
      --pids-limit int                 Tune container pids limit (set -1 for unlimited)
      --privileged                     Give extended privileges to this container
  -p, --publish list                   Publish a container's port(s) to the host
  -P, --publish-all                    Publish all exposed ports to random ports
      --read-only                      Mount the container's root filesystem as read only
      --restart string                 Restart policy to apply when a container exits (default "no")
      --rm                             Automatically remove the container when it exits
      --runtime string                 Runtime to use for this container
      --security-opt list              Security Options
      --shm-size bytes                 Size of /dev/shm
      --sig-proxy                      Proxy received signals to the process (default true)
      --stop-signal string             Signal to stop a container (default "SIGTERM")
      --stop-timeout int               Timeout (in seconds) to stop a container
      --storage-opt list               Storage driver options for the container
      --sysctl map                     Sysctl options (default map[])
      --tmpfs list                     Mount a tmpfs directory
  -t, --tty                            Allocate a pseudo-TTY
      --ulimit ulimit                  Ulimit options (default [])
  -u, --user string                    Username or UID (format: <name|uid>[:<group|gid>])
      --userns string                  User namespace to use
      --uts string                     UTS namespace to use
  -v, --volume list                    Bind mount a volume
      --volume-driver string           Optional volume driver for the container
      --volumes-from list              Mount volumes from the specified container(s)
  -w, --workdir string                 Working directory inside the container
```

常用参数解释：

```sh
-d: 后台运行容器，并返回容器ID；
-a stdin: 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；
-i: 以交互模式运行容器，通常与 -t 同时使用；
-t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；
--name="nginx": 为容器指定一个名称；
--dns 8.8.8.8: 指定容器使用的DNS服务器，默认和宿主一致；
--expose=[]: 开放一个端口或一组端口；
--volume , -v: 绑定一个卷
```


- 使用docker镜像nginx:latest以后台模式启动一个容器,并将容器命名为mynginx

```sh
$ docker run --name mynginx -d nginx:latest
7b8234a6fd41ee7176f18f7d6d6c772ad3709a50d39006f4dff9f38d6575a922
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
7b8234a6fd41        nginx:latest        "nginx -g 'daemon of…"   14 seconds ago      Up 14 seconds       80/tcp              mynginx
```

- 使用镜像nginx:latest以交互模式启动一个容器,在容器内执行/bin/bash命令

```sh
$ docker run --name mynginx1 -it nginx:latest /bin/bash
root@4f898710186c:/# whoami
root
root@4f898710186c:/# ls
bin  boot  dev	etc  home  lib	lib64  media  mnt  opt	proc  root  run  sbin  srv  sys  tmp  usr  var
```

此时保持mynginx1容器交互容器不退出，在另外一个终端查看docker运行情况：

```sh
$ docker ps 
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
4f898710186c        nginx:latest        "/bin/bash"              About a minute ago   Up About a minute   80/tcp              mynginx1
7b8234a6fd41        nginx:latest        "nginx -g 'daemon of…"   3 minutes ago        Up 3 minutes        80/tcp              mynginx
```

退出mynginx1容器，再查看docker运行情况：

```sh
root@4f898710186c:/# exit
exit
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
7b8234a6fd41        nginx:latest        "nginx -g 'daemon of…"   5 minutes ago       Up 5 minutes        80/tcp              mynginx
```
可以发现容器也退出了，只有mynginx容器还在后台运行。


## 将容器中80端口映射到本机的8088端口

```sh
$ docker run --name mynginx2 -p 8088:80 -d nginx:latest
e424323f60c0fa5d42fd785a718509e9afe57247c47765fbd644d12595198b30
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
e424323f60c0        nginx:latest        "nginx -g 'daemon of…"   11 seconds ago      Up 10 seconds       0.0.0.0:8088->80/tcp   mynginx2
7b8234a6fd41        nginx:latest        "nginx -g 'daemon of…"   13 minutes ago      Up 12 minutes       80/tcp                 mynginx
```
此时，在本机访问 [http://localhost:8088/](http://localhost:8088/) 可以看到Nginx的欢迎页面，说明映射正常。

## 进入到在后台运行的容器中，打开容器的交互界面

推荐使用`docker exec`方式进入到在后台运行的docker容器中。

`docker attach container`：附加到运行容器中。不推荐使用，经常会卡住。

```sh
# docker exec -it  容器ID /bin/bash
docker exec -it 7b82 /bin/bash
$ docker exec -it 7b82 /bin/bash
root@7b8234a6fd41:/# nginx -h
nginx version: nginx/1.17.8
Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]

Options:
  -?,-h         : this help
  -v            : show version and exit
  -V            : show version and configure options then exit
  -t            : test configuration and exit
  -T            : test configuration, dump it and exit
  -q            : suppress non-error messages during configuration testing
  -s signal     : send signal to a master process: stop, quit, reopen, reload
  -p prefix     : set prefix path (default: /etc/nginx/)
  -c filename   : set configuration file (default: /etc/nginx/nginx.conf)
  -g directives : set global directives out of configuration file

root@7b8234a6fd41:/# nginx -v
nginx version: nginx/1.17.8
```

## 将docker容器目录挂载到本地目录

```sh
$ mkdir -p ~/mydocker/local_nginx
# 将容器中的/test_folder目录挂载到本机的~/mydocker/local_nginx目录下
$ docker run --name mynginx3 -p 8090:80 -v  ~/mydocker/local_nginx:/test_folder -d nginx:latest
26533089c5e95e2c900e4e544bbde286d1e30c613dd0e48f43992b71a3ccd5e2

$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
26533089c5e9        nginx:latest        "nginx -g 'daemon of…"   3 minutes ago       Up 3 minutes        0.0.0.0:8090->80/tcp   mynginx3
e424323f60c0        nginx:latest        "nginx -g 'daemon of…"   22 minutes ago      Up 22 minutes       0.0.0.0:8088->80/tcp   mynginx2
7b8234a6fd41        nginx:latest        "nginx -g 'daemon of…"   35 minutes ago      Up 35 minutes       80/tcp                 mynginx
# 进入到容器中
$ docker exec -it 26533 /bin/bash
root@26533089c5e9:/# ls -lah
total 76K
drwxr-xr-x   1 root root 4.0K Mar  3 11:02 .
drwxr-xr-x   1 root root 4.0K Mar  3 11:02 ..
-rwxr-xr-x   1 root root    0 Mar  3 11:02 .dockerenv
drwxr-xr-x   2 root root 4.0K Feb 24 00:00 bin
drwxr-xr-x   2 root root 4.0K Feb  1 17:09 boot
drwxr-xr-x   5 root root  340 Mar  3 11:02 dev
drwxr-xr-x   1 root root 4.0K Mar  3 11:02 etc
drwxr-xr-x   2 root root 4.0K Feb  1 17:09 home
drwxr-xr-x   1 root root 4.0K Feb 26 20:02 lib
drwxr-xr-x   2 root root 4.0K Feb 24 00:00 lib64
drwxr-xr-x   2 root root 4.0K Feb 24 00:00 media
drwxr-xr-x   2 root root 4.0K Feb 24 00:00 mnt
drwxr-xr-x   2 root root 4.0K Feb 24 00:00 opt
dr-xr-xr-x 182 root root    0 Mar  3 11:02 proc
drwx------   2 root root 4.0K Feb 24 00:00 root
drwxr-xr-x   1 root root 4.0K Mar  3 11:02 run
drwxr-xr-x   2 root root 4.0K Feb 24 00:00 sbin
drwxr-xr-x   2 root root 4.0K Feb 24 00:00 srv
dr-xr-xr-x  13 root root    0 Mar  3 10:27 sys
drwxr-xr-x   2 root root   64 Mar  3 10:15 test_folder
drwxrwxrwt   1 root root 4.0K Feb 26 20:02 tmp
drwxr-xr-x   1 root root 4.0K Feb 24 00:00 usr
drwxr-xr-x   1 root root 4.0K Feb 24 00:00 var
root@26533089c5e9:/# cd test_folder/
root@26533089c5e9:/test_folder#
root@26533089c5e9:/test_folder# echo 'abc' > abc.txt
root@26533089c5e9:/test_folder# mkdir test1
root@26533089c5e9:/test_folder# echo 'test1' > test1/test1.txt

```
在容器目录中创建一些文件，看看在本机上面是否可以查看到：


- 查看docker容器信息

```sh
$ cd ~/mydocker/local_nginx
$ $ tree
.
├── abc.txt
└── test1
    └── test1.txt

1 directory, 2 files

$ cat abc.txt 
abc
$ cat test1/test1.txt 
test1
$ ls -lah
total 8
drwxr-xr-x  4 meizhaohui  staff   128B  3  3 19:10 .
drwxr-xr-x  3 meizhaohui  staff    96B  3  3 18:15 ..
-rw-r--r--  1 meizhaohui  staff     4B  3  3 19:10 abc.txt
drwxr-xr-x  3 meizhaohui  staff    96B  3  3 19:10 test1
$ ls -lah test1
total 8
drwxr-xr-x  3 meizhaohui  staff    96B  3  3 19:10 .
drwxr-xr-x  4 meizhaohui  staff   128B  3  3 19:10 ..
-rw-r--r--  1 meizhaohui  staff     6B  3  3 19:10 test1.txt
```
可以看出本地已经生成了相应的文件和文件夹，并且文件的内容也是对的。

对本地文件进行更新，看一下在容器中是否可以同步过来。

```sh
meizhaohui@MacBook:/Users/meizhaohui/mydocker/local_nginx $ echo 'd' >> abc.txt 
meizhaohui@MacBook:/Users/meizhaohui/mydocker/local_nginx $ echo 'test' >> test1/test1.txt
meizhaohui@MacBook:/Users/meizhaohui/mydocker/local_nginx $ cp -rf test1 test2
meizhaohui@MacBook:/Users/meizhaohui/mydocker/local_nginx $ ll
total 8
-rw-r--r--  1 meizhaohui  staff     6B  3  3 19:15 abc.txt
drwxr-xr-x  3 meizhaohui  staff    96B  3  3 19:10 test1
drwxr-xr-x  3 meizhaohui  staff    96B  3  3 19:15 test2
```

检查容器，发现同步更新了：

```sh
root@26533089c5e9:/test_folder# ls
abc.txt  test1	test2
root@26533089c5e9:/test_folder# cat abc.txt
abc
d
root@26533089c5e9:/test_folder# cat test1/test1.txt
test1
test
root@26533089c5e9:/test_folder# cat test2/test1.txt
test1
test
```

再次测试挂载：

```sh
$ ls
local_nginx
$ docker run --name mynginx4 -p 8091:80 -v  ~/mydocker/local_nginx1:/ -d nginx:latest
docker: Error response from daemon: invalid volume specification: '/Users/meizhaohui/mydocker/local_nginx1:/': invalid mount config for type "bind": invalid specification: destination can't be '/'.
See 'docker run --help'.
$ docker run --name mynginx4 -p 8091:80 -v  ~/mydocker/local_nginx1:/home -d nginx:latest
662c6d0045762d9e2d233c7976a1a7dc78c2f2d1fe8455c98b9b11908096a05f
$ ls -lah
total 0
drwxr-xr-x   4 meizhaohui  staff   128B  3  3 19:18 .
drwxr-xr-x+ 43 meizhaohui  staff   1.3K  3  3 19:19 ..
drwxr-xr-x   5 meizhaohui  staff   160B  3  3 19:15 local_nginx
drwxr-xr-x   2 meizhaohui  staff    64B  3  3 19:18 local_nginx1
```

可以发现：

    1. 挂载时，不能直接挂载容器中的根目录；
    2. 挂载的，宿主机和容器中的目录可以不用事先创建，docker会自动创建。


- 查看docker容器挂载点

```sh
$  docker inspect 662c6|jq ".[0].HostConfig.Binds"
[
  "/Users/meizhaohui/mydocker/local_nginx1:/home"
]
$
```

- 启动停止运行的docker容器

```sh
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                         PORTS                  NAMES
662c6d004576        nginx:latest        "nginx -g 'daemon of…"   35 minutes ago      Up 35 minutes                  0.0.0.0:8091->80/tcp   mynginx4
26533089c5e9        nginx:latest        "nginx -g 'daemon of…"   51 minutes ago      Up 51 minutes                  0.0.0.0:8090->80/tcp   mynginx3
e424323f60c0        nginx:latest        "nginx -g 'daemon of…"   About an hour ago   Up About an hour               0.0.0.0:8088->80/tcp   mynginx2
4f898710186c        nginx:latest        "/bin/bash"              About an hour ago   Exited (0) About an hour ago                          mynginx1
7b8234a6fd41        nginx:latest        "nginx -g 'daemon of…"   About an hour ago   Up About an hour               80/tcp                 mynginx

# 启动 mynginx1容器
$ docker start 4f8987
4f8987
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
662c6d004576        nginx:latest        "nginx -g 'daemon of…"   35 minutes ago      Up 35 minutes       0.0.0.0:8091->80/tcp   mynginx4
26533089c5e9        nginx:latest        "nginx -g 'daemon of…"   51 minutes ago      Up 51 minutes       0.0.0.0:8090->80/tcp   mynginx3
e424323f60c0        nginx:latest        "nginx -g 'daemon of…"   About an hour ago   Up About an hour    0.0.0.0:8088->80/tcp   mynginx2
4f898710186c        nginx:latest        "/bin/bash"              About an hour ago   Up 3 seconds        80/tcp                 mynginx1
7b8234a6fd41        nginx:latest        "nginx -g 'daemon of…"   About an hour ago   Up About an hour    80/tcp                 mynginx
$
```


- 停止所有的docker容器

```sh
$ docker ps -aq
662c6d004576
26533089c5e9
e424323f60c0
4f898710186c
7b8234a6fd41
$ docker stop $(docker ps -qa)
662c6d004576
26533089c5e9
e424323f60c0
4f898710186c
7b8234a6fd41
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

- 删除所有的docker容器

```sh
$ docker rm $(docker ps -aq)
662c6d004576
26533089c5e9
e424323f60c0
4f898710186c
7b8234a6fd41
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

- 启动centos容器

特别说明：**Docker容器后台运行,就必须有一个前台进程.
容器运行的命令如果不是那些一直挂起的命令（比如运行top，tail），就是会自动退出的**

```sh
$ docker run --name mycentos -d meizhaohui/meicentos:latest ping 0.0.0.0
ae9e7499e89532f99e6cb7fdf0834ecfbf21bcf1b2526ee0af104a03088f0517
$ docker ps
CONTAINER ID        IMAGE                         COMMAND             CREATED             STATUS              PORTS               NAMES
ae9e7499e895        meizhaohui/meicentos:latest   "ping 0.0.0.0"      3 seconds ago       Up 3 seconds                            mycentos
$ docker exec -it ae9e /bin/bash
[root@ae9e7499e895 /]# ps
  PID TTY          TIME CMD
    6 pts/0    00:00:00 bash
   24 pts/0    00:00:00 ps
[root@ae9e7499e895 /]# ps -ef|grep ping
root         1     0  0 20:25 ?        00:00:00 ping 0.0.0.0
root        26     6  0 20:25 pts/0    00:00:00 grep --color=auto ping
```
- Centos7 Docker容器中报错 `Failed to get D-Bus connection: Operation not permitted`

我们 Centos7容器中查看httpd的状态，会提示异常：

```sh
[root@ae9e7499e895 ~]# systemctl status httpd
Failed to get D-Bus connection: Operation not permitted
```
如果要是用`systemctl`管理服务就要加上参数 `--privileged` 来增加权，并且不能使用默认的`bash`，换成`init`，命令如下:

```sh
# 删除原来的容器
 docker stop ae9e7499e895
ae9e7499e895
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
$ docker ps -a
CONTAINER ID        IMAGE                         COMMAND             CREATED             STATUS                            PORTS               NAMES
ae9e7499e895        meizhaohui/meicentos:latest   "ping 0.0.0.0"      3 hours ago         Exited (137) About a minute ago                       mycentos
$ docker rm ae9e7499e895
ae9e7499e895
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

# 重新后台启动centos7容器
$ docker run --name mycentos --privileged -d meizhaohui/meicentos:latest usr/sbin/init
a1f530aec1866a4ac1562b3c03a1380c4022b87df4dd48c7c0068d040f9355db
$ docker ps
CONTAINER ID        IMAGE                         COMMAND             CREATED             STATUS              PORTS               NAMES
a1f530aec186        meizhaohui/meicentos:latest   "usr/sbin/init"     5 seconds ago       Up 4 seconds                            mycentos
$ docker exec -it alf530 /bin/bash
Error: No such container: alf530
$ docker exec -it a1f530 /bin/bash
[root@a1f530aec186 /]# systemctl status httpd
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
   Active: inactive (dead)
     Docs: man:httpd(8)
           man:apachectl(8)
```

- 在容器中安装php7.2环境

```sh
[root@a1f530aec186 ~]# yum install epel-release -y
Loaded plugins: fastestmirror, ovl
Loading mirror speeds from cached hostfile
epel/x86_64/metalink                                                                                                 | 8.1 kB  00:00:00
 * base: mirrors.163.com
 * epel: hk.mirrors.thegigabit.com
 * extras: mirrors.163.com
 * ius: mirrors.tuna.tsinghua.edu.cn
 * updates: mirrors.163.com
base                                                                                                                 | 3.6 kB  00:00:00
epel                                                                                                                 | 5.3 kB  00:00:00
extras                                                                                                               | 2.9 kB  00:00:00
http://mirrors.tuna.tsinghua.edu.cn/ius/stable/CentOS/7/x86_64/repodata/repomd.xml: [Errno 14] HTTP Error 404 - Not Found
Trying other mirror.
To address this issue please refer to the below wiki article

https://wiki.centos.org/yum-errors

If above article doesn't help to resolve this issue please use https://bugs.centos.org/.

http://hkg.mirror.rackspace.com/ius/stable/CentOS/7/x86_64/repodata/repomd.xml: [Errno 14] HTTP Error 404 - Not Found
Trying other mirror.
http://mirror.its.dal.ca/ius/stable/CentOS/7/x86_64/repodata/repomd.xml: [Errno 14] HTTP Error 404 - Not Found
Trying other mirror.
ius                                                                                                                  | 2.6 kB  00:00:00
updates                                                                                                              | 2.9 kB  00:00:00
(1/8): epel/x86_64/group_gz                                                                                          |  90 kB  00:00:00
(2/8): epel/x86_64/updateinfo                                                                                        | 1.0 MB  00:00:01
(3/8): base/7/x86_64/group_gz                                                                                        | 165 kB  00:00:01
(4/8): base/7/x86_64/primary_db                                                                                      | 6.0 MB  00:00:01
(5/8): extras/7/x86_64/primary_db                                                                                    | 159 kB  00:00:01
(6/8): updates/7/x86_64/primary_db                                                                                   | 6.7 MB  00:00:01
(7/8): ius/x86_64/primary_db                                                                                         | 325 kB  00:00:03
(8/8): epel/x86_64/primary_db                                                                                        | 6.7 MB  00:00:50
Resolving Dependencies
--> Running transaction check
---> Package epel-release.noarch 0:7-11 will be updated
---> Package epel-release.noarch 0:7-12 will be an update
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================================================================
 Package                               Arch                            Version                          Repository                     Size
============================================================================================================================================
Updating:
 epel-release                          noarch                          7-12                             epel                           15 k

Transaction Summary
============================================================================================================================================
Upgrade  1 Package

Total download size: 15 k
Downloading packages:
Delta RPMs disabled because /usr/bin/applydeltarpm not installed.
epel-release-7-12.noarch.rpm                                                                                         |  15 kB  00:00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Updating   : epel-release-7-12.noarch                                                                                                 1/2
  Cleanup    : epel-release-7-11.noarch                                                                                                 2/2
  Verifying  : epel-release-7-12.noarch                                                                                                 1/2
  Verifying  : epel-release-7-11.noarch                                                                                                 2/2

Updated:
  epel-release.noarch 0:7-12

Complete!
[root@a1f530aec186 ~]# rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm
Retrieving https://mirror.webtatic.com/yum/el7/webtatic-release.rpm
warning: /var/tmp/rpm-tmp.WF9IFE: Header V4 RSA/SHA1 Signature, key ID 62e74ca5: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:webtatic-release-7-3             ################################# [100%]
[root@a1f530aec186 ~]#

# 安装php软件
# 精简安装
# yum -y install php72w php72w-cli php72w-fpm php72w-common php72w-devel 

# 也可以安装 豪华版拓展
# yum -y install php72w php72w-cli php72w-fpm php72w-common php72w-devel php72w-embedded php72w-gd php72w-mbstring php72w-mysqlnd php72w-opcache php72w-pdo php72w-xml

# 我们安装豪华版
[root@a1f530aec186 ~]# yum -y install php72w php72w-cli php72w-fpm php72w-common php72w-devel php72w-embedded php72w-gd php72w-mbstring php72w-mysqlnd php72w-opcache php72w-pdo php72w-xml
Loaded plugins: fastestmirror, ovl
Loading mirror speeds from cached hostfile
 * base: mirrors.163.com
 * epel: ftp.iij.ad.jp
 * extras: mirrors.163.com
 * ius: mirrors.tuna.tsinghua.edu.cn
 * updates: mirrors.163.com
 * webtatic: uk.repo.webtatic.com
Resolving Dependencies
--> Running transaction check
---> Package mod_php72w.x86_64 0:7.2.27-1.w7 will be installed
--> Processing Dependency: libargon2.so.0()(64bit) for package: mod_php72w-7.2.27-1.w7.x86_64
---> Package php72w-cli.x86_64 0:7.2.27-1.w7 will be installed
---> Package php72w-common.x86_64 0:7.2.27-1.w7 will be installed
---> Package php72w-devel.x86_64 0:7.2.27-1.w7 will be installed
---> Package php72w-embedded.x86_64 0:7.2.27-1.w7 will be installed
---> Package php72w-fpm.x86_64 0:7.2.27-1.w7 will be installed
--> Processing Dependency: systemd-sysv for package: php72w-fpm-7.2.27-1.w7.x86_64
---> Package php72w-gd.x86_64 0:7.2.27-1.w7 will be installed
--> Processing Dependency: libpng15.so.15(PNG15_0)(64bit) for package: php72w-gd-7.2.27-1.w7.x86_64
--> Processing Dependency: libjpeg.so.62(LIBJPEG_6.2)(64bit) for package: php72w-gd-7.2.27-1.w7.x86_64
--> Processing Dependency: libpng15.so.15()(64bit) for package: php72w-gd-7.2.27-1.w7.x86_64
--> Processing Dependency: libjpeg.so.62()(64bit) for package: php72w-gd-7.2.27-1.w7.x86_64
--> Processing Dependency: libfreetype.so.6()(64bit) for package: php72w-gd-7.2.27-1.w7.x86_64
--> Processing Dependency: libXpm.so.4()(64bit) for package: php72w-gd-7.2.27-1.w7.x86_64
--> Processing Dependency: libX11.so.6()(64bit) for package: php72w-gd-7.2.27-1.w7.x86_64
---> Package php72w-mbstring.x86_64 0:7.2.27-1.w7 will be installed
---> Package php72w-mysqlnd.x86_64 0:7.2.27-1.w7 will be installed
---> Package php72w-opcache.x86_64 0:7.2.27-1.w7 will be installed
---> Package php72w-pdo.x86_64 0:7.2.27-1.w7 will be installed
---> Package php72w-xml.x86_64 0:7.2.27-1.w7 will be installed
--> Processing Dependency: libxslt.so.1(LIBXML2_1.0.24)(64bit) for package: php72w-xml-7.2.27-1.w7.x86_64
--> Processing Dependency: libxslt.so.1(LIBXML2_1.0.22)(64bit) for package: php72w-xml-7.2.27-1.w7.x86_64
--> Processing Dependency: libxslt.so.1(LIBXML2_1.0.18)(64bit) for package: php72w-xml-7.2.27-1.w7.x86_64
--> Processing Dependency: libxslt.so.1(LIBXML2_1.0.13)(64bit) for package: php72w-xml-7.2.27-1.w7.x86_64
--> Processing Dependency: libxslt.so.1(LIBXML2_1.0.11)(64bit) for package: php72w-xml-7.2.27-1.w7.x86_64
--> Processing Dependency: libxslt.so.1()(64bit) for package: php72w-xml-7.2.27-1.w7.x86_64
--> Processing Dependency: libexslt.so.0()(64bit) for package: php72w-xml-7.2.27-1.w7.x86_64
--> Running transaction check
---> Package freetype.x86_64 0:2.8-14.el7 will be installed
---> Package libX11.x86_64 0:1.6.7-2.el7 will be installed
--> Processing Dependency: libX11-common >= 1.6.7-2.el7 for package: libX11-1.6.7-2.el7.x86_64
--> Processing Dependency: libxcb.so.1()(64bit) for package: libX11-1.6.7-2.el7.x86_64
---> Package libXpm.x86_64 0:3.5.12-1.el7 will be installed
---> Package libargon2.x86_64 0:20161029-3.el7 will be installed
---> Package libjpeg-turbo.x86_64 0:1.2.90-8.el7 will be installed
---> Package libpng.x86_64 2:1.5.13-7.el7_2 will be installed
---> Package libxslt.x86_64 0:1.1.28-5.el7 will be installed
---> Package systemd-sysv.x86_64 0:219-67.el7_7.3 will be installed
--> Processing Dependency: systemd = 219-67.el7_7.3 for package: systemd-sysv-219-67.el7_7.3.x86_64
--> Running transaction check
---> Package libX11-common.noarch 0:1.6.7-2.el7 will be installed
---> Package libxcb.x86_64 0:1.13-1.el7 will be installed
--> Processing Dependency: libXau.so.6()(64bit) for package: libxcb-1.13-1.el7.x86_64
---> Package systemd.x86_64 0:219-62.el7_6.5 will be updated
---> Package systemd.x86_64 0:219-67.el7_7.3 will be an update
--> Processing Dependency: systemd-libs = 219-67.el7_7.3 for package: systemd-219-67.el7_7.3.x86_64
--> Running transaction check
---> Package libXau.x86_64 0:1.0.8-2.1.el7 will be installed
---> Package systemd-libs.x86_64 0:219-62.el7_6.5 will be updated
---> Package systemd-libs.x86_64 0:219-67.el7_7.3 will be an update
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================================================================
 Package                              Arch                        Version                               Repository                     Size
============================================================================================================================================
Installing:
 mod_php72w                           x86_64                      7.2.27-1.w7                           webtatic                      3.1 M
 php72w-cli                           x86_64                      7.2.27-1.w7                           webtatic                      3.1 M
 php72w-common                        x86_64                      7.2.27-1.w7                           webtatic                      1.3 M
 php72w-devel                         x86_64                      7.2.27-1.w7                           webtatic                      2.8 M
 php72w-embedded                      x86_64                      7.2.27-1.w7                           webtatic                      1.5 M
 php72w-fpm                           x86_64                      7.2.27-1.w7                           webtatic                      1.6 M
 php72w-gd                            x86_64                      7.2.27-1.w7                           webtatic                      139 k
 php72w-mbstring                      x86_64                      7.2.27-1.w7                           webtatic                      587 k
 php72w-mysqlnd                       x86_64                      7.2.27-1.w7                           webtatic                      198 k
 php72w-opcache                       x86_64                      7.2.27-1.w7                           webtatic                      246 k
 php72w-pdo                           x86_64                      7.2.27-1.w7                           webtatic                       90 k
 php72w-xml                           x86_64                      7.2.27-1.w7                           webtatic                      123 k
Installing for dependencies:
 freetype                             x86_64                      2.8-14.el7                            base                          380 k
 libX11                               x86_64                      1.6.7-2.el7                           base                          607 k
 libX11-common                        noarch                      1.6.7-2.el7                           base                          164 k
 libXau                               x86_64                      1.0.8-2.1.el7                         base                           29 k
 libXpm                               x86_64                      3.5.12-1.el7                          base                           55 k
 libargon2                            x86_64                      20161029-3.el7                        epel                           23 k
 libjpeg-turbo                        x86_64                      1.2.90-8.el7                          base                          135 k
 libpng                               x86_64                      2:1.5.13-7.el7_2                      base                          213 k
 libxcb                               x86_64                      1.13-1.el7                            base                          214 k
 libxslt                              x86_64                      1.1.28-5.el7                          base                          242 k
 systemd-sysv                         x86_64                      219-67.el7_7.3                        updates                        88 k
Updating for dependencies:
 systemd                              x86_64                      219-67.el7_7.3                        updates                       5.1 M
 systemd-libs                         x86_64                      219-67.el7_7.3                        updates                       411 k

Transaction Summary
============================================================================================================================================
Install  12 Packages (+11 Dependent packages)
Upgrade              (  2 Dependent packages)

Total download size: 22 M
Downloading packages:
Delta RPMs disabled because /usr/bin/applydeltarpm not installed.
(1/25): freetype-2.8-14.el7.x86_64.rpm                                                                               | 380 kB  00:00:00
(2/25): libX11-1.6.7-2.el7.x86_64.rpm                                                                                | 607 kB  00:00:00
(3/25): libXau-1.0.8-2.1.el7.x86_64.rpm                                                                              |  29 kB  00:00:00
(4/25): libX11-common-1.6.7-2.el7.noarch.rpm                                                                         | 164 kB  00:00:00
(5/25): libXpm-3.5.12-1.el7.x86_64.rpm                                                                               |  55 kB  00:00:00
(6/25): libpng-1.5.13-7.el7_2.x86_64.rpm                                                                             | 213 kB  00:00:00
(7/25): libxcb-1.13-1.el7.x86_64.rpm                                                                                 | 214 kB  00:00:00
(8/25): libjpeg-turbo-1.2.90-8.el7.x86_64.rpm                                                                        | 135 kB  00:00:00
(9/25): libxslt-1.1.28-5.el7.x86_64.rpm                                                                              | 242 kB  00:00:00
(10/25): libargon2-20161029-3.el7.x86_64.rpm                                                                         |  23 kB  00:00:00
warning: /var/cache/yum/x86_64/7/webtatic/packages/php72w-common-7.2.27-1.w7.x86_64.rpm: Header V4 RSA/SHA1 Signature, key ID 62e74ca5: NOKEY
Public key for php72w-common-7.2.27-1.w7.x86_64.rpm is not installed
(11/25): php72w-common-7.2.27-1.w7.x86_64.rpm                                                                        | 1.3 MB  00:01:02
(12/25): mod_php72w-7.2.27-1.w7.x86_64.rpm                                                                           | 3.1 MB  00:01:09
(13/25): php72w-devel-7.2.27-1.w7.x86_64.rpm                                                                         | 2.8 MB  00:01:43
(14/25): php72w-gd-7.2.27-1.w7.x86_64.rpm                                                                            | 139 kB  00:00:09
(15/25): php72w-embedded-7.2.27-1.w7.x86_64.rpm                                                                      | 1.5 MB  00:01:05
(16/25): php72w-fpm-7.2.27-1.w7.x86_64.rpm                                                                           | 1.6 MB  00:00:42
(17/25): php72w-opcache-7.2.27-1.w7.x86_64.rpm                                                                       | 246 kB  00:00:10
(18/25): php72w-mysqlnd-7.2.27-1.w7.x86_64.rpm                                                                       | 198 kB  00:00:13
(19/25): php72w-mbstring-7.2.27-1.w7.x86_64.rpm                                                                      | 587 kB  00:00:16
(20/25): systemd-libs-219-67.el7_7.3.x86_64.rpm                                                                      | 411 kB  00:00:00
(21/25): systemd-sysv-219-67.el7_7.3.x86_64.rpm                                                                      |  88 kB  00:00:00
(22/25): systemd-219-67.el7_7.3.x86_64.rpm                                                                           | 5.1 MB  00:00:01
(23/25): php72w-xml-7.2.27-1.w7.x86_64.rpm                                                                           | 123 kB  00:00:04
(24/25): php72w-pdo-7.2.27-1.w7.x86_64.rpm                                                                           |  90 kB  00:00:05
(25/25): php72w-cli-7.2.27-1.w7.x86_64.rpm                                                                           | 3.1 MB  00:02:54
--------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                       130 kB/s |  22 MB  00:02:55
Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-webtatic-el7
Importing GPG key 0x62E74CA5:
 Userid     : "Webtatic EL7 <rpms@webtatic.com>"
 Fingerprint: 830d b159 6d9b 9b01 99dc 24a3 e87f d236 62e7 4ca5
 Package    : webtatic-release-7-3.noarch (installed)
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-webtatic-el7
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : php72w-common-7.2.27-1.w7.x86_64                                                                                        1/27
  Installing : libargon2-20161029-3.el7.x86_64                                                                                         2/27
  Updating   : systemd-libs-219-67.el7_7.3.x86_64                                                                                      3/27
  Updating   : systemd-219-67.el7_7.3.x86_64                                                                                           4/27
  Installing : 2:libpng-1.5.13-7.el7_2.x86_64                                                                                          5/27
  Installing : freetype-2.8-14.el7.x86_64                                                                                              6/27
  Installing : systemd-sysv-219-67.el7_7.3.x86_64                                                                                      7/27
  Installing : php72w-cli-7.2.27-1.w7.x86_64                                                                                           8/27
  Installing : php72w-pdo-7.2.27-1.w7.x86_64                                                                                           9/27
  Installing : libXau-1.0.8-2.1.el7.x86_64                                                                                            10/27
  Installing : libxcb-1.13-1.el7.x86_64                                                                                               11/27
  Installing : libxslt-1.1.28-5.el7.x86_64                                                                                            12/27
  Installing : libjpeg-turbo-1.2.90-8.el7.x86_64                                                                                      13/27
  Installing : libX11-common-1.6.7-2.el7.noarch                                                                                       14/27
  Installing : libX11-1.6.7-2.el7.x86_64                                                                                              15/27
  Installing : libXpm-3.5.12-1.el7.x86_64                                                                                             16/27
  Installing : php72w-gd-7.2.27-1.w7.x86_64                                                                                           17/27
  Installing : php72w-xml-7.2.27-1.w7.x86_64                                                                                          18/27
  Installing : php72w-mysqlnd-7.2.27-1.w7.x86_64                                                                                      19/27
  Installing : php72w-devel-7.2.27-1.w7.x86_64                                                                                        20/27
  Installing : php72w-fpm-7.2.27-1.w7.x86_64                                                                                          21/27
  Installing : mod_php72w-7.2.27-1.w7.x86_64                                                                                          22/27
  Installing : php72w-embedded-7.2.27-1.w7.x86_64                                                                                     23/27
  Installing : php72w-mbstring-7.2.27-1.w7.x86_64                                                                                     24/27
  Installing : php72w-opcache-7.2.27-1.w7.x86_64                                                                                      25/27
  Cleanup    : systemd-219-62.el7_6.5.x86_64                                                                                          26/27
  Cleanup    : systemd-libs-219-62.el7_6.5.x86_64                                                                                     27/27
  Verifying  : php72w-pdo-7.2.27-1.w7.x86_64                                                                                           1/27
  Verifying  : php72w-xml-7.2.27-1.w7.x86_64                                                                                           2/27
  Verifying  : php72w-mbstring-7.2.27-1.w7.x86_64                                                                                      3/27
  Verifying  : php72w-mysqlnd-7.2.27-1.w7.x86_64                                                                                       4/27
  Verifying  : 2:libpng-1.5.13-7.el7_2.x86_64                                                                                          5/27
  Verifying  : libargon2-20161029-3.el7.x86_64                                                                                         6/27
  Verifying  : freetype-2.8-14.el7.x86_64                                                                                              7/27
  Verifying  : php72w-common-7.2.27-1.w7.x86_64                                                                                        8/27
  Verifying  : mod_php72w-7.2.27-1.w7.x86_64                                                                                           9/27
  Verifying  : php72w-devel-7.2.27-1.w7.x86_64                                                                                        10/27
  Verifying  : php72w-gd-7.2.27-1.w7.x86_64                                                                                           11/27
  Verifying  : php72w-fpm-7.2.27-1.w7.x86_64                                                                                          12/27
  Verifying  : libX11-1.6.7-2.el7.x86_64                                                                                              13/27
  Verifying  : libX11-common-1.6.7-2.el7.noarch                                                                                       14/27
  Verifying  : libxcb-1.13-1.el7.x86_64                                                                                               15/27
  Verifying  : php72w-opcache-7.2.27-1.w7.x86_64                                                                                      16/27
  Verifying  : libXpm-3.5.12-1.el7.x86_64                                                                                             17/27
  Verifying  : libjpeg-turbo-1.2.90-8.el7.x86_64                                                                                      18/27
  Verifying  : systemd-libs-219-67.el7_7.3.x86_64                                                                                     19/27
  Verifying  : systemd-219-67.el7_7.3.x86_64                                                                                          20/27
  Verifying  : libxslt-1.1.28-5.el7.x86_64                                                                                            21/27
  Verifying  : systemd-sysv-219-67.el7_7.3.x86_64                                                                                     22/27
  Verifying  : libXau-1.0.8-2.1.el7.x86_64                                                                                            23/27
  Verifying  : php72w-embedded-7.2.27-1.w7.x86_64                                                                                     24/27
  Verifying  : php72w-cli-7.2.27-1.w7.x86_64                                                                                          25/27
  Verifying  : systemd-libs-219-62.el7_6.5.x86_64                                                                                     26/27
  Verifying  : systemd-219-62.el7_6.5.x86_64                                                                                          27/27

Installed:
  mod_php72w.x86_64 0:7.2.27-1.w7               php72w-cli.x86_64 0:7.2.27-1.w7                php72w-common.x86_64 0:7.2.27-1.w7
  php72w-devel.x86_64 0:7.2.27-1.w7             php72w-embedded.x86_64 0:7.2.27-1.w7           php72w-fpm.x86_64 0:7.2.27-1.w7
  php72w-gd.x86_64 0:7.2.27-1.w7                php72w-mbstring.x86_64 0:7.2.27-1.w7           php72w-mysqlnd.x86_64 0:7.2.27-1.w7
  php72w-opcache.x86_64 0:7.2.27-1.w7           php72w-pdo.x86_64 0:7.2.27-1.w7                php72w-xml.x86_64 0:7.2.27-1.w7

Dependency Installed:
  freetype.x86_64 0:2.8-14.el7   libX11.x86_64 0:1.6.7-2.el7         libX11-common.noarch 0:1.6.7-2.el7     libXau.x86_64 0:1.0.8-2.1.el7
  libXpm.x86_64 0:3.5.12-1.el7   libargon2.x86_64 0:20161029-3.el7   libjpeg-turbo.x86_64 0:1.2.90-8.el7    libpng.x86_64 2:1.5.13-7.el7_2
  libxcb.x86_64 0:1.13-1.el7     libxslt.x86_64 0:1.1.28-5.el7       systemd-sysv.x86_64 0:219-67.el7_7.3

Dependency Updated:
  systemd.x86_64 0:219-67.el7_7.3                                    systemd-libs.x86_64 0:219-67.el7_7.3

Complete!
[root@a1f530aec186 ~]# php -v
PHP 7.2.27 (cli) (built: Jan 26 2020 15:49:49) ( NTS )
Copyright (c) 1997-2018 The PHP Group
Zend Engine v3.2.0, Copyright (c) 1998-2018 Zend Technologies
    with Zend OPcache v7.2.27, Copyright (c) 1999-2018, by Zend Technologies
[root@a1f530aec186 ~]# php -m
[PHP Modules]
bz2
calendar
Core
ctype
curl
date
dom
exif
fileinfo
filter
ftp
gd
gettext
gmp
hash
iconv
json
libxml
mbstring
mysqli
mysqlnd
openssl
pcntl
pcre
PDO
pdo_mysql
pdo_sqlite
Phar
readline
Reflection
session
shmop
SimpleXML
sockets
SPL
sqlite3
standard
tokenizer
wddx
xml
xmlreader
xmlwriter
xsl
Zend OPcache
zip
zlib

[Zend Modules]
Zend OPcache

[root@a1f530aec186 ~]#
```
- 安装php xdebug模式

```sh
[root@a1f530aec186 ~]# yum install pecl -y
[root@a1f530aec186 ~]# pecl install xdebug
WARNING: channel "pecl.php.net" has updated its protocols, use "pecl channel-update pecl.php.net" to update
downloading xdebug-2.9.2.tgz ...
Starting to download xdebug-2.9.2.tgz (242,959 bytes)
..................................................done: 242,959 bytes
90 source files, building
running: make INSTALL_ROOT="/var/tmp/pear-build-defaultuserUJOuP7/install-xdebug-2.9.2" install
Installing shared extensions:     /var/tmp/pear-build-defaultuserUJOuP7/install-xdebug-2.9.2/usr/lib64/php/modules/

  +----------------------------------------------------------------------+
  |                                                                      |
  |   INSTALLATION INSTRUCTIONS                                          |
  |   =========================                                          |
  |                                                                      |
  |   See https://xdebug.org/install.php#configure-php for instructions  |
  |   on how to enable Xdebug for PHP.                                   |
  |                                                                      |
  |   Documentation is available online as well:                         |
  |   - A list of all settings:  https://xdebug.org/docs-settings.php    |
  |   - A list of all functions: https://xdebug.org/docs-functions.php   |
  |   - Profiling instructions:  https://xdebug.org/docs-profiling2.php  |
  |   - Remote debugging:        https://xdebug.org/docs-debugger.php    |
  |                                                                      |
  |                                                                      |
  |   NOTE: Please disregard the message                                 |
  |       You should add "extension=xdebug.so" to php.ini                |
  |   that is emitted by the PECL installer. This does not work for      |
  |   Xdebug.                                                            |
  |                                                                      |
  +----------------------------------------------------------------------+


running: find "/var/tmp/pear-build-defaultuserUJOuP7/install-xdebug-2.9.2" | xargs ls -dils
2360032    4 drwxr-xr-x 3 root root    4096 Mar  4 00:18 /var/tmp/pear-build-defaultuserUJOuP7/install-xdebug-2.9.2
2360132    4 drwxr-xr-x 3 root root    4096 Mar  4 00:18 /var/tmp/pear-build-defaultuserUJOuP7/install-xdebug-2.9.2/usr
2360133    4 drwxr-xr-x 3 root root    4096 Mar  4 00:18 /var/tmp/pear-build-defaultuserUJOuP7/install-xdebug-2.9.2/usr/lib64
2360134    4 drwxr-xr-x 3 root root    4096 Mar  4 00:18 /var/tmp/pear-build-defaultuserUJOuP7/install-xdebug-2.9.2/usr/lib64/php
2360135    4 drwxr-xr-x 2 root root    4096 Mar  4 00:18 /var/tmp/pear-build-defaultuserUJOuP7/install-xdebug-2.9.2/usr/lib64/php/modules
2360131 1468 -rwxr-xr-x 1 root root 1500096 Mar  4 00:18 /var/tmp/pear-build-defaultuserUJOuP7/install-xdebug-2.9.2/usr/lib64/php/modules/xdebug.so

Build process completed successfully
Installing '/usr/lib64/php/modules/xdebug.so'
install ok: channel://pecl.php.net/xdebug-2.9.2
configuration option "php_ini" is not set to php.ini location
You should add "zend_extension=/usr/lib64/php/modules/xdebug.so" to php.ini
[root@a1f530aec186 ~]#

# 修改配置文件/etc/php.ini

# 将以下内容添加到/etc/php.ini文件的最后一行
zend_extension=/usr/lib64/php/modules/xdebug.so

# 添加完成后，查看`php -m`
[root@a1f530aec186 ~]# php -m|grep debug
xdebug
Xdebug
....

说明配置正常。

- php-fpm开机自启

```sh
[root@a1f530aec186 ~]# systemctl enable php-fpm
Created symlink from /etc/systemd/system/multi-user.target.wants/php-fpm.service to /usr/lib/systemd/system/php-fpm.service.
[root@a1f530aec186 ~]# systemctl start php-fpm
[root@a1f530aec186 ~]# systemctl status php-fpm
● php-fpm.service - The PHP FastCGI Process Manager
   Loaded: loaded (/usr/lib/systemd/system/php-fpm.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2020-03-04 00:31:31 CST; 8s ago
 Main PID: 4792 (php-fpm)
   Status: "Ready to handle connections"
   CGroup: /docker/a1f530aec1866a4ac1562b3c03a1380c4022b87df4dd48c7c0068d040f9355db/docker/a1f530aec1866a4ac1562b3c03a1380c4022b87df4dd48c7c0068d040f9355db/system.slice/php-fpm.service
           ├─4792 php-fpm: master process (/etc/php-fpm.conf)
           ├─4793 php-fpm: pool www
           ├─4794 php-fpm: pool www
           ├─4795 php-fpm: pool www
           ├─4796 php-fpm: pool www
           └─4797 php-fpm: pool www
           ‣ 4792 php-fpm: master process (/etc/php-fpm.conf)

Mar 04 00:31:31 a1f530aec186 systemd[1]: Starting The PHP FastCGI Process Manager...
Mar 04 00:31:31 a1f530aec186 systemd[1]: Started The PHP FastCGI Process Manager.
[root@a1f530aec186 ~]# ps -ef|grep php
root      4792     1  0 00:31 ?        00:00:00 php-fpm: master process (/etc/php-fpm.conf)
apache    4793  4792  0 00:31 ?        00:00:00 php-fpm: pool www
apache    4794  4792  0 00:31 ?        00:00:00 php-fpm: pool www
apache    4795  4792  0 00:31 ?        00:00:00 php-fpm: pool www
apache    4796  4792  0 00:31 ?        00:00:00 php-fpm: pool www
apache    4797  4792  0 00:31 ?        00:00:00 php-fpm: pool www
root      4800  1519  0 00:31 pts/0    00:00:00 grep --color=auto php
[root@a1f530aec186 ~]# netstat -tunlp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      726/sshd
tcp        0      0 127.0.0.1:9000          0.0.0.0:*               LISTEN      4792/php-fpm: maste
tcp6       0      0 :::22                   :::*                    LISTEN      726/sshd
[root@a1f530aec186 ~]#
```

可以看到php-fpm监听着9000端口。

# 安装subversion环境

 - 添加subversion yum源

```sh
cat > /etc/yum.repos.d/wandisco-svn.repo << EOF
[WandiscoSVN]
name=Wandisco SVN Repo
baseurl=http://opensource.wandisco.com/centos/7/svn-1.11/RPMS/\$basearch/
enabled=1
gpgcheck=0
EOF

# 上面命令具体执行时显示如下：
[root@a1f530aec186 ~]# cat > /etc/yum.repos.d/wandisco-svn.repo << EOF
> [WandiscoSVN]
> name=Wandisco SVN Repo
> baseurl=http://opensource.wandisco.com/centos/7/svn-1.11/RPMS/\$basearch/
> enabled=1
> gpgcheck=0
> EOF

[root@a1f530aec186 ~]# cat /etc/yum.repos.d/wandisco-svn.repo
[WandiscoSVN]
name=Wandisco SVN Repo
baseurl=http://opensource.wandisco.com/centos/7/svn-1.11/RPMS/$basearch/
enabled=1
gpgcheck=0
[root@a1f530aec186 ~]#
```
- 安装

```sh
[root@a1f530aec186 ~]# yum install subversion-1.11.0-1 mod_dav_svn-1.11.0-1 -y
Loaded plugins: fastestmirror, ovl
Loading mirror speeds from cached hostfile
 * base: mirrors.163.com
 * epel: ftp.iij.ad.jp
 * extras: mirrors.163.com
 * ius: mirrors.tuna.tsinghua.edu.cn
 * updates: mirrors.163.com
 * webtatic: uk.repo.webtatic.com
WandiscoSVN                                                                                                          | 2.9 kB  00:00:00
WandiscoSVN/x86_64/primary_db                                                                                        |  22 kB  00:00:00
Resolving Dependencies
--> Running transaction check
---> Package mod_dav_svn.x86_64 0:1.11.0-1 will be installed
---> Package subversion.x86_64 0:1.11.0-1 will be installed
--> Processing Dependency: libserf-1.so.0()(64bit) for package: subversion-1.11.0-1.x86_64
--> Running transaction check
---> Package libserf.x86_64 0:1.3.9-1.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================================================================
 Package                           Arch                         Version                             Repository                         Size
============================================================================================================================================
Installing:
 mod_dav_svn                       x86_64                       1.11.0-1                            WandiscoSVN                        87 k
 subversion                        x86_64                       1.11.0-1                            WandiscoSVN                       2.6 M
Installing for dependencies:
 libserf                           x86_64                       1.3.9-1.el7                         WandiscoSVN                        52 k

Transaction Summary
============================================================================================================================================
Install  2 Packages (+1 Dependent package)

Total download size: 2.8 M
Installed size: 9.4 M
Downloading packages:
(1/3): libserf-1.3.9-1.el7.x86_64.rpm                                                                                |  52 kB  00:00:00
(2/3): mod_dav_svn-1.11.0-1.x86_64.rpm                                                                               |  87 kB  00:00:00
(3/3): subversion-1.11.0-1.x86_64.rpm                                                                                | 2.6 MB  00:00:01
--------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                       1.7 MB/s | 2.8 MB  00:00:01
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : libserf-1.3.9-1.el7.x86_64                                                                                               1/3
  Installing : subversion-1.11.0-1.x86_64                                                                                               2/3
  Installing : mod_dav_svn-1.11.0-1.x86_64                                                                                              3/3
  Verifying  : libserf-1.3.9-1.el7.x86_64                                                                                               1/3
  Verifying  : mod_dav_svn-1.11.0-1.x86_64                                                                                              2/3
  Verifying  : subversion-1.11.0-1.x86_64                                                                                               3/3

Installed:
  mod_dav_svn.x86_64 0:1.11.0-1                                         subversion.x86_64 0:1.11.0-1

Dependency Installed:
  libserf.x86_64 0:1.3.9-1.el7

Complete!
[root@a1f530aec186 ~]#
```

- 查看SVN版本信息

```sh
[root@a1f530aec186 ~]# svn --version
svn, version 1.11.0 (r1845130)
   compiled Nov  1 2018, 12:32:40 on x86_64-redhat-linux-gnu

Copyright (C) 2018 The Apache Software Foundation.
This software consists of contributions made by many people;
see the NOTICE file for more information.
Subversion is open source software, see http://subversion.apache.org/

The following repository access (RA) modules are available:

* ra_svn : Module for accessing a repository using the svn network protocol.
  - with Cyrus SASL authentication
  - handles 'svn' scheme
* ra_local : Module for accessing a repository on local disk.
  - handles 'file' scheme
* ra_serf : Module for accessing a repository via WebDAV protocol using serf.
  - using serf 1.3.9 (compiled with 1.3.8)
  - handles 'http' scheme
  - handles 'https' scheme

The following authentication credential caches are available:

* Plaintext cache in /root/.subversion
* Gnome Keyring
* GPG-Agent

[root@a1f530aec186 ~]# svn  <-- 此处按了两次tab键，查看svn查关命令
svn            svnadmin       svndumpfilter  svnfsfs        svnlook        svnrdump       svnserve       svnsync        svnversion
[root@a1f530aec186 ~]# svn
```

- 创建SVN测试数据

```sh
# 创建密码文件，并设置admin账号和密码
[root@a1f530aec186 ~]# htpasswd -c -b /home/svn/passwd admin admin
Adding password for user admin
[root@a1f530aec186 ~]# cat /home/svn/passwd
admin:$apr1$1u/XWzHD$9AsQjIW3t/uP2In0C5GCs0

# 创建密码文件
[root@a1f530aec186 ~]# cat > /home/svn/authz << EOF
> [/]
> admin = rw
> EOF
[root@a1f530aec186 ~]# cat /home/svn/authz
[/]
admin = rw

# 添加httpd配置文件
cat > /etc/httpd/conf.d/subversion.conf << EOF
<Location /svn>
        DAV svn
        SVNParentPath /home/svn/svnrepos
        AuthType Basic
        AuthName "SVN Repository"
        AuthUserFile /home/svn/passwd
        AuthzSVNAccessFile /home/svn/authz
        Require valid-user
</Location> 
EOF

# 以上命令执行如下：
[root@a1f530aec186 ~]# cat > /etc/httpd/conf.d/subversion.conf << EOF
> <Location /svn>
>         DAV svn
>         SVNParentPath /home/svn/svnrepos
>         AuthType Basic
>         AuthName "SVN Repository"
>         AuthUserFile /home/svn/passwd
>         AuthzSVNAccessFile /home/svn/authz
>         Require valid-user
> </Location>
> EOF

[root@a1f530aec186 ~]# cat /etc/httpd/conf.d/subversion.conf
<Location /svn>
        DAV svn
        SVNParentPath /home/svn/svnrepos
        AuthType Basic
        AuthName "SVN Repository"
        AuthUserFile /home/svn/passwd
        AuthzSVNAccessFile /home/svn/authz
        Require valid-user
</Location>

# 添加lib库
[root@a1f530aec186 ~]# cat /etc/httpd/conf.modules.d/00-dav.conf
LoadModule dav_module modules/mod_dav.so
LoadModule dav_fs_module modules/mod_dav_fs.so
LoadModule dav_lock_module modules/mod_dav_lock.so
[root@a1f530aec186 ~]# echo "LoadModule dav_svn_module     modules/mod_dav_svn.so" >> /etc/httpd/conf.modules.d/00-dav.conf
[root@a1f530aec186 ~]# echo "LoadModule authz_svn_module   modules/mod_authz_svn.so" >> /etc/httpd/conf.modules.d/00-dav.conf
[root@a1f530aec186 ~]# cat /etc/httpd/conf.modules.d/00-dav.conf
LoadModule dav_module modules/mod_dav.so
LoadModule dav_fs_module modules/mod_dav_fs.so
LoadModule dav_lock_module modules/mod_dav_lock.so
LoadModule dav_svn_module     modules/mod_dav_svn.so
LoadModule authz_svn_module   modules/mod_authz_svn.so

# 添加httpd svn utf-8支持
cat >> /etc/httpd/conf/httpd.conf << EOF
<IfModule mod_dav_fs.c>
    # Location of the WebDAV lock database.
    DAVLockDB /var/lib/dav/lockdb
    SVNUseUTF8 On
</IfModule>
EOF

[root@a1f530aec186 ~]# cat >> /etc/httpd/conf/httpd.conf << EOF
> <IfModule mod_dav_fs.c>
>     # Location of the WebDAV lock database.
>     DAVLockDB /var/lib/dav/lockdb
>     SVNUseUTF8 On
> </IfModule>
> EOF

# 查看配置文件最后10行内容
[root@a1f530aec186 ~]# tail -f /etc/httpd/conf/httpd.conf

# Supplemental configuration
#
# Load config files in the "/etc/httpd/conf.d" directory, if any.
IncludeOptional conf.d/*.conf
<IfModule mod_dav_fs.c>
    # Location of the WebDAV lock database.
    DAVLockDB /var/lib/dav/lockdb
    SVNUseUTF8 On
</IfModule>

# 修改httpd的ServerName
[root@a1f530aec186 ~]# sed '/#ServerName www.example.com:80/a ServerName 127.0.0.1:80' /etc/httpd/conf/httpd.conf|grep -n 'ServerName'
89:# ServerName gives the name and port that the server uses to identify itself.
95:#ServerName www.example.com:80
96:ServerName 127.0.0.1:80
[root@a1f530aec186 ~]# sed -i '/#ServerName www.example.com:80/a ServerName 127.0.0.1:80' /etc/httpd/conf/httpd.conf
[root@a1f530aec186 ~]# grep -n 'ServerName' /etc/httpd/conf/httpd.conf
89:# ServerName gives the name and port that the server uses to identify itself.
95:#ServerName www.example.com:80
96:ServerName 127.0.0.1:80

# 检查httpd配置是否正确
[root@a1f530aec186 ~]# httpd -t
Syntax OK
```

- 创建SVN测试数据

```sh
# 创建SVN根目录
[root@a1f530aec186 ~]# SVN_REPO_HOME="/home/svn/svnrepos"
[root@a1f530aec186 ~]# mkdir -p $SVN_REPO_HOME
[root@a1f530aec186 ~]# ls -lah /home/svn/
total 12K
drwxr-xr-x 3 root root 4.0K Mar  4 00:45 .
drwxr-xr-x 1 root root 4.0K Mar  4 00:45 ..
drwxr-xr-x 2 root root 4.0K Mar  4 00:45 svnrepos

# 创建SVN测试仓库testinfo
root@a1f530aec186 ~]# svnadmin create /home/svn/svnrepos/testinfo
[root@a1f530aec186 ~]# ls -lah /home/svn/svnrepos/
total 12K
drwxr-xr-x 3 root root 4.0K Mar  4 01:11 .
drwxr-xr-x 3 root root 4.0K Mar  4 00:54 ..
drwxr-xr-x 6 root root 4.0K Mar  4 01:11 testinfo

# 修改SVN根目录权限
[root@a1f530aec186 ~]# chown -R apache:apache /home/svn
[root@a1f530aec186 ~]# ls -lah /home/svn/svnrepos/
total 12K
drwxr-xr-x 3 apache apache 4.0K Mar  4 01:11 .
drwxr-xr-x 3 apache apache 4.0K Mar  4 00:54 ..
drwxr-xr-x 6 apache apache 4.0K Mar  4 01:11 testinfo
[root@a1f530aec186 ~]# ls -lah /home/svn/
total 20K
drwxr-xr-x 3 apache apache 4.0K Mar  4 00:54 .
drwxr-xr-x 1 root   root   4.0K Mar  4 00:45 ..
-rw-r--r-- 1 apache apache   15 Mar  4 00:54 authz
-rw-r--r-- 1 apache apache   44 Mar  4 00:52 passwd
drwxr-xr-x 3 apache apache 4.0K Mar  4 01:11 svnrepos
```

- 创建SVN服务

```sh
# 添加服务
cat > /usr/lib/systemd/system/svnserve.service << EOF
[Unit]
Description=Subversion server daemon
Documentation=man:svnserve(8) man:svnserve.conf(5)
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/usr/bin/svnserve --daemon --root=${SVN_REPO_HOME} --pid-file=/var/run/svnserve.pid
ExecStop=/bin/kill -HUP \${MAINPID}

[Install]  
WantedBy=multi-user.target
EOF

# 以上命令执行时显示如下：
[root@a1f530aec186 ~]# cat > /usr/lib/systemd/system/svnserve.service << EOF
> [Unit]
> Description=Subversion server daemon
> Documentation=man:svnserve(8) man:svnserve.conf(5)
> After=syslog.target network.target
>
> [Service]
> Type=forking
> ExecStart=/usr/bin/svnserve --daemon --root=${SVN_REPO_HOME} --pid-file=/var/run/svnserve.pid
> ExecStop=/bin/kill -HUP \${MAINPID}
>
> [Install]
> WantedBy=multi-user.target
> EOF
[root@a1f530aec186 ~]#
```



- 重启服务

```sh
systemctl daemon-reload
systemctl enable svnserve
systemctl start svnserve
systemctl status svnserve
systemctl enable httpd
systemctl start httpd
systemctl status httpd


[root@a1f530aec186 ~]# systemctl daemon-reload
[root@a1f530aec186 ~]# systemctl enable svnserve
Created symlink from /etc/systemd/system/multi-user.target.wants/svnserve.service to /usr/lib/systemd/system/svnserve.service.
[root@a1f530aec186 ~]# systemctl start svnserve
[root@a1f530aec186 ~]# systemctl status svnserve
● svnserve.service - Subversion server daemon
   Loaded: loaded (/usr/lib/systemd/system/svnserve.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2020-03-04 01:15:57 CST; 9s ago
     Docs: man:svnserve(8)
           man:svnserve.conf(5)
  Process: 4904 ExecStart=/usr/bin/svnserve --daemon --root=/home/svn/svnrepos --pid-file=/var/run/svnserve.pid (code=exited, status=0/SUCCESS)
 Main PID: 4905 (svnserve)
   CGroup: /docker/a1f530aec1866a4ac1562b3c03a1380c4022b87df4dd48c7c0068d040f9355db/docker/a1f530aec1866a4ac1562b3c03a1380c4022b87df4dd48c7c0068d040f9355db/system.slice/svnserve.service
           └─4905 /usr/bin/svnserve --daemon --root=/home/svn/svnrepos --pid-file=/var/run/svnserve.pid
           ‣ 4905 /usr/bin/svnserve --daemon --root=/home/svn/svnrepos --pid-file=/var/run/svnserve.pid

Mar 04 01:15:57 a1f530aec186 systemd[1]: Starting Subversion server daemon...
Mar 04 01:15:57 a1f530aec186 systemd[1]: Started Subversion server daemon.
[root@a1f530aec186 ~]# systemctl enable httpd
Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service.
[root@a1f530aec186 ~]# systemctl start httpd
[root@a1f530aec186 ~]# systemctl status httpd
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2020-03-04 01:16:21 CST; 5s ago
     Docs: man:httpd(8)
           man:apachectl(8)
 Main PID: 4922 (httpd)
   Status: "Processing requests..."
   CGroup: /docker/a1f530aec1866a4ac1562b3c03a1380c4022b87df4dd48c7c0068d040f9355db/docker/a1f530aec1866a4ac1562b3c03a1380c4022b87df4dd48c7c0068d040f9355db/system.slice/httpd.service
           ├─4922 /usr/sbin/httpd -DFOREGROUND
           ├─4923 /usr/sbin/httpd -DFOREGROUND
           ├─4924 /usr/sbin/httpd -DFOREGROUND
           ├─4925 /usr/sbin/httpd -DFOREGROUND
           ├─4926 /usr/sbin/httpd -DFOREGROUND
           └─4927 /usr/sbin/httpd -DFOREGROUND
           ‣ 4922 /usr/sbin/httpd -DFOREGROUND

Mar 04 01:16:21 a1f530aec186 systemd[1]: Starting The Apache HTTP Server...
Mar 04 01:16:21 a1f530aec186 systemd[1]: Started The Apache HTTP Server.
[root@a1f530aec186 ~]#
```

至此，centos7中的php7.2和svn环境都配置完成，

下面将容器提交到hub仓库中。

## 提交容器镜像到hub仓库

- 打包提交

```sh
# 查看正在运行的容器
 $ docker ps 
CONTAINER ID        IMAGE                         COMMAND             CREATED             STATUS              PORTS               NAMES
a1f530aec186        meizhaohui/meicentos:latest   "usr/sbin/init"     About an hour ago   Up About an hour                        mycentos

# 打包容器成为镜像
 $ docker commit -a "meizhaohui" -m"centos7 with php7.2 and subversion environment;add Xdebug mode to PHP and create test svn data and svnserve" a1f530aec186 meizhaohui/centos_php_svn:latest
sha256:965a0413bc4c999c18ffbff54a8febe5c602b1b090f3690510ab2a70fda40e86

# 其中，-a: 提交镜像的作者，-m：提交时的说明文字，a1f..为容器id, meizhaohui/centos_php_svn:latest为打包的镜像和标签


 $ docker ps -a
CONTAINER ID        IMAGE                         COMMAND             CREATED             STATUS              PORTS               NAMES
a1f530aec186        meizhaohui/meicentos:latest   "usr/sbin/init"     2 hours ago         Up 2 hours                              mycentos

# 再次查看镜像，可以看到本地多出了刚才制作的镜像
 $ docker images
REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
meizhaohui/centos_php_svn   latest              965a0413bc4c        4 minutes ago       983MB
nginx                       latest              a1523e859360        5 days ago          127MB
meizhaohui/meicentos        latest              e64cd9abd46d        10 months ago       710MB

# 登陆hub仓库
 $ docker login
Authenticating with existing credentials...
Login Succeeded

# 提交镜像
 $ docker push meizhaohui/centos_php_svn
The push refers to repository [docker.io/meizhaohui/centos_php_svn]
bd4118a4d75e: Pushing  116.4MB/272.3MB
bd4118a4d75e: Pushed 
d69483a6face: Mounted from meizhaohui/meicentos 

latest: digest: sha256:818acbee0a4144a9febdddde4a4a18f827bcf3cd6348c97d3a215070f9e1fd4a size: 954
```

- 修改镜像基本信息

登陆[https://hub.docker.com/repository/docker/meizhaohui/centos_php_svn](https://hub.docker.com/repository/docker/meizhaohui/centos_php_svn), 可以看新的镜像已经上传成功，只是基本信息没有填写。

如基本信息改成以下内容：

    Configured with PHP 7.2.27 with Xdebug and SVN 1.11.Auto start httpd and svnserve service.


# 使用新镜像运行web服务

$ docker run --name centos_php_svn --privileged -p 8080:80 -p 9001:9001  -d meizhaohui/centos_php_svn:latest

```sh
# 下载最新镜像
meizhaohui@MacBook:/Users/meizhaohui $ docker pull meizhaohui/centos_php_svn
Using default tag: latest
latest: Pulling from meizhaohui/centos_php_svn
Digest: sha256:818acbee0a4144a9febdddde4a4a18f827bcf3cd6348c97d3a215070f9e1fd4a
Status: Image is up to date for meizhaohui/centos_php_svn:latest
docker.io/meizhaohui/centos_php_svn:latest

# 同时开发docker容器中两个端口，并映射到本机上
# 容器中80端口映射到本机的8080端口，
meizhaohui@MacBook:/Users/meizhaohui $ docker run --name centos_php_svn --privileged -p 8080:80 -p 9001:9000 -d meizhaohui/centos_php_svn:latest
80006f0526ecb4a48dab772ad5a78154dbbd6a432c27099bb07b33ef7251417a

# 查看容器运行情况
meizhaohui@MacBook:/Users/meizhaohui $ docker ps
CONTAINER ID        IMAGE                              COMMAND             CREATED             STATUS              PORTS                                          NAMES
80006f0526ec        meizhaohui/centos_php_svn:latest   "usr/sbin/init"     5 seconds ago       Up 4 seconds        0.0.0.0:9001->9000/tcp, 0.0.0.0:8080->80/tcp   centos_php_svn
a1f530aec186        meizhaohui/meicentos:latest        "usr/sbin/init"     2 hours ago         Up 2 hours                                                         mycentos
```

- 验证web网页是否正常运行

访问[http://localhost:8080/svn/testinfo/](http://localhost:8080/svn/testinfo/)，可以正常打开页面提示框，输入用户名admin和密码admin,可以正常打开SVN页面，并看到页面显示`testinfo - Revision 0: /`，说明Apache和SVN运行正常。

访问[http://localhost:9001/](http://localhost:9001/)，不能正常显示，原因不明。



## 普通用户运行docker命令

如让`meizhaohui`这个普通用户能够运行docker命令，则只需要执行以下命令即可：

```sh
$ sudo gpasswd -a meizhaohui docker
```

这样就将普通用户加入到`docker`组中，然后退出远程连接，再重新连接服务器，此时就可以以普通用户执行docker命令了。
