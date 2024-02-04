# 查看下载的docker镜像的版本信息

[[toc]]

## 1. 现象描述

通常我们喜欢使用`docker pull 镜像名`这种方式下载docker镜像，如下载`redis`或`nginx`镜像：

```sh
# 下载redis镜像
[root@node1 ~]# docker pull redis
Using default tag: latest
latest: Pulling from library/redis
Digest: sha256:b0bdc1a83caf43f9eb74afca0fcfd6f09bea38bb87f6add4a858f06ef4617538
Status: Image is up to date for redis:latest
docker.io/library/redis:latest

# 下载nginx镜像
[root@node1 ~]# docker pull nginx
Using default tag: latest
latest: Pulling from library/nginx
Digest: sha256:67f9a4f10d147a6e04629340e6493c9703300ca23a2f7f3aa56fe615d75d31ca
Status: Image is up to date for nginx:latest
docker.io/library/nginx:latest
```

当我们不指定标签名称时，docker默认会下载最新的`latest`镜像，此时查看镜像信息：

```sh
[root@node1 ~]# docker images redis
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
redis        latest    e0ce02f88e58   2 weeks ago   130MB
[root@node1 ~]# docker images nginx
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    89da1fb6dcb9   2 weeks ago   187MB
[root@node1 ~]#
```

可以看到，redis和nginx的标签都是`latest`，我们不知道其具体的版本信息。特别是过段时间回来再看这些镜像，不知道其版本号是多少，这时候就容易让人迷糊。

## 2. 通过元数据查看镜像版本信息

我们可以通过`docker inspect`来获取docker镜像的元数据，在元数据中找版本信息。

如查看`redis`镜像的元数据：

```sh
[root@node1 ~]# docker inspect $(docker images -q redis)
[
  {
    "Id": "sha256:e0ce02f88e589621ae0c99073142b587c1bbe3cfbab70b484e7af700d7057e0e",
    "RepoTags": [
      "redis:latest"
    ],
    "RepoDigests": [
      "redis@sha256:b0bdc1a83caf43f9eb74afca0fcfd6f09bea38bb87f6add4a858f06ef4617538"
    ],
    "Parent": "",
    "Comment": "",
    "Created": "2023-07-28T14:21:59.941273751Z",
    "Container": "626e72d72b6d44575942c41f7beaedbb45fe110af5f228e511d813fcbe1b0447",
    "ContainerConfig": {
      "Hostname": "626e72d72b6d",
      "Domainname": "",
      "User": "",
      "AttachStdin": false,
      "AttachStdout": false,
      "AttachStderr": false,
      "ExposedPorts": {
        "6379/tcp": {}
      },
      "Tty": false,
      "OpenStdin": false,
      "StdinOnce": false,
      "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "GOSU_VERSION=1.16",
        "REDIS_VERSION=7.0.12",
        "REDIS_DOWNLOAD_URL=http://download.redis.io/releases/redis-7.0.12.tar.gz",
        "REDIS_DOWNLOAD_SHA=9dd83d5b278bb2bf0e39bfeb75c3e8170024edbaf11ba13b7037b2945cf48ab7"
      ],
      "Cmd": [
        "/bin/sh",
        "-c",
        "#(nop) ",
        "CMD [\"redis-server\"]"
      ],
      "Image": "sha256:704697321bb76bf7c8f21fd065c355417b05f4da9ba3abf578dd1309447bc8d1",
      "Volumes": {
        "/data": {}
      },
      "WorkingDir": "/data",
      "Entrypoint": [
        "docker-entrypoint.sh"
      ],
      "OnBuild": null,
      "Labels": {}
    },
    "DockerVersion": "20.10.23",
    "Author": "",
    "Config": {
      "Hostname": "",
      "Domainname": "",
      "User": "",
      "AttachStdin": false,
      "AttachStdout": false,
      "AttachStderr": false,
      "ExposedPorts": {
        "6379/tcp": {}
      },
      "Tty": false,
      "OpenStdin": false,
      "StdinOnce": false,
      "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "GOSU_VERSION=1.16",
        "REDIS_VERSION=7.0.12",
        "REDIS_DOWNLOAD_URL=http://download.redis.io/releases/redis-7.0.12.tar.gz",
        "REDIS_DOWNLOAD_SHA=9dd83d5b278bb2bf0e39bfeb75c3e8170024edbaf11ba13b7037b2945cf48ab7"
      ],
      "Cmd": [
        "redis-server"
      ],
      "Image": "sha256:704697321bb76bf7c8f21fd065c355417b05f4da9ba3abf578dd1309447bc8d1",
      "Volumes": {
        "/data": {}
      },
      "WorkingDir": "/data",
      "Entrypoint": [
        "docker-entrypoint.sh"
      ],
      "OnBuild": null,
      "Labels": null
    },
    "Architecture": "amd64",
    "Os": "linux",
    "Size": 129934853,
    "VirtualSize": 129934853,
    "GraphDriver": {
      "Data": {
        "LowerDir": "/var/lib/docker/overlay2/559931ac36db38c9eec91ce53727a6fa0a8e497f18d1d11735e1f7ff10d2da41/diff:/var/lib/docker/overlay2/f940b91e7d5c24977da3b9acaf5a427ffa296979ed9bd64d832e311469546c08/diff:/var/lib/docker/overlay2/27a0709d2e333c40f79182444d70e8c347056b481c394c398d968a214463be05/diff:/var/lib/docker/overlay2/74a14c4603e813d32832f6379476875032ac464cd6226616454a4cc7badbe0dd/diff:/var/lib/docker/overlay2/5af9d9e4255f7dbf4f9196595bf32d6d71c2a40c2e6c49190cf19fd59a318034/diff",
        "MergedDir": "/var/lib/docker/overlay2/c855c18d47f7145d50611ffaebb8da469aeb85019b4b407b6240785216d47913/merged",
        "UpperDir": "/var/lib/docker/overlay2/c855c18d47f7145d50611ffaebb8da469aeb85019b4b407b6240785216d47913/diff",
        "WorkDir": "/var/lib/docker/overlay2/c855c18d47f7145d50611ffaebb8da469aeb85019b4b407b6240785216d47913/work"
      },
      "Name": "overlay2"
    },
    "RootFS": {
      "Type": "layers",
      "Layers": [
        "sha256:c6e34807c2d51444c41c15f4fda65847faa2f43c9b4b976a2f6f476eca7429ce",
        "sha256:7f284306d56a23e9497dc243919ba75953d6d9d8a6a8a7aa3460b188cc2e93b6",
        "sha256:3a669a586605c9f75c5de4052547e00ec04aae6688d39666b417b41f37abeb0d",
        "sha256:de7c13f0f6750f1fc3e0218839796262ae5a9798613a69cebd94004364d8ceb4",
        "sha256:7daa3b979b8f0ae421fb31cb3b63932cf63efc6d1d8086450a7f0f1e4b4981e5",
        "sha256:b0a6e763f9e55b207e5a3bb131252c66f89e9e55bf983bfeee406b18bd925c5a"
      ]
    },
    "Metadata": {
      "LastTagTime": "0001-01-01T00:00:00Z"
    }
  }
]
[root@node1 ~]#
```

