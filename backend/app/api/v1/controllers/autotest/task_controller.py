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
from app.api.v1.params.autotest.task_param import TaskQueryParams
from app.api.v1.services.autotest.task_service import TaskService
from app.api.v1.schemas.autotest.task_schema import TaskCreateSchema, TaskUpdateSchema


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail", summary="获取执行记录详情", description="获取执行记录详情")
async def get_obj_detail(
        id: int = Query(..., description="执行记录ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:task:query"])),
) -> JSONResponse:
    result_dict = await TaskService.get_detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取执行记录详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取执行记录详情成功")

@router.get("/list", summary="查询执行记录", description="查询执行记录")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: TaskQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:task:query"])),
) -> JSONResponse:
    result_dict_list = await TaskService.get_list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"{auth.user.name} 查询执行记录列表成功")
    return SuccessResponse(data=result_dict, msg="查询执行记录列表成功")

@router.post("/create", summary="创建执行记录", description="创建执行记录")
async def create_obj(
        data: TaskCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:task:create"])),
) -> JSONResponse:
    result_dict = await TaskService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建执行记录成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建执行记录成功")

@router.put("/update", summary="修改执行记录", description="修改执行记录")
async def update_obj(
        data: TaskUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:task:update"])),
) -> JSONResponse:
    result_dict = await TaskService.update_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 修改执行记录成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改执行记录成功")

@router.delete("/delete", summary="删除执行记录", description="删除执行记录")
async def delete_obj(
        id: int = Query(..., description="执行记录ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:task:delete"])),
) -> JSONResponse:
    await TaskService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除执行记录成功: {id}")
    return SuccessResponse(msg="删除执行记录成功")
