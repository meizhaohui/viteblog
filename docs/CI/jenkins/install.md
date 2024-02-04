# Jenkins安装与基本配置

[[toc]]



参考：

- [install jenkins](https://www.jenkins.io/doc/book/installing/linux/)
- [Jenkins Redhat Packages](https://pkg.jenkins.io/redhat/)

操作系统和基础软件说明：

```sh
$ cat /etc/centos-release
CentOS Linux release 7.6.1810 (Core)
$ java -version
openjdk version "1.8.0_232"
OpenJDK Runtime Environment (build 1.8.0_232-b09)
OpenJDK 64-Bit Server VM (build 25.232-b09, mixed mode)
$
```

## 1. 安装

查看yum源中是否有jenkins包：

```sh
# 搜索jenkins包
$ sudo yum search jenkins
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Repository google-chrome is listed more than once in the configuration
Determining fastest mirrors
 * webtatic: uk.repo.webtatic.com
================================================= N/S matched: jenkins =================================================
jenkins.noarch : Jenkins Automation Server
python2-jenkins.noarch : Python bindings for the remote Jenkins API
python2-jenkins-job-builder.noarch : Manage Jenkins jobs with YAML
python36-jenkins.noarch : Python bindings for the remote Jenkins API
cinch.noarch : A tool for provisioning Jenkins components for CI
perl-Digest-JHash.x86_64 : Perl extension for 32 bit Jenkins Hashing Algorithm
spooky-c.x86_64 : C port of Bob Jenkins' spooky hash

  Name and summary matches only, use "search all" for everything.
  

# 可以看到，能够搜索到jenkins包，此时查看jenkinq包信息
$ sudo yum info jenkins
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Repository google-chrome is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * webtatic: uk.repo.webtatic.com
Installed Packages
Name        : jenkins
Arch        : noarch
Version     : 2.291
Release     : 1.1
Size        : 71 M
Repo        : installed
From repo   : jenkins
Summary     : Jenkins Automation Server
URL         : http://jenkins.io/
License     : MIT/X License, GPL/CDDL, ASL2
Description : Jenkins is an open source automation server which enables developers around the world to reliably automate
            :  their development lifecycle processes of all kinds, including build, document, test, package, stage,
            : deployment, static analysis and many more.
            :
            : Jenkins is being widely used in areas of Continous Integration, Continuous Delivery, DevOps, and other
            : areas. And it is not only about software, the same automation techniques can be applied in other areas
            : like Hardware Engineering, Embedded Systems, BioTech, etc.
            :
            : For information see https://jenkins.io
            :
            :
            : Authors:
            : --------
            :     Kohsuke Kawaguchi <kk@kohsuke.org>

$
```

安装：

```sh
$ sudo yum install jenkins
```

查看jenkins版本信息：

```sh
$ rpm -qa|grep jenkins
jenkins-2.291-1.1.noarch
```



## 2. 启动Jenkins

```sh
# 设置开机启动
$ sudo systemctl enable jenkins
jenkins.service is not a native service, redirecting to /sbin/chkconfig.
Executing /sbin/chkconfig jenkins on

# 启动jenkins服务
$ sudo systemctl start jenkins

# 查看jenkins服务状态
$ sudo systemctl status jenkins
● jenkins.service - LSB: Jenkins Automation Server
   Loaded: loaded (/etc/rc.d/init.d/jenkins; bad; vendor preset: disabled)
   Active: active (running) since Sun 2022-03-27 20:02:59 CST; 5s ago
     Docs: man:systemd-sysv-generator(8)
  Process: 29710 ExecStart=/etc/rc.d/init.d/jenkins start (code=exited, status=0/SUCCESS)
    Tasks: 22
   Memory: 286.7M
   CGroup: /system.slice/jenkins.service
           └─29732 /etc/alternatives/java -Dcom.sun.akuma.Daemon=daemonized -Djava.awt.headless=true -DJENKINS_HOME=/...

Mar 27 20:02:58 hellogitlab.com systemd[1]: Starting LSB: Jenkins Automation Server...
Mar 27 20:02:58 hellogitlab.com runuser[29715]: pam_unix(runuser:session): session opened for user jenkins by (uid=0)
Mar 27 20:02:59 hellogitlab.com jenkins[29710]: Starting Jenkins [  OK  ]
Mar 27 20:02:59 hellogitlab.com systemd[1]: Started LSB: Jenkins Automation Server.
$
```

查看jenkins进程和端口号：

```sh
$ ps -ef|grep jenkins
jenkins  29732     1  6 20:02 ?        00:00:37 /etc/alternatives/java -Dcom.sun.akuma.Daemon=daemonized -Djava.awt.headless=true -DJENKINS_HOME=/var/lib/jenkins -jar /usr/lib/jenkins/jenkins.war --logfile=/var/log/jenkins/jenkins.log --webroot=/var/cache/jenkins/war --daemon --httpPort=8080 --debug=5 --handlerCountMax=100 --handlerCountMaxIdle=20
meizhao+ 31636 27398  0 20:12 pts/0    00:00:00 grep --color=auto jenkins
$ netstat -tunlp|grep jenkins
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
$ sudo netstat -tunlp|grep java
tcp6       0      0 :::8080                 :::*                    LISTEN      29732/java
$
```

可以看到，jenkins监听的是`8080`端口。



## 3. 防火墙设置

防火墙放行`8080`端口。

```sh
# 放行8080端口号
$ sudo firewall-cmd --permanent --zone=public --add-port="8080/tcp"
success

# 重新加载防火墙配置
$ sudo firewall-cmd --reload
success

# 检查8080端口号是否放行
$ sudo firewall-cmd --zone=public --query-port=8080/tcp
yes
```

此时，就可以在浏览器中打开jenkins了，如果你没有域名，可以用主机http://IP:8080 方式访问Jenkins。



## 4. 基本配置

### 4.1 解锁 Jenkins

![](/img/20220327203005.png)

按提示，查看`/var/lib/jenkins/secrets/initialAdminPassword`获取管理员密码：

```sh
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
09b50e899c754312befbf984ab9096c8
```

将查看到的密码填写到页面中，并点击“继续”按钮。

### 4.2 自定义Jenkins

![](/img/20220327203246.png)

此时点击“安装推荐的插件”，此时会自动安装推荐的插件：

![](/img/20220327203349.png)

等待安装完成。

### 4.3 创建管理员账号

推荐的插件安装完成后，可以创建一个管理员账号，如创建的管理员账号"meizhaohui"，并设置密码。

![](/img/20220327203954.png)

点击“保存并完成”。

### 4.4 实例配置

此时会自动生成Jenkins对应的URL路径：

![](/img/20220327204125.png)

点击“保存并完成”。然后在弹出的Jenkins已就绪页面，点击“开始使用Jenkins”即可。

这样，Jenkins就安装完成并可以正常使用了。



## 5. 更新Jenkins

在jenkins管理页面，可以看到，存在漏洞风险：

![](/img/20220327205127.png)

我们直接按页面提示，下载最新的`jenkins.war`包(2.340)，只需要把下载的jenkins.war 替换原来的jenkins.war 就可以了。

原来的jenkins.war包在哪里，我们可以像如下方式查看：

```sh
$ rpm -ql jenkins
/etc/init.d/jenkins
/etc/logrotate.d/jenkins
/etc/sysconfig/jenkins
/usr/lib/jenkins
/usr/lib/jenkins/jenkins.war
/usr/sbin/rcjenkins
/var/cache/jenkins
/var/lib/jenkins
/var/log/jenkins
$
```

可以看到，`/usr/lib/jenkins/jenkins.war`是其存放路径。

我们将下载下来的`jenkins.war`上传到服务器上，并替换原来的war包。

```sh
# 查看原来的war包
$ ll /usr/lib/jenkins/
total 72564
-rw-r--r-- 1 root root 74305520 May  4  2021 jenkins.war

# 备份
$ sudo mv /usr/lib/jenkins/jenkins.war ~/jenkins.2.291.war

# 再次查看一下，是否移走
$ ll /usr/lib/jenkins/
total 0

# 复制war包
$ sudo cp jenkins.war /usr/lib/jenkins/

# 再次查看war包，发现权限和之前不一样，应修改一下权限
$ ll /usr/lib/jenkins/
total 89112
-rw------- 1 root root 91245352 Mar 27 20:59 jenkins.war

# 修改权限，更改为644
$ sudo chmod 644 /usr/lib/jenkins/jenkins.war 
$ ll /usr/lib/jenkins/jenkins.war 
-rw-r--r-- 1 root root 91245352 Mar 27 20:59 /usr/lib/jenkins/jenkins.war

# 重命名最新的war包
$ mv jenkins.war jenkins.2.340.war

# 查看备份的war包
$ ll jenkins*
-rw-r--r-- 1 root       root       74305520 May  4  2021 jenkins.2.291.war
-rw------- 1 meizhaohui meizhaohui 91245352 Mar 27 20:57 jenkins.2.340.war
$ 
```

重启jenkins服务：

```sh
$ sudo systemctl restart jenkins
```

发现启动失败。

先卸载旧版本的jenkins。

```sh
$ yum remove jenkins -y 
```



我们重新使用`yum`安装jenkins。

```sh
# 安装jenkins源
$ sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat/jenkins.repo

# 安装key
$ sudo rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key
```

再重新安装jenkins。

```sh
$ sudo yum install jenkins -y
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Repository google-chrome is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * webtatic: uk.repo.webtatic.com
Resolving Dependencies
--> Running transaction check
---> Package jenkins.noarch 0:2.340-1.1 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==================================================================================================================
 Package                   Arch                     Version                       Repository                 Size
==================================================================================================================
Installing:
 jenkins                   noarch                   2.340-1.1                     jenkins                    87 M

Transaction Summary
==================================================================================================================
Install  1 Package

Total size: 87 M
Installed size: 87 M
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : jenkins-2.340-1.1.noarch                                                                       1/1 
  Verifying  : jenkins-2.340-1.1.noarch                                                                       1/1 

Installed:
  jenkins.noarch 0:2.340-1.1                                                                                      

Complete!
$ 
```

然后启动jenkins:

```sh
# 重新加载配置文件
$ sudo systemctl daemon-reload

# 启动Jenkins服务
$ sudo systemctl start jenkins

# 设置开机启动
$ sudo systemctl enable jenkins
Created symlink from /etc/systemd/system/multi-user.target.wants/jenkins.service to /usr/lib/systemd/system/jenkins.service.

# 查看jenkins服务状态
$ sudo systemctl status jenkins
● jenkins.service - Jenkins Continuous Integration Server
   Loaded: loaded (/usr/lib/systemd/system/jenkins.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2022-03-28 00:10:17 CST; 33s ago
   CGroup: /system.slice/jenkins.service
           ├─15741 /bin/sh /etc/rc.d/init.d/jenkins start
           ├─15747 runuser -s /bin/bash jenkins -c ulimit -S -c 0 >/dev/null 2>&1 ; /etc/alternatives/java -Dja...
           ├─15748 bash -c ulimit -S -c 0 >/dev/null 2>&1 ; /etc/alternatives/java -Djava.awt.headless=true -DJ...
           └─15749 /etc/alternatives/java -Djava.awt.headless=true -DJENKINS_HOME=/var/lib/jenkins -jar /usr/sh...

Mar 28 00:10:16 hellogitlab.com systemd[1]: Starting LSB: Jenkins Automation Server...
Mar 28 00:10:16 hellogitlab.com runuser[15747]: pam_unix(runuser:session): session opened for user jenkins ...d=0)
Mar 28 00:10:17 hellogitlab.com systemd[1]: Started LSB: Jenkins Automation Server.
Mar 28 00:10:17 hellogitlab.com jenkins[15738]: Starting Jenkins [  OK  ]
Hint: Some lines were ellipsized, use -l to show in full.
$ 
```

启动后，然后浏览器中打开jenkins服务，并进行配置即可。

![](/img/20220328002204.png)

在Jenkins页面右下角可以看到Jenkins已经更新到`Jenkins 2.340`版本了。说明更新成功。
