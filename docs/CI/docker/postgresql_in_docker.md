
# docker配置PostgreSQL数据库

参考官方文档 https://hub.docker.com/_/postgres

## 1. 下载镜像

下载`postgres`镜像：

```sh
[root@hellogitlab ~]# docker pull postgres
Using default tag: latest
Trying to pull repository docker.io/library/postgres ...
^[[Olatest: Pulling from docker.io/library/postgres
a076a628af6f: Already exists
d54fa0e0eb76: Pull complete
8950a7ea6876: Pull complete
1cc02b1df09e: Pull complete
06f548e51228: Pull complete
74665692d4ea: Pull complete
235e34eb13ab: Pull complete
4ad7ef5e2e79: Pull complete
76670339b0f8: Pull complete
496fa0539f99: Pull complete
f32ecbdf3b52: Pull complete
7536b8fe81ac: Pull complete
71dfc17927aa: Pull complete
fd48bac409bb: Pull complete
Digest: sha256:ec74afc9fa969a235462c27017a3fe73a05c9d4725d7e4afbe2ba6eb82fdfc87
Status: Downloaded newer image for docker.io/postgres:latest
[root@hellogitlab ~]# docker images postgres
REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
docker.io/postgres   latest              acf5fb8bfd76        2 months ago        314 MB
```

## 2. 创建本地持久化目录

创建本地持久化目录：

```sh
[root@hellogitlab ~]# mkdir /dockerdata && cd /dockerdata
[root@hellogitlab dockerdata]# mkdir -p  postgresql/data
[root@hellogitlab dockerdata]# cd postgresql/
[root@hellogitlab postgresql]# ls
data
[root@hellogitlab postgresql]#
```

## 3. 尝试运行容器

为了密码安全，我们创建一个保证密码的配置文件`postgres-passwd`:

```sh
[root@hellogitlab postgresql]# echo 'POSTGRES_PASSWORD=securepasswd' > postgres-passwd
[root@hellogitlab postgresql]# echo 'POSTGRES_USER=postgres' >> postgres-passwd
POSTGRES_PASSWORD=securepasswd
POSTGRES_USER=postgres
[root@hellogitlab postgresql]# 
```



运行`postgresql`容器：

```sh
docker run --name postgres-server --restart=always -p 5432:5432 -v /dockerdata/postgresql/data:/var/lib/postgresql/data -e POSTGRES_PASSWORD_FILE=/dockerdata/postgresql/postgres_passwd -d postgres
```

使用这种方式运行容器中一直提示找不到文件：

```sh
[root@hellogitlab postgresql]# docker run --name postgres-server --restart=always -p 5432:5432 -v /dockerdata/postgresql/data:/var/lib/postgresql/data -e POSTGRES_PASSWORD_FILE=/dockerdata/postgresql/postgres_passwd -d postgres
be7218055a40da7c58c46742286dc73ee8bcd824f1180a29d591d0b7bb1fad6d
[root@hellogitlab postgresql]# docker logs be72
/usr/local/bin/docker-entrypoint.sh: line 21: /dockerdata/postgresql/postgres_passwd: No such file or directory
/usr/local/bin/docker-entrypoint.sh: line 21: /dockerdata/postgresql/postgres_passwd: No such file or directory
/usr/local/bin/docker-entrypoint.sh: line 21: /dockerdata/postgresql/postgres_passwd: No such file or directory
/usr/local/bin/docker-entrypoint.sh: line 21: /dockerdata/postgresql/postgres_passwd: No such file or directory
[root@hellogitlab postgresql]#
```

百度搜索`docker postgresql POSTGRES_PASSWORD_FILE`设置`POSTGRES_PASSWORD_FILE`文件的参考文献非常少。

我们改用直接在命令行设置密码形式运行：


```sh
[root@hellogitlab ~]# docker run --name postgres-server --restart=always -p 5432:5432 -v /dockerdata/postgresql/data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=securepasswd -d postgres
27a0f23540d8e23a1b86b56465d35e60c768ac822fb95b54b527996d30658a0a
[root@hellogitlab ~]# docker ps |head -n 1; docker ps |grep postgres
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                              NAMES
27a0f23540d8        postgres            "docker-entrypoint..."   2 minutes ago       Up 2 minutes        0.0.0.0:5432->5432/tcp             postgres-server
```

