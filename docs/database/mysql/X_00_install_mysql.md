# CentOS7安装mysql

[[toc]]

## 1. 概述  

本文档记录在CentOS7系统上面安装mariadb，然后启动mysql。

MariaDB数据库管理系统是MySQL的一个分支。

> 当 MariaDB Server 的前身 MySQL 于 2009 年被 Oracle 收购时，MySQL 创始人 Michael “Monty” Widenius 出于对 Oracle 管理权的担忧而分叉了该项目，并将新项目命名为 MariaDB。 MySQL 以他的第一个女儿 My 命名，而 MariaDB 则以他的第二个女儿 Maria 命名。 

操作系统版本：

```sh
[root@ansible ~]# cat /etc/centos-release
CentOS Linux release 7.9.2009 (Core)
```



## 2. yum安装mariadb-server

先搜索一下yum源中有没有mariadb-server软件包:

```sh
[root@ansible ~]# yum search mariadb-server
Loaded plugins: fastestmirror
Repodata is over 2 weeks old. Install yum-cron? Or run: yum makecache fast
Loading mirror speeds from cached hostfile
 * base: mirrors.aliyun.com
 * extras: mirrors.aliyun.com
 * updates: mirrors.aliyun.com
========================================================================================================================= N/S matched: mariadb-server =========================================================================================================================
mariadb-server.x86_64 : The MariaDB server and related files

  Name and summary matches only, use "search all" for everything.
[root@ansible-node1 ~]# yum info mariadb-server
Loaded plugins: fastestmirror
Repodata is over 2 weeks old. Install yum-cron? Or run: yum makecache fast
Loading mirror speeds from cached hostfile
 * base: mirrors.aliyun.com
 * extras: mirrors.aliyun.com
 * updates: mirrors.aliyun.com
Available Packages
Name        : mariadb-server
Arch        : x86_64
Epoch       : 1
Version     : 5.5.68
Release     : 1.el7
Size        : 11 M
Repo        : base/7/x86_64
Summary     : The MariaDB server and related files
URL         : http://mariadb.org
License     : GPLv2 with exceptions and LGPLv2 and BSD
Description : MariaDB is a multi-user, multi-threaded SQL database server. It is a
            : client/server implementation consisting of a server daemon (mysqld)
            : and many different client programs and libraries. This package contains
            : the MariaDB server and some accompanying files and directories.
            : MariaDB is a community developed branch of MySQL.

[root@ansible ~]#
```

可以看到，远程仓库中有mariadb-server软件包。

就可以直接安装。

