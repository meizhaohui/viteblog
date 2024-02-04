# K8S集群部署

## 1. 虚拟机基本配置

我们先在VirtualBox中创建一个基本的CentOS7虚拟机。然后在该基础虚拟机上面进行一些配置。作为一个基础的虚拟机。

### 1.1 虚拟机硬件配置

虚拟机使用双网卡：

- 网卡1，仅主机(Host-Only)网络。
- 网卡2，网络地址转换(NAT)。

内存大小：2048MB。

处理器数量：2 CPU。

虚拟分配空间： 20 GB。

### 1.2 虚拟机软件配置

CentOS系统安装成功后，在部署K8S集群前，先对虚拟机进行以下配置：

完成基本的配置：
1. 时间同步，使用`chronyd`服务同步时间。

2. 时区设置，设置为亚洲/上海。

3. 关闭防火墙，关闭`firewalld`服务。

4. 关闭SELinux，设置`SELINUX=disabled`。

5. 关闭SWAP，使用`swapoff -a`关闭SWAP。

6. 安装基本软件，如vim,jq,python,docker等

7. vim配置

8. 快捷命令配置

9. 允许 iptables 检查桥接流量

使用以下脚本：

```sh
#!/bin/bash
# filename: k8s_pre_install_init.sh
# Author: meizhaohui
# Date: 2021-07-29 23:25:28
echo “Config yum”
echo "Install EPEL yum"
yum install -y epel-release
sed -e 's!^metalink=!#metalink=!g' \
    -e 's!^#baseurl=!baseurl=!g' \
    -e 's!//download\.fedoraproject\.org/pub!//mirrors.tuna.tsinghua.edu.cn!g' \
    -e 's!http://mirrors!https://mirrors!g' \
    -i /etc/yum.repos.d/epel.repo /etc/yum.repos.d/epel-testing.repo

sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e 's|^#baseurl=http://mirror.centos.org|baseurl=https://mirrors.tuna.tsinghua.edu.cn|g' \
    -i.bak \
    /etc/yum.repos.d/CentOS-Base.repo

echo "Install IUS yum"
yum install -y https://repo.ius.io/ius-release-el7.rpm

echo "Set yum tools"
yum install -y deltarpm yum-utils device-mapper-persistent-data lvm2 lrzsz net-tools wget

echo "Set Aliyun Docker yum mirror"
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

yum install -y vim git224 jq deltarpm python3 go wget

echo "Config vimrc"
cat >> ~/.vimrc << EOF
syntax on
filetype plugin indent on
set hlsearch
set backspace=2
set autoindent
set ruler
set showmode
set nu
set bg=dark
set ts=4
set softtabstop=4
set shiftwidth=4
set fileencodings=utf-8,gbk,gb18030,gk2312
set showcmd
set clipboard+=unnamed
set cursorline
set confirm
set autoindent
set cindent
set expandtab
set laststatus=2
EOF


echo "Config .bashrc"
cat >> ~/.bashrc << EOF
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
alias setip='change_ip'
function change_ip(){
    node_ip=\$1
    config_folder="/etc/sysconfig/network-scripts"
    ip_config=\$(grep 'IPADDR' "\${config_folder}"/ifcfg-*|grep -v 'ifcfg-lo'|awk -F":" '{print \$1}')
    sed -i.bak "s/IPADDR.*/IPADDR=\"\$node_ip\"/g" "\${ip_config}"
}
alias addhosts="add_ip_parse"
function add_ip_parse(){
    ip=\$1
    domain=\$2
    simple=\$(echo "\${domain}"|awk -F'.' '{print \$1}')
    echo -e "\${ip}\t\${domain}\t\${simple}" >> /etc/hosts
}
alias ping='ping -c 3'
alias ip='hostname -I'
# sync time
alias st='systemctl restart chronyd && chronyc sources -v'
EOF


echo "Install Docker"
yum install -y docker-ce docker-ce-cli containerd.io

echo "Start Docker"
sed -i.bak '/ExecStart=\/usr\/bin\/dockerd/aExecStartPost=/usr/sbin/iptables -P FORWARD ACCEPT' /usr/lib/systemd/system/docker.service
systemctl daemon-reload
systemctl enable docker
systemctl start docker
echo "Config Docker mirror"
cat >> /etc/docker/daemon.json << EOF
{"registry-mirrors":["https://reg-mirror.qiniu.com/"]}
EOF
systemctl restart docker
systemctl status docker

echo "Stop Firewall"
systemctl stop firewalld
systemctl disable firewalld

echo "Disable SWAP"
swapoff -a
swapstatus=$(grep -v 'Filename' /proc/swaps |wc -l)
if [[ "${swapstatus}" -eq 0 ]]; then
    sed -i.bak '/ swap /s/^#*/# /' /etc/fstab
    echo "SWAP disabled!"
fi

echo "Disable SELinux"
setenforce 0
sed -i.bak 's/^SELINUX.*/SELINUX=disabled/g' /etc/selinux/config
getenforce

echo "Sync time"
yum -y install chrony
systemctl enable chronyd
systemctl start chronyd
systemctl status chronyd

echo "Set iptables"
# 允许 iptables 检查桥接流量
cat > /etc/modules-load.d/k8s.conf << EOF
br_netfilter
EOF

cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

# 使配置生效
sysctl --system

echo "Please use command 'setip' to change the IP and 'addhosts' to add new domain parse!!!"
echo "Done!"

```

## 2. 虚拟机配置

虚拟机系统信息：

```sh
[root@master ~]# cat /etc/centos-release
CentOS Linux release 7.7.1908 (Core)
[root@master ~]# 
```



我们在VirtualBox中复制几个刚才创建的虚拟机，并分别使用`setip`、`sethostname`命令修改虚拟机IP和主机名称，并设置节点名称解析。

我计划设置一个master和两个节点,IP和域名对应关系如下：

```
192.168.56.60 master.mytest.com
192.168.56.61 node1.mytest.com
192.168.56.62 node2.mytest.com
```

设置后重启虚拟机，查看IP、主机名和名称解析:

```sh
[root@master ~]# hostname -I
192.168.56.60 172.17.0.1 
[root@master ~]# hostname 
master.mytest.com
[root@master ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.56.60 master.mytest.com master kubeapi.mytest.com kubeapi k8s-master
192.168.56.61 node1.mytest.com node1 k8s-node1
192.168.56.62 node2.mytest.com node2 k8s-node2
```

此时，对k8s测试虚拟机进行备份，生成相应的快照。快照名称为`k8s_0`，并且描述信息为"k8s安装k8s前，配置好各节点IP和域名"。这样后面做测试时，可以快速恢复到该快照，不需要重新安装系统配置网络等。

![](/img/20210812135252.png)

启动三台虚拟机。



## 3. 安装k8s集群

### 3.1 修改Docker的CGroup的驱动

**提示：以下操作需要在本示例中的所有3台虚拟机上分别进行。**

