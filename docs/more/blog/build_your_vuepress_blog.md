# VuePress从零开始搭建自己的博客 基础配置

[[toc]]

注册域名(hellogitlab.com)后，需要让网站运行起来，发现VuePress不错，尝试使用VuePress搭建自己的博客系统。

## VuePress是什么？
VuePress是以Vue驱动的静态网站生成器，是一个由Vue、Vue Router和webpack驱动的单页应用。在VuePress中，你可以使用Markdown编写文档，然后生成网页，每一个由VuePress生成的页面都带有预渲染好的HTML，也因此具有非常好的加载性能和搜索引擎优化。同时，一旦页面被加载，Vue将接管这些静态内容，并将其转换成一个完整的单页应用，其他的页面则会只在用户浏览到的时候才按需加载。

详情请看[VuePress官方文档](https://vuepress.vuejs.org/zh/)

## VuePress特性
+ 为技术文档而优化的内置Markdown拓展
+ 在Markdown文件中使用Vue组件的能力
+ Vue驱动的自定义主题系统
+ 自动生成Service Worker(支持PWA)
+ Google Analytics集成
+ 基于Git的"最后更新时间"
+ 多语言支持
+ 响应式布局

## 环境搭建

### 安装
VuePress支持使用Yarn和npm来安装，Node.js版本需要>=8才可以。

### yarn安装

参考：
- [yarn安装指导](https://yarnpkg.com/en/docs/install#centos-stable)


- 安装node.js
```sh
[root@hellogitlab ~]# curl --silent --location https://rpm.nodesource.com/setup_8.x | bash -

## Installing the NodeSource Node.js 8.x LTS Carbon repo...


## Inspecting system...

+ rpm -q --whatprovides redhat-release || rpm -q --whatprovides centos-release || rpm -q --whatprovides cloudlinux-release || rpm -q --whatprovides sl-release
+ uname -m

## Confirming "el7-x86_64" is supported...

+ curl -sLf -o /dev/null 'https://rpm.nodesource.com/pub_8.x/el/7/x86_64/nodesource-release-el7-1.noarch.rpm'

## Downloading release setup RPM...

+ mktemp
+ curl -sL -o '/tmp/tmp.3ZGyljVBAB' 'https://rpm.nodesource.com/pub_8.x/el/7/x86_64/nodesource-release-el7-1.noarch.rpm'

## Installing release setup RPM...

+ rpm -i --nosignature --force '/tmp/tmp.3ZGyljVBAB'

## Cleaning up...

+ rm -f '/tmp/tmp.3ZGyljVBAB'

## Checking for existing installations...

+ rpm -qa 'node|npm' | grep -v nodesource

## Run `sudo yum install -y nodejs` to install Node.js 8.x LTS Carbon and npm.
## You may also need development tools to build native addons:
     sudo yum install gcc-c++ make
## To install the Yarn package manager, run:
     curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo
     sudo yum install yarn

# 安装node.js
[root@hellogitlab ~]# yum install nodejs -y
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package nodejs.x86_64 2:8.17.0-1nodesource will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================================================================================================
 Package                          Arch                             Version                                           Repository                            Size
================================================================================================================================================================
Installing:
 nodejs                           x86_64                           2:8.17.0-1nodesource                              nodesource                            18 M

Transaction Summary
================================================================================================================================================================
Install  1 Package

Total download size: 18 M
Installed size: 55 M
Downloading packages:
nodejs-8.17.0-1nodesource.x86_64.rpm                                                                                                     |  18 MB  00:00:04     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : 2:nodejs-8.17.0-1nodesource.x86_64                                                                                                           1/1 
  Verifying  : 2:nodejs-8.17.0-1nodesource.x86_64                                                                                                           1/1 

Installed:
  nodejs.x86_64 2:8.17.0-1nodesource                                                                                                                            

Complete!
```

- 查看node.js版本信息
```sh
[root@hellogitlab ~]# node --version
v8.17.0
[root@hellogitlab ~]# node -v
v8.17.0
```

- 添加yarn的yum源
```sh
[root@hellogitlab ~]# curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo
```

- 安装yarn

```sh
[root@hellogitlab ~]# yum install yarn -y 
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package yarn.noarch 0:1.21.1-1 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================================================================================================
 Package                             Arch                                  Version                                    Repository                           Size
================================================================================================================================================================
Installing:
 yarn                                noarch                                1.21.1-1                                   yarn                                1.2 M

Transaction Summary
================================================================================================================================================================
Install  1 Package

Total download size: 1.2 M
Installed size: 5.1 M
Downloading packages:
yarn-1.21.1-1.noarch.rpm                                                                                                                 | 1.2 MB  00:00:05     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : yarn-1.21.1-1.noarch                                                                                                                         1/1 
  Verifying  : yarn-1.21.1-1.noarch                                                                                                                         1/1 

Installed:
  yarn.noarch 0:1.21.1-1                                                                                                                                        

Complete!
```

- 查看yarn的版本信息
```sh
[root@hellogitlab ~]# yarn --version
1.21.1
[root@hellogitlab ~]# yarn -v
1.21.1
```

### 全局安装VuePress

#### 安装VuePress

我们使用``yarn``工具安装VuePress。
```sh
[root@hellogitlab ~]# yarn global add vuepress
yarn global v1.21.1
[1/4] Resolving packages...
warning vuepress > @vuepress/core > @vue/babel-preset-app > core-js@2.6.11: core-js@<3 is no longer maintained and not recommended for usage due to the number of issues. Please, upgrade your dependencies to the actual version of core-js@3.
warning vuepress > @vuepress/core > @vue/babel-preset-app > @babel/runtime-corejs2 > core-js@2.6.11: core-js@<3 is no longer maintained and not recommended for usage due to the number of issues. Please, upgrade your dependencies to the actual version of core-js@3.
[2/4] Fetching packages...
info fsevents@1.2.11: The platform "linux" is incompatible with this module.
info "fsevents@1.2.11" is an optional dependency and failed compatibility check. Excluding it from installation.
[3/4] Linking dependencies...
[4/4] Building fresh packages...
success Installed "vuepress@1.2.0" with binaries:
      - vuepress
Done in 15.16s.
```

- 查看vuepress命令是否可用
```sh
[root@hellogitlab ~]# whereis vuepress
vuepress: /usr/local/bin/vuepress
[root@hellogitlab ~]# vuepress
bash: vuepress: command not found
[root@hellogitlab ~]# ls -lah /usr/local/bin/vuepress 
lrwxrwxrwx 1 root root 55 Dec 29 12:48 /usr/local/bin/vuepress -> ../share/.config/yarn/global/node_modules/.bin/vuepress
```

- 添加软链接
```sh
[root@hellogitlab ~]# ln -s /usr/local/bin/vuepress /usr/bin/vuepress
[root@hellogitlab ~]# vuepress --help
vuepress v1.2.0

Usage:
  $ vuepress <command> [options]

Commands:
  dev [targetDir]    start development server
  build [targetDir]  build dir as static site
  eject [targetDir]  copy the default theme into .vuepress/theme for customization.
  info               Shows debugging information about the local environment

For more info, run any command with the `--help` flag:
  $ vuepress dev --help
  $ vuepress build --help
  $ vuepress eject --help
  $ vuepress info --help

Options:
  -v, --version  Display version number 
  -h, --help     Display this message
[root@hellogitlab ~]# whereis vuepress
vuepress: /usr/bin/vuepress /usr/local/bin/vuepress
```

- 查看vuepress的版本信息
```sh
[root@hellogitlab ~]# vuepress -v
vuepress/1.2.0 linux-x64 node-v8.17.0
```


#### 创建项目目录

创建目录``myblog``
```sh
[root@hellogitlab ~]# mkdir myblog && cd myblog
[root@hellogitlab myblog]# 
[root@hellogitlab myblog]# pwd
/root/myblog
```
#### 初始化项目
```sh
[root@hellogitlab myblog]# yarn init -y
yarn init v1.21.1
warning The yes flag has been set. This will automatically answer yes to all questions, which may have security implications.
success Saved package.json
Done in 0.06s.

[root@hellogitlab myblog]# ls -lah
total 12K
drwxr-xr-x   2 root root 4.0K Dec 29 13:01 .
dr-xr-x---. 15 root root 4.0K Dec 29 13:00 ..
-rw-r--r--   1 root root   87 Dec 29 13:01 package.json
[root@hellogitlab myblog]# cat package.json 
{
  "name": "myblog",
  "version": "1.0.0",
  "main": "index.js",
  "license": "MIT"
}
```
#### 新建docs文件夹
docs文件夹作为项目文档根目录，主要放置Markdown类型的文章和.vuepress文件夹。

```sh
[root@hellogitlab myblog]# mkdir docs
[root@hellogitlab myblog]# ls -lah
total 16K
drwxr-xr-x   3 root root 4.0K Dec 29 13:02 .
dr-xr-x---. 15 root root 4.0K Dec 29 13:00 ..
drwxr-xr-x   2 root root 4.0K Dec 29 13:02 docs
-rw-r--r--   1 root root   87 Dec 29 13:01 package.json
```
#### 设置package.json
VuePress中有两个命令，``vuepress dev docs``命令运行本地服务，通过访问http://localhost:8080即可预览网站，``vuepress build docs``命令用来生成静态文件，默认情况下，放置在docs/.vuepress/dist目录中，当然你也可以在docs/.vuepress/config.js中的dest字段来修改默认存放目录。

在package.json中添加以下内容
```sh
{
  "scripts": {
    "docs:dev": "vuepress dev docs",
    "docs:build": "vuepress build docs"
  }
}
```

添加后，内容如下:
```sh
[root@hellogitlab myblog]# cat package.json 
{
  "name": "myblog",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "docs:dev": "vuepress dev docs",
    "docs:build": "vuepress build docs"
  },
  "license": "MIT"
}
```

#### 创建README.md
在docs目录下新建README.md文件
```
[root@hellogitlab myblog]# echo '# Hello VuePress!' > docs/README.md
[root@hellogitlab myblog]# cat docs/README.md 
# Hello VuePress!
```

#### 运行项目

- 使用``yarn docs:dev``运行项目
```
[root@hellogitlab myblog]# yarn docs:dev
yarn run v1.21.1
$ vuepress dev docs
wait Extracting site metadata...
tip Apply theme @vuepress/theme-default ...
tip Apply plugin container (i.e. "vuepress-plugin-container") ...
tip Apply plugin @vuepress/register-components (i.e. "@vuepress/plugin-register-components") ...
tip Apply plugin @vuepress/active-header-links (i.e. "@vuepress/plugin-active-header-links") ...
tip Apply plugin @vuepress/search (i.e. "@vuepress/plugin-search") ...
tip Apply plugin @vuepress/nprogress (i.e. "@vuepress/plugin-nprogress") ...

✔ Client
  Compiled successfully in 5.38s

ℹ ｢wds｣: Project is running at http://0.0.0.0:8081/
ℹ ｢wds｣: webpack output is served from /
ℹ ｢wds｣: Content not from webpack is served from /root/myblog/docs/.vuepress/public
ℹ ｢wds｣: 404s will fallback to /index.html
success [13:20:13] Build 2e672e finished in 5384 ms! 
> VuePress dev server listening at http://localhost:8081/

✔ Client
  Compiled successfully in 161.01ms
success [13:20:14] Build 89b3ca finished in 162 ms! ( http://localhost:8081/ )
```

- 访问``http://hellogitlab.com:8081/``
此时可以在界面上面看到"Hello VuePress!"，说明一个基础的VuePress博客就配置好。

#### 生成静态文件

- 使用``yarn docs:build``命令生成静态文件。
- 默认情况下，文件将会被生成在 .vuepress/dist，当然，你也可以通过 .vuepress/config.js 中的 dest 字段来修改，生成的文件可以部署到任意的静态文件服务器上。

```sh
[root@hellogitlab myblog]# yarn docs:build
yarn run v1.21.1
$ vuepress build docs
wait Extracting site metadata...
tip Apply theme @vuepress/theme-default ...
tip Apply plugin container (i.e. "vuepress-plugin-container") ...
tip Apply plugin @vuepress/register-components (i.e. "@vuepress/plugin-register-components") ...
tip Apply plugin @vuepress/active-header-links (i.e. "@vuepress/plugin-active-header-links") ...
tip Apply plugin @vuepress/search (i.e. "@vuepress/plugin-search") ...
tip Apply plugin @vuepress/nprogress (i.e. "@vuepress/plugin-nprogress") ...

✔ Client
  Compiled successfully in 9.96s

✔ Server
  Compiled successfully in 6.09s

wait Rendering static HTML...
success Generated static files in docs/.vuepress/dist.

Done in 12.14s.
```

此时，生成了.vuepress目录。

- docs/.vuepress: 用于存放全局的配置、组件、静态资源等。
- docs/.vuepress/config.js: 配置文件的入口文件，也可以是 YML 或 toml。


#### 创建config.js
进入到.vuepress目录中，然后创建config.js，config.js是VuePress必要的配置文件，它导出y一个javascript对象。

```sh
[root@hellogitlab myblog]# cd docs/
[root@hellogitlab docs]# ls
README.md
[root@hellogitlab docs]# cd .vuepress/
[root@hellogitlab .vuepress]# ls
dist
[root@hellogitlab .vuepress]# touch config.js
[root@hellogitlab .vuepress]# ls
config.js  dist
[root@hellogitlab .vuepress]# vi config.js 
[root@hellogitlab .vuepress]# cat config.js 
module.exports = {
    title: 'Hello VuePress',
    description: 'Just playing around'
}
```

#### 创建public文件夹
进入到.vuepress目录中，然后创建public文件夹，此文件夹主要放静态资源文件，例如favicons和PWA的图标。

```sh
[root@hellogitlab .vuepress]# mkdir -p public/{img,css} 
[root@hellogitlab .vuepress]# ll
total 12
-rw-r--r-- 1 root root   89 Dec 29 16:21 config.js
drwxr-xr-x 3 root root 4096 Dec 29 13:23 dist
drwxr-xr-x 4 root root 4096 Dec 29 16:32 public
[root@hellogitlab .vuepress]# ls public/
css  img
```

img存放图片，css存放样式文件。此时，项目的结构差不多就出来了。

```sh
myblog
├─── docs
│   ├── README.md
│   └── .vuepress
│       ├── public
│       │   ├── img
│       │   └── css
│       └── config.js
└── package.json

```

以上只是简单了搭建了一下博客的开发环境，接下来是博客主要的基本配置config.js，也是必须要做的。


此时运行项目，打开"http://hellogitlab.com:8081/"查看到界面如下图所示:

![vuepress_set_title](/img/vuepress_set_title.png) 

## 基本配置
一个config.js的主要配置包括网站的标题、描述、主题、端口号的配置。这里简单的列举一下常用配置。

### 网站信息

我们对config.js进行一些修改，首先设置网站的标题和网站的描述信息。

```javascript
module.exports = {
    title: '个人主页', 
    description: '梅朝辉的博客',
    head: [
        ['link', { rel: 'icon', href: '/img/logo.ico' }],
    ]
}
```

+ title：网站标题
+ description：网站描述
+ head：额外的需要被注入到当前页面的HTML"head"中的标签，其中路径的"/"就是public资源目录。

具体配置详情请看文档：[配置](https://vuepress.vuejs.org/zh/config/#%E5%9F%BA%E6%9C%AC%E9%85%8D%E7%BD%AE)

### 端口号设置

VuePress默认的端口号是8080，我们先设置为80，后面等知道如何配置HTTPS协议后，再配置成443端口。

```javascript
module.exports = {
    title: '个人主页', 
    description: '梅朝辉的博客',
    head: [
        ['link', { rel: 'icon', href: '/img/logo.ico' }],
    ],
    port: 80
}
```

此时运行项目，打开"http://hellogitlab.com/"查看到界面如下图所示:

![vuepress_set_port](/img/vuepress_set_port.png)


### Markdown显示代码行号

```javascript
module.exports = {
    title: '个人主页', 
    description: '梅朝辉的博客',
    head: [
        ['link', { rel: 'icon', href: '/img/logo.ico' }],
    ],
    port: 80,
    markdown: {
        lineNumbers: true,  // 代码显示行号
    }, 
}
```


### 主题配置

#### 导航栏设置

导航栏设置配置``themeConfig.nav``属性。参考：https://vuepress.vuejs.org/zh/theme/default-theme-config.html#%E5%AF%BC%E8%88%AA%E6%A0%8F-logo
```javascript
module.exports = {
    themeConfig: {
        nav: [
            { text:'首页', link: '/'},
            {
                text: '博文',
                items: [
                    { text: 'Python', link: '/python/' },
                    { text: 'Golang', link: '/golang/' }
                    { text: 'Web', link: '/web/' }
                    
                ]
            }, 
            { text:'关于', link: '/about/'},
            { text: 'Github', link: 'https://www.github.com/meizhaohui' }
        ] 
    }
}
```

- 导航栏配置``nav``，此配置主要用于配置导航栏的链接，例如以上首页的link为"/"，默认是根目录(docs目录)下的README.md。
- "/python/"链接到根目录docs下的python文件夹下的README.md文件。
- "/golang/"链接到根目录docs下的golang文件夹下的README.md文件。
- "/web/"链接到根目录docs下的web文件夹下的README.md文件。
- "/about/"链接到根目录docs下的about文件夹下的README.md文件。

准备博文或关于页面的基础数据，在docs目录下面新建python,golang,web,about等文件夹，并在各文件夹下面创建README.md文件。

```sh
[root@hellogitlab docs]# mkdir -p ./{python,golang,web,about}
[root@hellogitlab docs]# echo "# Python Docs" > python/README.md
[root@hellogitlab docs]# echo "# Golang Docs" > golang/README.md
[root@hellogitlab docs]# echo "# web Docs" > web/README.md
[root@hellogitlab docs]# echo "# About Docs" > about/README.md
```

以上首先创建几个子文件夹，然后在各目录中创建README.md文件。


此时运行项目，打开"http://hellogitlab.com/"查看到界面如下图所示:

![vuepress_set_nav](/img/vuepress_set_nav.png)

在右上角出现了导航栏，可以看到多出了"首页"、"博文"、"关于"、"Github"等导航，我们点击"博文"，可以看到下拉框中显示了我们定义的"Python"、"Golang"、"Web"三个超链接。

![vuepress_set_nav_down_menu](/img/vuepress_set_nav_down_menu.png)

点击相应的超链接，可以打开各自的页面，如打开"Python"超链接，跳转到 http://hellogitlab.com/python/ 页面：

![vuepress_set_nav_python_docs](/img/vuepress_set_nav_python_docs.png)




#### 侧边栏设置

想要使侧边栏（Sidebar）生效，需要配置themeConfig.sidebar，基本的配置，需要一个包含了多个链接的数组。


侧边栏设置示例:

```sh
[root@hellogitlab docs]# cat .vuepress/config.js
module.exports = {
    title: '个人主页',
    description: '梅朝辉的博客',
    head: [
        ['link', { rel: 'icon', href: '/img/logo.ico' }],
    ],
    port: 80,
    markdown: {
        lineNumbers: true // 代码显示行号
    },
    themeConfig: {
        nav: [
            { text:'首页', link: '/'},
            {
                text: '博文',
                items: [
                    { text: 'Python', link: '/python/' },
                    { text: 'Golang', link: '/golang/' },
                    { text: 'Web', link: '/web/' }
                ]
            }, 
            { text:'关于', link: '/about/'},
            { text: 'Github', link: 'https://www.github.com/meizhaohui' }
        ],
        sidebar: {
            '/python/': [
                {
                    title: 'Python基础知识',
                    collapsable: false,  // 是否可折叠，默认可折叠true 
                    children: [
                        "python1",
                        "python2",
                        "python3"
                    ]
                },
                {
                    title: 'Python Web',
                    collapsable: false,
                    children: [
                        "python4",
                        "python5",
                        "python6"
                    ]
                },
            ],
            '/golang/': [
                "",
                "golang1",
                "golang2",
                "golang3"
            ],
            '/web/': [
                "",
                "web1"
            ],
        },
        sidebarDepth: 2, // 侧边栏显示深度，默认为1，即显示一级标题
    }
}
```

- ``sidebar``用于设置侧边栏，'/python/'、 '/golang/'、'/web/'与导航栏类似，分别指代docs根目录下的python,golang,web等文件夹。
- '/python/'定义下，通过在list中定义两个json数据进行侧边栏分组，将"python1"、"python2"、"python3"分到'Python基础知识'组中，将"python4"、"python5"、"python6"分到'Python Web'组中。
- ``collapsable: false``表示侧边栏是否可折叠，``false``为不可折叠，默认为``true``，表示可折叠，可参加golang或web侧边栏的效果。
- '/python/'、 '/golang/'、'/web/'的定义就组成了多个侧边栏，不同的博文子类的侧边栏显示不一样。
- 侧边栏``children``列表中定义的是Markdown文件对应的名称，如"python1"对应python文件夹下面python1.md文件，"python2"对应python文件夹下面python2.md文件，"golang1"对应golang文件夹下面golang1.md文件。
- ``sidebarDepth``嵌套的标题链接深度，默认的深度为1。

准备侧边栏的基础数据：
```sh
[root@hellogitlab docs]# echo "# python1" > python/python1.md
[root@hellogitlab docs]# echo "# python2" > python/python2.md
[root@hellogitlab docs]# echo "# python3" > python/python3.md
[root@hellogitlab docs]# echo "# python4" > python/python4.md
[root@hellogitlab docs]# echo "# python5" > python/python5.md
[root@hellogitlab docs]# echo "# python6" > python/python6.md
[root@hellogitlab docs]# echo -e "# Golang 1\n## 二级标题\n" > golang/golang1.md
[root@hellogitlab docs]# echo -e "# Golang 2\n## 二级标题\n" > golang/golang2.md
[root@hellogitlab docs]# echo -e "# Golang 3\n## 二级标题\n" > golang/golang3.md
[root@hellogitlab docs]# echo -e "# web 1\n ## head 2" > web/web1.md
```

运行项目：
```sh
[root@hellogitlab docs]# yarn docs:dev
yarn run v1.21.1
$ vuepress dev docs
wait Extracting site metadata...
tip Apply theme @vuepress/theme-default ...
tip Apply plugin container (i.e. "vuepress-plugin-container") ...
tip Apply plugin @vuepress/register-components (i.e. "@vuepress/plugin-register-components") ...
tip Apply plugin @vuepress/active-header-links (i.e. "@vuepress/plugin-active-header-links") ...
tip Apply plugin @vuepress/search (i.e. "@vuepress/plugin-search") ...
tip Apply plugin @vuepress/nprogress (i.e. "@vuepress/plugin-nprogress") ...

✔ Client
  Compiled successfully in 4.03s

ℹ ｢wds｣: Project is running at http://0.0.0.0:80/
ℹ ｢wds｣: webpack output is served from /
ℹ ｢wds｣: Content not from webpack is served from /root/myblog/docs/.vuepress/public
ℹ ｢wds｣: 404s will fallback to /index.html
success [23:49:32] Build 4f5a0c finished in 4033 ms! 
> VuePress dev server listening at http://localhost:80/

✔ Client
  Compiled successfully in 172.09ms
success [23:49:32] Build 5591e0 finished in 173 ms! ( http://localhost:80/ )
```

此时运行项目，打开"http://hellogitlab.com/python/"查看到界面如下图所示:

![vuepress_set_sidebar_python](/img/vuepress_set_sidebar_python.png)

可以看到Python相关的侧边栏正常显示出来了，并且进行了分组显示。


打开"http://hellogitlab.com/golang/"查看到界面如下图所示:

![vuepress_set_sidebar_golang](/img/vuepress_set_sidebar_golang.png)

可以看到Python相关的侧边栏正常显示出来了，并且进行了分组显示。


### 自定义页面

默认的主题提供了一个首页（Homepage）的布局(用于这个网站的主页)。想要使用它，需要在你的根级 README.md设置``home: true``，然后添加数据。

重新定义一下docs目录下的README.md文件：
```
[root@hellogitlab docs]# cat README.md 
---
home: true
heroImage: img/gitlab.jfif
actionText: 查看我的博文 →
actionLink: /python/
features:
- title: Hello Python
  details: 简单易学的Python编程语言
- title: Hello Golang
  details: Go 是互联网时代的C语言
- title: Hello Web
  details: 手把手教你学web页面
footer: MIT Licensed | Copyright © 2019-present Zhaohui Mei
---
```

重新打开网站首页，查看到的效果如下图所示：

![vuepress_set_self_home](/img/vuepress_set_self_home.png)

以上一个基本的博客系统就配置好了！

参考：

- [yarn安装指导](https://yarnpkg.com/en/docs/install#centos-stable)
- [VuePress从零开始搭建自己专属博客](https://segmentfault.com/a/1190000015237352?utm_source=tag-newest)
- [用Vuepress搭建博客?看这篇就完事了,轻松玩转Vuepress](https://segmentfault.com/a/1190000021096838)
- [VuePress中文网](http://caibaojian.com/vuepress/guide/)
- [基于vuepress的个人博客搭建完全教程](https://www.jianshu.com/p/2220dbacfde1)
- [姜帅杰的博客](https://www.jiangshuaijie.com/)