```sh
[root@ansible ~]# yum install mariadb-server
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package mariadb-server.x86_64 1:5.5.68-1.el7 will be installed
--> Processing Dependency: mariadb(x86-64) = 1:5.5.68-1.el7 for package: 1:mariadb-server-5.5.68-1.el7.x86_64
--> Processing Dependency: perl-DBI for package: 1:mariadb-server-5.5.68-1.el7.x86_64
--> Processing Dependency: perl-DBD-MySQL for package: 1:mariadb-server-5.5.68-1.el7.x86_64
--> Processing Dependency: perl(Data::Dumper) for package: 1:mariadb-server-5.5.68-1.el7.x86_64
--> Processing Dependency: perl(DBI) for package: 1:mariadb-server-5.5.68-1.el7.x86_64
--> Running transaction check
---> Package mariadb.x86_64 1:5.5.68-1.el7 will be installed
---> Package perl-DBD-MySQL.x86_64 0:4.023-6.el7 will be installed
---> Package perl-DBI.x86_64 0:1.627-4.el7 will be installed
--> Processing Dependency: perl(RPC::PlServer) >= 0.2001 for package: perl-DBI-1.627-4.el7.x86_64
--> Processing Dependency: perl(RPC::PlClient) >= 0.2000 for package: perl-DBI-1.627-4.el7.x86_64
---> Package perl-Data-Dumper.x86_64 0:2.145-3.el7 will be installed
--> Running transaction check
---> Package perl-PlRPC.noarch 0:0.2020-14.el7 will be installed
--> Processing Dependency: perl(Net::Daemon) >= 0.13 for package: perl-PlRPC-0.2020-14.el7.noarch
--> Processing Dependency: perl(Net::Daemon::Test) for package: perl-PlRPC-0.2020-14.el7.noarch
--> Processing Dependency: perl(Net::Daemon::Log) for package: perl-PlRPC-0.2020-14.el7.noarch
--> Processing Dependency: perl(Compress::Zlib) for package: perl-PlRPC-0.2020-14.el7.noarch
--> Running transaction check
---> Package perl-IO-Compress.noarch 0:2.061-2.el7 will be installed
--> Processing Dependency: perl(Compress::Raw::Zlib) >= 2.061 for package: perl-IO-Compress-2.061-2.el7.noarch
--> Processing Dependency: perl(Compress::Raw::Bzip2) >= 2.061 for package: perl-IO-Compress-2.061-2.el7.noarch
---> Package perl-Net-Daemon.noarch 0:0.48-5.el7 will be installed
--> Running transaction check
---> Package perl-Compress-Raw-Bzip2.x86_64 0:2.061-3.el7 will be installed
---> Package perl-Compress-Raw-Zlib.x86_64 1:2.061-4.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

===============================================================================================================================================================================================================================================================================
 Package                                                                      Arch                                                        Version                                                              Repository                                                 Size
===============================================================================================================================================================================================================================================================================
Installing:
 mariadb-server                                                               x86_64                                                      1:5.5.68-1.el7                                                       base                                                       11 M
Installing for dependencies:
 mariadb                                                                      x86_64                                                      1:5.5.68-1.el7                                                       base                                                      8.8 M
 perl-Compress-Raw-Bzip2                                                      x86_64                                                      2.061-3.el7                                                          base                                                       32 k
 perl-Compress-Raw-Zlib                                                       x86_64                                                      1:2.061-4.el7                                                        base                                                       57 k
 perl-DBD-MySQL                                                               x86_64                                                      4.023-6.el7                                                          base                                                      140 k
 perl-DBI                                                                     x86_64                                                      1.627-4.el7                                                          base                                                      802 k
 perl-Data-Dumper                                                             x86_64                                                      2.145-3.el7                                                          base                                                       47 k
 perl-IO-Compress                                                             noarch                                                      2.061-2.el7                                                          base                                                      260 k
 perl-Net-Daemon                                                              noarch                                                      0.48-5.el7                                                           base                                                       51 k
 perl-PlRPC                                                                   noarch                                                      0.2020-14.el7                                                        base                                                       36 k

Transaction Summary
===============================================================================================================================================================================================================================================================================
Install  1 Package (+9 Dependent packages)

Total download size: 21 M
Installed size: 110 M
Is this ok [y/d/N]: y
Downloading packages:
(1/10): mariadb-5.5.68-1.el7.x86_64.rpm                                                                                                                                                                                                                 | 8.8 MB  00:00:01
(2/10): perl-Compress-Raw-Bzip2-2.061-3.el7.x86_64.rpm                                                                                                                                                                                                  |  32 kB  00:00:00
(3/10): perl-Compress-Raw-Zlib-2.061-4.el7.x86_64.rpm                                                                                                                                                                                                   |  57 kB  00:00:00
(4/10): perl-DBD-MySQL-4.023-6.el7.x86_64.rpm                                                                                                                                                                                                           | 140 kB  00:00:00
(5/10): mariadb-server-5.5.68-1.el7.x86_64.rpm                                                                                                                                                                                                          |  11 MB  00:00:02
(6/10): perl-Data-Dumper-2.145-3.el7.x86_64.rpm                                                                                                                                                                                                         |  47 kB  00:00:00
(7/10): perl-DBI-1.627-4.el7.x86_64.rpm                                                                                                                                                                                                                 | 802 kB  00:00:00
(8/10): perl-IO-Compress-2.061-2.el7.noarch.rpm                                                                                                                                                                                                         | 260 kB  00:00:00
(9/10): perl-Net-Daemon-0.48-5.el7.noarch.rpm                                                                                                                                                                                                           |  51 kB  00:00:00
(10/10): perl-PlRPC-0.2020-14.el7.noarch.rpm                                                                                                                                                                                                            |  36 kB  00:00:00
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                                                                                                          8.5 MB/s |  21 MB  00:00:02
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : perl-Data-Dumper-2.145-3.el7.x86_64                                                                                                                                                                                                                        1/10
  Installing : 1:perl-Compress-Raw-Zlib-2.061-4.el7.x86_64                                                                                                                                                                                                                2/10
  Installing : 1:mariadb-5.5.68-1.el7.x86_64                                                                                                                                                                                                                              3/10
  Installing : perl-Net-Daemon-0.48-5.el7.noarch                                                                                                                                                                                                                          4/10
  Installing : perl-Compress-Raw-Bzip2-2.061-3.el7.x86_64                                                                                                                                                                                                                 5/10
  Installing : perl-IO-Compress-2.061-2.el7.noarch                                                                                                                                                                                                                        6/10
  Installing : perl-PlRPC-0.2020-14.el7.noarch                                                                                                                                                                                                                            7/10
  Installing : perl-DBI-1.627-4.el7.x86_64                                                                                                                                                                                                                                8/10
  Installing : perl-DBD-MySQL-4.023-6.el7.x86_64                                                                                                                                                                                                                          9/10
  Installing : 1:mariadb-server-5.5.68-1.el7.x86_64                                                                                                                                                                                                                      10/10
  Verifying  : perl-Compress-Raw-Bzip2-2.061-3.el7.x86_64                                                                                                                                                                                                                 1/10
  Verifying  : perl-Net-Daemon-0.48-5.el7.noarch                                                                                                                                                                                                                          2/10
  Verifying  : perl-Data-Dumper-2.145-3.el7.x86_64                                                                                                                                                                                                                        3/10
  Verifying  : 1:mariadb-server-5.5.68-1.el7.x86_64                                                                                                                                                                                                                       4/10
  Verifying  : perl-DBD-MySQL-4.023-6.el7.x86_64                                                                                                                                                                                                                          5/10
  Verifying  : 1:mariadb-5.5.68-1.el7.x86_64                                                                                                                                                                                                                              6/10
  Verifying  : 1:perl-Compress-Raw-Zlib-2.061-4.el7.x86_64                                                                                                                                                                                                                7/10
  Verifying  : perl-DBI-1.627-4.el7.x86_64                                                                                                                                                                                                                                8/10
  Verifying  : perl-IO-Compress-2.061-2.el7.noarch                                                                                                                                                                                                                        9/10
  Verifying  : perl-PlRPC-0.2020-14.el7.noarch                                                                                                                                                                                                                           10/10

Installed:
  mariadb-server.x86_64 1:5.5.68-1.el7

Dependency Installed:
  mariadb.x86_64 1:5.5.68-1.el7       perl-Compress-Raw-Bzip2.x86_64 0:2.061-3.el7 perl-Compress-Raw-Zlib.x86_64 1:2.061-4.el7 perl-DBD-MySQL.x86_64 0:4.023-6.el7 perl-DBI.x86_64 0:1.627-4.el7 perl-Data-Dumper.x86_64 0:2.145-3.el7 perl-IO-Compress.noarch 0:2.061-2.el7
  perl-Net-Daemon.noarch 0:0.48-5.el7 perl-PlRPC.noarch 0:0.2020-14.el7

Complete!
[root@ansible ~]#
```

