# lookups插件

[[toc]]

## 1. 概述

- 我们在[debug调试模块](./debug.md)中使用了多种方式定义变量，但这些变量的定义大部分是静态的，其实Ansible支持从外部数据拉取信息，比如从数据库里面读取信息然后定义给一个变量，这时候就可以使用`lookups`插件。
- lookups插件，官方文档 [Lookups](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_lookups.html#playbooks-lookups)。
- Lookup plugins 官方文档 [Lookup plugins](https://docs.ansible.com/ansible/latest/plugins/lookup.html)。


### 1.1 查看lookups可用查看列表

如果你想要查看有哪些lookup插件可以使用，可以使用如下命令进行查看：

```sh
[ansible@ansible ~]$ ansible-doc -t lookup -l
aws_secret            Look up secrets stored in AWS Secrets Manager
manifold              get credentials from Manifold.co
vars                  Lookup templated value of variables
sequence              generate a list based on a number sequence
first_found           return first file found from list
keyring               grab secrets from the OS keyring
nested                composes a list with nested elements of other lists
cpm_metering          Get Power and Current data from WTI OOB/Combo and PDU devices
list                  simply returns what it is given
avi                   Look up ``Avi`` objects
file                  read file contents
conjur_variable       Fetch credentials from CyberArk Conjur
dnstxt                query a domain(s)'s DNS txt fields
k8s                   Query the K8s API
template              retrieve contents of file after templating with Jinja2
cpm_status            Get status and parameters from WTI OOB and PDU devices
cartesian             returns the cartesian product of lists
nios                  Query Infoblox NIOS objects
varnames              Lookup matching variable names
inventory_hostnames   list of inventory hosts matching a host pattern
passwordstore         manage passwords with passwordstore.org's pass utility
redis                 fetch data from Redis
onepassword           fetch field values from 1Password
laps_password         Retrieves the LAPS password for a server
nios_next_ip          Return the next available IP address for a network
dict                  returns key/value pair items from dictionaries
etcd                  get info from an etcd server
onepassword_raw       fetch an entire item from 1Password
hiera                 get info from hiera data
config                Lookup current Ansible configuration values
nios_next_network     Return the next available network range for a network-container
subelements           traverse nested key from a list of dictionaries
shelvefile            read keys from Python shelve file
filetree              recursively match all files in a directory tree
gcp_storage_file      Return GC Storage content
mongodb               lookup info from MongoDB
cyberarkpassword      get secrets from CyberArk AIM
indexed_items         rewrites lists to return 'indexed items'
csvfile               read data from a TSV or CSV file
chef_databag          fetches data from a Chef Databag
flattened             return single list completely flattened
aws_account_attribute Look up AWS account attributes
password              retrieve or generate a random password, stored in a file
random_choice         return random element from list
skydive               Query Skydive objects
aws_service_ip_ranges Look up the IP ranges for services provided in AWS such as EC2 and S3
env                   read the value of environment variables
url                   return contents from URL
items                 list of items
credstash             retrieve secrets from Credstash on AWS
dig                   query DNS using the dnspython library
lines                 read lines from command
rabbitmq              Retrieve messages from an AMQP/AMQPS RabbitMQ queue
together              merges lists into synchronized list
pipe                  read output from a command
consul_kv             Fetch metadata from a Consul key value store
hashi_vault           retrieve secrets from HashiCorp's vault
grafana_dashboard     list or search grafana dashboards
lastpass              fetch data from lastpass
fileglob              list files matching a pattern
aws_ssm               Get the value for a SSM parameter or all parameters under a path
ini                   read data from a ini file
```

### 1.2 查看单个插件使用方法

查看单个插件的使用方法，可以像下面这样，查看`dict`插件的使用方法：

```sh
[ansible@ansible ~]$ ansible-doc -t lookup dict
> DICT    (/usr/lib/python2.7/site-packages/ansible/plugins/lookup/dict.py)

        Takes dictionaries as input and returns a list with each item in the list being a
        dictionary with 'key' and 'value' as keys to the previous dictionary's structure.

  * This module is maintained by The Ansible Community
OPTIONS (= is mandatory):

= _terms
        A list of dictionaries



        METADATA:
          status:
          - preview
          supported_by: community


EXAMPLES:

vars:
  users:
    alice:
      name: Alice Appleworth
      telephone: 123-456-7890
    bob:
      name: Bob Bananarama
      telephone: 987-654-3210
[ansible@ansible ~]$
```

## 2. 插件的使用

### 2.1 file插件

如我们想通过lookup file插件查看`/etc/selinux/config`配置文件内容。

通过命令行查看`/etc/selinux/config`配置文件内容：

```sh
[ansible@ansible ~]$ cat /etc/selinux/config

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted


[ansible@ansible ~]$
```

编写剧本文件`lookups_file.yml`:

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    file_contents: "{{ lookup('file', '/etc/selinux/config') }}"

  tasks:
    - name: debug lookups file contents
      ansible.builtin.debug:
        msg: |
          The contents is {{ file_contents }}

```

检查并运行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint lookups_file.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook lookups_file.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [debug lookups file contents] *************************************************************************************
ok: [node1] => {
    "msg": "The contents is \n# This file controls the state of SELinux on the system.\n# SELINUX= can take one of these three values:\n#     enforcing - SELinux security policy is enforced.\n#     permissive - SELinux prints warnings instead of enforcing.\n#     disabled - No SELinux policy is loaded.\nSELINUX=disabled\n# SELINUXTYPE= can take one of three values:\n#     targeted - Targeted processes are protected,\n#     minimum - Modification of targeted policy. Only selected processes are protected. \n#     mls - Multi Level Security protection.\nSELINUXTYPE=targeted\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

可以看到，正常输出了文件各行的内容。


### 2.2 ini插件

首先编写一个`users.ini`配置文件：

```ini
[production]
user = zhangsan

[integration]
user = lisi

```

编写剧本文件`lookups_ini.yml`:

```yaml
---
- hosts: node1

  tasks:
    - name: debug lookups ini file
      ansible.builtin.debug:
        msg: |
          User in integration is {{ lookup('ini', 'user section=integration file=users.ini') }}".
          User in production  is {{ lookup('ini', 'user section=production  file=users.ini') }}.

```

检查并执行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint lookups_ini.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook lookups_ini.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [debug lookups ini file] ******************************************************************************************
ok: [node1] => {
    "msg": "User in integration is lisi.\nUser in production  is zhangsan.\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

可以看到，正常从配置文件中获取到了`user`块对应的值，`integration`集成环境用户是`lisi`，`production`生产环境用户是`zhangsan`。


### 2.3 pipe管道插件

编写剧本文件`lookups_pipe.yml`：

```yaml
---
- hosts: node1

  tasks:
    - name: raw result of running date command"
      ansible.builtin.debug:
        msg: |
          现在时间是:{{ lookup('pipe', 'date +"%Y%m%d %H:%M:%S"') }}

```

检查并执行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint lookups_pipe.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook lookups_pipe.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [raw result of running date command"] *****************************************************************************
ok: [node1] => {
    "msg": "现在时间是:20231021 21:51:13\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

可以看到，已经打印出当前时间了，说明正常执行了`date`命令了。


## 3. 自定义lookups插件

### 3.1 检查插件配置信息 

在ansible配置文件中定义了lookup插件存放的位置。

```sh
[ansible@ansible ~]$ grep lookup_plugins /etc/ansible/ansible.cfg
#lookup_plugins     = /usr/share/ansible/plugins/lookup
[ansible@ansible ~]$
```

可以看到`lookup_plugins     = /usr/share/ansible/plugins/lookup`，即默认过滤器位置是`/usr/share/ansible/plugins/lookup`。

我们可以修改该行配置，修改成其他路径，或者直接使用该默认路径即可。

### 3.2 查看插件源码

我们可以通过`ansible --version`查看ansible源文件目录：

```sh
[root@ansible ~]# ansible --version
ansible 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/root/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /bin/ansible
  python version = 2.7.5 (default, Nov 16 2020, 22:23:17) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
[root@ansible ~]#
```

可以知道源文件目录`/usr/lib/python2.7/site-packages/ansible`。

相应的可以找到`lookup`插件目录：

```sh
[root@ansible ~]# cd /usr/lib/python2.7/site-packages/ansible/plugins/lookup/
[root@ansible lookup]# ll file.py
-rw-r--r-- 1 root root 2847 Oct 11  2021 file.py
[root@ansible lookup]# ll ini.py
-rw-r--r-- 1 root root 5487 Oct 11  2021 ini.py
[root@ansible lookup]# ll pipe.py
-rw-r--r-- 1 root root 2892 Oct 11  2021 pipe.py
[root@ansible lookup]#
```

以下列出三个源文件内容：

file.py 文件内容如下：

```py
# (c) 2012, Daniel Hokka Zakrisson <daniel@hozac.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: file
    author: Daniel Hokka Zakrisson <daniel@hozac.com>
    version_added: "0.9"
    short_description: read file contents
    description:
        - This lookup returns the contents from a file on the Ansible controller's file system.
    options:
      _terms:
        description: path(s) of files to read
        required: True
      rstrip:
        description: whether or not to remove whitespace from the ending of the looked-up file
        type: bool
        required: False
        default: True
      lstrip:
        description: whether or not to remove whitespace from the beginning of the looked-up file
        type: bool
        required: False
        default: False
    notes:
      - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
      - this lookup does not understand 'globing', use the fileglob lookup instead.
"""

EXAMPLES = """
- debug: msg="the value of foo.txt is {{lookup('file', '/etc/foo.txt') }}"

- name: display multiple file contents
  debug: var=item
  with_file:
    - "/path/to/foo.txt"
    - "bar.txt"  # will be looked in files/ dir relative to play or in role
    - "/path/to/biz.txt"
"""

RETURN = """
  _raw:
    description:
      - content of file(s)
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_text
from ansible.utils.display import Display

display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        ret = []

        for term in terms:
            display.debug("File lookup term: %s" % term)

            # Find the file in the expected search path
            lookupfile = self.find_file_in_search_path(variables, 'files', term)
            display.vvvv(u"File lookup using %s as file" % lookupfile)
            try:
                if lookupfile:
                    b_contents, show_data = self._loader._get_file_contents(lookupfile)
                    contents = to_text(b_contents, errors='surrogate_or_strict')
                    if kwargs.get('lstrip', False):
                        contents = contents.lstrip()
                    if kwargs.get('rstrip', True):
                        contents = contents.rstrip()
                    ret.append(contents)
                else:
                    raise AnsibleParserError()
            except AnsibleParserError:
                raise AnsibleError("could not locate file in lookup: %s" % term)

        return ret
```

ini.py 文件内容如下：

```py
# (c) 2015, Yannig Perre <yannig.perre(at)gmail.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: ini
    author: Yannig Perre <yannig.perre(at)gmail.com>
    version_added: "2.0"
    short_description: read data from a ini file
    description:
      - "The ini lookup reads the contents of a file in INI format C(key1=value1).
        This plugin retrieves the value on the right side after the equal sign C('=') of a given section C([section])."
      - "You can also read a property file which - in this case - does not contain section."
    options:
      _terms:
        description: The key(s) to look up
        required: True
      type:
        description: Type of the file. 'properties' refers to the Java properties files.
        default: 'ini'
        choices: ['ini', 'properties']
      file:
        description: Name of the file to load.
        default: ansible.ini
      section:
        default: global
        description: Section where to lookup the key.
      re:
        default: False
        type: boolean
        description: Flag to indicate if the key supplied is a regexp.
      encoding:
        default: utf-8
        description:  Text encoding to use.
      default:
        description: Return value if the key is not in the ini file.
        default: ''
"""

EXAMPLES = """
- debug: msg="User in integration is {{ lookup('ini', 'user section=integration file=users.ini') }}"

- debug: msg="User in production  is {{ lookup('ini', 'user section=production  file=users.ini') }}"

- debug: msg="user.name is {{ lookup('ini', 'user.name type=properties file=user.properties') }}"

- debug:
    msg: "{{ item }}"
  with_ini:
    - '.* section=section1 file=test.ini re=True'
"""

RETURN = """
_raw:
  description:
    - value(s) of the key(s) in the ini file
"""
import os
import re
from io import StringIO

from ansible.errors import AnsibleError, AnsibleAssertionError
from ansible.module_utils.six.moves import configparser
from ansible.module_utils._text import to_bytes, to_text
from ansible.module_utils.common._collections_compat import MutableSequence
from ansible.plugins.lookup import LookupBase


def _parse_params(term):
    '''Safely split parameter term to preserve spaces'''

    keys = ['key', 'type', 'section', 'file', 're', 'default', 'encoding']
    params = {}
    for k in keys:
        params[k] = ''

    thiskey = 'key'
    for idp, phrase in enumerate(term.split()):
        for k in keys:
            if ('%s=' % k) in phrase:
                thiskey = k
        if idp == 0 or not params[thiskey]:
            params[thiskey] = phrase
        else:
            params[thiskey] += ' ' + phrase

    rparams = [params[x] for x in keys if params[x]]
    return rparams


class LookupModule(LookupBase):

    def get_value(self, key, section, dflt, is_regexp):
        # Retrieve all values from a section using a regexp
        if is_regexp:
            return [v for k, v in self.cp.items(section) if re.match(key, k)]
        value = None
        # Retrieve a single value
        try:
            value = self.cp.get(section, key)
        except configparser.NoOptionError:
            return dflt
        return value

    def run(self, terms, variables=None, **kwargs):

        self.cp = configparser.ConfigParser()

        ret = []
        for term in terms:
            params = _parse_params(term)
            key = params[0]

            paramvals = {
                'file': 'ansible.ini',
                're': False,
                'default': None,
                'section': "global",
                'type': "ini",
                'encoding': 'utf-8',
            }

            # parameters specified?
            try:
                for param in params[1:]:
                    name, value = param.split('=')
                    if name not in paramvals:
                        raise AnsibleAssertionError('%s not in paramvals' %
                                                    name)
                    paramvals[name] = value
            except (ValueError, AssertionError) as e:
                raise AnsibleError(e)

            # Retrieve file path
            path = self.find_file_in_search_path(variables, 'files',
                                                 paramvals['file'])

            # Create StringIO later used to parse ini
            config = StringIO()
            # Special case for java properties
            if paramvals['type'] == "properties":
                config.write(u'[java_properties]\n')
                paramvals['section'] = 'java_properties'

            # Open file using encoding
            contents, show_data = self._loader._get_file_contents(path)
            contents = to_text(contents, errors='surrogate_or_strict',
                               encoding=paramvals['encoding'])
            config.write(contents)
            config.seek(0, os.SEEK_SET)

            self.cp.readfp(config)
            var = self.get_value(key, paramvals['section'],
                                 paramvals['default'], paramvals['re'])
            if var is not None:
                if isinstance(var, MutableSequence):
                    for v in var:
                        ret.append(v)
                else:
                    ret.append(var)
        return ret
```

pipe.py 文件内容如下：

```py
# (c) 2012, Daniel Hokka Zakrisson <daniel@hozac.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
    lookup: pipe
    author: Daniel Hokka Zakrisson <daniel@hozac.com>
    version_added: "0.9"
    short_description: read output from a command
    description:
      - Run a command and return the output.
    options:
      _terms:
        description: command(s) to run.
        required: True
    notes:
      - Like all lookups this runs on the Ansible controller and is unaffected by other keywords, such as become,
        so if you need to different permissions you must change the command or run Ansible as another user.
      - Alternatively you can use a shell/command task that runs against localhost and registers the result.
      - Pipe lookup internally invokes Popen with shell=True (this is required and intentional).
        This type of invocation is considered as security issue if appropriate care is not taken to sanitize any user provided or variable input.
        It is strongly recommended to pass user input or variable input via quote filter before using with pipe lookup.
        See example section for this.
        Read more about this L(Bandit B602 docs,https://bandit.readthedocs.io/en/latest/plugins/b602_subprocess_popen_with_shell_equals_true.html)
"""

EXAMPLES = r"""
- name: raw result of running date command"
  debug:
    msg: "{{ lookup('pipe', 'date') }}"

- name: Always use quote filter to make sure your variables are safe to use with shell
  debug:
    msg: "{{ lookup('pipe', 'getent ' + myuser | quote ) }}"
"""

RETURN = r"""
  _string:
    description:
      - stdout from command
"""

import subprocess

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        ret = []
        for term in terms:
            '''
            http://docs.python.org/2/library/subprocess.html#popen-constructor

            The shell argument (which defaults to False) specifies whether to use the
            shell as the program to execute. If shell is True, it is recommended to pass
            args as a string rather than as a sequence

            https://github.com/ansible/ansible/issues/6550
            '''
            term = str(term)

            p = subprocess.Popen(term, cwd=self._loader.get_basedir(), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            (stdout, stderr) = p.communicate()
            if p.returncode == 0:
                ret.append(stdout.decode("utf-8").rstrip())
            else:
                raise AnsibleError("lookup_plugin.pipe(%s) returned %d" % (term, p.returncode))
        return ret
```

### 3.3 编写自定义lookups插件Python脚本

可以参考这里 [Executing Custom Lookup Plugins in the Ansible Automation Platform](https://www.ansiblepilot.com/articles/executing-custom-lookup-plugins-in-the-ansible-automation-platform/#:~:text=Executing%20Custom%20Lookup%20Plugins%20in%20the%20Ansible%20Automation,Conclusion%20...%205%20Academy%20...%206%20Donate%20)

编写自定义lookups插件token。

对应的`token.py`文件内容：

```py
# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: test
  author: Luca Berton <luca@ansiblepilot.com>
  version_added: "0.1"  # same as collection version
  short_description: read API token
  description:
      - This lookup returns the token from the provided API.
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import requests

display = Display()

class LookupModule(LookupBase):

    _URL_ = "https://reqres.in/api/login"

    def run(self, terms, variables=None, **kwargs):
      payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
      }
      try:
        res = requests.post(self._URL_, data=payload)
        res.raise_for_status()
        ret = res.json()['token']

      except requests.exceptions.HTTPError as e:
        raise AnsibleError('There was an error getting a token. The lookup API returned %s', response.status_code)
      except Exception as e:
        raise AnsibleError('Unhandled exception is lookup plugin. Origin: %s', e)

      return [ret]

```

对应剧本文件：

```yaml
---
- name: Exec the lookup plugin
  hosts: all
  tasks:
    - name: Use Custom Lookup Plugin
      debug:
        msg: "{{ lookup('token') }}"
```

该自定义插件会获取网站api的token值。


### 3.4 编写获取手机号归属地和运营商信息插件

可以通过[https://www.apispace.com/explore/service#](https://www.apispace.com/explore/service#) 来获取手机号码归属地信息。

![](/img/Snipaste_2023-10-21_23-36-31.png)

如，我们随便查询一个靓号`18966666666`:

![](/img/Snipaste_2023-10-21_23-37-50.png)
可以知道其是陕西西安 联通的手机号。

再查询另一个靓号`15266666666`:

![](/img/Snipaste_2023-10-21_23-59-06.png)
可以知道其是山东临沂 中国移动的手机号。

在网页上面测试，可以看到对应的号码返回的结果是西安的：

![](/img/Snipaste_2023-10-21_23-40-09.png)

编写获取手机号的归属地信息的`/usr/share/ansible/plugins/lookup/teladdress.py`脚本:

```py
#!/usr/bin/python3
import requests

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

class LookupModule(LookupBase):

    def get_address(self, mobile):
        """get the mobile address and isp info"""
        url = "https://eolink.o.apispace.com/teladress/teladress"
        # change the token value
        token = "your_secure_token"
        payload = {"mobile":int(mobile)}
        headers = {
            "X-APISpace-Token":token,
            "Authorization-Type":"apikey",
            "Content-Type":"application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data')
            province = data.get('province')
            city = data.get('city')
            isp = data.get('isp')

            return province, city, isp

    def run(self, terms, variables, **kwargs):
        ret = []
        for term in terms:
            display.debug("teladdress lookup term: %s" % term)
            province, city, isp = self.get_address(term)
            result_str = 'address: %s, %s, isp: %s' % (province, city, isp)
            display.debug("result_str: %s" % result_str)
            ret.append(result_str)

        return ret
```

注意，不要在该python脚本中使用中文,另外，你测试时应修改token值，token值请在
[https://www.apispace.com/](https://www.apispace.com/) 网站上获取。并且把`/usr/share/ansible/plugins/lookup/teladdress.py`脚本存放到Ansible控制主机对应路径下。

编写剧本文件：

```yaml
---
- hosts: node1

  # 定义变量
  vars:
    mobile_number: "{{ mobile |default(18966666666) }}"

  tasks:
    - name: get the mobile address and isp info
      ansible.builtin.debug:
        msg: |
          手机号:{{ mobile_number }} {{ lookup('teladdress', mobile_number) }}

```

检查执行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint lookups_custom.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook lookups_custom.yml -v -e mobile=15266666666
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ****************************************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************************
ok: [node1]

TASK [get the mobile address and isp info] **********************************************************************************************************************************************
ok: [node1] => {
    "msg": "手机号:15266666666 address: 山东, 临沂, isp: 移动\n"
}

PLAY RECAP ******************************************************************************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$ ansible-playbook lookups_custom.yml -v -e mobile=18966666666
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ****************************************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************************
ok: [node1]

TASK [get the mobile address and isp info] **********************************************************************************************************************************************
ok: [node1] => {
    "msg": "手机号:18966666666 address: 陕西, 西安, isp: 电信\n"
}

PLAY RECAP ******************************************************************************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$

```

运行结果效果图:

![](/img/Snipaste_2023-10-22_00-00-30.png)
可以看到，通过自己编写的插件获取的结果与通过百度号码认证平台获取的结果地址基本是一致的（由于存在携号转网的情况，运营商信息不一定准确），也就说明我们编写的插件是起作用了。

