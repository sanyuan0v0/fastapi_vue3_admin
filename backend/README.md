# 后端介绍

> 该项目是一个基于python的web服务框架，基于fastapi和sqlalchemy实现，支持多版本接口，支持swagger文档，支持redis缓存，支持mysql数据库，支持mongodb数据库，支持celery任务队列，支持jwt认证，支持日志记录，支持插件扩展，支持多环境配置，支持uvicorn部署，支持gunicorn部署，支持docker部署，支持nginx部署。

## 项目结构

```sh
fastapi_project/backend
├─ app                     # 项目核心代码 
│  ├─ almbic               # 数据库迁移文件
│  ├─ api                  # 接口模块  
│  │  └─ v1                # 接口版本模块
│  │     ├─ controllers    # 控制器模块
│  │     ├─ crud           # 数据库操作模块
│  │     ├─ models         # orm模型模块
│  │     ├─ params         # 参数模块
│  │     ├─ schemas        # pydantic模型模块
│  │     ├─ services       # 业务模块
│  │     └─ urls           # 路由模块
│  ├─ common               # 公共模块
│  ├─ config               # 项目配置文件
│  ├─ core                 # 项目核心模块
│  ├─ module_task          # 项目任务模块
│  ├─ plugin               # 项目插件模块
│  ├─ scripts              # 项目初始化模块
│  └─ utils                # 工具模块
├─ logs                    # 项目日志文件
├─ static                  # 项目静态文件
├─ templates               # 项目模板文件
├─ main.py                 # 项目启动文件
├─ alembic.ini             # alembic配置文件
├─ gunicorn.py             # gunicorn配置文件
├─ requirements.txt        # 项目依赖文件
├─ dev_sql.db              # 项目数据库文件
└─ README.md               # 项目说明文档

```

## 项目安装

- 1、克隆项目

  git clone <https://gitee.com/tao__tao/fastapi_vue3_admin.git>

- 2、切换到项目目录

  cd fastapi_vue3_admin/backend

- 3、虚拟环境安装

  python -m venv venv

- 4、虚拟环境激活

  source venv/bin/activate

- 5、安装依赖

  pip install -r requirements.txt

## 项目启动

```sh
# 方式一：
python main.py init   # 初始化数据
python main.py run    # 启动服务
# 方式二：
uvicorn main:create_app --host 0.0.0.0 --port 8000 --factory --workers 4
# 方式三：
gunicorn -c gunicorn.py main:create_app

# 修改了模型后需要：重新生成迁移文件，然后应用迁移
# 生成迁移
python main.py revision "初始化迁移" --env=dev(不加默认为dev)
# 应用迁移
python main.py upgrade --env=dev(不加默认为dev)
```