安装时，会自动安装一些依赖。



此时查看`mariadb`服务信息：

```sh
[root@ansible ~]# systemctl status mariadb
● mariadb.service - MariaDB database server
   Loaded: loaded (/usr/lib/systemd/system/mariadb.service; disabled; vendor preset: disabled)
   Active: inactive (dead)
[root@ansible ~]#
```

可以看到，还没有启动起来。



## 3. 设置UTF-8编码

为了让后续创建的数据库里面中文不乱码，我们设置一下mysql默认的编码格式为`utf-8`。

主要修改以下几个配置文件。

- 编辑`/etc/my.cnf`增加10-14行的内容：

```ini {10-14}
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
# Settings user and group are ignored when systemd is used.
# If you need to run mysqld under a different user or group,
# customize your systemd unit file for mariadb according to the
# instructions in http://fedoraproject.org/wiki/Systemd
default-storage-engine = innodb
innodb_file_per_table
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8

[mysqld_safe]
log-error=/var/log/mariadb/mariadb.log
pid-file=/var/run/mariadb/mariadb.pid

#
# include all files from the config directory
#
!includedir /etc/my.cnf.d
```

- 编辑`/etc/my.cnf.d/client.cnf`，增加第6行行的内容：

```ini {8}
#
# These two groups are read by the client library
# Use it for options that affect all clients, but not the server
#


[client]
default-character-set = utf8

# This group is not read by mysql client library,
# If you use the same .cnf file for MySQL and MariaDB,
# use it for MariaDB-only client options
[client-mariadb]
```

