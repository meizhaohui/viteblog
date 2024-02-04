# 通过进程pid查询对应docker容器信息

[[toc]]

## 1. 一般获取方法

我们都知道Docker容器的哲学是一个Docker容器只运行一个进程。在这种情况下，我们可以很容器找到进程和容器的对应关系。

如，我们在进程中发现有一个`redis-server`的程序：

```sh
[root@docker ~]# ps -ef|grep -v grep|grep redis
polkitd  17942 17923  0 22:36 ?        00:00:03 redis-server *:6379
```

可以知道，其进程PID是`17942`。

### 1.1 通过`docker top`命令查看

当我们服务器上面运行的容器不多时，可以直接使用这种方式查看：

```sh
# 查看运行的容器
[root@docker ~]# docker ps
CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS             PORTS                    NAMES
77e8f1f47d09   meizhaohui/testimage:v1   "/bin/bash /root/run…"   22 minutes ago   Up 22 minutes                               wizardly_carson
80bbd285db0b   sonatype/nexus3:3.59.0    "/opt/sonatype/nexus…"   2 weeks ago      Up 2 weeks         0.0.0.0:8081->8081/tcp   nexus
790a0902c364   e0ce02f88e58              "docker-entrypoint.s…"   4 weeks ago      Up About an hour   0.0.0.0:6375->6379/tcp   redis-6375
[root@docker ~]#
```

可以看到，也就三个容器，直接`docker top`分别查看三个容器运行的进程信息即可：

```sh
[root@docker ~]# docker top wizardly_carson
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                5229                29140               0                   23:45               pts/0               00:00:00            sleep 1
root                29140               29120               0                   23:19               pts/0               00:00:00            /bin/bash /root/run.sh /bin/bash
root                29181               29140               0                   23:19               pts/0               00:00:00            ping baidu.com -c 10000
root                29182               29140               0                   23:19               pts/0               00:00:00            ping baidu.com -c 10000
[root@docker ~]# docker top nexus
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
200                 5265                5245                0                   Aug21               ?                   02:36:11            /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.382.b05-2.el8.x86_64/jre/bin/java -server -Dinstall4j.jvmDir=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.382.b05-2.el8.x86_64/jre -Dexe4j.moduleName=/opt/sonatype/nexus/bin/nexus -XX:+UnlockDiagnosticVMOptions -Dinstall4j.launcherId=245 -Dinstall4j.swt=false -Di4jv=0 -Di4jv=0 -Di4jv=0 -Di4jv=0 -Di4jv=0 -Xms2703m -Xmx2703m -XX:MaxDirectMemorySize=2703m -Djava.util.prefs.userRoot=/nexus-data/javaprefs -XX:+UnlockDiagnosticVMOptions -XX:+LogVMOutput -XX:LogFile=../sonatype-work/nexus3/log/jvm.log -XX:-OmitStackTraceInFastThrow -Djava.net.preferIPv4Stack=true -Dkaraf.home=. -Dkaraf.base=. -Dkaraf.etc=etc/karaf -Djava.util.logging.config.file=etc/karaf/java.util.logging.properties -Dkaraf.data=../sonatype-work/nexus3 -Dkaraf.log=../sonatype-work/nexus3/log -Djava.io.tmpdir=../sonatype-work/nexus3/tmp -Dkaraf.startLocalConsole=false -Djdk.tls.ephemeralDHKeySize=2048 -Djava.endorsed.dirs=lib/endorsed -Di4j.vpt=true -classpath /opt/sonatype/nexus/.install4j/i4jruntime.jar:/opt/sonatype/nexus/lib/boot/nexus-main.jar:/opt/sonatype/nexus/lib/boot/activation-1.1.1.jar:/opt/sonatype/nexus/lib/boot/jakarta.xml.bind-api-2.3.3.jar:/opt/sonatype/nexus/lib/boot/jaxb-runtime-2.3.3.jar:/opt/sonatype/nexus/lib/boot/txw2-2.3.3.jar:/opt/sonatype/nexus/lib/boot/istack-commons-runtime-3.0.10.jar:/opt/sonatype/nexus/lib/boot/org.apache.karaf.main-4.3.9.jar:/opt/sonatype/nexus/lib/boot/osgi.core-7.0.0.jar:/opt/sonatype/nexus/lib/boot/org.apache.karaf.specs.activator-4.3.9.jar:/opt/sonatype/nexus/lib/boot/org.apache.karaf.diagnostic.boot-4.3.9.jar:/opt/sonatype/nexus/lib/boot/org.apache.karaf.jaas.boot-4.3.9.jar com.install4j.runtime.launcher.UnixLauncher run 9d17dc87 0 0 org.sonatype.nexus.karaf.NexusMain
[root@docker ~]# docker top redis-6375
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
polkitd             17942               17923               0                   22:36               ?                   00:00:03            redis-server *:6379
[root@docker ~]#
```

