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
from app.api.v1.params.autotest.suite_param import SuiteQueryParams
from app.api.v1.services.autotest.suite_service import SuiteService
from app.api.v1.schemas.autotest.suite_schema import SuiteCreateSchema, SuiteUpdateSchema


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail", summary="获取套件详情", description="获取套件详情")
async def get_obj_detail(
        id: int = Query(..., description="套件ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:suite:query"])),
) -> JSONResponse:
    result_dict = await SuiteService.get_detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取套件详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取套件详情成功")

@router.get("/list", summary="查询套件", description="查询套件")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: SuiteQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:suite:query"])),
) -> JSONResponse:
    result_dict_list = await SuiteService.get_list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"{auth.user.name} 查询套件列表成功")
    return SuccessResponse(data=result_dict, msg="查询套件列表成功")

@router.post("/create", summary="创建套件", description="创建套件")
async def create_obj(
        data: SuiteCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:suite:create"])),
) -> JSONResponse:
    result_dict = await SuiteService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建套件成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建套件成功")

@router.put("/update", summary="修改套件", description="修改套件")
async def update_obj(
        data: SuiteUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:suite:update"])),
) -> JSONResponse:
    result_dict = await SuiteService.update_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 修改套件成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改套件成功")

@router.delete("/delete", summary="删除套件", description="删除套件")
async def delete_obj(
        id: int = Query(..., description="套件ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:suite:delete"])),
) -> JSONResponse:
    await SuiteService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除套件成功: {id}")
    return SuccessResponse(msg="删除套件成功")
