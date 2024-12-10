# -*- coding: utf-8 -*-

from fastapi import APIRouter, BackgroundTasks, Depends, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from app.core.logger import logger
from app.api.v1.services.common.common_service import CommonService
from app.common.response import SuccessResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute


router = APIRouter(route_class=OperationLogRoute)


@router.get(
    '/list',
    summary="获取文件列表",
    description="获取文件列表",
    dependencies=[Depends(AuthPermission(permissions=['common:file:query']))]
)
async def common_get_file_list(request: Request)->JSONResponse:
    """
    获取文件列表
    """
    file_result = await CommonService.get_file_list_services(request)
    return SuccessResponse(msg='获取文件列表成功', data=file_result)

@router.post(
    '/upload',
    summary="上传文件",
    description="上传文件",
    dependencies=[Depends(AuthPermission(permissions=['common:file:upload']))]
)
async def common_upload(
    request: Request,
    file: UploadFile = File(...)
) -> JSONResponse:
    upload_result = await CommonService.upload_service(request, file)
    logger.info(f"上传文件成功: {file.filename}")
    return SuccessResponse(msg='上传成功', data=upload_result)


@router.get(
    '/download',
    summary="下载文件",
    description="下载文件",
    dependencies=[Depends(AuthPermission(permissions=['common:file:download']))]
)
async def common_download(
    background_tasks: BackgroundTasks,
    file_name: str = Query(alias='fileName'),
    delete: bool = Query(),
) -> StreamingResponse:
    download_result = await CommonService.download_services(background_tasks, file_name, delete)
    logger.info(f"下载文件成功: {file_name}")

    return StreamResponse(msg='下载成功', data=download_result)


@router.get(
    '/download/resource',
    summary="下载资源",
    description="下载资源",
    dependencies=[Depends(AuthPermission(permissions=['common:file:download']))]
)
async def common_download_resource(
    resource: str = Query()
) -> StreamingResponse:
    download_resource_result = await CommonService.download_resource_services(resource)
    logger.info(f"下载资源成功: {resource}")

    return StreamResponse(msg='下载成功', data=download_resource_result.result)