可以看到postgres-server容器运行正常！



以上运行容器命令中，需要输入` POSTGRES_PASSWORD=securepasswd`来指定密码，也存在一定的风险。

通过`docker run`帮助文档可知我们可以使用`--env-file list     Read in a file of environment variables (default [])`参数来将环境变量设置在文件中。我们可以配置一个环境变量文件。

我们先环境一个`.postgres.env`的环境变量文件,并存放在`/dockerdata/postgresql`目录下，其内容如下：

```
POSTGRES_USER=manager
POSTGRES_PASSWORD=securepasswd
POSTGRES_DB=testdb
```

查看文件内容：

```sh
[root@hellogitlab postgresql]# pwd
/dockerdata/postgresql
[root@hellogitlab postgresql]# cat .postgres.env
POSTGRES_USER=manager
POSTGRES_PASSWORD=securepasswd
POSTGRES_DB=testdb
```

我们将之前运行的`postgres-server`容器删除掉。然后重新创建新的容器。



## 4. 删除不用的容器

我们在`~/.bashrc`文件中加上以下内容：

```sh
alias dkr='remove_docker_container'
function remove_docker_container()
{
    container_name=$1
    docker stop "${container_name}"
    docker rm "${container_name}"
}
```

然后使用`source ~/.bashrc`使快捷命令生效。我们使用快捷命令将之前生成的`postgres-server`容器删除掉。

```sh
[root@hellogitlab ~]# dkr postgres-server
postgres-server
postgres-server
[root@hellogitlab ~]# docker ps -a|grep postgres
```

可以看到`postgres-server`容器已经被删除掉了。

将之前容器本地挂载的目录下的文件清空掉。

```sh
[root@hellogitlab ~]# trash-put /dockerdata/postgresql/data/*
[root@hellogitlab ~]# trash-empty
```



## 5. 通过环境文件读取环境变量来运行容器

运行以下命令：

```text
docker run --name postgres-server --restart=always -p 5432:5432 -v /dockerdata/postgresql/data:/var/lib/postgresql/data --env-file=/dockerdata/postgresql/.postgres.env -d postgres
```

命令释义：

- `docker run` 运行容器。
- `--name postgres-server`指定容器名称。
- `--restart=always` docker服务重启后本容器自动启动。
- `-p 5432:5432` 将容器中的5432端口映射到宿主机端口的5432端口， `-p 宿主机端口:容器内部端口`。
- `-v /dockerdata/postgresql/data:/var/lib/postgresql/data` 将容器中路径`/var/lib/postgresql/data`挂载到宿主机的`/dockerdata/postgresql/data`目录，实现数据持久化。
- `--env-file=/dockerdata/postgresql/.postgres.env` 从环境变量文件中读取环境变量。
- `-d postgres` 在后台运行容器。 

执行命令：

```sh
[root@hellogitlab ~]# docker run --name postgres-server --restart=always -p 5432:5432 -v /dockerdata/postgresql/data:/var/lib/postgresql/data --env-file=/dockerdata/postgresql/.postgres.env -d postgres
ab552ed59830c46f5d6db2f128807b5f2be9e16ed59e5f06d58361439cef8755
[root@hellogitlab ~]# dkc postgres-server
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                              NAMES
ab552ed59830        postgres            "docker-entrypoint..."   19 seconds ago      Up 19 seconds       0.0.0.0:5432->5432/tcp             postgres-server
[root@hellogitlab ~]#
```

查看日志信息：

