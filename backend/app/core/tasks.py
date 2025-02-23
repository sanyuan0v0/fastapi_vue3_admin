# -*- coding: utf-8 -*-

import time

from celery_app import celery_app
from app.core.logger import logger

@celery_app.task
def task(res):
    try:
        logger.info(f"开始执行任务: {res}")
        time.sleep(3)
        result = f"发送任务: {res}"
        logger.info(f"任务执行成功: {result}")
        return result
    except Exception as e:
        logger.error(f"任务执行失败: {e}")
        raise