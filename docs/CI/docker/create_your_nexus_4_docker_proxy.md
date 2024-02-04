# 搭建自己的nexus私有仓库4--搭建docker私有仓库

[[toc]]

本文档是nexus系列课程第4篇。
- nexus系列课程第1篇，请参考 [搭建自己的nexus私有仓库1--nexus初体验](./create_your_nexus.md)
- nexus系列课程第2篇，请参考 [搭建自己的nexus私有仓库2--创建python pypi代理](./create_your_nexus_2.md)
- nexus系列课程第3篇，请参考 [搭建自己的nexus私有仓库3--创建yum ius代理](./create_your_nexus_3.md)

本文计划做以下事情：

- 使用nexus创建docker代理仓库(proxy)、本地仓库(hosted)和组仓库(group)。
- 使用HTTP形式，从代理仓库下载镜像，构建镜像并上传到私有仓库。
- 使用HTTPS形式，配置nginx反向代理，从代理仓库下载镜像，构建镜像并上传到私有仓库。


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

我们在[搭建自己的nexus私有仓库1--nexus初体验](./create_your_nexus.md)中是使用的以下命令启动nexus容器：

```sh
[root@nexus ~]# docker run -d --restart always -p 8081:8081 --name nexus sonatype/nexus3:3.59.0
80bbd285db0bc84a50b785a2aeb688d8bf6879e5fa1381357fa1426a9f38148a
[root@nexus ~]#
```

可以看到，docker容器启动没有没有设置持久化映射。当前只暴露了一个8081端口：
```sh
[root@nexus ~]# docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED        STATUS        PORTS                    NAMES
80bbd285db0b   sonatype/nexus3:3.59.0   "/opt/sonatype/nexus…"   5 months ago   Up 5 months   0.0.0.0:8081->8081/tcp   nexus
[root@nexus ~]# netstat -tunlp|grep docker
tcp        0      0 0.0.0.0:8081            0.0.0.0:*               LISTEN      5231/docker-proxy
[root@nexus ~]#
```

可以看到，只暴露了8081端口。

同时，我们在nexus上面配置了Yum、Pypi代理，并且能够正常工作。

本篇文章相对复杂，参考了一些大佬的博客，记录如下：

