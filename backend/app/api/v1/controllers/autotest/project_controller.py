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
from app.api.v1.params.autotest.project_param import ProjectQueryParams
from app.api.v1.services.autotest.project_service import ProjectService
from app.api.v1.schemas.autotest.project_schema import ProjectCreateSchema, ProjectUpdateSchema


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail", summary="获取项目详情", description="获取项目详情")
async def get_obj_detail(
        id: int = Query(..., description="项目ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:project:query"])),
) -> JSONResponse:
    result_dict = await ProjectService.get_detail_services(id=id, auth=auth)
    logger.info(f"{auth.user.name} 获取项目详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取项目详情成功")

@router.get("/list", summary="查询项目", description="查询项目")
async def get_obj_list(
        page: PaginationQueryParams = Depends(),
        search: ProjectQueryParams = Depends(),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:project:query"])),
) -> JSONResponse:
    result_dict_list = await ProjectService.get_list_services(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"{auth.user.name} 查询项目列表成功")
    return SuccessResponse(data=result_dict, msg="查询项目列表成功")

@router.post("/create", summary="创建项目", description="创建项目")
async def create_obj(
        data: ProjectCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:project:create"])),
) -> JSONResponse:
    result_dict = await ProjectService.create_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 创建项目成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建项目成功")

@router.put("/update", summary="修改项目", description="修改项目")
async def update_obj(
        data: ProjectUpdateSchema,
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:project:update"])),
) -> JSONResponse:
    result_dict = await ProjectService.update_services(auth=auth, data=data)
    logger.info(f"{auth.user.name} 修改项目成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改项目成功")

@router.delete("/delete", summary="删除项目", description="删除项目")
async def delete_obj(
        id: int = Query(..., description="项目ID"),
        auth: AuthSchema = Depends(AuthPermission(permissions=["autotest:project:delete"])),
) -> JSONResponse:
    await ProjectService.delete_services(auth=auth, id=id)
    logger.info(f"{auth.user.name} 删除项目成功: {id}")
    return SuccessResponse(msg="删除项目成功")
