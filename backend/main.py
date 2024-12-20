# -*- coding: utf-8 -*-

import os
import uvicorn
import typer
from fastapi import FastAPI

from app.common.enums import Environment

shell_app = typer.Typer()


def create_app() -> FastAPI:
    
    from app.config.setting import settings
    from app.plugin.init_app import (
    register_middlewares,
    register_exceptions,
    register_routers,
    register_files,
    reset_api_docs,
    lifespan
)
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
def run(env: Environment = typer.Option(Environment.DEV, "--env", help="运行环境 (dev, test, prod)")):
    # 设置环境变量
    os.environ["ENVIRONMENT"] = env.value
    from app.config.setting import settings
    
    # 启动uvicorn服务
    uvicorn.run(
        app='main:create_app',
        **settings.get_uvicorn_config
    )

@shell_app.command()
def init():
    import asyncio
    from app.scripts.initialize import InitializeData
    # 初始化数据
    data = InitializeData()
    # 使用asyncio.run来运行异步函数
    asyncio.run(data.run())


if __name__ == '__main__':
    # 启动服务
    # 方式一：
    # uvicorn main:create_app --host 0.0.0.0 --port 8000 --factory --workers 4
    # 方式二：
    # python main.py run    # 启动服务
    # python3 main.py run --env=dev
    # python main.py init   # 初始化数据
    # 方式三：(linux部署使用)
    # gunicorn -c gunicorn.py main:create_app
    shell_app()
