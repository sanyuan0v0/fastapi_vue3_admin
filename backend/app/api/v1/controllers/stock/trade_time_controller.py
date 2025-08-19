from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from app.common.response import SuccessResponse
from app.utils.stock_realtime import get_trade_date_last
from app.core.logger import logger
from enum import Enum

class TradeTimeType(str, Enum):
    run_date = "first"
    run_date_nph = "last"


router = APIRouter(route_class=OperationLogRoute)

@router.get("/{type}", summary="获取交易时间", description="获取交易时间")
async def get_trade_time_controller(type: TradeTimeType=Path(..., description="交易时间类型")) -> JSONResponse:
    run_date, run_date_nph = get_trade_date_last()
    logger.info(f"获取交易时间成功 {run_date} {run_date_nph}")
    trade_time = run_date if type == TradeTimeType.run_date else run_date_nph
    result_dict = {
        "trade_time": trade_time,
    }
    return SuccessResponse(data=result_dict, msg="获取交易时间成功")
