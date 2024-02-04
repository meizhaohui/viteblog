#  搭建自己的nexus私有仓库8--Nexus3的数据库结构

[[toc]]

本文档是nexus系列课程第8篇。

- nexus系列课程第1篇，请参考 [搭建自己的nexus私有仓库1--nexus初体验](./create_your_nexus.md)
- nexus系列课程第2篇，请参考 [搭建自己的nexus私有仓库2--创建python pypi代理](./create_your_nexus_2.md)
- nexus系列课程第3篇，请参考 [搭建自己的nexus私有仓库3--创建yum ius代理](./create_your_nexus_3.md)
- nexus系列课程第4篇，请参考 [搭建自己的nexus私有仓库4--创建docker私有仓库](./create_your_nexus_4_docker_proxy.md)
- nexus系列课程第5篇，请参考 [搭建自己的nexus私有仓库5--测试docker仓库pull和push](./create_your_nexus_5_test_docker_proxy.md)
- nexus系列课程第6篇，请参考 [搭建自己的nexus私有仓库6--使用nginx反向代理](./create_your_nexus_6_nginx_proxy.md)
- nexus系列课程第7篇，请参考 [搭建自己的nexus私有仓库7--修改nexus容器时区](./create_your_nexus_7_change_timezone.md)

## 1. 情况说明

之前有一个需求，是在docker启动nexus容器后，自动创建代理仓库，不用手动在Web上面操作，最开始的思路是想通过修改数据库来实现。但后来发现nexus有api接口可以使用，因此改用`curl`或Python程序调用nexus的API接口来创建代理仓库。

![](/img/Snipaste_2024-01-29_23-14-31.png)



但此处还是简单看一下数据库的里面的表信息。



### 1.1 登陆进neuxs容器命令行

```sh
[root@nexus ~]# docker exec -it nexus /bin/bash
bash-4.4$ pwd
/opt/sonatype
```



### 1.2 查看db文件夹文件信息

查看db目录下的文件夹的信息：

```sh
bash-4.4$ cd /opt/sonatype/sonatype-work/nexus3/db
bash-4.4$ pwd
/opt/sonatype/sonatype-work/nexus3/db
bash-4.4$ ls -lah
total 48K
drwxr-xr-x  6 nexus nexus 4.0K Jan 21 19:37 .
drwxrwxrwx 16 root  root  4.0K Jan 29 21:07 ..
drwxr-xr-x  2 nexus nexus 4.0K Jan 28 23:19 OSystem
drwxr-xr-x  2 nexus nexus  12K Jan 29 22:14 component
drwxr-xr-x  2 nexus nexus  12K Jan 29 21:13 config
-rw-r--r--  1 nexus nexus    2 Jan 21 19:37 frozen.marker
-rw-r--r--  1 nexus nexus   93 Jan 21 19:37 model.properties
drwxr-xr-x  2 nexus nexus 4.0K Jan 29 21:08 security
bash-4.4$
```



## 2.数据库查询

### 2.1 数据库component组件库命令行操作

#### 2.1.1 进入到数据库component组件库命令行

进入到数据库命令行：

```sh
# 一定要转到/tmp目录下
bash-4.4$ cd /tmp  
bash-4.4$ java -jar /opt/sonatype/nexus/lib/support/nexus-orient-console.jar

OrientDB console v.2.2.36 (build d3beb772c02098ceaea89779a7afd4b7305d3788, branch 2.2.x) https://www.orientdb.com
Type 'help' to display all the supported commands.

# 登陆db
orientdb> connect plocal:/nexus-data/db/component admin admin

Connecting to database [plocal:/nexus-data/db/component] with user 'admin'...
2024-01-29 22:14:44:337 WARNI {db=component} Storage 'component' was not closed properly. Will try to recover from write ahead log... [OLocalPaginatedStorage]
2024-01-29 22:14:44:340 WARNI {db=component} Record com.orientechnologies.orient.core.storage.impl.local.paginated.wal.OFuzzyCheckpointEndRecord{lsn=LSN{segment=30, position=985}} will be skipped during data restore [OLocalPaginatedStorage]
2024-01-29 22:14:44:341 WARNI {db=component} Record OFuzzyCheckpointStartRecord{lsn=LSN{segment=30, position=992}} com.orientechnologies.orient.core.storage.impl.local.paginated.wal.OFuzzyCheckpointStartRecord{lsn=null, previousCheckpoint=LSN{segment=30, position=945}} will be skipped during data restore [OLocalPaginatedStorage]
2024-01-29 22:14:44:341 WARNI {db=component} Record com.orientechnologies.orient.core.storage.impl.local.paginated.wal.OFuzzyCheckpointEndRecord{lsn=LSN{segment=30, position=1032}} will be skipped during data restore [OLocalPaginatedStorage]OK
orientdb {db=component}>
```