参考： [部署v1.20版的Kubernetes集群](https://mp.weixin.qq.com/s/dMygLTxvdUEieQsaQ2RGLA)

kubelet需要让docker容器引擎使用systemd作为CGroup的驱动，其默认值为cgroupfs，因而，我们还需要编辑docker的配置文件/etc/docker/daemon.json，添加内容`"exec-opts": ["native.cgroupdriver=systemd"]`。添加完成后，查看docker的配置文件：

```sh
[root@master ~]# cat /etc/docker/daemon.json 
{
    "registry-mirrors": ["https://reg-mirror.qiniu.com/"],
    "exec-opts": ["native.cgroupdriver=systemd"]
}
[root@master ~]# 
```

修改后，重启docker服务：

```sh
[root@master ~]# systemctl restart docker
[root@master ~]# systemctl status docker
● docker.service - Docker Application Container Engine
   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2021-08-12 14:38:00 CST; 8s ago
     Docs: https://docs.docker.com
  Process: 32491 ExecStartPost=/usr/sbin/iptables -P FORWARD ACCEPT (code=exited, status=0/SUCCESS)
 Main PID: 32361 (dockerd)
    Tasks: 8
   Memory: 31.9M
   CGroup: /system.slice/docker.service
           └─32361 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

Aug 12 14:38:00 master.mytest.com dockerd[32361]: time="2021-08-12T14:38:00.291438542+08:00" level=info msg="ccResolverWra...e=grpc
Aug 12 14:38:00 master.mytest.com dockerd[32361]: time="2021-08-12T14:38:00.291447604+08:00" level=info msg="ClientConn sw...e=grpc
Aug 12 14:38:00 master.mytest.com dockerd[32361]: time="2021-08-12T14:38:00.302327988+08:00" level=info msg="[graphdriver]...rlay2"
Aug 12 14:38:00 master.mytest.com dockerd[32361]: time="2021-08-12T14:38:00.307250795+08:00" level=info msg="Loading conta...tart."
Aug 12 14:38:00 master.mytest.com dockerd[32361]: time="2021-08-12T14:38:00.412650926+08:00" level=info msg="Default bridg...dress"
Aug 12 14:38:00 master.mytest.com dockerd[32361]: time="2021-08-12T14:38:00.456379139+08:00" level=info msg="Loading conta...done."
Aug 12 14:38:00 master.mytest.com dockerd[32361]: time="2021-08-12T14:38:00.473722675+08:00" level=info msg="Docker daemon...0.10.8
Aug 12 14:38:00 master.mytest.com dockerd[32361]: time="2021-08-12T14:38:00.473786016+08:00" level=info msg="Daemon has co...ation"
Aug 12 14:38:00 master.mytest.com systemd[1]: Started Docker Application Container Engine.
Aug 12 14:38:00 master.mytest.com dockerd[32361]: time="2021-08-12T14:38:00.495967020+08:00" level=info msg="API listen on....sock"
Hint: Some lines were ellipsized, use -l to show in full.
[root@master ~]# 
```

### 3.2 添加kubernetes的YUM源

参考：[Kubernetes 镜像](https://developer.aliyun.com/mirror/kubernetes?spm=a2c6h.13651102.0.0.3e221b118BVyvx)

在三台虚拟机上执行以下命令：

```sh
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```

然后查看一下`/etc/yum.repos.d/kubernetes.repo`文件：

```sh
[root@master ~]# cat /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
[root@master ~]# 
```

由于官网未开放同步方式, 可能会有索引gpg检查失败的情况, 这时请用 `yum install -y --nogpgcheck kubelet kubeadm kubectl` 安装。

### 3.3 安装kubectl、kubelet和kubeadm

由于kubernetes官方更新比较快，2021年8月份已经发布到v1.22版本了，为了便于后期能够在网上搜索资料，我不用最新版本的，使用`v1.18`版本。

我们先看一下仓库中有哪些版本：

```sh
[root@master ~]# yum search kubelet --showduplicates|tail -n 40
kubelet-1.18.10-0.x86_64 : Container cluster management
kubelet-1.18.12-0.x86_64 : Container cluster management
kubelet-1.18.13-0.x86_64 : Container cluster management
kubelet-1.18.14-0.x86_64 : Container cluster management
kubelet-1.18.15-0.x86_64 : Container cluster management
kubelet-1.18.16-0.x86_64 : Container cluster management
kubelet-1.18.17-0.x86_64 : Container cluster management
kubelet-1.18.18-0.x86_64 : Container cluster management
kubelet-1.18.19-0.x86_64 : Container cluster management
kubelet-1.18.20-0.x86_64 : Container cluster management
kubelet-1.19.0-0.x86_64 : Container cluster management
kubelet-1.19.1-0.x86_64 : Container cluster management
kubelet-1.19.2-0.x86_64 : Container cluster management
kubelet-1.19.3-0.x86_64 : Container cluster management
kubelet-1.19.4-0.x86_64 : Container cluster management
kubelet-1.19.5-0.x86_64 : Container cluster management
kubelet-1.19.6-0.x86_64 : Container cluster management
kubelet-1.19.7-0.x86_64 : Container cluster management
kubelet-1.19.8-0.x86_64 : Container cluster management
kubelet-1.19.9-0.x86_64 : Container cluster management
kubelet-1.19.10-0.x86_64 : Container cluster management
kubelet-1.19.11-0.x86_64 : Container cluster management
kubelet-1.19.12-0.x86_64 : Container cluster management
kubelet-1.19.13-0.x86_64 : Container cluster management
kubelet-1.20.0-0.x86_64 : Container cluster management
kubelet-1.20.1-0.x86_64 : Container cluster management
kubelet-1.20.2-0.x86_64 : Container cluster management
kubelet-1.20.4-0.x86_64 : Container cluster management
kubelet-1.20.5-0.x86_64 : Container cluster management
kubelet-1.20.6-0.x86_64 : Container cluster management
kubelet-1.20.7-0.x86_64 : Container cluster management
kubelet-1.20.8-0.x86_64 : Container cluster management
kubelet-1.20.9-0.x86_64 : Container cluster management
kubelet-1.21.0-0.x86_64 : Container cluster management
kubelet-1.21.1-0.x86_64 : Container cluster management
kubelet-1.21.2-0.x86_64 : Container cluster management
kubelet-1.21.3-0.x86_64 : Container cluster management
kubelet-1.22.0-0.x86_64 : Container cluster management

  Name and summary matches only, use "search all" for everything.
[root@master ~]# 
```

我们安装`kubelet-1.18.20`这个版本。使用相同的方法，可以知道，`kubeadm`和`kubelet`也有相同的版本。

我们直接安装指定版本的kubernetes软件包：

```sh
[root@master ~]# yum install -y --nogpgcheck kubectl-1.18.20 kubelet-1.18.20 kubeadm-1.18.20
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package kubeadm.x86_64 0:1.18.20-0 will be installed
--> Processing Dependency: kubernetes-cni >= 0.8.6 for package: kubeadm-1.18.20-0.x86_64
--> Processing Dependency: cri-tools >= 1.13.0 for package: kubeadm-1.18.20-0.x86_64
---> Package kubectl.x86_64 0:1.18.20-0 will be installed
---> Package kubelet.x86_64 0:1.18.20-0 will be installed
--> Processing Dependency: socat for package: kubelet-1.18.20-0.x86_64
--> Processing Dependency: conntrack for package: kubelet-1.18.20-0.x86_64
--> Running transaction check
---> Package conntrack-tools.x86_64 0:1.4.4-7.el7 will be installed
--> Processing Dependency: libnetfilter_cttimeout.so.1(LIBNETFILTER_CTTIMEOUT_1.1)(64bit) for package: conntrack-tools-1.4.4-7.el7.x86_64
--> Processing Dependency: libnetfilter_cttimeout.so.1(LIBNETFILTER_CTTIMEOUT_1.0)(64bit) for package: conntrack-tools-1.4.4-7.el7.x86_64
--> Processing Dependency: libnetfilter_cthelper.so.0(LIBNETFILTER_CTHELPER_1.0)(64bit) for package: conntrack-tools-1.4.4-7.el7.x86_64
--> Processing Dependency: libnetfilter_queue.so.1()(64bit) for package: conntrack-tools-1.4.4-7.el7.x86_64
--> Processing Dependency: libnetfilter_cttimeout.so.1()(64bit) for package: conntrack-tools-1.4.4-7.el7.x86_64
--> Processing Dependency: libnetfilter_cthelper.so.0()(64bit) for package: conntrack-tools-1.4.4-7.el7.x86_64
---> Package cri-tools.x86_64 0:1.13.0-0 will be installed
---> Package kubernetes-cni.x86_64 0:0.8.7-0 will be installed
---> Package socat.x86_64 0:1.7.3.2-2.el7 will be installed
--> Running transaction check
---> Package libnetfilter_cthelper.x86_64 0:1.0.0-11.el7 will be installed
---> Package libnetfilter_cttimeout.x86_64 0:1.0.0-7.el7 will be installed
---> Package libnetfilter_queue.x86_64 0:1.0.2-2.el7_2 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

===================================================================================================================================
 Package                                 Arch                    Version                         Repository                   Size
===================================================================================================================================
Installing:
 kubeadm                                 x86_64                  1.18.20-0                       kubernetes                  8.8 M
 kubectl                                 x86_64                  1.18.20-0                       kubernetes                  9.5 M
 kubelet                                 x86_64                  1.18.20-0                       kubernetes                   21 M
Installing for dependencies:
 conntrack-tools                         x86_64                  1.4.4-7.el7                     base                        187 k
 cri-tools                               x86_64                  1.13.0-0                        kubernetes                  5.1 M
 kubernetes-cni                          x86_64                  0.8.7-0                         kubernetes                   19 M
 libnetfilter_cthelper                   x86_64                  1.0.0-11.el7                    base                         18 k
 libnetfilter_cttimeout                  x86_64                  1.0.0-7.el7                     base                         18 k
 libnetfilter_queue                      x86_64                  1.0.2-2.el7_2                   base                         23 k
 socat                                   x86_64                  1.7.3.2-2.el7                   base                        290 k

Transaction Summary
===================================================================================================================================
Install  3 Packages (+7 Dependent packages)

Total download size: 63 M
Installed size: 266 M
。。。省略
Installed:
  kubeadm.x86_64 0:1.18.20-0                 kubectl.x86_64 0:1.18.20-0                 kubelet.x86_64 0:1.18.20-0                

Dependency Installed:
  conntrack-tools.x86_64 0:1.4.4-7.el7                             cri-tools.x86_64 0:1.13.0-0                                     
  kubernetes-cni.x86_64 0:0.8.7-0                                  libnetfilter_cthelper.x86_64 0:1.0.0-11.el7                     
  libnetfilter_cttimeout.x86_64 0:1.0.0-7.el7                      libnetfilter_queue.x86_64 0:1.0.2-2.el7_2                       
  socat.x86_64 0:1.7.3.2-2.el7                                    

Complete!
[root@master ~]# 
```

查看kubernetes软件安装情况：

```sh
[root@master ~]# rpm -qa|grep kube
kubelet-1.18.20-0.x86_64
kubectl-1.18.20-0.x86_64
kubernetes-cni-0.8.7-0.x86_64
kubeadm-1.18.20-0.x86_64
[root@master ~]# kubelet --version
Kubernetes v1.18.20
[root@master ~]# kubeadm version -o=short
v1.18.20
[root@master ~]# kubectl version --short=true
Client Version: v1.18.20
The connection to the server localhost:8080 was refused - did you specify the right host or port?
[root@master ~]#
```

可以看到，kubernetes相关的几个命令都能正常使用，并且版本也是我们指定的`v1.18.20`。

为了方便后续执行命令，我们可以设置快捷命令：
```sh
alias k8let='kubelet'
alias k8adm='kubeadm'
alias k8ctl='kubectl'
```

使用命令`yum install -y --nogpgcheck kubectl-1.18.20 kubelet-1.18.20 kubeadm-1.18.20`在各节点上安装相应的软件包。

这样我们的kubernetes软件包就安装完成了。



另外，我们设置一下`kubelet`开机启动：

```sh
[root@master ~]# systemctl enable kubelet
Created symlink from /etc/systemd/system/multi-user.target.wants/kubelet.service to /usr/lib/systemd/system/kubelet.service.
[root@master ~]# 
```

此时不要直接启动`kubelet`，因为其配置文件还没有生成。



### 3.4 在master上进行集群初始化

现在我们只用在master虚拟机上面进行集群的初始化。

> 该步骤开始尝试构建Kubernetes集群的master节点，配置完成后，各worker节点直接加入到集群中的即可。需要特别说明的是，由kubeadm部署的Kubernetes集群上，集群核心组件kube-apiserver、kube-controller-manager、kube-scheduler和etcd等均会以静态Pod的形式运行，它们所依赖的镜像文件默认来自于gcr.io这一Registry服务之上。但我们无法直接访问该服务，常用的解决办法有如下两种，本示例将选择使用更易于使用的后一种方式。
>
> - 使用能够到达该服务的代理服务；
> - 使用国内的镜像服务器上的服务，例如gcr.azk8s.cn/google_containers和registry.aliyuncs.com/google_containers等 。

#### 3.4.1 拉取镜像

在运行初始化命令之前先运行如下命令单独获取相关的镜像文件，而后再运行后面的`kubeadm init`命令，以便于观察到镜像文件的下载过程。

查看镜像列表：

```sh
kubeadm config images list --image-repository registry.aliyuncs.com/google_containers
```

执行：

```sh
[root@master ~]# kubeadm config images list --image-repository registry.aliyuncs.com/google_containers
I0812 15:40:30.984989   29210 version.go:255] remote version is much newer: v1.22.0; falling back to: stable-1.18
W0812 15:40:33.317410   29210 configset.go:202] WARNING: kubeadm cannot validate component configs for API groups [kubelet.config.k8s.io kubeproxy.config.k8s.io]
registry.aliyuncs.com/google_containers/kube-apiserver:v1.18.20
registry.aliyuncs.com/google_containers/kube-controller-manager:v1.18.20
registry.aliyuncs.com/google_containers/kube-scheduler:v1.18.20
registry.aliyuncs.com/google_containers/kube-proxy:v1.18.20
registry.aliyuncs.com/google_containers/pause:3.2
registry.aliyuncs.com/google_containers/etcd:3.4.3-0
registry.aliyuncs.com/google_containers/coredns:1.6.7
[root@master ~]# 
```

可以看到，该镜像仓库中有多个镜像。



拉取镜像文件：

```sh
kubeadm config images pull --image-repository registry.aliyuncs.com/google_containers
```

执行：

```sh
# 在拉取镜像前，查看docker的镜像列表
[root@master ~]# docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE

# 拉取镜像
[root@master ~]# kubeadm config images pull  --image-repository registry.aliyuncs.com/google_containers
I0812 15:44:28.995830   12325 version.go:255] remote version is much newer: v1.22.0; falling back to: stable-1.18
W0812 15:44:31.565048   12325 configset.go:202] WARNING: kubeadm cannot validate component configs for API groups [kubelet.config.k8s.io kubeproxy.config.k8s.io]
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-apiserver:v1.18.20
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-controller-manager:v1.18.20
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-scheduler:v1.18.20
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-proxy:v1.18.20
[config/images] Pulled registry.aliyuncs.com/google_containers/pause:3.2
[config/images] Pulled registry.aliyuncs.com/google_containers/etcd:3.4.3-0
[config/images] Pulled registry.aliyuncs.com/google_containers/coredns:1.6.7

# 查看命令是否正常退出
[root@master ~]# echo $?
0

# 再次查看docker的镜像
[root@master ~]# docker images
REPOSITORY                                                        TAG        IMAGE ID       CREATED         SIZE
registry.aliyuncs.com/google_containers/kube-proxy                v1.18.20   27f8b8d51985   8 weeks ago     117MB
registry.aliyuncs.com/google_containers/kube-apiserver            v1.18.20   7d8d2960de69   8 weeks ago     173MB
registry.aliyuncs.com/google_containers/kube-scheduler            v1.18.20   a05a1a79adaa   8 weeks ago     96.1MB
registry.aliyuncs.com/google_containers/kube-controller-manager   v1.18.20   e7c545a60706   8 weeks ago     162MB
registry.aliyuncs.com/google_containers/pause                     3.2        80d28bedfe5d   18 months ago   683kB
registry.aliyuncs.com/google_containers/coredns                   1.6.7      67da37a9a360   18 months ago   43.8MB
registry.aliyuncs.com/google_containers/etcd                      3.4.3-0    303ce5db0e90   21 months ago   288MB
[root@master ~]# docker images|wc -l
8
[root@master ~]# 
```

可以看到docker的镜像已经拉取到本地了。



#### 3.4.2 集群初始化

执行以下命令：

```sh
kubeadm init \
    --kubernetes-version=v1.18.20 \
    --apiserver-advertise-address=192.168.56.60 \
    --image-repository registry.aliyuncs.com/google_containers \
    --control-plane-endpoint kubeapi.mytest.com \
    --pod-network-cidr=10.244.0.0/16 \
    --service-cidr=10.96.0.0/12 \
    --token-ttl=0
```

> 命令中的各选项简单说明如下： 
>
> - --image-repository：指定要使用的镜像仓库，默认为gcr.io；
>
> - --kubernetes-version：kubernetes程序组件的版本号，它必须要与安装的kubelet程序包的版本号相同；
>
> - --control-plane-endpoint：控制平面的固定访问端点，可以是IP地址或DNS名称，会被用于集群管理员及集群组件的kubeconfig配置文件的API Server的访问地址；单控制平面部署时可以不使用该选项；
>
> - --pod-network-cidr：Pod网络的地址范围，其值为CIDR格式的网络地址，通常，Flannel网络插件的默认为10.244.0.0/16，Project Calico插件的默认值为192.168.0.0/16；
>
> - --service-cidr：Service的网络地址范围，其值为CIDR格式的网络地址，默认为10.96.0.0/12；通常，仅Flannel一类的网络插件需要手动指定该地址；
>
> - --apiserver-advertise-address：apiserver通告给其他组件的IP地址，一般应该为Master节点的用于集群内部通信的IP地址，0.0.0.0表示节点上所有可用地址；
>
> - --token-ttl：共享令牌（token）的过期时长，默认为24小时，0表示永不过期；为防止不安全存储等原因导致的令牌泄露危及集群安全，建议为其设定过期时长。未设定该选项时，在token过期后，若期望再向集群中加入其它节点，可以使用如下命令重新创建token，并生成节点加入命令。
>
>     ```sh
>     kubeadm token create --print-join-command
>     ```

执行：

```sh
[root@master ~]# kubeadm init \
>     --kubernetes-version=v1.18.20 \
>     --apiserver-advertise-address=192.168.56.60 \
>     --image-repository registry.aliyuncs.com/google_containers  \
>     --control-plane-endpoint kubeapi.mytest.com \
>     --pod-network-cidr=10.244.0.0/16 \
>     --service-cidr=10.96.0.0/12 \
>     --token-ttl=0
W0812 16:11:06.680875    6714 configset.go:202] WARNING: kubeadm cannot validate component configs for API groups [kubelet.config.k8s.io kubeproxy.config.k8s.io]
[init] Using Kubernetes version: v1.18.20

# 梅朝辉注释： 步骤1：进行预检查，看环境是否满足要求，如CPU需要2核、SWAP需要关闭等等
# 此处提示一个警告，该版本的Docker未经过验证
[preflight] Running pre-flight checks
        [WARNING SystemVerification]: this Docker version is not on the list of validated versions: 20.10.8. Latest validated version: 19.03

# 梅朝辉注释： 步骤2：下载k8s集群需要的镜像
# 我们在上一节已经拉取了镜像，此处初始化就会缩短时间，通过提前拉取镜像，可以看到镜像是否能够拉取成功
# 避免在集群初始化时出现异常
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'

# 梅朝辉注释： 步骤3：启动kubelet组件，并准备kubelet的配置文件
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Starting the kubelet

# 梅朝辉注释： 步骤4： 生成证书,存放在/etc/kubernetes/pki目录下
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [master.mytest.com kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local kubeapi.mytest.com] and IPs [10.96.0.1 192.168.56.60]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [master.mytest.com localhost] and IPs [192.168.56.60 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [master.mytest.com localhost] and IPs [192.168.56.60 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key


# 梅朝辉注释： 步骤5：生成kubeconfig配置文件
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file

# 梅朝辉注释： 步骤6：控制面板，以静态Pod的形式启动APIServer和Controller-Manager
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
W0812 16:11:12.395441    6714 manifests.go:225] the default kube-apiserver authorization-mode is "Node,RBAC"; using "Node,RBAC"
[control-plane] Creating static Pod manifest for "kube-scheduler"
W0812 16:11:12.396611    6714 manifests.go:225] the default kube-apiserver authorization-mode is "Node,RBAC"; using "Node,RBAC"

# 梅朝辉注释： 步骤7：以静态Pod的形式启动etcd
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"

# 梅朝辉注释： 步骤8： 等待控制面板启动
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s

# 梅朝辉注释：所有控制面板组件都是健康的
[apiclient] All control plane components are healthy after 20.512808 seconds

# 梅朝辉注释： 步骤9： 存储kubelet配置文件到ConfigMap中 
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config-1.18" in namespace kube-system with the configuration for the kubelets in the cluster

# 梅朝辉注释：证书上传，忽略
[upload-certs] Skipping phase. Please see --upload-certs

# 梅朝辉注释：步骤10： 给master节点添加标签，标记污点，后续创建Pod时，不会分配到master节点上
[mark-control-plane] Marking the node master.mytest.com as control-plane by adding the label "node-role.kubernetes.io/master=''"
[mark-control-plane] Marking the node master.mytest.com as control-plane by adding the taints [node-role.kubernetes.io/master:NoSchedule]

# 梅朝辉注释：步骤11： 引导TOKEN，配置bootstrap tls，给节点自动颁发证书
[bootstrap-token] Using token: ntf08x.uaudrocid80akszx
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[kubelet-finalize] Updating "/etc/kubernetes/kubelet.conf" to point to a rotatable kubelet client certificate and key

# 梅朝辉注释：步骤12： 安装插件，CoreDNS为K8S集群中做内部解析的，Kube-Proxy是负责Pod的网络的 
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

# 梅朝辉注释：k8s控制平面初始化成功
Your Kubernetes control-plane has initialized successfully!

# 梅朝辉注释：用户需要执行的步骤1：复制配置文件,使得可以使用kubectl命令。
# 如果不拷贝，则不能使用`kubectl get node`查看集群节点信息，此时是直接没有权限的
To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

# 梅朝辉注释：用户可选的步骤1：添加其他控制平面节点，这样可以将集群升级为高可用。
You can now join any number of control-plane nodes by copying certificate authorities
and service account keys on each node and then running the following as root:

  kubeadm join kubeapi.mytest.com:6443 --token ntf08x.uaudrocid80akszx \
    --discovery-token-ca-cert-hash sha256:e60ab1ae8fcc0f8b8d3d2256c59738723a7ad04bee1aa0c0a1d8256bc62b4293 \
    --control-plane 


# 梅朝辉注释：用户需要执行的步骤2：在节点中执行命令，将节点加入到集群中，注意，该需要需要在node节点中执行
Then you can join any number of worker nodes by running the following on each as root:

kubeadm join kubeapi.mytest.com:6443 --token ntf08x.uaudrocid80akszx \
    --discovery-token-ca-cert-hash sha256:e60ab1ae8fcc0f8b8d3d2256c59738723a7ad04bee1aa0c0a1d8256bc62b4293 
[root@master ~]# echo $?
0
[root@master ~]# 
```

执行集群初始化时，会经过多个步骤，各个步骤的解释，详见上面命令行操作中的备注信息。

如果此处你想初始化失败，可以使用`kubeadm reset`来重置k8s集群，并且需要执行以下命令来删除相关文件：
```sh
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
ipvsadm --clear
systemctl stop kubelet
systemctl stop docker
rm -rf /var/lib/cni/*
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/*
rm -rf $HOME/.kube/config
systemctl start docker
```

#### 3.4.3  验证k8s集群初始化过程(可忽略)

- 查看kubelet的配置文件

```sh
[root@master ~]# cat /var/lib/kubelet/kubeadm-flags.env
KUBELET_KUBEADM_ARGS="--cgroup-driver=systemd --network-plugin=cni --pod-infra-container-image=registry.aliyuncs.com/google_containers/pause:3.2"
[root@master ~]# 
[root@master ~]# cat -n /var/lib/kubelet/config.yaml 
     1  apiVersion: kubelet.config.k8s.io/v1beta1
     2  authentication:
     3    anonymous:
     4      enabled: false
     5    webhook:
     6      cacheTTL: 0s
     7      enabled: true
     8    x509:
     9      clientCAFile: /etc/kubernetes/pki/ca.crt
    10  authorization:
    11    mode: Webhook
    12    webhook:
    13      cacheAuthorizedTTL: 0s
    14      cacheUnauthorizedTTL: 0s
    15  clusterDNS:
    16  - 10.96.0.10
    17  clusterDomain: cluster.local
    18  cpuManagerReconcilePeriod: 0s
    19  evictionPressureTransitionPeriod: 0s
    20  fileCheckFrequency: 0s
    21  healthzBindAddress: 127.0.0.1
    22  healthzPort: 10248
    23  httpCheckFrequency: 0s
    24  imageMinimumGCAge: 0s
    25  kind: KubeletConfiguration
    26  nodeStatusReportFrequency: 0s
    27  nodeStatusUpdateFrequency: 0s
    28  rotateCertificates: true
    29  runtimeRequestTimeout: 0s
    30  staticPodPath: /etc/kubernetes/manifests
    31  streamingConnectionIdleTimeout: 0s
    32  syncFrequency: 0s
    33  volumeStatsAggPeriod: 0s
[root@master ~]# 
```

- 查看证书列表

```sh
[root@master ~]# ls -lh /etc/kubernetes/pki/
total 56K
-rw-r--r-- 1 root root 1.3K Aug 12 16:11 apiserver.crt
-rw-r--r-- 1 root root 1.1K Aug 12 16:11 apiserver-etcd-client.crt
-rw------- 1 root root 1.7K Aug 12 16:11 apiserver-etcd-client.key
-rw------- 1 root root 1.7K Aug 12 16:11 apiserver.key
-rw-r--r-- 1 root root 1.1K Aug 12 16:11 apiserver-kubelet-client.crt
-rw------- 1 root root 1.7K Aug 12 16:11 apiserver-kubelet-client.key
-rw-r--r-- 1 root root 1.1K Aug 12 16:11 ca.crt
-rw------- 1 root root 1.7K Aug 12 16:11 ca.key
drwxr-xr-x 2 root root  162 Aug 12 16:11 etcd
-rw-r--r-- 1 root root 1.1K Aug 12 16:11 front-proxy-ca.crt
-rw------- 1 root root 1.7K Aug 12 16:11 front-proxy-ca.key
-rw-r--r-- 1 root root 1.1K Aug 12 16:11 front-proxy-client.crt
-rw------- 1 root root 1.7K Aug 12 16:11 front-proxy-client.key
-rw------- 1 root root 1.7K Aug 12 16:11 sa.key
-rw------- 1 root root  451 Aug 12 16:11 sa.pub
[root@master ~]# ls -lh /etc/kubernetes/pki/etcd/
total 32K
-rw-r--r-- 1 root root 1017 Aug 12 16:11 ca.crt
-rw------- 1 root root 1.7K Aug 12 16:11 ca.key
-rw-r--r-- 1 root root 1.1K Aug 12 16:11 healthcheck-client.crt
-rw------- 1 root root 1.7K Aug 12 16:11 healthcheck-client.key
-rw-r--r-- 1 root root 1.2K Aug 12 16:11 peer.crt
-rw------- 1 root root 1.7K Aug 12 16:11 peer.key
-rw-r--r-- 1 root root 1.2K Aug 12 16:11 server.crt
-rw------- 1 root root 1.7K Aug 12 16:11 server.key
[root@master ~]# 
```

可以看到，生成了非常多的证书文件。

- 查看kubeconfig配置文件

```sh
[root@master ~]# ls -lh /etc/kubernetes/
total 32K
-rw------- 1 root root 5.4K Aug 12 16:11 admin.conf
-rw------- 1 root root 5.4K Aug 12 16:11 controller-manager.conf
-rw------- 1 root root 1.9K Aug 12 16:11 kubelet.conf
drwxr-xr-x 2 root root  113 Aug 12 16:11 manifests
drwxr-xr-x 3 root root 4.0K Aug 12 16:11 pki
-rw------- 1 root root 5.4K Aug 12 16:11 scheduler.conf
[root@master ~]# 
```

由于`kubeadm init`最后让复制`/etc/kubernetes/admin.conf`配置文件，我们先备份一下该文件：

```sh
[root@master ~]# cp /etc/kubernetes/admin.conf{,.bak}
[root@master ~]# ls -lh /etc/kubernetes/admin.conf*
-rw------- 1 root root 5.4K Aug 12 16:11 /etc/kubernetes/admin.conf
-rw------- 1 root root 5.4K Aug 12 17:26 /etc/kubernetes/admin.conf.bak
[root@master ~]# 
```

- 查看kubelet状态

```sh
[root@master ~]# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: active (running) since Thu 2021-08-12 16:11:34 CST; 1h 16min ago
     Docs: https://kubernetes.io/docs/
 Main PID: 8433 (kubelet)
    Tasks: 15
   Memory: 37.3M
   CGroup: /system.slice/kubelet.service
           └─8433 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/ku...

Aug 12 17:27:12 master.mytest.com kubelet[8433]: W0812 17:27:12.080379    8433 cni.go:237] Unable to update cni config: no.../net.d
Aug 12 17:27:12 master.mytest.com kubelet[8433]: E0812 17:27:12.654601    8433 kubelet.go:2212] Container runtime network ...alized
Aug 12 17:27:17 master.mytest.com kubelet[8433]: W0812 17:27:17.082894    8433 cni.go:237] Unable to update cni config: no.../net.d
Aug 12 17:27:17 master.mytest.com kubelet[8433]: E0812 17:27:17.668554    8433 kubelet.go:2212] Container runtime network ...alized
Aug 12 17:27:22 master.mytest.com kubelet[8433]: W0812 17:27:22.092081    8433 cni.go:237] Unable to update cni config: no.../net.d
Aug 12 17:27:22 master.mytest.com kubelet[8433]: E0812 17:27:22.683736    8433 kubelet.go:2212] Container runtime network ...alized
Aug 12 17:27:27 master.mytest.com kubelet[8433]: W0812 17:27:27.093106    8433 cni.go:237] Unable to update cni config: no.../net.d
Aug 12 17:27:27 master.mytest.com kubelet[8433]: E0812 17:27:27.701610    8433 kubelet.go:2212] Container runtime network ...alized
Aug 12 17:27:32 master.mytest.com kubelet[8433]: W0812 17:27:32.093955    8433 cni.go:237] Unable to update cni config: no.../net.d
Aug 12 17:27:32 master.mytest.com kubelet[8433]: E0812 17:27:32.715703    8433 kubelet.go:2212] Container runtime network ...alized
Hint: Some lines were ellipsized, use -l to show in full.
[root@master ~]# 
[root@master ~]# ps -ef|grep 'bin/kubelet'|grep -v 'grep'
root      8433     1  1 16:11 ?        00:01:26 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/config.yaml --cgroup-driver=systemd --network-plugin=cni --pod-infra-container-image=registry.aliyuncs.com/google_containers/pause:3.2
```



这时，可以看到，`kubelet`服务已经启动了，通过进程可以发现，`kubelet`启动时，使用了`kubeadm init`初始化生成的多个配置文件。



#### 3.4.4 复制配置文件并验证

在我们复制`/etc/kubernetes/admin.conf`前，我们先执行一条命令`kubectl get nodes`:

```sh
[root@master ~]# kubectl get nodes
The connection to the server localhost:8080 was refused - did you specify the right host or port?
[root@master ~]# 
```

此时，可以看到，不能正常获取到集群的节点信息。

执行这三条命令：

```sh
 mkdir -p $HOME/.kube
 sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
 sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

我们是`root`用户，直接在master上面执行：

```sh
[root@master ~]# mkdir -p $HOME/.kube
[root@master ~]# sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
[root@master ~]# sudo chown $(id -u):$(id -g) $HOME/.kube/config
[root@master ~]# ls -lah .kube/config 
-rw------- 1 root root 5.4K Aug 12 17:40 .kube/config
[root@master ~]# 
```

此时再次查看节点信息:

```sh
[root@master ~]# kubectl get nodes
NAME                STATUS     ROLES    AGE   VERSION
master.mytest.com   NotReady   master   90m   v1.18.20
[root@master ~]# 
```

此时，可以看到，当前的master节点的状态是`NotReady`，即未就绪状态。



此时，我们查看一下日志信息：

```sh
[root@master ~]# tail /var/log/messages 
Aug 12 17:44:12 master kubelet: E0812 17:44:12.357037    8433 kubelet.go:2212] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
Aug 12 17:44:12 master kubelet: W0812 17:44:12.617353    8433 cni.go:237] Unable to update cni config: no networks found in /etc/cni/net.d
Aug 12 17:44:17 master kubelet: E0812 17:44:17.373716    8433 kubelet.go:2212] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
Aug 12 17:44:17 master kubelet: W0812 17:44:17.624174    8433 cni.go:237] Unable to update cni config: no networks found in /etc/cni/net.d
Aug 12 17:44:22 master kubelet: E0812 17:44:22.389514    8433 kubelet.go:2212] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
Aug 12 17:44:22 master kubelet: W0812 17:44:22.630131    8433 cni.go:237] Unable to update cni config: no networks found in /etc/cni/net.d
Aug 12 17:44:27 master kubelet: E0812 17:44:27.407339    8433 kubelet.go:2212] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
Aug 12 17:44:27 master kubelet: W0812 17:44:27.630585    8433 cni.go:237] Unable to update cni config: no networks found in /etc/cni/net.d
Aug 12 17:44:32 master kubelet: E0812 17:44:32.423892    8433 kubelet.go:2212] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
Aug 12 17:44:32 master kubelet: W0812 17:44:32.631120    8433 cni.go:237] Unable to update cni config: no networks found in /etc/cni/net.d
```



可以看到`NetworkPluginNotReady`信息，即kubernetes的网络插件没有准备好。因此，我们需要先安装一下kubernates的网络插件。

此时，查看Pod的信息：

```sh
[root@master ~]# kubectl get pods -A
NAMESPACE     NAME                                        READY   STATUS    RESTARTS   AGE
kube-system   coredns-7ff77c879f-fbdl7                    0/1     Pending   0          95m
kube-system   coredns-7ff77c879f-zkx44                    0/1     Pending   0          95m
kube-system   etcd-master.mytest.com                      1/1     Running   0          96m
kube-system   kube-apiserver-master.mytest.com            1/1     Running   0          96m
kube-system   kube-controller-manager-master.mytest.com   1/1     Running   0          96m
kube-system   kube-proxy-nzmm4                            1/1     Running   0          95m
kube-system   kube-scheduler-master.mytest.com            1/1     Running   0          96m
[root@master ~]# 
```

可以看到`coredns`也处于`pending`状态。

下一步就是要安装网络插件。



### 3.5 安装网络插件

> Kubernetes系统上Pod网络的实现依赖于第三方插件进行，这类插件有近数十种之多，较为著名的有flannel、calico、canal和kube-router等，简单易用的实现是为CoreOS提供的flannel项目。下面的命令用于在线部署flannel至Kubernetes系统之上：
>
> ~]# kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

我们先下载一下这个文件，看看文件内容。

你也可以直接点[下载kube-flannel.yml](/resource/softs/k8s/kube-flannel.yml) 下载我已经修改好的配置文件kube-flannel.yml。

```sh
# 下载
[root@master ~]# wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
--2021-08-12 17:54:03--  https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.111.133, 185.199.108.133, 185.199.109.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.111.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 4813 (4.7K) [text/plain]
Saving to: ‘kube-flannel.yml’

