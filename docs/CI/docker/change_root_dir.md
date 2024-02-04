# 修改默认数据存储目录

默认情况下，docker数据存储目录为`/var/lib/docker`,可以通过`docker info`查看：

```sh
# docker info|grep 'Docker Root Dir'
 Docker Root Dir: /var/lib/docker
```

可以通过以下方式个性数据存储目录。

- 方式一，修改启动配置`/usr/lib/systemd/system/docker.service`。
- 方式二，修改配置文件`/etc/docker/daemon.json`。

## 1. 修改启动配置

查看默认的启动配置：

```sh
# grep 'ExecStart' /usr/lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
```

查看`dockerd`帮助信息：

```sh
# dockerd --help|grep 'data-root'
      --data-root string                        Root directory of persistent Docker state (default "/var/lib/docker")
```

可以看到，只用增加`--data-root`参数就可以设置数据存储目录，我们在启动配置中增加`--data-root=/data/docker`配置，修改后配置如下：

```sh
# grep 'ExecStart' /usr/lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H fd:// --data-root=/data/docker --containerd=/run/containerd/containerd.sock
```

注意，此处的数据存储目录`/data/docker`不需要我们手动创建。

重新加载配置并重启docker服务：

```sh
# 重新加载配置
# systemctl daemon-reload

# 重启docker服务
# systemctl restart docker

# 查看docker服务状态
# systemctl status docker
```



查看目录信息：

```sh
# ls -lah /data/docker/
total 52K
drwx--x--x 13 root root 4.0K Jul 29 07:19 .
drwxr-xr-x  3 root root 4.0K Jul 29 07:19 ..
drwx--x--x  4 root root 4.0K Jul 29 07:19 buildkit
drwx-----x  2 root root 4.0K Jul 29 07:19 containers
drwx------  3 root root 4.0K Jul 29 07:19 image
drwxr-x---  3 root root 4.0K Jul 29 07:19 network
drwx-----x  3 root root 4.0K Jul 29 07:19 overlay2
drwx------  4 root root 4.0K Jul 29 07:19 plugins
drwx------  2 root root 4.0K Jul 29 07:19 runtimes
drwx------  2 root root 4.0K Jul 29 07:19 swarm
drwx------  2 root root 4.0K Jul 29 07:19 tmp
drwx------  2 root root 4.0K Jul 29 07:19 trust
drwx-----x  2 root root 4.0K Jul 29 07:19 volumes
# ls -lah /var/lib/docker/
total 52K
drwx--x--x  13 root root 4.0K Jul 29 07:19 .
drwxr-xr-x. 34 root root 4.0K Apr 30 22:43 ..
drwx--x--x   4 root root 4.0K Mar 17 09:12 buildkit
drwx-----x   2 root root 4.0K Mar 17 09:12 containers
drwx------   3 root root 4.0K Mar 17 09:12 image
drwxr-x---   3 root root 4.0K Mar 17 09:12 network
drwx-----x  38 root root 4.0K Jul 29 07:19 overlay2
drwx------   4 root root 4.0K Mar 17 09:12 plugins
drwx------   2 root root 4.0K Jul 29 07:19 runtimes
drwx------   2 root root 4.0K Mar 17 09:12 swarm
drwx------   2 root root 4.0K Jul 29 07:19 tmp
drwx------   2 root root 4.0K Mar 17 09:12 trust
drwx-----x   2 root root 4.0K Jul 29 07:19 volumes
# du -sh /var/lib/docker/
2.1G	/var/lib/docker/
# du -sh /data/docker/
244K	/data/docker/
```

可以看到修改数据存储目录后，原先的存储的数据并没有完成复制到新的存储目录中。

将原来目录中的文件迁移到新的目录中：

```sh
# 复制原来的数据目录
# /bin/cp -rf /var/lib/docker /data/

# 重启docker服务
# systemctl restart docker

# 再次查看镜像，可以看到镜像数据又恢复了
# docker images

# 查看新的数据目录信息
# docker info|grep Root
 Docker Root Dir: /data/docker
```

## 2. 修改配置文件

我们将先启动配置文件还原，然后再重启docker服务：

```sh
# 使用vim编辑启动文件保存后，查看启动命令
# grep 'ExecStart' /usr/lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

# 重新加载配置
# systemctl daemon-reload

# 重启docker服务
# systemctl restart docker

# 查看当前数据存储目录，可以数据存储目录已经还原了
# docker info|grep Root
 Docker Root Dir: /var/lib/docker
```

修改配置文件`/etc/docker/daemon.json`，如果该文件不存在则创建该文件。

```sh
# cat /etc/docker/daemon.json
{
    "data-root": "/data/docker"
}
```

然后重启docker服务：

```sh
# 重启docker服务
# systemctl restart docker

# 查看当前数据存储目录
# docker info|grep Root
 Docker Root Dir: /data/docker
```

可以看到数据存储目录已经更新了。



