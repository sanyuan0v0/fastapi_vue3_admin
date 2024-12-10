# -*- coding: utf-8 -*-

from fastapi import APIRouter
from app.api.v1.controllers.common.common_controller import router as CommonRouter


CommonApiRouter = APIRouter(prefix="/common")


CommonApiRouter.include_router(router=CommonRouter, prefix="/file", tags=["文件模块"])