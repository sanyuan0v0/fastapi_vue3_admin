# -*- coding: utf-8 -*-

from typing import Dict, Any
from celery import Celery
from datetime import datetime

from pydantic import RedisDsn

from app.config.setting import settings

REDIS_URL: RedisDsn = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_NAME}"
# 创建 Celery 实例
celery_app = Celery(
    "worker", 
    broker=REDIS_URL,
    backend=REDIS_URL,  # 使用 Redis 存储任务结果
    include=["tasks"],  # 包含任务模块
)

# 配置 Celery
celery_app.conf.update(
    result_expires=3600,  # 任务结果过期时间（秒）
    timezone="Asia/Shanghai",  # 时区
)

# 不可以使用协程：TypeError: object AsyncResult can't be used in 'await' expression
@celery_app.task
def background_task(data):
    return f"task_id: {data}"

