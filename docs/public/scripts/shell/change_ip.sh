#!/bin/bash
# filename: change_ip.sh
# author:   meizhaohui
configfile=/etc/sysconfig/network-scripts/ifcfg-enp0s3
IP=$1
echo "待分配IP:${IP}"
echo "IP 修改前配置文件内容："
cat "${configfile}"
sed -i "s/^IPADDR=.*$/IPADDR=$IP/g" "${configfile}"
echo -e "\n=========================\n"
echo "IP 修改后配置文件内容："
cat "${configfile}"
echo "重启虚拟机。请使用新IP($IP)重新登陆。"
shutdown -r now