![](/img/Snipaste_2023-09-09_23-46-25.png)

可以看到最后一个容器`redis-6375`的PID是`17942`，刚好与我们要查找到redis进程`17942`相同。这样就找到了进程对应的容器名称，也是知道了容器信息了。


### 1.2 通过`docker inspect`命令查看

通过`docker inspect`可以获取容器的远数据信息。

我们可以通过依次检查三个运行的容器的元数据信息：

```sh
[root@docker ~]# docker inspect wizardly_carson|jq '.[0].State'
{
  "Status": "running",
  "Running": true,
  "Paused": false,
  "Restarting": false,
  "OOMKilled": false,
  "Dead": false,
  "Pid": 29140,
  "ExitCode": 0,
  "Error": "",
  "StartedAt": "2023-09-09T15:19:01.819911076Z",
  "FinishedAt": "0001-01-01T00:00:00Z"
}
[root@docker ~]# docker inspect wizardly_carson|jq '.[0].State.Pid'
29140
[root@docker ~]# docker inspect nexus|jq '.[0].State.Pid'
5265
[root@docker ~]# docker inspect redis-6375|jq '.[0].State.Pid'
17942
[root@docker ~]#
```

运行效果图：

![](/img/Snipaste_2023-09-09_23-52-15.png)
### 1.3 通过ps命令查看

通过`man ps`可以看到有这样的帮助信息：

```sh
To see every process with a user-defined format:
          ps -eo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,wchan:14,comm
          ps axo stat,euid,ruid,tty,tpgid,sess,pgrp,ppid,pid,pcpu,comm
          ps -Ao pid,tt,user,fname,tmout,f,wchan
```

我们使用`ps -eo`命令来输出指定样式的结果。

我们主要使用`pid`和`cgroup`信息：

```sh
[root@docker ~]# ps -eo 'pid,cgroup'|grep -v grep |grep 17942
17942 11:blkio:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,10:pids:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,9:devices:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,8:freezer:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,7:cpuset:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,6:perf_event:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,5:memory:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,4:hugetlb:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,3:cpuacct,cpu:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,2:net_prio,net_cls:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095,1:name=systemd:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
```

![](/img/Snipaste_2023-09-10_00-01-14.png)
查询出的结果中包含有docker容器的id值相关的信息，如以上结果中`/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095`字符串中`790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095`就是容器的长ID信息。

再通过`docker ps`反查容器ID对应的容器信息：

```sh
[root@docker ~]# docker ps --no-trunc|grep 790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095   sha256:e0ce02f88e589621ae0c99073142b587c1bbe3cfbab70b484e7af700d7057e0e   "docker-entrypoint.sh redis-server"   4 weeks ago      Up About an hour   0.0.0.0:6375->6379/tcp   redis-6375
```

这样也获取到了进程对应的容器是`redis-6375`。

### 1.4 查看进程/proc/$PID/cgroup文件

如进程变量`PID=17942`，直接查看`/proc/$PID/cgroup`文件内容：

```sh
[root@docker ~]# PID=17942
[root@docker ~]# cat /proc/$PID/cgroup
11:blkio:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
10:pids:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
9:devices:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
8:freezer:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
7:cpuset:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
6:perf_event:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
5:memory:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
4:hugetlb:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
3:cpuacct,cpu:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
2:net_prio,net_cls:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
1:name=systemd:/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095
[root@docker ~]#
```

也可以知道进程对应的容器长ID是`790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095`。像上节一样使用`docker ps --no-trunc`命令也可以查到对应容器是`redis-6375`。

### 1.5 异常容器示例

我们都知道Docker容器的哲学是一个Docker容器只运行一个进程,但是有时候我们就是需要在一个Docker容器中运行多个进程。也就有可能容器进程创建了新的子进程。

就像我们运行的`wizardly_carson`容器一样：

```sh
[root@docker ~]# docker top wizardly_carson
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                13132               29140               0                   00:11               pts/0               00:00:00            sleep 1
root                29140               29120               0                   Sep09               pts/0               00:00:00            /bin/bash /root/run.sh /bin/bash
root                29181               29140               0                   Sep09               pts/0               00:00:00            ping baidu.com -c 10000
root                29182               29140               0                   Sep09               pts/0               00:00:00            ping baidu.com -c 10000
[root@docker ~]# docker top wizardly_carson
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                13176               29140               0                   00:11               pts/0               00:00:00            sleep 1
root                29140               29120               0                   Sep09               pts/0               00:00:00            /bin/bash /root/run.sh /bin/bash
root                29181               29140               0                   Sep09               pts/0               00:00:00            ping baidu.com -c 10000
root                29182               29140               0                   Sep09               pts/0               00:00:00            ping baidu.com -c 10000
[root@docker ~]#
```