可以看到，redis镜像的元数据信息非常多。我们可以看到，上面信息中，在28行处的`Env`环境变量配置中，有指定redis的版本信息。我们借助`jq`命令，可以快捷过滤我们想要的关键信息：

```sh
[root@node1 ~]# docker inspect $(docker images -q redis)|jq '.[0].ContainerConfig.Env'
[
  "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  "GOSU_VERSION=1.16",
  "REDIS_VERSION=7.0.12",
  "REDIS_DOWNLOAD_URL=http://download.redis.io/releases/redis-7.0.12.tar.gz",
  "REDIS_DOWNLOAD_SHA=9dd83d5b278bb2bf0e39bfeb75c3e8170024edbaf11ba13b7037b2945cf48ab7"
]
[root@node1 ~]#
```

![](/img/Snipaste_2023-08-15_21-46-06.png)
jq命令的使用，可以参考我的总结文档[JSON解析工具-jq](../../OS/Centos/json_tool_jq.md)

可以看到，Redis的版本信息是`REDIS_VERSION=7.0.12`。

相应的，使用同样的方法查看nginx镜像中nginx的版本信息：

```sh
[root@node1 ~]# docker inspect $(docker images -q nginx)|jq '.[0].ContainerConfig.Env'
[
  "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  "NGINX_VERSION=1.25.1",
  "NJS_VERSION=0.7.12",
  "PKG_RELEASE=1~bookworm"
]
[root@node1 ~]#
```

但并不是所有的镜像都会在`Env`环境变量中配置版本信息，如`hello-world`镜像：

```sh
[root@node1 ~]# docker images hello-world
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    9c7a54a9a43c   3 months ago   13.3kB
[root@node1 ~]# docker inspect $(docker images -q hello-world)|jq '.[0].ContainerConfig.Env'
[
  "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
]
[root@node1 ~]#
```

此时，可以看到，`hello-world`镜像没有在环境变量中指定版本信息。


## 3.为镜像打标签

如给redis镜像打标签，加上版本信息：

查看镜像信息：
```sh
[root@node1 ~]# docker images redis
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
redis        latest    e0ce02f88e58   2 weeks ago   130MB
[root@node1 ~]#
```

查看`docker tag`帮助信息：

```sh
[root@node1 ~]# docker tag --help

Usage:  docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]

Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
[root@node1 ~]#
```

上一节点我们已经知道redis版本信息是`REDIS_VERSION=7.0.12`，给`redis:latest`镜像打上新标签：

```sh
[root@node1 ~]# docker tag redis:latest redis:7.0.12
```

此时，查看redis镜像信息：

```sh
[root@node1 ~]# docker images redis
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
redis        7.0.12    e0ce02f88e58   2 weeks ago   130MB
redis        latest    e0ce02f88e58   2 weeks ago   130MB
[root@node1 ~]#
```

可以看到，redis镜像存在`latest`和`7.0.12`两个标签，我们现在将`latest`标签删除掉。

查看`docker image`帮助信息：

```sh
[root@node1 ~]# docker image --help

Usage:  docker image COMMAND

Manage images

Commands:
  build       Build an image from a Dockerfile
  history     Show the history of an image
  import      Import the contents from a tarball to create a filesystem image
  inspect     Display detailed information on one or more images
  load        Load an image from a tar archive or STDIN
  ls          List images
  prune       Remove unused images
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rm          Remove one or more images
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE

Run 'docker image COMMAND --help' for more information on a command.
[root@node1 ~]#
```

可以看到，可以使用`rm`子命令来删除镜像。

```sh
[root@node1 ~]# docker image rm redis:latest
Untagged: redis:latest

[root@node1 ~]# docker images redis
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
redis        7.0.12    e0ce02f88e58   2 weeks ago   130MB
[root@node1 ~]#
```

可以看到，标签名`latest`的redis镜像已经删除了，只留下标签为`7.0.12`的redis镜像，这样，以后查看redis镜像时，一眼就能看出该镜像对应的redis版本信息，不用通过元数据去查看镜像版本信息。

因此，建议后期下载docker镜像时，直接带上标签来下载docker镜像。