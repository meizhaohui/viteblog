# zabbix日志监控Permission denied权限异常处理

## 1. 问题描述
配置了zabbix监控日志`/var/log/messages`时，页面显示监控项是“Not supported”不支持的。

![](/img/Snipaste_2023-03-15_22-13-50.png)
登陆到zabbix-agent节点，查看节点日志信息，发现日志报以下异常：
```sh
[root@zabbix-agent ~]# tail -f /srv/zabbix/logs/zabbix_agentd.log
  1687:20230315:202950.434 TLS support:            NO
  1687:20230315:202950.434 **************************
  1687:20230315:202950.434 using configuration file: /srv/zabbix/etc/zabbix_agentd.conf
  1687:20230315:202950.434 agent #0 started [main process]
  1688:20230315:202950.435 agent #1 started [collector]
  1691:20230315:202950.435 agent #4 started [listener #3]
  1689:20230315:202950.435 agent #2 started [listener #1]
  1690:20230315:202950.435 agent #3 started [listener #2]
  1692:20230315:202950.436 agent #5 started [active checks #1]
  1692:20230315:220454.113 active check "log[/var/log/messages,"ERROR",,,skip,]" is not supported: Cannot open file "/var/log/messages": [13] Permission denied
```

即可知zabbix无`/var/log/messages`文件的权限。

查看权限信息：
```sh
[root@zabbix-agent ~]# ls -lah /var/log/messages
-rw------- 1 root root 367K Mar 15 22:16 /var/log/messages
[root@zabbix-agent ~]#
```

可以看到只用`root`用户有读写权限，而我们zabbix agent程序是使用的zabbix用户运行的：
```sh
[root@zabbix-agent ~]# ps -ef|grep zabbix_agent
zabbix    1687     1  0 20:58 ?        00:00:00 /srv/zabbix/sbin/zabbix_agentd
zabbix    1688  1687  0 20:58 ?        00:00:01 /srv/zabbix/sbin/zabbix_agentd: collector [idle 1 sec]
zabbix    1689  1687  0 20:58 ?        00:00:01 /srv/zabbix/sbin/zabbix_agentd: listener #1 [waiting for connection]
zabbix    1690  1687  0 20:58 ?        00:00:01 /srv/zabbix/sbin/zabbix_agentd: listener #2 [waiting for connection]
zabbix    1691  1687  0 20:58 ?        00:00:01 /srv/zabbix/sbin/zabbix_agentd: listener #3 [waiting for connection]
zabbix    1692  1687  0 20:58 ?        00:00:01 /srv/zabbix/sbin/zabbix_agentd: active checks #1 [idle 1 sec]
root      3015  2070  0 22:17 pts/0    00:00:00 grep --color=auto zabbix_agent
[root@zabbix-agent ~]#
```

## 2. 配置权限

有以下方案修改权限：

- 1. 直接修改文件拥有者是`zabbix`，所属组是`root`。 -- 不推荐
- 2. 修改agent配置文件`AllowRoot=1`，重启agent，以`root`用户启动zabbix agent服务。 -- 不推荐
- 3. 使用`setfacl`给日志文件加上读权限。-- 推荐

### 2.1 修改日志文件拥有者

直接使用`chown`修改文件拥有者信息：
```sh
[root@zabbix-agent ~]# chown zabbix.root /var/log/messages
[root@zabbix-agent ~]# ll /var/log/messages
-rw------- 1 zabbix root 376149 Mar 15 22:30 /var/log/messages
[root@zabbix-agent ~]#
```

此时查看文件权限：
```sh
[root@zabbix-agent ~]# getfacl -p /var/log/messages
# file: /var/log/messages
# owner: zabbix
# group: root
user::rw-
group::---
other::---

[root@zabbix-agent ~]#
```
可以看到`zabbix`已经成了文件的`owner`拥有者了，说明有权限了。

过了一会儿后，在页面上可以看到监控项变成`Enable`启用状态了。
![](/img/Snipaste_2023-03-15_22-33-54.png)

