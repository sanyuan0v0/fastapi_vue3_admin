# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.api.v1.controllers.autotest.api_case_controller import router as APICaseRouter
from app.api.v1.controllers.autotest.environment_controller import router as EnvironmentRouter
from app.api.v1.controllers.autotest.task_controller import router as TaskRouter
from app.api.v1.controllers.autotest.global_data_controller import router as GlobalDataRouter
from app.api.v1.controllers.autotest.module_controller import router as ModuleRouter
from app.api.v1.controllers.autotest.notification_config_controller import router as NotificationConfigRouter
from app.api.v1.controllers.autotest.project_controller import router as ProjectRouter
from app.api.v1.controllers.autotest.repont_controller import router as ReportRouter
from app.api.v1.controllers.autotest.suite_controller import router as SuiteRouter


AutoTestApiRouter = APIRouter(prefix="/autotest")


AutoTestApiRouter.include_router(router=ProjectRouter, prefix="/project", tags=["项目模块"])
AutoTestApiRouter.include_router(router=EnvironmentRouter, prefix="/environment", tags=["环境模块"])
AutoTestApiRouter.include_router(router=NotificationConfigRouter, prefix="/notificationconfig", tags=["通知配置模块"])
AutoTestApiRouter.include_router(router=GlobalDataRouter, prefix="/globaldata", tags=["全局数据模块"])
AutoTestApiRouter.include_router(router=ModuleRouter, prefix="/module", tags=["所属模块"])
AutoTestApiRouter.include_router(router=APICaseRouter, prefix="/apicase", tags=["接口用例模块"])
AutoTestApiRouter.include_router(router=SuiteRouter, prefix="/suite", tags=["套件模块"])
AutoTestApiRouter.include_router(router=TaskRouter, prefix="/task", tags=["任务模块"])
AutoTestApiRouter.include_router(router=ReportRouter, prefix="/report", tags=["报告模块"])
