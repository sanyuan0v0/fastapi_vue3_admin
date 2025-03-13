# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

from app.config.setting import settings


class LoggerHandler:
    """日志处理器类,用于配置和管理日志"""

    _instance: Optional['LoggerHandler'] = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(__name__)
            self._configure_logger()

    def _configure_logger(self):
        """配置日志处理器"""
        try:
            # 清除现有处理器
            self.logger.handlers.clear()

            # 设置日志级别
            self.logger.setLevel(settings.LOGGER_LEVEL)

            # 创建日志格式器
            formatter = logging.Formatter(fmt=settings.LOGGER_FORMAT)

            # 确保日志目录存在
            settings.LOGGER_FILEPATH.parent.mkdir(parents=True, exist_ok=True)

            # 配置文件处理器
            file_handler = TimedRotatingFileHandler(
                filename=settings.LOGGER_FILEPATH,
                when=settings.WHEN,
                interval=settings.INTERVAL,
                backupCount=settings.BACKUPCOUNT,
                encoding=settings.ENCODING
            )
            file_handler.setLevel(settings.LOGGER_LEVEL)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # 配置控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(settings.LOGGER_LEVEL)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        except Exception as e:
            self.logger.error(f"日志配置失败: {e}")

    def __enter__(self):
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """关闭并清理文件处理器"""
        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                self.logger.removeHandler(handler)
        return True


# 全局日志实例
logger = LoggerHandler().logger
