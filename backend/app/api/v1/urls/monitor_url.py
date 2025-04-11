# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.api.v1.controllers.monitor.cache_controller import router as CacheRouter
from app.api.v1.controllers.monitor.online_controller import router as OnlineRouter
from app.api.v1.controllers.monitor.server_controller import router as ServerRouter



MonitorApiRouter = APIRouter(prefix="/monitor")


MonitorApiRouter.include_router(router=CacheRouter, prefix="/cache", tags=["缓存模块"])
MonitorApiRouter.include_router(router=OnlineRouter,  prefix="/online",  tags=["在线用户模块"])
MonitorApiRouter.include_router(router=ServerRouter, prefix="/server", tags=["服务器模块"])