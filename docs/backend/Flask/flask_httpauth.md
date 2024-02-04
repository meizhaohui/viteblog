# 接口认证管理之Flask_HTTPAuth

- pypi页面：[https://pypi.org/project/Flask-HTTPAuth/](https://pypi.org/project/Flask-HTTPAuth/)
- 官方文档：[https://flask-httpauth.readthedocs.io/en/latest/](https://flask-httpauth.readthedocs.io/en/latest/)
- 安装：`pip install Flask-HTTPAuth`。

## 用户名密码认证

可以使用用户名密码的方式进行基本认证。官方给出的示例代码：

```python
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


if __name__ == '__main__':
    app.run()

```

函数`verify_password`将会校验用户名，以及加密后的用户密码。

```sh
 python3
Python 3.8.2 (default, Dec 21 2020, 15:06:04)
[Clang 12.0.0 (clang-1200.0.32.29)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from werkzeug.security import generate_password_hash, check_password_hash
>>> passwd = 'hello'
>>> secure_passwd = generate_password_hash(passwd)
>>> secure_passwd
'pbkdf2:sha256:150000$9vtnh4rA$775ed39a2138da674805b4e7cf78230c0b714f88823b11e99b1b640aaf7eb9bc'
>>> check_password_hash(secure_passwd, passwd)
True
>>> exit()
```

`generate_password_hash(passwd)`会对用户密码原文进行加密，而`check_password_hash(secure_passwd, passwd)`会校验加密后的密码`secure_passwd`与密码原文`passwd`是否匹配。

我们在`/etc/hosts`中配置一下域名映射，增加以下内容：

```ini
# test flask
127.0.0.1 testflask.com
```



运行Flask程序，访问`http://testflask.com:5000/`,可以看到需要输入用户名和密码信息：

![](/img/20210506212631.png)

如果点击`取消`，则页面会显示`Unauthorized Access`表示未经授权的访问。我们使用`curl`命令来测试一下：

```sh
$ curl http://testflask.com:5000/
Unauthorized Access
$ curl -i http://testflask.com:5000/
HTTP/1.0 401 UNAUTHORIZED
Content-Type: text/html; charset=utf-8
Content-Length: 19
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Thu, 06 May 2021 13:58:05 GMT

Unauthorized Access
```

直接请求，则提示未授权。

增加用户名和密码信息：

```sh
$ curl -u john:hello http://testflask.com:5000/
Hello, john!                                                                                                         $ curl -u john:hello -i http://testflask.com:5000/
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 12
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Thu, 06 May 2021 13:30:24 GMT

Hello, john!
$ curl -u susan:bye -i http://testflask.com:5000/
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 13
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Thu, 06 May 2021 13:31:43 GMT

Hello, susan!
```

当指定用户名和密码时，能正常访问信息。

## 异常处理

我们在代码中增加异常处理，未认证用户提示'未授权，禁止访问'信息。修改代码：

```sh
from flask import Flask, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# 解决中文乱码的问题，将json数据内的中文正常显示
app.config['JSON_AS_ASCII'] = False

auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': '未授权，禁止访问'}), 403)


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


if __name__ == '__main__':
    app.run()

```

然后再使用`curl`命令调用：

```sh
$ curl -i http://testflask.com:5000/
HTTP/1.0 403 FORBIDDEN
Content-Type: application/json
Content-Length: 42
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Thu, 06 May 2021 13:55:17 GMT

{
  "error": "未授权，禁止访问"
}
```



## 通过Token认证

我们也可以通过Token的方式进行认证。官方示例如下：

```python
from flask import Flask
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run()
```

我们可以使用Postman进行API测试：

![](/img/20210506220650.png)

此时，使用`curl`命令发送请求，需要设置请求头：

```sh
$ curl -H "Authorization:Bearer secret-token-1" -i http://testflask.com:5000/
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 12
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Thu, 06 May 2021 14:10:31 GMT

Hello, john!

$ curl -H "Authorization:Bearer secret-token-2" -i http://testflask.com:5000/
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 13
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Thu, 06 May 2021 14:11:24 GMT

Hello, susan!
```

注意`"Authorization:Bearer *****"`处通过`Bearer `来指定认证类型。

## 多重认证

Flask-HTTPAuth扩展还支持几种不同认证的组合，比如上面介绍的`HTTPBasicAuth`和`HTTPTokenAuth`，我们可以将两者组合在一起，其中任意一个认证通过，即可以访问应用视图。实现起来也很简单，只需将不同的认证实例化为不同的对象，并将其传入`MultiAuth`对象即可。

修改后的代码如下：

```python
from flask import Flask, make_response, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# 解决中文乱码的问题，将json数据内的中文正常显示
app.config['JSON_AS_ASCII'] = False

basic_auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

token_auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

# 将需要支持的认证实例化传入到MultiAuth对象
multi_auth = MultiAuth(basic_auth, token_auth)


@token_auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@basic_auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@basic_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': '未授权，禁止访问'}), 403)


@token_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': '未授权，禁止访问'}), 403)


@app.route('/')
@multi_auth.login_required
def index():
    return "Hello, {}!".format(multi_auth.current_user())


if __name__ == '__main__':
    app.run()

```

再次调用接口：

```sh
$ curl -u susan:bye -i http://testflask.com:5000/
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 13
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Thu, 06 May 2021 14:23:11 GMT

Hello, susan!
$ curl -H "Authorization:Bearer secret-token-2" -i http://testflask.com:5000/
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 13
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Thu, 06 May 2021 14:23:04 GMT

Hello, susan!
```

可以看到通过用户名密码方式、Token方式都能正常调用接口。



参考：

- Flask-HTTPAuth官方文档 [https://flask-httpauth.readthedocs.io/en/latest/](https://flask-httpauth.readthedocs.io/en/latest/)

- flask 简单flask-httpauth验证 [https://my.oschina.net/ahaoboy/blog/1620605](https://my.oschina.net/ahaoboy/blog/1620605)

- Flask扩展系列(九)–HTTP认证 [http://www.bjhee.com/flask-ext9.html](http://www.bjhee.com/flask-ext9.html)

  