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
    /* 临时关闭pagefindPlugin */
    plugins: [pagefindPlugin({
      customSearchQuery: chineseSearchOptimize,
      btnPlaceholder: '搜索',
      placeholder: '搜索文档',
      emptyText: '空空如也',
      heading: '共: {{searchResult}} 条结果',
      // 搜索结果不展示最后修改日期日期
      showDate: false,
    })],
    
    // 修复打包异常
    build:{
      sourcemap: false,
      minify: 'terser',
      chunkSizeWarningLimit: 3500,
      emptyOutDir: true,
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true
        }
      },
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules')) {
              return id.toString().split('node_modules/')[1].split('/')[0].toString();
            }
          },
          chunkFileNames: (chunkInfo) => {
            const facadeModuleId = chunkInfo.facadeModuleId ? chunkInfo.facadeModuleId.split('/') : [];
            const fileName = facadeModuleId[facadeModuleId.length - 2] || '[name]';
            return `js/${fileName}/[name].[hash].js`;
          }
        }
      }
    },
  },
  // tab标签页上面显示的标题
  title: '编程技术分享',
  description: '阿梅的IT成长之路，记录操作系统、前后端等学习总结文档',
  
  // 生成干净的URL，避免下载本地文件时在URL后面增加.html后缀
  cleanUrls: true,
  // 忽略指定死链接，避免编译打包失败
  ignoreDeadLinks: [
    // ignore all localhost links
    /^http?:\/\/localhost/,
    // ignore all links include "/scripts/""
    /\/scripts\//,
    // ignore all links include "/resource/""
    /\/resource\//,
    // custom function, ignore all links include "ignore"
    (url) => {
      return url.toLowerCase().includes('ignore')
    }
  ],
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
       copyright: 'Copyright © 2019-2024 阿梅的博客 <a href="https://beian.miit.gov.cn" target="_blank" rel="noopener noreferrer">京ICP备19051502号</a>'
     },

    // 显示上次更新时间
    // 优化上次更新时间显示
    // lastUpdated: true,
    lastUpdated: {
      formatOptions: {
        dateStyle: 'medium',
        timeStyle: 'medium'
      }
    },
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