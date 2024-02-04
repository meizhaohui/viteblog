#!/bin/bash
# filename: clone_vm.sh
# author:   meizhaohui
old_vmname=$1
new_vmname=$2
old_ip=$3
new_ip=$4
isrunning_flag=$(VBoxManage list runningvms|grep -c "${old_vmname}")
if [[ "${isrunning_flag}" -gt 0 ]]; then
    echo "${old_vmname} 虚拟机正在运行，禁止克隆，请退出"
    exit 1
else
    echo "${old_vmname} 虚拟机未运行，开始克隆"
fi
VBoxManage clonevm "${old_vmname}" --name "${new_vmname}" --register && echo "虚拟机 ${new_vmname} 克隆成功" || exit 2
echo "启动虚拟机 ${new_vmname}"
VBoxManage startvm "${new_vmname}" --type headless
sleep 60
# cat change_ip.sh |ssh root@192.168.56.101 "bash -s" "192.168.56.110"
cat change_ip.sh |ssh root@${old_ip} "bash -s" "${new_ip}"
