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
  ],
  


  '/backend/': [
    {
      text: '后端',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Python docs', link: '/backend/python/' },
        { text: 'Flask docs', link: '/backend/Flask/' },
        { text: 'Java docs', link: '/backend/Java/' },
        { text: 'Golang docs', link: '/backend/golang/' }
      ]
    }
  ],
  '/database/': [
    {
      text: '后端',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'MySQL docs', link: '/database/mysql/' },
        { text: 'MongoDB docs', link: '/database/mongodb/' },
        { text: 'Oracle docs', link: '/database/oracle/' },
        { text: 'Redis docs', link: '/database/redis/' },
      ]
    }
  ],
}