编辑`/etc/my.cnf.d/mysql-clients.cnf`，增加第6行行的内容：

```ini {7}
#
# These groups are read by MariaDB command-line tools
# Use it for options that affect only one utility
#

[mysql]
default-character-set=utf8

[mysql_upgrade]

[mysqladmin]

[mysqlbinlog]

[mysqlcheck]

[mysqldump]

[mysqlimport]

[mysqlshow]

[mysqlslap]
```

以上配置修改完成后，就可以启动mariadb服务。

## 4. 启动mariadb服务

- 启动服务：`systemctl start mariadb`
- 设置开机启动：`systemctl enable mariadb`
- 查看服务状态：`systemctl status mariadb`

```sh
[root@ansible ~]# systemctl start mariadb
[root@ansible ~]# systemctl enable mariadb
Created symlink from /etc/systemd/system/multi-user.target.wants/mariadb.service to /usr/lib/systemd/system/mariadb.service.
[root@ansible ~]# systemctl status mariadb
● mariadb.service - MariaDB database server
   Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; vendor preset: disabled)
   Active: active (running) since Tue 2024-07-23 22:28:28 CST; 12s ago
 Main PID: 1969 (mysqld_safe)
   CGroup: /system.slice/mariadb.service
           ├─1969 /bin/sh /usr/bin/mysqld_safe --basedir=/usr
           └─2194 /usr/libexec/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib64/mysql/plugin --log-error=/var/log/mariadb/mariadb.log --pid-file=/var/run/mariadb/mariadb.pid --socket=/var/lib/mysql/mysql.sock

Jul 23 22:28:26 ansible mariadb-prepare-db-dir[1886]: MySQL manual for more instructions.
Jul 23 22:28:26 ansible mariadb-prepare-db-dir[1886]: Please report any problems at http://mariadb.org/jira
Jul 23 22:28:26 ansible mariadb-prepare-db-dir[1886]: The latest information about MariaDB is available at http://mariadb.org/.
Jul 23 22:28:26 ansible mariadb-prepare-db-dir[1886]: You can find additional information about the MySQL part at:
Jul 23 22:28:26 ansible mariadb-prepare-db-dir[1886]: http://dev.mysql.com
Jul 23 22:28:26 ansible mariadb-prepare-db-dir[1886]: Consider joining MariaDB's strong and vibrant community:
Jul 23 22:28:26 ansible mariadb-prepare-db-dir[1886]: https://mariadb.org/get-involved/
Jul 23 22:28:26 ansible mysqld_safe[1969]: 240723 22:28:26 mysqld_safe Logging to '/var/log/mariadb/mariadb.log'.
Jul 23 22:28:26 ansible mysqld_safe[1969]: 240723 22:28:26 mysqld_safe Starting mysqld daemon with databases from /var/lib/mysql
Jul 23 22:28:28 ansible systemd[1]: Started MariaDB database server.
[root@ansible ~]#
```

