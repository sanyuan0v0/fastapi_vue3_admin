# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.dependencies import AuthPermission
from app.core.logger import logger
from app.common.response import SuccessResponse
from app.api.v1.services.monitor.server_service import ServerService
from app.core.router_class import OperationLogRoute


router = APIRouter(route_class=OperationLogRoute)


@router.get(
    '/info',
    summary="查询服务器监控信息",
    description="查询服务器监控信息",
    dependencies=[Depends(AuthPermission(permissions=["monitor:server:query"]))]
)
async def get_monitor_server_info_controller() -> JSONResponse:
    # 获取全量数据
    result_dict = await ServerService.get_server_monitor_info_service()
    logger.info('获取服务器监控信息成功')

    return SuccessResponse(data=result_dict, msg='获取服务器监控信息成功')
