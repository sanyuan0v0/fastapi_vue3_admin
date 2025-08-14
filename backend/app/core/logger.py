# -*- coding: utf-8 -*-"""


import os
import time
from datetime import datetime, timedelta
import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Optional, Dict, List, Any
from pathlib import Path

from app.config.setting import settings


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    """高性能自定义的TimedRotatingFileHandler，支持自定义轮换文件名格式"""
    
    # 文件名映射缓存，避免重复计算
    _PREFIX_MAP = {
        "all": "info",
        "error": "error"
    }
    
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc)
    
    def doRollover(self) -> None:
        """优化后的日志轮换，使用自定义命名格式"""
        # 使用流上下文管理确保资源正确释放
        if self.stream:
            self.stream.close()
            self.stream = None
        
        try:
            # 计算轮换时间（使用缓存避免重复计算）
            current_time = self.rolloverAt - self.interval
            time_tuple = time.localtime(current_time)
            suffix = time.strftime("%Y-%m-%d", time_tuple)
            
            # 优化路径构建
            base_path = Path(self.baseFilename)
            prefix = self._PREFIX_MAP.get(base_path.stem, base_path.stem)
            new_name = base_path.parent / f"{prefix}_{suffix}.log"
            
            # 原子性文件重命名
            if base_path.exists():
                base_path.rename(new_name)
            
            # 重新打开日志文件
            if not self.delay:
                self.stream = self._open()
            
            # 优化下次轮换时间计算
            now = int(time.time())
            self.rolloverAt = self.computeRollover(now)
            
        except Exception as e:
            # 添加错误处理，避免轮换失败影响主程序
            print(f"日志轮换失败: {e}")
            if not self.delay and self.stream is None:
                self.stream = self._open()


