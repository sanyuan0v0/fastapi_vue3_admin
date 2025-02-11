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
from app.api.v1.params.autotest.module_param import ModuleQueryParams
from app.api.v1.services.autotest.module_service import ModuleService
from app.api.v1.schemas.autotest.module_schema import ModuleCreateSchema, ModuleUpdateSchema


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail", summary="获取模块详情", description="获取模块详情")
async def get_obj_detail(
        id: int = Query(..., description="模块ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:module:query"])),
) -> JSONResponse:
    result_dict = await ModuleService.get_detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取模块详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取模块详情成功")

@router.get("/list", summary="查询模块", description="查询模块")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: ModuleQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:module:query"])),
) -> JSONResponse:
    result_dict_list = await ModuleService.get_list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"{auth.user.name} 查询模块列表成功")
    return SuccessResponse(data=result_dict, msg="查询模块列表成功")

@router.post("/create", summary="创建模块", description="创建模块")
async def create_obj(
        data: ModuleCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:module:create"])),
) -> JSONResponse:
    result_dict = await ModuleService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建模块成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建模块成功")

@router.put("/update", summary="修改模块", description="修改模块")
async def update_obj(
        data: ModuleUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:module:update"])),
) -> JSONResponse:
    result_dict = await ModuleService.update_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 修改模块成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改模块成功")

@router.delete("/delete", summary="删除模块", description="删除模块")
async def delete_obj(
        id: int = Query(..., description="模块ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:module:delete"])),
) -> JSONResponse:
    await ModuleService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除模块成功: {id}")
    return SuccessResponse(msg="删除模块成功")
