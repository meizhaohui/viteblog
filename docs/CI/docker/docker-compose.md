# docker-compose的使用

[[toc]]


## 1. 概述

> Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services. Then, with a single command, you create and start all the services from your configuration.
> 
> Compose works in all environments; production, staging, development, testing, as well as CI workflows. It also has commands for managing the whole lifecycle of your application:
> - Start, stop, and rebuild services
> - View the status of running services
> - Stream the log output of running services
> - Run a one-off command on a service

即：

- Docker Compose 是一个用于管理多容器的Docker应用程序的工具。通过compose，你可以通过YAML文件来定义配置你的应用服务，然后通过一个单一命令，就可以创建并启动你配置的所有的服务。 
- Compose能运行在各种环境下，像生产环境、预发布环境、开发环境、测试环境、CI工作流等，有管理应用全生命周期的命令。
    - start启动、stop停止、rebuild重新构建服务。
    - 查看运行服务的状态信息。
    - 查看运行服务的日志信息。
    - 对服务运行一次性命令。
- compose手册[Docker Compose overview](https://docs.docker.com/compose/)
- 从 2023 年 7 月起，Compose V1 停止接收更新。 它在新版本的 Docker Desktop 中也不再可用。
- Compose V2 包含在所有当前支持的 Docker Desktop 版本中。
- compose参考文档 [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/compose-file-v3/)
- Docker compose允许你使用 YAML 文件来定义应用程序的服务、网络和卷等内容，并在单个主机或多个主机上进行部署。Docker Compose 有以下版本：
    - v1：这是最早的版本，支持基本功能，如构建镜像、启动容器、设置环境变量等。废弃不用。
    - v2.x：增加了对Swarm模式的支持，可以通过docker stack命令将Compose文件部署到Swarm集群中。
    - v3.x：引入了一些新特性，例如配置命名空间、healthcheck检查、秘密管理等。同时也提供了对Kubernetes的支持。
- 在 `docker-compose.yml`文件中指定的version必须与安装在主机上的Docker Compose版本相匹配。如果使用不同版本之间的兼容性问题，则可能会导致意外行为或错误。
- Docker Compose有几个版本，每个版本都提供了不同的特性和兼容性。在编写`docker-compose.yml`文件时，请确保所指定的version与主机上安装的Docker Compose版本相匹配，以避免任何问题。




## 2. docker-compose与docker版本对应关系

This table shows which Compose file versions support specific Docker releases.

|compose文件版本|docker引擎版本|
|:---:|:--------:|
| Compose specification | 19.03.0+ |
| 3.8 | 19.03.0+ |
| 3.7 | 18.06.0+ |
| 3.6 | 18.02.0+ |
| 3.5 | 17.12.0+ |
| 3.4 | 17.09.0+ |
| 3.3 | 17.06.0+ |
| 3.2 | 17.04.0+ |
| 3.1 | 1.13.1+  |
| 3   | 1.13.0+  |
| 2.4 | 17.12.0+ |
| 2.3 | 17.06.0+ |
| 2.2 | 1.13.0+  |
| 2.1 | 1.12.0+  |
| 2   | 1.10.0+  |
