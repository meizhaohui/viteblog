# 搭建自己的nexus私有仓库7--修改nexus容器时区

[[toc]]

本文档是nexus系列课程第7篇。

- nexus系列课程第1篇，请参考 [搭建自己的nexus私有仓库1--nexus初体验](./create_your_nexus.md)
- nexus系列课程第2篇，请参考 [搭建自己的nexus私有仓库2--创建python pypi代理](./create_your_nexus_2.md)
- nexus系列课程第3篇，请参考 [搭建自己的nexus私有仓库3--创建yum ius代理](./create_your_nexus_3.md)
- nexus系列课程第4篇，请参考 [搭建自己的nexus私有仓库4--创建docker私有仓库](./create_your_nexus_4_docker_proxy.md)
- nexus系列课程第5篇，请参考 [搭建自己的nexus私有仓库5--测试docker仓库pull和push](./create_your_nexus_5_test_docker_proxy.md)
- nexus系列课程第6篇，请参考 [搭建自己的nexus私有仓库6--使用nginx反向代理](./create_your_nexus_6_nginx_proxy.md)

第4篇中，已经使用nexus创建docker代理仓库(proxy)、本地仓库(hosted)和聚合仓库(group)，并尝试通过HTTP方式从代理仓库下载镜像，并且可以正常下载镜像。在第5篇中，测试了使用以上三种仓库作为docker加速源时的`pull`拉取和`push`推送镜像情况。

本文计划做以下事情：

- 修改运行的容器的时区信息，使其使用北京时间。




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



在第5篇中已经测试了三类仓库支持的docker pull和push操作情况：


| 仓库类型       | 仓库名称      | HTTP端口号 | HTTPS端口号 | 支持docker操作 |
| -------------- | :------------ | ---------- | ----------- | :------------- |
| proxy代理仓库  | docker-proxy  | 8001       | 不设置      | pull           |
| hosted本地仓库 | docker-hosted | 8002       | 不设置      | pull、push     |
| group聚合仓库  | docker-group  | 8003       | 不设置      | pull           |