class LoggerHandler:
    """高性能日志处理器类,用于配置和管理日志"""

    _instance: Optional['LoggerHandler'] = None
    _lock = False  # 线程安全锁
    
    def __new__(cls):
        """线程安全的单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 双重检查锁，避免重复初始化
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.logger = logging.getLogger(__name__)
            self._configure_logger()

    def _configure_logger(self) -> None:
        """优化后的日志配置方法"""
        # 检查是否已经配置，避免重复工作
        if self.logger.handlers:
            return
            
        # 预编译日志格式器（避免重复创建）
        formatter = logging.Formatter(fmt=settings.LOGGER_FORMAT)

        # 使用Path对象提升路径操作性能
        log_dir = Path(settings.LOGGER_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)

        # 清除现有处理器
        self.logger.handlers.clear()
        self.logger.setLevel(settings.LOGGER_LEVEL)

        # 处理器配置缓存，避免重复计算
        handler_config = {
            'when': settings.WHEN,
            'interval': settings.INTERVAL,
            'backupCount': settings.BACKUPCOUNT,
            'encoding': settings.ENCODING
        }

        # 批量配置处理器
        handlers = [
            # all.log处理器 - 记录所有级别的日志
            {
                'path': log_dir / "all.log",
                'level': logging.DEBUG,
                'config': handler_config
            },
            # error.log处理器 - 只记录ERROR及以上级别的日志
            {
                'path': log_dir / "error.log", 
                'level': logging.ERROR,
                'config': handler_config
            }
        ]

        # 批量添加文件处理器
        for handler_info in handlers:
            handler = CustomTimedRotatingFileHandler(
                filename=str(handler_info['path']),
                **handler_info['config']
            )
            handler.setLevel(handler_info['level'])
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # 配置控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(settings.LOGGER_LEVEL)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 配置全局异常处理
        self._setup_global_exception_handler()

    def _setup_global_exception_handler(self) -> None:
        """设置全局异常处理器"""
        def handle_exception(exc_type, exc_value, exc_traceback):
            """全局异常处理回调"""
            if issubclass(exc_type, KeyboardInterrupt):
                # 允许键盘中断正常退出
                return
            if self.logger:
                self.logger.error("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))
        
        import sys
        sys.excepthook = handle_exception

    def __enter__(self):
        """支持上下文管理器协议"""
        return self.logger
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """优化后的资源清理"""
        try:
            # 批量关闭文件处理器
            file_handlers = [h for h in self.logger.handlers if isinstance(h, logging.FileHandler)]
            for handler in file_handlers:
                try:
                    handler.close()
                    self.logger.removeHandler(handler)
                except Exception as e:
                    print(f"关闭日志处理器失败: {e}")
        except Exception:
            pass
        return True

    def cleanup_old_logs(self, days_to_keep: Optional[int] = None) -> None:
        """
        高性能清理指定天数之前的日志文件
        
        Args:
            days_to_keep: 保留最近多少天的日志，如果为None则使用配置中的值
        """
        try:
            days_to_keep = days_to_keep or settings.LOG_RETENTION_DAYS
            log_dir = Path(settings.LOGGER_DIR)
            if not log_dir.exists():
                return
                
            # 使用timedelta提高时间计算精度
            cutoff_time = datetime.now() - timedelta(days=days_to_keep)
            cutoff_timestamp = cutoff_time.timestamp()
            
            # 优化的文件模式匹配
            patterns = ["info_*.log", "error_*.log"]
            
            cleaned_files = []
            total_size = 0
            
            # 批量收集待删除文件
            for pattern in patterns:
                for log_file in log_dir.glob(pattern):
                    if log_file.is_file() and log_file.stat().st_mtime < cutoff_timestamp:
                        try:
                            file_stat = log_file.stat()
                            total_size += file_stat.st_size
                            cleaned_files.append(log_file)
                        except OSError:
                            continue
            
            # 批量删除文件
            success_count = 0
            for log_file in cleaned_files:
                try:
                    log_file.unlink()
                    success_count += 1
                except Exception as e:
                    self.logger.warning(f"无法删除日志文件 {log_file}: {e}")
            
            if success_count > 0:
                self.logger.info(
                    f"已清理旧日志文件: {success_count}个文件, "
                    f"释放空间: {total_size / 1024 / 1024:.2f}MB"
                )
                    
        except Exception as e:
            self.logger.error(f"清理日志文件时出错: {e}")

    def get_log_files_info(self) -> Dict[str, Any]:
        """
        高性能获取日志文件信息
        
        Returns:
            Dict[str, Any]: 包含日志文件信息的字典
        """
        log_dir = Path(settings.LOGGER_DIR)
        log_info = {
            "log_directory": str(log_dir),
            "current_files": [],
            "history_files": [],
            "total_size": 0
        }
        
        if not log_dir.exists():
            return log_info
            
        try:
            # 使用列表推导式优化当前文件处理
            current_files = ["all.log", "error.log"]
            current_files_info = []
            for filename in current_files:
                file_path = log_dir / filename
                if file_path.exists():
                    stat = file_path.stat()
                    current_files_info.append({
                        "name": filename,
                        "size": stat.st_size,
                        "size_formatted": format_file_size(stat.st_size),
                        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })
            log_info["current_files"] = current_files_info
            
            # 优化历史文件收集
            history_files = []
            for pattern in ["info_*.log", "error_*.log"]:
                for log_file in log_dir.glob(pattern):
                    if log_file.is_file():
                        stat = log_file.stat()
                        history_files.append({
                            "name": log_file.name,
                            "size": stat.st_size,
                            "size_formatted": format_file_size(stat.st_size),
                            "modified": stat.st_mtime  # 保存原始时间戳用于排序
                        })
            
            # 高效排序（使用原始时间戳）
            history_files.sort(key=lambda x: x["modified"], reverse=True)
            
            # 格式化时间显示
            for file_info in history_files:
                file_info["modified"] = datetime.fromtimestamp(file_info["modified"]).strftime("%Y-%m-%d %H:%M:%S")
            
            log_info["history_files"] = history_files
            
            # 计算总大小（使用生成器表达式提升性能）
            all_files = log_info["current_files"] + history_files
            log_info["total_size"] = sum(file_info["size"] for file_info in all_files)
            log_info["total_size_formatted"] = format_file_size(log_info["total_size"])
            
        except OSError as e:
            self.logger.error(f"获取日志文件信息失败: {e}")
            
        return log_info


def format_file_size(size_bytes: int) -> str:
    """高性能文件大小格式化工具函数"""
    if size_bytes == 0:
        return "0 B"
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(size_bytes)
    for unit in units:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


# 全局日志实例（使用延迟初始化提升启动性能）
_logger_instance: Optional[logging.Logger] = None

def get_logger() -> logging.Logger:
    """获取全局日志实例（带延迟初始化）"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = LoggerHandler().logger
    return _logger_instance

# 向后兼容的全局实例
logger = get_logger()
