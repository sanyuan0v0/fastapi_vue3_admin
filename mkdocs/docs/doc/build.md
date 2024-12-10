# 部署介绍

## docker

``` dockerfile
# 使用官方的 Python 3.10 镜像作为基础镜像
FROM python:3.10
# 使用 LABEL 替代 MAINTAINER
LABEL maintainer="管理员"
# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# 设置时区
ENV TZ Asia/Shanghai

# 升级pip版本
# RUN python -m pip install --upgrade pip

# 创建容器工作目录
RUN mkdir -p /opt/fastapi_project
# 设置容器内工作目录
WORKDIR /opt/fastapi_project
# 将当前主机目录全部文件复制至容器工作目录
COPY ./requirements.txt /code/requirements.txt
# 安装依赖
RUN pip install --no-cache-dir --upgrade -r /opt/fastapiproject/backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 部署 nginx
RUN apt-get update && apt-get install -y nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# # 部署mysql
# RUN apt-get install -y mysql-server

# # 部署redis
# RUN apt-get install -y redis-server

# # 部署mongo
# RUN apt-get install -y mongodb


#CMD 运行以下命令，daemon off后台运行，否则启动完就自动关闭
CMD ["nginx", "-g", "daemon off;"]  

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# 暴露端口
EXPOSE 8000
# python main.py run 或者 uvicorn main:create_app --host 0.0.0.0 --port 8000 --workers 4
ENTRYPOINT ["uvicorn", "backend.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--workers", 4]
# ENTRYPOINT ["gunicorn", "-c", "gunicorn.py", "main:create_app"]

```

## docker-componse

```yaml
version: "3.10.11"

# 应用服务
services:
  # 应用服务
  fastapi_getway:
    # 容器名称
    container_name: fastapi
    # 镜像名称
    image: fastapi
    env_file: .env
    networks:
      - db_network
      - web_network
    # 构建镜像
    build:
      context: ./
      dockerfile: Dockerfile
    #build: .
    # 将容器运行在特权模式下，意味着容器内的进程将具
    # 有访问宿主机的权限，包括文件系统、设备和系统功能等
    privileged: true
    # 指定容器中运行的用户
    user: root
    # 启动策略为始终重启
    restart: always
    # 设置网络模式为host模式
    network_mode: host
    # 端口映射
    ports:
      - 8020:8020
    # 文件挂载
    volumes:
      - ./:/data/apps
      - ./uploads:/data/apps/uploads
    # 执行命令
    command: python app.py runserver 0.0.0.0:8020 --noreload
    # 日志配置
    logging:
      driver: "json-file"
      options:
        max-size: "500m"
        max-file: "10"
  # nginx服务
  nginx:
    container_name: nginx
    restart: always
    image: "nginx:latest"
    ports:
      - "5000:5000"
    volumes:
      - ./nginx:/etc/nginx/conf.d
    networks:
      - web_network
    depends_on:
      - flask_api

  # 中间件服务
  mysql:
    container_name: mysql
    image: mysql:latest
    restart: always
    ports:
      - "3306:3306"
        # 数据卷挂载
        
networks:
  db_network:
    driver: bridge
  web_network:
    driver: bridge

```

## nginx

```nginx
########### 每个指令必须有分号结束。#################
user administrator administrators; # 配置用户或组，默认为nobody nobody
worker_processes 2; # 允许生成的进程数，默认为1
pid /nginx/pid/nginx.pid; # 指定 Nginx 进程运行文件存放地址
error_log log/error.log debug; # 制定日志路径，级别。这个设置可以放入全局块、http块、server块，级别依次为：debug|info|notice|warn|error|crit|alert|emerg

events {
    accept_mutex on; # 设置网络连接序列化，防止惊群现象发生，默认为on
    multi_accept on; # 设置一个进程是否同时接受多个网络连接，默认为off
    use epoll; # 事件驱动模型，select|poll|kqueue|epoll|resig|/dev/poll|eventport
    worker_connections 1024; # 最大连接数，默认为512
}

http {
    include mime.types; # 文件扩展名与文件类型映射表
    default_type application/octet-stream; # 默认文件类型，默认为text/plain

    # 取消服务日志
    access_log off;

    # 自定义日志格式
    log_format access '$remote_addr–$remote_user [$time_local] $request $status $body_bytes_sent $http_referer $http_user_agent $http_x_forwarded_for';

    # 启用访问日志
    access_log log/access.log access; # combined为日志格式的默认值

    sendfile on; # 允许sendfile方式传输文件，默认为off，可以在http块、server块、location块
    sendfile_max_chunk 100k; # 每个进程每次调用传输数量不能大于设定的值，默认为0，即不设上限
    keepalive_timeout 65; # 连接超时时间，默认为75秒，可以在http、server、location块

    # 定义上游服务器
    upstream mysvr {
        server 127.0.0.1:7878;
        server 192.168.10.121:3333 backup; # 热备
    }

    # 错误页
    error_page 404 https://www.baidu.com;

    # 定义一个 server 块
    server {
        # 单连接请求上限次数
        keepalive_requests 120;

        # 监听端口
        listen 4545;

        # 监听地址
        server_name 127.0.0.1;

        # 前端代理
        location / {
    proxy_set_header Host $host;
    root /web/front/;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header REMOTE-HOST $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    try_files $uri $uri/ /index.html;
    index /index.html;
        }

        # 后端代理
        location  /api/ {
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header REMOTE-HOST $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                add_header Access-Control-Allow-Methods *;
                add_header Access-Control-Allow-Origin $http_origin;
                proxy_pass http://127.0.0.1:8010/;
        }
    }
}
```
