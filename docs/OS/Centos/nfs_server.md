# CentOS7搭建NFS服务器

[[toc]]

测试主机信息：

| 主机信息 | 操作系统 | IP             |
| -------- | -------- | -------------- |
| 服务端   | CentOS7  | 192.168.56.101 |
| 客户端   | CentOS7  | 192.168.56.102 |




## 1. NFS Server服务端配置



### 1.1 安装包

```sh
# yum install nfs-utils -y
Loaded plugins: fastestmirror, langpacks
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package nfs-utils.x86_64 1:1.3.0-0.68.el7.2 will be installed
,,, 省略
Installed:
  nfs-utils.x86_64 1:1.3.0-0.68.el7.2

Dependency Installed:
  gssproxy.x86_64 0:0.7.0-30.el7_9       keyutils.x86_64 0:1.5.8-3.el7 libbasicobjects.x86_64 0:0.1.1-32.el7 libcollection.x86_64 0:0.7.0-32.el7 libini_config.x86_64 0:1.3.1-32.el7 libnfsidmap.x86_64 0:0.25-19.el7 libpath_utils.x86_64 0:0.2.1-32.el7 libref_array.x86_64 0:0.1.5-32.el7
  libverto-libevent.x86_64 0:0.2.5-4.el7 quota.x86_64 1:4.01-19.el7    rpcbind.x86_64 0:0.2.0-49.el7

Complete!
#
```



### 1.2 启动服务

```sh
# 启动服务
# systemctl start rpcbind nfs

# 设置开机启动
# systemctl enable rpcbind nfs
Created symlink from /etc/systemd/system/multi-user.target.wants/nfs-server.service to /usr/lib/systemd/system/nfs-server.service.

# 查看服务状态
# systemctl status rpcbind nfs
● rpcbind.service - RPC bind service
   Loaded: loaded (/usr/lib/systemd/system/rpcbind.service; enabled; vendor preset: enabled)
   Active: active (running) since Sat 2023-12-09 13:11:26 CST; 22s ago
 Main PID: 24318 (rpcbind)
   CGroup: /system.slice/rpcbind.service
           └─24318 /sbin/rpcbind -w


Dec 09 13:11:26 systemd[1]: Starting RPC bind service...
Dec 09 13:11:26 systemd[1]: Started RPC bind service.

● nfs-server.service - NFS server and services
   Loaded: loaded (/usr/lib/systemd/system/nfs-server.service; enabled; vendor preset: disabled)
   Active: active (exited) since Sat 2023-12-09 13:11:27 CST; 30s ago
 Main PID: 24348 (code=exited, status=0/SUCCESS)
   CGroup: /system.slice/nfs-server.service

Dec 09 13:11:27 systemd[1]: Starting NFS server and services...
Dec 09 13:11:27 systemd[1]: Started NFS server and services.
```

### 1.3 修改配置文件/etc/exports

配置文件/etc/exports 用于设置哪些目录可以共享给哪些客户端。

```sh
/home/reader/source 192.168.56.102(rw,sync,no_root_squash,no_all_squash)
```

将以上内容加入到`/etc/exports`文件中，然后查看文件内容：

```sh
# cat /etc/exports
/home/reader/source 192.168.56.102(rw,sync,no_root_squash,no_all_squash)

#
```

配置参数说明：

- /home/reader/source: 共享目录位置
- 192.168.56.102: 客户端IP范围, *代表所有，即没有限制
- rw: 权限设置，可读可写
- sync: 同步共享目录
- no_root_squash: 可以使用root授权
- no_all_squash: 可以使用普通用户授权



### 1.4 重启服务

```sh
# systemctl restart rpcbind nfs
# systemctl status rpcbind nfs|grep active
   Active: active (running) since Sat 2023-12-09 13:22:23 CST; 15s ago
   Active: active (exited) since Sat 2023-12-09 13:22:23 CST; 15s ago
  Process: 27595 ExecStartPost=/bin/sh -c if systemctl -q is-active gssproxy; then systemctl reload gssproxy ; fi (code=exited, status=0/SUCCESS)
```



### 1.5 检测本地的共享目录

```sh
# showmount -e localhost
Export list for localhost:
/home/reader/source 192.168.56.102
```

可以看到共享目录已经配置成功。





## 2. NFS Client客户端配置

像服务端一样安装`nfs-utils`包并启动服务：

