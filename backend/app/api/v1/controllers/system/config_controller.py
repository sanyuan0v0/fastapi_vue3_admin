# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import JSONResponse
from aioredis import Redis

from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission, redis_getter
from app.core.router_class import OperationLogRoute
from app.core.logger import logger
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.config_schema import ConfigUpdateSchema
from app.api.v1.services.system.config_service import ConfigService


router = APIRouter(route_class=OperationLogRoute)


@router.get("/info", summary="获取配置", description="获取配置")
async def get_obj_list_controller(
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:config:query"]))
) -> JSONResponse:
    result_dict = await ConfigService.get_service(auth=auth, id=1)
    logger.info(f"{auth.user.name} 获取配置成功")
    return SuccessResponse(data=result_dict, msg="查询配置列表成功")


@router.put("/update", summary="修改配置", description="修改配置")
async def update_objs_controller(
    data: ConfigUpdateSchema,
    redis: Redis = Depends(redis_getter), 
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:config:update"]))
) -> JSONResponse:
    result_dict = await ConfigService.update_service(auth=auth, redis=redis, data=data)
    logger.info(f"{auth.user.name} 更新配置成功 {result_dict}")
    return SuccessResponse(data=result_dict, msg="更新配置成功")


@router.post("/upload", summary="上传文件", dependencies=[Depends(AuthPermission(permissions=["system:config:upload"]))])
async def upload_file_controller(
    file: UploadFile,
    request: Request
) -> JSONResponse:
    result_str = await ConfigService.upload_service(base_url=str(request.base_url), file=file)
    logger.info(f"上传文件: {result_str}")
    return SuccessResponse(data=result_str, msg='上传文件成功')


@router.get("/init", summary="获取初始化配置", description="获取初始化配置")
async def get_init_config_controller(
    redis: Redis = Depends(redis_getter)
) -> JSONResponse:
    result_dict = await ConfigService.get_init_config_service(redis=redis)
    logger.info(f"获取初始化配置成功 {result_dict}")
    return SuccessResponse(data=result_dict, msg="获取初始化配置成功")