如我们的两个长ping进程`ping baidu.com -c 10000`，一个是`29181`，另一个是`29182`，都是容器进程`29140`的子进程。

这个时候我们如果想知道`29181`是哪个容器的进程，则使用上述1.1-1.4节的方法可能有点难以确认。

`docker top`就不试了，因为我们是从`docker top wizardly_carson`看到进程`29181`是个子进程。


我们尝试一下其他方法：

```sh
[root@docker ~]# docker inspect wizardly_carson|jq '.[0].State.Pid'
29140
[root@docker ~]# docker inspect wizardly_carson|jq|grep 29181
[root@docker ~]# docker inspect nexus|jq '.[0].State.Pid'
5265
[root@docker ~]# docker inspect redis-6375|jq '.[0].State.Pid'
17942
[root@docker ~]#
```

直接通过`docker inspect`未能获取到子进程信息。


```sh
[root@docker ~]# ps -eo 'pid,cgroup'|grep -v grep |grep 29181
29181 11:blkio:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,10:pids:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,9:devices:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,8:freezer:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,7:cpuset:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,6:perf_event:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,5:memory:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,4:hugetlb:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,3:cpuacct,cpu:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,2:net_prio,net_cls:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15,1:name=systemd:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
```
通过`ps`查看`cgroup`信息获取到容器长ID信息。

```sh
[root@docker ~]# PID=29181
[root@docker ~]# cat /proc/$PID/cgroup
11:blkio:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
10:pids:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
9:devices:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
8:freezer:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
7:cpuset:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
6:perf_event:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
5:memory:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
4:hugetlb:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
3:cpuacct,cpu:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
2:net_prio,net_cls:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
1:name=systemd:/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15
[root@docker ~]#
```
直接查看`/proc/$PID/cgroup`文件内容也获取到了。


## 2. 终极获取方法

可以直接在`/sys/fs/cgroup/memory/docker`目录下搜索`cgroup.procs`文件，该文件会记录每个容器对应的Pid和子进程Pid信息。

查看目录下的文件列表信息：

```sh
[root@docker ~]# ls /sys/fs/cgroup/memory/docker
77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15  memory.kmem.tcp.failcnt             memory.numa_stat
790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095  memory.kmem.tcp.limit_in_bytes      memory.oom_control
80bbd285db0bc84a50b785a2aeb688d8bf6879e5fa1381357fa1426a9f38148a  memory.kmem.tcp.max_usage_in_bytes  memory.pressure_level
cgroup.clone_children                                             memory.kmem.tcp.usage_in_bytes      memory.soft_limit_in_bytes
cgroup.event_control                                              memory.kmem.usage_in_bytes          memory.stat
cgroup.procs                                                      memory.limit_in_bytes               memory.swappiness
memory.failcnt                                                    memory.max_usage_in_bytes           memory.usage_in_bytes
memory.force_empty                                                memory.memsw.failcnt                memory.use_hierarchy
memory.kmem.failcnt                                               memory.memsw.limit_in_bytes         notify_on_release
memory.kmem.limit_in_bytes                                        memory.memsw.max_usage_in_bytes     tasks
memory.kmem.max_usage_in_bytes                                    memory.memsw.usage_in_bytes
memory.kmem.slabinfo                                              memory.move_charge_at_immigrate
[root@docker ~]#
```

查找`cgroup.procs`文件：
```sh
[root@docker ~]# find /sys/fs/cgroup/memory/docker -name 'cgroup.procs'
/sys/fs/cgroup/memory/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15/cgroup.procs
/sys/fs/cgroup/memory/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095/cgroup.procs
/sys/fs/cgroup/memory/docker/80bbd285db0bc84a50b785a2aeb688d8bf6879e5fa1381357fa1426a9f38148a/cgroup.procs
/sys/fs/cgroup/memory/docker/cgroup.procs
```

查找`cgroup.procs`文件，然后在查找到的文件中搜索我们想匹配的进程`29181`:
```sh
[root@docker ~]# find /sys/fs/cgroup/memory/docker -name 'cgroup.procs'|xargs grep --color=always 29181
/sys/fs/cgroup/memory/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15/cgroup.procs:29181
[root@docker ~]#
```
![](/img/Snipaste_2023-09-10_00-31-24.png)

可以看到，在文件`/sys/fs/cgroup/memory/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15/cgroup.procs`中匹配到了该进程。

使用该方法，可以随意匹配任意容器进程或其子进程，然后通过文件路径确定容器的长ID值。

编写快捷命令：