100%[=========================================================================================>] 4,813       8.32KB/s   in 0.6s   

2021-08-12 17:54:04 (8.32 KB/s) - ‘kube-flannel.yml’ saved [4813/4813]

[root@master ~]# 
```

查看`kube-flannel.yml`文件内容：

```sh
[root@master ~]# cat kube-flannel.yml 
---
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: psp.flannel.unprivileged
  annotations:
    seccomp.security.alpha.kubernetes.io/allowedProfileNames: docker/default
    seccomp.security.alpha.kubernetes.io/defaultProfileName: docker/default
    apparmor.security.beta.kubernetes.io/allowedProfileNames: runtime/default
    apparmor.security.beta.kubernetes.io/defaultProfileName: runtime/default
spec:
  privileged: false
  volumes:
  - configMap
  - secret
  - emptyDir
  - hostPath
  allowedHostPaths:
  - pathPrefix: "/etc/cni/net.d"
  - pathPrefix: "/etc/kube-flannel"
  - pathPrefix: "/run/flannel"
  readOnlyRootFilesystem: false
  # Users and groups
  runAsUser:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  # Privilege Escalation
  allowPrivilegeEscalation: false
  defaultAllowPrivilegeEscalation: false
  # Capabilities
  allowedCapabilities: ['NET_ADMIN', 'NET_RAW']
  defaultAddCapabilities: []
  requiredDropCapabilities: []
  # Host namespaces
  hostPID: false
  hostIPC: false
  hostNetwork: true
  hostPorts:
  - min: 0
    max: 65535
  # SELinux
  seLinux:
    # SELinux is unused in CaaSP
    rule: 'RunAsAny'
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: flannel
rules:
- apiGroups: ['extensions']
  resources: ['podsecuritypolicies']
  verbs: ['use']
  resourceNames: ['psp.flannel.unprivileged']
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - list
  - watch
