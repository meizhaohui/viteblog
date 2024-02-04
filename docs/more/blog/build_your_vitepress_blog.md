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

而官方文档是这么说的：



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

参考：

- 从 VuePress 迁移至 VitePress [https://github.com/maomao1996/daily-notes/issues/37](https://github.com/maomao1996/daily-notes/issues/37)
- 前端导航 [https://fe-nav.netlify.app/nav/](https://fe-nav.netlify.app/nav/)