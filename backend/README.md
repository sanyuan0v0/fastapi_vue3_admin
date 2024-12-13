# 后端介绍

> 该项目是一个基于python的web服务框架，基于fastapi和sqlalchemy实现，支持多版本接口，支持swagger文档，支持redis缓存，支持mysql数据库，支持mongodb数据库，支持celery任务队列，支持jwt认证，支持日志记录，支持插件扩展，支持多环境配置，支持uvicorn部署，支持gunicorn部署，支持docker部署，支持nginx部署。

用户 (User)

一个用户可以属于多个角色。
一个用户可以属于多个部门。
一个用户可以担任多个岗位。
角色 (Role)

一个角色可以分配给多个用户。
一个角色可以拥有多个菜单权限。
菜单 (Menu)

一个菜单可以被多个角色拥有。
菜单之间存在层级关系（树形结构）。
部门 (Department)

一个部门可以有多个用户。
部门之间存在层级关系（树形结构）。
岗位 (Position)

一个岗位可以有多个用户。
一个岗位可以属于一个部门。

## 项目结构

初始化 Alembic
alembic init alembic

生成初始迁移脚本：
alembic revision --autogenerate -m "initial migration"

应用迁移：
alembic upgrade head

```sh
fastapi_project/backend
├─ app                     # 项目核心代码 
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
│  ├─ plugin               # 项目插件模块
│  ├─ scripts              # 项目初始化模块
│  └─ utils                # 工具模块
├─ logs                    # 项目日志文件
├─ static                  # 项目静态文件
├─ templates               # 项目模板文件
├─ main.py                 # 项目启动文件
├─ gunicorn.py             # gunicorn配置文件
├─ requirements.txt        # 项目依赖文件
├─ dev_sql.db              # 项目数据库文件
└─ README.md               # 项目说明文档

```

## 项目安装

- 1、克隆项目

  git clone <https://gitee.com/tao__tao/my_demo_project.git>

- 2、切换到项目目录

  cd my_demo_project/fastapi_project/backend

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
```
