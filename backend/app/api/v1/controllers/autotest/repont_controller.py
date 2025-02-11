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
from app.api.v1.params.autotest.repont_param import ReportQueryParams
from app.api.v1.services.autotest.repont_service import ReportService
from app.api.v1.schemas.autotest.repont_schema import ReportCreateSchema, ReportUpdateSchema


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail", summary="获取报告详情", description="获取报告详情")
async def get_obj_detail(
        id: int = Query(..., description="报告ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:report:query"])),
) -> JSONResponse:
    result_dict = await ReportService.get_detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取报告详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取报告详情成功")

@router.get("/list", summary="查询报告", description="查询报告")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: ReportQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:report:query"])),
) -> JSONResponse:
    result_dict_list = await ReportService.get_list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"{auth.user.name} 查询报告列表成功")
    return SuccessResponse(data=result_dict, msg="查询报告列表成功")

@router.post("/create", summary="创建报告", description="创建报告")
async def create_obj(
        data: ReportCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:report:create"])),
) -> JSONResponse:
    result_dict = await ReportService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建报告成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建报告成功")

@router.put("/update", summary="修改报告", description="修改报告")
async def update_obj(
        data: ReportUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:report:update"])),
) -> JSONResponse:
    result_dict = await ReportService.update_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 修改报告成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改报告成功")

@router.delete("/delete", summary="删除报告", description="删除报告")
async def delete_obj(
        id: int = Query(..., description="报告ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:report:delete"])),
) -> JSONResponse:
    await ReportService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除报告成功: {id}")
    return SuccessResponse(msg="删除报告成功")