```sh
[root@hellogitlab ~]# docker logs ab55
The files belonging to this database system will be owned by user "postgres".
This user must also own the server process.
The database cluster will be initialized with locale "en_US.utf8".
The default database encoding has accordingly been set to "UTF8".
The default text search configuration will be set to "english".
Data page checksums are disabled.
fixing permissions on existing directory /var/lib/postgresql/data ... ok
creating subdirectories ... ok
selecting dynamic shared memory implementation ... posix
selecting default max_connections ... 100
selecting default shared_buffers ... 128MB
selecting default time zone ... Etc/UTC
creating configuration files ... ok
running bootstrap script ... ok
performing post-bootstrap initialization ... ok
syncing data to disk ... ok
Success. You can now start the database server using:
    pg_ctl -D /var/lib/postgresql/data -l logfile start
initdb: warning: enabling "trust" authentication for local connections
You can change this by editing pg_hba.conf or using the option -A, or
--auth-local and --auth-host, the next time you run initdb.
waiting for server to start....2021-03-31 12:48:37.826 UTC [45] LOG:  starting PostgreSQL 13.1 (Debian 13.1-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
2021-03-31 12:48:37.830 UTC [45] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2021-03-31 12:48:37.843 UTC [46] LOG:  database system was shut down at 2021-03-31 12:48:37 UTC
2021-03-31 12:48:37.849 UTC [45] LOG:  database system is ready to accept connections
 done
server started
CREATE DATABASE
/usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
waiting for server to shut down....2021-03-31 12:48:38.292 UTC [45] LOG:  received fast shutdown request
2021-03-31 12:48:38.297 UTC [45] LOG:  aborting any active transactions
2021-03-31 12:48:38.300 UTC [45] LOG:  background worker "logical replication launcher" (PID 52) exited with exit code 1
2021-03-31 12:48:38.300 UTC [47] LOG:  shutting down
2021-03-31 12:48:38.333 UTC [45] LOG:  database system is shut down
 done
server stopped
PostgreSQL init process complete; ready for start up.
2021-03-31 12:48:38.424 UTC [1] LOG:  starting PostgreSQL 13.1 (Debian 13.1-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
2021-03-31 12:48:38.425 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2021-03-31 12:48:38.425 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2021-03-31 12:48:38.432 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2021-03-31 12:48:38.440 UTC [73] LOG:  database system was shut down at 2021-03-31 12:48:38 UTC
2021-03-31 12:48:38.447 UTC [1] LOG:  database system is ready to accept connections
[root@hellogitlab ~]#
```

可以看到日志中没有报错，容器运行正常。

```sh
[root@hellogitlab ~]# docker inspect postgres-server|jq '.[].Config.Env'
[
  "POSTGRES_USER=manager",
  "POSTGRES_PASSWORD=securepasswd",
  "POSTGRES_DB=testdb",
  "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/postgresql/13/bin",
  "GOSU_VERSION=1.12",
  "LANG=en_US.utf8",
  "PG_MAJOR=13",
  "PG_VERSION=13.1-1.pgdg100+1",
  "PGDATA=/var/lib/postgresql/data"
]
```

可以看到我们设置的环境变量已经正常读取到容器的元数据当中了。



## 6. 进入容器操作数据库

使用以下命令进入到`postgres`数据库中：

```sh
[root@hellogitlab postgresql]# docker exec -it postgres-server /bin/bash
root@ab552ed59830:/# whoami
root
```

由于我们在创建容器的时候设置了环境变量，现在在容器内可以直接使用环境变量：

```sh
root@ab552ed59830:/# echo $POSTGRES_USER
manager
root@ab552ed59830:/# echo $POSTGRES_DB
testdb
```

可以看到环境变量能够正常使用。

下面我们使用`psql`连接到数据库命令行。

