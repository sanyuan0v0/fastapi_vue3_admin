# -*- coding: utf-8 -*-

import uvicorn
import typer
from fastapi import FastAPI

from app.config.setting import settings
from app.plugin.init_app import (
    register_middlewares,
    register_exceptions,
    register_routers,
    register_files,
    reset_api_docs,
    lifespan
)
from app.core.logger import logger


shell_app = typer.Typer()


def create_app() -> FastAPI:
    # 创建FastAPI应用
    app = FastAPI(**settings.get_backend_app_attributes, lifespan=lifespan)

    # 注册异常处理器
    register_exceptions(app)
    # 注册中间件
    register_middlewares(app)
    # 注册路由
    register_routers(app)
    # 注册静态文件
    register_files(app)
    # 重设API文档
    reset_api_docs(app)

    return app


@shell_app.command()
def run():
    logger.info(settings.BANNER)
    # 启动uvicorn服务
    uvicorn.run(
        app='main:create_app',
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
        log_config=settings.LOGGING_CONFIG,
        workers=settings.WORKERS,
        limit_concurrency=settings.LIMIT_CONCURRENCY,
        backlog=settings.BACKLOG,
        limit_max_requests=settings.LIMIT_MAX_REQUESTS,
        timeout_keep_alive=settings.TIMEOUT_KEEP_ALIVE,
        lifespan=settings.LIFESPAN,
        factory=settings.FACTORY,
    )


"""
初始化数据命令。

该命令用于初始化项目数据。通过调用 `InitializeData` 类的 `run` 方法，并使用 `asyncio.run` 来异步执行数据初始化过程。
"""


@shell_app.command()
def init():
    import asyncio
    from app.scripts.initialize import InitializeData
    # 初始化数据
    data = InitializeData()
    # 使用asyncio.run来运行异步函数
    asyncio.run(data.run())

# @shell_app.command()
# def migrate(env: Environment = Environment.pro):
#     """
#     将模型迁移到数据库，更新数据库表结构

#     :param env: 数据库环境
#     """
#     print("开始更新数据库表")
#     data = InitializeData()
#     data.migrate_model(env)


if __name__ == '__main__':
    # 启动服务
    # 方式一：
    # uvicorn main:create_app --host 0.0.0.0 --port 8000 --factory --workers 4
    # 方式二：
    # python main.py run    # 启动服务
    # python main.py init   # 初始化数据
    # 方式三：
    # gunicorn -c gunicorn.py main:create_app
    shell_app()
