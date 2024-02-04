// https://vitepress.dev/reference/site-config
export default {
  // 打包输出目录
  outDir: '../dist',

  // 站点语言标题等
  lang: 'zh-CN',
  title: '编程技术分享',
  description: '种一棵树最好的时间是十年前，其次就是现在',

  lastUpdated: true,
  cleanUrls: true,

  /* markdown 配置 */
  markdown: {
    lineNumbers: true
  },

  /* 主题配置 */
  themeConfig: {
    i18nRouting: false,
    logo: '/favicon.ico',
    // https://vitepress.dev/reference/default-theme-config
    nav: [{
        text: 'Home',
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
      },
      {
        text: '后端',
        items: [{
            text: 'Python',
            link: '/backend/python/'
          },
          {
            text: 'Flask',
            link: '/backend/Flask/'
          },
          {
            text: 'Java',
            link: '/backend/Java/'
          },
          {
            text: 'Golang',
            link: '/backend/golang/'
          },
          {
            text: 'PHP',
            link: '/backend/php/'
          },
          {
            text: 'C',
            link: '/backend/C/'
          },
        ]
      },
      {
        text: '数据库',
        items: [{
            text: 'MYSQL',
            link: '/database/mysql/'
          },
          {
            text: 'MongoDB',
            link: '/database/mongodb/'
          },
          {
            text: 'Oracle',
            link: '/database/oracle/'
          },
          {
            text: 'Redis',
            link: '/database/redis/'
          }
        ]
      },
      {
        text: '监控',
        items: [{
            text: 'Supervisor',
            link: '/monitor/supervisor/'
          },
          {
            text: 'Zabbix',
            link: '/monitor/zabbix/'
          }
        ]
      },
      {
        text: '配置管理',
        items: [{
            text: 'Git',
            link: '/CM/git/'
          },
          {
            text: 'SVN',
            link: '/CM/svn/'
          },
          {
            text: 'Ansible',
            link: '/CM/ansible/'
          },
          {
            text: 'Proxmox',
            link: '/CM/proxmox/'
          }
        ]
      },
      {
        text: '持续集成',
        items: [{
            text: 'Jenkins',
            link: '/CI/jenkins/'
          },
          {
            text: 'Docker',
            link: '/CI/docker/'
          },
          {
            text: 'k8s',
            link: '/CI/k8s/'
          },
          {
            text: 'GitLab',
            link: '/CI/gitlab/'
          }
        ]
      },
      {
        text: '友链',
        link: '/friendlink/'
      },
      {
        text: '更多',
        items: [{
            text: '关于我',
            link: '/more/me/'
          },
          {
            text: '关于博客',
            link: '/more/blog/'
          },
          {
            text: '软考',
            link: '/more/softexam/'
          },
          {
            text: '游戏',
            link: '/more/game/'
          },
          {
            text: '好用的工具',
            link: '/more/tools/'
          }
        ]
      }
    ],

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

    socialLinks: [{
      icon: 'github',
      link: 'https://github.com/vuejs/vitepress'
    }],
    /* 右侧大纲配置 */
    outline: {
      level: 'deep',
      label: '本页目录'
    },

    footer: {
      message: '如有转载或 CV 的请标注本站原文地址',
      copyright: 'Copyright © 2019-present maomao'
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