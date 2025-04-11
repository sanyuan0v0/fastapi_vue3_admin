# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.api.v1.controllers.system.auth_controller import router as AuthRouter
from app.api.v1.controllers.system.menu_controller import router as MenuRouter
from app.api.v1.controllers.system.dept_controller import router as DeptRouter
from app.api.v1.controllers.system.role_controller import router as RoleRouter
from app.api.v1.controllers.system.user_controller import router as UserRouter
from app.api.v1.controllers.system.operation_log_controller import router as LogRouter
from app.api.v1.controllers.system.position_controller import router as PositionRouter
from app.api.v1.controllers.system.notice_controller import router as NoticeRouter
from app.api.v1.controllers.system.config_controller import router as ConfigRouter
from app.api.v1.controllers.system.dict_controller import router as DictRouter
from app.api.v1.controllers.system.job_controller import router as JobRouter

SystemApiRouter = APIRouter(prefix="/system")

SystemApiRouter.include_router(router=AuthRouter, prefix="/auth", tags=["系统认证"])
SystemApiRouter.include_router(router=MenuRouter, prefix="/menu", tags=["菜单模块"])
SystemApiRouter.include_router(router=DeptRouter, prefix="/dept", tags=["部门模块"])
SystemApiRouter.include_router(router=RoleRouter, prefix="/role", tags=["角色模块"])
SystemApiRouter.include_router(router=UserRouter, prefix="/user", tags=["用户模块"])
SystemApiRouter.include_router(router=LogRouter,  prefix="/log",  tags=["日志模块"])
SystemApiRouter.include_router(router=PositionRouter, prefix="/position", tags=["岗位模块"])
SystemApiRouter.include_router(router=NoticeRouter, prefix="/notice", tags=["通知模块"])
SystemApiRouter.include_router(router=ConfigRouter, prefix="/config", tags=["配置模块"])
SystemApiRouter.include_router(router=DictRouter, prefix="/dict", tags=["字典模块"])
SystemApiRouter.include_router(router=JobRouter, prefix="/job", tags=["任务模块"])
