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