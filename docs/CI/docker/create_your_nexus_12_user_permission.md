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
