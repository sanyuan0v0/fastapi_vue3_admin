<div align="center">
   <p align="center">
      <img src="./mkdocs/docs/resources/images/logo.png" height="150" alt="logo"/>
   </p>
      <h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">Fastapi-Vue3-Admin v1.0.0</h1>
      <h4 align="center">基于Fastapi-Vue-Admi前后端分离的快速开发框架</h4>
   <p align="center">
      <a href="https://gitee.com/tao__tao/fastapi_vue3_admin.git">
         <img src="https://gitee.com/tao__tao/fastapi_vue3_admin/badge/star.svg?theme=dark">
      </a>
      <a href="https://github.com/1014TaoTao/fastapi_vue3_admin.git">
         <img src="https://img.shields.io/github/stars/1014TaoTao/fastapi_vue3_admin?style=social">
      </a>
      <a href="https://gitee.com/tao__tao/fastapi_vue3_admin/blob/master/LICENSE">
         <img src="https://img.shields.io/badge/License-MIT-orange">
      </a>
      <img src="https://img.shields.io/badge/Python-≥3.10-blue">
      <img src="https://img.shields.io/badge/NodeJS-≥20.0-blue">
      <img src="https://img.shields.io/badge/MySQL-≥8.0-blue">
      <img src="https://img.shields.io/badge/Redis-≥7.0-blue">
   </p>
</div>

简体中文 | [English](./README.en.md)

## 📚 项目介绍

**Fastapi-Vue3-Admin** 是一套完全开源的快速开发平台，提供免费使用。它结合了现代、高性能的技术栈，旨在帮助开发者快速搭建高质量的中后台系统。项目目录结构如下：

```sh
fastapi_vue_admin
├─ backend        # 后端工程
├─ frontend       # 前端工程
├─ devops         # 部署工程
├─ mkdocs         # 文档工程
|─ README.en.md   # 英文文档
└─ README.md      # 中文文档
```

- **后端**：
  - **FastAPI**：现代、高性能的异步框架
  - **Swagger**：自动生成交互式 API 文档
  - **Pydantic**：强制类型约束
  - **SQLAlchemy 2.0**：强大的 ORM 库

- **前端**：
  - **Vue3**：现代前端框架
  - **Ant Design Vue**：企业级 UI 组件库
  - **TypeScript**：静态类型检查
  - **Vite**：快速的构建工具

- **权限认证**：使用哈希密码和 JWT Bearer 令牌的 OAuth2
- **权限架构**：基于 RBAC 设计，支持动态权限菜单、按钮级别权限控制、数据级别权限控制
- **开箱即用**：适合新项目启动模板，也可用于学习参考

如果觉得项目不错，欢迎 Star 支持！

## 🍻 项目特点

- 模块化、松耦合
- 模块丰富、开箱即用
- 简洁易用、快速接入
- 文档详尽、易于维护
- 自顶向下、体系化设计
- 统一框架、统一组件、降低选择成本
- 开发规范、设计模式、代码分层模型
- 强大便捷的开发工具链
- 完善的本地中文化支持
- 设计为团队及企业使用

## 📌 内置模块

- **仪表盘**：仪表盘展示，常用功能入口。

- **系统管理**
  - **菜单管理**：配置系统菜单，操作权限，按钮权限标识等。
  - **部门管理**：配置系统组织机构，树结构展现支持数据权限。
  - **岗位管理**：主要管理用户担任岗位。
  - **角色管理**：角色菜单管理与权限分配、设置角色所拥有的菜单权限。
  - **用户管理**：用于维护管理系统的用户，常规信息的维护与账号设置。
  - **日志管理**：对系统中常用的较为固定的数据进行统一维护。
  - **配置管理**：主要是系统配置信息，如：系统名称、系统版本、系统描述等。
  - **公告管理**：系统通知公告信息发布维护。

- **监控管理**
  - **在线用户**：查看当前系统中在线的用户。
  - **服务器监控**：查看系统运行状态，包括内存、CPU、磁盘等。
  - **缓存监控**：查看系统缓存信息，如：缓存命中率、缓存键值等。

- **公共管理**
  - **接口管理**：系统接口维护，如：接口地址、请求方式等。
  - **文档管理**：系统接口文档维护，支持在线接口调用。

## 🍪  账号信息

| 账户类型   | 账号   | 密码   |
| :--------- | :----- | :----- |
| **管理员账户** | admin  | 123456 |
| **演示账户**   | demo   | 123456 |

## 👷 安装和使用

### 版本说明

| 类型     | 技术栈     | 版本       |
|----------|------------|------------|
| 后端     | Python     | 3.10       |
| 后端     | FastAPI    | 0.109      |
| 前端     | Node.js    | >= 20.0（推荐使用最新版）|
| 前端     | npm        | 16.14      |
| 前端     | Vue3       | 3.3        |
| 数据库   | MySQL      | 8.0 （推荐使用最新版）|
| 数据库   | PostgreSQL | 14（其他版本均未测试）|
| 数据库   | MongoDB    | 8.0（推荐使用最新版）|
| 中间件   | Redis      | 7.0 （推荐使用最新版）|

