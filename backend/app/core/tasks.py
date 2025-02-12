# -*- coding: utf-8 -*-

from typing import Dict, Any
from celery import Celery
from datetime import datetime

from app.config.setting import settings

# 创建 Celery 实例
celery_app = Celery(
    "worker", 
    broker=settings.get_redis_uri,
    backend=settings.get_redis_uri,  # 使用 Redis 存储任务结果
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

