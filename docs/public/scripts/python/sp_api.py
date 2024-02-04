import os
from xmlrpc.client import ServerProxy

# 从环境变量中读取supervisor访问用的URL,如 http://localhost:9001/RPC2
sp_url = os.environ.get('SUPERVISOR_URL')
server = ServerProxy(sp_url)
print('supervisord当前状态: {}'.format(server.supervisor.getState()))
print('API版本: {}'.format(server.supervisor.getAPIVersion()))
all_process_info = server.supervisor.getAllProcessInfo()
print('应用状态信息\nname        \tstatename\tdescription')
for info in all_process_info:
    print('{:<15}\t{:<9}\t{}'.format(
        info.get('name'),
        info.get('statename'),
        info.get('description')
    ))
