#!/bin/bash
##################################################
#      Filename: bashrc.sh
#        Author: Zhaohui Mei<mzh.whut@gmail.com>
#   Description: 记录.bashrc配置
#   Create Time: 2022-05-22 17:12:19
# Last Modified: 2022-09-17 20:40:05
##################################################

###########################################################
# Environments
# locale and language
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
# history
export HISTTIMEFORMAT="%d/%m/%y %T "
export PROMPT_COMMAND="history -a; $PROMPT_COMMAND"
# Set the JQ color scheme
export JQ_COLORS="1;31:7;31:1;32:0;37:0;32:1;33:1;37"

# python pipenv environment
export PIPENV_VENV_IN_PROJECT=1
export PIPENV_PYPI_MIRROR=https://mirrors.aliyun.com/pypi/simple

# Golang environment settings
export GOROOT=/usr/lib/golang # golang install path
export GOPATH=~/data/go_data  # golang workspace
export GOBIN=${GOPATH}/bin    # golang exe files
export PATH=${GOBIN}:${PATH}
export GOPROXY=https://goproxy.cn
export GO111MODULE=on
###########################################################

###########################################################
# 常用快捷命令
# alias rm='echo "rm can not be used,pleuse use safe-rm or mv"'
alias rm='echo -e "Info:\033[31mrm can not be used, please use \033[32msafe-rm\033[0m or \033[32mtrash-put\033[0m\n"'
alias cp='cp -i'
alias mv='mv -i'
alias vi='vim'
alias v.='vi ~/.bashrc'
alias s.='source ~/.bashrc && echo "reload OK"'
alias now='date +"%Y年%m月%d日_%H:%M:%S"'
alias tar='tar --no-same-owner'
alias cd1='cd ..'
alias cd2='cd ../..'
alias cd3='cd ../../..'
alias cd4='cd ../../../..'
alias cd5='cd ../../../../..'
alias cd6='cd ../../../../../..'
alias cdnet='cd /etc/sysconfig/network-scripts/'
alias sr='sudo su - root'
alias sudo='sudo '
alias ping='ping -c 3'
alias grep='grep --color=auto'
# 获取外网IP,不要使用小写ip作为快捷命令
alias IP='curl icanhazip.com'
# 软链接帮助
alias lnhelp='echo "ln -s exist_file soft_file"'
# 修改终端提示符
alias chps='export PS1="# "'
# 重置只读用户密码
alias resetreader='newpassword=$(date|md5sum|head -c 16);echo -n "$newpassword"|passwd --stdin reader > /dev/null && echo -e "username: reader\npassword: $newpassword" || echo "[Error] password reset failed."'

# 修改是否可以密码登陆
alias clm='change_login_mode'
function change_login_mode() {
    mode=$(sudo grep -c '^PasswordAuthentication yes' /etc/ssh/sshd_config)
    if [[ "${mode}" -eq 1 ]]; then
        sudo sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
    else
        sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
    fi
    sudo systemctl restart sshd
}

# 快速杀掉登陆用户进程
alias fastkill='kill_pts_login'
function kill_pts_login() {
    sudo kill -9 $(sudo ps -ef | grep "pts/$1$" | grep -v 'grep' | awk '{print $2}') && echo "killed the pts/$1 login"
}

# 代码部署
alias run='pushd ~/vueblog && sh deploy.sh'
alias autodeploy='auto_deploy'
function auto_deploy() {
    pushd ~/vueblog && pwd
    current=$(git log --pretty=oneline -n 1 | head)
    git pull
    new=$(git log --pretty=oneline -n 1 | head)
    if [[ "${current}" != "${new}" ]]; then
        echo "远程仓库有更新，开始自动部署"
        sh deploy.sh && echo "自动部署完成！"
    fi
    popd
}
###########################################################

###########################################################
# 防火墙相关
# list firewall port
# 列出防火墙放行端口
alias lfp='firewall-cmd --list-all'

# 防火墙增加放行端口
alias afp='add_firewall_port'
function add_firewall_port() {
    port=$1
    sudo firewall-cmd --zone=public --add-port="${port}/tcp" --permanent && sudo firewall-cmd --reload && sudo firewall-cmd --list-all
}

# 防火墙删除放行端口
alias dfp='remove_firewall_port'
function remove_firewall_port() {
    port=$1
    sudo firewall-cmd --zone=public --remove-port="${port}/tcp" --permanent && sudo firewall-cmd --reload && sudo firewall-cmd --list-all
}
###########################################################

###########################################################
# 代码编译
alias gcco='compile_c_code'
function compile_c_code() {
    filename="$1"
    outfile=$(basename "${filename}" | awk '{print $0".out"}')
    suffix=$(basename "${filename}" | awk -F'.' '{print $NF}')
    if [[ "${suffix}" == "cpp" ]]; then
        # you can use two methods to compile cpp code
        # gcc -lstdc++ -o
        g++ "${filename}" -o "${outfile}"
    else
        gcc "${filename}" -o "${outfile}"
    fi
}
###########################################################

###########################################################
# Docker commands
# 进入到docker容器中
alias dkin='dockerin'
function dockerin() {
    docker exec -it $1 /bin/bash
}
# 查看某个容器
alias dkc='docker_check'
function docker_check() {
    container_name=$1
    docker ps | head -n 1
    docker ps | grep "${container_name}"
}

# 删除某个容器
alias dkr='remove_docker_container'
function remove_docker_container() {
    container_name=$1
    docker stop "${container_name}"
    docker rm "${container_name}"
}
alias dpa='docker ps -a'
# go to the docker images directory
alias cdi='cd /var/lib/docker/image/overlay2/imagedb/content/sha256'
alias di='docker images'
###########################################################

# 博客快速设置提交内容
alias gfc='git_fast_commit'
function git_fast_commit() {
    message=$1
    folder_info=$(git status --show-stash | grep modified | sed 's/ //g' | grep -o 'docs/.*/' | sort | uniq | head -n 1 | awk -F"/" '{print $2"("$3"):"}')
    git commit -m"${folder_info}${message}"
    git --no-pager log -n 1
}

# 自动提交markdown相关的修改，避免typora异常
alias autopush='auto_commit_to_github'
function auto_commit_to_github() {
    pushd /drives/e/data/viteblog || exit 1
    now=$(date +"%Y%m%d_%H:%M:%S")
    folder_info=$(git status --show-stash | grep modified | grep -v 'docs/public' | sed 's/ //g' | grep -o 'docs/.*/' | sort | uniq | head -n 1 | awk -F"/" '{print $2"("$3"):"}')
    message="${folder_info} Automatically submit code on ${now}"
    git add .
    git commit -m "${message}"
    git push && rc "=" 30 && git push gitee main
}
