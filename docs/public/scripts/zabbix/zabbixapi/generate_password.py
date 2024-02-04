from common_tools import decrypt, encrypt

# 明文密码
password = 'zabbix'
print(encrypt(password))
print(decrypt(encrypt(password)))