- apiGroups:
  - ""
  resources:
  - nodes/status
  verbs:
  - patch
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: flannel
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: flannel
subjects:
- kind: ServiceAccount
  name: flannel
  namespace: kube-system
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: flannel
  namespace: kube-system
---
kind: ConfigMap
apiVersion: v1
metadata:
  name: kube-flannel-cfg
  namespace: kube-system
  labels:
    tier: node
    app: flannel
data:
  cni-conf.json: |
    {
      "name": "cbr0",
      "cniVersion": "0.3.1",
      "plugins": [
        {
          "type": "flannel",
          "delegate": {
            "hairpinMode": true,
            "isDefaultGateway": true
          }
        },
        {
          "type": "portmap",
          "capabilities": {
            "portMappings": true
          }
        }
      ]
    }
  net-conf.json: |
    {
      "Network": "10.244.0.0/16",
      "Backend": {
        "Type": "vxlan"
      }
    }
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-flannel-ds
  namespace: kube-system
  labels:
    tier: node
    app: flannel
spec:
  selector:
    matchLabels:
      app: flannel
  template:
    metadata:
      labels:
        tier: node
        app: flannel
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: kubernetes.io/os
                operator: In
                values:
                - linux
      hostNetwork: true
      priorityClassName: system-node-critical
      tolerations:
      - operator: Exists
        effect: NoSchedule
      serviceAccountName: flannel
      initContainers:
      - name: install-cni
        image: quay.io/coreos/flannel:v0.14.0
        command:
        - cp
        args:
        - -f
        - /etc/kube-flannel/cni-conf.json
        - /etc/cni/net.d/10-flannel.conflist
        volumeMounts:
        - name: cni
          mountPath: /etc/cni/net.d
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      containers:
      - name: kube-flannel
        image: quay.io/coreos/flannel:v0.14.0
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        resources:
          requests:
            cpu: "100m"
            memory: "50Mi"
          limits:
            cpu: "100m"
            memory: "50Mi"
        securityContext:
          privileged: false
          capabilities:
            add: ["NET_ADMIN", "NET_RAW"]
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        volumeMounts:
        - name: run
          mountPath: /run/flannel
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      volumes:
      - name: run
        hostPath:
          path: /run/flannel
      - name: cni
        hostPath:
          path: /etc/cni/net.d
      - name: flannel-cfg
        configMap:
          name: kube-flannel-cfg
