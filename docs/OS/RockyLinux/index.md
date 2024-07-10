# Rocky Linux docs

Rocky Linux学习笔记:



根据 [CentOS 官方公告](https://blog.centos.org/2023/04/end-dates-are-coming-for-centos-stream-8-and-centos-linux-7/)，CentOS 7 已经于 2024 年 6 月 30 日结束支持，其软件仓库也相应被上游移除。 

Rocky Linux可以作为CentOS的替换方案。今日安装一下这个新系统，试用一下：

```sh
[root@rockylinux ~]# cat /etc/rocky-release
Rocky Linux release 9.4 (Blue Onyx)
[root@rockylinux ~]# cat /etc/os-release
NAME="Rocky Linux"
VERSION="9.4 (Blue Onyx)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.4"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Rocky Linux 9.4 (Blue Onyx)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:9::baseos"
HOME_URL="https://rockylinux.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2032-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-9"
ROCKY_SUPPORT_PRODUCT_VERSION="9.4"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.4"
[root@rockylinux ~]# uname -a
Linux rockylinux 5.14.0-427.13.1.el9_4.x86_64 #1 SMP PREEMPT_DYNAMIC Wed May 1 19:11:28 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
[root@rockylinux ~]#
```

