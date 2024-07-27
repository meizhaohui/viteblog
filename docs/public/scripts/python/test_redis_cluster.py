# filename: test_redis_cluster.py
# pip install redis
from redis import RedisCluster
from redis.cluster import ClusterNode

password = "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-" \
           "pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
# 假设你的Redis集群节点在本地的6379, 6380, 6381, 6382, 6383, 6384端口上
startup_nodes = [
    ClusterNode(host="192.168.56.121", port="6379"),
    ClusterNode(host="192.168.56.121", port="6380"),
    ClusterNode(host="192.168.56.121", port="6381"),
    ClusterNode(host="192.168.56.121", port="6382"),
    ClusterNode(host="192.168.56.121", port="6383"),
    ClusterNode(host="192.168.56.121", port="6384"),

]

# 连接到Redis集群
rc = RedisCluster(startup_nodes=startup_nodes,
                  decode_responses=True,
                  password=password)

# 使用Redis集群
rc.set("foo", "bar")
print(rc.get("foo"))
print(rc.get("name"))
print(rc.get("num"))