可以看到，mariadb服务正常，没有报错。



## 5. mysql安全设置

运行安全向导`mysql_secure_installation`，设置root用户密码，移除匿名用户，禁止root远程登录等：

```sh
[root@ansible ~]# mysql_secure_installation

NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
      SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

In order to log into MariaDB to secure it, we'll need the current
password for the root user.  If you've just installed MariaDB, and
you haven't set the root password yet, the password will be blank,
so you should just press enter here.

Enter current password for root (enter for none):
OK, successfully used password, moving on...

Setting the root password ensures that nobody can log into the MariaDB
root user without the proper authorisation.

Set root password? [Y/n]  # <–-- 是否设置root用户密码，输入Y并回车或直接回车
New password:             # <–-- 设置root用户的密码
Re-enter new password:    # <–-- 再输入一次你设置的密码
Password updated successfully!
Reloading privilege tables..
 ... Success!


By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.

Remove anonymous users? [Y/n]   # <–-- 是否删除匿名用户,生产环境建议删除，所以直接回车
 ... Success!

Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.

Disallow root login remotely? [Y/n]   # <--- 是否禁止root远程登录，禁止，直接回车
 ... Success!

By default, MariaDB comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.

Remove test database and access to it? [Y/n]   # <--- 是否删除test数据库,直接回车
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? [Y/n]    # <--- 是否重新加载权限表,直接回车
 ... Success!

Cleaning up...

All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.

Thanks for using MariaDB!
[root@ansible ~]#
```

以上全部完成后，就可以使用`root`账号登陆mysql了。



```mysql
[root@ansible ~]# mysql -u root -p
Enter password:  # <–-- 输入root用户的密码
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 10
Server version: 5.5.68-MariaDB MariaDB Server

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
3 rows in set (0.00 sec)

MariaDB [(none)]>
```



使用`mysql -version`查看mysql的版本号:

```sh
[root@ansible ~]# mysql --version
mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
```



## 6. mysql命令行的简单使用



### 6.1 显示所有数据库

- 使用命令`show databases;`显示所有数据库。

```mariadb
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
3 rows in set (0.00 sec)

MariaDB [(none)]>
```



### 6.2 查看当前使用的字符集

- 使用命令`SHOW VARIABLES LIKE 'character%';`可以查看当前使用的字符集。

```mariadb
MariaDB [(none)]> SHOW VARIABLES LIKE 'character%';
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | utf8                       |
| character_set_filesystem | binary                     |
| character_set_results    | utf8                       |
| character_set_server     | utf8                       |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
8 rows in set (0.00 sec)

MariaDB [(none)]>
```



在安装Ansible UI工具semaphore时，因其依赖mysql服务，所以在这里以创建semaphore数据库为例，并创建一个用户并授权。



### 6.3 创建数据库

- 创建新数据库，假设数据库名为semaphore，则命令为`CREATE DATABASE semaphore;`。
- 查看创建的数据库的定义信息，使用`SHOW CREATE DATABASE db_name`。

```mariadb
MariaDB [(none)]> CREATE DATABASE semaphore;
Query OK, 1 row affected (0.00 sec)

MariaDB [(none)]> SHOW CREATE DATABASE semaphore;
+-----------+--------------------------------------------------------------------+
| Database  | Create Database                                                    |
+-----------+--------------------------------------------------------------------+
| semaphore | CREATE DATABASE `semaphore` /*!40100 DEFAULT CHARACTER SET utf8 */ |
+-----------+--------------------------------------------------------------------+
1 row in set (0.00 sec)

MariaDB [(none)]>
```

可以看到，数据库创建成功了，默认编码是`utf8`。



### 6.4 创建用户并授权

