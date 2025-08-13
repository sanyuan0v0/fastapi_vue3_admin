# uni-mini-router 在UniApp中的整合教程

## 一、uni-mini-router简介

uni-mini-router是一个轻量级的路由管理库，专为uni-app设计，解决了uni-app原生路由系统中没有路由拦截等关键功能的问题。它提供了类似Vue Router的API体验，使得在uni-app项目中实现更加灵活和强大的路由管理成为可能。

### 主要特点

1. **Vue Router风格API**：提供与Vue Router相似的API，降低学习成本
2. **路由拦截功能**：支持全局导航守卫，可以在路由跳转前后执行逻辑
3. **优雅的参数传递**：支持params和query方式传参
4. **命名路由**：支持通过路由名称进行导航
5. **类型支持**：完整的TypeScript类型定义
6. **轻量级**：体积小，性能高效

## 二、安装与基本配置

### 1. 安装uni-mini-router

使用npm或yarn安装uni-mini-router：

```bash
pnpm add - uni-mini-router
```

### 2. 初始化路由

在项目中创建router目录并初始化路由配置：

```typescript
// src/router/index.ts
import { createRouter } from 'uni-mini-router'
import { pages, subPackages } from 'virtual:uni-pages'

// 生成路由配置
function generateRoutes() {
  const routes = pages.map((page) => {
    const newPath = `/${page.path}`
    return { ...page, path: newPath }
  })

  // 处理分包路由
  if (subPackages && subPackages.length > 0) {
    subPackages.forEach((subPackage) => {
      const subRoutes = subPackage.pages.map((page: any) => {
        const newPath = `/${subPackage.root}/${page.path}`
        return { ...page, path: newPath }
      })
      routes.push(...subRoutes)
    })
  }

  return routes
}

// 创建路由实例
const router = createRouter({
  routes: generateRoutes(),
})

export default router
```

### 3. 在main.ts中挂载路由

```typescript
// src/main.ts
import { createSSRApp } from 'vue'
import App from './App.vue'
import router from './router'

export function createApp() {
  const app = createSSRApp(App)

  // 使用路由
  app.use(router)

  return {
    app
  }
}
```

### 4. 配置自动导入（可选，推荐）

使用unplugin-auto-import插件可以自动导入路由相关hooks，无需每次手动导入：

```typescript
// vite.config.ts
import AutoImport from 'unplugin-auto-import/vite'

export default defineConfig({
  plugins: [
    AutoImport({
      imports: [
        'vue',
        {
          from: 'uni-mini-router',
          imports: ['createRouter', 'useRouter', 'useRoute']
        }
      ],
      dts: 'src/auto-imports.d.ts'
    })
  ]
})
```

## 三、路由基本用法

### 1. 编程式导航

uni-mini-router提供了多种导航方法：

```typescript
const router = useRouter()

// 字符串路径导航
router.push('/pages/index/index')

// 对象导航(通过路径)
router.push({ path: '/pages/index/index' })

// 对象导航(通过名称)
router.push({ name: 'index' })

// 携带参数
router.push({
  path: '/pages/detail/index',
  query: { id: 10 }
})

// 通过名称 + 参数
router.push({
  name: 'detail',
  params: { id: 10 }
})

// Tab页面导航
router.pushTab('/pages/home/index')

// 关闭当前页面并跳转
router.replace('/pages/index/index')

// 关闭所有页面并跳转
router.replaceAll('/pages/index/index')

// 返回上一级
router.back()

// 返回多级
router.back(2)
```

### 2. 获取和使用路由信息

```typescript
const route = useRoute()

// 访问当前路由信息
console.log(route.path) // 当前路由路径
console.log(route.name) // 当前路由名称
console.log(route.query) // 查询参数
console.log(route.params) // 路由参数
```

### 3. 接收页面参数

在页面组件中接收传递的参数：

```typescript
<script setup lang="ts">
const route = useRoute()
const router = useRouter()

// 方法1: 直接从route对象获取
const id = route.query.id || route.params.id

// 方法2: 通过onLoad生命周期获取
onLoad((option) => {
  console.log('页面参数:', option)
  // option中包含所有传递的参数
})
</script>
```

> ⚠️ **重要说明**：在uni-mini-router中，params和query参数都会转换为查询字符串放在URL中，两者在实际效果上没有区别。这种设计是为了与Vue Router保持API一致性。

## 四、导航守卫

uni-mini-router提供了全局导航守卫功能，可以在路由跳转前后执行自定义逻辑。

### 1. 全局前置守卫

```typescript
// src/router/index.ts
router.beforeEach((to, from, next) => {
  console.log('路由跳转:', from.path, '->', to.path)

  // 检查是否需要登录
  if (to.meta && to.meta.requireAuth) {
    // 检查登录状态
    const isLoggedIn = uni.getStorageSync('token')

    if (!isLoggedIn) {
      // 未登录，跳转到登录页
      uni.showToast({ title: '请先登录', icon: 'none' })
      next('/pages/login/index')
      return
    }
  }

  // 继续导航
  next()
})
```

