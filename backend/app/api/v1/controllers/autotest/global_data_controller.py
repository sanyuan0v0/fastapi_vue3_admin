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
from app.api.v1.params.autotest.global_data_param import GlobalDataQueryParams
from app.api.v1.services.autotest.global_data_service import GlobalDataService
from app.api.v1.schemas.autotest.global_data_schema import GlobalDataCreateSchema, GlobalDataUpdateSchema


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail", summary="获取全局参数详情", description="获取全局参数详情")
async def get_obj_detail(
        id: int = Query(..., description="全局参数ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:globaldata:query"])),
) -> JSONResponse:
    result_dict = await GlobalDataService.get_detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取全局参数详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取全局参数详情成功")

@router.get("/list", summary="查询全局参数", description="查询全局参数")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: GlobalDataQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:globaldata:query"])),
) -> JSONResponse:
    result_dict_list = await GlobalDataService.get_list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"{auth.user.name} 查询全局参数列表成功")
    return SuccessResponse(data=result_dict, msg="查询全局参数列表成功")

@router.post("/create", summary="创建全局参数", description="创建全局参数")
async def create_obj(
        data: GlobalDataCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:globaldata:create"])),
) -> JSONResponse:
    result_dict = await GlobalDataService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建全局参数成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建全局参数成功")

@router.put("/update", summary="修改全局参数", description="修改全局参数")
async def update_obj(
        data: GlobalDataUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:globaldata:update"])),
) -> JSONResponse:
    result_dict = await GlobalDataService.update_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 修改全局参数成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改全局参数成功")

@router.delete("/delete", summary="删除全局参数", description="删除全局参数")
async def delete_obj(
        id: int = Query(..., description="全局参数ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:globaldata:delete"])),
) -> JSONResponse:
    await GlobalDataService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除全局参数成功: {id}")
    return SuccessResponse(msg="删除全局参数成功")
