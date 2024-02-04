# ansible-vault数据加密

[[toc]]


## 1. 概述

- Ansible Vault对变量和文件进行加密，这样您就可以保护密码或密钥等敏感内容，而不是将其作为明文显示在剧本或角色中。然后你可以将加密后的内容上传到版本管理仓库中，而不用担心密码泄露。
- 官方文档：[Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/vault.html)。
- 命令行参数说明[ansible-vault](https://docs.ansible.com/ansible/latest/cli/ansible-vault.html#ansible-vault)。
- 简单来说，对于密码之类的敏感信息，可以使用ansible-vault加密后，再存储到系统中，避免敏感信息泄露。

## 2. ansible-vault命令初探

### 2.1 查看帮助信息

可以通过以下方式查看ansible-vault命令的帮助信息：

```sh
[ansible@master ~]$ ansible-vault -h
usage: ansible-vault [-h] [--version] [-v]
                     {create,decrypt,edit,view,encrypt,encrypt_string,rekey}
                     ...

encryption/decryption utility for Ansible data files

positional arguments:
  {create,decrypt,edit,view,encrypt,encrypt_string,rekey}
    create              Create new vault encrypted file
    decrypt             Decrypt vault encrypted file
    edit                Edit vault encrypted file
    view                View vault encrypted file
    encrypt             Encrypt YAML file
    encrypt_string      Encrypt a string
    rekey               Re-key a vault encrypted file

optional arguments:
  --version             show program's version number, config file location,
                        configured module search path, module location,
                        executable location and exit
  -h, --help            show this help message and exit
  -v, --verbose         verbose mode (-vvv for more, -vvvv to enable
                        connection debugging)

See 'ansible-vault <command> --help' for more information on a specific
command.
[ansible@master ~]$
```

可以看到`ansible_vault`包含几个位置参数以及可选参数，以下详细说明：

位置参数：

- `create`，创建新的加密文件
- `decrypt`, 对加密文件进行解密
- `edit`, 编辑加密文件
- `view`，查看加密文件内容，可以理解为查看解密后的内容
- `encrypt`，对YAML文件进行加密
- `encrypt_string`，对字符串进行加密
- `rekey`，改变用于加密、解密的口令

可选参数：

- `--version`，查看程序版本信息，配置文件位置等信息。
- `-h`或`--help`，打印帮助信息。
- `-v`或`--verbose`，详细模式，可以看更多的日志信息。

### 2.2 设置快捷命令

一看到这种长的命令，就想用快捷命令代替，能少写几个字母就少写。

设置快捷命令：

```sh
alias av='ansible-vault'
alias avc='ansible-vault create'
alias avd='ansible-vault decrypt'
alias ave='ansible-vault encrypt'
alias aves='ansible-vault encrypt_string'
alias avr='ansible-vault rekey'
# modify = edit
alias avm='ansible-vault edit'
alias avv='ansible-vault view'
alias v.='vim ~/.bashrc'
alias s.='source ~/.bashrc && echo "Reload OK"'
```

将以上内容添加到`~/.bashrc`配置文件中，然后使用`source ~/.bashrc`使配置生效。然后就可以查看`ansible-vault`相关的快捷命令了：

```sh
[ansible@master ~]$ alias |grep av
alias av='ansible-vault'
alias avc='ansible-vault create'
alias avd='ansible-vault decrypt'
alias ave='ansible-vault encrypt'
alias aves='ansible-vault encrypt_string'
alias avm='ansible-vault edit'
alias avr='ansible-vault rekey'
alias avv='ansible-vault view'
[ansible@master ~]$ av --version
ansible-vault 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ansible/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /bin/ansible-vault
  python version = 2.7.5 (default, Nov 16 2020, 22:23:17) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
[ansible@master ~]$
```

可以看到，快捷命令已经生效了。

### 2.3 创建加密数据文件

可以使用快捷命令`alias avc='ansible-vault create'`创建一个加密数据文件，我们直接在命令行输入`avc secure.yml`命令：
```sh
[ansible@master ansible_playbooks]$ avc secure.yml
New Vault password:    # 此处要求输入密码，我们输入123456
Confirm New Vault password:   # 此处要求再次输入密码，我们再次输入123456
```

此时，会打开一个临时文件：

![](/img/Snipaste_2023-08-10_21-46-45.png)
我们在文件中输入内容：

```yaml
---
info:
  passwd: 123456
  api_token: 1234567890asdfghjkl
```

然后保存并退出vim。此时直接使用`cat`命令查看文件内容：

```sh
[ansible@master ansible_playbooks]$ cat secure.yml
$ANSIBLE_VAULT;1.1;AES256
30383063333230356437303661313335386636306136333162336534336139313364643963323833
3030343865663764353664333062376161333438623032330a616265643733656663626233396531
65613238643437643232303064613432323661323630643364343235626439656331633235396238
6364646437326130320a333034323964363763636161303838653337333362383438313266666466
62393064666162623638313566623733303362663965306531343234653239353765663731653032
65656263363161363263633863383833326137383335376564643833353665383732623934346133
336161646264306634636636353865323339
[ansible@master ansible_playbooks]$
```

可以看到，文件内容是加密后的随机字符串，直接看文本内容是不知道原文是什么，也就是生成了加密数据了。


### 2.4 查看加密数据文件原文

上一节生成了加密数据文件`secure.yml`文件，如果想查看加密数据文件的原文，可以使用快捷命令`alias avv='ansible-vault view'`:

```sh
[ansible@master ansible_playbooks]$ avv secure.yml
Vault password:    # 此处要求提供密码验证，我们输入正确密码123456
---
info:
  passwd: 123456
  api_token: 1234567890asdfghjkl

[ansible@master ansible_playbooks]$
```
可以看到，在输入正确密码后，输出了原文信息。

如果密码输入错误，看看输出效果怎样：

```sh
[ansible@master ansible_playbooks]$ avv secure.yml
Vault password:     # 此处要求提供密码验证，我们随机输入错误密码 abcdef
ERROR! Decryption failed (no vault secrets were found that could decrypt) on secure.yml for secure.yml
[ansible@master ansible_playbooks]$
```

提示异常，`ERROR! Decryption failed (no vault secrets were found that could decrypt)`，即解密失败，找不到可以解密的保密库机密！！

也就是说一旦我们忘记密码，那么加密数据文件的原文就找不到了，所以一定要保存好加密用的密码！！！！


### 2.5 更新加密的数据文件

有的时候，需要对原文进行修改，这个时候就可以使用快捷命令`alias avm='ansible-vault edit'`进行修改。比如，我想将原文中`passwd`的密码值从`123456`修改成`654321`:

```sh
[ansible@master ansible_playbooks]$ avm secure.yml
Vault password:    # 此处要求提供密码验证，我们输入正确密码123456
```

此时，会自动打开vim，只用在vim中对原文进行正常编辑，然后保存即可。

![](/img/Snipaste_2023-08-10_22-08-44.png)

此时ansible会自动对原文进行重新加密，并更新加密文件。此时查看加密文件内容：

```sh
[ansible@master ansible_playbooks]$ cat secure.yml
$ANSIBLE_VAULT;1.1;AES256
31333231336630393462373566613132623065363731326361326237376536343533333031666236
3536306165353565633233616637393633373431636333310a666235633564343337313634393662
37343866376661613333346361386237393462353032623132353763303862386539383262313330
6338303136643566310a623335313832643937656163393534616132313033393334636534333537
35646564336365643831366437393561383834656432663762613762323464313062396264333639
35386161393066356265326432653131343533326166396561363438376434316138643963326638
623562626566313632396361656463346234
[ansible@master ansible_playbooks]$
```

可以看到，加密文件内容已经与开始的时候不一样了！！！


再次使用`avv`查看加密数据文件的原文：

```sh
[ansible@master ansible_playbooks]$ avv secure.yml
Vault password:    # 此处要求提供密码验证，我们输入正确密码123456
---
info:
  passwd: 654321
  api_token: 1234567890asdfghjkl

[ansible@master ansible_playbooks]$
```

可以看到，原文内容已经更新成功了！

### 2.6 更新加密数据文件口令

刚开始测试时，我们设置了个非常简单的口令`123456`，非常容易被别人猜到，这个时候，我们就应该设置一个强度高一点的口令，如我们将口令修改为`1234567890`，此处作测试，没有用非常复杂的口令，你自己在生产环境时，建议用复杂的口令。

这时快捷命令`alias avr='ansible-vault rekey'`就可以用了。

注意：
- 该命令会先访问当前口令，输入正确口令之后才能允许你进行设置新的口令和再次确认新口令。
- 如果你使用版本控制系统管理这个文件，即使你的文件内容（即原文）没有变化，也需要再次进行提交，重置密钥的操作将会更新最终加密的文件（即加密数据文件也更新了），需要提交到仓库中去。

```
[ansible@master ansible_playbooks]$ avr secure.yml
Vault password:     # 此处要求提供密码验证，我们输入当前的密码123456
New Vault password:    # 此处要求输入密码，我们输入1234567890
Confirm New Vault password:   # 此处要求再次输入密码，我们再次输入1234567890
Rekey successful
```
可以看到，口令更新成功。

此时查看加密数据文件内容，可以发现文件内容已经发生了变化。
```sh
[ansible@master ansible_playbooks]$ cat secure.yml
$ANSIBLE_VAULT;1.1;AES256
36656137376363336232626237623435663936643534623665646561313130303766336232316634
3238386633626535303165653265643166343431323538380a613662336536663631303766643465
32336632356236633734313435643035323964666636666230373137363064353863356232623564
6438383839633239320a323736326437336434376637656165613935363331386630333838343033
31393233363764316465366566663633643936353837333536333530346331333230653930366637
66633864306235613331376466653632356232363365343030336163343539306237633763376633
356238363035383737643537343831656261
[ansible@master ansible_playbooks]$
```

### 2.7 对加密数据文件进行解密还原

有的时候，我们可能不需要对原文进行加密了，这时就不需要加密数据文件，可以对其进行解密，还原成原文本来面貌。

此时，就可以使用快捷命令`alias avd='ansible-vault decrypt'`进行解密了。

```sh
[ansible@master ansible_playbooks]$ avd secure.yml
Vault password:     # 此处要求提供密码验证，我们输入当前的密码1234567890
Decryption successful
```
可以看到，提示解密成功，我们查看一下文件内容：

```sh
[ansible@master ansible_playbooks]$ cat secure.yml
---
info:
  passwd: 654321
  api_token: 1234567890asdfghjkl

[ansible@master ansible_playbooks]$
```

可以看到，文件本来面貌已经展现在面前，直接看到原文内容了！！也就是加密数据文件解密还原了。


### 2.8 对已经存在文件进行加密

上一节已经直接能看到原文内容了，心里就得不安稳，还是想把存在密码和TOKEN口令的文件加密了，这个时候就需要对已经存在的文件进行加密。

这时快捷命令`alias ave='ansible-vault encrypt'`就可以用了。

我们设置密码为`1234567890`。

```sh
[ansible@master ansible_playbooks]$ ave secure.yml
New Vault password:    # 此处要求输入密码，我们输入1234567890
Confirm New Vault password:    # 此处要求再次输入密码，我们再次输入1234567890
Encryption successful
```

可以看到，提示加密成功。

我们看一下加密数据文件内容：

```sh
[ansible@master ansible_playbooks]$ cat secure.yml
$ANSIBLE_VAULT;1.1;AES256
64623038383331303532383866626531356631393266333534376131336166346230303038373632
3565383239366538323037616635663263306134373533610a393832313563343438303030663764
64326430373536643536376665626436383135316438646538393932373065643062356238316161
3235343062326438630a396139636130633035393038613162366466313834313632613962303835
64303934396339646438363561383030653636393632363532313166313934323034383234363661
65633932386566383535393164353837333435356634333965353133366230333834613935363634
316262663435636436613337326433663963
[ansible@master ansible_playbooks]$
```

可以看到，又重新生成了加密数据文件，其内容与之前加密时的字符串又是不一样的，即每次加密时，虽然加密口令相同，但生成的加密数据文件里面的字符却是不一样的！！

这个时候，还是可以使用`avv`命令来查看加密数据文件对应的原文内容。

### 2.9 加密字符串

前面的操作，我们进行加密的都是文件，有的时候，我们并不需要对文件全部进行加密，只想加密码其中的某一部分，如密码字符串。

如我们只想对密码`654321`进行加密。

此时，可以使用快捷命令`alias aves='ansible-vault encrypt_string'`进行字符串加密。

```sh
[ansible@master ansible_playbooks]$ aves 654321
New Vault password:    # 此处要求输入密码，我们输入1234567890
Confirm New Vault password:    # 此处要求再次输入密码，我们再次输入1234567890
!vault |
          $ANSIBLE_VAULT;1.1;AES256
          35663161366133623732333335363431333063643835313565613435623964636636303565306466
          3763303361383265613464353134333336333061326231630a343565336634333339373563303063
          31316330346234626162343736626461616333303936323634333330656139653131353661353238
          3738336133346535380a653933636261303933316262616531643166356164373632383731316161
          6438
Encryption successful
[ansible@master ansible_playbooks]$
```
可以看到，已经生成了加密后的字符串。


## 3. 剧本的使用


### 3.1 剧本中使用加密字符串

接着2.9节，我们生成了密码`654321`的加密字符串，我们编写一个`vault.yml`的剧本文件，用于显示加密字符串的原文，其内容如下：

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - user_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          35663161366133623732333335363431333063643835313565613435623964636636303565306466
          3763303361383265613464353134333336333061326231630a343565336634333339373563303063
          31316330346234626162343736626461616333303936323634333330656139653131353661353238
          3738336133346535380a653933636261303933316262616531643166356164373632383731316161
          6438

  tasks:
    - name: display variable from encryption variable 
      ansible.builtin.debug:
        msg: The user password is {{ user_password }}

```

我们直接运行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint vault.yml
[ansible@master ansible_playbooks]$ ansible-playbook vault.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display variable from encryption variable] ***********************************************************************
fatal: [node1]: FAILED! => {"msg": "Attempting to decrypt but no vault secrets found"}

PLAY RECAP *************************************************************************************************************
node1                      : ok=1    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

![](/img/Snipaste_2023-08-10_23-08-27.png)
可以看到，直接运行时报错，未能读取到加密字符串对应的解密口令，剧本运行失败。

通过`ansible-playbook`帮助命令，可以查看`vault`相关的选项：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook --help|grep vault
                        [-e EXTRA_VARS] [--vault-id VAULT_IDS]
                        [--ask-vault-pass | --vault-password-file VAULT_PASSWORD_FILES]
  --ask-vault-pass      ask for vault password
  --vault-id VAULT_IDS  the vault identity to use
  --vault-password-file VAULT_PASSWORD_FILES
                        vault password file
```

可以看到，有三个选项可以指定：

- `--ask-vault-pass`,询问vault口令。
- `--vault-id VAULT_IDS`,从vault清单文件中读取口令。
- `--vault-password-file VAULT_PASSWORD_FILES`,从密码文件中读取口令。

### 3.2 询问口令

我们运行剧本时，增加`--ask-vault-pass`参数，让ansible向我们询问口令。

```sh
[ansible@master ansible_playbooks]$ ansible-playbook vault.yml -v --ask-vault-pass
Using /etc/ansible/ansible.cfg as config file
Vault password:     # 此处要求提供密码验证，我们输入当前的密码1234567890

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display variable from encryption variable] ***********************************************************************
ok: [node1] => {
    "msg": "The user password is 654321"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

当密码验证成功后，开始执行剧本，任务`display variable from encryption variable`打印出了密码是`654321`，说明成功解析出了加密字符串的原文字符串了！这样，剧本文件中的密码就正常被加密了，在剧本运行时可以正常读取到密码原文。


### 3.3 从密码文件中读取口令

我们可以将口令写入到文件，然后使用`--vault-id`或`--vault-password-file`指定密码文件。

```sh
# 将口令写入文件中
[ansible@master ansible_playbooks]$ echo '1234567890' > .pwdfile

# 执行剧本
[ansible@master ansible_playbooks]$ ansible-playbook vault.yml -v --vault-id .pwdfile
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display variable from encryption variable] ***********************************************************************
ok: [node1] => {
    "msg": "The user password is 654321"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$ ansible-playbook vault.yml -v --vault-password-file .pwdfile
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display variable from encryption variable] ***********************************************************************
ok: [node1] => {
    "msg": "The user password is 654321"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

![](/img/Snipaste_2023-08-10_23-29-34.png)
可以看到，通过`--vault-id`或`--vault-password-file`选项指定密码文件后，Ansible自动读取了密码信息，然后成功执行了剧本，获取了了加密字符串的原文`654321`了。

对密码文件进行权限限制：

```sh
# 权限默认是644
[ansible@master ansible_playbooks]$ ls -lah .pwdfile
-rw-r--r-- 1 ansible ansible 11 Aug 10 23:26 .pwdfile

# 将权限修改成600，其他人都不可读
[ansible@master ansible_playbooks]$ chmod 600 .pwdfile

# 再次查看文件权限，可以看到权限已经更新了
[ansible@master ansible_playbooks]$ ls -lah .pwdfile
-rw------- 1 ansible ansible 11 Aug 10 23:26 .pwdfile
```

注意，不要将密码文件上传到版本控制仓库里面去了！！


### 3.4 使用ansible-vault加密用户密码

我们使用ansible-vault对变量文件`vars/user_list.yml`进行加密。

变量文件`vars/user_list.yml`内容如下：

```yaml
---
user_hosts:
  - node1
user_info:
  - user: test1
    # 密码需要用引号括起来,避免纯数字密码被解析成int类型数字
    password: "123456"
    # 备注信息可以使用中文，但尽量不用中文
    comment: "自动创建用户test1"
  - user: test2
    password: "654321"
    comment: "auto created test2"
  - user: test3
    password: "abcdefg"
    comment: "auto created test3"

```

剧本文件`user.yml`文件内容如下：

```sh
---
- hosts: "{{ user_hosts }}"
  vars_files:
    - vars/user_list.yml
  tasks:
    - name: display variable from variable list
      ansible.builtin.debug:
        msg:  |
        The username is {{ item.user }}, 
        the password is {{ item.password }}, 
        the comment is {{ item.comment }}.
      loop: "{{ user_info }}"

    - name: create users
      ansible.builtin.user:
        name:  "{{ item.user }}"
        password: "{{ item.password|password_hash('sha512') }}"
        comment: "{{ item.comment }}"
        state: present
      loop: "{{ user_info }}"
      become: yes

```

检查剧本文件：

```sh
[ansible@master ansible_playbooks]$ ansible-lint user.yml vars/user_list.yml
[ansible@master ansible_playbooks]$
```

可以看到，没有异常。

然后，对变量文件进行加密，避免我们的密码内容被别人知道了。

这时快捷命令`alias ave='ansible-vault encrypt'`就可以用了。

我们设置密码为`1234567890`。

```sh
[ansible@master ansible_playbooks]$ ave vars/user_list.yml
New Vault password:    # 此处要求输入密码，我们输入1234567890
Confirm New Vault password:    # 此处要求再次输入密码，我们再次输入1234567890
Encryption successful
```

可以看到，提示加密成功。

查看加密数据文件：

```sh
[ansible@master ansible_playbooks]$ cat vars/user_list.yml
$ANSIBLE_VAULT;1.1;AES256
32636366313763626530396237646633393832386663393961643436643662656565353365643662
6639623436656132383033333933323863373333613865300a396334303735353135323766346436
64376134393432333061333032353335653166393930383763383731346334393334653561656538
6439613334656661630a623864323562373465346133323165396534303162663738366136616530
35353537643037626262303339306334313433313139376633313735613730376263383262306632
61373437323161386433633230623834333165333464396133653362396564326631373965333739
34353735636663333461646465313233623332656434396563323336643762386233363363323631
34346265343565656666303837306435646439343534663735656438663732653564333133326164
31353264646562353666313665363864363833663563313230363139336535393531663333613530
64383038313034373530636161336535343237343766393039376264396562636339663937613638
33633235396333346462663936323865663032313962343937616164336433356130383833356664
37666332333166303337633333613061643838363533663966643538646662633761333238353939
30613038386661623133303264663639336564333231313461363132666632353961613132306334
35633662663065373537393437353165346661393231343236353765623566656133306639363836
39336163666631343861343734663637333734613263613166373061626235323233316631643365
33376338346461626164633534643930316262333762623930353931643233623735306264333632
63303266323166613735363034386336396437343062663037626431386135643433383035396461
30383132663037383936336463333239306637623161383861393737366135383361333463323362
32303737393630376161313931663365323061313430653266316339326632343138306566313633
31383230313463303364333964633830306166343232623836336464376539326435636135303665
34323237303435393066313963303634393735646134613566363636363539396332613862623832
31373864653137343932633034616130393562626432323961386661613231656332396565666464
37643935373139333538653464356163333731366361663666383934313431663334653265383963
31643564313337323733346331333532343536636663303364383839613136393537353438343138
3436
[ansible@master ansible_playbooks]$
```
可以看到，文件已经加密了！

我们来执行一下剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook user.yml -v --ask-vault-pass
Using /etc/ansible/ansible.cfg as config file
Vault password:

PLAY [[u'node1']] ******************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display variable from variable list] *****************************************************************************
ok: [node1] => (item={u'comment': u'\u81ea\u52a8\u521b\u5efa\u7528\u6237test1', u'password': u'123456', u'user': u'test1'}) => {
    "msg": "The username is test1, the password is 123456, the comment is 自动创建用户test1."
}
ok: [node1] => (item={u'comment': u'auto created test2', u'password': u'654321', u'user': u'test2'}) => {
    "msg": "The username is test2, the password is 654321, the comment is auto created test2."
}
ok: [node1] => (item={u'comment': u'auto created test3', u'password': u'abcdefg', u'user': u'test3'}) => {
    "msg": "The username is test3, the password is abcdefg, the comment is auto created test3."
}