### 获取代码

```sh
git clone https://gitee.com/tao__tao/fastapi_vue3_admin.git
```

### 后端

1. 安装依赖

   ```shell
   cd backend
   pip3 install -r requirements.txt

   pip install 遇到UnicodeDecodeError: 'gbk' codec can't decode byte 0xad in position
   解决方案：https://www.cnblogs.com/RexTooru/p/17303318.html
   ```

2. 修改项目数据库配置信息
   在`app/config/.env.dev(.env.test、.env.prod)`文件中的`DB_DRIVER`数据库驱动类型，以及对应的数据库的配置信息

3. 创建名为`fastapi_vue_admin`的数据库

4. 初始化数据库数据

   ```shell
   # 进入后端根目录 backend 下运行
   # 运行命令后会自动生成数据库内的表和数据
   # 如已初始化数据库数据，此命令可不执行
   python3 main.py init
   ```

5. 启动

   ```shell
   # 进入后端根目录 backend 下运行
   python3 main.py run
   # 如果使用celery管理任务，需要另外启动celery
   启动普通任务work: celery -A celery_app.celery_app worker --loglevel=info
   启动定时任务work: celery -A celery_app.celery_app beat --loglevel=info
   ```

### 前端

1. 安装依赖

   ```shell
   cd frontend
   npm install
   ```

2. 运行

   ```shell
   npm run dev
   ```

3. 打包

   ```shell
   npm run build
   ```

### 访问项目

- 前端地址：<http://127.0.0.1:5180>
- 账号：`admin` 密码：`123456`
- 接口地址：<http://127.0.0.1:8000/api/v1/docs>

## 🔧 模块展示

<table>
    <tr>
        <td><img src="./mkdocs/docs/resources/images/login.png"/>登陆</td>
        <td><img src="./mkdocs/docs/resources/images/dashboard.png"/>仪表盘</td>
   </tr>
   <tr>
        <td><img src="./mkdocs/docs/resources/images/menu.png"/>菜单管理</td>
        <td><img src="./mkdocs/docs/resources/images/dept.png"/>部门管理</td>
   </tr>
   <tr>
        <td><img src="./mkdocs/docs/resources/images/position.png"/>岗位管理</td>
        <td><img src="./mkdocs/docs/resources/images/role.png"/>角色管理</td>
   </tr>
   <tr>
        <td><img src="./mkdocs/docs/resources/images/user.png"/>用户管理</td>
        <td><img src="./mkdocs/docs/resources/images/log.png"/>日志管理</td>
   </tr>
   <tr>
        <td><img src="./mkdocs/docs/resources/images/config.png"/>配置管理</td>
        <td><img src="./mkdocs/docs/resources/images/online.png"/>在线用户管理</td>
   </tr>
   <tr>
        <td><img src="./mkdocs/docs/resources/images/service.png"/>服务器监控</td>
        <td><img src="./mkdocs/docs/resources/images/cache.png"/>缓存监控</td>
   </tr>
   <tr>
        <td><img src="./mkdocs/docs/resources/images/task.jpeg"/>任务管理</td>
        <td><img src="./mkdocs/docs/resources/images/docs.png"/>接口管理</td>
   </tr>
        <td><img src="./mkdocs/docs/resources/images/redoc.png"/>文档管理</td>
        <td><img src="./mkdocs/docs/resources/images/info.png"/>个人信息</td>
   </tr>
   </tr>
        <td><img src="./mkdocs/docs/resources/images/help.png"/>在线文档</td>
   </tr>
</table>

## ✨ 特别鸣谢

感谢以下项目的贡献和支持，使本项目得以顺利完成：

- [FastAPI 项目](https://fastapi.tiangolo.com/)
- [Vue3 项目](https://v3.cn.vuejs.org/)
- [KInit 项目](https://gitee.com/ktianc/kinit)
- [Fastapi-Vue3-Admin 项目](https://gitee.com/senqi666/fastapi-vue-admin)
- [Vue-FastAPI-Admin 项目](https://gitee.com/mizhexiaoxiao/vue-fastapi-admin)
- [RuoYi-Vue3-FastAPI 项目](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI)

## 🎨 微信群

在下方为群二维码，可以用于技术交流，也可以一起讨论在项目使用过程中遇到的各种问题。真心希望大家一起优化该项目，积极讨论，让我们一起抱团取暖！

### 群二维码

<table>
    <tr>
      <td><img src="./mkdocs/docs/resources/images/微信.jpg"/></td>
        <td><img src="./mkdocs/docs/resources/images/wechat.png"/></td>
        <td><img src="./mkdocs/docs/resources/images/wechatPay.jpg"/></td>
    </tr>
</table>
