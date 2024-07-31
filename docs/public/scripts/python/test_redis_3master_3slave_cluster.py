# filename: test_redis_3master_3slave_cluster.py
# pip install redis
from redis import RedisCluster
from redis.cluster import ClusterNode

password = "fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMV" \
           "i8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R"
# 假设你的Redis集群节点在三个主机上的29736, 29737端口上
startup_nodes = [
    ClusterNode(host="192.168.56.121", port="29736"),
    ClusterNode(host="192.168.56.121", port="29737"),
    ClusterNode(host="192.168.56.122", port="29736"),
    ClusterNode(host="192.168.56.122", port="29737"),
    ClusterNode(host="192.168.56.123", port="29736"),
    ClusterNode(host="192.168.56.123", port="29737"),

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
