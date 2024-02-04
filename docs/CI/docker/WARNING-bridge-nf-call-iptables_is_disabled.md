# Docker Info bridge-nf-call-iptables is disabled警告处理

在执行`docker info`命令时，会提示以下警告：

## 警告描述

```sh
# docker info
.... docker相关信息，此处省略
 Live Restore Enabled: false

WARNING: bridge-nf-call-iptables is disabled
WARNING: bridge-nf-call-ip6tables is disabled
```

## 解决办法

执行以下命令：

```sh
# echo 'net.bridge.bridge-nf-call-ip6tables = 1' >> /etc/sysctl.conf
# echo 'net.bridge.bridge-nf-call-iptables = 1' >> /etc/sysctl.conf
```

查看配置是否生效：

```sh
# sysctl -p|grep 'net.bridge'
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
```

## 校验

再次执行`docker info`命令：

```sh
# docker info
Client:
 Context:    default
 Debug Mode: false
 Plugins:
  app: Docker App (Docker Inc., v0.9.1-beta3)
  buildx: Docker Buildx (Docker Inc., v0.7.1-docker)
  scan: Docker Scan (Docker Inc., v0.12.0)
... 省略
 Live Restore Enabled: false
# echo $?
0
```

可以看到，已经没有警告信息了。