```sh
# 查看帮助信息
root@ab552ed59830:/# psql --help
psql is the PostgreSQL interactive terminal.

Usage:
  psql [OPTION]... [DBNAME [USERNAME]]

General options:
  -c, --command=COMMAND    run only single command (SQL or internal) and exit
  -d, --dbname=DBNAME      database name to connect to (default: "root")
  -f, --file=FILENAME      execute commands from file, then exit
  -l, --list               list available databases, then exit
  -v, --set=, --variable=NAME=VALUE
                           set psql variable NAME to VALUE
                           (e.g., -v ON_ERROR_STOP=1)
  -V, --version            output version information, then exit
  -X, --no-psqlrc          do not read startup file (~/.psqlrc)
  -1 ("one"), --single-transaction
                           execute as a single transaction (if non-interactive)
  -?, --help[=options]     show this help, then exit
      --help=commands      list backslash commands, then exit
      --help=variables     list special variables, then exit

Input and output options:
  -a, --echo-all           echo all input from script
  -b, --echo-errors        echo failed commands
  -e, --echo-queries       echo commands sent to server
  -E, --echo-hidden        display queries that internal commands generate
  -L, --log-file=FILENAME  send session log to file
  -n, --no-readline        disable enhanced command line editing (readline)
  -o, --output=FILENAME    send query results to file (or |pipe)
  -q, --quiet              run quietly (no messages, only query output)
  -s, --single-step        single-step mode (confirm each query)
  -S, --single-line        single-line mode (end of line terminates SQL command)

Output format options:
  -A, --no-align           unaligned table output mode
      --csv                CSV (Comma-Separated Values) table output mode
  -F, --field-separator=STRING
                           field separator for unaligned output (default: "|")
  -H, --html               HTML table output mode
  -P, --pset=VAR[=ARG]     set printing option VAR to ARG (see \pset command)
  -R, --record-separator=STRING
                           record separator for unaligned output (default: newline)
  -t, --tuples-only        print rows only
  -T, --table-attr=TEXT    set HTML table tag attributes (e.g., width, border)
  -x, --expanded           turn on expanded table output
  -z, --field-separator-zero
                           set field separator for unaligned output to zero byte
  -0, --record-separator-zero
                           set record separator for unaligned output to zero byte

Connection options:
  -h, --host=HOSTNAME      database server host or socket directory (default: "local socket")
  -p, --port=PORT          database server port (default: "5432")
  -U, --username=USERNAME  database user name (default: "root")
  -w, --no-password        never prompt for password
  -W, --password           force password prompt (should happen automatically)

For more information, type "\?" (for internal commands) or "\help" (for SQL
commands) from within psql, or consult the psql section in the PostgreSQL
documentation.

Report bugs to <pgsql-bugs@lists.postgresql.org>.
PostgreSQL home page: <https://www.postgresql.org/>
root@ab552ed59830:/#
```

PostgreSQL 语法详细可参考： https://www.runoob.com/postgresql/postgresql-syntax.html

我们通过`psql`命令进入到数据库命令行：

```sh
root@ab552ed59830:/# POSTGRES_PASSWORD=$POSTGRES_PASSWORD psql -U$POSTGRES_USER -d$POSTGRES_DB
psql (13.1 (Debian 13.1-1.pgdg100+1))
Type "help" for help.

testdb=#
```

可以看到已经进入到`testdb`数据库下了。

## 7. 创建数据库和用户并授权

我们为nextcloud私有云盘创建一个`nextcloud`的数据库，并创建一个`ncadmin`的用户，并将`ncadmin`授权控制`nextcloud`数据库。



- 创建数据库

```sh
CREATE DATABASE your_dbname;
```

执行命令：

```sh
testdb=# CREATE DATABASE nextcloud;
CREATE DATABASE
testdb=# \list nextcloud
                             List of databases
   Name    |  Owner  | Encoding |  Collate   |   Ctype    | Access privileges
-----------+---------+----------+------------+------------+-------------------
 nextcloud | manager | UTF8     | en_US.utf8 | en_US.utf8 |
(1 row)
```

- 创建用户

```sh
CREATE USER username WITH password 'password';
```

执行命令:

```sh
testdb=# CREATE USER ncadmin WITH password 'securepasswd';
CREATE ROLE
```

列出所有用户：

```sh
testdb=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of
-----------+------------------------------------------------------------+-----------
 manager   | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 ncadmin   |                                                            | {}
```

- 授权

```
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;
```

执行命令：

```sh
testdb=# GRANT ALL PRIVILEGES ON DATABASE nextcloud TO ncadmin;
GRANT
testdb=# \list nextcloud
                             List of databases
   Name    |  Owner  | Encoding |  Collate   |   Ctype    | Access privileges
-----------+---------+----------+------------+------------+-------------------
 nextcloud | manager | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/manager        +
           |         |          |            |            | manager=CTc/manager  +
           |         |          |            |            | ncadmin=CTc/manager
(1 row)
```

