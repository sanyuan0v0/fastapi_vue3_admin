# fastdocs

## 项目结构

```sh
fastapi_vue3_admin/fastdocs
├─ .vitepress           # 静态资源文件
│  ├─ cache             # 缓存
│  ├─ theme             # 主题
│  └─ config.js         # 配置文件
├─ src                  # 源代码
│  ├─ about             # 关于
│  ├─ guide.md          # 指南
│  └─ index.md          # 首页
├─ package.json         # 项目依赖文件件
└─ README.md            # 项目说明文档

```

## 快速开始

```sh
# 进入前端工程目录
cd fastdocs
# 安装依赖
pnpm install
# 运行文档工程
pnpm run docs:dev
# 构建文档工程
pnpm run docs:build
```
