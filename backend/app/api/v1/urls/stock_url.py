# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.api.v1.controllers.stock.comprehensive_controller import router as ComprehensiveRouter



StockApiRouter = APIRouter(prefix="/stock", tags=["股票模块"])


StockApiRouter.include_router(router=ComprehensiveRouter, prefix="/comprehensive")
