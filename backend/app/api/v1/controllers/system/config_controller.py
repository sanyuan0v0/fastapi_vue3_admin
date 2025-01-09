# -*- coding: utf-8 -*-

from typing import List
from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.common.request import PaginationService
from app.core.base_params import PaginationQueryParams
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.logger import logger
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.config_schema import ConfigUpdateSchema
from app.api.v1.params.system.config_param import ConfigQueryParams
from app.api.v1.services.system.config_service import ConfigService


router = APIRouter(route_class=OperationLogRoute)


@router.get("/list", summary="查询配置", description="查询配置")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: ConfigQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["system:config:query"])),
) -> JSONResponse:
    result_dict_list = await ConfigService.list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    logger.info(f"{auth.user.name} 查询配置列表成功")
    return SuccessResponse(data=result_dict, msg="查询配置列表成功")

@router.put("/batch", summary="批量修改配置", description="批量修改配置")
async def batch_objs(
        request: Request,
        data: List[ConfigUpdateSchema],
        auth: AuthSchema = Depends(AuthPermission(permissions=["system:config:update"])),
) -> JSONResponse:
    result_list_dict = await ConfigService.batch_services(auth=auth, request=request, data=data)
    logger.info(f"{auth.user.name} 批量更新配置成功 {result_list_dict}")
    return SuccessResponse(data=result_list_dict, msg="批量更新配置成功")

@router.post("/upload", summary="上传文件", dependencies=[Depends(AuthPermission(permissions=["system:config:upload"]))])
async def upload_file(
        file: UploadFile, 
        request: Request
) -> JSONResponse:
    result_str = await ConfigService.upload_services(request=request, file=file)
    logger.info(f"上传文件: {result_str}")
    return SuccessResponse(data=result_str, msg='上传文件成功')

@router.get("/init", summary="获取初始化配置", description="获取初始化配置")
async def get_init_config(
        request: Request,
) -> JSONResponse:
    result_dict = await ConfigService.get_init_config(request=request)
    logger.info(f"获取初始化配置成功 {result_dict}")
    return SuccessResponse(data=result_dict, msg="获取初始化配置成功")
