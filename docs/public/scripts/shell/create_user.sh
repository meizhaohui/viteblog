#!/bin/bash
##################################################
#      Filename: create_user.sh
#        Author: Zhaohui Mei<mzh.whut@gmail.com>
#   Description: Create user with password
#   Create Time: 2022-05-07 23:41:54
# Last Modified: 2022-05-07 23:44:17
##################################################

# 用户名
username="$1"
# 明文密码
password="$2"
# 加密后的密码字符串
encrypted_password=$(echo "${password}" | openssl passwd -1 -salt $(< /dev/urandom tr -dc '[:alnum:]' | head -c 32) -stdin)
echo useradd -p "${encrypted_password}" "${username}"
# 创建用户并指定密码
useradd -p "${encrypted_password}" "${username}"
out_ip=$(curl ifconfig.me)
in_ip=$(hostname -I|awk '{print $1}')
# 提示信息
echo -e "\033[1;32m恭喜您，用户创建成功，请使用如下信息连接服务器:\033[0m"
echo "外网IP: ${out_ip}"
echo "内网IP: ${in_ip}"
echo "用户名: ${username}"
echo "密  码: ${password}"