[root@master ~]# 
```

通过下面的命令，可知，该配置文件中使用的是`quay.io`镜像仓库，是国外的镜像仓库，下载会比较慢，我们换成Docker的镜像仓库，由于我们配置了加速源，可以很快的下载下来。

```sh
[root@master ~]# grep -n 'image' kube-flannel.yml 
169:        image: quay.io/coreos/flannel:v0.14.0
183:        image: quay.io/coreos/flannel:v0.14.0
```

我们将这两行进行替换掉，使用`lizhenliang/flannel`镜像。

备份并替换：

```sh
[root@master ~]# cp kube-flannel.yml{,.bak}
[root@master ~]# ls kube-flannel.yml*
kube-flannel.yml  kube-flannel.yml.bak
[root@master ~]# sed -n 's@image: quay.io/coreos/flannel@image: lizhenliang/flannel@gp' kube-flannel.yml
        image: lizhenliang/flannel:v0.14.0
        image: lizhenliang/flannel:v0.14.0
[root@master ~]# sed -i 's@image: quay.io/coreos/flannel@image: lizhenliang/flannel@g' kube-flannel.yml
[root@master ~]# grep -n 'image' kube-flannel.yml 
169:        image: lizhenliang/flannel:v0.14.0
183:        image: lizhenliang/flannel:v0.14.0
```

可以看到，文件已经替换成功。

然后，直接运行，使用命令`kubectl apply -f kube-flannel.yml`来安装网络插件：

```sh
[root@master ~]# kubectl apply -f kube-flannel.yml
podsecuritypolicy.policy/psp.flannel.unprivileged created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.apps/kube-flannel-ds created
[root@master ~]# echo $?
0
[root@master ~]# 
```



命令正常执行。我们再看一下节点和Pod状态：

```sh
[root@master ~]# kubectl get nodes
NAME                STATUS   ROLES    AGE    VERSION
master.mytest.com   Ready    master   120m   v1.18.20
[root@master ~]# kubectl get pods -A
NAMESPACE     NAME                                        READY   STATUS    RESTARTS   AGE
kube-system   coredns-7ff77c879f-fbdl7                    1/1     Running   0          120m
kube-system   coredns-7ff77c879f-zkx44                    1/1     Running   0          120m
kube-system   etcd-master.mytest.com                      1/1     Running   0          120m
kube-system   kube-apiserver-master.mytest.com            1/1     Running   0          120m
kube-system   kube-controller-manager-master.mytest.com   1/1     Running   0          120m
kube-system   kube-flannel-ds-b722r                       1/1     Running   0          2m14s
kube-system   kube-proxy-nzmm4                            1/1     Running   0          120m
kube-system   kube-scheduler-master.mytest.com            1/1     Running   0          120m
[root@master ~]# 
```

此时，可以看到，节点已经变成`Ready`就绪状态，并且所有的Pod都是`Running`运行状态。


此时，coredns有可能启动失败：
```sh
[root@k8s-master ~]# kubectl get pods -n kube-system
NAME                                 READY   STATUS    RESTARTS   AGE
coredns-7ff77c879f-g4cvs             0/1     Pending   0          45m
coredns-7ff77c879f-wbvwd             0/1     Pending   0          44m
etcd-k8s-master                      1/1     Running   0          80m
kube-apiserver-k8s-master            1/1     Running   0          80m
kube-controller-manager-k8s-master   1/1     Running   0          80m
kube-flannel-ds-89mmk                1/1     Running   0          42m
kube-flannel-ds-9k7nw                1/1     Running   0          56m
kube-flannel-ds-w5lpj                1/1     Running   0          41m
kube-proxy-glfmr                     1/1     Running   0          79m
kube-proxy-vscq8                     1/1     Running   0          42m
kube-proxy-vxk8w                     1/1     Running   0          41m
kube-scheduler-k8s-master            1/1     Running   0          80m
[root@k8s-master ~]#
```

查看日志信息：
```sh
[root@k8s-master ~]# tail /var/log/messages
Nov 22 22:16:14 master kubelet: {
Nov 22 22:16:14 master kubelet: "type": "portmap",
Nov 22 22:16:14 master kubelet: "capabilities": {
Nov 22 22:16:14 master kubelet: "portMappings": true
Nov 22 22:16:14 master kubelet: }
Nov 22 22:16:14 master kubelet: }
Nov 22 22:16:14 master kubelet: ]
Nov 22 22:16:14 master kubelet: }
Nov 22 22:16:14 master kubelet: : [failed to find plugin "flannel" in path [/opt/cni/bin]]
Nov 22 22:16:14 master kubelet: W1122 22:16:14.196831    2946 cni.go:237] Unable to update cni config: no valid networks found in /etc/cni/net.d
[root@k8s-master ~]#
```

查看pod coredns的事件信息：
```sh
[root@k8s-master ~]# kubectl describe pod coredns-7ff77c879f-g4cvs  -n kube-system
....省略
Volumes:
  config-volume:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      coredns
    Optional:  false
  coredns-token-jbfmf:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  coredns-token-jbfmf
    Optional:    false
QoS Class:       Burstable
Node-Selectors:  kubernetes.io/os=linux
Tolerations:     CriticalAddonsOnly
                 node-role.kubernetes.io/master:NoSchedule
                 node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason            Age                  From               Message
  ----     ------            ----                 ----               -------
  Warning  FailedScheduling  44m (x22 over 47m)   default-scheduler  0/1 nodes are available: 1 node(s) had taint {node.kubernetes.io/not-ready: }, that the pod didn't tolerate.
  Warning  FailedScheduling  44m (x3 over 44m)    default-scheduler  0/2 nodes are available: 2 node(s) had taint {node.kubernetes.io/not-ready: }, that the pod didn't tolerate.
  Warning  FailedScheduling  106s (x32 over 43m)  default-scheduler  0/3 nodes are available: 3 node(s) had taint {node.kubernetes.io/not-ready: }, that the pod didn't tolerate.
