# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.api.v1.controllers.autotest.case_controller import router as CaseRouter
from app.api.v1.controllers.autotest.task_controller import router as TaskRouter
from app.api.v1.controllers.autotest.project_controller import router as ProjectRouter


AutoTestApiRouter = APIRouter(prefix="/autotest")


AutoTestApiRouter.include_router(router=ProjectRouter, prefix="/project", tags=["项目模块"])
AutoTestApiRouter.include_router(router=CaseRouter, prefix="/case", tags=["用例模块"])
AutoTestApiRouter.include_router(router=TaskRouter, prefix="/task", tags=["任务模块"])
