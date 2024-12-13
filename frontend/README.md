# 前端介绍

这是一个基于Vue3的Vite项目，使用Vue3、Vite、TypeScript、Vuex、Vue-router、Ant-Design-Vue、Axios等框架。

- npm init vue@latest   创建项目
- cd frontend           进入项目
- npm install           安装依赖
- npm run dev           启动项目

## 项目结构

```sh
fastapi_project/frontend
├─ public               # 静态资源文件 
│  └─ site              # 帮助文档模块
├─ src                  # 源代码
│  ├─ api               # 接口文件
│  ├─ components        # 组件模块
│  ├─ layouts           # 布局模块
│  ├─ router            # 路由模块
│  ├─ store             # 状态管理模块
│  ├─ utils             # 工具模块
│  ├─ view              # 视图模块
│  ├─ App.vue           # 根组件
│  ├─ main.js           # 入口文件
│  └─ styles.css        # 全局样式文件
├─ .env.development     # 项目开发环境配置
├─ .env.production      # 项目生产环境配置
├─ index.html           # 模板文件
├─ package.json         # 项目依赖文件
├─ tsconfig.json        # ts配置文件
├─ vite.config.js       # vite服务配置文件
└─ README.md            # 项目说明文档

```

## 项目配置

查看 [Vite Configuration Reference](https://vitejs.dev/config/).

## 项目启动

### 初始化依赖

```sh
npm install
```

### 启动开发环境

```sh
npm run dev
```

### 构建项目

```sh
npm run build
```

### 项目检查

```sh
[ESLint](https://eslint.org/)

npm run lint
```
