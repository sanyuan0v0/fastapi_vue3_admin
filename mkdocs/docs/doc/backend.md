# 后端介绍

> 该项目是一个基于python的web服务框架，基于fastapi和sqlalchemy实现，支持多版本接口，支持swagger文档，支持redis缓存，支持mysql数据库，支持mongodb数据库，支持celery任务队列，支持jwt认证，支持日志记录，支持插件扩展，支持多环境配置，支持uvicorn部署，支持gunicorn部署，支持docker部署，支持nginx部署。

## 后端

1. 安装依赖

   ```shell
   cd backend
   pip3 install -r requirements.txt
   ```

2. 修改项目数据库配置信息
   在`app/core/config.py`文件中的`SQLALCHEMY_DATABASE_URI`、`MONGO_DB_URL`、`REDIS_URL`

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
   ```