```sh
# 安装包
# yum install nfs-utils -y

# 启动服务
# systemctl start rpcbind nfs

# 设置开机启动
# systemctl enable rpcbind nfs

# 查看服务状态
# systemctl status rpcbind nfs
```



### 2.1 创建挂载点

```sh
# 创建挂载点
# mkdir -p /home/reader/source

# 查看并修改挂载点目录权限
# ll /home/reader/
total 4
drwxr-xr-x 2 root root 4096 Dec  9 13:40 source
# chown reader. source/
# ll /home/reader/
total 4
drwxr-xr-x 2 reader reader 4096 Dec  9 13:40 source
```



### 2.2 挂载共享目录

```sh
# mount -t nfs -o rw,timeo=2,soft 192.168.56.101:/home/reader/source /home/reader/source
```



### 2.3 查看挂载信息

```sh
# df -h /home/reader/source
Filesystem                    Size  Used Avail Use% Mounted on
192.168.56.101:/home/reader/source   59G   46G   11G  82% /home/reader/source
```

可以看到挂载成功。

### 2.4 测试文件共享

在服务端创建目录和文件：

```sh
# su - reader
Last login: Sat Dec  9 13:52:49 CST 2023 on pts/0
[reader@nfs-seerver ~]$ cd source/
[reader@nfs-seerver source]$ ll
total 0
[reader@nfs-seerver source]$ mkdir data
[reader@nfs-seerver source]$ echo 's1' > data/test1.txt
[reader@nfs-seerver source]$ ll
total 4
drwxrwxr-x 2 reader reader 4096 Dec  9 13:55 data
[reader@nfs-seerver source]$ ll data
total 4
-rw-rw-r-- 1 reader reader 3 Dec  9 13:55 test1.txt
```

客户端查看共享文件，并尝试写人文件：

```sh
# su - reader
[reader@nfs-client ~]$ cd source/
[reader@nfs-client source]$ ll
total 4
drwxrwxr-x 2 1004 1004 4096 Dec  9 13:55 data
[reader@nfs-client source]$ ll data
total 4
-rw-rw-r-- 1 1004 1004 3 Dec  9 13:55 test1.txt
[reader@nfs-client source]$ echo 's2' >> data/test1.txt
-bash: data/test1.txt: Permission denied
[reader@nfs-client source]$
```

可以看到：

- 显示的共享文件的`UID:GID`是`1004:1004`，而不是显示`reader:reader`。
- 写人文件时提示`Permission denied`权限拒绝。

出现这种情况是因为在服务端和客户端用户的`UID、GID`信息不一致。



查看服务端`reader`的ID信息：

```sh
[reader@nfs-seerver ~]$ id
uid=1004(reader) gid=1004(reader) groups=1004(reader)
```

查看客户端`reader`的ID信息：

```sh
[reader@nfs-client ~]$ id
uid=1003(reader) gid=1003(reader) groups=1003(reader)
```

