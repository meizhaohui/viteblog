
# docker配置redis缓存

我们可以使用redis来配置缓存，加速网站访问。

redis镜像：

```sh
[root@hellogitlab ~]# docker pull redis
Using default tag: latest
Trying to pull repository docker.io/library/redis ...
latest: Pulling from docker.io/library/redis
a076a628af6f: Already exists
f40dd07fe7be: Pull complete
ce21c8a3dbee: Pull complete
ee99c35818f8: Pull complete
56b9a72e68ff: Pull complete
3f703e7f380f: Pull complete
Digest: sha256:0f97c1c9daf5b69b93390ccbe8d3e2971617ec4801fd0882c72bf7cad3a13494
Status: Downloaded newer image for docker.io/redis:latest
[root@hellogitlab dockerdata]# docker images redis
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
docker.io/redis     latest              621ceef7494a        2 months ago        104 MB
```

在Redis官网下载一份redis安装程序，并解压，修改其中的`redis.conf`配置文件。

创建本地持久化目录：

```sh
[root@hellogitlab ~]# mkdir /dockerdata && cd /dockerdata
[root@hellogitlab dockerdata]# mkdir redis
[root@hellogitlab dockerdata]# cd redis
[root@hellogitlab redis]# wget http://download.redis.io/redis-stable/redis.conf
--2021-03-28 23:34:56--  http://download.redis.io/redis-stable/redis.conf
正在解析主机 download.redis.io (download.redis.io)...
2021-03-28 23:34:57 (97.1 KB/s) - 已保存 “redis.conf” [92222/92222])
# 修改redis.conf内容
[root@hellogitlab redis]#
# 查看所有配置
[root@hellogitlab redis]# grep -v '#' redis.conf|grep -v '^$'|sort
acllog-max-len 128
activerehashing yes
always-show-logo yes
aof-load-truncated yes
aof-rewrite-incremental-fsync yes
aof-use-rdb-preamble yes
appendfilename "appendonly.aof"
appendfsync everysec
appendonly yes
auto-aof-rewrite-min-size 64mb
auto-aof-rewrite-percentage 100
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit pubsub 32mb 8mb 60
client-output-buffer-limit replica 256mb 64mb 60
daemonize no
databases 16
dbfilename dump.rdb
dir ./
dynamic-hz yes
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
hll-sparse-max-bytes 3000
hz 10
jemalloc-bg-thread yes
latency-monitor-threshold 0
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
lazyfree-lazy-user-del no
list-compress-depth 0
list-max-ziplist-size -2
logfile "/data/redis.log"
loglevel notice
lua-time-limit 5000
no-appendfsync-on-rewrite no
notify-keyspace-events ""
pidfile /var/run/redis_6378.pid
port 6378
protected-mode yes
rdbchecksum yes
rdbcompression yes
rdb-del-sync-files no
rdb-save-incremental-fsync yes
repl-disable-tcp-nodelay no
repl-diskless-load disabled
repl-diskless-sync-delay 5
repl-diskless-sync no
replica-lazy-flush no
replica-priority 100
replica-read-only yes
replica-serve-stale-data yes
requirepass **************securepassword******************
save 300 10
save 60 10000
save 900 1
set-max-intset-entries 512
slowlog-log-slower-than 10000
slowlog-max-len 128
stop-writes-on-bgsave-error yes
stream-node-max-bytes 4096
stream-node-max-entries 100
supervised no
tcp-backlog 511
tcp-keepalive 300
timeout 0
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
[root@hellogitlab redis]#
```

注意以下需要关注的配置：

```ini
# 注释掉这部分，使redis可以外部访问
# bind 127.0.0.1
# 不用守护线程的方式启动，默认是no，如设置为yes后台守护进程,则redis启动后就马上退出！！注意此处！！！！！！！
daemonize no
# 给redis设置密码，注意密码不要让别人知道
requirepass 你的密码
# redis持久化,默认是no
appendonly yes
# 防止出现远程主机强迫关闭了一个现有的连接的错误，保持默认300即可
tcp-keepalive 300
# 设置保护模式，禁止远程访问，仅本机访问
protected-mode yes
# 修改端口号，默认6379，修改为6378
port 6378
# pidfile文档
pidfile /var/run/redis_6378.pid
# 日志文件,不要设置为`/var/log/redis/redis.log`，否则会存在日志文件不存在的异常
logfile "/data/redis.log"
```

