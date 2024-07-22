# filename: test_redis_sentinel.py
# pip install redis
from redis import Sentinel
 
# 哨兵的地址和端口，格式为(host, port)
sentinels = [('192.168.56.121', 49736), ('192.168.56.122', 49736), ('192.168.56.123', 49736)]
password = "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
service_name = 'mymaster'
# 创建Sentinel实例
# sentinel_kwargs 用来配置哨兵的密码。password用来配置redis密码
sentinel = Sentinel(sentinels, socket_timeout=0.1, sentinel_kwargs={'password': password}, password=password)
 
# 获取主服务器
master = sentinel.master_for(service_name, socket_timeout=0.1, password=password)
print(f'master:{master}')
master_info = sentinel.discover_master(service_name)
master_ip = master_info[0]
master_port = master_info[1]
print(f'master ip:{master_ip}')
print(f'master port:{master_port}')
 
# 获取从服务器
slave = sentinel.slave_for(service_name, socket_timeout=0.1, password=password)
 
# 使用主服务器或从服务器进行操作
master.set('key', 'value')
print(master.get('key'))
print(master.get('name'))
print(master.get('num'))
master.set('client', 'client')