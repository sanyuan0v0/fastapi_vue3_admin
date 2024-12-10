<div align="center">
   <p align="center">
      <img src="./mkdocs/docs/resources/images/logo.png" height="150" alt="logo"/>
   </p>
      <h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">Fastapi-Vue-Admin v1.0.0</h1>
      <h4 align="center">A rapid development framework for front-end and back-end separation based on Fastapi-Vue-Admin</h4>
   <p align="center">
      <img src="https://img.shields.io/badge/Python-≥3.10-blue">
      <img src="https://img.shields.io/badge/NodeJS-≥20.0-blue">
      <img src="https://img.shields.io/badge/MySQL-≥8.0-blue">
      <img src="https://img.shields.io/badge/Redis-≥7.0-blue">
   </p>
</div>

English | [Chinese](./README.md)

## 📚 Project Introduction

**fastapi-vue-admin** is a fully open-source rapid development platform that provides free usage. It combines modern, high-performance technology stacks to help developers quickly build high-quality backend systems. The project directory structure is as follows:

```sh
my_demo_project/fastapi_project
├─ backend        # Backend project
├─ frontend       # Frontend project
├─ mkdocs         # Documentation project
├─ build          # Deployment project
├─ README.en.md   # English documentation
└─ README.md      # Chinese documentation


- **Backend**：
  - **FastAPI**：A modern, high-performance asynchronous framework.
  - **Swagger**：Automatically generates interactive API documentation.
  - **Pydantic**：Enforces type constraints.
  - **SQLAlchemy 2.0**：A powerful ORM library.

- **Frontend**：
  - **Vue3**：A modern frontend framework.
  - **Ant Design Vue**：An enterprise-level UI component library.
  - **TypeScript**：Static type checking.
  - **Vite**：A fast build tool.

- **Authentication**：OAuth2 using hashed passwords and JWT Bearer tokens.
- **Authorization Architecture**：Designed based on RBAC, supporting dynamic permission menus, button-level permission control, and data-level permission control.
- **Ready-to-use**：Suitable as a starting template for new projects, also useful for learning and reference.

If you find the project helpful, please give it a star!

## 🍻 Project Features

- Modular and loosely coupled
- Rich modules, ready-to-use
- Simple and easy to integrate
- Comprehensive documentation, easy to maintain
- Top-down, systematic design
- Unified framework, unified components, reducing selection costs
- Development standards, design patterns, code layering models
- Powerful and convenient development toolchain
- Complete local internationalization support
- Designed for team and enterprise use

## 📌 Built-in Modules

- **Dashboard**
  - **Workbench**：Dashboard display, entry point for common features.
  - **Analytics**：Displays various statistical information to help users understand system performance.

- **System Management**
  - **Menu Management**：Configures system menus, operation permissions, and button permission identifiers.
  - **Department Management**：Configures the organizational structure of the system, supports data permissions in tree structures.
  - **Position Management**：Manages user positions.
  - **Role Management**：Manages role menus and permission allocation, sets menu permissions for roles.
  - **User Management**：Maintains and manages system users, including regular information maintenance and account settings.
  - **Log Management**：Uniformly maintains commonly used and relatively fixed data in the system.
  - **API Management**：Maintains the system's configuration information, uniformly manages website configuration management functions.
  - **Common Management**：Maintains the release and management of system notifications and announcements.

- **Monitoring Management**
  - **Online Users**：Views currently online users in the system.
  - **Server Monitoring**：Views the system's runtime status, including memory, CPU, disk, etc.
  - **Cache Monitoring**：Views system cache information, such as cache hit rate and cache keys.

- **Common Management**
  - **API Management**：Maintains system APIs, such as API addresses and request methods.
  - **Documentation Management**：Maintains system API documentation, supports online API calls.
  - **File Management**：Configures file uploads, currently supports local storage, and can obtain storage addresses based on specific configurations.


## 🍪  Account Information

| Account Type   | Username   | Password  |
| :--------- | :----- | :----- |
| **Admin Account** | admin  | 123456 |
| **Demo Account**   | demo   | 123456 |

## 👷 Installation and Usage

### Version Information

| Type | Technology Stack | Version  |
|----------|------------|------------|
| Backend     | Python     | 3.10       |
| Backend     | FastAPI    | 0.109      |
| Frontend     | Node.js    | >= 20.0（Recommended latest version）|
| Frontend     | npm        | 16.14      |
| Frontend     | Vue3       | 3.3        |
| Database   | MySQL      | 8.0 Recommended latest version|
| Database   | PostgreSQL | 14（Recommended latest version）|
| Database   | MongoDB    | 8.0（Recommended latest version）|
| Middleware   | Redis      | 7.0 Recommended latest version|

### Get the Code

```sh
git clone https://gitee.com/tao__tao/fastapi_vue_admin.git
```

### Backend

1. Install dependencies

   ```shell
   cd backend
   pip3 install -r requirements.txt
   ```

2. Modify project database configuration
   In the `app/core/config.py` file, modify `SQLALCHEMY_DATABASE_URI`、`MONGO_DB_URL` and `REDIS_URL`

3. Create a database named `fastapi_vue_admin`

4. Initialize database data

   ```shell
   # Run in the root directory of the backend project (backend)
   # This command will automatically generate tables and data in the database
   # If the database has already been initialized, this command can be skipped
   python3 main.py init
   ```

5. Start the backend

   ```shell
   # Run in the root directory of the backend project (backend)
   python3 main.py run
   ```

### Frontend

1. Install dependencies

   ```shell
   cd frontend
   npm install
   ```

2. Run the frontend

   ```shell
   npm run dev
   ```

3. Build the frontend

   ```shell
   npm run build
   ```

### Access the Project

- Frontend URL: <http://127.0.0.1:5180>
- Username: `admin` Password: `123456`
- API URL: <http://127.0.0.1:8000/api/v1/docs>

## 🔧 Module Showcase

### Login

![Login](./mkdocs/docs/resources/images/login.png)

### Workbench

![Workbench](./mkdocs/docs/resources/images/dashboard.png)

### Analytics

![Analytics](./mkdocs/docs/resources/images/analytics.png)

### Menu

![Menu](./mkdocs/docs/resources/images/menu.png)

### Department

![Department](./mkdocs/docs/resources/images/dept.png)

### Position

![Position](./mkdocs/docs/resources/images/position.png)

### Role

![Role](./mkdocs/docs/resources/images/role.png)

### User

![User](./mkdocs/docs/resources/images/user.png)

### Log

![Log](./mkdocs/docs/resources/images/log.png)

### Online

![Online](./mkdocs/docs/resources/images/online.png)

### Server

![Server](./mkdocs/docs/resources/images/service.png)

### Cache

![Cache](./mkdocs/docs/resources/images/cache.png)

### API

![API](./mkdocs/docs/resources/images/docs.png)

### Documentation

![Documentation](./mkdocs/docs/resources/images/redoc.png)

### File

![File](./mkdocs/docs/resources/images/file.png)

### Personal

![Personal](./mkdocs/docs/resources/images/info.png)

### Help

![Help](./mkdocs/docs/resources/images/help.png)

## ✨ Special Thanks

Thank you to the following projects for their contributions and support, which have made this project possible:

- [FastAPI Project](https://fastapi.tiangolo.com/)
- [Vue3 Project](https://v3.cn.vuejs.org/)
- [KInit Project](https://gitee.com/ktianc/kinit)
- [FastAPI-Vue-Admin Project](https://gitee.com/senqi666/fastapi-vue-admin)
- [Vue-FastAPI-Admin Project](https://gitee.com/mizhexiaoxiao/vue-fastapi-admin)
- [RuoYi-Vue3-FastAPI Project](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI)

## 🎨 WeChat Group

The QR codes below are personal codes that can be used for technical discussions and to discuss various issues encountered during project usage. I sincerely hope everyone can optimize the project together and actively participate in discussions to support each other!！

### Personal QR Codes

<table>
    <tr>
        <td><img src="./mkdocs/docs/resources/images/wechat.jpg"/></td>
        <td><img src="./mkdocs/docs/resources/images/wechatPay.jpg"/></td>
    </tr>
</table>
