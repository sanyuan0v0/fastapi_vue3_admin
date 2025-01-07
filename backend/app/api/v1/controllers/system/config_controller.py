# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.common.request import PaginationService
from app.core.base_params import PaginationQueryParams
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.logger import logger
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.config_schema import ConfigCreateSchema, ConfigUpdateSchema
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


@router.post("/create", summary="创建配置", description="创建配置")
async def create_obj(
        data: ConfigCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["system:config:create"])),
) -> JSONResponse:
    result_dict = await ConfigService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建配置成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建配置成功")


@router.put("/update", summary="修改配置", description="修改配置")
async def update_obj(
        data: ConfigUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["system:config:update"])),
) -> JSONResponse:
    result_dict = await ConfigService.update_services(auth=auth, id=data.id, data=data)
    logger.info(f"{auth.user.name} 修改配置成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改配置成功")


@router.delete("/delete", summary="删除配置", description="删除配置")
async def delete_obj(
        id: int = Query(..., description="配置ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["system:config:delete"])),
) -> JSONResponse:
    await ConfigService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除配置成功: {id}")
    return SuccessResponse(msg="删除配置成功")


@router.get("/detail", summary="获取配置详情", description="获取配置详情")
async def get_obj_detail(
        id: int = Query(..., description="配置ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["system:config:query"])),
) -> JSONResponse:
    result_dict = await ConfigService.detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取配置详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取配置详情成功")