```
查看文件信息：
```sh
[root@k8s-master ~]# ls -lah /etc/cni/net.d/
total 4.0K
drwxr-xr-x 2 root root  33 Nov 22 21:14 .
drwxr-xr-x 3 root root  19 Nov 22 21:14 ..
-rw-r--r-- 1 root root 292 Nov 22 21:14 10-flannel.conflist
[root@k8s-master ~]# ls -lah /opt/c
cni/        containerd/
[root@k8s-master ~]# ls -lah /opt/cni/bin/
total 46M
drwxr-xr-x. 2 root root  235 Nov  5 00:24 .
drwxr-xr-x. 3 root root   17 Nov  5 00:24 ..
-rwxr-xr-x. 1 root root 2.7M Sep 15 07:11 bandwidth
-rwxr-xr-x. 1 root root 3.0M Sep 15 07:11 bridge
-rwxr-xr-x. 1 root root 7.1M Sep 15 07:11 dhcp
-rwxr-xr-x. 1 root root 3.1M Sep 15 07:11 firewall
-rwxr-xr-x. 1 root root 2.7M Sep 15 07:11 host-device
-rwxr-xr-x. 1 root root 2.3M Sep 15 07:11 host-local
-rwxr-xr-x. 1 root root 2.8M Sep 15 07:11 ipvlan
-rwxr-xr-x. 1 root root 2.3M Sep 15 07:11 loopback
-rwxr-xr-x. 1 root root 2.8M Sep 15 07:11 macvlan
-rwxr-xr-x. 1 root root 2.6M Sep 15 07:11 portmap
-rwxr-xr-x. 1 root root 2.9M Sep 15 07:11 ptp
-rwxr-xr-x. 1 root root 2.5M Sep 15 07:11 sbr
-rwxr-xr-x. 1 root root 2.0M Sep 15 07:11 static
-rwxr-xr-x. 1 root root 2.4M Sep 15 07:11 tuning
-rwxr-xr-x. 1 root root 2.8M Sep 15 07:11 vlan
-rwxr-xr-x. 1 root root 2.5M Sep 15 07:11 vrf
[root@k8s-master ~]#
```

出现此问题，是因为高版本的插件中没有`flannel`程序。
可以使用以下命令下载低版本的插件：
```sh
wget https://github.com/containernetworking/plugins/releases/download/v0.8.7/cni-plugins-linux-amd64-v0.8.7.tgz
```
你也可以直接点[下载flannel](/resource/softs/k8s/flannel) 下载。

下载后，将其解压：
```sh
[root@master ~]# wget https://github.com/containernetworking/plugins/releases/download/v0.8.7/cni-plugins-linux-amd64-v0.8.7.tgz
[root@master ~]# mkdir cni-plugins
[root@master ~]# tar -zxvf cni-plugins-linux-amd64-v0.8.7.tgz -C cni-plugins
[root@master ~]# ls -lah cni-plugins/flannel
-rwxr-xr-x 1 root root 3.3M Aug 27  2020 cni-plugins-v0.8.7/flannel
```
将flannel文件复制到`/opt/cni/bin`目录下，并添加可执行权限：
```sh
[root@master ~]# cp cni-plugins/flannel /opt/cni/bin/
[root@master ~]# chmod +x /opt/cni/bin/flannel
[root@master ~]# ll /opt/cni/bin/flannel
-rwxr-xr-x 1 root root 3439780 Aug 27  2020 /opt/cni/bin/flannel
```

此时再重启coredns两个pod:
```sh
[root@k8s-master bin]# kubectl delete pod coredns-7ff77c879f-g4cvs -n kube-system
pod "coredns-7ff77c879f-g4cvs" deleted
[root@k8s-master bin]# kubectl delete pod coredns-7ff77c879f-wbvwd -n kube-system
pod "coredns-7ff77c879f-wbvwd" deleted
[root@k8s-master bin]# kubectl get pods -A
NAMESPACE     NAME                                 READY   STATUS    RESTARTS   AGE
kube-system   coredns-7ff77c879f-hvxgz             1/1     Running   0          35s
kube-system   coredns-7ff77c879f-p4f8q             1/1     Running   0          18s
kube-system   etcd-k8s-master                      1/1     Running   1          42h
kube-system   kube-apiserver-k8s-master            1/1     Running   1          42h
kube-system   kube-controller-manager-k8s-master   1/1     Running   1          42h
kube-system   kube-flannel-ds-89mmk                1/1     Running   0          41h
kube-system   kube-flannel-ds-9k7nw                1/1     Running   1          41h
kube-system   kube-flannel-ds-w5lpj                1/1     Running   0          41h
kube-system   kube-proxy-glfmr                     1/1     Running   1          42h
kube-system   kube-proxy-vscq8                     1/1     Running   0          41h
kube-system   kube-proxy-vxk8w                     1/1     Running   0          41h
kube-system   kube-scheduler-k8s-master            1/1     Running   1          42h
[root@k8s-master bin]# kubectl get nodes
NAME         STATUS     ROLES    AGE   VERSION
k8s-master   Ready      master   42h   v1.18.20
k8s-node1    NotReady   <none>   41h   v1.18.20
k8s-node2    NotReady   <none>   41h   v1.18.20
```
这个时候，可以看到master节点所有pod正常运行！说明master主节点配置正常。

按相同的方式，在k8s-node1和k8s-node2节点下载`flannel`文件，并放在`/opt/cni/bin/flannel`路径，增加可执行权限，然后重启`kubelet`。
```sh
[root@k8s-node1 ~]# chmod +x /opt/cni/bin/flannel
[root@k8s-node1 ~]# ll /opt/cni/bin/flannel
-rwxr-xr-x 1 root root 3439780 Aug 27  2020 /opt/cni/bin/flannel
[root@k8s-node1 ~]# systemctl restart kubelet
[root@k8s-node1 ~]# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/usr/lib/systemd/system/kubelet.service; disabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: active (running) since Thu 2022-11-24 15:02:06 CST; 15min ago
     Docs: https://kubernetes.io/docs/
 Main PID: 2880 (kubelet)
    Tasks: 16
   Memory: 33.3M
   CGroup: /system.slice/kubelet.service
           └─2880 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/ku...

Nov 24 15:02:12 k8s-node1 kubelet[2880]: W1124 15:02:12.774079    2880 pod_container_deletor.go:77] Container "b...iners
Nov 24 15:02:12 k8s-node1 kubelet[2880]: I1124 15:02:12.803000    2880 reconciler.go:224] operationExecutor.Veri...110")
Nov 24 15:02:12 k8s-node1 kubelet[2880]: I1124 15:02:12.803040    2880 reconciler.go:224] operationExecutor.Veri...110")
Nov 24 15:02:12 k8s-node1 kubelet[2880]: I1124 15:02:12.803060    2880 reconciler.go:224] operationExecutor.Veri...110")
Nov 24 15:02:12 k8s-node1 kubelet[2880]: I1124 15:02:12.803076    2880 reconciler.go:224] operationExecutor.VerifyCon...
Nov 24 15:02:12 k8s-node1 kubelet[2880]: I1124 15:02:12.803092    2880 reconciler.go:224] operationExecutor.Veri...110")
Nov 24 15:02:12 k8s-node1 kubelet[2880]: I1124 15:02:12.803106    2880 reconciler.go:224] operationExecutor.Veri...110")
Nov 24 15:02:12 k8s-node1 kubelet[2880]: I1124 15:02:12.803120    2880 reconciler.go:224] operationExecutor.Veri...110")
Nov 24 15:02:12 k8s-node1 kubelet[2880]: I1124 15:02:12.803135    2880 reconciler.go:224] operationExecutor.VerifyCon...
Nov 24 15:02:12 k8s-node1 kubelet[2880]: I1124 15:02:12.803144    2880 reconciler.go:157] Reconciler: start to s...state
Hint: Some lines were ellipsized, use -l to show in full.
[root@k8s-node1 ~]#
```
节点k8s-node2按相同的方法下载flannel，设置权限，并重启kubelet服务。

此时再查看集群信息：
```sh
[root@k8s-master ~]# kubectl get nodes
NAME         STATUS   ROLES    AGE   VERSION
k8s-master   Ready    master   42h   v1.18.20
k8s-node1    Ready    <none>   41h   v1.18.20
k8s-node2    Ready    <none>   41h   v1.18.20
```
可以看到，集群配置成功！！！ 注意，如果你还没配置其他节点，可以按后续步骤添加节点。


现在查看一下正常运行的容器：

```sh
[root@master ~]# docker ps
CONTAINER ID   IMAGE                                               COMMAND                  CREATED         STATUS         PORTS     NAMES
37b88f5b0af3   67da37a9a360                                        "/coredns -conf /etc…"   3 minutes ago   Up 3 minutes             k8s_coredns_coredns-7ff77c879f-zkx44_kube-system_1f5d8bfd-d4ff-4efa-b70d-f98d7538675e_0
53c4440c7b72   67da37a9a360                                        "/coredns -conf /etc…"   3 minutes ago   Up 3 minutes             k8s_coredns_coredns-7ff77c879f-fbdl7_kube-system_9cd6f3f4-b234-45d3-906f-37afb75dc5c4_0
a5505760cae2   registry.aliyuncs.com/google_containers/pause:3.2   "/pause"                 3 minutes ago   Up 3 minutes             k8s_POD_coredns-7ff77c879f-zkx44_kube-system_1f5d8bfd-d4ff-4efa-b70d-f98d7538675e_0
0fe8b36cf268   registry.aliyuncs.com/google_containers/pause:3.2   "/pause"                 3 minutes ago   Up 3 minutes             k8s_POD_coredns-7ff77c879f-fbdl7_kube-system_9cd6f3f4-b234-45d3-906f-37afb75dc5c4_0
b257627cbd18   8522d622299c                                        "/opt/bin/flanneld -…"   4 minutes ago   Up 4 minutes             k8s_kube-flannel_kube-flannel-ds-b722r_kube-system_a0f30718-ec8e-4931-8e95-0bc33d464945_0
e20aa5d56136   registry.aliyuncs.com/google_containers/pause:3.2   "/pause"                 4 minutes ago   Up 4 minutes             k8s_POD_kube-flannel-ds-b722r_kube-system_a0f30718-ec8e-4931-8e95-0bc33d464945_0
fbb59a9fcd3d   27f8b8d51985                                        "/usr/local/bin/kube…"   2 hours ago     Up 2 hours               k8s_kube-proxy_kube-proxy-nzmm4_kube-system_92c5af10-9aa3-49a8-9d2f-ed46045d09f3_0
ae903b4033d9   registry.aliyuncs.com/google_containers/pause:3.2   "/pause"                 2 hours ago     Up 2 hours               k8s_POD_kube-proxy-nzmm4_kube-system_92c5af10-9aa3-49a8-9d2f-ed46045d09f3_0
4195620f0212   a05a1a79adaa                                        "kube-scheduler --au…"   2 hours ago     Up 2 hours               k8s_kube-scheduler_kube-scheduler-master.mytest.com_kube-system_c871ae39a802385d75a9bc63229003c0_0
33246821314b   7d8d2960de69                                        "kube-apiserver --ad…"   2 hours ago     Up 2 hours               k8s_kube-apiserver_kube-apiserver-master.mytest.com_kube-system_c58a587dd1f416378a0cec08a0e83e51_0
1a5b0f255ca2   303ce5db0e90                                        "etcd --advertise-cl…"   2 hours ago     Up 2 hours               k8s_etcd_etcd-master.mytest.com_kube-system_9c3f6e582e1acc630efb5ee84d994008_0
01521565d76a   registry.aliyuncs.com/google_containers/pause:3.2   "/pause"                 2 hours ago     Up 2 hours               k8s_POD_kube-scheduler-master.mytest.com_kube-system_c871ae39a802385d75a9bc63229003c0_0
029f7c6b66d0   e7c545a60706                                        "kube-controller-man…"   2 hours ago     Up 2 hours               k8s_kube-controller-manager_kube-controller-manager-master.mytest.com_kube-system_912a1414f7cd245daf8395f4c4899e74_0
6f8255098622   registry.aliyuncs.com/google_containers/pause:3.2   "/pause"                 2 hours ago     Up 2 hours               k8s_POD_kube-apiserver-master.mytest.com_kube-system_c58a587dd1f416378a0cec08a0e83e51_0
05a46b32c721   registry.aliyuncs.com/google_containers/pause:3.2   "/pause"                 2 hours ago     Up 2 hours               k8s_POD_etcd-master.mytest.com_kube-system_9c3f6e582e1acc630efb5ee84d994008_0
2cca357c6e5c   registry.aliyuncs.com/google_containers/pause:3.2   "/pause"                 2 hours ago     Up 2 hours               k8s_POD_kube-controller-manager-master.mytest.com_kube-system_912a1414f7cd245daf8395f4c4899e74_0
[root@master ~]# docker ps |wc -l
17
[root@master ~]# 
```

可以看到，此时已经运行了17个容器了。

可以看到运行了很多`pause`容器，这个容器有什么作用？后续研究。



### 3.6 添加集群节点

上面我们已经知道master节点已经能够正常工作了。现在我们只用在各节点上面运行`kubeadm init`时生成的将节点加入集群的命令：

```sh
kubeadm join kubeapi.mytest.com:6443 --token ntf08x.uaudrocid80akszx \
    --discovery-token-ca-cert-hash sha256:e60ab1ae8fcc0f8b8d3d2256c59738723a7ad04bee1aa0c0a1d8256bc62b4293
