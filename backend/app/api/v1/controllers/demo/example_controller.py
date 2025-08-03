# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
import urllib.parse

from app.common.response import StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParams
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.base_schema import BatchSetAvailable
from app.core.logger import logger
from app.common.request import PaginationService
from app.utils.common_util import bytes2file_response
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.params.demo.example_param import ExampleQueryParams
from app.api.v1.services.demo.example_service import ExampleService
from app.api.v1.schemas.demo.example_schema import (
    ExampleCreateSchema,
    ExampleUpdateSchema
)


router = APIRouter(route_class=OperationLogRoute)

@router.get("/detail/{id}", summary="获取示例详情", description="获取示例详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="示例ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:query"]))
) -> JSONResponse:
    result_dict = await ExampleService.get_example_detail_service(id=id, auth=auth)
    logger.info(f"获取示例详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取示例详情成功")

@router.get("/list", summary="查询示例列表", description="查询示例列表")
async def get_obj_list_controller(
    page: PaginationQueryParams = Depends(),
    search: ExampleQueryParams = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:query"]))
) -> JSONResponse:
    result_dict_list = await ExampleService.get_example_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"查询示例列表成功")
    return SuccessResponse(data=result_dict, msg="查询公告列表成功")

@router.post("/create", summary="创建示例", description="创建示例")
async def create_obj_controller(
    data: ExampleCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:create"]))
) -> JSONResponse:
    result_dict = await ExampleService.create_example_service(auth=auth, data=data)
    logger.info(f"创建示例成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建示例成功")

@router.put("/update", summary="修改示例", description="修改示例")
async def update_obj_controller(
    data: ExampleUpdateSchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:update"]))
) -> JSONResponse:
    result_dict = await ExampleService.update_example_service(auth=auth, data=data)
    logger.info(f"修改示例成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改示例成功")

@router.delete("/delete", summary="删除示例", description="删除示例")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:delete"]))
) -> JSONResponse:
    await ExampleService.delete_example_service(auth=auth, ids=ids)
    logger.info(f"删除示例成功: {ids}")
    return SuccessResponse(msg="删除示例成功")

@router.patch("/available/setting", summary="批量修改示例状态", description="批量修改示例状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:patch"]))
) -> JSONResponse:
    await ExampleService.set_example_available_service(auth=auth, data=data)
    logger.info(f"批量修改示例状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改示例状态成功")

@router.post('/export', summary="导出示例", description="导出示例")
async def export_obj_list_controller(
    search: ExampleQueryParams = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:export"]))
) -> StreamingResponse:
    # 获取全量数据
    result_dict_list = await ExampleService.get_example_list_service(search=search, auth=auth)
    export_result = await ExampleService.batch_export_service(obj_list=result_dict_list)
    logger.info('导出示例成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {
            'Content-Disposition': 'attachment; filename=example.xlsx'
        }
    )

@router.post('/import', summary="导入示例", description="导入示例")
async def import_obj_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:import"]))
) -> JSONResponse:
    batch_import_result = await ExampleService.batch_import_service(file=file, auth=auth, update_support=True)
    logger.info(f"导入示例成功: {batch_import_result}")
    return SuccessResponse(data=batch_import_result, msg="导入示例成功")

@router.post('/download/template', summary="获取示例导入模板", description="获取示例导入模板", dependencies=[Depends(AuthPermission(permissions=["demo:example:download"]))])
async def export_obj_template_controller()-> StreamingResponse:
    example_import_template_result = await ExampleService.import_template_download_service()
    logger.info('获取示例导入模板成功')

    return StreamResponse(
        data=bytes2file_response(example_import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {
            'Content-Disposition': f'attachment; filename={urllib.parse.quote("示例导入模板.xlsx")}',
            'Access-Control-Expose-Headers': 'Content-Disposition'
        }
    )