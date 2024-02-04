# 解决Mysql "Index column size too large. The maximum column size is 767 bytes."异常

[[toc]]

在mysql插入数据时有时会出现以下异常：

```sql
ERROR 1709 (HY000) at line 213 in file: 'z_blog.sql': Index column size too large. The maximum column size is 767 bytes.
```
## 原因
由于`MySQL的`Innodb`引擎表索引字段长度的限制为`767`字节，因此对于多字节字符集的大字段或者多字段组合，创建索引时会出现此错误。

如果是`utf8mb4`字符集，由于`utf8mb4`是4字节字符集，则默认支持的索引字段最大长度是`191`字符（767字节/4字节每字符≈191字符），因此在`varchar (255)`或`char (255)` 类型字段上创建索引会失败。

如果是`utf8`字符集，由于`utf8`是3字节字符集，则默认支持的索引字段最大长度是`255`字符（767字节/3字节每字符≈255字符），则`varchar (255)`或`char (255)`不会失败。


## 处理步骤

增加以下参数到mysql配置文件中：

```
innodb_large_prefix = ON
innodb-file-per-table = ON
innodb_file_format = BARRACUDA
```

### 修改配置文件

MariaDB的配置文件`/etc/my.cnf.d/server.cnf`中使用以下配置:

```
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
init_connect = 'SET NAMES utf8mb4'
innodb_large_prefix = ON
innodb-file-per-table = ON
innodb_file_format = BARRACUDA

[client]
default-character-set=utf8mb4
```


### 重启MariaDB

```sh
[root@hellogitlab data]# systemctl restart mariadb
[root@hellogitlab data]# systemctl status mariadb 
● mariadb.service - MariaDB database server
   Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2019-11-21 23:32:47 CST; 7s ago
  Process: 27499 ExecStartPost=/usr/libexec/mariadb-wait-ready $MAINPID (code=exited, status=0/SUCCESS)
  Process: 27464 ExecStartPre=/usr/libexec/mariadb-prepare-db-dir %n (code=exited, status=0/SUCCESS)
 Main PID: 27498 (mysqld_safe)
   CGroup: /system.slice/mariadb.service
           ├─27498 /bin/sh /usr/bin/mysqld_safe --basedir=/usr
           └─27772 /usr/libexec/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib64/mysql/plugin --log-error=/var/log/maria...

Nov 21 23:32:44 hellogitlab.com systemd[1]: Starting MariaDB database server...
Nov 21 23:32:44 hellogitlab.com mariadb-prepare-db-dir[27464]: Database MariaDB is probably initialized in /var/lib/mysql already, nothi... done.
Nov 21 23:32:44 hellogitlab.com mariadb-prepare-db-dir[27464]: If this is not the case, make sure the /var/lib/mysql is empty before run...b-dir.
Nov 21 23:32:45 hellogitlab.com mysqld_safe[27498]: 191121 23:32:45 mysqld_safe Logging to '/var/log/mariadb/mariadb.log'.
Nov 21 23:32:45 hellogitlab.com mysqld_safe[27498]: 191121 23:32:45 mysqld_safe Starting mysqld daemon with databases from /var/lib/mysql
Nov 21 23:32:47 hellogitlab.com systemd[1]: Started MariaDB database server.
Hint: Some lines were ellipsized, use -l to show in full.
```

### 查看信息

```sql
MariaDB [(none)]> SHOW GLOBAL VARIABLES WHERE variable_name IN ('innodb_file_format', 'innodb_large_prefix', 'innodb_file_per_table');
+-----------------------+-----------+
| Variable_name         | Value     |
+-----------------------+-----------+
| innodb_file_format    | Barracuda |
| innodb_file_per_table | ON        |
| innodb_large_prefix   | ON        |
+-----------------------+-----------+
3 rows in set (0.00 sec)

MariaDB [(none)]> SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';
+--------------------------+--------------------+
| Variable_name            | Value              |
+--------------------------+--------------------+
| character_set_client     | utf8mb4            |
| character_set_connection | utf8mb4            |
| character_set_database   | utf8mb4            |
| character_set_filesystem | binary             |
| character_set_results    | utf8mb4            |
| character_set_server     | utf8mb4            |
| character_set_system     | utf8               |
| collation_connection     | utf8mb4_general_ci |
| collation_database       | utf8mb4_unicode_ci |
| collation_server         | utf8mb4_unicode_ci |
+--------------------------+--------------------+
10 rows in set (0.00 sec)
```

- 修改前每种编码类型支持的最大字符数：

| Charset  |Bytes Per Char| Max Char |
| -------- | ------------ | -------- |
|   utf8   |   3 bytes    |   255    |
| utf8mb4  |   4 bytes    |   191    |
|  latin1  |   1 byte     |   767    |

- 修改后每种编码类型支持的最大字符数：

| Charset  |Bytes Per Char| Max Char |
| -------- | ------------ | -------- |
|   utf8   |   3 bytes    |  21845   |
| utf8mb4  |   4 bytes    |  16384   |
|  latin1  |   1 byte     |  65536   |




参考：
- [The maximum column size is 767 bytes错误处理](https://help.aliyun.com/knowledge_detail/41707.html)
- [ERROR 1709 (HY000) Index column size too large. The maximum column size is 767 bytes.](https://moodle.org/mod/forum/discuss.php?d=366263)