- B站大佬录制视频 [使用 Nexus 制作 Docker 私库 学习 2022-11-24](https://www.bilibili.com/video/BV1nM411r7yL/?spm_id_from=333.880.my_history.page.click&vd_source=54304ea09e70b7840a863dd0e187751c)
- 以上视频对应文档，[在 Docker 中安装 Nexus](https://xuxiaowei-com-cn.gitee.io/gitlab-k8s/docs/nexus/docker-install-nexus)
- [Docker 私库 自定义配置](https://xuxiaowei-com-cn.gitee.io/gitlab-k8s/docs/nexus/docker-repository)
- [Docker 安装 Nexus3，并配置 Nginx 反向代理](https://www.jianshu.com/p/b87ace01aee4)
- [使用nexus3配置docker私有仓库](https://wiki.eryajf.net/pages/1816.html#_1-%E5%AE%89%E8%A3%85-nexus3%E3%80%82)
- [Nexus3最佳实践系列：搭建Docker私有仓库](https://zhangge.net/5139.html)
- 官方文档 [SSL Certificate Guide](https://support.sonatype.com/hc/en-us/articles/213465768-SSL-Certificate-Guide)
- [Configuring SSL](https://help.sonatype.com/en/configuring-ssl.html)


通过官方文档 [SSL Certificate Guide](https://support.sonatype.com/hc/en-us/articles/213465768-SSL-Certificate-Guide)和观看视频发现，在nexus 容器中配置HTTPS协议添加证书非常麻烦，我们不使用该方式，而是直接使用Nginx作反向代理到后端Nexus容器暴露的HTTP协议的端口。

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


## 3. nexus创建docker proxy代理仓库

### 3.1 docker代理未暴露端口说明

在系列文章第一篇中，我们知道通过点击页面顶部的齿轮设置图标：

![](/img/Snipaste_2023-08-22_22-33-54.png)
进入到设置页面后，点击左侧的【Repositories】进入到仓库管理页面，点击【Create Repository】按钮，我们需要使用的docker仓库，以看到`docker(proxy)`：

![](/img/Snipaste_2024-01-20_23-04-27.png)
我们直接点击`docker(proxy)`进入到docker代理仓库配置界面，依次填写相关信息。

docker代理仓库说明： 
- name: docker-proxy
- format: docker
- type: proxy
- HTTP端口：8001
- HTTPS端口：不勾选，忽略
- Allow anonymous docker pull ( Docker Bearer Token Realm required )： 允许匿名下载镜像，勾选该处。
- Enable Docker V1 API: 允许docker客户端使用V1 API，勾选该处。
- Remote storage: 远程存储仓库的URL地址，如我们直接代理腾讯云软件源站，~~其公网地址是 [https://mirrors.cloud.tencent.com](https://mirrors.cloud.tencent.com)，内网地址是[https://mirror.ccs.tencentyun.com](https://mirror.ccs.tencentyun.com)，你也可以使用其他国内加速源。为了让演示更具一般性，我使用公网地址 [https://mirrors.cloud.tencent.com](https://mirrors.cloud.tencent.com)进行代理~~。参考[腾讯云软件源加速软件包下载和更新](https://cloud.tencent.com/document/product/213/8623)。
::: warning 说明
后面通过测试发现，在腾讯云主机上面部署的nuxus容器，使用公网地址https://mirrors.cloud.tencent.com 对docker镜像加速不起作用，使用内网地址https://mirror.ccs.tencentyun.com 能正常加速。

也可以使用其他加速源：
- 科大镜像：https://docker.mirrors.ustc.edu.cn
- 网易：https://hub-mirror.c.163.com
- 阿里云：https://<你的ID>.mirror.aliyuncs.com
:::

- Docker Index: 这里为了确保能够拉取 DockerHub 最新的镜像，我选择了 Use DockerHub 这个 Index。
- HTTP request setting，HTTP请求设置，我们一般只需要设置一下User-Agent请求头即可，如填写"Sync docker image. email: mzh.whut@gmail.com"。

![](/img/Snipaste_2024-01-20_23-21-03.png)
**注意，代理URL请使用科大镜像、网易、阿里云等加速源，或者腾讯内网地址https://mirror.ccs.tencentyun.com ，不要使用截图中的腾讯外网地址 https://mirrors.cloud.tencent.com 。**

**注意，代理URL请使用科大镜像、网易、阿里云等加速源，或者腾讯内网地址https://mirror.ccs.tencentyun.com ，不要使用截图中的腾讯外网地址 https://mirrors.cloud.tencent.com 。**

**注意，代理URL请使用科大镜像、网易、阿里云等加速源，或者腾讯内网地址https://mirror.ccs.tencentyun.com ，不要使用截图中的腾讯外网地址 https://mirrors.cloud.tencent.com 。**

我自己通过测试发现在腾讯云主机上面使用腾讯内网地址https://mirror.ccs.tencentyun.com 加速更稳定。

由于我们是测试阶段，docker使用的blob还是使用默认`default` Blob存储即可，最后点击【Create repository】创建仓库即可。



创建后，点击新创建的`docker-proxy`仓库，可以看到仓库详情：
![](/img/Snipaste_2024-01-20_23-25-34.png)
这里的URL [http://nexushub.com:8081/repository/docker-proxy/](http://nexushub.com:8081/repository/docker-proxy/) 并不是我们docker代理仓库使用的地址，如果直接在浏览器中访问，可以看到以下说明：

![](/img/Snipaste_2024-01-20_23-27-03.png)
即`This docker proxy repository is not directly browseable at this URL`，docker代理仓库不能直接在浏览器中浏览。

我们再次看端口开放情况：

```sh
[root@nexus ~]# netstat -tunlp|grep docker
tcp        0      0 0.0.0.0:8081            0.0.0.0:*               LISTEN      5231/docker-proxy
[root@nexus ~]#
```

可以看到，主机上面并没有暴露8001端口。进入容器中查看一下：

```sh
[root@nexus ~]# docker exec -it nexus /bin/bash
bash-4.4$ curl 127.0.0.1:8001
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1"/>
<title>Error 400 Not a Docker request</title>
</head>
<body><h2>HTTP ERROR 400 Not a Docker request</h2>
<table>
<tr><th>URI:</th><td>/</td></tr>
<tr><th>STATUS:</th><td>400</td></tr>
<tr><th>MESSAGE:</th><td>Not a Docker request</td></tr>
<tr><th>SERVLET:</th><td>-</td></tr>
</table>
<hr/><a href="https://eclipse.org/jetty">Powered by Jetty:// 9.4.51.v20230217</a><hr/>

</body>
</html>
bash-4.4$ exit
exit
[root@nexus ~]#
```

可以看到，容器中已经正常监听了8001端口，但主机上面还没有监听到。所以，在我们创建容器时，就应该提前规划好docker容器需要监听的端口，好提前做好端口映射到主机上。因此，我们需要重新创建neuxs容器，将需要暴露的docker端口可加起来。


### 3.2 docker代理正常暴露端口

#### 3.2.1 重新运行docker容器

上面我们在主机上没有正常暴露，无法使用docker代理，因此需要重新运行一下nexus容器，将之前的容器删除掉。

为了使后面的配置能够保存下来，将数据文件保存到挂载卷中。


将之前的nexus容器删除掉：

```sh
[root@nexus ~]# docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED        STATUS        PORTS                    NAMES
80bbd285db0b   sonatype/nexus3:3.59.0   "/opt/sonatype/nexus…"   5 months ago   Up 5 months   0.0.0.0:8081->8081/tcp   nexus
[root@nexus ~]# docker stop nexus
nexus
[root@nexus ~]# docker rm nexus
nexus
[root@nexus ~]# docker ps -a|grep nexus
[root@nexus ~]#
```

可以看到，nexus容器已经删除成功了。

创建挂载卷目录，用于文件共享，同时修改挂载目录的权限：

```sh
[root@nexus ~]# mkdir -p /some/dir/nexus-data
[root@nexus ~]# chmod 777 /some/dir/nexus-data
[root@nexus ~]# ll /some/dir/
total 4
drwxrwxrwx 2 root root 4096 Jan 21 19:26 nexus-data
[root@nexus ~]#
```

用以下命令运行新的容器：
```sh
docker run -d --restart always -p 8081:8081 -p 8001-8003:8001-8003  -v /some/dir/nexus-data:/nexus-data --name nexus sonatype/nexus3:3.59.0
```

运行容器，并查看端口暴露情况：

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

查看密码：

```sh
[root@nexus ~]# cat /some/dir/nexus-data/admin.password
b0466c4f-aeb5-49a4-b61a-f2904890c5fa[root@nexus ~]#
[root@nexus ~]#
```

注意密码是`b0466c4f-aeb5-49a4-b61a-f2904890c5fa`。

使用初始密码登陆后，需要修改密码。

登陆后，可以看到，之前我手动创建的仓库都没有了。

![](/img/Snipaste_2024-01-21_19-42-50.png)
此处我们不演示yum、pypi代理，其配置参考系列文章前几篇即可，此处我着重关注docker代理的配置。

按3.1节方式重新创建`docker-proxy`代理仓库。此节我们再创建`docker-hosted`本地仓库和`docker-group`聚合仓库。

#### 3.2.2 创建docker blob 对象

为了使docker的blob和其他的不同，我们创建一个docker的blob，用来存储docker相关的文件。

依次点击【Repository】--【Blob Stores】--【Create Blob Store】:
![](/img/Snipaste_2024-01-21_19-53-57.png)
Blob类型选择`File`：

![](/img/Snipaste_2024-01-21_19-56-08.png)

然后，名称设置为`docker`，不勾选【Soft Quota】，最后点击【Save】保存:
![](/img/Snipaste_2024-01-21_20-04-37.png)
可以看到，新的Blob创建成功：
![](/img/Snipaste_2024-01-21_20-06-44.png)

然后，创建`docker-proxy`代理仓库，注意blob选择【docker】即可，其他和上一节的配置一样。

#### 3.2.3 创建docker-hosted本地仓库

创建`docker-hosted`本地仓库：

docker本地仓库说明： 
- name: docker-hosted
- format: docker
- type: hosted
- HTTP端口：8002
- HTTPS端口：不勾选，忽略
- Allow anonymous docker pull ( Docker Bearer Token Realm required )： 允许匿名下载镜像，勾选该处。
- Enable Docker V1 API: 允许docker客户端使用V1 API，勾选该处
- Blob store: 选择【docker】blob对象
- Deployment policy: 测试时，先可以选择【Allow redeploy】允许重复发布，后期如果用在正式生产环境时，可以将该修改为【Disable redeploy】。

![](/img/Snipaste_2024-01-21_20-14-28.png)
相关信息填写好后，最后点击【Create repository】创建仓库即可。

#### 3.2.4 创建docker-group聚合仓库

创建`docker-group`聚合仓库：

docker聚合仓库说明： 
- name: docker-group
- format: docker
- type: group
- HTTP端口：8003
- HTTPS端口：不勾选，忽略
- Allow anonymous docker pull ( Docker Bearer Token Realm required )： 允许匿名下载镜像，勾选该处。
- Enable Docker V1 API: 允许docker客户端使用V1 API，勾选该处
- Blob store: 选择【docker】blob对象
- Group: Member Repositories，将【docker-hosted】和 【docker-proxy】添加到右侧，这里成员仓库的顺序可以稍微规划下，一般来说将本地的放前面，代理第三方的放后面，好处就是优先使用本地或小众的镜像仓库。

![](/img/Snipaste_2024-01-21_20-30-45.png)

![](/img/Snipaste_2024-01-21_20-31-43.png)
相关信息填写好后，最后点击【Create repository】创建仓库即可。

这样我们三个docker仓库已经创建好了：

![](/img/Snipaste_2024-01-21_20-41-29.png)

#### 3.2.5 开启匿名访问权限


依次点击【Security】--【Realms】,将【Docker Bearer Token Tealm】添加到右侧：
![](/img/Snipaste_2024-01-21_21-25-38.png)

最后点击【Save】保存即可。


### 3.3 测试代理仓库下载镜像

我们在master主节点测试是否能够正常拉取镜像。

先修改`/etc/docker/daemon.json`配置：

```sh
[root@master ~]# cd /etc/docker/

# 备份
[root@master docker]# mv daemon.json daemon.json.20240121.bak

# 修改配置文件
[root@master docker]# vi daemon.json

# 查看配置文件内容
[root@master docker]# cat daemon.json
{
    "insecure-registries":[
        "nexushub.com:8001",
        "nexushub.com:8002",
        "nexushub.com:8003"
    ],
    "registry-mirrors":[
        "http://nexushub.com:8001",
        "http://nexushub.com:8002",
        "http://nexushub.com:8003"
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

最开始使用[https://mirrors.cloud.tencent.com](https://mirrors.cloud.tencent.com)作为docker远程加速地址时，nexus容器日志会一直报异常：

```sh
[root@nexus ~]# docker logs nexus |grep --color=always mirrors.cloud.tencent.com|tail -n 5
2024-01-23 13:43:15,443+0000 WARN  [qtp1700352105-2733] anonymous org.sonatype.nexus.repository.docker.internal.V2Handlers - Is the remote url a valid docker endpoint? Remote host https://mirrors.cloud.tencent.com/ with path /v2/library/alpine/manifests/latest did not return the expected response. Error message: manifest unknown
2024-01-23 13:48:22,142+0000 WARN  [qtp1700352105-2422] anonymous org.sonatype.nexus.repository.docker.internal.V2Handlers - Is the remote url a valid docker endpoint? Remote host https://mirrors.cloud.tencent.com/ with path /v2/library/alpine/manifests/3.18 did not return the expected response. Error message: manifest unknown
2024-01-23 13:48:22,236+0000 WARN  [qtp1700352105-2407] anonymous org.sonatype.nexus.repository.docker.internal.V2Handlers - Is the remote url a valid docker endpoint? Remote host https://mirrors.cloud.tencent.com/ with path /v2/library/alpine/manifests/3.18 did not return the expected response. Error message: manifest unknown
2024-01-23 14:07:51,586+0000 WARN  [qtp1700352105-2422] anonymous org.sonatype.nexus.repository.docker.internal.V2Handlers - Is the remote url a valid docker endpoint? Remote host https://mirrors.cloud.tencent.com/ with path /v2/library/alpine/manifests/3.18 did not return the expected response. Error message: manifest unknown
2024-01-23 14:07:51,682+0000 WARN  [qtp1700352105-2407] anonymous org.sonatype.nexus.repository.docker.internal.V2Handlers - Is the remote url a valid docker endpoint? Remote host https://mirrors.cloud.tencent.com/ with path /v2/library/alpine/manifests/3.18 did not return the expected response. Error message: manifest unknown
[root@nexus ~]#
```

![](/img/Snipaste_2024-01-24_06-24-00.png)
因此，将加速地址改成腾讯云内网访问域名：https://mirrors.tencentyun.com，然后再尝试下载镜像就发现下载完成镜像后，nexus上面就会有对应blob信息，Browse中也可以看到对应的镜像信息。

然后下载镜像：
```sh
# 下载alpine镜像最新版本
[root@master ~]# docker pull alpine
Using default tag: latest
latest: Pulling from library/alpine
661ff4d9561e: Pull complete
Digest: sha256:51b67269f354137895d43f3b3d810bfacd3945438e94dc5ac55fdac340352f48
Status: Downloaded newer image for alpine:latest
docker.io/library/alpine:latest
[root@master ~]#

# 下载alpine镜像指定版本
[root@master ~]# docker pull alpine:3.18
3.18: Pulling from library/alpine
c926b61bad3b: Pull complete
Digest: sha256:34871e7290500828b39e22294660bee86d966bc0017544e848dd9a255cdf59e0
Status: Downloaded newer image for alpine:3.18
docker.io/library/alpine:3.18
[root@master ~]#
```

正常代理时，nexus容器日志如下：

```sh
[root@nexus ~]$ docker logs -f nexus
.... 省略
2024-01-23 22:10:37,861+0000 INFO  [qtp1700352105-3163] anonymous org.sonatype.nexus.repository.httpclient.internal.HttpClientFacetImpl - Repository status for docker-proxy changed from READY to AVAILABLE - reason n/a for n/a
2024-01-23 22:10:38,280+0000 INFO  [elasticsearch[953A371A-D6B62003-687DD2CD-53B697DD-2FE6DB90][clusterService#updateTask][T#1]] *SYSTEM org.elasticsearch.cluster.metadata - [953A371A-D6B62003-687DD2CD-53B697DD-2FE6DB90] [2e558aa1029f36cea9ed93e744bf70bea008fe46] update_mapping [component]
```

在nexus上面检查：

Blob中显示已经有10个blob对象了：
![](/img/Snipaste_2024-01-24_06-28-20.png)

在nexus Browse中也可以看到对应的镜像信息:
![](/img/Snipaste_2024-01-24_06-27-30.png)

如果能够正常代理，则下载镜像时，上面两个位置的信息会发生变化，blob对象会增加，Browse浏览器中也可以看到新下载的镜像信息。

我们在`/etc/docker/daemon.json`配置了代理的三个端口，现在不确定下载镜像时，到底走的哪个镜像加速地址，后续再分别测试。为避免本篇文本太长，将其他测试和nginx代理配置放到下一篇文章中。