TASK [create users] ****************************************************************************************************
changed: [node1] => (item={u'comment': u'\u81ea\u52a8\u521b\u5efa\u7528\u6237test1', u'password': u'123456', u'user': u'test1'}) => {"ansible_loop_var": "item", "changed": true, "comment": "自动创建用户test1", "create_home": true, "group": 1003, "home": "/home/test1", "item": {"comment": "自动创建用户test1", "password": "123456", "user": "test1"}, "name": "test1", "password": "NOT_LOGGING_PASSWORD", "shell": "/bin/bash", "state": "present", "system": false, "uid": 1003}
changed: [node1] => (item={u'comment': u'auto created test2', u'password': u'654321', u'user': u'test2'}) => {"ansible_loop_var": "item", "changed": true, "comment": "auto created test2", "create_home": true, "group": 1004, "home": "/home/test2", "item": {"comment": "auto created test2", "password": "654321", "user": "test2"}, "name": "test2", "password": "NOT_LOGGING_PASSWORD", "shell": "/bin/bash", "state": "present", "system": false, "uid": 1004}
changed: [node1] => (item={u'comment': u'auto created test3', u'password': u'abcdefg', u'user': u'test3'}) => {"ansible_loop_var": "item", "changed": true, "comment": "auto created test3", "create_home": true, "group": 1005, "home": "/home/test3", "item": {"comment": "auto created test3", "password": "abcdefg", "user": "test3"}, "name": "test3", "password": "NOT_LOGGING_PASSWORD", "shell": "/bin/bash", "state": "present", "system": false, "uid": 1005}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

