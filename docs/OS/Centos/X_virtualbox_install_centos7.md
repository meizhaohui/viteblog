# 在VirtualBox中安装CentOS7虚拟机系统

[[toc]]

有时我们在学习一些新的知识时，需要使用VitualBox或者VMware配置和安装虚拟机系统，并在虚拟机系统中进行一些实验操作。



今天再次总结一下在VirtualBox中安装CentOS7虚拟机。你也可以使用VMware workstation创建虚拟机，由于我使用VMware workstation创建虚拟机时，VMware workstation启动卡顿，感觉电脑卡顿严重，VitualBox相对来说轻量一些。



## Windows系统中安装VirtualBox

可以在腾讯软件中心下载VirtualBox, [https://pc.qq.com/detail/3/detail_1023.html](https://pc.qq.com/detail/3/detail_1023.html),也可以在官网下载，下载完成后直接双击`virtualbox-Win-latest_6.0.12.exe`可执行文件安装即可。

双击桌面中的`Oracle VM VirtualBox`图标，可以打开VirtualBox应用。

![](/img/20200511232616.jpg)



## 下载CentOS7镜像

可以在CentOS官网[https://www.centos.org/download](https://www.centos.org/download)下载镜像，但由于网络原因在官网下载速度可能很慢，因此建议使用国内的镜像站去下载，如阿里云的镜像站，清华大学的镜像站。



我们使用`CentOS-7-x86_64-Minimal-1810.iso`这个版本。



## 新建CentOS7虚拟机

我们在VirtualBox中新建虚拟机。

- 新建虚拟机，设置虚拟机名称：

![](/img/20200511233502.png)



::: warning 警告

如果你看到的版本选项只有32-bit，没有64-bit的话，极有可能你的电脑BIOS未开启虚拟化技术，请进入BIOS修改。

:::

- 设置虚拟机内存

将默认的1024MB改成2048MB：

![](/img/20200511233603.png)

- 现在创建虚拟机

点击"创建"即可：

![](/img/20200511233700.png)

- 使用默认的硬盘文件类型

![](/img/20200511233812.png)



- 设置动态分配物理硬盘

![](/img/20200511233847.png)

- 创建虚拟硬盘

设置虚拟硬盘大小为20GB，并点击“创建”按钮：

![](/img/20200511233935.png)

此时创建出了一个CentOS7的虚拟机：

![](/img/20200511234109.png)

注意，此时不要点击“启动”按钮，还需要进行一些配置。我们先关注一下网络配置，待会再来设置虚拟机的其他设置。



## VirtualBox虚拟机网络环境配置

VirtualBox安装完成后，会在设备管理器->网络适配器中增加一个名称为"VirutalBox Host-Only Ethernet Adapter"的适配器：

![1589291889022](/img/1589291889022.png)



我们在`控制面板\网络和 Internet\网络连接`中查看这个网络：

![](/img/20200511235136.png)

可以看到它现在没有发包也没有接收包：

![](/img/20200511235204.png)

我们为“以太网2”配置一下DNS.



### VitualBox网络适配器DNS配置

首先，我们查看宿主机的网络详情：

![](/img/20200511235547.png)

可以看到宿主机的`IPv4 DNS服务器`信息，记录下这两个IP字段信息，我的信息如上图中的：

- 192.168.1.1
- 202.103.x.x



我们给VirtualBox网络适配器配置一下DNS:



![config dns](/img/20200512000136.png)





### 查看VirtualBox主机网络管理器

![](/img/20200512000521.png)

![](/img/20200512000606.png)

![](/img/20200512000635.png)

记住上面的最小地址和最大地址：

- 最小地址：192.168.56.3

- 最大地址：192.168.56.254

这个地址区间是我们虚拟机内部可以使用的IP区间！后面需要用到。



## VirtualBox中修改CentOS7虚拟机默认配置

### 显卡控制器设置

将显卡控制器的默认设置"VMSVGA"改为“VBoxVGA”:

![显卡控制器默认设置](/img/20200512212842.jpg)

![](/img/20200512213100.png)



### 存储设置

存储设置中选择我们下载的CentOS7镜像iso文件：

![](/img/20200512213203.png)



### 声音设置

我们关闭虚拟机中的声音，即不启用声音，去掉"启用声音"前面的勾选。

![](/img/20200512213349.png)



### 串口设置

我们不启用串口：

![](/img/20200512213548.png)



### USB设备

不启用USB控制器：

![1589290606079](/img/1589290606079.png)



### 共享文件夹和用户界面

共享文件夹和用户界面不用设置，保持默认即可。



### 网络设置

网张设置非常关键，为了让我们宿主机和虚拟机之间能够相互ping通，我们需要配置两块网卡。

- 网卡1：仅主机(Host-Only)网络：用于与宿主机通信，例如通过WinSCP传输文件、从宿主机访问虚拟机上的WEB服务等。
- 网卡2：网络地址转换(NAT)：虚拟机可访问宿主机，宿主机不能访问虚拟机，虚拟机可以访问外部网络，是访问外网更优的方案。



网卡1配置仅主机(Host-Only)网络：

![1589290989891](/img/1589290989891.png)



网卡2配置网络地址转换(NAT):

![1589291035198](/img/1589291035198.png)

以上配置完成后，可以再检查一下确认是否配置正确。确认无误后，可以启动虚拟机。



## CentOS7系统安装

首先启动centos7虚拟机：

![](/img/20200512221929.png)



### 启动异常处理



- Failed to attach the network LUN (VERR_INTNET_FLT_IF_NOT_FOUND).

![](/img/20200512222053.png)

我们先禁用一下“VirtualBox Host-Only Ethernet Adapter”,然后再启动：

禁用设备：

![](/img/20200512222250.png)

再启用设备即可。



可以使用上下键选择不同的选项，按`alt`键鼠标退出虚拟机回到宿主机。

在虚拟机中可以使用上下左右键，或者tab键进行焦点切换。 

### 安装

选择“Install CentOS 7”:

![1589293507799](/img/1589293507799.png)



保持默认的安装语言为英文：

![](/img/20200512223034.png)

配置本地化-时间和日期设置：

![](/img/20200512223232.png)



点击中国地图区域，设置区域为”Asia-Shanghai“，即”亚洲-上海“，最后点击”Done“确认：

![](/img/20200512223415.png)



语言支持可以选择你想使用的语言，我们添加中文支持：

![](/img/20200512223613.png)



安装目标磁盘，我们选择我们创建的20GB的虚拟磁盘：

![](/img/20200512223732.png)



我们将两个网卡设置为启动状态，右上角处设置为”ON“状态，自动获取IP地址：

![](/img/20200512223916.png)

最终两个网络都显示”Conneted“表示已经连接网络：

![](/img/20200512224049.png)



以上配置完成后，点击”Begin Install“开始安装：

![1589294533039](img/1589294533039.png)



在安装系统的时候，需要配置用户设置，需要配置root账号密码和普通用户：

![1589294732001](/img/1589294732001.png)



配置root密码，因为我们是做测试，所以可以设置一个简单的密码，如`123456`，两次输入root账号的密码后，按Done确认：

![](/img/20200512230417.png)



有时候，为了系统的安全，我们会禁止root账号远程登陆，此时有必要设置一个普通账号，并将其设置为超级用户，这样就可以使用这个超级用户账号远程登陆来管理服务器，因此我们创建一个普通账号：

![](/img/20200512230749.png)

注意，创建普通账号时，将”Make this user administrator“即将该用户配置为超级用户。



安装完成后，点击”Reboot“按钮重启虚拟机：

![](/img/20200513064659.png)



重启后，保持默认的”CentOS Linux(3.10.90-957.el7.x86_64) 7 (Core)“：

![](/img/20200513065012.png)

### 登陆CentOS7系统

首次进入系统时，需要输入登陆用户名和密码：

![](/img/20200513065234.png)

我们使用root账号和密码登陆：

![](/img/20200513065419.png)

### 检查CentOS7系统联网信息

我们首先检查虚拟机中是否能够ping通外网，如果通ping通外网，说明虚拟机能够正常访问外网。

#### 检查虚拟机是否能正常ping通外网

使用命令`ping -c 3 baidu.com`检查虚拟机是否能正常ping通外网：

![](/img/20200513065717.png)

可以看到，能够正常接收到外网返回的包，说明虚拟机能够正常访问外问。



#### 查看虚拟机IP信息，检查宿主机是否能够ping通虚拟机

首先获取虚拟机IP信息：

```sh
ip a show
```

![](/img/20200513070453.png)

此时可以发现`enp0s3`网络异常，`enp0s8`网络正常（正常显示了ip地址10.0.3.15）,我们检查一下`enp0s3`的网络配置：

![](/img/20200513070703.png)



可以发现`ONBOOT=no`说明没有配置为开机自启动，我们将`ONBOOT=no`改成`ONBOOT=yes`,执行下面的命令：

```sh
sed -i 's/ONBOOT=no/ONBOOT=yes/g' ifcfg-enp0s3
```

![1589325083976](/img/1589325083976.png)

运行`shutdown -r now`重启虚拟机,重启后，使用root账号和密码登陆，再次查看虚拟机IP信息：



![1589325208055](/img/1589325208055.png)



此时显示出IP地址为`192.168.56.7`,我们使用宿主机的`cmd`命令行尝试ping一下虚拟机：

![1589325349015](/img/1589325349015.png)

可以发现能够正常ping通虚拟机网络，说明宿主机和虚拟机之间网络是连通的，相互之间都能访问彼此！说明我们的网络现在配置正常了！

也可以在宿主机上面使用`ssh`连接虚拟机：

```sh
$ ssh root@192.168.56.7                                                           
The authenticity of host '192.168.56.7 (192.168.56.7)' can't be established.      
ECDSA key fingerprint is SHA256:AaS+AeTLXe3iqzGpn8vfqqoYtaO7bpsullHOxnj7kT8.      
Are you sure you want to continue connecting (yes/no)? yes                        
Warning: Permanently added '192.168.56.7' (ECDSA) to the list of known hosts.     
root@192.168.56.7's password:                                                     
Last login: Wed May 13 20:12:02 2020                                              
[root@localhost ~]# w                                                             
 20:12:57 up 2 min,  2 users,  load average: 0.18, 0.19, 0.08                     
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT               
root     tty1                      20:12   49.00s  0.02s  0.02s -bash             
root     pts/0    192.168.56.2     20:12    1.00s  0.03s  0.01s w                 
[root@localhost ~]#                                                               
```

说明宿主机和虚拟机之间的网络正常呢。

## CentOS7虚拟机静态IP配置

为了我们的虚拟机保持稳定的IP地址，我们给虚拟机配置一下静态IP。

根据前面的配置可知虚拟机的IP字段范围如下：

- 最小地址：192.168.56.3
- 最大地址：192.168.56.254

你可以使用`SecureCRT`或者`XShell`登陆到虚拟机，并进行以下操作。



- 查看当前的网络配置

```sh
[root@localhost ~]# cd /etc/sysconfig/network-scripts/
[root@localhost network-scripts]# ls
ifcfg-enp0s3  ifdown-ippp    ifdown-sit       ifup-bnep  ifup-plusb   ifup-TeamPort
ifcfg-enp0s8  ifdown-ipv6    ifdown-Team      ifup-eth   ifup-post    ifup-tunnel
ifcfg-lo      ifdown-isdn    ifdown-TeamPort  ifup-ippp  ifup-ppp     ifup-wireless
ifdown        ifdown-post    ifdown-tunnel    ifup-ipv6  ifup-routes  init.ipv6-global
ifdown-bnep   ifdown-ppp     ifup             ifup-isdn  ifup-sit     network-functions
ifdown-eth    ifdown-routes  ifup-aliases     ifup-plip  ifup-Team    network-functions-ipv6
[root@localhost network-scripts]# cat ifcfg-enp0s3       
TYPE=Ethernet                                            
PROXY_METHOD=none                                        
BROWSER_ONLY=no                                          
BOOTPROTO=dhcp                                           
DEFROUTE=yes                                             
IPV4_FAILURE_FATAL=no                                    
IPV6INIT=yes                                             
IPV6_AUTOCONF=yes                                        
IPV6_DEFROUTE=yes                                        
IPV6_FAILURE_FATAL=no                                    
IPV6_ADDR_GEN_MODE=stable-privacy                        
NAME=enp0s3                                              
UUID=b626df68-6af3-47e8-85ce-54b4f773ec01                
DEVICE=enp0s3                                            
ONBOOT=yes                                               
```

- 修改配置文件

将`BOOTPROTO=dhcp`改为`BOOTPROTO=static`,并且增加`IPADDR=192.168.56.3`，我们使用以下命令进行替换操作：

```sh
# 备份配置文件
[root@localhost network-scripts]# cp ifcfg-enp0s3 ifcfg-enp0s3.bak

# 替换dhcp为static，设置为静态IP
[root@localhost network-scripts]# sed -i 's/BOOTPROTO=dhcp/BOOTPROTO=static/g' ifcfg-enp0s3

# 尝试在文件最后增加一行，表示IP信息
[root@localhost network-scripts]# sed '$aIPADDR=192.168.56.3' ifcfg-enp0s3
TYPE=Ethernet 
PROXY_METHOD=none
BROWSER_ONLY=no  
BOOTPROTO=static 
DEFROUTE=yes  
IPV4_FAILURE_FATAL=no  
IPV6INIT=yes  
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no  
IPV6_ADDR_GEN_MODE=stable-privacy 
NAME=enp0s3
UUID=b626df68-6af3-47e8-85ce-54b4f773ec01 
DEVICE=enp0s3 
ONBOOT=yes 
IPADDR=192.168.56.3

# 将修改实际插入到文件中
[root@localhost network-scripts]# sed  -i '$aIPADDR=192.168.56.3' ifcfg-enp0s3

# 再次查看配置文件
[root@localhost network-scripts]# cat ifcfg-enp0s3 
TYPE=Ethernet 
PROXY_METHOD=none
BROWSER_ONLY=no  
BOOTPROTO=static 
DEFROUTE=yes  
IPV4_FAILURE_FATAL=no  
IPV6INIT=yes  
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no  
IPV6_ADDR_GEN_MODE=stable-privacy 
NAME=enp0s3
UUID=b626df68-6af3-47e8-85ce-54b4f773ec01 
DEVICE=enp0s3 
ONBOOT=yes 
IPADDR=192.168.56.3  
[root@localhost network-scripts]# 
```

- 重启网络

```sh
[root@localhost network-scripts]# systemctl restart network
```

此时，远程连接会断开，我们在VirutalBox的虚拟机界面使用`ip a show`查看配置是否生效：

![](/img/20200513205220.png)

使用XShell 6连接虚拟机：

![](/img/20200513205501.png)

可以看到可以正常连接！说明配置正确。



使用`shutdown -h now`将虚拟机关机！

至此，VirutalBox中安装的纯净CentOS7 mini版本配置完成了，可以使用VirtualBox的备份【系统快照】功能，给当前虚拟机设置一个快照，后续可以使用这个基本虚拟机创建其他虚拟机。

## 创建虚拟机快照

在虚拟机关机状态下，点击虚拟机的“备份[系统快照]”创建快照：

![1589375195020](/img/1589375195020.png)

点击“生成”，在弹出的“生成备份”界面中填写`备份名称`和`备份描述`，便于后期使用时选择备份时间点，如下图所示：

![1589375508986](/img/1589375508986.png)



后续我们就可以在该备份时间点处进行备份恢复或者复制到新的虚拟机：

![1589375879546](/img/1589375879546.png)



我们利用这个快照点可以创建新的虚拟机，如k8s节点，jumpServer堡垒机等等。


虚拟机安装成功后，可以配置以下常用命令：

```sh
# cat ~/.bashrc
# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
alias v.='vim ~/.bashrc'
alias s.='source ~/.bashrc && echo "Reload OK"'
alias vi='vim'
alias cdnet='pushd /etc/sysconfig/network-scripts/'
alias cd1='cd ..'
alias cd2='cd ../..'
alias cd3='cd ../../..'
alias cd4='cd ../../../..'
alias newhostname='hostnamectl set-hostname'
export LANG=en_US.UTF-8
alias addhosts="add_ip_parse"
function add_ip_parse(){
    ip=$1
    domain=$2
    simple=$(echo "${domain}"|awk -F'.' '{print $1}')
    echo -e "${ip}\t${domain}\t${simple}" >> /etc/hosts
}

alias setip='change_static_ip'
function change_static_ip() {
    new_ip=$1
    net_file="/etc/sysconfig/network-scripts/ifcfg-enp0s3"
    sed -i 's/BOOTPROTO=dhcp/BOOTPROTO=static/g' "${net_file}"
    echo "IPADDR=${new_ip}" >> "${net_file}"
    systemctl restart network
}
```

## virutalbox命令行

- `VBoxManage list vms` 列出所有虚拟机。
- `VBoxManage list runningvms` 显示正在运行的虚拟机。
- `VBoxManage startvm <vm_name> --type gui` 启动指定的虚拟机,与平时启动虚拟机相同。
- `VBoxManage startvm <vm_name> --type headless` 无GUI,在后台运行虚拟机，可以通过远程SSH连接，节省电脑资源。
- `VBoxManage controlvm <vm_name> acpipowerbutton` 正常关闭虚拟机。


示例：
```sh
# 列出所有虚拟机
[mzh@MacBookPro ~ ]$ VBoxManage list vms
"k8s-base" {5bb7eeb3-6f30-4a0a-a907-32ca8dd16f6b}
"src-host" {cb42eac9-0bb4-49c6-bef7-c334b7867ed3}
"dest-host" {a5507bbb-490e-433d-8412-e184286403ab}
"k8s-master" {2a783bfa-fafd-4910-aace-0af8dd3549ab}

# 列出正在运行的虚拟机，可以看到，此时没有运行虚拟机
[mzh@MacBookPro ~ ]$ VBoxManage list runningvms

# 正常启动虚拟机
[mzh@MacBookPro ~ ]$ VBoxManage startvm "k8s-master" --type gui
Waiting for VM "k8s-master" to power on...
VM "k8s-master" has been successfully started.
[mzh@MacBookPro ~ ]$
```
此时，使用`活动监视器`查看virtualbox应用cpu/内存占用情况：

cpu占用：
![](/img/Snipaste_2022-11-21_20-21-07.png)
内存占用：
![](/img/Snipaste_2022-11-21_20-21-54.png)

停止虚拟机：
```sh
[mzh@MacBookPro ~ ]$ VBoxManage controlvm "k8s-master" acpipowerbutton
[mzh@MacBookPro ~ ]$
```

再用无GUI模式启动虚拟机：
```sh
[mzh@MacBookPro ~ ]$ VBoxManage startvm "k8s-master" --type headless
Waiting for VM "k8s-master" to power on...
VM "k8s-master" has been successfully started.
[mzh@MacBookPro ~ ]$
```
此时，cpu占用情况：
![](/img/Snipaste_2022-11-21_20-27-49.png)
内存占用情况：
![](/img/Snipaste_2022-11-21_20-28-26.png)
可以看到CPU占用从18.8%下降到8.2%,内存占用从2.73GB下降到2.55GB，可以节省一些主机资源。

参考：



- [virtualbox安装centos并设置静态IP](https://blog.csdn.net/asdf_1234_/article/details/91470680)