```

我们在node1和node2节点上面分别运行以上命令。

在node1节点执行：

```sh
[root@node1 ~]# kubeadm join kubeapi.mytest.com:6443 --token ntf08x.uaudrocid80akszx \
>     --discovery-token-ca-cert-hash sha256:e60ab1ae8fcc0f8b8d3d2256c59738723a7ad04bee1aa0c0a1d8256bc62b4293
W0812 18:33:16.483466   15374 join.go:346] [preflight] WARNING: JoinControlPane.controlPlane settings will be ignored when control-plane flag is not set.
[preflight] Running pre-flight checks
        [WARNING SystemVerification]: this Docker version is not on the list of validated versions: 20.10.8. Latest validated version: 19.03
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'
[kubelet-start] Downloading configuration for the kubelet from the "kubelet-config-1.18" ConfigMap in the kube-system namespace
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.

[root@node1 ~]# echo $?
0
[root@node1 ~]# 
```

再在node2节点执行：

```sh
[root@node2 ~]# kubeadm join kubeapi.mytest.com:6443 --token ntf08x.uaudrocid80akszx \
>     --discovery-token-ca-cert-hash sha256:e60ab1ae8fcc0f8b8d3d2256c59738723a7ad04bee1aa0c0a1d8256bc62b4293
W0812 18:34:17.352493   14951 join.go:346] [preflight] WARNING: JoinControlPane.controlPlane settings will be ignored when control-plane flag is not set.
[preflight] Running pre-flight checks
        [WARNING SystemVerification]: this Docker version is not on the list of validated versions: 20.10.8. Latest validated version: 19.03
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'
[kubelet-start] Downloading configuration for the kubelet from the "kubelet-config-1.18" ConfigMap in the kube-system namespace
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.

[root@node2 ~]# echo $?
0
[root@node2 ~]# 
```

可以看到，在node1和node2节点上面都执行成功了。



我们现在在master上面查看一下集群节点的相关状态信息。

```sh
[root@master ~]# kubectl get nodes
NAME                STATUS   ROLES    AGE     VERSION
master.mytest.com   Ready    master   144m    v1.18.20
node1.mytest.com    Ready    <none>   2m30s   v1.18.20
node2.mytest.com    Ready    <none>   89s     v1.18.20
[root@master ~]# kubectl get nodes -o wide
NAME                STATUS   ROLES    AGE     VERSION    INTERNAL-IP     EXTERNAL-IP   OS-IMAGE                KERNEL-VERSION           CONTAINER-RUNTIME
master.mytest.com   Ready    master   144m    v1.18.20   192.168.56.60   <none>        CentOS Linux 7 (Core)   3.10.0-1062.el7.x86_64   docker://20.10.8
node1.mytest.com    Ready    <none>   2m45s   v1.18.20   192.168.56.61   <none>        CentOS Linux 7 (Core)   3.10.0-1062.el7.x86_64   docker://20.10.8
node2.mytest.com    Ready    <none>   104s    v1.18.20   192.168.56.62   <none>        CentOS Linux 7 (Core)   3.10.0-1062.el7.x86_64   docker://20.10.8
[root@master ~]# 
```

查看Pod信息：

```sh
[root@master ~]# kubectl get pods -A
NAMESPACE     NAME                                        READY   STATUS    RESTARTS   AGE
kube-system   coredns-7ff77c879f-fbdl7                    1/1     Running   0          146m
kube-system   coredns-7ff77c879f-zkx44                    1/1     Running   0          146m
kube-system   etcd-master.mytest.com                      1/1     Running   0          146m
kube-system   kube-apiserver-master.mytest.com            1/1     Running   0          146m
kube-system   kube-controller-manager-master.mytest.com   1/1     Running   0          146m
kube-system   kube-flannel-ds-2pqx7                       1/1     Running   0          3m34s
kube-system   kube-flannel-ds-b722r                       1/1     Running   0          28m
kube-system   kube-flannel-ds-lhbps                       1/1     Running   0          4m35s
kube-system   kube-proxy-4sfq6                            1/1     Running   0          3m34s
kube-system   kube-proxy-nzmm4                            1/1     Running   0          146m
kube-system   kube-proxy-vll68                            1/1     Running   0          4m35s
kube-system   kube-scheduler-master.mytest.com            1/1     Running   0          146m
[root@master ~]# kubectl get pods -A -o wide
NAMESPACE     NAME                                        READY   STATUS    RESTARTS   AGE     IP              NODE                NOMINATED NODE   READINESS GATES
kube-system   coredns-7ff77c879f-fbdl7                    1/1     Running   0          146m    10.244.0.3      master.mytest.com   <none>           <none>
kube-system   coredns-7ff77c879f-zkx44                    1/1     Running   0          146m    10.244.0.2      master.mytest.com   <none>           <none>
kube-system   etcd-master.mytest.com                      1/1     Running   0          146m    192.168.56.60   master.mytest.com   <none>           <none>
kube-system   kube-apiserver-master.mytest.com            1/1     Running   0          146m    192.168.56.60   master.mytest.com   <none>           <none>
kube-system   kube-controller-manager-master.mytest.com   1/1     Running   0          146m    192.168.56.60   master.mytest.com   <none>           <none>
kube-system   kube-flannel-ds-2pqx7                       1/1     Running   0          3m43s   192.168.56.62   node2.mytest.com    <none>           <none>
kube-system   kube-flannel-ds-b722r                       1/1     Running   0          28m     192.168.56.60   master.mytest.com   <none>           <none>
kube-system   kube-flannel-ds-lhbps                       1/1     Running   0          4m44s   192.168.56.61   node1.mytest.com    <none>           <none>
kube-system   kube-proxy-4sfq6                            1/1     Running   0          3m43s   192.168.56.62   node2.mytest.com    <none>           <none>
kube-system   kube-proxy-nzmm4                            1/1     Running   0          146m    192.168.56.60   master.mytest.com   <none>           <none>
kube-system   kube-proxy-vll68                            1/1     Running   0          4m44s   192.168.56.61   node1.mytest.com    <none>           <none>
kube-system   kube-scheduler-master.mytest.com            1/1     Running   0          146m    192.168.56.60   master.mytest.com   <none>           <none>
[root@master ~]# 
```

这样，我们的集群就安装配置成功了！



我们将三台虚拟机关机，然后创建备份快照。快照名称为`k8s_1`，描述信息为`k8s集群部署完成，nodes和pods都正常运行，未添加其他实际应用。`

![](/img/20210812221324.png)





## 4. Kubernetes集群第一个应用

我们已经成功安装配置了k8s集群，现在是时候在集群上面部署应用了。我们来部署Kubernetes Dashboard这个UI系统。

可参考：

- [Kubernetes Dashboard](https://github.com/kubernetes/dashboard)
- [kubernetesui/dashboard](https://registry.hub.docker.com/r/kubernetesui/dashboard)

按官方帮助信息，只需要执行命令：

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml
```

即可。

你也可以直接点[下载recommended.yaml](/resource/softs/k8s/recommended.yaml) 下载我已经修改好的配置文件recommended.yaml。

我们先手动下载`recommended.yaml`文件：

```sh
[root@master ~]# wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml
--2021-08-12 23:04:15--  https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.111.133, 185.199.110.133, 185.199.108.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.111.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 7552 (7.4K) [text/plain]
Saving to: ‘recommended.yaml’

100%[=============================================================================================================================>] 7,552       --.-K/s   in 0s      

2021-08-12 23:04:16 (44.1 MB/s) - ‘recommended.yaml’ saved [7552/7552]

[root@master ~]# 
```

