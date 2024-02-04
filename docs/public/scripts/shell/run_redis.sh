#!/bin/bash
##################################################
#      Filename: run_redis.sh
#        Author: Zhaohui Mei<mzh.whut@gmail.com>
#   Description: Run multiple docker Redis services
#          Time: 2023-08-12 22:41:38
##################################################

# 删除历史运行的redis容器
redis_num=$(docker ps -a | grep -v grep | grep -c redis)
echo "redis num:${redis_num}"
if [ "${redis_num}" -gt 0 ]; then
    docker ps -a | grep -v grep | grep redis | awk '{print $1}' | xargs docker rm -f
fi
sleep 5

# 运行的容器个数
NUM=5
# 初始默认端口号
DEFAULT_PORT=6379
while [ "${NUM}" -gt 0 ]; do
    echo "current number is: ${NUM}, current port is: ${DEFAULT_PORT}"
    docker run -p "${DEFAULT_PORT}":6379 -d --name "redis-${DEFAULT_PORT}" redis:latest
    NUM="$((NUM - 1))"
    DEFAULT_PORT="$((DEFAULT_PORT - 1))"
    sleep 3
done
