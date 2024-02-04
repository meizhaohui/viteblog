#!/bin/bash
##################################################
#      Filename: file_watch.sh
#        Author: Zhaohui Mei<mzh.whut@gmail.com>
#   Description: rsync+inotify实现文件监听，并同步到远程目标端
#   Create Time: 2022-11-13 14:45:47
# Last Modified: 2022-11-13 21:46:47
##################################################

# 目标端(备份服务器)主机IP
dest_host="192.168.56.12"
# 源端需要监听并同步的目录
src_dir="/var/lib/docker"
# 目标端存放备份数据的目录
dest_dir="/var/lib"
# 目标端执行数据同步的用户名
user="root"
inotifywait="/usr/bin/inotifywait"

# -m|--monitor 持续监听
# -r|--recursive 递归模式
# -q|--quiet 减少冗余信息，只打印出事件的信息
# --timefmt 设置时间格式
# --format 设置监听到文件变化时的输出格式
# -e|--event 监听的事件
${inotifywait} -mrq --timefmt '%Y%m%d %H:%M:%S' \
    --format '%T %w%f %e' \
    --event modify,delete,create,attrib "${src_dir}" |
    while read -r files; do
        rsync -avzP --delete --timeout=100 "${src_dir}" "${user}"@"${dest_host}":"${dest_dir}"
        echo "${files} was rsynced" >>/tmp/rsync.log 2>&1
    done
