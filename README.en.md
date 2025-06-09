<div align="center">
     <p align="center">
          <img src="./backend/docs/resources/logo.png" width="100"/> 
     </p>
     <h2 align="center">Fastapi-Vue3-Admin v1.0.0</h2>
     <h4 align="center">A modern, open-source, full-stack integrated rapid development platform for mid - and back - end systems. Give a ⭐️ to support!</h4>
     <p align="center">
          <a href="https://gitee.com/tao__tao/fastapi_vue3_admin.git" target="_blank">
               <img src="https://gitee.com/tao__tao/fastapi_vue3_admin/badge/star.svg?theme=dark" alt="Gitee Stars">
          </a>
          <a href="https://github.com/1014TaoTao/fastapi_vue3_admin.git" target="_blank">
               <img src="https://img.shields.io/github/stars/1014TaoTao/fastapi_vue3_admin?style=social" alt="GitHub Stars">
          </a>
          <a href="https://gitee.com/tao__tao/fastapi_vue3_admin/blob/master/LICENSE" target="_blank">
               <img src="https://img.shields.io/badge/License-MIT-orange" alt="License">
          </a>
          <img src="https://img.shields.io/badge/Python-≥3.10-blue"> 
          <img src="https://img.shields.io/badge/NodeJS-≥20.0-blue"> 
          <img src="https://img.shields.io/badge/MySQL-≥8.0-blue"> 
          <img src="https://img.shields.io/badge/Redis-≥7.0-blue"> 
          <img src="https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white"/> 
          <img src="https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3"/> 
          <img src="https://img.shields.io/badge/-JavaScript-563D7C?style=flat-square&logo=bootstrap"/> 
     </p>
</div>

---

English | [Chinese](./README.md)

---

## 📘 Project Introduction (Author: @1014TaoTao)

**Fastapi-Vue3-Admin** is a **completely open-source, highly modular, and technologically advanced modern rapid development platform**. Its aim is to help developers efficiently build high-quality enterprise-level mid - and back - end systems. This project adopts a **front - end and back - end separation architecture**, integrating the Python back - end framework `FastAPI` and the mainstream front - end framework `Vue3` to achieve unified development across multiple terminals, providing a one - stop out - of - the - box development experience.

> **Original Design Concept**: With modularity and loose coupling at its core, it pursues rich functional modules, simple and easy - to - use interfaces, detailed development documentation, and convenient maintenance methods. By unifying frameworks and components, it reduces the cost of technology selection, follows development specifications and design patterns, builds a powerful code hierarchical model, and comes with comprehensive local Chinese support. It is specifically tailored for team and enterprise development scenarios.

```sh
fastapi_vue3_admin
├─ backend        # Backend project
├─ frontend       # Frontend project
├─ devops         # Deployment project
├─ docker-compose.yaml # Deployment file
├─ start.sh       # One-click deployment script
├─ LICENSE        # License agreement
|─ README.en.md   # English documentation
└─ README.md      # Chinese documentation
```

---

## ✨ Core Highlights

| Feature | Description |
| ---- | ---- |
| 🔭 Rapid Development | A completely open-source modern rapid development platform designed to help developers efficiently build high-quality mid- and back-end systems. |
| 🌐 Full-stack Integration | Front-end and back-end separation, integrating Python (FastAPI) + Vue3 for multi-terminal development. |
| 🧱 Modular Design | Highly decoupled system functions, facilitating easy expansion and maintenance. |
| ⚡️ High-performance Asynchronous | Uses the FastAPI asynchronous framework + Redis cache to optimize API response speed. |
| 🔒 Secure Authentication | Supports the JWT OAuth2 authentication mechanism to ensure system security. |
| 📊 Permission Management | The RBAC model enables fine-grained permission control at the menu, button, and data levels. |
| 🚀 Rapid Deployment | Supports one-click deployment with Docker/Docker Compose/Nginx. |
| 📄 Developer-friendly | Provides comprehensive Chinese documentation, a Chinese interface, and a visual toolchain to reduce the learning curve. |
| 🚀 Quick Access | Based on mainstream front-end technology stacks such as Vue3, Vite5, Pinia, and Ant Design Vue, it's ready to use out of the box. |

---

## 🛠️ Technology Stack Overview

| Type     | Technology Selection            | Description |
|----------|---------------------------------|---------------------------------|
| Backend Framework | FastAPI / Uvicorn / Pydantic 2.0 / Alembic | A modern, high-performance asynchronous framework with enforced type constraints and data migration capabilities. |
| ORM      | SQLAlchemy 2.0      | A powerful ORM library. |
| Scheduled Tasks | APScheduler         | Easily implement scheduled tasks. |
| Authentication | PyJWT               | Implement JWT authentication. |
| Frontend Framework | Vue3 / Vite5 / Pinia / TypeScript | Quickly develop Vue3 applications. |
| UI Library    | Ant Design Vue | Quickly develop beautiful UI components. |
| Database   | MySQL / MongoDB     | Powerful databases. |
| Cache     | Redis               | A powerful caching database. |
| Documentation     | Swagger / Redoc     | Automatically generate API documentation. |
| Deployment     | Docker / Nginx / Docker Compose | Quickly deploy projects. |

---

## 📌 Built-in Modules

| Module Name     | Sub-module Name | Description |
|----------|---------------------|---------------------|
| Dashboard    | Workbench, Analysis Page  | Entry for commonly used functions |
| System Management  | Includes sub-modules such as menu, department, position, role, user, log, configuration, announcement, dictionary, and task | Main system functions |
| Monitoring Management  | Online users, server monitoring, cache monitoring | System monitoring and management functions |
| Public Management  | Interface management, document management | Project interface documentation |

---

