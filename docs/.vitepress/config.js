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

    // 自定义深色模式开关标签
    // 该标签仅显示在移动视图中
    darkModeSwitchLabel: '外观',
    // 自定义返回顶部按钮的标签
    // 该标签仅显示在移动视图中
    returnToTopLabel: '返回顶部',

    // VitePress支持使用浏览器内置索引进行模糊全文搜索
    // 此处使用本地搜索
    search: {
      provider: 'local'
    },
    
    // 自定义上一个和下一个链接上方显示的文本
    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    }
  }
}