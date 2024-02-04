# unarchive模块
[[toc]]

## 1. 概要

- `unarchive`模块用于对归档文件进行解压。 
- 默认情况下，它会在解包之前将源文件从本地系统复制到目标系统。
- 如果设置`remote_src=yes`则表示解压远程主机上面的归档文件。 
- 如果需要校验文件,请使用`get_url`[https://docs.ansible.com/ansible/2.9/modules/get_url_module.html#get-url-module](https://docs.ansible.com/ansible/2.9/modules/get_url_module.html#get-url-module)或`url`[https://docs.ansible.com/ansible/2.9/modules/uri_module.html#uri-module](https://docs.ansible.com/ansible/2.9/modules/uri_module.html#uri-module)模块，而不是`fetch`模块来获取文件，并且设置`remote_src=yes`。
- 官方文档：[https://docs.ansible.com/ansible/latest/collections/ansible/builtin/unarchive_module.html#ansible-collections-ansible-builtin-unarchive-module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/unarchive_module.html#ansible-collections-ansible-builtin-unarchive-module) 或 [https://docs.ansible.com/ansible/2.9/modules/unarchive_module.html](https://docs.ansible.com/ansible/2.9/modules/unarchive_module.html)



::: warning 注意
    Requires zipinfo and gtar/unzip command on target host.

    Requires zstd command on target host to expand .tar.zst files.

    Can handle .zip files using unzip as well as .tar, .tar.gz, .tar.bz2, .tar.xz, and .tar.zst files using gtar.

    Does not handle .gz files, .bz2 files, .xz, or .zst files that do not contain a .tar archive.

    Existing files/directories in the destination which are not in the archive are not touched. This is the same behavior as a normal archive extraction.

    Existing files/directories in the destination which are not in the archive are ignored for purposes of deciding if the archive should be unpacked or not.

:::

即：

::: warning 注意
- 远程主机需要有`zipinfo`、`gtar`、`unzip`等命令。
- 对于扩展是 `.tar.zst` 的归档文件，则需要 `zstd` 命令。
- 使用 `unzip` 命令处理 `.zip` 压缩包。
- 使用 `gtar` 命令处理 .tar, .tar.gz, .tar.bz2, .tar.xz, and .tar.zst 等类型的压缩包。
- 不处理不包含 `.tar` 归档的 `.gz`、`.bz2` 、 `.xz` 或 `.zst` 等文件。
- 目标中不在存档中的现有文件/目录不会被创建。这与正常的存档提取行为相同。
- 目标中不在存档中的现有文件/目录将被忽略，以便决定是否应解压缩存档。
:::



## 2. 参数

| 参数                     | 可选值 | 默认值 | 说明                                                         |
| ------------------------ | ------ | ------ | ------------------------------------------------------------ |
| `attributes`             |        |        | `string`，文件最终的属性 |
| `copy`             | `true`、`false`       |  `true`      | `boolean`，是否从Ansible主机复制归档文件到远程主机。已经废弃，请使用`remote_src`参数 |
| `remote_src`             | `true`、`false`       |  `false`      | `boolean`，归档文件是否在远程主机上，而不是在Ansible主机上|
| `creates`             |        |      | `path`，如果指定的绝对路径（文件或目录）已经存在，则不会运行此步骤。指定的绝对路径（文件或目录）必须低于`dest`给定的基本路径 |
| `decrypt`             | `true`、`false`       |  `false`      | `boolean`，此选项控制使用vault自动解密源文件。|
| `dest`             |        |      | `path`，必须字段，解压后文件存放的路径。本模块不会自动创建基础目录 |
| `src`             |        |      | `path`，必须字段，归档文件目录。默认情况下`remote_src=no`，从Ansible主机上复制归档文件到远程主机。如果`remote_src=yes`，则远程主机上的归档文件需要存在。当归档文件设置为远程主机上时，如果`src`包含URL地址，则会先去下载文件，然后再解压 |
| `exclude`             |        |   `[]`   | `list`/`elements=string`，列出您要从取消归档操作中排除的目录和文件项。与`include`互斥|
| `extra_opts`             |        |   `[]`   | `list`/`elements=string`,指定其他选项。|
| `include`             |        |   `[]`   | `list`/`elements=string`，要从存档中提取的目录和文件项的列表。如果include不为空，则只提取此处列出的文件。与`exclude`互斥|
| `keep_newer`             | `true`、`false`       |  `false`      | `boolean`，解压时不替换比归档文件中还新的已经存在的文件|
| `list_files`             | `true`、`false`       |  `false`      | `boolean`，列出归档文件中包含哪些文件|
| `io_buffer_size`             |       |  65536      | `integer`，用于从存档中提取文件的内存缓冲区的大小（以字节为单位）|
| `validate_certs`             | `true`、`false`       |  `true`      | `boolean`，如果从URL下载归档文件时，是否进行证书校验。对于自签名证书的网站，此处应设置为`false`|
| `owner`、`group`、`mode`             |       |       | 设置文件最终的用户属主、用户组、模式等信息|


## 3. 官方示例

```yaml
- name: Extract foo.tgz into /var/lib/foo
  ansible.builtin.unarchive:
    src: foo.tgz
    dest: /var/lib/foo

- name: Unarchive a file that is already on the remote machine
  ansible.builtin.unarchive:
    src: /tmp/foo.zip
    dest: /usr/local/bin
    remote_src: yes

- name: Unarchive a file that needs to be downloaded (added in 2.0)
  ansible.builtin.unarchive:
    src: https://example.com/example.zip
    dest: /usr/local/bin
    remote_src: yes

- name: Unarchive a file with extra options
  ansible.builtin.unarchive:
    src: /tmp/foo.zip
    dest: /usr/local/bin
    extra_opts:
    - --transform
    - s/^xxx/yyy/
```


## 4. 剧本的使用

### 4.1 从远程下载tomcat

编写剧本文件unarchive.yml：
```yaml
- hosts: node1
  tasks:
    - name: create base folder
      ansible.builtin.file:
        path: /srv/tomcat
        state: directory
      become: yes

    - name: Unarchive a file that needs to be downloaded (added in 2.0)
      ansible.builtin.unarchive:
        src: https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.73/bin/apache-tomcat-9.0.73.tar.gz
        dest: /srv/tomcat
        validate_certs: no
        remote_src: yes
      become: yes
```

检查并执行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-lint unarchive.yml
[ansible@master ansible_playbooks]$ ansible-playbook unarchive.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [create base folder] **********************************************************************************************
ok: [node1] => {"changed": false, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/srv/tomcat", "size": 4096, "state": "directory", "uid": 0}

TASK [Unarchive a file that needs to be downloaded (added in 2.0)] *****************************************************
changed: [node1] => {"changed": true, "dest": "/srv/tomcat", "extract_results": {"cmd": ["/bin/gtar", "--extract", "-C", "/srv/tomcat", "-z", "-f", "/home/ansible/.ansible/tmp/ansible-tmp-1680016802.82-22786-277884550702385/apache-tomcat-9.0.73.tar0iQ883.gz"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 4096, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1680016802.82-22786-277884550702385/apache-tomcat-9.0.73.tar0iQ883.gz", "state": "directory", "uid": 0}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到执行成功。

在节点上也可以看到解压好的tomcat文件：
```sh
[root@node1 ~]# ll /srv/tomcat/
total 4
drwxr-xr-x 9 root root 4096 Mar 28 23:26 apache-tomcat-9.0.73
[root@node1 ~]# ll /srv/tomcat/apache-tomcat-9.0.73/
total 148
drwxr-x--- 2 root root  4096 Mar 28 23:26 bin
-rw-r----- 1 root root 19992 Feb 27 23:33 BUILDING.txt
drwx------ 2 root root  4096 Feb 27 23:33 conf
-rw-r----- 1 root root  6210 Feb 27 23:33 CONTRIBUTING.md
drwxr-x--- 2 root root  4096 Mar 28 23:26 lib
-rw-r----- 1 root root 57092 Feb 27 23:33 LICENSE
drwxr-x--- 2 root root  4096 Feb 27 23:33 logs
-rw-r----- 1 root root  2333 Feb 27 23:33 NOTICE
-rw-r----- 1 root root  3398 Feb 27 23:33 README.md
-rw-r----- 1 root root  6901 Feb 27 23:33 RELEASE-NOTES
-rw-r----- 1 root root 16505 Feb 27 23:33 RUNNING.txt
drwxr-x--- 2 root root  4096 Mar 28 23:26 temp
drwxr-x--- 7 root root  4096 Feb 27 23:33 webapps
drwxr-x--- 2 root root  4096 Feb 27 23:33 work
[root@node1 ~]#
```

### 4.2 从ansible主机复制tomcat包

当有多个远程主机需要从网站上下载压缩包的话，就显得比较浪费时间，我们可以先将压缩包下载到Ansible主机，然后再从Ansible主机分发到各个远程主机上，这样就可以不用重复下载，加快剧本执行速度。

我们优化一下以上剧本文件。

先下载tomcat压缩包，然后在远程主机解压，并启动tomcat:

```yaml
- hosts: node1
  tasks:
    - name: Download tomcat file
      ansible.builtin.get_url:
        url: https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.73/bin/apache-tomcat-9.0.73.tar.gz
        dest: /home/ansible/ansible_playbooks/files/apache-tomcat-9.0.73.tar.gz
        validate_certs: no
      # 由Ansible主机代理，即直接下载到Ansible主机上
      delegate_to: 127.0.0.1

    - name: create base folder
      ansible.builtin.file:
        path: /srv/tomcat
        state: directory
      become: yes

    - name: Extract apache-tomcat-9.0.73.tar.gz into /srv/tomcat
      ansible.builtin.unarchive:
        src: /home/ansible/ansible_playbooks/files/apache-tomcat-9.0.73.tar.gz
        dest: /srv/tomcat
      become: yes

    - name: Start tomcat server
      shell: nohup ./startup.sh &
      args:
        chdir: /srv/tomcat/apache-tomcat-9.0.73/bin
      become: yes
      # [301] Commands should not change things if nothing needs doing
      register: myoutput
      changed_when: myoutput.rc != 0

    - name: Wait for port 8080 to become open on the host
      wait_for:
        port: 8080
        delay: 5
        timeout: 10
      become: yes
```

执行剧本文件：
```sh
[ansible@master ansible_playbooks]$ ansible-playbook unarchive_local.yml  -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Download tomcat file] ********************************************************************************************
ok: [node1 -> 127.0.0.1] => {"changed": false, "dest": "/home/ansible/ansible_playbooks/files/apache-tomcat-9.0.73.tar.gz", "elapsed": 0, "gid": 1002, "group": "ansible", "mode": "0664", "msg": "HTTP Error 304: Not Modified", "owner": "ansible", "size": 11625808, "state": "file", "uid": 1002, "url": "https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.73/bin/apache-tomcat-9.0.73.tar.gz"}

TASK [create base folder] **********************************************************************************************
changed: [node1] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/srv/tomcat", "size": 4096, "state": "directory", "uid": 0}

TASK [Extract apache-tomcat-9.0.73.tar.gz into /srv/tomcat] ************************************************************
changed: [node1] => {"changed": true, "dest": "/srv/tomcat", "extract_results": {"cmd": ["/bin/gtar", "--extract", "-C", "/srv/tomcat", "-z", "-f", "/home/ansible/.ansible/tmp/ansible-tmp-1680186620.1-1089-66455494262879/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 4096, "src": "/home/ansible/.ansible/tmp/ansible-tmp-1680186620.1-1089-66455494262879/source", "state": "directory", "uid": 0}

TASK [Start tomcat server] *********************************************************************************************
changed: [node1] => {"changed": true, "cmd": "nohup ./startup.sh &", "delta": "0:00:00.036106", "end": "2023-03-30 22:30:21.938376", "rc": 0, "start": "2023-03-30 22:30:21.902270", "stderr": "", "stderr_lines": [], "stdout": "Tomcat started.", "stdout_lines": ["Tomcat started."]}

TASK [Wait for port 8080 to become open on the host] *******************************************************************
ok: [node1] => {"changed": false, "elapsed": 5, "match_groupdict": {}, "match_groups": [], "path": null, "port": 8080, "search_regex": null, "state": "started"}

PLAY RECAP *************************************************************************************************************
node1                      : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到远程主机tomcat启动了。在节点上面检查一下：

```sh
[root@node1 ~]# ps -ef|grep tomcat
root     22431     1  1 22:30 ?        00:00:02 //bin/java -Djava.util.logging.config.file=/srv/tomcat/apache-tomcat-9.0.73/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djdk.tls.ephemeralDHKeySize=2048 -Djava.protocol.handler.pkgs=org.apache.catalina.webresources -Dorg.apache.catalina.security.SecurityListener.UMASK=0027 -Dignore.endorsed.dirs= -classpath /srv/tomcat/apache-tomcat-9.0.73/bin/bootstrap.jar:/srv/tomcat/apache-tomcat-9.0.73/bin/tomcat-juli.jar -Dcatalina.base=/srv/tomcat/apache-tomcat-9.0.73 -Dcatalina.home=/srv/tomcat/apache-tomcat-9.0.73 -Djava.io.tmpdir=/srv/tomcat/apache-tomcat-9.0.73/temp org.apache.catalina.startup.Bootstrap start
root     23133 13800  0 22:32 pts/0    00:00:00 grep --color=auto tomcat
[root@node1 ~]# netstat -tunlp|grep 8080
tcp6       0      0 :::8080                 :::*                    LISTEN      22431/java
[root@node1 ~]#
```

可以看到，tomcat成功启动了！！
