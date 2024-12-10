# -*- coding: utf-8 -*-

from datetime import date
from functools import lru_cache
import os
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Union
from pydantic import MongoDsn, RedisDsn
from pydantic_settings import BaseSettings
from sqlalchemy import URL
from uvicorn.config import LifespanType


class Settings(BaseSettings):
    """系统配置类"""

    BANNER: ClassVar[str] = """
     ______        _                  _ 
    |  ____|      | |     /\         (_)
    | |__ __ _ ___| |_   /  \   _ __  _ 
    |  __/ _` / __| __| / /\ \ | '_ \| |
    | | | (_| \__ \ |_ / ____ \| |_) | |
    |_|  \__,_|___/\__/_/    \_\ .__/|_|
                               | |      
                               |_|
    """
    # ================================================= #
    # ******************* 项目配置 ****************** #
    # ================================================= #
    # 项目根目录
    BASE_DIR: Path = Path(__file__).parent.parent.parent

    # 服务器配置
    SERVER_HOST: str = 'localhost'  # 允许访问的IP地址
    SERVER_PORT: int = 8000  # 服务端口
    RELOAD: bool = True  # 是否自动重启
    WORKERS: int = 1  # 启动进程数
    FACTORY: bool = True  # 是否使用异步模式
    LIMIT_CONCURRENCY: int = 1000  # 最大并发连接数
    BACKLOG: int = 2048  # 等待队列最大连接数
    LIMIT_MAX_REQUESTS: int = 4094  # HTTP最大请求数
    TIMEOUT_KEEP_ALIVE: int = 5  # 保持连接时间(秒)
    LIFESPAN: LifespanType = "on"  # 生命周期模式

    # ================================================= #
    # ******************* API文档配置 ****************** #
    # ================================================= #
    DEBUG: bool = True  # 调试模式
    TITLE: str = "🎉 Fastapi Vue Admin 🎉"  # 文档标题
    VERSION: str = '0.1.0'  # 版本号
    DESCRIPTION: str = "该项目是一个基于python的web服务框架，基于fastapi和sqlalchemy实现。"  # 文档描述
    SUMMARY: str | None = "接口汇总"  # 文档概述
    DOCS_URL: str | None = "/docs"  # Swagger UI路径
    REDOC_URL: str | None = "/redoc"  # ReDoc路径
    ROOT_PATH: str = "/api/v1"  # API路由前缀

    # ================================================= #
    # ******************** 跨域配置 ******************** #
    # ================================================= #
    CORS_ORIGIN_ENABLE: bool = True  # 是否启用跨域
    ALLOW_ORIGINS: List[str] = ["*"]  # 允许的域名列表
    ALLOW_METHODS: List[str] = ["*"]  # 允许的HTTP方法
    ALLOW_HEADERS: List[str] = ["*"]  # 允许的请求头
    ALLOW_CREDENTIALS: bool = True  # 是否允许携带cookie

    # ================================================= #
    # ******************* 登录认证配置 ****************** #
    # ================================================= #
    SECRET_KEY: str = "vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=krylxcjq75vzps$"  # JWT密钥
    ALGORITHM: str = "HS256"  # JWT算法
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # access_token过期时间(分钟)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # refresh_token过期时间(分钟)
    TOKEN_TYPE: str = "bearer"  # token类型
    JWT_REDIS_EXPIRE_MINUTES: int = 30  # redis缓存过期时间(分钟)

    # ================================================= #
    # ***************** 演示模型配置 ***************** #
    # ================================================= #
    DEMO_ENABLE: bool = False  # 是否开启演示模式
    DEMO_WHITE_LIST_PATH: List[str] = [  # 演示白名单
        "/system/auth/login",
        "/system/auth/token/refresh",
        "/system/auth/captcha/get"
    ]
    DEMO_BLACK_LIST_PATH: List[str] = [  # 演示黑名单
        "/auth/login"
    ]

    # ================================================= #
    # ***************** 静态文件配置 ***************** #
    # ================================================= #
    STATIC_ENABLE: bool = True  # 是否启用静态文件
    STATIC_URL: str = "/static"  # 访问路由
    STATIC_DIR: str = "static"  # 目录名
    STATIC_ROOT: Path = BASE_DIR.joinpath(STATIC_DIR)  # 绝对路径

    # ================================================= #
    # ***************** 模板文件配置 ***************** #
    # ================================================= #
    TEMPLATES_ENABLE: bool = True  # 是否启用模板
    TEMPLATES_URL: str = "/templates"  # 访问路由
    TEMPLATES_DIR: str = "templates"  # 目录名
    TEMPLATES_ROOT: Path = BASE_DIR.joinpath(TEMPLATES_DIR)  # 绝对路径
    
    # ================================================= #
    # ******************* 临时文件配置 ******************* #
    # ================================================= #
    UPLOAD_PROFILE_PATH: Path = 'static/upload'
    UPLOAD_FILE_PATH: Path = STATIC_ROOT.joinpath('upload')  # 上传目录
    DOWNLOAD_FILE_PATH: Path = STATIC_ROOT.joinpath('download')  # 下载目录
    UPLOAD_MACHINE: str = 'A'  # 上传机器标识
    ALLOWED_EXTENSIONS: list[str] = [  # 允许的文件类型
        # 图片
        '.bmp', '.gif', '.jpg', '.jpeg', '.png', '.ico',
        # 文档
        '.csv', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.html', '.htm', '.txt', '.pdf',
        # 压缩包
        '.rar', '.zip', '.gz', '.bz2',
        # 视频
        '.mp4', '.avi', '.rmvb'
    ]
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 最大文件大小(10MB)

    # ================================================= #
    # ******************** 缓存配置 ******************* #
    # ================================================= #
    CACHE_ENABLE: bool = True  # 是否启用缓存
    CACHES_DIR: Path = 'static/caches'  # 缓存目录
    CACHE_EXPIRE_SECONDS: int = 300  # 缓存过期时间(秒)
    
    # ================================================= #
    # ***************** Swagger配置 ***************** #
    # ================================================= #
    SWAGGER_CSS_URL: Path = "static/swagger/swagger-ui/swagger-ui.css"
    SWAGGER_JS_URL: Path = "static/swagger/swagger-ui/swagger-ui-bundle.js"
    REDOC_JS_URL: Path = "static/swagger/redoc/bundles/redoc.standalone.js"
    FAVICON_URL: Path = "static/swagger/favicon.png"

    # ================================================= #
    # ******************** 数据库配置 ******************* #
    # ================================================= #
    SQL_DB_ENABLE: bool = True  # 是否启用数据库
    DATABASE_ECHO: bool = False  # 是否显示SQL日志
    ECHO_POOL: bool = False  # 是否显示连接池日志
    POOL_SIZE: int = 20  # 连接池大小
    MAX_OVERFLOW: int = 10  # 最大溢出连接数
    POOL_TIMEOUT: int = 30  # 连接超时时间(秒)
    POOL_RECYCLE: int = 1800  # 连接回收时间(秒)
    POOL_PRE_PING: bool = True  # 是否开启连接预检
    FUTURE: bool = True  # 是否使用SQLAlchemy 2.0特性
    AUTOCOMMIT: bool = False  # 是否自动提交
    AUTOFETCH: bool = False  # 是否自动获取
    EXPIRE_ON_COMMIT: bool = False  # 是否在提交时过期
    # SQLite数据库连接
    SQLALCHEMY_DATABASE_URI: str | URL = f"sqlite+aiosqlite:///{BASE_DIR.joinpath('dev_sql.db')}?characterEncoding=UTF-8"
    # MySQL数据库连接
    # SQLALCHEMY_DATABASE_URI: str | URL = f"mysql+asyncmy://root:123456@localhost:3306/fastapi_vue_admin?charset=utf8mb4"
    # PostgreSQL数据库连接
    # SQLALCHEMY_DATABASE_URI: str | URL = f"postgresql+asyncpg://postgres:123456@localhost:5432/fastapi_vue_admin"

    # ================================================= #
    # ******************** MongoDB配置 ******************* #
    # ================================================= #
    MONGO_DB_ENABLE: bool = True  # 是否启用MongoDB
    MONGO_DB_NAME: str = 'fastapi_vue_admin'  # 数据库名
    # 连接地址
    MONGO_DB_URL: MongoDsn = f"mongodb://localhost:27017/{MONGO_DB_NAME}"

    # ================================================= #
    # ******************** Redis配置 ******************* #
    # ================================================= #
    REDIS_ENABLE: bool = True  # 是否启用Redis
    REDIS_URL: RedisDsn = f"redis://localhost:6379/1"

    # ================================================= #
    # ******************** 验证码配置 ******************* #
    # ================================================= #
    CAPTCHA_ENABLE: bool = True  # 是否启用验证码
    CAPTCHA_EXPIRE_SECONDS: int = 60  # 验证码过期时间(秒)
    CAPTCHA_FONT_PATH: Path = 'static/assets/font/Arial.ttf'  # 字体路径
    CAPTCHA_FONT_SIZE: int = 40

    # ================================================= #
    # ********************* 日志配置 ******************* #
    # ================================================= #
    LOGGER_NAME: str = date.today().strftime(r'%Y-%m-%d.log')  # 日志文件名
    LOGGER_FILEPATH: Path = BASE_DIR.joinpath('logs', LOGGER_NAME)  # 日志文件路径
    BACKUPCOUNT: int = 10  # 日志文件备份数
    WHEN: str = 'MIDNIGHT'  # 日志分割时间
    INTERVAL: int = 1  # 日志分割间隔
    ENCODING: str = 'utf-8'  # 日志编码
    LOGGER_LEVEL: str = 'INFO'  # 日志级别
    # 日志格式
    LOGGER_FORMAT: str = '%(asctime)s - %(levelname)s - [%(name)s:%(filename)s:%(funcName)s:%(lineno)d] %(message)s'

    # 日志配置字典
    LOGGING_CONFIG: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": LOGGER_FORMAT,
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": LOGGER_FORMAT,
            },
        },
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access_console": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "formatter": "default",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": LOGGER_FILEPATH,
                "when": WHEN,
                "backupCount": BACKUPCOUNT,
                "encoding": ENCODING,
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["file", "console"], "level": LOGGER_LEVEL, "propagate": False},
            "uvicorn.error": {"handlers": ["file", "console"], "level": LOGGER_LEVEL, "propagate": False},
            "uvicorn.access": {"handlers": ["file", "access_console"], "level": LOGGER_LEVEL, "propagate": False},
        },
    }

    REQUEST_LOG_RECORD: bool = True  # 是否记录请求日志
    OPERATION_LOG_RECORD: bool = True  # 是否记录操作日志
    OPERATION_RECORD_METHOD: List[str] = ["POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]  # 需要记录的请求方法
    IGNORE_OPERATION_FUNCTION: List[str] = ["get_captcha_for_login"]  # 忽略记录的函数

    # ================================================= #
    # ******************* Gzip压缩配置 ******************* #
    # ================================================= #
    GZIP_ENABLE: bool = True  # 是否启用Gzip
    GZIP_MIN_SIZE: int = 1000  # 最小压缩大小(字节)
    GZIP_COMPRESS_LEVEL: int = 9  # 压缩级别(1-9)

    # ================================================= #
    # ******************* 初始化数据 ****************** #
    # ================================================= #
    SCRIPT_DIR: Path = 'app/scripts/data'  # 管理员路由目录

    # ================================================= #
    # ******************* 其他配置 ******************* #
    # ================================================= #
    # 中间件列表
    MIDDLEWARES: List[Optional[str]] = [
        "app.core.middlewares.CustomCORSMiddleware" if CORS_ORIGIN_ENABLE else None,
        "app.core.middlewares.RequestLogMiddleware" if REQUEST_LOG_RECORD else None,
        "app.core.middlewares.CustomGZipMiddleware" if GZIP_ENABLE else None,
        "app.core.middlewares.DemoEnvMiddleware" if DEMO_ENABLE else None,
    ]

    # 事件列表
    EVENTS: List[Optional[str]] = [
        # "app.core.database.mongodb_connect" if MONGO_DB_ENABLE else None,
        "app.core.database.redis_connect" if REDIS_ENABLE else None,
    ]

    @property
    def get_backend_app_attributes(self) -> Dict[str, Union[str, bool, None]]:
        """获取FastAPI应用属性"""
        return {
            "debug": self.DEBUG,
            "title": self.TITLE,
            "version": self.VERSION,
            "description": self.DESCRIPTION,
            "summary": self.SUMMARY,
            "docs_url": None,
            "redoc_url": None,
            "root_path": self.ROOT_PATH
        }

    @property
    def get_cors_middleware_attributes(self) -> Dict[str, Union[List[str], bool]]:
        """获取CORS中间件属性"""
        return {
            "allow_origins": self.ALLOW_ORIGINS,
            "allow_methods": self.ALLOW_METHODS,
            "allow_headers": self.ALLOW_HEADERS,
            "allow_credentials": self.ALLOW_CREDENTIALS
        }

    class Config:
        """配置类"""
        env_file = ".env"  # 环境变量文件
        env_file_encoding = "utf-8"  # 环境变量文件编码
        case_sensitive = True  # 大小写敏感


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """获取配置"""
    env = os.getenv("ENVIRONMENT", "dev")  # 获取环境变量 dev
    env_file = f".env.{env}"  # 环境变量文件 .env.dev
    return Settings(_env_file=env_file)  # 加载对应环境的配置文件


settings = get_settings()
