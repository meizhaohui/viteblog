# filter过滤器

[[toc]]

## 1. 过滤器概述

- Ansible有非常多的过滤器，详细可参考：[Filter Plugins](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#filter-plugins)
- Ansible使用Jinja2标准过滤器，并增加了一些Ansible特有的过滤器，可参考[Filter plugins](https://docs.ansible.com/ansible/latest/plugins/filter.html)，你也可以自定义过滤器，请参考[create custom Ansible filters as plugins](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#filter-plugins)。
- Jinja2内置过滤器也有很多，详细可参考[List of Builtin Filters](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters)

![](/img/Snipaste_2023-10-01_23-03-22.png)

以下列出Ansible官方文档列出的过滤器：

- b64decode filter – Decode a base64 string
- b64encode filter – Encode a string as base64
- basename filter – get a path’s base name
- bool filter – cast into a boolean
- checksum filter – checksum of input data
- combinations filter – combinations from the elements of a list
- combine filter – combine two dictionaries
- comment filter – comment out a string
- commonpath filter – gets the common path
- dict2items filter – Convert a dictionary into an itemized list of dictionaries
- difference filter – the difference of one list from another
- dirname filter – get a path’s directory name
- expanduser filter – Returns a path with ~ translation.
- expandvars filter – expand environment variables
- extract filter – extract a value based on an index or key
- fileglob filter – explode a path glob to matching files
- flatten filter – flatten lists within a list
- from_json filter – Convert JSON string into variable structure
- from_yaml filter – Convert YAML string into variable structure
- from_yaml_all filter – Convert a series of YAML documents into a variable structure
- hash filter – hash of input data
- human_readable filter – Make bytes/bits human readable
- human_to_bytes filter – Get bytes from string
- intersect filter – intersection of lists
- items2dict filter – Consolidate a list of itemized dictionaries into a dictionary
- log filter – log of (math operation)
- mandatory filter – make a variable’s existance mandatory
- md5 filter – MD5 hash of input data
- normpath filter – Normalize a pathname
- password_hash filter – convert input password into password_hash
- path_join filter – Join one or more path components
- permutations filter – permutations from the elements of a list
- pow filter – power of (math operation)
- product filter – cartesian product of lists
- quote filter – shell quoting
- random filter – random number or list item
- realpath filter – Turn path into real path
- regex_escape filter – escape regex chars
- regex_findall filter – extract all regex matches from string
- regex_replace filter – replace a string via regex
- regex_search filter – extract regex match from string
- rekey_on_member filter – Rekey a list of dicts into a dict using a member
- relpath filter – Make a path relative
- root filter – root of (math operation)
- sha1 filter – SHA-1 hash of input data
- shuffle filter – randomize a list
- split filter – split a string into a list
- splitext filter – split a path into root and file extension
- strftime filter – date formating
- subelements filter – returns a product of a list and its elements
- symmetric_difference filter – different items from two lists
- ternary filter – Ternary operation filter
- to_datetime filter – Get datetime from string
- to_json filter – Convert variable to JSON string
- to_nice_json filter – Convert variable to ‘nicely formatted’ JSON string
- to_nice_yaml filter – Convert variable to YAML string
- to_uuid filter – namespaced UUID generator
- to_yaml filter – Convert variable to YAML string
- type_debug filter – show input data type
- union filter – union of lists
- unique filter – set of unique items of a list
- unvault filter – Open an Ansible Vault
- urldecode filter – Decode percent-encoded sequences
- urlsplit filter – get components from URL
- vault filter – vault your secrets
- win_basename filter – Get a Windows path’s base name
- win_dirname filter – Get a Windows path’s directory
- win_splitdrive filter – Split a Windows path by the drive letter
- zip filter – combine list elements
- zip_longest filter – combine list elements, with filler

可以看到过滤器非常多。

## 2. Jinja2过滤器的使用

- Jinja2内置过滤器也有很多，详细可参考[List of Builtin Filters](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters)

我们简单使用一下：

- `upper`，将值全部变成大写。
- `lower`，将值全部变成小写。
- `capitalize`，将值第一个字符变成大写，其他字符全部变成小写。

我们来测试一下，编写剧本文件`filter_jinja2.yml`:

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - message: "Ansible provides open-source automation that reduces complexity and runs everywhere."

  tasks:
    - name: display the message
      ansible.builtin.debug:
        msg: |
          The base message is {{ message }}
          The upper message is {{ message|upper }}
          The lower message is {{ message|lower }}
          The capitalize message is {{ message|capitalize }}

```

检查并运行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint filter_jinja2.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook filter_jinja2.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display the message] *********************************************************************************************
ok: [node1] => {
    "msg": "The base message is Ansible provides open-source automation that reduces complexity and runs everywhere.\nThe upper message is ANSIBLE PROVIDES OPEN-SOURCE AUTOMATION THAT REDUCES COMPLEXITY AND RUNS EVERYWHERE.\nThe lower message is ansible provides open-source automation that reduces complexity and runs everywhere.\nThe capitalize message is Ansible provides open-source automation that reduces complexity and runs everywhere.\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

可以看到，剧本中的过滤器起作用了。使用`upper`过滤器，将定义的`message`变量的字符串全部变成了大写输出；使用`lower`过滤器，将定义的`message`变量的字符串全部变成了小写输出；使用`capitalize`过滤器，将定义的`message`变量的字符串首字母变成了大写`A`，其他字符全部变成了小写输出。

此处不详细介绍Jinja2每一个过滤器的使用，有需要时再查询官方文档。

## 3. Ansible内置过滤器的使用

### 3.1 base64编解码

Base64是一种二进制到文本的编码方式。详细可参考[base64](https://zh.m.wikipedia.org/zh-hans/Base64)

可以使用以下过滤器进行base64编解码：

- `b64decode`，base64解码。
- `b64encode`，base64编码。

#### 3.1.1 命令行测试base64编解码

在命令行测试base64命令。查看帮助信息：
```sh
[ansible@ansible ~]$ base64 --help
Usage: base64 [OPTION]... [FILE]
Base64 encode or decode FILE, or standard input, to standard output.

Mandatory arguments to long options are mandatory for short options too.
  -d, --decode          decode data
  -i, --ignore-garbage  when decoding, ignore non-alphabet characters
  -w, --wrap=COLS       wrap encoded lines after COLS character (default 76).
                          Use 0 to disable line wrapping

      --help     display this help and exit
      --version  output version information and exit

With no FILE, or when FILE is -, read standard input.

The data are encoded as described for the base64 alphabet in RFC 3548.
When decoding, the input may contain newlines in addition to the bytes of
the formal base64 alphabet.  Use --ignore-garbage to attempt to recover
from any other non-alphabet bytes in the encoded stream.

GNU coreutils online help: <http://www.gnu.org/software/coreutils/>
For complete documentation, run: info coreutils 'base64 invocation'
[ansible@ansible ~]$
```

使用`echo`命令时，默认会加入执行符。我们进行base64编码时，不需要换行符：

```sh
# 默认情况下，带换行符编码
[ansible@ansible ~]$ echo "Ansible is powerful."|base64
QW5zaWJsZSBpcyBwb3dlcmZ1bC4K

# 不换行符编码
[ansible@ansible ~]$ echo -n "Ansible is powerful."|base64
QW5zaWJsZSBpcyBwb3dlcmZ1bC4=
[ansible@ansible ~]$
```

可以看到，最后一位不一样，前面编码是一样的。

解码：

```sh
[ansible@ansible ~]$ echo "Ansible is powerful."|base64|base64 -d
Ansible is powerful.
[ansible@ansible ~]$ echo -n "Ansible is powerful."|base64|base64 -d
Ansible is powerful.[ansible@ansible ~]$
```

可以看到，解码时，`echo`命令不带`-n`参数时，base64解码时会解码出`\n`换行符自动换行。而`echo`命令带`-n`参数时，base64解码时不会额外解码`\n`换行符，只解码我们定义的字符串。


#### 3.1.2 使用Ansible剧本进行base64编解码

编写剧本文件`filter_base64.yml`:

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - message: "Ansible is powerful."

  tasks:
    - name: display the message
      ansible.builtin.debug:
        msg: |
          The base message is {{ message }}
          The encoded message is {{ message|b64encode }}
          The decoded message is {{ message|b64encode|b64decode }}

```

检查并执行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint filter_base64.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook filter_base64.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display the message] *********************************************************************************************
ok: [node1] => {
    "msg": "The base message is Ansible is powerful.\nThe encoded message is QW5zaWJsZSBpcyBwb3dlcmZ1bC4=\nThe decoded message is Ansible is powerful.\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

可以看到，使用Ansible `b64encode`过滤器编码后的编码`QW5zaWJsZSBpcyBwb3dlcmZ1bC4=`与在命令行测试时获取到的编码字符串是一样的，最终使用`b64decode`解码得到的原始字符串`Ansible is powerful.`正是我们定义的字符串变量的值，说明解码也是正常的！

### 3.2 Path路径相关过滤器

#### 3.2.1 获取路径的文件名或目录路径

- `basename`过滤器，获取路径的文件名。
- `dirname`过滤器，获取路径的目录路径。

编写剧本文件`filter_path.yml`:

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - config_path: "/srv/tomcat/apache-tomcat-9.0.73/conf/server.xml"

  tasks:
    - name: display the different path
      ansible.builtin.debug:
        msg: |
          The config path is {{ config_path }}
          The basename is {{ config_path|ansible.builtin.basename }}
          The dirname is {{ config_path|ansible.builtin.dirname }}

```

检查并执行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint filter_path.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook filter_path.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display the different path] **************************************************************************************
ok: [node1] => {
    "msg": "The config path is /srv/tomcat/apache-tomcat-9.0.73/conf/server.xml\nThe basename is server.xml\nThe dirname is /srv/tomcat/apache-tomcat-9.0.73/conf\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

可以看到，`basename`过滤器获取到路径`/srv/tomcat/apache-tomcat-9.0.73/conf/server.xml`对应的文件名`server.xml`，而`dirname`过滤器获取到路径`/srv/tomcat/apache-tomcat-9.0.73/conf/server.xml`对应的路径`/srv/tomcat/apache-tomcat-9.0.73/conf`。

#### 3.2.2 规范化路径

有时路径输入时，可能多写了`/`符号，可以通过`normpath`过滤器来规范化路径。

注意，该过滤器是`New in ansible-core 2.15` ansible 2.15版本引入的。

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - config_path: "/srv/tomcat/apache-tomcat-9.0.73//conf//server.xml"

  tasks:
    - name: display the different path
      ansible.builtin.debug:
        msg: |
          The config path is {{ config_path }}
          The normpath is {{ config_path|ansible.builtin.normpath }}
```

正常测试正常的话，输出`The normpath is /srv/tomcat/apache-tomcat-9.0.73/conf/server.xml`。由于我的ansible版本是ansible 2.9.27版本，执行剧本会报`ansible.builtin.normpath`过滤器不存在异常。


#### 3.2.3 获取文件扩展名

可以通过`splitext`获取路径对应的文件扩展名。

编写剧本文件`filter_splitext.yml`:

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - config_path: "/srv/tomcat/apache-tomcat-9.0.73/conf/server.xml"

  tasks:
    - name: display the filename root and extension
      ansible.builtin.debug:
        msg: |
          The config path is {{ config_path }}
          The filename root and extension list is {{ config_path|ansible.builtin.splitext }}

```

执行剧本：

```sh
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display the filename root and extension] *************************************************************************
ok: [node1] => {
    "msg": "The config path is /srv/tomcat/apache-tomcat-9.0.73/conf/server.xml\nThe filename root and extension list is (u'/srv/tomcat/apache-tomcat-9.0.73/conf/server', u'.xml')\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

可以看到，获取到扩展是`.xml`，与官网示例有差异，示例：

```yaml
# gobble => [ '/etc/make', 'conf' ]
gobble: "{{ '/etc/make.conf' | splitext }}"

# file_n_ext => [ 'ansible', 'cfg' ]
file_n_ext: "{{ 'ansible.cfg' | splitext }}"

# hoax => ['/etc/hoasdf', '']
hoax: '{{ "/etc//hoasdf/"|splitext }}'
```

#### 3.2.4 获取软链接真实路径

- 可以使用`realpath`来获取软链接的真实路径。

::: warning 注意
该过滤器只会获取Ansible管理节点文件系统上面对应的软链接的真实路径。
:::

先在节点1上查看`java`对应的软链接信息：

```sh
[root@node1 ~]# ls -lah /usr/bin/java
lrwxrwxrwx 1 root root 22 Mar 28  2023 /usr/bin/java -> /etc/alternatives/java
[root@node1 ~]# ls -lah /etc/alternatives/java
lrwxrwxrwx 1 root root 73 Mar 28  2023 /etc/alternatives/java -> /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.362.b08-1.el7_9.x86_64/jre/bin/java
[root@node1 ~]#
```

在Ansible管理节点执行以上命令：

```sh
[root@ansible ~]# ls -lah /usr/bin/java
lrwxrwxrwx 1 root root 22 Sep 13 22:43 /usr/bin/java -> /etc/alternatives/java
[root@ansible ~]# ls -lah /etc/alternatives/java
lrwxrwxrwx 1 root root 73 Sep 13 22:43 /etc/alternatives/java -> /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.382.b05-1.el7_9.x86_64/jre/bin/java
[root@ansible ~]#
```

可以看到，两个节点上面`java`最终的路径是不一样的。管理节点上面对应的是` /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.382.b05-1.el7_9.x86_64/jre/bin/java`，而node1节点上面对应的是`/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.362.b08-1.el7_9.x86_64/jre/bin/java`。

请看以下示例。

编写剧本文件`filter_realpath.yml`:

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - java_path: "/usr/bin/java"

  tasks:
    - name: display the real path
      ansible.builtin.debug:
        msg: |
          The java path is {{ java_path }}
          The real path is {{ java_path|ansible.builtin.realpath }}

```

检查并运行剧本：
```sh
[ansible@ansible ansible_playbooks]$ ansible-lint filter_realpath.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook filter_realpath.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display the real path] *******************************************************************************************
ok: [node1] => {
    "msg": "The java path is /usr/bin/java\nThe real path is /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.382.b05-1.el7_9.x86_64/jre/bin/java\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

最终输出的是`"The java path is /usr/bin/java\nThe real path is /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.382.b05-1.el7_9.x86_64/jre/bin/java\n"`，对应的路径是Ansible管理节点上面的`java`的真实路径，不是节点node1上面的`java`的真实路径。

#### 3.2.5 其他路径相关过滤器

- `commonpath`，获取列表中多个路径最长的公共路径。`New in ansible-core 2.15`。 2.15版本引入的。

示例：

```yaml
# To get the longest common path (ex. '/foo/bar') from the given list of paths (ex. ['/foo/bar/foobar','/foo/bar'])
{{ listofpaths | commonpath }}
```

- `fileglob`，通配符匹配，返回匹配路径的所有文件组成的列表。

::: warning 注意
该过滤器只会获取Ansible管理节点文件系统上面匹配到的文件。
:::

编写剧本文件`filter_fileglob.yml`：

```sh
---
- hosts: node1
  # 定义变量
  vars:
    - nginx_path: "/etc/nginx/*.conf"

  tasks:
    - name: find nginx conf files
      ansible.builtin.debug:
        msg: |
          The config file list is {{ nginx_path|fileglob }}

```

运行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint filter_fileglob.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook filter_fileglob.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [find nginx conf files] *******************************************************************************************
ok: [node1] => {
    "msg": "The config file list is [u'/etc/nginx/fastcgi.conf', u'/etc/nginx/nginx.conf']\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

可以看到，匹配到了2个nginx的配置文件。

- `path_join`，将列表路径元素合并成一个长路径。`New in ansible-base 2.10`。2.10版本引入的。

示例：

```yaml
# If path == 'foo/bar' and file == 'baz.txt', the result is '/etc/foo/bar/subdir/baz.txt'
{{ ('/etc', path, 'subdir', file) | path_join }}

# equivalent to '/etc/subdir/{{filename}}'
wheremyfile: "{{ ['/etc', 'subdir', filename] | path_join }}"

# trustme => '/etc/apt/trusted.d/mykey.gpgp'
trustme: "{{ ['/etc', 'apt', 'trusted.d', 'mykey.gpg'] | path_join }}"

```

- `relpath`，获取相对路径。

示例：

```yaml
# foobar => ../test/me.txt
testing: "{{ '/tmp/test/me.txt' | relpath('/tmp/other/') }}"
otherrelpath: "{{ mypath | relpath(mydir) }}"

```

### 3.3 hash散列相关过滤器

- `hash`，默认使用`SHA-1`算法返回输入数据的散列值，可以设置其他算法。
- `checksum`，使用`SHA-1`算法返回输入数据的散列值。
- `md5`，返回输入数据的MD5值。
- `sha1`，使用`SHA-1`算法返回输入数据的散列值。
- `password_hash`，默认使用`sha512`算法返回输入密码的加密字符串，可以设置其他算法。

编写测试剧本`filter_hash.yml`:

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - password: "test2"

  tasks:
    - name: display the different hash value
      ansible.builtin.debug:
        msg: |
          The password is {{ password }}
          The default hash password is {{ password|hash }}
          The sha1 hash password is {{ password|hash('sha1') }}
          The md5 hash password is {{ password|hash('md5') }}
          The checksum password is {{ password|checksum }}
          The md5 password is {{ password|md5 }}
          The password_hash password is {{ password|password_hash }}

```

检查并执行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint filter_hash.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook filter_hash.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display the different hash value] ********************************************************************************
ok: [node1] => {
    "msg": "The password is test2\nThe default hash password is 109f4b3c50d7b0df729d299bc6f8e9ef9066971f\nThe sha1 hash password is 109f4b3c50d7b0df729d299bc6f8e9ef9066971f\nThe md5 hash password is ad0234829205b9033196ba818f7a872b\nThe checksum password is 109f4b3c50d7b0df729d299bc6f8e9ef9066971f\nThe md5 password is ad0234829205b9033196ba818f7a872b\nThe password_hash password is $6$npQoaVnVxSg3idL5$Ejk3Xa2nR4zNIabU8dJQ64wRgFygw7aLGjip5J9M985bV0ZrNgHQTffmhY4ebs5QS6dPk/JhWh5uobzoA1M610\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

可以看到，各过滤器能正常获取到结果。

在官方过滤器列表中，可以看到有非常多的过滤器，我们不一一去测试，后面实际使用时再测试。

## 4. 自定义过滤器

### 4.1 编写自定义过滤器Python脚本 

在ansible配置文件中定义了过滤器存放的位置。

```sh
[ansible@ansible ~]$ grep -C3 filter_plugins /etc/ansible/ansible.cfg
#lookup_plugins     = /usr/share/ansible/plugins/lookup
#inventory_plugins  = /usr/share/ansible/plugins/inventory
#vars_plugins       = /usr/share/ansible/plugins/vars
#filter_plugins     = /usr/share/ansible/plugins/filter
#test_plugins       = /usr/share/ansible/plugins/test
#terminal_plugins   = /usr/share/ansible/plugins/terminal
#strategy_plugins   = /usr/share/ansible/plugins/strategy
[ansible@ansible ~]$
```

可以看到`filter_plugins     = /usr/share/ansible/plugins/filter`，即默认过滤器位置是`/usr/share/ansible/plugins/filter`。

我们可以修改该行配置，修改成其他路径，或者直接使用该默认路径即可。

::: warning 注意
如果使用角色，也可以直接在角色对应的子目录filter_plugins下创建自定义过滤器。如将自定义过滤器存放到`roles/demo/filter_plugins`目录，则在`demo`角色中就可以使用相应的过滤器。
:::

我们需要将编写的自定义过滤器Python脚本存放到该目录下。

参考 [ansible中过滤器的介绍以及如何自定义过滤器](https://www.cnblogs.com/dogfei/p/17311916.html)

编写过滤器文件`split_everything.py`:

```py
#coding=utf-8
import re

def split_everything(content):
    """以多个分隔符将字符串分割成列表"""
    return re.split(',|\||:|;|@', content)


class FilterModule(object):
    def filters(self):
        return {
            "split_everything": split_everything,
        }
```

另外，在[这里](https://www.jianshu.com/p/d578bb58edf3)看到另一个`to_list`的过滤器编写示例：

```py
from ansible import errors

def to_list(value):
    try:
        res_list = value.split(",")
        return res_list
    except Exception, e:
        raise errors.AnsibleFilterError("to list error: %s" % str(e))

class FilterModule(object):
    def filters(self):
        return {
          'to_list': to_list
        }

```

编写自定义过滤器时，先写一个自己定义的函数，然后套用后面的`class FilterModule(object):`类，定义一个`filters`方法，返回一个字典，字典元素的键是需要使用的过滤器名称，值是自定义的函数的名称。

将编写的自定义过滤器`filter_everything.py`放到过滤器目录下:

```sh
[ansible@ansible ~]$ ll /usr/share/ansible/plugins/filter
total 4
-rw-r--r-- 1 root root 285 Oct 16 22:40 split_everything.py
[ansible@ansible ~]$ cat /usr/share/ansible/plugins/filter/split_everything.py
#coding=utf-8
import re

def split_everything(content):
    """以多个分隔符将字符串分割成列表"""
    return re.split(',|\||:|;|@', content)


class FilterModule(object):
    def filters(self):
        return {
            "split_everything": split_everything,
        }
[ansible@ansible ~]$
```

### 4.2 使用自定义过滤器

编写测试剧本：

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - test_string: "a,b;c|d:e@f"

  tasks:
    - name: use custom filter to split test string to list
      ansible.builtin.debug:
        msg: |
          The test_string is {{ test_string }}
          The split list is {{ test_string|split_everything }}

```

即我们需要将`a,b;c|d:e@f`字符串按多个字符分隔开，形成一个列表。

手动测试：

```python
[ansible@ansible ~]$ python3
Python 3.6.8 (default, Nov 16 2020, 16:55:22)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import re
>>>
>>> def split_everything(content):
...     """以多个分隔符将字符串分割成列表"""
...     return re.split(',|\||:|;|@', content)
...
>>> test_string = "a,b;c|d:e@f"
>>> split_everything(test_string)
['a', 'b', 'c', 'd', 'e', 'f']
>>>
```

可以看到，使用自定义函数能够正常切割，形成列表。

我们测试一下剧本：

```sh
[ansible@ansible ~]$ cd ansible_playbooks/
[ansible@ansible ansible_playbooks]$ ll filter_custom.yml
-rw-rw-r-- 1 ansible ansible 301 Oct 16 22:38 filter_custom.yml
[ansible@ansible ansible_playbooks]$ ansible-lint filter_custom.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook filter_custom.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [use custom filter to split test string to list] ******************************************************************
ok: [node1] => {
    "msg": "The test_string is a,b;c|d:e@f\nThe split list is [u'a', u'b', u'c', u'd', u'e', u'f']\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

可以看到，自定义过滤器能够正常运行，最终生成的列表是`[u'a', u'b', u'c', u'd', u'e', u'f']`，与我们测试得到的结果是一样的。

运行效果图：

![](/img/Snipaste_2023-10-16_23-02-50.png)