#### 2.1.2 查看数据库索引

显示所有索引：

```sql
orientdb {db=component}> list indexes;


INDEXES
+----+-------+-------+----------------+-------------------+---------------------+----------------------------------------------------------------------------+
|#   |RECORDS|COLLATE|TYPE            |FIELDS             |CLASS                |NAME                                                                        |
+----+-------+-------+----------------+-------------------+---------------------+----------------------------------------------------------------------------+
|0   |58     |       |UNIQUE          |                   |asset                |asset_bucket_component_name_idx                                             |
|1   |58     |       |NOTUNIQUE       |                   |asset                |asset_bucket_name_idx                                                       |
|2   |58     |       |UNIQUE          |                   |asset                |asset_bucket_rid_idx                                                        |
|3   |13     |default|NOTUNIQUE       |component(LINK)    |asset                |asset_component_idx                                                         |
|4   |57     |ci     |NOTUNIQUE       |name(STRING)       |asset                |asset_name_ci_idx                                                           |
|5   |58     |default|UNIQUE          |asset_id(LINK)     |browse_node          |browse_node_asset_id_idx                                                    |
|6   |12     |default|NOTUNIQUE       |component_id(LINK) |browse_node          |browse_node_component_id_idx                                                |
|7   |76     |       |UNIQUE          |                   |browse_node          |browse_node_repository_name_parent_path_name_idx                            |
|8   |10     |default|UNIQUE          |repository_name(...|bucket               |bucket_repository_name_idx                                                  |
|9   |12     |       |UNIQUE          |                   |component            |component_bucket_group_name_version_idx                                     |
|10  |12     |       |NOTUNIQUE       |                   |component            |component_bucket_name_version_idx                                           |
|11  |4      |ci     |NOTUNIQUE       |ci_name(STRING)    |component            |component_ci_name_ci_idx                                                    |
|12  |12     |       |NOTUNIQUE       |                   |component            |component_group_name_version_ci_idx                                         |
|13  |0      |       |NOTUNIQUE       |                   |coordinate_downloa...|coordinate_download_count_namespace_name_version_ip_address_idx             |
|14  |0      |       |NOTUNIQUE       |                   |coordinate_downloa...|coordinate_download_count_namespace_name_version_repository_name_idx        |
|15  |0      |       |NOTUNIQUE       |                   |coordinate_downloa...|coordinate_download_count_namespace_name_version_username_idx               |
|16  |0      |       |UNIQUE          |                   |coordinate_downloa...|coordinate_download_count_repository_name_namespace_name_version_date_ip_...|
|17  |0      |       |UNIQUE_HASH_I...|                   |deleted_blob_index   |deleted_blob_index_blobstore_blob_id_idx                                    |
|18  |0      |default|DICTIONARY      |                   |                     |dictionary                                                                  |
|19  |0      |default|UNIQUE          |digest(STRING)     |docker_foreign_layers|docker_foreign_layers_digest_idx                                            |
|20  |0      |default|UNIQUE_HASH_I...|name(STRING)       |OFunction            |OFunction.name                                                              |
|21  |3      |ci     |UNIQUE          |name(STRING)       |ORole                |ORole.name                                                                  |
|22  |3      |ci     |UNIQUE          |name(STRING)       |OUser                |OUser.name                                                                  |
|23  |1      |ci     |UNIQUE          |node_id(STRING)    |statushealthcheck    |statushealthcheck_node_id_idx                                               |
+----+-------+-------+----------------+-------------------+---------------------+----------------------------------------------------------------------------+
|    |447    |       |                |                   |                     |TOTAL                                                                       |
+----+-------+-------+----------------+-------------------+---------------------+----------------------------------------------------------------------------+
orientdb {db=component}>

```



#### 2.1.3 查看bucket表



查询bucket表：

```sql
orientdb {db=component}> select from bucket;

+----+-----+------+---------------+----------+
|#   |@RID |@CLASS|repository_name|attributes|
+----+-----+------+---------------+----------+
|0   |#23:0|bucket|nuget-hosted   |{}        |
|1   |#23:1|bucket|maven-snapshots|{}        |
|2   |#23:2|bucket|nuget.org-proxy|{}        |
|3   |#23:3|bucket|maven-central  |{}        |
|4   |#23:4|bucket|docker-hosted  |{}        |
|5   |#24:0|bucket|nuget-group    |{}        |
|6   |#24:1|bucket|maven-public   |{}        |
|7   |#24:2|bucket|maven-releases |{}        |
|8   |#24:3|bucket|docker-proxy   |{}        |
|9   |#24:4|bucket|docker-group   |{}        |
+----+-----+------+---------------+----------+

10 item(s) found. Query executed in 0.015 sec(s).
```



