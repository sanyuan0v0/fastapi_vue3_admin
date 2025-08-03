# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.api.v1.controllers.demo.example_controller import router as ExampleRouter


DemoApiRouter = APIRouter(prefix="/demo")


DemoApiRouter.include_router(router=ExampleRouter, prefix="/example", tags=["示例模块"])