### 2. 全局后置守卫

```typescript
// src/router/index.ts
router.afterEach((to, from) => {
  console.log('路由跳转完成:', to.path)

  // 可以在这里做一些统计或记录
})
```

### 3. 路由元数据配置

可以在页面文件中使用`<route>`自定义块来定义路由元数据：

```vue
<template>
  <!-- 页面内容 -->
</template>

<script setup>
// 页面逻辑
</script>

<route lang="json">
{
  "name": "protected-page",
  "meta": {
    "requireAuth": true,
    "title": "需要登录的页面"
  }
}
</route>
```

## 五、实战示例：登录权限控制

### 1. 定义带有权限控制的路由

```typescript
// src/router/index.ts
import { createRouter } from 'uni-mini-router'

const router = createRouter({
  routes: generateRoutes()
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 检查页面是否需要登录
  if (to.meta && to.meta.requireAuth) {
    const token = uni.getStorageSync('token')

    if (!token) {
      // 显示登录提示
      uni.showModal({
        title: '提示',
        content: '该功能需要登录后使用',
        confirmText: '去登录',
        cancelText: '返回',
        success: (res) => {
          if (res.confirm) {
            // 记住原来要去的页面
            uni.setStorageSync('redirect', to.fullPath)
            next('/pages/login/index')
          } else {
            // 取消则返回首页
            next('/pages/index/index')
          }
        }
      })
      return
    }
  }

  // 继续导航
  next()
})

export default router
```

### 2. 登录成功后跳转回原页面

```vue
<!-- src/pages/login/index.vue -->
<script setup>
const router = useRouter()

function handleLogin() {
  // 模拟登录请求
  setTimeout(() => {
    // 登录成功，存储token
    uni.setStorageSync('token', 'user_token_example')

    // 获取之前要去的页面
    const redirect = uni.getStorageSync('redirect') || '/pages/index/index'
    uni.removeStorageSync('redirect')

    // 跳转回原来的页面
    router.replaceAll(redirect)
  }, 1000)
}
</script>
```

## 六、最佳实践与性能优化

### 1. 合理使用跳转方式

- **router.push**：需要保留当前页面、可返回时使用
- **router.replace**：不需要返回当前页面时使用
- **router.replaceAll**：需要清除所有页面栈时使用（如登录后）
- **router.pushTab**：跳转到tabBar页面时使用

### 2. 参数传递最佳实践

- 对于简单数据，直接使用参数传递
- 对于复杂数据或对象，可使用以下方法：

```typescript
// 传递复杂对象
const complexData = { name: 'product', details: { id: 1, features: ['a', 'b'] } }

// 方法1: JSON序列化 + URL编码
router.push({
  path: '/pages/detail/index',
  query: { data: encodeURIComponent(JSON.stringify(complexData)) }
})

// 接收页面
onLoad((option) => {
  if (option.data) {
    try {
      const data = JSON.parse(decodeURIComponent(option.data))
      console.log(data)
    } catch (e) {
      console.error('参数解析错误', e)
    }
  }
})

// 方法2: 对于非常大的数据，考虑使用全局状态管理或本地存储
```

### 3. 路由懒加载

uni-mini-router自动支持小程序的分包加载特性，可以在pages.json中配置分包：

```json
{
  "pages": [
    // 主包页面
  ],
  "subPackages": [
    {
      "root": "pages/module",
      "pages": [
        {
          "path": "detail/index",
          "style": {
            "navigationBarTitleText": "详情页"
          }
        }
      ]
    }
  ]
}
```

## 七、路由调试与测试

### 1. 路由日志记录

```typescript
// src/router/index.ts
router.beforeEach((to, from, next) => {
  console.log(`[Router] ${from.path || '初始页面'} -> ${to.path}`, {
    params: to.params,
    query: to.query,
  })
  next()
})
```

### 2. 常见问题解决

1. **路由参数获取不到**：
   - 检查传参方式是否正确
   - 使用`console.log`打印完整的option对象
   - 尝试同时检查route.query和route.params

2. **页面未注册**：
   - 确保页面已在pages.json中正确注册
   - 检查路径大小写是否正确

3. **导航守卫不生效**：
   - 确保在路由配置后调用守卫
   - 检查是否正确调用next()函数

## 总结

uni-mini-router为uni-app提供了Vue Router风格的路由解决方案，特别是增加了路由拦截功能，解决了uni-app原生路由的限制。通过简单配置，就能在uni-app中实现更加灵活的路由管理，包括权限控制、参数传递和路由拦截等高级功能。

使用uni-mini-router可以让你的uni-app项目路由管理更加规范化和工程化，提升开发效率和代码质量。

参考资料：

- [uni-mini-router GitHub仓库](https://github.com/Moonofweisheng/uni-mini-router)
- [uni-mini-router官方文档](https://moonofweisheng.github.io/uni-mini-router/)
- [uni-app官方路由文档](https://uniapp.dcloud.net.cn/tutorial/page.html)
