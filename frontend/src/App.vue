<template>
  <ConfigProvider
    :locale="zhCN"
    :theme="{
      algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
    }"
  >
    <div id="app">
      <router-view />
    </div>
  </ConfigProvider>
</template>

<script lang="ts" setup>
import { ConfigProvider, theme } from 'ant-design-vue'
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import { ref, provide } from 'vue'
import { useRouter } from 'vue-router'

dayjs.locale('zh-cn')

// 主题状态
const isDarkMode = ref(localStorage.getItem('theme') === 'dark')

// 提供主题状态和切换方法给所有子组件
provide('isDarkMode', isDarkMode)

// 全局切换主题方法
const toggleTheme = (darkMode: boolean) => {
  isDarkMode.value = darkMode
  if (darkMode) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

provide('toggleTheme', toggleTheme)

// 初始化主题
if (isDarkMode.value) {
  document.documentElement.classList.add('dark')
}

// 禁用Promise reject输出控制台
window.addEventListener('unhandledrejection', function browserRejectionHandler(event) {
  event && event.preventDefault()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

body,
html {
  margin: 0;
  width: 100%;
  height: 100vh;
}

.ant-page-header {
  padding: 20px 0;
}

.ant-table-thead > tr > th {
  padding: 12px 8px !important;
}

.ant-table-wrapper .ant-table-tbody > tr > td {
  padding: 12px 8px;
}

.ant-modal .ant-modal-header {
  margin-bottom: 20px;
}
</style>
