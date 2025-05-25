# backend

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
├─ env                     # 项目环境配置文件
├─ logs                    # 项目日志文件
├─ sql                     # 项目数据库文件
├─ static                  # 项目静态文件
├─ main.py                 # 项目启动文件
├─ alembic.ini             # alembic配置文件
├─ gunicorn.py             # gunicorn配置文件
├─ requirements.txt        # 项目依赖文件
├─ mkdocs.yml              # mkdocs配置文件
├─ dev_sql.db              # 项目数据库文件
└─ README.md               # 项目说明文档

```

## 快速开始

```sh
#  进入后端工程目录
cd backend
# 安装依赖
pip3 install -r requirements.txt
# 启动后端服务
python3 main.py run 
或 
python3 main.py run--env=dev 
# 生成迁移文件
python3 main.py revision "初始化迁移" --env=dev(不加默认为dev)
# 应用迁移
python3 main.py upgrade --env=dev(不加默认为dev)
```

## Markdown转静态网站（mkdocs-material使用）介绍

- 名称：mkdocs-material
- 官网：<https://squidfunk.github.io/mkdocs-material/>
- 完整文档信息清访问 [mkdocs官网](https://www.mkdocs.org).

## 工具安装

```sh
pip install mkdocs-material
```

## 工具使用

### 创建项目

```sh
mkdocs new 项目名称
```

### 编辑构建文档

```yaml
theme:
  name: material
```

### 启动服务

```sh
mkdocs serve
```

### 构建静态站点

```sh
mkdocs build
```

### 获取帮助

```sh
mkdocs -h
```

### 生成所有依赖

```sh
pip freeze > requirements.txt
```