我们查看一下`recommended.yaml`文件的`service`配置：

```sh
[root@master ~]# ls -la recommended.yaml 
-rw-r--r-- 1 root root 7552 Aug 12 23:04 recommended.yaml
[root@master ~]# cat -n recommended.yaml|sed  -n '30,46p'
    30  ---
    31  
    32  kind: Service
    33  apiVersion: v1
    34  metadata:
    35    labels:
    36      k8s-app: kubernetes-dashboard
    37    name: kubernetes-dashboard
    38    namespace: kubernetes-dashboard
    39  spec:
    40    ports:
    41      - port: 443
    42        targetPort: 8443
    43    selector:
    44      k8s-app: kubernetes-dashboard
    45  
    46  ---
[root@master ~]# 
```

我们备份yaml文件并增加一下：

```sh
[root@master ~]# cp recommended.yaml{,.bak}
[root@master ~]# ls -la recommended.yaml*
-rw-r--r-- 1 root root 7552 Aug 12 23:04 recommended.yaml
-rw-r--r-- 1 root root 7552 Aug 12 23:22 recommended.yaml.bak
[root@master ~]# vi recommended.yaml
[root@master ~]# cat -n recommended.yaml|sed  -n '30,47p'
    30  ---
    31  
    32  kind: Service
    33  apiVersion: v1
    34  metadata:
    35    labels:
    36      k8s-app: kubernetes-dashboard
    37    name: kubernetes-dashboard
    38    namespace: kubernetes-dashboard
    39  spec:
    40    type: NodePort
    41    ports:
    42      - port: 443
    43        targetPort: 8443
    44    selector:
    45      k8s-app: kubernetes-dashboard
    46  
    47  ---
[root@master ~]# 
[root@master ~]# diff recommended.yaml recommended.yaml.bak 
40d39
<   type: NodePort
[root@master ~]#
```

第40行的`type:NodePort`是新增的内容。



然后，我们使用命令`kubectl apply -f recommended.yaml`创建应用：

```sh
[root@master ~]# kubectl apply -f recommended.yaml
namespace/kubernetes-dashboard created
serviceaccount/kubernetes-dashboard created
service/kubernetes-dashboard created
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
secret/kubernetes-dashboard-key-holder created
configmap/kubernetes-dashboard-settings created
role.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrole.rbac.authorization.k8s.io/kubernetes-dashboard created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
deployment.apps/kubernetes-dashboard created
service/dashboard-metrics-scraper created
deployment.apps/dashboard-metrics-scraper created
[root@master ~]# 
```

查看Pod信息：

```sh
[root@master ~]# kubectl get pods -A
NAMESPACE              NAME                                         READY   STATUS    RESTARTS   AGE
kube-system            coredns-7ff77c879f-fbdl7                     1/1     Running   1          7h16m
kube-system            coredns-7ff77c879f-zkx44                     1/1     Running   1          7h16m
kube-system            etcd-master.mytest.com                       1/1     Running   1          7h16m
kube-system            kube-apiserver-master.mytest.com             1/1     Running   1          7h16m
kube-system            kube-controller-manager-master.mytest.com    1/1     Running   1          7h16m
kube-system            kube-flannel-ds-2pqx7                        1/1     Running   1          4h54m
kube-system            kube-flannel-ds-b722r                        1/1     Running   1          5h18m
kube-system            kube-flannel-ds-lhbps                        1/1     Running   1          4h55m
kube-system            kube-proxy-4sfq6                             1/1     Running   1          4h54m
kube-system            kube-proxy-nzmm4                             1/1     Running   1          7h16m
kube-system            kube-proxy-vll68                             1/1     Running   1          4h55m
kube-system            kube-scheduler-master.mytest.com             1/1     Running   1          7h16m
kubernetes-dashboard   dashboard-metrics-scraper-78f5d9f487-grsqn   1/1     Running   0          50s
kubernetes-dashboard   kubernetes-dashboard-6bc5cb8879-wswsl        1/1     Running   0          50s
[root@master ~]#
[root@master ~]# kubectl get pods -n kubernetes-dashboard
NAME                                         READY   STATUS    RESTARTS   AGE
dashboard-metrics-scraper-78f5d9f487-grsqn   1/1     Running   0          4m22s
kubernetes-dashboard-6bc5cb8879-wswsl        1/1     Running   0          4m22s
```

可以看到`kubernetes-dashboard`已经正常运行。



查看对应的Service信息：

```sh
[root@master ~]# kubectl get services -n kubernetes-dashboard
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
dashboard-metrics-scraper   ClusterIP   10.96.169.151   <none>        8000/TCP        3m56s
kubernetes-dashboard        NodePort    10.102.68.190   <none>        443:31934/TCP   3m57s
[root@master ~]# 
```

查看对应的Pod在哪个节点上运行的：

```sh
[root@master ~]# kubectl get pods -n kubernetes-dashboard -o wide
NAME                                         READY   STATUS    RESTARTS   AGE     IP           NODE               NOMINATED NODE   READINESS GATES
dashboard-metrics-scraper-78f5d9f487-grsqn   1/1     Running   0          7m18s   10.244.2.2   node2.mytest.com   <none>           <none>
kubernetes-dashboard-6bc5cb8879-wswsl        1/1     Running   0          7m18s   10.244.1.2   node1.mytest.com   <none>           <none>
[root@master ~]# kubectl get services -n kubernetes-dashboard -o wide
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE     SELECTOR
dashboard-metrics-scraper   ClusterIP   10.96.169.151   <none>        8000/TCP        7m37s   k8s-app=dashboard-metrics-scraper
kubernetes-dashboard        NodePort    10.102.68.190   <none>        443:31934/TCP   7m38s   k8s-app=kubernetes-dashboard
[root@master ~]# 
```

可以知道`kubernetes-dashboard`运行在节点node1上面。其对应的端口号是`31934`。

为了能在我们宿主机上面能够访问集群中的应用，我们在宿主机上面也配置一下域名解析。

```sh
$ tail -n 5 /etc/hosts
# k8s
192.168.56.60 master.mytest.com master kubeapi.mytest.com kubeapi k8s-master
192.168.56.61 node1.mytest.com node1 k8s-node1
192.168.56.62 node2.mytest.com node2 k8s-node2
```

现在我们在宿主机上面访问`node1.mytest.com:31934`  [http://node1.mytest.com:31934/](http://node1.mytest.com:31934/) 看看会看到什么。

![](/img/20210812234800.png)

可以看到，页面返回的信息是"Client sent an HTTP request to an HTTPS server."，提示需要使用`https`方式访问。

我们改成https方式访问，访问链接 [https://node1.mytest.com:31934/](https://node1.mytest.com:31934/)，此时看到的界面如下：

![](/img/20210812235059.png)

我们选择`高级`,并"接受风险并继续"，看到如下页面：

![](/img/20210812235850.png)



可以看到，可以通过两种方式进行登陆。我们使用token的方式登陆。



下面先来生成token。

- 创建service account

```sh
[root@master ~]# kubectl create serviceaccount dashboard-admin -n kube-system
serviceaccount/dashboard-admin created
```

- service account账户绑定到集群角色cluster-admin

```sh
[root@master ~]# kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kube-system:dashboard-admin  
clusterrolebinding.rbac.authorization.k8s.io/dashboard-admin created
[root@master ~]# 
```

- 获取secret的名称

```sh
[root@master ~]# kubectl get secret -n kube-system|head -n 1; kubectl get secret -n kube-system|grep 'dash'
NAME                                             TYPE                                  DATA   AGE
dashboard-admin-token-4kkdc                      kubernetes.io/service-account-token   3      9m20s
[root@master ~]# kubectl get secret -n kube-system|grep 'dash'|awk '{print $1}'
dashboard-admin-token-4kkdc
```

- 获取token值

```sh
[root@master ~]# kubectl describe secrets -n kube-system dashboard-admin-token-4kkdc 
Name:         dashboard-admin-token-4kkdc
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: dashboard-admin
              kubernetes.io/service-account.uid: a666ccfc-13d5-49c8-bdbd-9f725b01fcbb

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1025 bytes
namespace:  11 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IjhLTWpoZUpQbGtxSUgxTnFMdGRJY2lVNlNBeU1XNzNqaXpfU1l4RkY5cmMifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tNGtrZGMiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiYTY2NmNjZmMtMTNkNS00OWM4LWJkYmQtOWY3MjViMDFmY2JiIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.hg8xgiYKLH5tyZ8W7UvTRDYXv0vhGphGOxbCuLA4Yn_LbFbrMdmNTqcZQT-kgsS7RMVMgK9NWYZtv9szzhPwdWoLTkTcTLtyECHwhXOk6usSFlCVA8CI_2qj8l4zUty0MLEHSGF_jTcZsvio8UH8dCxCbPPx5Ks3ZcEfw-nMm6rA4hRqH1dQ0YhTk_VC01dv81x17W9SOwsAZoXOpUUFelhxBHIE8iChUmOxtjUvPjmXYn2sOJ_F7cF6PAG_HZQv4y0Gg8uwUMWlNy6fRrKIIOdfcPbSv8fYH486y1C9uc8YXI7p2DQx5nU5qDQtWslGc_9kftGzW-vzypzrzWsGXw
[root@master ~]# 
```

`token`行的内容就是最后需要的数据。将其复制粘贴到Web界面的输入框中。

然后，我们就可以进入到DashBoard界面了。

![](/img/20210813003529.png)

此时，在界面上面看到没有任何Pod。

我们可以快速创建一个Pod。

如，创建一个Nginx的Pod:

```sh
[root@master ~]# kubectl create deployment myweb --image=nginx
deployment.apps/myweb created
[root@master ~]# kubectl get pods 
NAME                     READY   STATUS    RESTARTS   AGE
myweb-544b6f5455-2hs9m   1/1     Running   0          60s
[root@master ~]# 
```

此时，在DashBoard界面上面会自动显示出刚才创建的myweb这个Pod：

![](/img/20210813004324.png)

至此，k8s集群以及其基本应用的尝试已经完成了。



后续，再在集群上面进行深入的学习。



学习过程中存在的疑问：

- docker pause镜像的作用？
- k8s是如何选择在哪个节点上面运行Pod的？
- k8s为什么不能在master上面运行自己的Pod？
- Pod是什么？
- k8s可以使用非自签名证书吗？
- 如何访问k8s的服务，如Web页面，怎么样确定端口号的？



问题比较多，后面一点一点的总结分析。