#### 2.1.4 查看Ouser用户表


```sql
orientdb {db=component}> select from OUser;

+----+----+------+------+------+------+-----------------------------------------------------------------------------------------------------------------+
|#   |@RID|@CLASS|roles |status|name  |password                                                                                                         |
+----+----+------+------+------+------+-----------------------------------------------------------------------------------------------------------------+
|0   |#5:0|OUser |[#4:0]|ACTIVE|admin |{PBKDF2WithHmacSHA256}022C0C79CB77D9DC018FB0B511EA0FD1BDE50BCD83122425:6337B53123456F83EC857DA30718838C41C4E5C...|
|1   |#5:1|OUser |[#4:1]|ACTIVE|reader|{PBKDF2WithHmacSHA256}07973269B341692E08FB5981BA55BCDCE518C4961F1CAE79:BDE1F86ED69121234565AFF63280B99D7AA0B26...|
|2   |#5:2|OUser |[#4:2]|ACTIVE|writer|{PBKDF2WithHmacSHA256}523DBE160CD26092F03AC874548A1519D35E20411BFA2C55:4B2C2F862C04F6D56541234563080537710F87B...|
+----+----+------+------+------+------+-----------------------------------------------------------------------------------------------------------------+

3 item(s) found. Query executed in 0.001 sec(s).
orientdb {db=component}>
```

#### 2.1.5 查看ORole角色表

```sql
orientdb {db=component}> select from ORole;

+----+----+------+----+------+---------+------------------------------------------------------------------------------------------------------------+
|#   |@RID|@CLASS|mode|name  |inherited|rules                                                                                                       |
+----+----+------+----+------+---------+------------------------------------------------------------------------------------------------------------+
|0   |#4:0|ORole |1   |admin |         |{database.bypassRestricted=31}                                                                              |
|1   |#4:1|ORole |0   |reader|         |{database.cluster.internal=2, database.cluster.orole=0, database=2, database.function=2, database.schema=...|
|2   |#4:2|ORole |0   |writer|         |{database.cluster.internal=2, database.class.oschedule=2, database.class.osequence=2, database.class.ouse...|
+----+----+------+----+------+---------+------------------------------------------------------------------------------------------------------------+

3 item(s) found. Query executed in 0.002 sec(s).
```



#### 2.1.6 查看component组件表

```sql
+----+-----+---------+-----+------+------+----------+------------------+------------------+------------------+------------------------------------------------+
|#   |@RID |@CLASS   |group|bucket|format|version   |last_updated      |name              |ci_name           |attributes                                      |
+----+-----+---------+-----+------+------+----------+------------------+------------------+------------------+------------------------------------------------+
|0   |#25:0|component|     |#24:3 |docker|latest    |2024-01-23 22:1...|library/alpine    |library/alpine    |{docker={imageName=library/alpine, imageTag=l...|
|1   |#25:1|component|     |#24:3 |docker|latest    |2024-01-23 22:4...|meizhaohui/meic...|meizhaohui/meic...|{docker={imageName=meizhaohui/meicentos, imag...|
|2   |#25:2|component|     |#24:3 |docker|3.19      |2024-01-24 13:3...|library/alpine    |library/alpine    |{docker={imageName=library/alpine, imageTag=3...|
|3   |#25:3|component|     |#23:4 |docker|hosted    |2024-01-26 13:5...|mysql-client      |mysql-client      |{docker={imageName=mysql-client, imageTag=hos...|
|4   |#25:4|component|     |#24:3 |docker|3.17      |2024-01-27 14:5...|library/alpine    |library/alpine    |{docker={imageName=library/alpine, imageTag=3...|
|5   |#25:5|component|     |#23:4 |docker|push-by...|2024-01-28 08:4...|mysql-client      |mysql-client      |{docker={imageName=mysql-client, imageTag=pus...|
|6   |#26:0|component|     |#24:3 |docker|3.18      |2024-01-23 22:1...|library/alpine    |library/alpine    |{docker={imageName=library/alpine, imageTag=3...|
|7   |#26:1|component|     |#24:3 |docker|latest    |2024-01-23 22:5...|library/redis     |library/redis     |{docker={imageName=library/redis, imageTag=la...|
|8   |#26:2|component|     |#24:3 |docker|3.9       |2024-01-24 13:5...|library/alpine    |library/alpine    |{docker={imageName=library/alpine, imageTag=3...|
|9   |#26:3|component|     |#24:3 |docker|3.16      |2024-01-26 14:1...|library/alpine    |library/alpine    |{docker={imageName=library/alpine, imageTag=3...|
|10  |#26:4|component|     |#24:3 |docker|3.15      |2024-01-27 16:2...|library/alpine    |library/alpine    |{docker={imageName=library/alpine, imageTag=3...|
|11  |#26:5|component|     |#24:3 |docker|3.14      |2024-01-28 09:0...|library/alpine    |library/alpine    |{docker={imageName=library/alpine, imageTag=3...|
+----+-----+---------+-----+------+------+----------+------------------+------------------+------------------+------------------------------------------------+

12 item(s) found. Query executed in 0.01 sec(s).
```

