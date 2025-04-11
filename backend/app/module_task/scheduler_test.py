# -*- coding: utf-8 -*-

import time
from datetime import datetime

from app.core.logger import logger

def job(*args, **kwargs):
    """
    定时任务执行同步函数示例
    """
    logger.info(f'{datetime.now()}同步函数执行了')
    try:
        logger.info(f"开始执行任务: {args}{kwargs}")
        time.sleep(3)
        logger.info(f"任务执行成功: {args}{kwargs}")
    except Exception as e:
        logger.error(f"任务执行失败: {e}")
        raise

async def async_job(*args, **kwargs):
    """
    定时任务执行异步函数示例
    """
    logger.info(f'{datetime.now()}异步函数执行了')
    try:
        logger.info(f"开始执行任务: {args}{kwargs}")
        time.sleep(3)
        logger.info(f"任务执行成功: {args}{kwargs}")
    except Exception as e:
        logger.error(f"任务执行失败: {e}")
        raise

