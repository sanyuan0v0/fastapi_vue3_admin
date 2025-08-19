# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParams
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.logger import logger
from app.common.request import PaginationService
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.params.stock.spot_param import SpotQueryParams
from app.api.v1.services.stock.spot_service import SpotService


router = APIRouter(route_class=OperationLogRoute)


@router.get("/detail/{date}/{code}", summary="获取每日股票数据详情", description="获取每日股票数据详情")
async def get_obj_detail_controller(
    date: str = Path(..., description="日期"),
    code: str = Path(..., description="代码"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["stock:spot:query"]))
) -> JSONResponse:
    result_dict = await SpotService.get_spot_detail_service(date=date, code=code, auth=auth)
    logger.info(f"获取每日股票数据详情成功 {date} {code}")
    return SuccessResponse(data=result_dict, msg="获取每日股票数据详情成功")

@router.get("/list", summary="查询每日股票数据列表", description="查询每日股票数据列表")
async def get_obj_list_controller(
    page: PaginationQueryParams = Depends(),
    search: SpotQueryParams = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["stock:spot:query"]))
) -> JSONResponse:
    result_dict_list = await SpotService.get_spot_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"查询每日股票数据列表成功")
    return SuccessResponse(data=result_dict, msg="查询每日股票数据列表成功")
