# -*- coding: utf-8 -*-

# Gunicorn是否为守护进程（后端进程）
daemon = True

# 监听内网端口8000, 绑定的IP地址和端口
bind = "0.0.0.0:8000"

# 工作目录
chdir = '.'

# 工作模式，采用uvicorn库
worker_class = "uvicorn.workers.UvicornWorker"

# 服务器中排队等待的最大连接数
backlog = 2048

# 定义同时开启的处理请求的进程数量
workers = 4

# 数据库连接数
threads = 2

# 最大客户端并发数量
worker_connections = 1000

# 访问超时时间，默认30s
timeout = 600

# 接收到restart信号后，worker可以在graceful_timeout时间内，继续处理完当前requests
graceful_timeout = 60

# server端保持连接时间
keepalive = 2

# # HTTP请求行的最大大小
limit_request_line = 4094

# # 限制HTTP请求中请求头字段的数量
limit_request_fields = 100

# # 限制HTTP请求中请求头的大小
limit_request_field_size = 8190

reload = False

# 设置进程pid记录文件目录
pidfile = 'logs/gunicorn.pid'

# 日志级别
loglevel = 'debug'
# 访问日志文件路径
accesslog = "logs/gunicorn_access.log"
# 错误日志文件的路径
errorlog = "logs/gunicorn_error.log"
# 访问日志文件格式
access_log_format = '%(t)s %(h)s "%(r)s" %(s)s %(b)s "%(f)s" "%(L)s"'

# 启动命令 : gunicorn -c gunicorn.py main:create_app
# 启动查看 : ps -ef | grep gunicorn
# 停止命令 : kill -9 $(ps -ef | grep gunicorn | awk '{print $2}')
# 在Linux中查看Gunicorn相关的进程树结构命令：pstree -ap | grep gunicorn
# Dockerfile中启动命令：ENTRYPOINT ["gunicorn", "-c", "gunicorn.py", "main:create_app"]