参考：[nfs permissions problems/same username different uid/gid](https://bbs.archlinux.org/viewtopic.php?id=67418)

> Make the uid/gid match the user ON THE SERVER and add the 'all_squash' option.
>
> Here is my /etc/exports on the **server**:
>
> ```
> /share    192.168.1.2(rw,all_squash,anonuid=100,anongid=102)
> ```
>
> Now I can rw to the nfs share... the owner still appears as 100:102 but oh well.

我这边这应该这么修改：

```sh
[root@nfs-server ~]# cat /etc/exports
/home/reader/source 192.168.56.102(rw,sync,all_squash,anonuid=1004,anongid=1004)
```

 参数说明：

- all_squash：将远程访问的所有普通用户及所属组都映射为匿名用户或用户组（nobody）。
- anonuid： 将远程访问的所有用户都映射为匿名用户，并指定该用户为本地用户（UID=xxx） 。
- anongid： 将远程访问的所有用户组都映射为匿名用户组账户，并指定该匿名用户组账户为本地用户组账户（GID=xxx） 。



此处的`anonuid=1004,anongid=1004`对应的uid=1004和gid=1004就是我们服务端reader对应的uid他gid。



客户端再重启服务：

```sh
# systemctl restart rpcbind nfs
```



重新测试。

现在服务端新建文件和文件夹：

```sh
[root@nfs-server ~]# cd /home/reader/source/
[root@nfs-server source]# ll
total 0
[root@nfs-server source]# su - reader
Last login: Sat Dec  9 22:38:16 CST 2023 on pts/0
[reader@nfs-seerver ~]$ cd source/
[reader@nfs-seerver source]$ mkdir a b c
[reader@nfs-seerver source]$ touch a1 b1 c1
[reader@nfs-seerver source]$ ll
total 12
drwxrwxr-x 2 reader reader 4096 Dec  9 22:56 a
-rw-rw-r-- 1 reader reader    0 Dec  9 22:57 a1
drwxrwxr-x 2 reader reader 4096 Dec  9 22:56 b
-rw-rw-r-- 1 reader reader    0 Dec  9 22:57 b1
drwxrwxr-x 2 reader reader 4096 Dec  9 22:56 c
-rw-rw-r-- 1 reader reader    0 Dec  9 22:57 c1
[reader@nfs-seerver source]$
```

可以看到是我们想使用的`reader`账号。



再在客户端进行查看：

```sh
[root@nfs-client source]# su - reader
Last login: Sat Dec  9 22:38:27 CST 2023 on pts/0
[reader@nfs-client ~]$ cd source/
[reader@nfs-client source]$ ll
total 12
drwxrwxr-x 2 nobody nobody 4096 Dec  9 22:56 a
-rw-rw-r-- 1 nobody nobody    0 Dec  9 22:57 a1
drwxrwxr-x 2 nobody nobody 4096 Dec  9 22:56 b
-rw-rw-r-- 1 nobody nobody    0 Dec  9 22:57 b1
drwxrwxr-x 2 nobody nobody 4096 Dec  9 22:56 c
-rw-rw-r-- 1 nobody nobody    0 Dec  9 22:57 c1
[reader@nfs-client source]$
```

此时，在客户端都显示的是`nobody:nobody`。



尝试写文件：

```sh
[reader@nfs-client source]$ mkdir d e f
[reader@nfs-client source]$ echo 'a1' >> a1
[reader@nfs-client source]$ echo 'b1' >> b1
[reader@nfs-client source]$ echo 'c1' >> c1
[reader@nfs-client source]$ echo 'd1' >> d1
[reader@nfs-client source]$ echo 'e1' >> e1
[reader@nfs-client source]$ ll
total 44
drwxrwxr-x 2 nobody nobody 4096 Dec  9 22:56 a
-rw-rw-r-- 1 nobody nobody    3 Dec  9 23:00 a1
drwxrwxr-x 2 nobody nobody 4096 Dec  9 22:56 b
-rw-rw-r-- 1 nobody nobody    3 Dec  9 23:00 b1
drwxrwxr-x 2 nobody nobody 4096 Dec  9 22:56 c
-rw-rw-r-- 1 nobody nobody    3 Dec  9 23:00 c1
drwxrwxr-x 2 nobody nobody 4096 Dec  9 23:00 d
-rw-rw-r-- 1 nobody nobody    3 Dec  9 23:00 d1
drwxrwxr-x 2 nobody nobody 4096 Dec  9 23:00 e
-rw-rw-r-- 1 nobody nobody    3 Dec  9 23:00 e1
drwxrwxr-x 2 nobody nobody 4096 Dec  9 23:00 f
[reader@nfs-client source]$
```

可以看到能够正常写入。



此时在服务端检查一下：

```sh
[reader@nfs-seerver source]$ ll
total 44
drwxrwxr-x 2 reader reader 4096 Dec  9 22:56 a
-rw-rw-r-- 1 reader reader    3 Dec  9 23:00 a1
drwxrwxr-x 2 reader reader 4096 Dec  9 22:56 b
-rw-rw-r-- 1 reader reader    3 Dec  9 23:00 b1
drwxrwxr-x 2 reader reader 4096 Dec  9 22:56 c
-rw-rw-r-- 1 reader reader    3 Dec  9 23:00 c1
drwxrwxr-x 2 reader reader 4096 Dec  9 23:00 d
-rw-rw-r-- 1 reader reader    3 Dec  9 23:00 d1
drwxrwxr-x 2 reader reader 4096 Dec  9 23:00 e
-rw-rw-r-- 1 reader reader    3 Dec  9 23:00 e1
drwxrwxr-x 2 reader reader 4096 Dec  9 23:00 f
[reader@nfs-seerver source]$ cat a1
a1
[reader@nfs-seerver source]$ cat b1
b1
[reader@nfs-seerver source]$ cat c1
c1
[reader@nfs-seerver source]$ cat d1
d1
[reader@nfs-seerver source]$ cat e1
e1
[reader@nfs-seerver source]$
```

可以看到，客户端的数据正常在服务端显示出来了。



通过这种方式可以在NFS客户端进行正常的文件读写操作，并且在NFS服务端也能够正常显示文件权限信息。唯一的缺陷是在客户端上面显示的文件所属者和文件所属组是`nobody:nobody`。



### 2.5 其他说明

可以通过`usermod`和`groupmod`来修改用户的UID他GID信息：

```sh
[root@node1 ~]# usermod --help
Usage: usermod [options] LOGIN

Options:
  -c, --comment COMMENT         new value of the GECOS field
  -d, --home HOME_DIR           new home directory for the user account
  -e, --expiredate EXPIRE_DATE  set account expiration date to EXPIRE_DATE
  -f, --inactive INACTIVE       set password inactive after expiration
                                to INACTIVE
  -g, --gid GROUP               force use GROUP as new primary group
  -G, --groups GROUPS           new list of supplementary GROUPS
  -a, --append                  append the user to the supplemental GROUPS
                                mentioned by the -G option without removing
                                the user from other groups
  -h, --help                    display this help message and exit
  -l, --login NEW_LOGIN         new value of the login name
  -L, --lock                    lock the user account
  -m, --move-home               move contents of the home directory to the
                                new location (use only with -d)
  -o, --non-unique              allow using duplicate (non-unique) UID
  -p, --password PASSWORD       use encrypted password for the new password
  -R, --root CHROOT_DIR         directory to chroot into
  -P, --prefix PREFIX_DIR       prefix directory where are located the /etc/* files
  -s, --shell SHELL             new login shell for the user account
  -u, --uid UID                 new UID for the user account
  -U, --unlock                  unlock the user account
  -v, --add-subuids FIRST-LAST  add range of subordinate uids
  -V, --del-subuids FIRST-LAST  remove range of subordinate uids
  -w, --add-subgids FIRST-LAST  add range of subordinate gids
  -W, --del-subgids FIRST-LAST  remove range of subordinate gids
  -Z, --selinux-user SEUSER     new SELinux user mapping for the user account

[root@node1 ~]# groupmod --help
Usage: groupmod [options] GROUP

Options:
  -g, --gid GID                 change the group ID to GID
  -h, --help                    display this help message and exit
  -n, --new-name NEW_GROUP      change the name to NEW_GROUP
  -o, --non-unique              allow to use a duplicate (non-unique) GID
  -p, --password PASSWORD       change the password to this (encrypted)
                                PASSWORD
  -R, --root CHROOT_DIR         directory to chroot into
  -P, --prefix PREFIX_DIR       prefix directory where are located the /etc/* files
```

在系统部署时，没有运行很多服务的时候可以使用`usermod`和`groupmod`来修改用户ID信息，后期就不建议修改了，因为改变用户UID和GID会对运行的服务产生影响。





## 3. NFS参数说明

- 访问权限选项
    - 设置输出目录只读：`ro`
    - 设置输出目录读写：`rw`

 

- 用户映射选项
  - all_squash：将远程访问的所有普通用户及所属组都映射为匿名用户或用户组（nobody
  - no_all_squash：与all_squash取反（默认设置）
  - root_squash：将root用户及所属组都映射为匿名用户或用户组（默认设置）
  - no_root_squash：与rootsquash取反
  - anonuid=xxx：将远程访问的所有用户都映射为匿名用户，并指定该用户为本地用户（UID=xxx）
  - anongid=xxx：将远程访问的所有用户组都映射为匿名用户组账户，并指定该匿名用户组账户为本地用户组账户（GID=xxx）

 

- 其它选项
  - secure：限制客户端只能从小于1024的tcp/ip端口连接nfs服务器（默认设置）
  - insecure：允许客户端从大于1024的tcp/ip端口连接服务器
  - sync：将数据同步写入内存缓冲区与磁盘中，效率低，但可以保证数据的一致性
  - async：将数据先保存在内存缓冲区中，必要时才写入磁盘
  - wdelay：检查是否有相关的写操作，如果有则将这些写操作一起执行，这样可以提高效率（默认设置）
  - no_wdelay：若有写操作则立即执行，应与sync配合使用
  - subtree：若输出目录是一个子目录，则nfs服务器将检查其父目录的权限(默认设置)
  - no_subtree：即使输出目录是一个子目录，nfs服务器也不检查其父目录的权限，这样可以提高效率。