启动redis:

```jsx
[root@hellogitlab ~]# docker run --name redis-server --restart=always -p 6378:6378 -v /dockerdata/redis/redis.conf:/etc/redis/redis.conf -v /dockerdata/redis/data:/data -d redis:latest redis-server /etc/redis/redis.conf
ecef03de2237f243d031cafae5fc4870f4dee7d33aa269038fe7f180c2dfd66d
```

参数解释：

```sh
`docker run` 运行docker容器
`--name redis-server`  指定容器名称
`--restart=always` docker重启后，启动容器
`-p 6378:6378`  把容器内的6378端口映射到宿主机6378端口
`-v /dockerdata/redis/redis.conf:/etc/redis/redis.conf` 把主机上的redis.conf放在容器的/etc/redis/redis.conf位置
`-v /dockerdata/redis/data:/data` 把redis持久化的数据在宿主机内显示，做数据备份,也就是把redis数据存在宿主机的/dockerdata/redis/data目录下
`-d redis:latest` 在后台运行redis容器
`redis-server /etc/redis/redis.conf` 关键配置，让redis不是无配置启动，而是按照/etc/redis/redis.conf的配置启动的
```

如果你启动过程中redis一直重启，有可能就是你的`daemoniz`配置成了`daemonize yes`，导致redis在后台运行。而docker容器必须要有一个前台进程才能留存否则容器会自动退出。



查看运行情况：

```sh
[root@hellogitlab redis]# docker ps |head -n 1; docker ps|grep redis-server
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                              NAMES
ecef03de2237        redis:latest        "docker-entrypoint..."   41 seconds ago      Up 40 seconds       0.0.0.0:6378->6378/tcp, 6379/tcp   redis-server
```

我们在宿主机上安装一下`redis`工具，使用命令行连接redis容器：

```sh
[root@hellogitlab ~]# yum install redis -y
[meizhaohui@hellogitlab ~]$ redis-cli -p 6378 -a "securepassword"
127.0.0.1:6378> get a
"b"
127.0.0.1:6378> set b c
OK
127.0.0.1:6378> get b
"c"
127.0.0.1:6378>
```

说明能够正常写入数据到redis中。



查询所有key:

```sh
127.0.0.1:6378> keys *
  1) "f944948d6e25ff6be26d865176a21c4a/imagePath-ad10a4b5e8c0338e5a79b03b164af307-integration_gitlab-app.svg"
  2) "b57a02f0af280eb6ce504c367c12e078/imagePath-ad10a4b5e8c0338e5a79b03b164af307-dashboard-favicon.ico"
  3) "b57a02f0af280eb6ce504c367c12e078/imagePath-ad10a4b5e8c0338e5a79b03b164af307-core-desktopapp.svg"
  4) "b57a02f0af280eb6ce504c367c12e078/imagePath-ad10a4b5e8c0338e5a79b03b164af307-settings-favicon.ico"
  5) "f944948d6e25ff6be26d865176a21c4a/imagePath-ad10a4b5e8c0338e5a79b03b164af307-passwords-favicon.ico"
  6) "f944948d6e25ff6be26d865176a21c4a/imagePath-ad10a4b5e8c0338e5a79b03b164af307-user_status-app.svg"
  7) "f944948d6e25ff6be26d865176a21c4a/imagePath-ad10a4b5e8c0338e5a79b03b164af307-privacy-app-dark.svg"
  8) "PHPREDIS_SESSION:06e5ea25cde5b68c2c6d0a5953ed981e"
  9) "PHPREDIS_SESSION:6c4158267fae83bf947def98c6e394ef"
```

使用`flushdb`删除所有key:

```sh
127.0.0.1:6378> flushdb
OK
127.0.0.1:6378> keys *
(empty list or set)
```



