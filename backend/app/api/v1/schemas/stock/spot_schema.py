# -*- coding: utf-8 -*-

from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, Field
from app.core.validator import DateStr


class SpotOutSchema(BaseModel):
    """响应模型"""
    model_config = ConfigDict(from_attributes=True)

    date: Optional[DateStr] = Field(None, description="日期")
    code: Optional[str] = Field(None, description="代码")
    name: Optional[str] = Field(None, description="名称")
    new_price: Optional[float] = Field(None, description="最新价")
    change_rate: Optional[float] = Field(None, description="涨跌幅")
    ups_downs: Optional[float] = Field(None, description="涨跌额")
    volume: Optional[int] = Field(None, description="成交量")
    deal_amount: Optional[int] = Field(None, description="成交额")
    amplitude: Optional[float] = Field(None, description="振幅")
    turnoverrate: Optional[float] = Field(None, description="换手率")
    volume_ratio: Optional[float] = Field(None, description="量比")
    open_price: Optional[float] = Field(None, description="今开")
    high_price: Optional[float] = Field(None, description="最高")
    low_price: Optional[float] = Field(None, description="最低")
    pre_close_price: Optional[float] = Field(None, description="昨收")
    speed_increase: Optional[float] = Field(None, description="涨速")
    industry: Optional[str] = Field(None, description="所处行业")
    listing_date: Optional[DateStr] = Field(None, description="上市时间")


class SpotDetailSchema(SpotOutSchema):
    """详情模型"""
    speed_increase_5: Optional[float] = Field(None, description="5分钟涨跌")
    speed_increase_60: Optional[float] = Field(None, description="60日涨跌幅")
    speed_increase_all: Optional[float] = Field(None, description="年初至今涨跌幅")
    dtsyl: Optional[float] = Field(None, description="市盈率动")
    pe9: Optional[float] = Field(None, description="市盈率TTM")
    pe: Optional[float] = Field(None, description="市盈率静")
    pbnewmrq: Optional[float] = Field(None, description="市净率")
    basic_eps: Optional[float] = Field(None, description="每股收益")
    bvps: Optional[float] = Field(None, description="每股净资产")
    per_capital_reserve: Optional[float] = Field(None, description="每股公积金")
    per_unassign_profit: Optional[float] = Field(None, description="每股未分配利润")
    roe_weight: Optional[float] = Field(None, description="加权净资产收益率")
    sale_gpr: Optional[float] = Field(None, description="毛利率")
    debt_asset_ratio: Optional[float] = Field(None, description="资产负债率")
    total_operate_income: Optional[int] = Field(None, description="营业收入")
    toi_yoy_ratio: Optional[float] = Field(None, description="营业收入同比增长")
    parent_netprofit: Optional[int] = Field(None, description="归属净利润")
    netprofit_yoy_ratio: Optional[float] = Field(None, description="归属净利润同比增长")
    report_date: Optional[DateStr] = Field(None, description="报告期")
    total_shares: Optional[int] = Field(None, description="总股本")
    free_shares: Optional[int] = Field(None, description="已流通股份")
    total_market_cap: Optional[int] = Field(None, description="总市值")
    free_cap: Optional[int] = Field(None, description="流通市值")


class SpotCreateSchema(BaseModel):
    """新增模型"""
    pass


class SpotUpdateSchema(BaseModel):
    """更新模型"""
    pass
