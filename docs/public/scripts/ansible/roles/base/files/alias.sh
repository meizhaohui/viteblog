# meizhaohui add this
export LANG=en_US.UTF-8
alias vim='vi'
alias s.='source ~/.bashrc && echo "Reload OK"'
alias v.='vim ~/.bashrc'
alias va='vim ~/.alias.sh'
alias ls='ls --color=auto'
alias ltime='ls -lah --time-style=long-iso --color=always'
alias grep='grep --color=always'
# 清屏
alias c='clear'
# 切换目录
alias cd1='cd ..'
alias cd2='cd ../..'
alias cd3='cd ../../..'
# diff命令输出颜色
alias diff='colordiff'
# 历史命令
alias h='history'
# 查看后台任务
alias j='jobs -l'
# 日期时间
alias now='date +"%Y年%m月%d日 %H:%M:%S"'
alias today='date +"%Y%m%d"'
# 增加安全性
# Parenting changing perms on / #
alias chown='chown --preserve-root'
alias chmod='chmod --preserve-root'
alias chgrp='chgrp --preserve-root'
# 进程搜索
alias psg='ps -ef|grep'
# 你可以在此追加其他别名