- 更新用户密码

```
ALTER USER name WITH PASSWORD 'password'; 
```

执行命令：

```sh
testdb=# ALTER USER ncadmin WITH PASSWORD 'newsecurepasswd';
ALTER ROLE
```

退出：

```sh
testdb=# exit
root@ab552ed59830:/#
```

## 8. 测试授权是否成功

为了测试在宿主机上面能否连接到容器的数据库，我们在宿主机上面安装postgresql客户端：

```sh
[root@hellogitlab ~]# yum install postgresql -y
总下载量：3.3 M
安装大小：17 M
Downloading packages:
(1/2): postgresql-libs-9.2.24-4.el7_8.x86_64.rpm                                                                                                                  | 234 kB  00:00:00
(2/2): postgresql-9.2.24-4.el7_8.x86_64.rpm                                                                                                                       | 3.0 MB  00:00:00
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
总计                                                                                                                                                     4.1 MB/s | 3.3 MB  00:00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  正在安装    : postgresql-libs-9.2.24-4.el7_8.x86_64                                                                                                                                1/2
  正在安装    : postgresql-9.2.24-4.el7_8.x86_64                                                                                                                                     2/2
  验证中      : postgresql-9.2.24-4.el7_8.x86_64                                                                                                                                     1/2
  验证中      : postgresql-libs-9.2.24-4.el7_8.x86_64                                                                                                                                2/2

已安装:
  postgresql.x86_64 0:9.2.24-4.el7_8

作为依赖被安装:
  postgresql-libs.x86_64 0:9.2.24-4.el7_8

完毕！
[root@hellogitlab ~]# psql --version
psql (PostgreSQL) 9.2.24
```

登陆：

```sh
root@hellogitlab ~]# psql -Uncadmin -dnextcloud -h localhost
用户 ncadmin 的口令：
psql (9.2.24, 服务器 13.1 (Debian 13.1-1.pgdg100+1))
警告：psql 版本9.2， 服务器版本13.0.
一些psql功能可能无法工作.
输入 "help" 来获取帮助信息.
nextcloud->
nextcloud->
```

能够正常登陆进数据库命令行，尝试创建表并插入数据：

```sh
# 参考：https://www.runoob.com/postgresql/postgresql-create-table.html
# 创建表
nextcloud=> CREATE TABLE COMPANY(
nextcloud(>    ID INT PRIMARY KEY     NOT NULL,
nextcloud(>    NAME           TEXT    NOT NULL,
nextcloud(>    AGE            INT     NOT NULL,
nextcloud(>    ADDRESS        CHAR(50),
nextcloud(>    SALARY         REAL,
nextcloud(>    JOIN_DATE      DATE
nextcloud(> );
CREATE TABLE

# 查看表
nextcloud-> \d
               关联列表
 架构模式 |  名称   |  型别  | 拥有者
----------+---------+--------+---------
 public   | company | 资料表 | ncadmin
(1 行记录)

# 向表中插入数据
nextcloud=> INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY,JOIN_DATE) VALUES (1, 'Paul', 32, 'California', 20000.00,'2001-07-13');
INSERT 0 1


# 查询表数据
nextcloud=> SELECT * FROM company;
 id | name | age |                      address                       | salary | join_date
----+------+-----+----------------------------------------------------+--------+------------
  1 | Paul |  32 | California                                         |  20000 | 2001-07-13
(1 行记录)


# 删除表
nextcloud=> DROP TABLE company;
DROP TABLE
nextcloud=> SELECT * FROM company;
ERROR:  relation "company" does not exist
第1行SELECT * FROM company;
                   ^
nextcloud=>

# 退出
nextcloud-> \quit
```

说明操作正常！连接没有问题。



参考：

- [postgres Docker Official Images](https://hub.docker.com/_/postgres)
- [如何通过env文件传递docker中的环境变量](http://www.cocoachina.com/articles/44949)
- [PostgreSQL 语法](https://www.runoob.com/postgresql/postgresql-syntax.html)