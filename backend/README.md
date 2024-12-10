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
my_demo_project/fastapi_project/backend
├─ app                     # 项目核心代码 
│  ├─ api                  # 接口模块  
│  │  ├─ common            # 公共模块
│  │  ├─ utils             # 工具模块
│  │  └─ v1                # 接口版本模块
│  │     ├─ controllers    # 控制器模块
│  │     ├─ models         # 模型模块
│  │     ├─ schemas        # 数据模型模块
│  │     └─ services       # 业务模块
│  ├─ config               # 项目配置文件
│  ├─ core                 # 项目核心模块
│  ├─ plugin               # 项目插件模块
│  └─ scripts              # 项目脚本模块
├─ main.py                 # 项目启动文件
├─ gunicorn.py             # gunicorn配置文件
├─ logs                    # 项目日志文件
├─ data                    # 项目数据文件
├─ upload                  # 项目上传文件
├─ static                  # 项目静态文件
├─ templates               # 项目模板文件
├─ requirements.txt        # 项目依赖文件
├─ nginx.conf              # nginx配置文件
├─ dev_sql.db              # 项目数据库文件
├─ init_db.sql             # 项目初始化数据库文件
├─ start.sh                # 项目启动脚本
├─ stop.sh                 # 项目停止脚本
├─ docker-compose.yaml     # docker-compose配置文件
├─ Dockerfile              # docker镜像构建文件
├─ README.en.md            # 项目英文文档 
└─ README.md               # 项目中文文档

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

## 相关技术

```sh
一 Nginx配置文件简介
Nginx的配置文件是一个文本文件，通常位于/conf/nginx.conf。它使用一种简洁而灵活的语法来定义Nginx服务器的行为和功能。配置文件中的指令按照特定的顺序进行解析和执行，从而实现对服务器行为的精确控制。

二 Nginx配置文件的结构、指令、用法和解析
Nginx的默认配置文件是nginx.conf。下面是nginx默认配置文件内容的解析和配置文件的用法的说明：
配置文件的结构：

全局块：配置全局的指令，对整个Nginx服务器起作用。
events块：配置与连接相关的指令，如工作进程数和连接超时时间等。
http块：配置HTTP服务器的指令，如监听端口、虚拟主机和HTTP模块等。
server块：配置虚拟主机的指令，可以配置多个server块来支持多个域名或IP地址。
location块：配置URL路径的指令，可以在server块或http块中使用。
配置文件的指令：

listen：指定Nginx服务器监听的端口
server_name：指定虚拟主机的域名或IP地址
root：指定网站的根目录
index：指定默认的首页文件
location：指定URL路径的匹配规则和处理方式
proxy_pass：配置反向代理服务器的目标地址
rewrite：配置URL重写规则
user：指定Nginx worker进程运行的用户
worker_processes：指定Nginx启动的worker进程数
error_log：指定错误日志的路径
pid：指定进程ID文件的路径
events：配置事件模块，如worker连接数
http：配置HTTP模块
include：包含其他配置文件
server：定义一个虚拟主机。
配置文件的用法：

修改监听端口：在http块或server块中使用listen指令来指定监听的端口。
配置虚拟主机：在http块中使用server块来配置虚拟主机，可以使用server_name指令来指定域名或IP地址。
配置反向代理：在location块中使用proxy_pass指令来配置反向代理服务器的目标地址。
配置URL重写：在location块中使用rewrite指令来配置URL重写规则。
配置文件的解析：

Nginx按照配置文件的结构从上到下依次解析，先解析全局块，再解析events块，最后解析http块。
在http块中可以配置多个server块，Nginx会根据请求的域名或IP地址来匹配对应的server块。
在server块中可以配置多个location块，Nginx会根据请求的URL路径来匹配对应的location块。
```