```sh
alias gcbp='get_container_by_pid'
# 通过进程PID查询容器信息
function get_container_by_pid() {
    pid=$1
    find /sys/fs/cgroup/memory/docker -name 'cgroup.procs'|xargs grep --color=always "${pid}"
    container_id=$(find /sys/fs/cgroup/memory/docker -name 'cgroup.procs'|xargs grep "${pid}"|awk -F'/' '{print $7}'|cut -c1-12)
    if [[ -n "${container_id}" ]]; then
    	docker ps|head -n 1 ; docker ps |grep --color=always "${container_id}"
    else
    	echo "进程 ${pid} 不在任何一个容器中，请检查"
    fi
}
```

将以上信息存放到`~/.bashrc`文件中，然后使用`source ~/.bashrc`加载配置。

然后进行测试：

```sh
# 查看wizardly_carson容器的PID,可以看到能够匹配到容器信息
[root@docker ~]# gcbp 29140
/sys/fs/cgroup/memory/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15/cgroup.procs:29140
CONTAINER ID   IMAGE                     COMMAND                  CREATED       STATUS       PORTS                    NAMES
77e8f1f47d09   meizhaohui/testimage:v1   "/bin/bash /root/run…"   2 hours ago   Up 2 hours                            wizardly_carson

# 查看wizardly_carson容器子进程的PID,可以看到能够匹配到容器信息
[root@docker ~]# gcbp 29181
/sys/fs/cgroup/memory/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15/cgroup.procs:29181
CONTAINER ID   IMAGE                     COMMAND                  CREATED       STATUS       PORTS                    NAMES
77e8f1f47d09   meizhaohui/testimage:v1   "/bin/bash /root/run…"   2 hours ago   Up 2 hours                            wizardly_carson

# 查看wizardly_carson容器子进程的PID,可以看到能够匹配到容器信息
[root@docker ~]# gcbp 29182
/sys/fs/cgroup/memory/docker/77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15/cgroup.procs:29182
CONTAINER ID   IMAGE                     COMMAND                  CREATED       STATUS       PORTS                    NAMES
77e8f1f47d09   meizhaohui/testimage:v1   "/bin/bash /root/run…"   2 hours ago   Up 2 hours                            wizardly_carson

# 查看nexus容器的进程，可以看到能够匹配到容器信息
[root@docker ~]# gcbp 5265
/sys/fs/cgroup/memory/docker/80bbd285db0bc84a50b785a2aeb688d8bf6879e5fa1381357fa1426a9f38148a/cgroup.procs:5265
CONTAINER ID   IMAGE                     COMMAND                  CREATED       STATUS       PORTS                    NAMES
80bbd285db0b   sonatype/nexus3:3.59.0    "/opt/sonatype/nexus…"   2 weeks ago   Up 2 weeks   0.0.0.0:8081->8081/tcp   nexus

# 查看redis-6375容器的进程，可以看到能够匹配到容器信息
[root@docker ~]# gcbp 17942
/sys/fs/cgroup/memory/docker/790a0902c36417b1388820b59d9156181d718a327bb6fa09880c4568fdd07095/cgroup.procs:17942
CONTAINER ID   IMAGE                     COMMAND                  CREATED       STATUS       PORTS                    NAMES
790a0902c364   e0ce02f88e58              "docker-entrypoint.s…"   4 weeks ago   Up 2 hours   0.0.0.0:6375->6379/tcp   redis-6375

# 查看containerd-shim-runc-v2进程，可以看到未能匹配到容器信息
[root@docker ~]# gcbp 29120
进程 29120 不在任何一个容器中，请检查
[root@docker ~]# ps -ef|grep -v grep|grep 29120
root     29120     1  0 Sep09 ?        00:00:04 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 77e8f1f47d093f6136e7a7bdf65ac3b87974922a200b2ce05a551cc6485d6d15 -address /run/containerd/containerd.sock
root     29140 29120  0 Sep09 pts/0    00:00:01 /bin/bash /root/run.sh /bin/bash
[root@docker ~]#
```

![](/img/Snipaste_2023-09-10_00-58-11.png)

到此，可以看到，最后的快捷命令可以通用上，匹配上容器进程或容器子进程，不在容器中的进程也给出提示。

参考：

- [在docker宿主机上查找指定容器内运行的所有进程的PID](https://www.cnblogs.com/keithtt/p/7591097.html)
- [Docker - 查看容器进程在宿主机的 PID](https://www.cnblogs.com/xy14/p/12002816.html)
- [如何根据PID查找进程是在哪个容器实例运行的](https://blog.csdn.net/joker_zhou/article/details/124091728)
- [如何制作Docker镜像](https://zhuanlan.zhihu.com/p/122380334)
- [如何在一个Docker中同时运行多个程序进程?](https://cloud.tencent.com/developer/article/1683445)


