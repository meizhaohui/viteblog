# mysql数据库的创建、删除与使用

[[toc]]

## 概述  

本文档包括数据库的创建、删除和使用。

## 查看mysql版本号

使用`mysql -version`查看mysql的版本号:

```sh
[root@hopewait mysql]# mysql –version
mysql Ver 14.14 Distrib 5.6.35, for Linux (x86_64) using EditLine wrapper
```

## mysql数据库物理文件存放位置

使用`%datadir%`查看物理文件存放目录:

```sql
mysql> show global variables like "%datadir%" \G
*************************** 1. row ***************************
Variable_name: datadir
    Value: /usr/local/mysql/data/
1 row in set (0.06 sec)
```

## 显示存在的数据库

使用`show databases`查看当前数据库系统中所有的数据库名称:

```sql
mysql>  show databases\G
*************************** 1. row ***************************
Database: information_schema
*************************** 2. row ***************************
Database: mysql
*************************** 3. row ***************************
Database: performance_schema
*************************** 4. row ***************************
Database: test
*************************** 5. row ***************************
Database: wordpress
5 rows in set (0.08 sec)
```

## 创建数据库

使用`create database database_name`创建数据库:

```sql
mysql> create database test_db;
Query OK, 1 row affected (0.00 sec)
    
mysql>  show databases\G
*************************** 1. row ***************************
Database: information_schema
*************************** 2. row ***************************
Database: mysql
*************************** 3. row ***************************
Database: performance_schema
*************************** 4. row ***************************
Database: test
*************************** 5. row ***************************
Database: wordpress
*************************** 6. row ***************************
Database: test_db
5 rows in set (0.08 sec)
```

## 查看创建好的数据库的定义

使用`show create database database_name`可以查看创建好的数据库是如何定义的:

```sql
mysql> show create database test_db\G
*************************** 1. row ***************************
Database: test_db
Create Database: CREATE DATABASE `test_db` /*!40100 DEFAULT CHARACTER SET latin1 */
1 row in set (0.00 sec)
```

## 使用数据库

使用`use database_name`切换数据库，在该数据库下面工作:

```sql
mysql> use test_db;
Database changed
```

## 删除数据库

使用`drop database database_name`删除数据库:

```sql
mysql> drop database test_db;
Query OK, 0 rows affected (0.01 sec)
    
mysql> show create database test_db\G
ERROR 1049 (42000): Unknown database 'test_db'
```

**数据库删除后，数据库中的存储的所有数据表和数据也一同被删除，而且不能恢复。需谨慎操作!!!**
    
## 数据库存储引擎

- 数据库存储引擎是数据库底层软件组件，数据库管理系统DBMS使用数据引擎进行创建、查询、更新和删除数据操作。
- 不同的存储引擎提供不同的存储机制、索引技巧、锁定水平等功能，使用不同的存储引擎，可以获得特定的功能。
- 针对具体的要求，可以对每一个使用不同的存储引擎。
- 可以使用`show engines`查看系统所支持的引擎类型。
- Support列表示某种引擎是否能使用。YES表示可以使用，NO表示不能使用，DEFAULT表示默认存储引擎。
- mysql5.5.5之后默认存储引擎为`InnoDB`（事务型数据库的首选引擎，支持事务安全表ACID，支持行锁定和外键）。
- mysql5.5.5之前默认存储引擎为`MyISAM`（拥有较高的插入、查询速度，但不支持事务）。

查看存储引擎:

```sql
mysql> show engines \G
*************************** 1. row ***************************
Engine: MRG_MYISAM
Support: YES
Comment: Collection of identical MyISAM tables
Transactions: NO
XA: NO
Savepoints: NO
*************************** 2. row ***************************
Engine: CSV
Support: YES
Comment: CSV storage engine
Transactions: NO
XA: NO
Savepoints: NO
*************************** 3. row ***************************
Engine: MyISAM
Support: DEFAULT
Comment: Default engine as of MySQL 3.23 with great performance
Transactions: NO
XA: NO
Savepoints: NO
*************************** 4. row ***************************
Engine: InnoDB
Support: YES
Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
XA: YES
Savepoints: YES
*************************** 5. row ***************************
Engine: MEMORY
Support: YES
Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
XA: NO
Savepoints: NO
5 rows in set (0.00 sec)
    
mysql> show engines\G
*************************** 1. row ***************************
Engine: FEDERATED
Support: NO
Comment: Federated MySQL storage engine
Transactions: NULL
XA: NULL
Savepoints: NULL
*************************** 2. row ***************************
Engine: MRG_MYISAM
Support: YES
Comment: Collection of identical MyISAM tables
Transactions: NO
XA: NO
Savepoints: NO
*************************** 3. row ***************************
Engine: MyISAM
Support: YES
Comment: MyISAM storage engine
Transactions: NO
XA: NO
Savepoints: NO
*************************** 4. row ***************************
Engine: BLACKHOLE
Support: YES
Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
XA: NO
Savepoints: NO
*************************** 5. row ***************************
Engine: CSV
Support: YES
Comment: CSV storage engine
Transactions: NO
XA: NO
Savepoints: NO
*************************** 6. row ***************************
Engine: MEMORY
Support: YES
Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
XA: NO
Savepoints: NO
*************************** 7. row ***************************
Engine: ARCHIVE
Support: YES
Comment: Archive storage engine
Transactions: NO
XA: NO
Savepoints: NO
*************************** 8. row ***************************
Engine: PERFORMANCE_SCHEMA
Support: YES
Comment: Performance Schema
Transactions: NO
XA: NO
Savepoints: NO
*************************** 9. row ***************************
Engine: InnoDB
Support: DEFAULT
Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
XA: YES
Savepoints: YES
9 rows in set (0.00 sec)
```

## 查看默认存储引擎

`storage_engine`变量中保存了默认存储引擎:

```sql
mysql> show variables like 'storage_engine'\G
*************************** 1. row ***************************
Variable_name: storage_engine
Value: InnoDB
1 row in set (0.00 sec)
```

