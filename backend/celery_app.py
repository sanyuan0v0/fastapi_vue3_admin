# -*- coding: utf-8 -*-

from celery import Celery


from app.config.setting import settings


celery_app = Celery(
    'task_manager',  # 任务名称
    broker=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_NAME}", # broker消息中间件，
    backend=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_NAME}",  
    include=['app.core.tasks'] # tasks.py文件的引入
)

celery_app.conf.update(
    timezone='Asia/Shanghai',
    enable_utc=False,
    broker_connection_retry_on_startup = True # 设置启动时重试 broker 连接
)

# 启动celery
# celery -A celery_app.celery_app worker --loglevel=info
# celery -A celery_app.celery_app beat --loglevel=info