- 创建新用户并设置密码，假设用户名为`myuser`，密码为`mypassword`，则应使用以下命令：

```mariadb
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
```

我创建一个用户名`ansibleui`，密码为`mypassword`的用户：

```mariadb
# 创建新户
MariaDB [(none)]> CREATE USER 'ansibleui'@'localhost' IDENTIFIED BY 'mypassword';
Query OK, 0 rows affected (0.00 sec)

# 查询刚创建出的用户
MariaDB [(none)]> select * from mysql.user where user='ansibleui'\G
*************************** 1. row ***************************
                  Host: localhost
                  User: ansibleui
              Password: *FABE5482D5AADF36D028AC443D117BE1180B9725
           Select_priv: N
           Insert_priv: N
           Update_priv: N
           Delete_priv: N
           Create_priv: N
             Drop_priv: N
           Reload_priv: N
         Shutdown_priv: N
          Process_priv: N
             File_priv: N
            Grant_priv: N
       References_priv: N
            Index_priv: N
            Alter_priv: N
          Show_db_priv: N
            Super_priv: N
 Create_tmp_table_priv: N
      Lock_tables_priv: N
          Execute_priv: N
       Repl_slave_priv: N
      Repl_client_priv: N
      Create_view_priv: N
        Show_view_priv: N
   Create_routine_priv: N
    Alter_routine_priv: N
      Create_user_priv: N
            Event_priv: N
          Trigger_priv: N
Create_tablespace_priv: N
              ssl_type:
            ssl_cipher:
           x509_issuer:
          x509_subject:
         max_questions: 0
           max_updates: 0
       max_connections: 0
  max_user_connections: 0
                plugin:
 authentication_string:
1 row in set (0.00 sec)

MariaDB [(none)]>
```



### 6.5 授权

- 授权`myuser`用户在`mydb`数据库上具有所有权限，则应使用以下命令：

```mariadb
GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'localhost';
```

我给`ansibleui`用户授权，拥有`semaphore`数据库所有权限：

```mariadb
MariaDB [(none)]> GRANT ALL PRIVILEGES ON semaphore.* TO 'ansibleui'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```



### 6.6 刷新权限表

6.5节点虽然给用户分配了权限，但未刷新权限表，权限没有正式生效。只有刷新权限表后，用户授权才正常。

使用以下命令`FLUSH PRIVILEGES;`刷新权限表。

```mariadb
MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.00 sec)
```



### 6.7 退出mysql命令行

- 使用`exit`退出命令行。

```sh
MariaDB [(none)]> exit
Bye
[root@ansible ~]#
```



### 6.8 测试新用户权限

使用用户名`ansibleui`，密码为`mypassword`的用户登陆mysql命令行：

```sh
[root@ansible ~]# mysql -uansibleui -p
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 13
Server version: 5.5.68-MariaDB MariaDB Server

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| semaphore          |
+--------------------+
2 rows in set (0.00 sec)
```



### 6.9 切换数据库

- 使用`use db_name`可以切换到名称为`db_name`的数据库。

```mariadb
MariaDB [(none)]> use semaphore
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [semaphore]>
```

可以看到，此时已经在`semaphore`数据库下了。



### 6.10 显示数据库下所有的表

- 使用`show tables;`;`可以显示数据库下所有的表。

```sh
MariaDB [semaphore]> show tables;
+------------------------------------+
| Tables_in_semaphore                |
+------------------------------------+
| access_key                         |
| event                              |
| event_backup_5784568               |
| migrations                         |
| option                             |
| project                            |
| project__environment               |
| project__integration               |
| project__integration_alias         |
| project__integration_extract_value |
| project__integration_matcher       |
| project__inventory                 |
| project__repository                |
| project__schedule                  |
| project__template                  |
| project__user                      |
| project__view                      |
| runner                             |
| session                            |
| task                               |
| task__output                       |
| user                               |
| user__token                        |
+------------------------------------+
23 rows in set (0.00 sec)

MariaDB [semaphore]> 
```