![](/img/Snipaste_2023-08-11_22-59-59.png)
可以看到，执行成功了！

这时，我们去节点node1上面检查一下：

```sh
[root@node1 ~]# tail -n 3 /etc/passwd
test1:x:1003:1003:自动创建用户test1:/home/test1:/bin/bash
test2:x:1004:1004:auto created test2:/home/test2:/bin/bash
test3:x:1005:1005:auto created test3:/home/test3:/bin/bash
[root@node1 ~]# ls -dl /home/test*
drwx------ 4 test1 test1 4096 Aug 11 23:02 /home/test1
drwx------ 2 test2 test2 4096 Aug 11 22:59 /home/test2
drwx------ 2 test3 test3 4096 Aug 11 22:59 /home/test3
[root@node1 ~]#
```

可以看到，用户创建成功了！！尝试使用test1、test2、test3账号登陆节点node1也可以正常登陆，说明密码设置正确！！

最后清理测试用户：

```sh
[root@node1 ~]# userdel -r test1
[root@node1 ~]# userdel -r test2
[root@node1 ~]# userdel -r test3
```

- user模块的使用，可参考[user模块](./user.md).
- 交互模式下设置用户密码，可参考 [对用户输入的密码进行加密](./debug.md)


## 4. ansible-vault理论知识