测试监控报警，向日志文件中写入数据：

```
[root@zabbix-agent ~]# echo "this is a test ERROR 20230315" >> /var/log/messages
You have new mail in /var/spool/mail/root
[root@zabbix-agent ~]# tail -n 1 /var/log/messages
this is a test ERROR 20230315
[root@zabbix-agent ~]#
```

过一会儿，zabbix监控界面上就弹出监控异常：

![](/img/Snipaste_2023-03-15_22-46-50.png)
说明我们的日志监控起作用了！！


然后，我们日志有轮转机制：
```sh
[root@zabbix-agent ~]# grep 'messages' /etc/logrotate.d/syslog
/var/log/messages
[root@zabbix-agent ~]# ll /var/log/messages*
-rw-------  1 zabbix root     71 Mar 15 22:58 /var/log/messages
-rw-------. 1 root   root 745869 Nov 13 22:06 /var/log/messages-20221113
-rw-------  1 root   root 419972 Mar 11 20:18 /var/log/messages-20230311
-rw-------  1 root   root   6296 Mar 12 08:35 /var/log/messages-20230312

# 强制轮转
[root@zabbix-agent ~]# logrotate -f /etc/logrotate.d/syslog
[root@zabbix-agent ~]# ll /var/log/messages*
-rw-------. 1 root root 745869 Nov 13 22:06 /var/log/messages-20221113
-rw-------  1 root root 419972 Mar 11 20:18 /var/log/messages-20230311
-rw-------  1 root root   6296 Mar 12 08:35 /var/log/messages-20230312
```

强制轮转后，发现日志文件没有了！！！

重启日志服务，发现日志文件又有了：
```sh
[root@zabbix-agent ~]# systemctl restart rsyslog
You have new mail in /var/spool/mail/root
[root@zabbix-agent ~]# ll /var/log/messages*
-rw-------  1 root root    805 Mar 15 23:03 /var/log/messages
-rw-------. 1 root root 745869 Nov 13 22:06 /var/log/messages-20221113
-rw-------  1 root root 419972 Mar 11 20:18 /var/log/messages-20230311
-rw-------  1 root root   6296 Mar 12 08:35 /var/log/messages-20230312
[root@zabbix-agent ~]# cat /var/log/messages
Mar 15 23:00:01 zabbix-agent systemd: Started Session 65 of user root.
Mar 15 23:01:01 zabbix-agent systemd: Started Session 66 of user root.
Mar 15 23:02:01 zabbix-agent systemd: Started Session 67 of user root.
Mar 15 23:03:14 zabbix-agent systemd: Stopping System Logging Service...
Mar 15 23:03:14 zabbix-agent rsyslogd: [origin software="rsyslogd" swVersion="8.24.0-38.el7" x-pid="1031" x-info="http://www.rsyslog.com"] exiting on signal 15.
Mar 15 23:03:14 zabbix-agent systemd: Stopped System Logging Service.
Mar 15 23:03:14 zabbix-agent systemd: Starting System Logging Service...
Mar 15 23:03:14 zabbix-agent rsyslogd: [origin software="rsyslogd" swVersion="8.24.0-38.el7" x-pid="3810" x-info="http://www.rsyslog.com"] start
Mar 15 23:03:14 zabbix-agent systemd: Started System Logging Service.
[root@zabbix-agent ~]#
```

说明日志轮转后，日志文件`/var/log/messages`的权限发生了变化，`zabbix`用户又失去了读权限。说明此种方案存在问题，不能根本上解决zabbix不能读日志的问题。


### 2.2 以root用户启动zabbix agent服务

