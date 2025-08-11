# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.api.v1.controllers.common.file_controller import router as FileRouter


FileApiRouter = APIRouter()


FileApiRouter.include_router(router=FileRouter, prefix="/file", tags=["文件模块"])