由之前的实践，我们知道ansible可以通过创建加密文件或者对已有文件进行加密，都需要输入vault口令，ansible-vault用该口令对原文数据进行加密处理。加密算法是AES加密算法。加密后的内容可以存储在版本控制系统中，不会泄密。

- AES，即Advanced Encryption Standard，高级加密标准。
- 密码学中的高级加密标准（Advanced Encryption Standard，AES），又称Rijndael加密法，是美国联邦政府采用的一种区块加密标准。
- 2006年开始，高级加密标准已成为对称密钥加密中最流行的算法之一。
- AES是基于公共对称密钥，因此在解密的时候需要提供相同的口令。
- AES采用对称分组密码体制，密钥长度的最少支持128、192、256位，分组长度128位，Ansible使用的是AES 256位最长密钥长度。
- AES-256加密算法是极其安全的。即使是使用目前世界上运算速度最快的集群来7*24小时地解密一个通过该算法加密的文件，也需要数十亿年的时间才能完成破解。所以，安全算法是没有问题的。我们要做的就是保管好自己的加密口令。

下面这些敏感数据，建议使用ansible-vault进行加密:

- 凭证，如数据库口令、应用凭证、管理员(root/Administrator)密码。
- API密钥，如远程访问密钥、私钥。
- Web服务器的SSL密钥。
- 应用部署的SSH私钥。



 