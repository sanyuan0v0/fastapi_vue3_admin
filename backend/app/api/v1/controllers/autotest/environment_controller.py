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
from app.api.v1.params.autotest.environment_param import EnvironmentQueryParams
from app.api.v1.services.autotest.environment_service import EnvironmentService
from app.api.v1.schemas.autotest.environment_schema import EnvironmentCreateSchema, EnvironmentUpdateSchema


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail", summary="获取环境详情", description="获取环境详情")
async def get_obj_detail(
        id: int = Query(..., description="环境ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:environment:query"])),
) -> JSONResponse:
    result_dict = await EnvironmentService.get_detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取环境详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取环境详情成功")

@router.get("/list", summary="查询环境", description="查询环境")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: EnvironmentQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:environment:query"])),
) -> JSONResponse:
    result_dict_list = await EnvironmentService.get_list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"{auth.user.name} 查询环境列表成功")
    return SuccessResponse(data=result_dict, msg="查询环境列表成功")

@router.post("/create", summary="创建环境", description="创建环境")
async def create_obj(
        data: EnvironmentCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:environment:create"])),
) -> JSONResponse:
    result_dict = await EnvironmentService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建环境成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建环境成功")

@router.put("/update", summary="修改环境", description="修改环境")
async def update_obj(
        data: EnvironmentUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:environment:update"])),
) -> JSONResponse:
    result_dict = await EnvironmentService.update_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 修改环境成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改环境成功")

@router.delete("/delete", summary="删除环境", description="删除环境")
async def delete_obj(
        id: int = Query(..., description="环境ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:environment:delete"])),
) -> JSONResponse:
    await EnvironmentService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除环境成功: {id}")
    return SuccessResponse(msg="删除环境成功")
