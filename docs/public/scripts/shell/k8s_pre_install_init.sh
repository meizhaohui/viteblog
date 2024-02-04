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
yum install -y yum-utils device-mapper-persistent-data lvm2

echo "Set Aliyun Docker yum mirror"
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

yum install -y vim git224 jq deltarpm python3 go

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
syntax on
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
EOF


echo "Install Docker"
yum install -y docker-ce docker-ce-cli containerd.io

echo "Start Docker"
sed -i.bak '/ExecStart=\/usr\/bin\/dockerd/aExecStartPost=/usr/sbin/iptables -P FORWARD ACCEPT' /usr/lib/systemd/system/docker.service
systemctl daemon-reload
systemctl enable docker
echo "Config Docker mirror"
cat >> /etc/docker/daemon.json << EOF
{"registry-mirrors":["https://reg-mirror.qiniu.com/"]}
EOF
systemctl start docker
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

echo "Please use command 'setip' to change the IP and 'addhosts' to add new domain parse!!!"
echo "Done!"
