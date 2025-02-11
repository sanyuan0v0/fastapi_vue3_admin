# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParams
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.logger import logger
from app.common.request import PaginationService
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.params.autotest.notification_config_param import NotificationConfigQueryParams
from app.api.v1.services.autotest.notification_config_service import NotificationConfigService
from app.api.v1.schemas.autotest.notification_config_schema import NotificationConfigCreateSchema, NotificationConfigUpdateSchema


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail", summary="获取通知配置详情", description="获取通知配置详情")
async def get_obj_detail(
        id: int = Query(..., description="通知配置ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:notificationconfig:query"])),
) -> JSONResponse:
    result_dict = await NotificationConfigService.get_detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取通知配置详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取通知配置详情成功")

@router.get("/list", summary="查询通知配置", description="查询通知配置")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: NotificationConfigQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:notificationconfig:query"])),
) -> JSONResponse:
    result_dict_list = await NotificationConfigService.get_list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"{auth.user.name} 查询通知配置列表成功")
    return SuccessResponse(data=result_dict, msg="查询通知配置列表成功")

@router.post("/create", summary="创建通知配置", description="创建通知配置")
async def create_obj(
        data: NotificationConfigCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:notificationconfig:create"])),
) -> JSONResponse:
    result_dict = await NotificationConfigService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建通知配置成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建通知配置成功")

@router.put("/update", summary="修改通知配置", description="修改通知配置")
async def update_obj(
        data: NotificationConfigUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:notificationconfig:update"])),
) -> JSONResponse:
    result_dict = await NotificationConfigService.update_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 修改通知配置成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改通知配置成功")

@router.delete("/delete", summary="删除通知配置", description="删除通知配置")
async def delete_obj(
        id: int = Query(..., description="通知配置ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:notificationconfig:delete"])),
) -> JSONResponse:
    await NotificationConfigService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除通知配置成功: {id}")
    return SuccessResponse(msg="删除通知配置成功")