可以看到，都是下城镜像时缓存的文件之类的信息。



### 2.2 数据库config配置库命令行操作

#### 2.2.1 进入到数据库config配置库命令行

进入到数据库命令行：


查询config信息


```sql
# 一定要转到/tmp目录下
bash-4.4$ cd /tmp
bash-4.4$ java -jar /opt/sonatype/nexus/lib/support/nexus-orient-console.jar

OrientDB console v.2.2.36 (build d3beb772c02098ceaea89779a7afd4b7305d3788, branch 2.2.x) https://www.orientdb.com
Type 'help' to display all the supported commands.
orientdb> 

# 登陆db
orientdb {db=component}> connect plocal:/nexus-data/db/config admin admin


Disconnecting from the database [component]...OK
Connecting to database [plocal:/nexus-data/db/config] with user 'admin'...
2024-01-29 22:36:42:533 WARNI {db=config} Storage 'config' was not closed properly. Will try to recover from write ahead log... [OLocalPaginatedStorage]
2024-01-29 22:36:42:534 WARNI {db=config} Record OFuzzyCheckpointStartRecord{lsn=LSN{segment=27, position=59610}} com.orientechnologies.orient.core.storage.impl.local.paginated.wal.OFuzzyCheckpointStartRecord{lsn=null, previousCheckpoint=LSN{segment=27, position=54035}} will be skipped during data restore [OLocalPaginatedStorage]
2024-01-29 22:36:42:534 WARNI {db=config} Record com.orientechnologies.orient.core.storage.impl.local.paginated.wal.OFuzzyCheckpointEndRecord{lsn=LSN{segment=27, position=59650}} will be skipped during data restore [OLocalPaginatedStorage]OK
orientdb {db=config}>
```

#### 2.2.2 查看数据库索引
```sql
orientdb {db=config}> list indexes;

INDEXES
+----+-------------------------------------+-----------------+-------+----------------------+-------+-----------------------+
|#   |NAME                                 |TYPE             |RECORDS|CLASS                 |COLLATE|FIELDS                 |
+----+-------------------------------------+-----------------+-------+----------------------+-------+-----------------------+
|0   |cleanup_format_idx                   |NOTUNIQUE        |0      |cleanup               |default|format(STRING)         |
|1   |cleanup_name_idx                     |UNIQUE           |0      |cleanup               |default|name(STRING)           |
|2   |dictionary                           |DICTIONARY       |3      |                      |default|                       |
|3   |healthcheckconfig_property_name_idx  |UNIQUE           |0      |healthcheckconfig     |ci     |property_name(STRING)  |
|4   |key_store_name_idx                   |UNIQUE           |2      |key_store             |default|name(STRING)           |
|5   |ldap_id_idx                          |UNIQUE           |0      |ldap                  |default|id(STRING)             |
|6   |ldap_name_idx                        |UNIQUE           |0      |ldap                  |default|name(STRING)           |
|7   |OFunction.name                       |UNIQUE_HASH_INDEX|0      |OFunction             |default|name(STRING)           |
|8   |ORole.name                           |UNIQUE           |3      |ORole                 |ci     |name(STRING)           |
|9   |OUser.name                           |UNIQUE           |3      |OUser                 |ci     |name(STRING)           |
|10  |quartz_calendar_name_idx             |UNIQUE           |0      |quartz_calendar       |default|name(STRING)           |
|11  |quartz_job_detail_name_group_idx     |UNIQUE           |3      |quartz_job_detail     |       |                       |
|12  |quartz_trigger_calendar_name_idx     |NOTUNIQUE        |1      |quartz_trigger        |default|calendar_name(STRING)  |
|13  |quartz_trigger_job_name_job_group_idx|NOTUNIQUE        |3      |quartz_trigger        |       |                       |
|14  |quartz_trigger_name_group_idx        |UNIQUE           |3      |quartz_trigger        |       |                       |
|15  |quartz_trigger_state_idx             |NOTUNIQUE        |1      |quartz_trigger        |default|state(STRING)          |
|16  |repository_blobstore_name_idx        |UNIQUE           |2      |repository_blobstore  |ci     |name(STRING)           |
|17  |repository_repository_name_idx       |UNIQUE           |10     |repository            |ci     |repository_name(STRING)|
|18  |repository_routingrule_name_idx      |UNIQUE           |0      |repository_routingrule|default|name(STRING)           |
|19  |script_name_idx                      |UNIQUE           |0      |script                |default|name(STRING)           |
|20  |selector_selector_name_idx           |UNIQUE           |0      |selector_selector     |default|name(STRING)           |
+----+-------------------------------------+-----------------+-------+----------------------+-------+-----------------------+
|    |TOTAL                                |                 |34     |                      |       |                       |
+----+-------------------------------------+-----------------+-------+----------------------+-------+-----------------------+
orientdb {db=config}>
```



