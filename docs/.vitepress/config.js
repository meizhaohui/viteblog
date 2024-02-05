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