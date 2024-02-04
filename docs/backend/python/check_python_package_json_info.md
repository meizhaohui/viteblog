# 查看Python第三方包的json信息

[[toc]]

在Python官方包管理网站 [https://pypi.org/](https://pypi.org/) 可以搜索到非常多的第三方包，有时我们需要获取这些包的json信息，则可以使用以下方式进行获取。

## 1. 查看包信息

如查看Flask包的相关信息：

![](/img/Snipaste_2022-08-01_06-18-16.png) 



## 2. 在Web中查看包的json信息

如获取Flask包对就把的json信息，则可以直接访问URL：[https://pypi.org/pypi/Flask/json](https://pypi.org/pypi/Flask/json)， 此时则可以看到其对应的json信息：

![](/img/Snipaste_2022-08-01_06-20-00.png) 



## 3. 使用curl和jq对包的json信息进行处理

有时我们在写脚本时，需要获取包的json信息，并进行过滤处理。

我们可以使用如下方式进行处理。你处理的时候，只需要将Flask替换成你关心的包名就可以了。

```sh
# 获取json信息并保存到本地文件中
$ curl -s https://pypi.org/pypi/Flask/json -o flask.json

# 查看flask.json文件信息，文件内容很长，我们使用jq美化，然后一页一页的输出
$ cat flask.json|jq -C|less
```

效果如下图：

![](/img/Snipaste_2022-08-01_06-27-45.png) 

此处截取部分json数据，如下所示：

```json
{

    "info": {
        "author": "Armin Ronacher",
        "author_email": "armin.ronacher@active-4.com",
        "bugtrack_url": null,
        "classifiers": [
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Framework :: Flask",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Internet :: WWW/HTTP :: WSGI",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
            "Topic :: Software Development :: Libraries :: Application Frameworks"
        ],
        "description": "Flask\n=====\n\nFlask is a lightweight `WSGI`_ web application framework. It is designed\nto make getting started quick and easy, with the ability to scale up to\ncomplex applications. It began as a simple wrapper around `Werkzeug`_\nand `Jinja`_ and has become one of the most popular Python web\napplication frameworks.\n\nFlask offers suggestions, but doesn't enforce any dependencies or\nproject layout. It is up to the developer to choose the tools and\nlibraries they want to use. There are many extensions provided by the\ncommunity that make adding new functionality easy.\n\n.. _WSGI: https://wsgi.readthedocs.io/\n.. _Werkzeug: https://werkzeug.palletsprojects.com/\n.. _Jinja: https://jinja.palletsprojects.com/\n\n\nInstalling\n----------\n\nInstall and update using `pip`_:\n\n.. code-block:: text\n\n    $ pip install -U Flask\n\n.. _pip: https://pip.pypa.io/en/stable/getting-started/\n\n\nA Simple Example\n----------------\n\n.. code-block:: python\n\n    # save this as app.py\n    from flask import Flask\n\n    app = Flask(__name__)\n\n    @app.route(\"/\")\n    def hello():\n        return \"Hello, World!\"\n\n.. code-block:: text\n\n    $ flask run\n      * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n\n\nContributing\n------------\n\nFor guidance on setting up a development environment and how to make a\ncontribution to Flask, see the `contributing guidelines`_.\n\n.. _contributing guidelines: https://github.com/pallets/flask/blob/main/CONTRIBUTING.rst\n\n\nDonate\n------\n\nThe Pallets organization develops and supports Flask and the libraries\nit uses. In order to grow the community of contributors and users, and\nallow the maintainers to devote more time to the projects, `please\ndonate today`_.\n\n.. _please donate today: https://palletsprojects.com/donate\n\n\nLinks\n-----\n\n-   Documentation: https://flask.palletsprojects.com/\n-   Changes: https://flask.palletsprojects.com/changes/\n-   PyPI Releases: https://pypi.org/project/Flask/\n-   Source Code: https://github.com/pallets/flask/\n-   Issue Tracker: https://github.com/pallets/flask/issues/\n-   Website: https://palletsprojects.com/p/flask/\n-   Twitter: https://twitter.com/PalletsTeam\n-   Chat: https://discord.gg/pallets\n",
        "description_content_type": "text/x-rst",
        "docs_url": null,
        "download_url": "",
        "downloads": {
            "last_day": -1,
            "last_month": -1,
            "last_week": -1
        },
        "home_page": "https://palletsprojects.com/p/flask",
        "keywords": "",
        "license": "BSD-3-Clause",
        "maintainer": "Pallets",
        "maintainer_email": "contact@palletsprojects.com",
        "name": "Flask",
        "package_url": "https://pypi.org/project/Flask/",
        "platform": null,
        "project_url": "https://pypi.org/project/Flask/",
        "project_urls": {
            "Changes": "https://flask.palletsprojects.com/changes/",
            "Chat": "https://discord.gg/pallets",
            "Documentation": "https://flask.palletsprojects.com/",
            "Donate": "https://palletsprojects.com/donate",
            "Homepage": "https://palletsprojects.com/p/flask",
            "Issue Tracker": "https://github.com/pallets/flask/issues/",
            "Source Code": "https://github.com/pallets/flask/",
            "Twitter": "https://twitter.com/PalletsTeam"
        },
        "release_url": "https://pypi.org/project/Flask/2.1.3/",
        "requires_dist": [
            "Werkzeug (>=2.0)",
            "Jinja2 (>=3.0)",
            "itsdangerous (>=2.0)",
            "click (>=8.0)",
            "importlib-metadata (>=3.6.0) ; python_version < \"3.10\"",
            "asgiref (>=3.2) ; extra == 'async'",
            "python-dotenv ; extra == 'dotenv'"
        ],
        "requires_python": ">=3.7",
        "summary": "A simple framework for building complex web applications.",
        "version": "2.1.3",
        "yanked": false,
        "yanked_reason": null
    },
    "last_serial": 14425946,
    "releases": {
        "0.1": [
            {
                "comment_text": "",
                "digests": {
                    "md5": "d0c458397c49114fa279716798ca80c8",
                    "sha256": "9da884457e910bf0847d396cb4b778ad9f3c3d17db1c5997cb861937bd284237"
                },
                "downloads": -1,
                "filename": "Flask-0.1.tar.gz",
                "has_sig": false,
                "md5_digest": "d0c458397c49114fa279716798ca80c8",
                "packagetype": "sdist",
                "python_version": "source",
                "requires_python": null,
                "size": 9168,
                "upload_time": "2010-04-16T14:29:37",
                "upload_time_iso_8601": "2010-04-16T14:29:37.458396Z",
                "url": "https://files.pythonhosted.org/packages/6e/49/43b514bfdaf4af12e6ef1f17aa25447157bcbb864c07775dacd72e8c8e02/Flask-0.1.tar.gz",
                "yanked": false,
                "yanked_reason": null
            }
        ],
        "0.10": [
            {
                "comment_text": "",
                "digests": {
                    "md5": "92bc6b6ebd37d3120c235430a0491a15",
                    "sha256": "84b3b352c3d6b888ee56c645d83a3b54a86fab6236be3d44fd55a275f2c8b207"
                },
                "downloads": -1,
                "filename": "Flask-0.10.tar.gz",
                "has_sig": false,
                "md5_digest": "92bc6b6ebd37d3120c235430a0491a15",
                "packagetype": "sdist",
                "python_version": "source",
                "requires_python": null,
                "size": 544031,
                "upload_time": "2013-06-13T08:35:51",
                "upload_time_iso_8601": "2013-06-13T08:35:51.483512Z",
                "url": "https://files.pythonhosted.org/packages/f3/46/53d83cbdb79b27678c7b032d5deaa556655dd034cc747ee609b3e3cbf95b/Flask-0.10.tar.gz",
                "yanked": false,
                "yanked_reason": null
            }
        ],
        .... 此处省略其他版本
         "2.1.3": [
            {
                "comment_text": "",
                "digests": {
                    "md5": "6a302f80514c2da4686b79bc734e2f70",
                    "sha256": "9013281a7402ad527f8fd56375164f3aa021ecfaff89bfe3825346c24f87e04c"
                },
                "downloads": -1,
                "filename": "Flask-2.1.3-py3-none-any.whl",
                "has_sig": true,
                "md5_digest": "6a302f80514c2da4686b79bc734e2f70",
                "packagetype": "bdist_wheel",
                "python_version": "py3",
                "requires_python": ">=3.7",
                "size": 95556,
                "upload_time": "2022-07-13T20:55:57",
                "upload_time_iso_8601": "2022-07-13T20:55:57.512393Z",
                "url": "https://files.pythonhosted.org/packages/af/6a/00d144ac1626fbb44c4ff36519712e258128985a5d0ae43344778ae5cbb9/Flask-2.1.3-py3-none-any.whl",
                "yanked": false,
                "yanked_reason": null
            },
            {
                "comment_text": "",
                "digests": {
                    "md5": "3c1d9aaeaed0f0b72b8b0aa5bc069f45",
                    "sha256": "15972e5017df0575c3d6c090ba168b6db90259e620ac8d7ea813a396bad5b6cb"
                },
                "downloads": -1,
                "filename": "Flask-2.1.3.tar.gz",
                "has_sig": true,
                "md5_digest": "3c1d9aaeaed0f0b72b8b0aa5bc069f45",
                "packagetype": "sdist",
                "python_version": "source",
                "requires_python": ">=3.7",
                "size": 630206,
                "upload_time": "2022-07-13T20:56:00",
                "upload_time_iso_8601": "2022-07-13T20:56:00.126199Z",
                "url": "https://files.pythonhosted.org/packages/5b/77/3accd62b8771954e9584beb03f080385b32ddcad30009d2a4fe4068a05d9/Flask-2.1.3.tar.gz",
                "yanked": false,
                "yanked_reason": null
            }
        ]
    },
    "urls": [
        {
            "comment_text": "",
            "digests": {
                "md5": "6a302f80514c2da4686b79bc734e2f70",
                "sha256": "9013281a7402ad527f8fd56375164f3aa021ecfaff89bfe3825346c24f87e04c"
            },
            "downloads": -1,
            "filename": "Flask-2.1.3-py3-none-any.whl",
            "has_sig": true,
            "md5_digest": "6a302f80514c2da4686b79bc734e2f70",
            "packagetype": "bdist_wheel",
            "python_version": "py3",
            "requires_python": ">=3.7",
            "size": 95556,
            "upload_time": "2022-07-13T20:55:57",
            "upload_time_iso_8601": "2022-07-13T20:55:57.512393Z",
            "url": "https://files.pythonhosted.org/packages/af/6a/00d144ac1626fbb44c4ff36519712e258128985a5d0ae43344778ae5cbb9/Flask-2.1.3-py3-none-any.whl",
            "yanked": false,
            "yanked_reason": null
        },
        {
            "comment_text": "",
            "digests": {
                "md5": "3c1d9aaeaed0f0b72b8b0aa5bc069f45",
                "sha256": "15972e5017df0575c3d6c090ba168b6db90259e620ac8d7ea813a396bad5b6cb"
            },
            "downloads": -1,
            "filename": "Flask-2.1.3.tar.gz",
            "has_sig": true,
            "md5_digest": "3c1d9aaeaed0f0b72b8b0aa5bc069f45",
            "packagetype": "sdist",
            "python_version": "source",
            "requires_python": ">=3.7",
            "size": 630206,
            "upload_time": "2022-07-13T20:56:00",
            "upload_time_iso_8601": "2022-07-13T20:56:00.126199Z",
            "url": "https://files.pythonhosted.org/packages/5b/77/3accd62b8771954e9584beb03f080385b32ddcad30009d2a4fe4068a05d9/Flask-2.1.3.tar.gz",
            "yanked": false,
            "yanked_reason": null
        }
    ],
    "vulnerabilities": [ ]

}
```

可以看到，json内容非常多。

此处尝试获取一些关键信息：

- 获取name包名属性

```sh
$ cat flask.json|jq '.info.name'
"Flask"
```

- 获取author作者属性

```sh
$ cat flask.json|jq '.info.author'
"Armin Ronacher"
```

- 获取依赖包信息

```sh
$ cat flask.json|jq '.info.requires_dist'
[
  "Werkzeug (>=2.0)",
  "Jinja2 (>=3.0)",
  "itsdangerous (>=2.0)",
  "click (>=8.0)",
  "importlib-metadata (>=3.6.0) ; python_version < \"3.10\"",
  "asgiref (>=3.2) ; extra == 'async'",
  "python-dotenv ; extra == 'dotenv'"
]
```

前三个信息示例截图信息：

![](/img/Snipaste_2022-08-01_06-44-54.png) 

- 查看2.1.3版本的信息

```sh
$ cat flask.json|jq '.releases."2.1.3"'
[
  {
    "comment_text": "",
    "digests": {
      "md5": "6a302f80514c2da4686b79bc734e2f70",
      "sha256": "9013281a7402ad527f8fd56375164f3aa021ecfaff89bfe3825346c24f87e04c"
    },
    "downloads": -1,
    "filename": "Flask-2.1.3-py3-none-any.whl",
    "has_sig": true,
    "md5_digest": "6a302f80514c2da4686b79bc734e2f70",
    "packagetype": "bdist_wheel",
    "python_version": "py3",
    "requires_python": ">=3.7",
    "size": 95556,
    "upload_time": "2022-07-13T20:55:57",
    "upload_time_iso_8601": "2022-07-13T20:55:57.512393Z",
    "url": "https://files.pythonhosted.org/packages/af/6a/00d144ac1626fbb44c4ff36519712e258128985a5d0ae43344778ae5cbb9/Flask-2.1.3-py3-none-any.whl",
    "yanked": false,
    "yanked_reason": null
  },
  {
    "comment_text": "",
    "digests": {
      "md5": "3c1d9aaeaed0f0b72b8b0aa5bc069f45",
      "sha256": "15972e5017df0575c3d6c090ba168b6db90259e620ac8d7ea813a396bad5b6cb"
    },
    "downloads": -1,
    "filename": "Flask-2.1.3.tar.gz",
    "has_sig": true,
    "md5_digest": "3c1d9aaeaed0f0b72b8b0aa5bc069f45",
    "packagetype": "sdist",
    "python_version": "source",
    "requires_python": ">=3.7",
    "size": 630206,
    "upload_time": "2022-07-13T20:56:00",
    "upload_time_iso_8601": "2022-07-13T20:56:00.126199Z",
    "url": "https://files.pythonhosted.org/packages/5b/77/3accd62b8771954e9584beb03f080385b32ddcad30009d2a4fe4068a05d9/Flask-2.1.3.tar.gz",
    "yanked": false,
    "yanked_reason": null
  }
]
```

你还可以使用jq命令过滤更多你想要的信息。