#### 2.2.3 查看repository仓库表

```sql
orientdb {db=config}> select from repository;


+----+-----+---------+------+---------+---------+---------+---------------------------------------------------------------------------------------------+
|#   |@RID |@CLASS   |online|recipe_na|routingRu|repositor|attributes                                                                                   |
+----+-----+---------+------+---------+---------+---------+---------------------------------------------------------------------------------------------+
|0   |#17:0|reposi...|true  |nuget-...|         |nuget-...|{storage={writePolicy=ALLOW, blobStoreName=default}}                                         |
|1   |#17:1|reposi...|true  |nuget-...|         |nuget-...|{group={memberNames=[nuget-hosted, nuget.org-proxy]}, storage={blobStoreName=default}}       |
|2   |#17:2|reposi...|true  |maven2...|         |maven-...|{maven={contentDisposition=INLINE, versionPolicy=SNAPSHOT, layoutPolicy=STRICT}, storage={...|
|3   |#17:3|reposi...|true  |maven2...|         |maven-...|{maven={versionPolicy=MIXED}, group={memberNames=[maven-releases, maven-snapshots, maven-c...|
|4   |#17:4|reposi...|true  |docker...|         |docker...|{component={proprietaryComponents=false}, docker={forceBasicAuth=false, httpPort=8002.0, v...|
|5   |#18:0|reposi...|true  |nuget-...|         |nuget....|{proxy={strictContentTypeValidation=true, contentMaxAge=1440, remoteUrl=https://api.nuget....|
|6   |#18:1|reposi...|true  |maven2...|         |maven-...|{maven={contentDisposition=INLINE, versionPolicy=RELEASE, layoutPolicy=STRICT}, storage={w...|
|7   |#18:2|reposi...|true  |maven2...|         |maven-...|{proxy={contentMaxAge=-1, remoteUrl=https://repo1.maven.org/maven2/, metadataMaxAge=1440},...|
|8   |#18:3|reposi...|true  |docker...|         |docker...|{replication={preemptivePullEnabled=false}, proxy={contentMaxAge=1440.0, remoteUrl=https:/...|
|9   |#18:4|reposi...|true  |docker...|         |docker...|{docker={forceBasicAuth=false, httpPort=8003.0, v1Enabled=true}, storage={strictContentTyp...|
+----+-----+---------+------+---------+---------+---------+---------------------------------------------------------------------------------------------+

10 item(s) found. Query executed in 0.007 sec(s).
orientdb {db=config}>
```



#### 2.2.4 查看repository_blobstore仓库blob存储表

```sql
orientdb {db=config}> select from repository_blobstore;


+----+-----+--------------------+-------+----+---------------------------------------------+
|#   |@RID |@CLASS              |name   |type|attributes                                   |
+----+-----+--------------------+-------+----+---------------------------------------------+
|0   |#19:0|repository_blobstore|default|File|{file={path=default}}                        |
|1   |#20:0|repository_blobstore|docker |File|{file={path=docker}, blobStoreQuotaConfig={}}|
+----+-----+--------------------+-------+----+---------------------------------------------+

2 item(s) found. Query executed in 0.005 sec(s).
orientdb {db=config}>
```

可以看到，表里面的信息相对复杂。如果我们想自动化设置Nexus上面的仓库信息，需要修改repository和repository_blobstore表。



此处不再详细查看每个表信息。