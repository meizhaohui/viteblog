# Ubuntu UFW防火墙设置

[[toc]]

### 安装

```sh
root@4144e8c22fff:/# apt-get install ufw -y
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  file iptables libexpat1 libip4tc2 libip6tc2 libmagic-mgc libmagic1 libmnl0 libmpdec2 libnetfilter-conntrack3
  libnfnetlink0 libnftnl11 libpython3-stdlib libpython3.8-minimal libpython3.8-stdlib libreadline8 libsqlite3-0
  libssl1.1 libxtables12 mime-support netbase python3 python3-minimal python3.8 python3.8-minimal readline-common ucf
  xz-utils
Suggested packages:
  firewalld kmod nftables python3-doc python3-tk python3-venv python3.8-venv python3.8-doc binutils binfmt-support
  readline-doc rsyslog
The following NEW packages will be installed:
  file iptables libexpat1 libip4tc2 libip6tc2 libmagic-mgc libmagic1 libmnl0 libmpdec2 libnetfilter-conntrack3
  libnfnetlink0 libnftnl11 libpython3-stdlib libpython3.8-minimal libpython3.8-stdlib libreadline8 libsqlite3-0
  libssl1.1 libxtables12 mime-support netbase python3 python3-minimal python3.8 python3.8-minimal readline-common ucf
  ufw xz-utils
0 upgraded, 29 newly installed, 0 to remove and 1 not upgraded.
...
...
...省略
```

### 查看版本和帮助信息

```sh
root@4144e8c22fff:/# ufw version
ufw 0.36
Copyright 2008-2015 Canonical Ltd.
root@4144e8c22fff:/# ufw --help

Usage: ufw COMMAND

Commands:
 enable                          enables the firewall
 disable                         disables the firewall
 default ARG                     set default policy
 logging LEVEL                   set logging to LEVEL
 allow ARGS                      add allow rule
 deny ARGS                       add deny rule
 reject ARGS                     add reject rule
 limit ARGS                      add limit rule
 delete RULE|NUM                 delete RULE
 insert NUM RULE                 insert RULE at NUM
 route RULE                      add route RULE
 route delete RULE|NUM           delete route RULE
 route insert NUM RULE           insert route RULE at NUM
 reload                          reload firewall
 reset                           reset firewall
 status                          show firewall status
 status numbered                 show firewall status as numbered list of RULES
 status verbose                  show verbose firewall status
 show ARG                        show firewall report
 version                         display version information

Application profile commands:
 app list                        list application profiles
 app info PROFILE                show information on PROFILE
 app update PROFILE              update PROFILE
 app default ARG                 set default application policy
```

### 启用防火墙

```sh
root@4144e8c22fff:/# ufw enable
Firewall is active and enabled on system startup
```

### 查看防火墙状态

```sh
root@4144e8c22fff:/# ufw status
Status: active
```

### 关闭一切外部对本机的访问

```sh
root@4144e8c22fff:/# ufw default deny 
Default incoming policy changed to 'deny'
(be sure to update your rules accordingly)
```

### 重启防火墙

```sh
root@4144e8c22fff:/# ufw reload
Status: active
```


### 防火墙放行80端口

```sh
root@4144e8c22fff:/# ufw allow 80/tcp
Status: active
```

### 查看端口放行状态

```sh
root@4144e8c22fff:/# ufw status
Status: active

To                         Action      From
--                         ------      ----
80/tcp                     ALLOW       Anywhere
80/tcp (v6)                ALLOW       Anywhere (v6)
```


### 防火墙禁止80端口

```sh
root@4144e8c22fff:/# ufw delete allow 80/tcp
Rule deleted
Rule deleted (v6)
root@4144e8c22fff:/# ufw status
Status: active
```

### 允许IP访问所有的本机端口

允许192.168.12.1访问本机上面的所有端口：

```sh
root@4144e8c22fff:/# ufw allow from 192.168.12.1
Rule added
root@4144e8c22fff:/# ufw status
Status: active

To                         Action      From
--                         ------      ----
Anywhere                   ALLOW       192.168.12.1
```


参考：

- [UFW防火墙简单设置](https://wiki.ubuntu.org.cn/UFW%E9%98%B2%E7%81%AB%E5%A2%99%E7%AE%80%E5%8D%95%E8%AE%BE%E7%BD%AE)

