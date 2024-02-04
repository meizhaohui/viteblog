#!/bin/bash
##################################################
#      Filename: file_watch_v2.sh
#        Author: Zhaohui Mei<mzh.whut@gmail.com>
#   Description: rsync+inotify实现文件监听，并同步到远程目标端
#   Create Time: 2022-11-13 14:45:47
# Last Modified: 2022-11-13 23:46:47
##################################################

# 脚本路径
SCRIPT_PATH="$(cd -P "$(dirname "$0")" && pwd)"
if [[ ! -f "${SCRIPT_PATH}/utils.sh" ]]; then
    echo "utils.sh文件不存在，请检查！"
    exit 1
fi
# load the utilities
source "${SCRIPT_PATH}/utils.sh"
# 配置文件
CONFIG_FILE="${SCRIPT_PATH}/file_watch.conf"
# 源端需要监控的目录列表组成的文件
SRC_LIST_FILE="${SCRIPT_PATH}/dir_list.txt"
# 源端监听文件变化的程序
inotifywait="/usr/bin/inotifywait"

# 定义函数
#######################################
# 读取配置文件
get_info() {
    keyword="$1"
    info=$(grep -v '^#' "${CONFIG_FILE}" | grep -v '^$' | grep "^${keyword} " | awk -F '[= ]+' '{print $2}')
    echo "${info}"
}
#######################################

msg_success "Step 1: 检查配置文件正确性"
all_src_dirs=$(grep '^SRC_DIR_' "${CONFIG_FILE}" | awk '{print $1}' | sed 's/SRC_DIR_//g' | sort -n)
all_dest_dirs=$(grep '^DEST_DIR_' "${CONFIG_FILE}" | awk '{print $1}' | sed 's/DEST_DIR_//g' | sort -n)
# 匹配关系数量
if [[ "${all_src_dirs}" != "${all_dest_dirs}" ]]; then
    msg_warn "配置文件${CONFIG_FILE}中源端SRC_DIR与目标端DEST_DIR之间的映射匹配关系异常，请检查！"
    exit 1
fi
all_map_count=$(grep -c '^SRC_DIR_' "${CONFIG_FILE}")
dest_host=$(get_info "DEST_HOST")
msg_info "目标端IP地址: ${dest_host}"
sync_num=$(get_info "SYNC_NUM")
msg_info "同步目录组总数: ${sync_num}"
if [[ "${all_map_count}" -ne "${sync_num}" ]]; then
    msg_warn "配置文件${CONFIG_FILE}中同步的配置信息组数${all_map_count}与SYNC_NUM=${sync_num} 的值不一致，请检查！"
    exit 1
fi
msg_success "Step 1: 检查配置文件正确性 ====> OK!"

msg_success "Step 2: 获取监听文件夹信息"
true >"${SRC_LIST_FILE}"
for num in $(seq "${all_map_count}"); do
    src_dir=$(get_info "SRC_DIR_${num}")
    msg_info "源端需要监听并同步的目录：${src_dir}"
    echo "${src_dir}" >>"${SRC_LIST_FILE}"
done

msg_success "Step 2: 获取监听文件夹信息 ====> OK!"

# 文件夹同步
do_rsync() {
    file="$1"
    msg_info "监测到文件发生变化：${file}"
    change_dir=$(while read -r line; do echo "${file}" | grep -q "${line}" && echo "${line}"; done <"${SRC_LIST_FILE}")
    msg_info "对应的配置文件源路径:${change_dir}"
    group_num=$(grep -E "SRC_DIR_.*= ${change_dir}" "${CONFIG_FILE}" | awk '{print $1}' | sed 's/SRC_DIR_//g')
    msg_info "当前正在处理第 ${group_num} 组文件同步"
    src_dir=$(get_info "SRC_DIR_${group_num}")
    dest_dir=$(get_info "DEST_DIR_${group_num}")
    username=$(get_info "USER_${group_num}")
    if [[ -z "${username}" ]]; then
        msg_warn "未配置目标端执行数据同步的用户名，使用默认用户名root"
        username="root"
    fi
    msg_info "源端需要监听并同步的目录：${src_dir}"
    msg_info "目标端存放备份数据的目录：${dest_dir}"
    msg_info "目标端执行数据同步的用户名：${username}"
    rsync -avzP --delete --timeout=100 "${src_dir}" "${username}"@"${dest_host}":"${dest_dir}"
    echo "${file} was rsynced" >>/tmp/rsync.log 2>&1

}

# 监听目录
inotify_dirs() {
    src_list_file="$1"
    # -m|--monitor 持续监听
    # -r|--recursive 递归模式
    # -q|--quiet 减少冗余信息，只打印出事件的信息
    # --timefmt 设置时间格式
    # --format 设置监听到文件变化时的输出格式
    # -e|--event 监听的事件
    # --fromfile 从文件中写取待监听的文件夹信息，一行一个目录信息
    ${inotifywait} -mrq --timefmt '%Y%m%d %H:%M:%S' \
        --format '%T %w%f %e' \
        --event modify,delete,create,attrib --fromfile "${src_list_file}" |
        while read -r files; do
            # 执行同步操作
            do_rsync "${files}"
        done
}

inotify_dirs "${SRC_LIST_FILE}"
