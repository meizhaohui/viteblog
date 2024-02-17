# VitePress从零开始搭建自己的博客 基础配置

[[toc]]

## 0. 为什么要使用VitePress搭建博客

主要有以下两个原因：

- 随着我博客文章越来越多后，使用vuepress本地编译时非常慢，经常编译的时候会出现` JavaScript heap out of memory`异常，导致本地查看博客效果时，非常的折腾。
- 服务端端会定时检查博客是否有更新，有更新就会自动编译，但编译时也会出现` JavaScript heap out of memory`异常，博客就不能第一时间显示在网站上，需要我手动去重新执行脚本编译。

VitePress是什么？

参考: [vitePress快速搭建及部署一个博客](https://cloud.tencent.com/developer/article/1952177)

> **什么是 VitePress？**
>
> VitePress 是 VuePress 的小弟弟，但是vitepress是在 Vite 上构建的。
>
> **动机**
>
> 主要是因为太慢！但是不怪 VuePress，怪 Webpack！
>
> Vite 则非常好的解决了问题：
>
> 1.几乎实时的服务启动
>
> 2.根据需要编译页面
>
> 3.非常轻量快速的 HMR（热模块重载）
>
> 另外，本身 VuePress 一些设计问题一直没有时间去修复，正好这次做个大重构。
>
> **改进的地方**
>
> 1.利用了 Vue 3 的改进的模板静态分析来尽可能字符串化静态内容
>
> 2.静态内容以字符串模式而不是渲染函数代码发送，JS 负载更便宜，注水（SSR 时生成 js 交互逻辑代码）也更快
>
> 3.这些优化仍然允许在 markdown 中混合使用 Vue 组件，编译器会帮你处理静态/动态分离工作
>
> 4.使用了 Vite
>
> 5.更快的 dev [服务器](https://cloud.tencent.com/act/pro/promotion-cvm?from_column=20065&from=20065)启动
>
> 6.更快的热更新
>
> 7.更快的构建（使用 Rollup）
>
> **更轻量的页面**
>
> Vue 3  + Rollup 代码分离 不会把所有页面的元数据都在一个请求中发送出去。客户端导航时再一起获得新页面的组件及元数据
>
> **其他不同点**
>
> 1.VitePress 更武断且更少的配置。VitePress目标是缩减掉当前 VuePress 的复杂性并从其极简主义的根源重新开始
>
> 2.VitePress 是面向未来的：其目标浏览器是只支持原生 ES 模块导入的浏览器。其鼓励使用原始的 JavaScript 而不用转义以及使用 CSS 变量来主题化

而官方文档 [什么是VitePress？](https://vitepress.qzxdp.cn/guide/what-is-vitepress.html) 是这么说的：



> **开发者体验** 
>
> VitePress 旨在在处理 Markdown 内容时提供出色的开发者体验 (DX)。
>
> - **[基于 Vite 引擎:](https://vitejs.dev/)** VitePress实现了即时的服务器启动，对编辑的更改始终在瞬间反映出来（<100毫秒），无需重新加载页面。
> - **[内置Markdown扩展:](https://vitepress.qzxdp.cn/guide/markdown.html)** VitePress提供了许多高级功能，包括Frontmatter（前置元数据）、表格、语法高亮等等，几乎所有你能想到的功能它都有。特别是在处理代码块方面，VitePress提供了许多高级功能，使其非常适合编写高度技术性的文档。
> - **[增强型Vue Markdown:](https://vitepress.qzxdp.cn/guide/using-vue.html)** 由于Vue模板与HTML具有100%的语法兼容性，因此每个Markdown页面也是一个Vue单文件组件（Single-File Component）[SFC](https://vuejs.org/guide/scaling-up/sfc.html)。您可以使用Vue模板的特性或导入的Vue组件，在静态内容中嵌入交互性。这意味着您可以在Markdown页面中使用Vue模板的语法和功能来实现交互效果。
>
> **性能** 
>
> 与许多传统的SSG不同，VitePress生成的网站实际上是一个[单页应用程序](https://en.wikipedia.org/wiki/Single-page_application) (SPA)。
>
> - **快速初始加载**
>
>   对于任何页面的初始访问，将提供静态的预渲染HTML，以实现极快的加载速度和最佳的SEO效果。然后，页面会加载一个JavaScript捆绑包，将页面转换为Vue单页面应用程序（SPA）进行"水合"（hydration）过程。水合过程非常快速：在[PageSpeed Insights](https://pagespeed.web.dev/report?url=https%3A%2F%2Fvitepress.dev%2F)上，即使在低端移动设备上使用缓慢的网络，典型的VitePress站点也能获得接近完美的性能分数。
>
> - **快速加载后导航**
>
>   更重要的是，SPA模型在初始加载之后为用户提供了更好的用户体验。在站点内进行后续导航将不再导致完整的页面重新加载。相反，将获取并动态更新进入页面的内容。VitePress还会自动预取视口内链接的页面块。在大多数情况下，加载后的导航将感觉瞬间完成。
>
> - **无损交互性**
>
>   为了能够对静态Markdown中嵌入的动态Vue部分进行水合（hydration），每个Markdown页面都会被处理为一个Vue组件并编译为JavaScript。这听起来可能效率低下，但是Vue编译器足够智能，能够将静态部分和动态部分分离，从而将水合成本和负载大小都最小化。对于初始页面加载，静态部分会自动从JavaScript负载中删除，并在水合过程中跳过。

说起来高大上，我们实际体验一把。



## 1. 安装依赖

> **先决条件** 
>
> - [Node.js](https://nodejs.org/) 版本 18 或更高版本。
> - 用于通过命令行界面 (CLI) 访问 VitePress 的终端。
> - 具有 [Markdown](https://en.wikipedia.org/wiki/Markdown) 语法支持的文本编辑器。
> - 推荐使用 [VSCode](https://code.visualstudio.com/) 以及[官方 Vue 扩展](https://marketplace.visualstudio.com/items?itemName=Vue.volar)。

我直接去 [https://nodejs.org/en](https://nodejs.org/en) 这里面下载，可以看到当前`20.11.0`是长期支持版，下载后安装到`D:\ProgramFiles\nodejs`目录，并将目录加入到Path环境变量。

### 1.1 安装nodejs

打开终端，查看版本信息：

```sh
# 查看nodejs版本信息
$ node --version
v20.11.0

# 查看npm版本信息
$ npm --version
10.2.4

# 查看命令所在路径
$ where node npm
D:\ProgramFiles\nodejs\node.exe
D:\ProgramFiles\nodejs\npm
D:\ProgramFiles\nodejs\npm.cmd
```



### 1.2 安装pnpm包管理工具

可参考[https://pnpm.io/zh/installation](https://pnpm.io/zh/installation)

安装方法：

```sh
npm install -g pnpm
```

安装：

```sh
# 安装pnpm
$ npm install -g pnpm

added 1 package in 2s


# 查看pnpm版本信息
$ pnpm --version
8.15.1                                                                                   
```

在家目录下创建文件`.pnpmrc`，其内容如下：

```
auto-install-peers=true

registry=https://registry.npmmirror.com
```



### 1.3 安装vitepress和vue

安装依赖：

```sh
$ pnpm add -D vitepress vue
Progress: resolved 1, reused 0, downloaded 0, added 0
Progress: resolved 31, reused 0, downloaded 19, added 0
Progress: resolved 109, reused 0, downloaded 59, added 0
Packages: +81
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Progress: resolved 116, reused 0, downloaded 79, added 41
Progress: resolved 116, reused 0, downloaded 80, added 76
Progress: resolved 116, reused 0, downloaded 81, added 81, done
.../node_modules/vue-demi postinstall$ node -e "try{require('./scripts/postinstall.js')}catch(e){}"
.../node_modules/vue-demi postinstall: Done
.../esbuild@0.19.12/node_modules/esbuild postinstall$ node install.js
.../esbuild@0.19.12/node_modules/esbuild postinstall: Done

devDependencies:
+ vitepress 1.0.0-rc.41
+ vue 3.4.15

Done in 6.2s

$
```

可以看到安装成功。

查看安装的包的版本信息：

```sh
$ pnpm list
Legend: production dependency, optional only, dev only

devDependencies:
vitepress 1.0.0-rc.41
vue 3.4.15
                                                                                         
$
```

## 2. 创建博客项目

参考 [vitepress入门](https://vitepress.qzxdp.cn/guide/getting-started.html)

创建项目目录:

```sh
# 切换到E盘下的data目录下
$ cd E:\data

# 查看当前路径，/drives/e/ 就表示E盘                                                              
$ pwd
/drives/e/data

# 创建博客目录viteblog
$ mkdir viteblog

# 切换到博客目录
$ cd viteblog/

# 查看当前路径
$ pwd
/drives/e/data/viteblog
                                                                                         
$
```

运行设置向导命令：

```sh
pnpm dlx vitepress init
```

注意，此处不要直接在MobaXterm命令行执行，执行会报异常，需要在windows cmd窗口执行。

![](/img/Snipaste_2024-02-03_23-04-02.png)

在cmd窗口执行：

![](/img/Snipaste_2024-02-03_23-05-21.png)

按提示运行命令`pnpm run docs:dev`，发现报错：

![](/img/Snipaste_2024-02-03_23-07-56.png)



将家目录下的`node_modules\.bin`目录加到环境变量Path中，如我的是`C:\Users\mch\node_modules\.bin`。

加入后，再打开命令行窗口，执行命令`pnpm run docs:dev`，还是报错：

![](/img/Snipaste_2024-02-03_23-22-05.png)

大意是没有配置文件。

docs/.vitepress 目录下默认有一个`config.mts`文件，我们复制一份为`config.js`，并修改其内容为如下：

```js
// https://vitepress.dev/reference/site-config
export default {
  title: "viteblog",
  description: "test vitepress blog",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Examples', link: '/markdown-examples' }
    ],

    sidebar: [
      {
        text: 'Examples',
        items: [
          { text: 'Markdown Examples', link: '/markdown-examples' },
          { text: 'Runtime API Examples', link: '/api-examples' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
    ]
  }
}

```

再执行命令`pnpm run docs:dev`，没报错了：

```sh
E:\data\viteblog>pnpm run docs:dev

> @ docs:dev E:\data\viteblog
> vitepress dev docs

Failed to resolve dependency: vitepress > @vue/devtools-api, present in 'optimizeDeps.include'
Failed to resolve dependency: vitepress > @vueuse/core, present in 'optimizeDeps.include'

  vitepress v1.0.0-rc.41

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

![](/img/Snipaste_2024-02-03_23-24-43.png)

访问页面 [http://localhost:5173/](http://localhost:5173/) 

![](/img/Snipaste_2024-02-03_23-25-25.png)

可以看到，可以正常打开！说明初始化网站正常了！



## 3. 网站优化

### 3.1 修改博客运行端口号

默认情况下，执行命令`pnpm run docs:dev`后会监听5173端口来运行博客程序。为了我们在浏览器中直接输入`localhost`就能打开博客，我修改一下博客的配置文件`package.json`，在`vitepress dev docs`后面增加内容` --port=80`，然后查看配置文件信息：

```sh
$ cat package.json
{
  "scripts": {
    "docs:dev": "vitepress dev docs --port=80",
    "docs:build": "vitepress build docs",
    "docs:preview": "vitepress preview docs"
  }
}
$
```

此时，浏览器打开`localhost`，就可以直接打开博客了：

![](/img/Snipaste_2024-02-04_20-12-58.png)



### 3.2 优化导航栏

随着博客文章越来越多，导航栏越来越多时，将导航栏配置都放在`config.js`文件中，会使该文件变得非常大。我们应将其拆分出来单独放一个文件中，也方便后期新增其他的导航信息。



不拆分前，`config.js`中关于导航栏的配置如下：

```js
  /* 主题配置 */
  themeConfig: {
    i18nRouting: false,
    logo: '/favicon.ico',
    // https://vitepress.dev/reference/default-theme-config
    nav: [{
        text: '首页',
        link: '/'
      },
      {
        text: '操作系统',
        items: [{
            text: 'CentOS',
            link: '/OS/Centos/'
          },
          {
            text: 'Ubuntu',
            link: '/OS/Ubuntu/'
          },
          {
            text: 'MacOS',
            link: '/OS/MacOS/'
          },
          {
            text: 'Windows',
            link: '/OS/Windows/'
          },
          {
            text: 'Cobbler',
            link: '/OS/Cobbler/'
          },
          {
            text: 'Rocky Linux',
            link: '/OS/RockyLinux/'
          }
        ]
      },
      {
        text: '前端',
        items: [{
            text: 'Vue',
            link: '/frontend/vue/'
          }
        ]
      }
     ]
```

会非常的长，在`.vitepress/`目录下创建配置文件夹`configs`，并在`configs`目录下创建`navConfig.js`文件，其内容如下：

```js
module.exports = [{
        text: '首页',
        link: '/'
    },
    {
        text: '操作系统',
        items: [{
                text: 'CentOS',
                link: '/OS/Centos/'
            },
            {
                text: 'Ubuntu',
                link: '/OS/Ubuntu/'
            },
            {
                text: 'MacOS',
                link: '/OS/MacOS/'
            },
            {
                text: 'Windows',
                link: '/OS/Windows/'
            },
            {
                text: 'Cobbler',
                link: '/OS/Cobbler/'
            },
            {
                text: 'Rocky Linux',
                link: '/OS/RockyLinux/'
            }
        ]
    },
    {
        text: '前端',
        items: [{
                text: 'Vue',
                link: '/frontend/vue/'
            },
            {
                text: 'Javascript',
                link: '/frontend/js/'
            }
        ]
    }
]

```

然后，修改`config.js`配置文件：

```js
// 将导航栏单独拆分成一个配置文件
const navConf = require('./configs/navConfig.js');
// https://vitepress.dev/reference/site-config
export default {
  // 打包输出目录
  outDir: '../dist',

  // 站点语言标题等
  lang: 'zh-CN',
  title: '编程技术分享',
  description: '阿梅的IT成长之路，记录操作系统、前后端等学习总结文档',
  
  // 显示上次更新时间
  lastUpdated: true,
  // 为了和vuepress保持一致，不生成干净的URL
  cleanUrls: false,

  /* markdown 配置 */
  markdown: {
    // 开启markdown行数显示
    lineNumbers: true
  },

  /* 主题配置 */
  themeConfig: {
    i18nRouting: false,
    logo: '/favicon.ico',
    // https://vitepress.dev/reference/default-theme-config
    // 导航栏
    nav: navConf,
    // 侧边栏
    sidebar: [{
      text: 'Examples',
      items: [{
          text: 'Markdown Examples',
          link: '/markdown-examples'
        },
        {
          text: 'Runtime API Examples',
          link: '/api-examples'
        }
      ]
    }],
    // 社交链接
    socialLinks: [{
      icon: 'github',
      link: 'https://github.com/meizhaohui/'
    }],
    /* 右侧大纲配置 */
    outline: {
      level: 'deep',
      label: '本页目录'
    },

    footer: {
      message: '如有转载或 CV 的请标注本站原文地址',
      copyright: 'Copyright © 2019-2024 阿梅的博客'
    },

    darkModeSwitchLabel: '外观',
    returnToTopLabel: '返回顶部',
    lastUpdatedText: '上次更新',


    /* Algolia DocSearch 配置 */
    // algolia,

    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    }
  }
}
```



第2行的`const navConf = require('./configs/navConfig.js');` 是我新增的，而`nav: navConf,`则是删除原来写到`config.js`中的导航栏信息后的配置信息。



这样导航栏就拆分出来了，效果图：

![](/img/Snipaste_2024-02-04_21-11-12.png)





### 3.3 优化侧边栏

目前侧边栏还是模板里面自带的两个例子，不是我想要的结果。如将每个分类的目录都加到左侧的侧边栏。

在`.vitepress/configs`配置文件夹下，编写配置文件`configs/sidebarConfig.js`，我这里是一个示例：

```js
// 侧边栏
module.exports = {
  '/OS/': [
    {
      text: 'CentOS',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: '学会使用命令帮助', link: '/OS/Centos/X_use_help' },
        { text: 'VIM编辑器的使用', link: '/OS/Centos/X_how_to_use_vim' },
        { text: 'Bash script中的通配符与正则表达式', link: '/OS/Centos/X_wildcard_regular_expression_in_bash_script' }
      ]
    },
    {
      text: 'Ubuntu',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Ubuntu桌面初始化安装配置', link: '/OS/Ubuntu/ubuntu_init' },
        { text: '更改ubuntu国内镜像源', link: '/OS/Ubuntu/ubuntu_change_repo' },
        { text: 'Ubuntu防火墙设置', link: '/OS/Ubuntu/ubuntu_firewall' }
      ]
    },
    {
      text: 'Windows',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'windows批处理的使用', link: '/OS/Windows/cmd' }
      ]
    },
    {
      text: 'RockyLinux',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'RockyLinux docs', link: '/OS/RockyLinux/' }
      ]
    },
    {
      text: 'MacOS',
      link: '/OS/MacOS/'
    },
    {
      text: 'Cobbler自动化系统',
      link: '/OS/Cobbler/'
    }
  ],
  '/frontend/': [
    {
      text: 'Vue',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'vue的基本使用', link: '/frontend/vue/vue_basic_use' },
        { text: '模板语法', link: '/frontend/vue/syntax' },
        { text: '计算属性与侦听器', link: '/frontend/vue/computed_watch' },
        { text: 'Vue-Multiselect下拉框强化插件的使用', link: '/frontend/vue/use_Vue-Multiselect' },
        { text: '动态绑定class或style样式', link: '/frontend/vue/class_style' },
        { text: 'v-if与v-show条件渲染', link: '/frontend/vue/v-if_v_show' },
        { text: 'v-for循环列表', link: '/frontend/vue/v-for' },
        { text: '事件处理', link: '/frontend/vue/events' },
        { text: '表单输入绑定', link: '/frontend/vue/forms' },
        { text: '组件基础', link: '/frontend/vue/components' }
      ]
    },
    {
      text: 'JavaScript',
      link: '/frontend/js/'
    },
  ]
}
```

你可以根据个人需要再加别的。

config.js中再进行修改：

```js
// 将导航栏单独拆分成一个配置文件
const navConf = require('./configs/navConfig.js');
// 将侧边栏单独拆分成一个配置文件
const sidebarConf = require('./configs/sidebarConfig.js');

// https://vitepress.dev/reference/site-config
export default {
  // 打包输出目录
  outDir: '../dist',
  base: process.env.APP_BASE_PATH || '/',

  // 站点语言标题等
  lang: 'zh-CN',
  title: '编程技术分享',
  description: '阿梅的IT成长之路，记录操作系统、前后端等学习总结文档',
  
  // 显示上次更新时间
  lastUpdated: true,
  // 为了和vuepress保持一致，不生成干净的URL
  cleanUrls: false,

  /* markdown 配置 */
  markdown: {
    // 开启markdown行数显示
    lineNumbers: true
  },

  /* 主题配置 */
  themeConfig: {
    i18nRouting: false,
    logo: '/favicon.ico',
    // https://vitepress.dev/reference/default-theme-config
    // 导航栏
    nav: navConf,
    // 侧边栏
    sidebar: sidebarConf,
    // 社交链接
    socialLinks: [{
      icon: 'github',
      link: 'https://github.com/meizhaohui/'
    }],
    /* 右侧大纲配置 */
    outline: {
      level: 'deep',
      label: '本页目录'
    },

    footer: {
      message: '如有转载或 CV 的请标注本站原文地址',
      copyright: 'Copyright © 2019-2024 阿梅的博客'
    },

    darkModeSwitchLabel: '外观',
    returnToTopLabel: '返回顶部',
    lastUpdatedText: '上次更新',


    /* Algolia DocSearch 配置 */
    // algolia,

    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    }
  }
}
```

这样就可以正常显示侧边栏了。

![](/img/Snipaste_2024-02-04_23-29-09.png)

博客有模有样了！

### 3.4 设置徽标<Badge type="info" text="default" />

参考 [https://vitepress.qzxdp.cn/reference/default-theme-badge.html](https://vitepress.qzxdp.cn/reference/default-theme-badge.html) 。

 您可以使用全局可用的`Badge`组件。 

```html
### Title <Badge type="info" text="default" />
### Title <Badge type="tip" text="^1.9.0" />
### Title <Badge type="warning" text="beta" />
### Title <Badge type="danger" text="caution" />
```

效果图：

![Snipaste_2024-02-07_22-17-37.png](/img/Snipaste_2024-02-07_22-17-37.png)

### 3.5 优化搜索功能

参考：

- vitepress 本地搜索 [https://vitepress.qzxdp.cn/reference/default-theme-search.html](https://vitepress.qzxdp.cn/reference/default-theme-search.html)
- vitepress 搜索插件 [https://www.npmjs.com/package/vitepress-plugin-pagefind](https://www.npmjs.com/package/vitepress-plugin-pagefind)

安装插件：

```
pnpm add -D vitepress-plugin-pagefind pagefind
```

```sh
# 查看当前工作路径
$ pwd
/drives/e/data/viteblog

# 安装插件
$ pnpm add -D vitepress-plugin-pagefind pagefind
Progress: resolved 0, reused 1, downloaded 0, added 0
Progress: resolved 67, reused 23, downloaded 25, added 0
Packages: +40
++++++++++++++++++++++++++++++++++++++++
Progress: resolved 161, reused 82, downloaded 39, added 12
Progress: resolved 161, reused 82, downloaded 39, added 39
Progress: resolved 161, reused 82, downloaded 40, added 39
Progress: resolved 161, reused 82, downloaded 40, added 40, done

devDependencies:
+ pagefind 1.0.4
+ vitepress-plugin-pagefind 0.2.11

Done in 7.3s
$
```

然后，在`.vitepress/config.js`增加插件相关内容：

![Snipaste_2024-02-08_22-43-21.png](/img/Snipaste_2024-02-08_22-43-21.png)

以上两个位置是新增的。



修改后的配置如下：

```js
/* 自动侧边栏 https://github.com/w3ctech-editorial-department/vitepress-auto-configure-nav-sidebar
import AutoConfigureNavSidebarPlugin from '@w3ctech-editorial-department/vitepress-auto-configure-nav-sidebar'
const { sidebar } = AutoConfigureNavSidebarPlugin({
  collapsed: true,
  isCollapse: true,
  showNavIcon: false,
  singleLayerNav: false,
  showSidebarIcon: true,
  ignoreFolders: ['.vuepress'],
  customIndexFileName: "目录",
})
*/

// 导入本地搜索插件 https://www.npmjs.com/package/vitepress-plugin-pagefind
import { chineseSearchOptimize, pagefindPlugin } from 'vitepress-plugin-pagefind'

// 将导航栏单独拆分成一个配置文件
const navConf = require('./configs/navConfig.js');
// 将侧边栏单独拆分成一个配置文件
const sidebarConf = require('./configs/sidebarConfig.js');

// https://vitepress.dev/reference/site-config
export default {
  // 打包输出目录
  outDir: '../dist',
  // 站点语言标题等
  lang: 'zh-CN',
  // 搜索功能优化
  // 注意，不要将vite属性放到themeConfig主题配置里面去了，会导致搜索插件不起作用
  vite: {
    plugins: [pagefindPlugin({
      customSearchQuery: chineseSearchOptimize,
      btnPlaceholder: '搜索',
      placeholder: '搜索文档',
      emptyText: '空空如也',
      heading: '共: {{searchResult}} 条结果',
      // 搜索结果不展示最后修改日期日期
      showDate: false,
    })],
  },
  // tab标签页上面显示的标题
  title: '编程技术分享',
  description: '阿梅的IT成长之路，记录操作系统、前后端等学习总结文档',
  
  // 为了和vuepress保持一致，不生成干净的URL
  cleanUrls: false,

  /* markdown 配置 */
  markdown: {
    // 开启markdown行数显示
    lineNumbers: true
  },

  /* 主题配置 */
  themeConfig: {
    // 是否将语言环境更改zh
    i18nRouting: false,
    // 显示在导航栏中网站标题之前的logo文件
    logo: '/favicon.ico',
    // 站点标题
    siteTitle: '编程技术分享',
    // https://vitepress.dev/reference/default-theme-config
    // 导航栏，导航菜单项的配置
    nav: navConf,
    // 侧边栏，侧边栏菜单项的配置
    sidebar: sidebarConf,
    // 右侧大纲配置，在大纲中显示的标题级别/
    outline: {
      level: 'deep',
      label: '当前页导航'
    },
    // 社交帐户链接
    socialLinks: [{
      icon: 'github',
      link: 'https://github.com/meizhaohui/'
    }],
    // 页脚配置
    // 当 SideBar 可见时，页脚将不会显示
    footer: {
      message: '本首页参考 https://notes.fe-mm.com/ 配置而成',
      copyright: 'Copyright © 2019-2024 阿梅的博客'
    },

    // 显示上次更新时间
    lastUpdated: true,
    lastUpdatedText: '上次更新',
    // 显示编辑链接
    editLink: {
        // 注意，把"/edit"字符前的地址换成你的github仓库地址
        pattern: 'https://github.com/meizhaohui/viteblog/edit/main/docs/:path',
        // 编辑链接显示的文本内容
        text: "在 GitHub 上编辑此页"
    },

    // 自定义深色模式开关标签
    // 该标签仅显示在移动视图中
    darkModeSwitchLabel: '外观',
    // 自定义返回顶部按钮的标签
    // 该标签仅显示在移动视图中
    returnToTopLabel: '返回顶部',

    // VitePress支持使用浏览器内置索引进行模糊全文搜索
    // 此处使用本地搜索
    // 你也可以配置algolia搜索
    // 需要去官网 https://docsearch.algolia.com/apply 申请key
    // 做相应的修改即可
    // search: {
    //   provider: 'algolia',
    //   options: {
    //     appId: '...',
    //     apiKey: '...',
    //     indexName: '...'
    // },
    search: {
      provider: 'local',
      text: '搜索',
    },
    
    // 自定义上一个和下一个链接上方显示的文本
    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    }
  }
}

```



搜索效果：

优化前：

![Snipaste_2024-02-08_22-25-29.png](/img/Snipaste_2024-02-08_22-25-29.png)

优化后：

![Snipaste_2024-02-08_22-38-52.png](/img/Snipaste_2024-02-08_22-38-52.png)

搜索结果中，最下方显示还是英文的，因为`vitepress-plugin-pagefind`插件里面源码`Search.vue`中使用的是硬编码，我们直接修改一下本地`Search.vue`文件：

![Snipaste_2024-02-16_22-39-52.png](/img/Snipaste_2024-02-16_22-39-52.png)

对应路径是 `node_modules/vitepress-plugin-pagefind/src/Search.vue`。

修改后，再次进行搜索，搜索结果底部已经正常显示中文了：

![Snipaste_2024-02-16_22-41-50.png](/img/Snipaste_2024-02-16_22-41-50.png)

### 3.6 图片单击放大

vitepress 实现，单击图片时图片放大，再次单击图像时图片缩小的功能。

详细可参考：Allow images to be zoomed in on click [https://github.com/vuejs/vitepress/issues/854](https://github.com/vuejs/vitepress/issues/854)

安装插件：

```sh
pnpm add -D medium-zoom
```



安装过程：

```sh
# 查看当前工作路径
$ pwd
/drives/e/data/viteblog

# 安装插件
$ pnpm add -D medium-zoom
Progress: resolved 0, reused 1, downloaded 0, added 0

   ╭──────────────────────────────────────────────────────────────────╮
   │                                                                  │
   │                Update available! 8.15.1 → 8.15.3.                │
   │   Changelog: https://github.com/pnpm/pnpm/releases/tag/v8.15.3   │
   │                Run "pnpm add -g pnpm" to update.                 │
   │                                                                  │
   │      Follow @pnpmjs for updates: https://twitter.com/pnpmjs      │
   │                                                                  │
   ╰──────────────────────────────────────────────────────────────────╯

Progress: resolved 75, reused 69, downloaded 2, added 0
Packages: +1
+
Progress: resolved 162, reused 121, downloaded 2, added 1, done

devDependencies:
+ medium-zoom 1.1.0

Done in 2.3s
$
```

 然后，在`.vitepress/theme/index.js`增加插件相关内容 ：

```js
import DefaultTheme from "vitepress/theme";
import { onMounted, watch, nextTick } from 'vue';
import { useRoute } from 'vitepress';
import mediumZoom from 'medium-zoom';
import "./custom.css";

export default {
  ...DefaultTheme,
  NotFound: () => "404", // <- this is a Vue 3 functional component
  enhanceApp({ app, router, siteData }) {
    // app is the Vue 3 app instance from createApp()
    // router is VitePress' custom router (see `lib/app/router.js`)
    // siteData is a ref of current site-level metadata.
  },
  setup() {
    const route = useRoute();
    const initZoom = () => {
      // mediumZoom('[data-zoomable]', { background: 'var(--vp-c-bg)' }); 
      mediumZoom('.main img', { background: 'var(--vp-c-bg)' });
    };
    onMounted(() => {
      initZoom();
    });
    watch(
      () => route.path,
      () => nextTick(() => initZoom())
    );
  },
};

```



修改后，内容如下：

![Snipaste_2024-02-16_23-20-23.png](/img/Snipaste_2024-02-16_23-20-23.png)

红线框出的是新增的。

然后在自定义样式`.vitepress/theme/custom.css`中增加以下内容：

```css
/**
  * Component: image zoom
  * -------------------------------------------------------------------------- */

.medium-zoom-overlay {
  z-index: 20;
}

.medium-zoom-image {
  z-index: 21;
}

```

重新运行项目就可以看到图片放大效果了！！



以上配置还是有点问题，当图片左侧存在侧边栏时，点击图片时会出现图片左半边不能正常显示的问题，

参考：

在自定义样式`.vitepress/theme/custom.css`中增加以下内容：

```js
/**
  * Component: image zoom
  * -------------------------------------------------------------------------- */

:root {
  --medium-zoom-z-index: 100;
  --medium-zoom-c-bg: var(--vp-c-bg);
}

.medium-zoom-overlay {
  /* override element style set by medium-zoom script */
  z-index: var(--medium-zoom-z-index);
  background-color: var(--medium-zoom-c-bg) !important;
}

.medium-zoom-overlay ~ img {
  z-index: calc(var(--medium-zoom-z-index) + 1);
}

```

此时，再重新运行项目，就不会出现图片被遮住的问题。



### 3.7 优化上次更新显示

参考：[https://vitepress.dev/reference/default-theme-config#lastupdated](https://vitepress.dev/reference/default-theme-config#lastupdated)

![Snipaste_2024-02-17_17-29-40.png](/img/Snipaste_2024-02-17_17-29-40.png)

```js
export default {
  themeConfig: {
    lastUpdated: {
      text: 'Updated at',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'medium'
      }
    }
  }
}
```

像官方示例一样，增加`formatOptions`参数，根据个人喜好可以调整`dataStyle`和`timeStyle`参数的值。





## 4. 页面异常处理

### 4.1 Error parsing JavaScript expression: Unterminated string constant

有时打开页面，提示一些莫名其妙的异常。

![Snipaste_2024-02-07_20-05-03.png](/img/Snipaste_2024-02-07_20-05-03.png)

此时我们可以在vscode中安装markdownlint插件，然后使用vscode打开对应的markdown文件，然后查看有哪些异常的位置需要修复：

![Snipaste_2024-02-07_20-12-04.png](/img/Snipaste_2024-02-07_20-12-04.png)

按每行提示进行修改，直到页面正常为止。

最后发现是约44行表格中左双大括号有问题，<code v-pre>"{{"</code> 外面需要使用`<code v-pre>` `</code>`来转义：

![Snipaste_2024-02-07_20-24-46.png](/img/Snipaste_2024-02-07_20-24-46.png)

### 4.2 打包异常Found dead link

使用`pnpm docs:build`打包项目时，可能会出现`Found dead link`异常，导致打包失败：

![Snipaste_2024-02-17_12-46-39.png](/img/Snipaste_2024-02-17_12-46-39.png)

可以参考 [https://vitepress.dev/reference/site-config#ignoredeadlinks](https://vitepress.dev/reference/site-config#ignoredeadlinks) 设置忽略死链接，但最好我们能够检查一下这些死链接到底是因为什么原因导致的，并修复这些死链接。

### 4.3 打包异常vitepress data not properly injected in app

使用`pnpm docs:build`打包项目时，可能会出现`vitepress data not properly injected in app`异常，导致打包失败：

![Snipaste_2024-02-17_16-40-20.png](/img/Snipaste_2024-02-17_16-40-20.png)

参考：[https://github.com/vuejs/vitepress/issues/2287](https://github.com/vuejs/vitepress/issues/2287)

![Snipaste_2024-02-17_16-42-18.png](/img/Snipaste_2024-02-17_16-42-18.png)

为了避免示例文件导致本地搜索异常，将docs目录下的`api-examples.md`和`markdown-examples.md`两个文件删除掉。



### 4.4 打包异常Some chunks are larger than 500 kB after minification

使用`pnpm docs:build`打包项目时，可能会出现`Some chunks are larger than 500 kB after minification`异常，导致打包失败：

![Snipaste_2024-02-17_13-12-57.png](/img/Snipaste_2024-02-17_13-12-57.png)



### 4.5 打包异常terser not found. Since Vite v3, terser has become an optional dependency

上一节修改打包配置时，又提示异常`[vite:terser] terser not found. Since Vite v3, terser has become an optional dependency. You need to install it.`。

需要手动安装该插件：

```sh
# 查看当前路径
$ pwd
/drives/e/data/viteblog

# 安装terser
$ pnpm add -D terser
Progress: resolved 0, reused 1, downloaded 0, added 0
Progress: resolved 111, reused 95, downloaded 11, added 0
Packages: +13 -3
+++++++++++++---
Progress: resolved 173, reused 123, downloaded 11, added 13, done

devDependencies:
- busuanzi.pure.js 1.0.3
+ terser 5.27.1

Done in 1.9s
$
```

### 4.6 打包异常Pagefind wasn't able to build an index

当使用`vitepress-plugin-pagefind`插件优化本地搜索时，使用`pnpm docs:build`打包项目时，可能会出现`Pagefind wasn't able to build an index`异常，导致打包失败：

![Snipaste_2024-02-17_17-58-24.png](/img/Snipaste_2024-02-17_17-58-24.png)

出现异常的原因是插件默认使用`npx pagefind --site docs\.vitepress\dist --exclude-selectors "div.aside, a.header-anchor"`命令去查找index文件，由于我们打包后生成的文件是在`docs`目录同级的`dist`目录，所以上面命令会报错。

而我们手动运行命令`npx pagefind --verbose --source dist`,则可以正常执行：

```sh
$ pwd
/drives/e/data/viteblog

$ npx pagefind --verbose --source dist
pagefind npm wrapper: Running the executable at E:\data\viteblog\node_modules\.pnpm\@pagefind+windows-x64@1.0.4\node_modules\@pagefind\windows-x64\bin\pagefind_extended.exe

Running Pagefind v1.0.4 (Extended)
Running in verbose mode
Running from: "E:\\data\\viteblog"
Source:       "dist"
Output:       "dist\\pagefind"

[Walking source directory]
Found 237 files matching **/*.{html}

[Parsing files]
Found a data-pagefind-body element on the site.
↳ Ignoring pages without this tag.
1 page found without an <html> element.
Pages without an outer <html> element will not be processed by default.
If adding this element is not possible, use the root selector config to target a different root element.
  * "/scripts/python/use_bottle2_" has no <html> element

[Reading languages]
Discovered 1 language: zh-cn
  * zh-cn: 234 pages

[Building search indexes]
Language zh-cn:
  Indexed 234 pages
  Indexed 42788 words
  Indexed 0 filters
  Indexed 0 sorts

Total:
  Indexed 1 language
  Indexed 234 pages
  Indexed 42788 words
  Indexed 0 filters
  Indexed 0 sorts
Note: Pagefind doesn't support stemming for the language zh-cn.
Search will still work, but will not match across root words.
Note: Pagefind doesn't support stemming for the language zh-cn.
Search will still work, but will not match across root words.

Finished in 5.693 seconds
1 configuration warning(s):

The `source` option is deprecated as of Pagefind 1.0. The `source` option has been renamed to `site`:

cli:    --site
config: site
env:    PAGEFIND_SITE
└─ "The location of your built static website"

pagefind npm wrapper: Process exited with status 0
$ 
```

修改`.vitepress/config.js`配置文件,增加以下两行：

```js
      // 修复打包时Pagefind wasn't able to build an index异常
      indexingCommand: 'npx pagefind --source "./dist" --bundle-dir "pagefind" --exclude-selectors "div.aside, a.header-anchor"',
```

![Snipaste_2024-02-17_18-20-23.png](/img/Snipaste_2024-02-17_18-20-23.png)

然后再次执行打包命令：

![Snipaste_2024-02-17_18-22-58.png](/img/Snipaste_2024-02-17_18-22-58.png)

可以看到，提示打包成功，但有警告。

即：

> 2 configuration warning(s):
>
> The `bundle-dir` option is deprecated as of Pagefind 1.0. Use either `output-subdir` or `output-path` instead:
>
> cli:    --output-subdir
> config: output_subdir
> env:    PAGEFIND_OUTPUT_SUBDIR
> └─ "Where to output the search files, relative to the processed site"
>
> cli:    --output-path
> config: output_path
> env:    PAGEFIND_OUTPUT_PATH
> └─ "Where to output the search files, relative to the working directory of the command"
>
>
> The `source` option is deprecated as of Pagefind 1.0. The `source` option has been renamed to `site`:
>
> cli:    --site
> config: site
> env:    PAGEFIND_SITE
> └─ "The location of your built static website"

也就是说，我们定义的`indexingCommand: 'npx pagefind --source "./dist" --bundle-dir "pagefind" --exclude-selectors "div.aside, a.header-anchor"'`中有两个选项在Pagefind 1.0版本中废弃了，建议用 `output-subdir` 或 `output-path` 代替`bundle-dir`选项；使用`site`代替`source`选项。或者使用环境变量。

修改配置文件：

```js
      // 修复打包时Pagefind wasn't able to build an index异常
      // indexingCommand: 'npx pagefind --source "./dist" --bundle-dir "pagefind" --exclude-selectors "div.aside, a.header-anchor"',
      indexingCommand: 'npx pagefind --site "./dist" --output-path "pagefind" --exclude-selectors "div.aside, a.header-anchor"',
```

![Snipaste_2024-02-17_18-31-12.png](/img/Snipaste_2024-02-17_18-31-12.png)

再次构建项目，可以看到构建成功，没有报异常：

![Snipaste_2024-02-17_18-40-07.png](/img/Snipaste_2024-02-17_18-40-07.png)





参考：

- 什么是VitePress？[https://vitepress.qzxdp.cn/guide/what-is-vitepress.html](https://vitepress.qzxdp.cn/guide/what-is-vitepress.html) 
- 茂茂物语: 各种笔记记录 [https://github.com/maomao1996/mm-notes](https://github.com/maomao1996/mm-notes)
- 茂茂物语 Mao Mao 的成长之路 [https://notes.fe-mm.com/](https://notes.fe-mm.com/)
- 从 VuePress 迁移至 VitePress [https://github.com/maomao1996/daily-notes/issues/37](https://github.com/maomao1996/daily-notes/issues/37)
- 前端导航 [https://fe-nav.netlify.app/nav/](https://fe-nav.netlify.app/nav/)
- [从零用VitePress搭建博客教程(4) – 如何自定义首页布局和主题样式修改？](https://www.cnblogs.com/myboogle/p/17776406.html)
- 粥里有勺糖 [https://theme.sugarat.top/](https://theme.sugarat.top/)
- Allow images to be zoomed in on click [https://github.com/vuejs/vitepress/issues/854](https://github.com/vuejs/vitepress/issues/854)
