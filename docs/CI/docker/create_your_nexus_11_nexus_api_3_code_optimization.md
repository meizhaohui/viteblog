#  搭建自己的nexus私有仓库11--Nexus API接口的使用优化

[[toc]]

本文档是nexus系列课程第11篇。

- nexus系列课程第1篇，请参考 [搭建自己的nexus私有仓库1--nexus初体验](./create_your_nexus.md)
- nexus系列课程第2篇，请参考 [搭建自己的nexus私有仓库2--创建python pypi代理](./create_your_nexus_2.md)
- nexus系列课程第3篇，请参考 [搭建自己的nexus私有仓库3--创建yum ius代理](./create_your_nexus_3.md)
- nexus系列课程第4篇，请参考 [搭建自己的nexus私有仓库4--创建docker私有仓库](./create_your_nexus_4_docker_proxy.md)
- nexus系列课程第5篇，请参考 [搭建自己的nexus私有仓库5--测试docker仓库pull和push](./create_your_nexus_5_test_docker_proxy.md)
- nexus系列课程第6篇，请参考 [搭建自己的nexus私有仓库6--使用nginx反向代理](./create_your_nexus_6_nginx_proxy.md)
- nexus系列课程第7篇，请参考 [搭建自己的nexus私有仓库7--修改nexus容器时区](./create_your_nexus_7_change_timezone.md)
- nexus系列课程第8篇，请参考 [搭建自己的nexus私有仓库8--Nexus3的数据库结构](./create_your_nexus_8_nexus_database.md) 
- nexus系列课程第9篇，请参考 [搭建自己的nexus私有仓库9--Nexus API接口的使用1](./create_your_nexus_9_nexus_api.md)
- nexus系列课程第10篇，请参考 [搭建自己的nexus私有仓库10--Nexus API接口的使用2](./create_your_nexus_10_nexus_api_2.md)
## 0. 情况说明

本篇是在前两篇的基础上，通过Python调用Nexus API接口创建Nexus相关仓库。

需要完成以下需求：


- [√] Neuxs API接口调用时，是否有动态Token，如何正确获取API接口Token值。
- [√] 创建docker blob对象存储，将docker单独存放在该blob对象存储中。
- [√] 激活【Docker Bearer Token Realm】，让能够匿名下载Docker镜像。
- [√] 创建yum、pypi、maven、docker之类的仓库，docker仓库由于涉及到三种类型的仓库创建，并且有端口配置，使用API时优先创建yum和pypi代理代理仓库来测试API接口。
- 快速创建一个用户账号，如账号名为`devops`，并将给其授权能够朝docker-hosted仓库推送镜像。



## 1. 优化Python代码

通过对比观察前两篇的Python代码可以发现以下特点：

- `payload`对应的json数据，可以直接写到Python代码中，也可以通过Python代码读取json文件来获取对应配置信息。
- 除了请求的API接口的`url`路径不一样，代码其他位置内容是一样的。
- 大部分的仓库可以直接根据json配置文件文件名来判断需要创建的仓库类型，为了自定义其他文件名，我们可以单独创建一个配置文件来定义json配置文件文件名与仓库类型的关系。

创建nexus_api文件夹，并在其中创建`config`配置文件夹：

![Snipaste_2024-03-03_18-07-22.png](/img/Snipaste_2024-03-03_18-07-22.png)

nexus_api文件夹目录结构如下：

```sh
$ find
.
./config
./config/docker-group.json
./config/docker-hosted.json
./config/docker-proxy.json
./config/epel-yum-proxy.json
./config/ius-yum-proxy.json
./config/maven-proxy.json
./config/nexus.yaml
./config/pypi-proxy.json
./config/yum-proxy.json
./main.py
./requirements.txt
```



## 1.1 定义nexus仓库的配置文件

`config/nexus.yaml`配置文件用于定义需要创建的仓库的配置文件与仓库类型的对应关系。

```yaml
nexus_info:
  Repositories:
    - file: yum-proxy.json
      type: proxy
      format: yum

    - name: epel-yum-proxy.json
      type: proxy
      format: yum

    - name: ius-yum-proxy.json
      type: proxy
      format: yum

    - name: pypi-proxy.json
      type: proxy
      format: pypi

    - name: maven-proxy.json
      type: proxy
      format: maven

    - name: docker-proxy.json
      type: proxy
      format: docker

    - name: docker-hosted.json
      type: hosted
      format: docker

    - name: docker-group.json
      type: group
      format: docker

```

如果有其他类型的仓库需要创建，只用创建对应的仓库的json配置文件，并增加到`config/nexus.yaml`配置文件中即可。



## 1.2 优化Python代码

使用`pipenv`创建虚拟环境，并安装相关依赖包：

```sh
$ pipenv run pip install requests yaml loguru
```

生成依赖文件：

```sh
$ pipenv run pip freeze
certifi==2024.2.2
charset-normalizer==3.3.2
colorama==0.4.6
idna==3.6
loguru==0.7.2
PyYAML==6.0.1
requests==2.31.0
urllib3==2.2.1
win32-setctime==1.1.0
$ pipenv run pip freeze > requirements.txt
$ 
```

