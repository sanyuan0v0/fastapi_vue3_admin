# devops


## 项目结构

```sh
fastapi_project/devops/     
├─ backend      # 后端部署目录
├─ mysql        # mysql部署目录
├─ nginx        # nginx部署目录
├─ redis        # redis部署目录
└─ README.md    # 项目说明文档

```

## 快速开始

```sh
# 复制脚本 `fastapi_vue3_amdin/start.sh` 脚本文件到服务器, 并赋予执行权限
chmod +x start.sh
# 执行脚本
./start.sh
#  访问地址
# 前端访问: `http://公网地址:80`, 
# 接口访问: `http://公网地址:8001/api/v1/docs`， 
# 登录 `admin/123456` 或  `demo/123456`
# 查看镜像:
docsker images -a
# 查看容器:
docsker compose ps
# 查看日志
docker logs -f <容器名>
# 服务停止
docsker compose down
# 删除镜像
docker rmi <镜像名>
# 删除容器
docker rm <容器名>
```

- **部署问题排查**:
  - 后端配置文件 `fastapi_vue3_amdin/backend/env/.env.prod.py`
  - 前端配置文件 `fastapi_vue3_amdin/frontend/vite.config.ts` 和 `fastapi_vue3_amdin/frontend/.env.production`
  - 部署文件  `fastapi_vue3_amdin/docker-compose.yaml` 和 `fastapi_vue3_amdin/devops/devops/nginx/nginx.conf`