首先看一下配置文件：
```sh
[root@zabbix-agent ~]# grep -i -C2  root /srv/zabbix/etc/zabbix_agentd.conf
# Timeout=3

### Option: AllowRoot
#	Allow the agent to run as 'root'. If disabled and the agent is started by 'root', the agent
#	will try to switch to the user specified by the User configuration option instead.
#	Has no effect if started under a regular user.
--
# Mandatory: no
# Default:
# AllowRoot=0

### Option: User
#	Drop privileges to a specific, existing user on the system.
#	Only has effect if run as 'root' and AllowRoot is disabled.
#
# Mandatory: no
[root@zabbix-agent ~]#
```
默认情况下，配置的是`AllowRoot=0`不允许`root`用户启动。

在zabbix最佳实践说明 [https://www.zabbix.com/documentation/current/en/manual/installation/requirements/best_practices](https://www.zabbix.com/documentation/current/en/manual/installation/requirements/best_practices) 中：
> Overview
> This section contains best practices that should be observed in order to set up Zabbix in a secure way.
>
> The practices contained here are not required for the functioning of Zabbix. They are recommended for better security of the system.
Access control 
> Principle of least privilege
> 
> The principle of least privilege should be used at all times for Zabbix. This principle means that user accounts (in Zabbix frontend) or process user (for Zabbix server/proxy or agent) have only those privileges that are essential to perform intended functions. In other words, user accounts at all times should run with as few privileges as possible.
>
> Giving extra permissions to 'zabbix' user will allow it to access configuration files and execute operations that can compromise the overall security of the infrastructure.
>
> When implementing the least privilege principle for user accounts, Zabbix frontend user types should be taken into account. It is important to understand that while a "Admin" user type has less privileges than "Super Admin" user type, it has administrative permissions that allow managing configuration and execute custom scripts.
> 
> Some information is available even for non-privileged users. For example, while Alerts → Scripts is not available for non-Super Admins, scripts themselves are available for retrieval by using Zabbix API. Limiting script permissions and not adding sensitive information (like access credentials, etc) should be used to avoid exposure of sensitive information available in global scripts.
> Secure user for Zabbix agent
> 
> In the default configuration, Zabbix server and Zabbix agent processes share one 'zabbix' user. If you wish to make sure that the agent cannot access sensitive details in server configuration (e.g. database login information), the agent should be run as a different user:
>
> Create a secure user
> 
> Specify this user in the agent configuration file ('User' parameter)
> 
> Restart the agent with administrator privileges. Privileges will be dropped to the specified user.

通过zabbix的最佳实践：
- 最低特权原则。Zabbix应始终使用最低特权原则。这一原则意味着用户帐户（在Zabbix前端）或进程用户（对于Zabbix服务器/代理或代理）仅具有执行预期功能所必需的特权。换句话说，用户帐户在任何时候都应该以尽可能少的权限运行。
- 向“zabbix”用户授予额外权限将允许其访问配置文件并执行可能危及基础设施整体安全的操作。

以下是关于zabbix安全的一些说明：
> 如果你的Zabbix的Admin口令太弱或者使用了默认口令（Admin/zabbix），而被黑客破解了口令的话，Zabbix服务器在黑客面前就已经毫无抵抗力了。黑客可以创建`system.run[command,<mode>]`监控项执行命令，甚至获取服务器shell，获取root权限。
> 
> 先介绍下`system.run[command,<mode>]`，这个监控项是agent自带的，使zabbix server可以远程在agent的机器上执行任意命令。方法有二：一是建立监控项，二是通过zabbix_get命令直接远程调用。命令执行权限限制于zabbix agent的启动用户，如果你为了方便，把agent的启动用户设置为root的话（`AllowRoot=1`），这是非常危险的。
> 
> 措施：
> 
> 1、很重要的一点，zabbix的登录口令一定要复杂，不要用默认口令或弱口令。
> 
> 2、zabbix的server和agent都不要以root启动，不要设置`AllowRoot=1`。
> 
> 3、禁止agent执行system.run，不要设置`EnableRemoteCommands=1`。
> 
> 4、经常打安全补丁，如果系统内核版本过低有漏洞的话，即使在zabbix用户下照样能获取root权限。
> 

因此，为了系统安全，我们不以`root`账号启动zabbix agent服务。

### 2.3 setfacl设置文件权限

```sh
[root@zabbix-agent ~]# ll /var/log/messages
-rw------- 1 root root 1444 Mar 15 23:28 /var/log/messages
You have new mail in /var/spool/mail/root
[root@zabbix-agent ~]# getfacl -p /var/log/messages
# file: /var/log/messages
# owner: root
# group: root
user::rw-
group::---
other::---

[root@zabbix-agent ~]# setfacl -m u:zabbix:r /var/log/messages
[root@zabbix-agent ~]# getfacl -p /var/log/messages
# file: /var/log/messages
# owner: root
# group: root
user::rw-
user:zabbix:r--
group::---
mask::r--
other::---

[root@zabbix-agent ~]#
```

此时已经有权限了。强制轮转：
```sh
[root@zabbix-agent ~]# ll /var/log/messages*
-rw-r-----+ 1 root root   1728 Mar 15 23:36 /var/log/messages
-rw-------. 1 root root 745869 Nov 13 22:06 /var/log/messages-20221113
-rw-------  1 root root 419972 Mar 11 20:18 /var/log/messages-20230311
-rw-------  1 root root   6296 Mar 12 08:35 /var/log/messages-20230312

# 强制轮转
[root@zabbix-agent ~]# logrotate -f /etc/logrotate.d/syslog
[root@zabbix-agent ~]# ll /var/log/messages*
-rw-------. 1 root root 745869 Nov 13 22:06 /var/log/messages-20221113
-rw-------  1 root root 419972 Mar 11 20:18 /var/log/messages-20230311
-rw-------  1 root root   6296 Mar 12 08:35 /var/log/messages-20230312

# 重启服务
[root@zabbix-agent ~]# systemctl restart rsyslog
[root@zabbix-agent ~]# ll /var/log/messages*
-rw-------  1 root root    592 Mar 15 23:37 /var/log/messages
-rw-------. 1 root root 745869 Nov 13 22:06 /var/log/messages-20221113
-rw-------  1 root root 419972 Mar 11 20:18 /var/log/messages-20230311
-rw-------  1 root root   6296 Mar 12 08:35 /var/log/messages-20230312
```

再次查看文件权限：
```sh
[root@zabbix-agent ~]# getfacl -p /var/log/messages
# file: /var/log/messages
# owner: root
# group: root
user::rw-
group::---
other::---

[root@zabbix-agent ~]#
```

可以看到轮转后文件权限没有了。

修改一下轮转文件配置文件：

```sh
[root@zabbix-agent ~]# cat /etc/logrotate.d/syslog
/var/log/cron
/var/log/maillog
/var/log/messages
/var/log/secure
/var/log/spooler
{
    missingok
    sharedscripts
    postrotate
        /bin/kill -HUP `cat /var/run/syslogd.pid 2> /dev/null` 2> /dev/null || true
        touch /var/log/messages && chmod 600 /var/log/messages
        /usr/bin/setfacl -m u:zabbix:r /var/log/messages
    endscript
}
[root@zabbix-agent ~]#
```

增加第11、12行内容，轮转后自动创建文件并设置权限。

此时轮转后日志权限仍然存在：
```sh
[root@zabbix-agent ~]# logrotate -f /etc/logrotate.d/syslog
[root@zabbix-agent ~]# ll /var/log/messages*
-rw-r-----+ 1 root root      0 Mar 15 23:58 /var/log/messages
-rw-------. 1 root root 745869 Nov 13 22:06 /var/log/messages-20221113
-rw-------  1 root root 419972 Mar 11 20:18 /var/log/messages-20230311
-rw-------  1 root root   6296 Mar 12 08:35 /var/log/messages-20230312
[root@zabbix-agent ~]# getfacl -p /var/log/messages
# file: /var/log/messages
# owner: root
# group: root
user::rw-
user:zabbix:r--
group::---
mask::r--
other::---

[root@zabbix-agent ~]#
```









