# -*- coding: utf-8 -*-

from fastapi import APIRouter
from app.api.v1.controllers.stock.trade_time_controller import router as TradeTimeRouter
from app.api.v1.controllers.stock.comprehensive_controller import router as ComprehensiveRouter
from app.api.v1.controllers.stock.spot_controller import router as SpotRouter



StockApiRouter = APIRouter(prefix="/stock", tags=["股票模块"])

StockApiRouter.include_router(router=TradeTimeRouter, prefix="/trade_time")
StockApiRouter.include_router(router=ComprehensiveRouter, prefix="/comprehensive")
StockApiRouter.include_router(router=SpotRouter, prefix="/spot")
