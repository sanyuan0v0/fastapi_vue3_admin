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
from app.api.v1.params.autotest.api_case_param import APICaseQueryParams
from app.api.v1.services.autotest.api_case_service import APICaseService
from app.api.v1.schemas.autotest.api_case_schema import APICaseCreateSchema, APICaseUpdateSchema


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail", summary="获取接口用例详情", description="获取接口用例详情")
async def get_obj_detail(
        id: int = Query(..., description="接口用例ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:apicase:query"])),
) -> JSONResponse:
    result_dict = await APICaseService.get_detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取接口用例详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取接口用例详情成功")

@router.get("/list", summary="查询接口用例", description="查询接口用例")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: APICaseQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:apicase:query"])),
) -> JSONResponse:
    result_dict_list = await APICaseService.get_list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"{auth.user.name} 查询接口用例列表成功")
    return SuccessResponse(data=result_dict, msg="查询接口用例列表成功")

@router.post("/create", summary="创建接口用例", description="创建接口用例")
async def create_obj(
        data: APICaseCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:apicase:create"])),
) -> JSONResponse:
    result_dict = await APICaseService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建接口用例成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建接口用例成功")

@router.put("/update", summary="修改接口用例", description="修改接口用例")
async def update_obj(
        data: APICaseUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:apicase:update"])),
) -> JSONResponse:
    result_dict = await APICaseService.update_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 修改接口用例成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改接口用例成功")

@router.delete("/delete", summary="删除接口用例", description="删除接口用例")
async def delete_obj(
        id: int = Query(..., description="接口用例ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:apicase:delete"])),
) -> JSONResponse:
    await APICaseService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除接口用例成功: {id}")
    return SuccessResponse(msg="删除接口用例成功")
