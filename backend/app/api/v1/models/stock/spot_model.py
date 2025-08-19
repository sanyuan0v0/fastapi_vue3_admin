# -*- coding: utf-8 -*-
from app.core.base_model import ModelBase
from sqlalchemy import DATE, VARCHAR, FLOAT, BIGINT, SMALLINT, Column
from sqlalchemy.dialects.mysql import BIT

class SpotModel(ModelBase):
    """
    每日股票数据表
    """

    __tablename__ = 'cn_stock_spot'
    __table_args__ = ({'comment': '每日股票数据表'})

    date = Column(DATE, primary_key=True, comment='日期')
    code = Column(VARCHAR(10), primary_key=True, comment='代码')
    name = Column(VARCHAR(20), comment='名称')
    new_price = Column(FLOAT, comment='最新价')
    change_rate = Column(FLOAT, comment='涨跌幅')
    ups_downs = Column(FLOAT, comment='涨跌额')
    volume = Column(BIGINT, comment='成交量')
    deal_amount = Column(BIGINT, comment='成交额')
    amplitude = Column(FLOAT, comment='振幅')
    turnoverrate = Column(FLOAT, comment='换手率')
    volume_ratio = Column(FLOAT, comment='量比')
    open_price = Column(FLOAT, comment='今开')
    high_price = Column(FLOAT, comment='最高')
    low_price = Column(FLOAT, comment='最低')
    pre_close_price = Column(FLOAT, comment='昨收')
    speed_increase = Column(FLOAT, comment='涨速')
    speed_increase_5 = Column(FLOAT, comment='5分钟涨跌')
    speed_increase_60 = Column(FLOAT, comment='60日涨跌幅')
    speed_increase_all = Column(FLOAT, comment='年初至今涨跌幅')
    dtsyl = Column(FLOAT, comment='市盈率动')
    pe9 = Column(FLOAT, comment='市盈率TTM')
    pe = Column(FLOAT, comment='市盈率静')
    pbnewmrq = Column(FLOAT, comment='市净率')
    basic_eps = Column(FLOAT, comment='每股收益')
    bvps = Column(FLOAT, comment='每股净资产')
    per_capital_reserve = Column(FLOAT, comment='每股公积金')
    per_unassign_profit = Column(FLOAT, comment='每股未分配利润')
    roe_weight = Column(FLOAT, comment='加权净资产收益率')
    sale_gpr = Column(FLOAT, comment='毛利率')
    debt_asset_ratio = Column(FLOAT, comment='资产负债率')
    total_operate_income = Column(BIGINT, comment='营业收入')
    toi_yoy_ratio = Column(FLOAT, comment='营业收入同比增长')
    parent_netprofit = Column(BIGINT, comment='归属净利润')
    netprofit_yoy_ratio = Column(FLOAT, comment='归属净利润同比增长')
    report_date = Column(DATE, comment='报告期')
    total_shares = Column(BIGINT, comment='总股本')
    free_shares = Column(BIGINT, comment='已流通股份')
    total_market_cap = Column(BIGINT, comment='总市值')
    free_cap = Column(BIGINT, comment='流通市值')
    industry = Column(VARCHAR(20), comment='所处行业')
    listing_date = Column(DATE, comment='上市时间')
