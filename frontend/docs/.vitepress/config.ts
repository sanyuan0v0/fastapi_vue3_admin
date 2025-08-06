import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: '/docs/dist',
  outDir: 'dist',
  lang: 'zh-CN',
  title: 'Fastapi Vue3 Admin',
  description: '现代、开源、全栈融合的中后台快速开发平台',
  head: [
    ['link', { rel: 'icon', href: '/favicon.png' }],
  ],
  locales: {
    root: { label: '简体中文' },
    en: { label: 'English' },
  },
  lastUpdated: true,
  cleanUrls: true,
  metaChunk: true,
  themeConfig: {
    logo: '/logo.jpg',
    siteTitle: 'Fastapi Vue3 Admin',
    nav: [
      { text: '首页', link: '/' },
      { text: '指南', link: '/guide' },
      { text: '演示环境', link: 'http://service.fastapiadmin.com', target: '_blank' },
      {
        text: '版本',
        items: [
          { text: 'master', link: 'https://github.com/1014TaoTao/fastapi_vue3_admin', target: '_blank' },
          { text: 'V2.0.0', link: 'https://github.com/1014TaoTao/fastapi_vue3_admin/tree/v2.0.0', target: '_blank' },
          { text: 'V1.0.0', link: 'https://github.com/1014TaoTao/fastapi_vue3_admin/tree/v1.0.0', target: '_blank' }
        ]
      },
      { text: '更新日志', link: 'https://github.com/1014TaoTao/fastapi_vue3_admin/commits/master/', target: '_blank' },
      {
        text: '社区',
        items: [
          { text: 'GitHub', link: 'https://github.com/1014TaoTao/fastapi_vue3_admin', target: '_blank' },
          { text: 'Gitee', link: 'https://gitee.com/tao__tao/fastapi_vue3_admin', target: '_blank' },
          { text: 'GitCode', link: 'https://gitcode.com/qq_36002987/fastapi_vue3_admin', target: '_blank' }
        ]
      },
      { text: '关于我们', link: '/about' },
    ],

    sidebar: [
      {
        text: '项目指南',
        items: [
          { text: '项目介绍', link: '/guide#📘项目介绍' },
          { text: '核心亮点', link: '/guide#✨核心亮点' },
          { text: '技术栈概览', link: '/guide#🛠️技术栈概览' },
          { text: '内置模块', link: '/guide#📌内置模块' },
          { text: 'Docker部署', link: '/guide#🍪演示环境' },
          {text: '安装和使用', link: '/guide#👷安装和使用' },
          {text: '模块展示', link: '/guide#🔧模块展示' },
          {text: '二开教程', link: '/guide#🚀二开教程' },
          {text: '特别鸣谢', link: '/guide#🙏特别鸣谢' },
          {text: '支持我', link: '/guide#❤️支持我' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/1014TaoTao/fastapi_vue3_admin' },
      { icon: 'gitee', link: 'https://gitee.com/tao__tao/fastapi_vue3_admin' },
      { icon: 'gitcode', link: 'https://gitcode.com/qq_36002987/fastapi_vue3_admin' }
    ],

    footer: {
      message: '<a href="https://github.com/1014TaoTao/fastapi_vue3_admin/blob/master/LICENSE" target="_blank">MIT License</a>',
      copyright: 'Copyright © 2025-2026 service.fastapiadmin.com 版权所有 |隐私 |条款 陕ICP备2025069493号-1'
    },

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '搜索文档',
                buttonAriaLabel: '搜索文档'
              },
              modal: {
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                  closeText: '关闭',
                },
              },
            },
          },
        },
      },
    },
    outline: 3,
  }
})
