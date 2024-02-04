# NTP时间同步

- NTP是用于同步网络中计算机时间的协议，全称为网络时间协议（Network Time Protocol）。

- 时区和时间一致性对于服务器非常重要，有时会直接影响到任务执行的结果。例如，您在更新数据库或者分析日志时，时间顺序对结果有很大影响。为避免在服务器上运行业务时出现逻辑混乱和网络请求错误等问题，您需要统一相关服务器的时区设置。另外，您还可以通过NTP服务同步各网络中服务器的本地时间。 

## 1. NTP服务器列表

推荐您使用域名，而非IP地址，以免出现IP地址变动影响使用的情况！

| 序号 | 服务器名称      | 域名           |
|------|-----------------|:---------------|
| 1    | 阿里云NTP服务器 | ntp.aliyun.com |
| 2    | 中国            | cn.ntp.org.cn  |
| 3    | 中国教育网      | edu.ntp.org.cn |
| 4    | 中国香港        | hk.ntp.org.cn  |
| 5    | 中国台湾        | tw.ntp.org.cn  |
| 6    | 日本            | jp.ntp.org.cn  |
| 7    | 韩国            | kr.ntp.org.cn  |
| 8    | 新加坡          | sgp.ntp.org.cn |
| 9    | 美国            | us.ntp.org.cn  |
| 10   | 德国            | de.ntp.org.cn  |
| 11   | 印度尼西亚      | ina.ntp.org.cn |


## 2. 配置定时同步

我们使用阿里云NTP服务器。

- 定时任务配置文件`/var/spool/cron/root`。

使用`crontab -e`命令打开定时任务编辑器，输入以下内容：

```sh
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

# time sync
*/2 * * * * ntpdate ntp.aliyun.com
```

即每两分钟同步一次时间。


查看定时任务信息：
```sh
[root@master ~]# crontab -l
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

# sync time
*/2 * * * * ntpdate ntp.aliyun.com

[root@master ~]#
```