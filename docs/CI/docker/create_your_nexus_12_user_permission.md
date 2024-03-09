#  搭建自己的nexus私有仓库12--Nexus权限配置

[[toc]]

本文档是nexus系列课程第12篇，使用Nexus API接口配置用户权限。

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
- nexus系列课程第11篇，请参考 [搭建自己的nexus私有仓库11--Nexus API接口的使用优化](./create_your_nexus_11_nexus_api_3_code_optimization.md)

## 0. 情况说明

nexus系列课程第9-11篇详细讲解了通过Python调用Nexus API接口创建Nexus相关仓库。

已经完成以下需求：

- [√] Neuxs API接口调用时，是否有动态Token，如何正确获取API接口Token值。
- [√] 创建docker blob对象存储，将docker单独存放在该blob对象存储中。
- [√] 激活【Docker Bearer Token Realm】，让能够匿名下载Docker镜像。
- [√] 创建yum、pypi、maven、docker之类的仓库，docker仓库由于涉及到三种类型的仓库创建，并且有端口配置，使用API时优先创建yum和pypi代理代理仓库来测试API接口。

本篇需要完成以下需求：

- 快速创建一个用户账号，如账号名为`devops`，并将给其授权能够朝docker-hosted仓库推送镜像。



## 1. 业务分析

在创建用户前，我们先分析一下现有用户是如何配置了。



## 1.1 本地账号分析

在Nexus管理页面，依次点击【Security】-【Users】:

![Snipaste_2024-03-09_19-57-47.png](/img/Snipaste_2024-03-09_19-57-47.png)

可以看到，当前有两个本地用户，一个是`admin`管理员用户，另外一个是`anonymous`匿名用户。点击一下`anonymous`匿名用户，查看其有什么权限：

![Snipaste_2024-03-09_20-01-31.png](/img/Snipaste_2024-03-09_20-01-31.png)

可以看到有以下信息：

- ID: anonymous
- First Name: Anonymous
- Last Name: User
- Email: anonymous@example.org
- Status: Active
- Roles: nx-anonymous

再看一下`admin`管理员用户的信息：

![Snipaste_2024-03-09_20-03-53.png](/img/Snipaste_2024-03-09_20-03-53.png)

可以看到管理人配置的信息如下：

- ID: admin
- First Name: Administrator
- Last Name: User
- Email: admin@example.org
- Status: Active
- Roles: nx-admin



可以看到，用户权限是通过Roles角色来控制的，管理员用户配置了`nx-admin`角色，匿名用户配置了`nx-anonymous`角色。



### 1.2 角色分析

在Nexus管理页面，依次点击【Security】-【Roles】:

![Snipaste_2024-03-09_20-08-16.png](/img/Snipaste_2024-03-09_20-08-16.png)

可以看到，有`nx-admin`和`nx-anonymous`两个角色。

`nx-admin`角色详情如下：

![Snipaste_2024-03-09_20-09-26.png](/img/Snipaste_2024-03-09_20-09-26.png)

即：

- Role ID: nx-admin

- Role Name: nx-admin

- Role Description:  Administrator Role 

- Privileges: nx-all

而`nx-anonymous`角色详情如下：

![Snipaste_2024-03-09_20-12-08.png](/img/Snipaste_2024-03-09_20-12-08.png)

即：

- Role ID:  nx-anonymous 
- Role Name:  nx-anonymous 
- Role Description:   Anonymous Role 
- Privileges: 
  - nx-healthcheck-read
  - nx-search-read
  - nx-repository-view-*-*-read
  - nx-repository-view-*-*-browse

通过分析匿名用户的权限可以知道，在未登陆Nexus系统时，匿名用户是可以搜索仓库和在Browse浏览器中浏览仓库信息的。我们要创建的devops用户，只需要比匿名用户新增朝`docker-hosted`本地仓库推送镜像的权限即可。



### 1.3 权限分析

在Nexus管理页面，依次点击【Security】-【Privileges】，并搜索docker关键字，查看docker查看的权限：

![Snipaste_2024-03-09_20-24-06.png](/img/Snipaste_2024-03-09_20-24-06.png)

为了让devops这个普通用户能够上传docker镜像，我们需要增加`nx-repository-view-docker-docker-hosted-add`权限。

我们先来创建一个测试