在第6篇中，我们使用Nginx代理Nexus，并配置SSL证书，通过[https://nexus.hellogitlab.com/](https://nexus.hellogitlab.com/)能够正常访问到Nexus web管理控制台，通过配置docker加速源 [https://docker-registry.hellogitlab.com/](https://docker-registry.hellogitlab.com/) 能够正常拉取docker官方镜像和docker-hosted本地仓库中的镜像，并且能够正常push推送镜像到Nexus的docker-hosted本地仓库中：

| 域名                            | 端口    | 代理地址                             |
| ------------------------------- | ------- | ------------------------------------ |
| nexus.hellogitlab.com           | 80、443 | nexushub.com:8080                    |
| docker-registry.hellogitlab.com | 80、443 | nexushub.com:8002、nexushub.com:8003 |



## 2. 现象说明

### 2.1 Nexus web页面显示

我们在上一篇中，最后推送镜像到Nexus docket-hosted本地仓库时，可以在页面上面看到以下信息：

![](/img/Snipaste_2024-01-28_22-56-48.png)

即属性下面的`last_modified`显示的是UTC时间:

- **last_modified** 2024-01-28T08:48:05.565Z

而上面的`Blob created`却是用的中国标签时间：

-  **Blob created**	Sun Jan 28 2024 16:48:05 GMT+0800 (中国标准时间)



### 2.2 容器内时间显示

首先，进入到nexus容器命令行：

```sh
# 查看主机时间
[root@nexus ~]# date
Sun Jan 28 23:03:54 CST 2024

# 进入到nexus容器命令行
[root@nexus ~]# docker exec -it nexus /bin/bash
bash-4.4$
```



查看容器内部当前时间：

```sh
bash-4.4$ date
Sun Jan 28 15:03:56 UTC 2024
```

可以看到，容器内部使用的是UTC时间。



为了让我们看得更舒服，我们将容器内部的时区调整为中国标准时间。



## 3. 时区调整

时区调整，主要是增加`TZ="Asia/Shanghai"`环境变量。

### 3.1 设置TZ环境变量

::: warning 警告

使用此种方式不起作用。

请使用下一节复制时区文件方式来修改容器内时区。

:::



参考：

- 可以参考我另外一篇文章 [docker容器增加端口映射](./add_port_to_container/md) ，修改容器配置文件。
- 参考 [How to set an environment variable in a running docker container](https://stackoverflow.com/questions/27812548/how-to-set-an-environment-variable-in-a-running-docker-container)

> **Get the Container ID**
>
> Save the ID of the container you want to edit for easier access to the files.
>
> ```sh
> export CONTAINER_ID=`docker inspect --format="{{.Id}}" <YOUR CONTAINER NAME>`
> ```
>
> **Edit Container Configuration**
>
> Edit the configuration file, go to the "Env" section, and add your key.
>
> ```sh
> sudo vim /var/lib/docker/containers/$CONTAINER_ID/config.v2.json
> ```
>
> My file looks like this:
>
> ```sh
> ...,"Env":["TEST=1",...
> ```
>
> **Stop and Start Docker**
>
> I found that restarting Docker didn't work, I had to stop and then start Docker with two separate commands.
>
> ```sh
> sudo systemctl stop docker
> sudo systemctl start docker
> ```



先停止neuxs容器：

```sh
[root@nexus ~]# docker stop nexus
nexus
[root@nexus ~]# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
[root@nexus ~]#
```

获取neuxs容器ID，并查看配置文件：

```sh
# 获取neuxs容器ID
[root@nexus ~]# export CONTAINER_ID=`docker inspect --format="{{.Id}}" nexus`

# 查看配置文件
[root@nexus ~]# ls /var/lib/docker/containers/$CONTAINER_ID/config.v2.json
/var/lib/docker/containers/8b931229efd4a2749a16342b149901a74674ec5b771591a808baebc744ebcdc4/config.v2.json
[root@nexus ~]#
```

备份配置文件：

```sh
# 备份配置文件
[root@nexus ~]# cp -p /var/lib/docker/containers/$CONTAINER_ID/config.v2.json{,.bak}

# 查看备份原文件和备份文件
[root@nexus ~]# ll /var/lib/docker/containers/$CONTAINER_ID/config.v2.json*
-rw------- 1 root root 4429 Jan 28 23:20 /var/lib/docker/containers/8b931229efd4a2749a16342b149901a74674ec5b771591a808baebc744ebcdc4/config.v2.json
-rw------- 1 root root 4429 Jan 28 23:20 /var/lib/docker/containers/8b931229efd4a2749a16342b149901a74674ec5b771591a808baebc744ebcdc4/config.v2.json.bak
[root@nexus ~]#
```



停止docker服务：

```sh
[root@nexus ~]# systemctl stop docker docker.socket
```



配置文件`config.v2.json`是压缩的json格式，不便于阅读和修改。我们使用`jq`命令存一份美化后的文件，关于`jq`命令的使用，可参考[JSON解析工具-jq](../../OS/Centos/json_tool_jq.md) 。

```sh
# 生成美化后的json配置文件
[root@nexus ~]# cat /var/lib/docker/containers/$CONTAINER_ID/config.v2.json|jq > /var/lib/docker/containers/$CONTAINER_ID/config.v2.jq.json

# 使用vi编辑配置，可以看到40-50行就是关于环境变量的配置
[root@nexus ~]# vi /var/lib/docker/containers/$CONTAINER_ID/config.v2.jq.json
[root@nexus ~]#
```



40-50行内容如下：

```sh
将Env相关的配置显示出来
[root@nexus ~]# head -n 50 /var/lib/docker/containers/$CONTAINER_ID/config.v2.jq.json|tail -n 11
    "Env": [
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "container=oci",
      "SONATYPE_DIR=/opt/sonatype",
      "NEXUS_HOME=/opt/sonatype/nexus",
      "NEXUS_DATA=/nexus-data",
      "NEXUS_CONTEXT=",
      "SONATYPE_WORK=/opt/sonatype/sonatype-work",
      "DOCKER_TYPE=rh-docker",
      "INSTALL4J_ADD_VM_PARAMS=-Xms2703m -Xmx2703m -XX:MaxDirectMemorySize=2703m -Djava.util.prefs.userRoot=/nexus-data/javaprefs"
    ],
[root@nexus ~]#
```

我们在PATH环境变量的下一行增加内容，修改后再查看内容：

```sh
[root@nexus ~]# head -n 51 /var/lib/docker/containers/$CONTAINER_ID/config.v2.jq.json|tail -n 12
    "Env": [
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "TZ=Asia/Shanghai",
      "container=oci",
      "SONATYPE_DIR=/opt/sonatype",
      "NEXUS_HOME=/opt/sonatype/nexus",
      "NEXUS_DATA=/nexus-data",
      "NEXUS_CONTEXT=",
      "SONATYPE_WORK=/opt/sonatype/sonatype-work",
      "DOCKER_TYPE=rh-docker",
      "INSTALL4J_ADD_VM_PARAMS=-Xms2703m -Xmx2703m -XX:MaxDirectMemorySize=2703m -Djava.util.prefs.userRoot=/nexus-data/javaprefs"
    ],
[root@nexus ~]#
```

再将修改后的`config.v2.jq.json`文件压缩后保存到`config.v2.json`文件中：

```sh
[root@nexus ~]# cat /var/lib/docker/containers/$CONTAINER_ID/config.v2.jq.json|jq -c >  /var/lib/docker/containers/$CONTAINER_ID/config.v2.json

# 查看配置文件的时区环境变量信息
[root@nexus ~]# grep -o 'TZ=Asia/Shanghai'  /var/lib/docker/containers/$CONTAINER_ID/config.v2.json
TZ=Asia/Shanghai
```



修改完成后，再启动docker服务:

```sh
[root@nexus ~]# systemctl start docker docker.socket
```

此时nexus容器会自动重启：

```sh
# 查看正在运行的容器
[root@nexus ~]# docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED      STATUS         PORTS                                                      NAMES
8b931229efd4   sonatype/nexus3:3.59.0   "/opt/sonatype/nexus…"   7 days ago   Up 3 minutes   0.0.0.0:8001-8003->8001-8003/tcp, 0.0.0.0:8081->8081/tcp   nexus
[root@nexus ~]#
```

进入nexus容器命令行，并查看时间：

```sh
# 进入nexus命令行
[root@nexus ~]# docker exec -it nexus /bin/bash

# 时间还是相差8小时
bash-4.4$ date
Sun Jan 28 15:43:44 Asia 2024

# 时区环境变量已经生效了
bash-4.4$ echo $TZ
Asia/Shanghai
```

此时可以看TZ环境变量已经正常读取到了，但时间还是不对。



发现时区仍然不对，我们将Nexus容器的配置文件还原：

```sh
# 停止掉docker相关服务
[root@nexus ~]# systemctl stop docker docker.socket

# 切换到容器配置文件目录
[root@nexus ~]# cd /var/lib/docker/containers/8b931229efd4a2749a16342b149901a74674ec5b771591a808baebc744ebcdc4/

# 查看相关配置文件
# config.v2.json.bak是我们原始的备份文件
[root@nexus 8b931229efd4a2749a16342b149901a74674ec5b771591a808baebc744ebcdc4]# ls
8b931229efd4a2749a16342b149901a74674ec5b771591a808baebc744ebcdc4-json.log  checkpoints  config.v2.jq.json  config.v2.json  config.v2.json.bak  hostconfig.json  hostname  hosts  mounts  resolv.conf  resolv.conf.hash

# 还原配置文件，提示是否覆盖，输入y覆盖即可
[root@nexus 8b931229efd4a2749a16342b149901a74674ec5b771591a808baebc744ebcdc4]# cp -p config.v2.json.bak config.v2.json
cp: overwrite ‘config.v2.json’? y

# 启动docker服务
[root@nexus 8b931229efd4a2749a16342b149901a74674ec5b771591a808baebc744ebcdc4]# cd
[root@nexus ~]# systemctl start docker docker.socket

# 查看docker容器运行情况
[root@nexus ~]# docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED      STATUS         PORTS                                                      NAMES
8b931229efd4   sonatype/nexus3:3.59.0   "/opt/sonatype/nexus…"   8 days ago   Up 4 seconds   0.0.0.0:8001-8003->8001-8003/tcp, 0.0.0.0:8081->8081/tcp   nexus
[root@nexus ~]# 
```



### 3.2 复制Asia/Shanghai时区文件到容器中

Nexus主机上面时区是正常的，我们直接复制该文件到容器里面去：

```sh
# 查看主机时间
[root@nexus ~]# date
Mon Jan 29 20:51:34 CST 2024
[root@nexus ~]#

# 查看/etc/localtime 时区文件指向
[root@nexus ~]# ls -lah /etc/localtime
lrwxrwxrwx 1 root root 35 Mar 19  2023 /etc/localtime -> ../usr/share/zoneinfo/Asia/Shanghai
[root@nexus ~]# 
```



复制文件到容器neuxs中：

```sh
[root@nexus ~]# docker cp ../usr/share/zoneinfo/Asia/Shanghai nexus:/root/
```



以root用户进入容器：

```sh
[root@nexus ~]# docker exec --privileged -u root -it nexus /bin/bash
[root@8b931229efd4 sonatype]# cp -p /etc/localtime{,.bak}
```

将上传的`Shanghai`文件移动到`/usr/share/zoneinfo/Asia`目录：

```sh
# 创建存放时区文件的目录
[root@8b931229efd4 sonatype]# mkdir -p /usr/share/zoneinfo/Asia

# 将上传的文件移动到该目录
[root@8b931229efd4 sonatype]# mv ~/Shanghai /usr/share/zoneinfo/Asia/
```

将原来的`/etc/localtime`文件删除掉：

```sh
[root@8b931229efd4 sonatype]# rm /etc/localtime
rm: remove symbolic link '/etc/localtime'? y
[root@8b931229efd4 sonatype]#
```



创建`/etc/localtime`软链接：

```sh
[root@8b931229efd4 sonatype]# cd /etc/
[root@8b931229efd4 etc]# ln -s ../usr/share/zoneinfo/Asia/Shanghai localtime
[root@8b931229efd4 etc]# ls -lah localtime
lrwxrwxrwx 1 root root 35 Jan 29 20:59 localtime -> ../usr/share/zoneinfo/Asia/Shanghai
```

查看容器时间：

```sh
# 在容器中查看时间
[root@8b931229efd4 ~]# date
Mon Jan 29 20:59:21 CST 2024

# 退出容器
[root@8b931229efd4 ~]# exit
[root@nexus ~]# 
```

可以看到，此时是正常的中国标准时间了。



重启nexus容器：

```sh
[root@nexus ~]# docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED      STATUS         PORTS                                                      NAMES
8b931229efd4   sonatype/nexus3:3.59.0   "/opt/sonatype/nexus…"   8 days ago   Up 3 minutes   0.0.0.0:8001-8003->8001-8003/tcp, 0.0.0.0:8081->8081/tcp   nexus
[root@nexus ~]# docker restart nexus
nexus
[root@nexus ~]# docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED      STATUS        PORTS                                                      NAMES
8b931229efd4   sonatype/nexus3:3.59.0   "/opt/sonatype/nexus…"   8 days ago   Up 1 second   0.0.0.0:8001-8003->8001-8003/tcp, 0.0.0.0:8081->8081/tcp   nexus
[root@nexus ~]#
```



查看neuxs容器最后20行日志：

```sh
[root@nexus ~]# docker logs -n 20 nexus
2024-01-29 21:08:34,314+0800 INFO  [jetty-main-1] *SYSTEM org.sonatype.nexus.internal.webresources.WebResourceServlet - Max-age: 30 days (2592000 seconds)
2024-01-29 21:08:34,321+0800 INFO  [jetty-main-1] *SYSTEM com.softwarementors.extjs.djn.servlet.DirectJNgineServlet - Servlet GLOBAL configuration: debug=false, providersUrl=service/extdirect, minify=false, batchRequestsMultithreadingEnabled=true, batchRequestsMinThreadsPoolSize=16, batchRequestsMaxThreadsPoolSize=80, batchRequestsMaxThreadsPerRequest=8, batchRequestsMaxThreadKeepAliveSeconds=60, gsonBuilderConfiguratorClass=org.sonatype.nexus.extdirect.internal.ExtDirectGsonBuilderConfigurator, dispatcherClass=com.softwarementors.extjs.djn.servlet.ssm.SsmDispatcher, jsonRequestProcessorThreadClass=org.sonatype.nexus.extdirect.internal.ExtDirectJsonRequestProcessorThread, contextPath=--not specified: calculated via Javascript--, createSourceFiles=true
2024-01-29 21:08:34,321+0800 INFO  [jetty-main-1] *SYSTEM com.softwarementors.extjs.djn.servlet.DirectJNgineServlet - Servlet GLOBAL configuration: registryConfiguratorClass=
2024-01-29 21:08:34,335+0800 INFO  [jetty-main-1] *SYSTEM com.softwarementors.extjs.djn.jscodegen.CodeFileGenerator - Creating source files for APIs...
2024-01-29 21:08:34,490+0800 INFO  [jetty-main-1] *SYSTEM org.sonatype.nexus.siesta.SiestaServlet - JAX-RS RuntimeDelegate: org.sonatype.nexus.siesta.internal.resteasy.SisuResteasyProviderFactory@7d8515a0
2024-01-29 21:08:34,525+0800 INFO  [jetty-main-1] *SYSTEM org.jboss.resteasy.plugins.validation.i18n - RESTEASY008550: Unable to find CDI supporting ValidatorFactory. Using default ValidatorFactory
2024-01-29 21:08:36,530+0800 INFO  [jetty-main-1] *SYSTEM org.sonatype.nexus.siesta.SiestaServlet - Initialized
2024-01-29 21:08:36,541+0800 INFO  [jetty-main-1] *SYSTEM org.sonatype.nexus.repository.httpbridge.internal.ViewServlet - Initialized
2024-01-29 21:08:36,572+0800 INFO  [jetty-main-1] *SYSTEM org.eclipse.jetty.server.handler.ContextHandler - Started o.e.j.w.WebAppContext@55ee9d51{Sonatype Nexus,/,file:///opt/sonatype/nexus/public/,AVAILABLE}
2024-01-29 21:08:36,620+0800 INFO  [jetty-main-1] *SYSTEM org.eclipse.jetty.server.AbstractConnector - Started ServerConnector@37d1e2d9{HTTP/1.1, (http/1.1)}{0.0.0.0:8081}
2024-01-29 21:08:36,620+0800 INFO  [jetty-main-1] *SYSTEM org.eclipse.jetty.server.Server - Started @38060ms
2024-01-29 21:08:36,620+0800 INFO  [jetty-main-1] *SYSTEM org.sonatype.nexus.bootstrap.jetty.JettyServer -
-------------------------------------------------

Started Sonatype Nexus OSS 3.59.0-01

-------------------------------------------------
2024-01-29 21:08:36,627+0800 INFO  [jetty-main-1] *SYSTEM org.eclipse.jetty.server.AbstractConnector - Started ServerConnector@21f42c2f{HTTP/1.1, (http/1.1)}{0.0.0.0:8002}
2024-01-29 21:08:36,630+0800 INFO  [jetty-main-1] *SYSTEM org.eclipse.jetty.server.AbstractConnector - Started ServerConnector@1b91877a{HTTP/1.1, (http/1.1)}{0.0.0.0:8003}
2024-01-29 21:08:36,631+0800 INFO  [jetty-main-1] *SYSTEM org.eclipse.jetty.server.AbstractConnector - Started ServerConnector@35b8a70c{HTTP/1.1, (http/1.1)}{0.0.0.0:8001}
[root@nexus ~]#
```

可以看到日志时间已经是正常的北京时间了，说明通过这种方法配置的时区没有问题。



再次在Nexus web管理控制台查看之前推送镜像到Nexus docket-hosted本地仓库的 mysql-client: push-by-ssl 镜像，其属性`last_modified`显示已经更新成北京时间了:

![](/img/Snipaste_2024-01-29_21-11-12.png)



再登陆容器里面确认一次容器里面的时间：

```sh
# 登陆到neuxs容器命令行
[root@nexus ~]# docker exec -it nexus /bin/bash
bash-4.4$ date
Mon Jan 29 21:13:57 CST 2024
bash-4.4$ exit
exit
[root@nexus ~]# date
Mon Jan 29 21:14:00 CST 2024
[root@nexus ~]#
```

可以看到，时间是北京时间！！！



至此，neuxs容器的时区修改成功了。