## 🍪 Demo Environment

- Demo URL: <http://service.fastapiadmin.com>
- Administrator account: `admin` Password: `123456`
- Demo account: `demo` Password: `123456`

---

## 👷 Installation and Usage

### Version Information

| Type     | Technology Stack     | Version       |
|----------|----------------------|---------------|
| Backend  | Python               | 3.10 (Versions greater than 3.10 may have compatibility issues. Upgrades will be considered in the future, but not for now.) |
| Backend  | FastAPI              | 0.109         |
| Frontend | Node.js              | >= 20.0 (It is recommended to use the latest version.) |
| Frontend | npm                  | 16.14         |
| Frontend | Vue3                 | 3.3           |
| Database | MySQL                | 8.0 (It is recommended to use the latest version.) |
| Middleware | Redis              | 7.0 (It is recommended to use the latest version.) |

---

### Get Code

```sh
# Clone the code to your local machine
git clone https://gitee.com/tao__tao/fastapi_vue3_admin.git
或
git clone https://github.com/1014TaoTao/fastapi_vue3_admin.git
```

---

### Local Backend Startup

```sh
# Enter the backend project directory
cd backend
# Install dependencies
pip3 install -r requirements.txt
# Start the backend service
python3 main.py run 
or 
python3 main.py run --env=dev 
# Generate migration files
python3 main.py revision "Initial migration" --env=dev (default is dev if not specified)
# Apply migrations
python3 main.py upgrade --env=dev (default is dev if not specified)
```

---

### Local Frontend Startup

```sh
# Enter the frontend project directory
cd frontend
# Install dependencies
npm install
# Start the frontend service
npm run dev
# Build the frontend and generate the `frontend/dist` directory
npm run build
```

---

### Local Access Address

- Frontend address: <http://127.0.0.1:5180>
- API address: <http://127.0.0.1:8001/api/v1/docs>
- Administrator account: `admin` Password: `123456`
- Demo account: `demo` Password: `123456`

---

### Docker Build

```sh
# Copy the script `fastapi_vue3_admin/start.sh` to the server and grant execution permissions
chmod +x start.sh
# Execute the script
./start.sh
# View images:
docker images -a
# View containers:
docker compose ps
# View logs
docker logs -f <Container Name>
# Stop the service
docker compose down
# Delete an image
docker rmi <Image Name>
# Delete a container
docker rm <Container Name>
# Backend configuration file directory
fastapi_vue3_admin/backend/env/.env.prod.py
# Frontend configuration file directory
fastapi_vue3_admin/frontend/vite.config.ts
and 
fastapi_vue3_admin/frontend/.env.production
# Deployment file directory  
fastapi_vue3_admin/docker-compose.yaml
and 
fastapi_vue3_admin/devops/devops/nginx/nginx.conf

```

---

## 🔧 Models

<table>
    <tr>
        <td><img src="./backend/docs/resources/login.png"/>Login</td>
        <td><img src="./backend/docs/resources/dashboard.png"/>Dashboard</td>
        <td><img src="./backend/docs/resources/menu.png"/>Menu Management</td>
        <td><img src="./backend/docs/resources/dept.png"/>Department Management</td>
   </tr>
   <tr>
        <td><img src="./backend/docs/resources/position.png"/>Position Management</td>
        <td><img src="./backend/docs/resources/role.png"/>Role Management</td>
        <td><img src="./backend/docs/resources/user.png"/>User Management</td>
        <td><img src="./backend/docs/resources/log.png"/>Log Management</td>
   </tr>
   <tr>
        <td><img src="./backend/docs/resources/config.png"/>Configuration Management</td>
        <td><img src="./backend/docs/resources/online.png"/>Online User Management</td>
        <td><img src="./backend/docs/resources/service.png"/>Server Monitoring</td>
        <td><img src="./backend/docs/resources/cache.png"/>Cache Monitoring</td>
   </tr>
   <tr>
        <td><img src="./backend/docs/resources/job.png"/>Task Management</td>
        <td><img src="./backend/docs/resources/docs.png"/>API Management</td>
        <td><img src="./backend/docs/resources/redoc.png"/>Document Management</td>
        <td><img src="./backend/docs/resources/info.png"/>Personal Information</td>
   </tr>
   <tr>
        <td><img src="./backend/docs/resources/help.png"/>Online Documentation</td>
        <td><img src="./backend/docs/resources/dict.png"/>Dictionary Management</td>
   </tr>
</table>

---

## 🙏 Thanks

Thanks to the contributions and support of the following projects, which have enabled the successful completion of this project:

- [FastAPI Project](https://fastapi.tiangolo.com/)
- [Vue3 Project](https://v3.cn.vuejs.org/)
- [KInit Project](https://gitee.com/ktianc/kinit)
- [Fastapi-Vue3-Admin Project](https://gitee.com/senqi666/fastapi-vue-admin)
- [Vue-FastAPI-Admin Project](https://gitee.com/mizhexiaoxiao/vue-fastapi-admin)
- [RuoYi-Vue3-FastAPI Project](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI)
- [APScheduler Project](https://github.com/agronholm/apscheduler)
- [Vite Project](https://github.com/vitejs/vite)

---

## 🎨 Community

<table>
    <tr>
        <td><img src="./backend/docs/resources/wechat.jpg"/></td>
        <td><img src="./backend/docs/resources/group.jpg"/></td>
        <td><img src="./backend/docs/resources/wechatPay.jpg"/></td>
    </tr>
</table>

---

## ❤️ Star

If you like this project, please give it a ⭐️ Star to show your support! Thank you very much!

---

## 👀 Visitor Statistics

![Visitor Count](https://profile-counter.glitch.me/1014TaoTao/count.svg)

---
