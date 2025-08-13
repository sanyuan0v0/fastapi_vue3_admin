import request from "@/utils/request";

const ComprehensiveAPI = {
  getComprehensiveList(query: ComprehensivePageQuery) {
    return request<ApiResponse<PageResult<ComprehensiveTable[]>>>({
      url: `/stock/comprehensive/list`,
      method: "get",
      params: query,
    });
  },

  getComprehensiveDetail(date: string, code: string) {

    return request<ApiResponse<ComprehensiveTable>>({
      url: `/stock/comprehensive/detail/${date}/${code}`,
      method: "get",
    });
  },
};

export default ComprehensiveAPI;

export interface ComprehensivePageQuery extends PageQuery {
  /** 示例标题 */
  name?: string;
  /** 示例状态 */
  code?: string;
  /** 开始时间 */
  start_date?: string;
  /** 结束时间 */
  end_date?: string;
}

export interface ComprehensiveTable {
  date?: string;                  // 日期
  code?: string;                  // 代码
  name?: string;                  // 名称
  new_price?: number;             // 最新价
  change_rate?: number;           // 涨跌幅
  volume_ratio?: number;          // 量比
  high_price?: number;            // 最高价
  low_price?: number;             // 最低价
  pre_close_price?: number;       // 昨收价
  volume?: number;                // 成交量
  deal_amount?: number;           // 成交额
  turnoverrate?: number;          // 换手率
  listing_date?: string;          // 上市时间
  industry?: string;              // 行业
  area?: string;                  // 地区
  concept?: string;               // 概念
  style?: string;                 // 板块
  is_hs300?: string;             // 沪300
  is_sz50?: string;              // 上证50
  is_zz500?: string;             // 中证500
  is_zz1000?: string;            // 中证1000
  is_cy50?: string;              // 创业板50
  pe9?: number;                  // 市盈率TTM
  pbnewmrq?: number;             // 市净率MRQ
  pettmdeducted?: number;        // 市盈率TTM扣非
  ps9?: number;                  // 市销率TTM
  pcfjyxjl9?: number;            // 市现率TTM
  predict_pe_syear?: number;     // 预测市盈率今年
  predict_pe_nyear?: number;     // 预测市盈率明年
  total_market_cap?: number;     // 总市值
  free_cap?: number;             // 流通市值
  dtsyl?: number;                // 动态市盈率
  ycpeg?: number;                // 预测PEG
  enterprise_value_multiple?: number; // 企业价值倍数
  basic_eps?: number;            // 每股收益
  bvps?: number;                 // 每股净资产
  per_netcash_operate?: number;  // 每股经营现金流
  per_fcfe?: number;             // 每股自由现金流
  per_capital_reserve?: number;  // 每股资本公积
  per_unassign_profit?: number;  // 每股未分配利润
  per_surplus_reserve?: number;  // 每股盈余公积
  per_retained_earning?: number; // 每股留存收益
  parent_netprofit?: number;     // 归属净利润
  deduct_netprofit?: number;     // 扣非净利润
  total_operate_income?: number; // 营业总收入
  roe_weight?: number;           // 净资产收益率ROE
  jroa?: number;                 // 总资产净利率ROA
  roic?: number;                 // 投入资本回报率ROIC
  zxgxl?: number;                // 最新股息率
  sale_gpr?: number;             // 毛利率
  sale_npr?: number;             // 净利率
  netprofit_yoy_ratio?: number;  // 净利润增长率
  deduct_netprofit_growthrate?: number; // 扣非净利润增长率
  toi_yoy_ratio?: number;        // 营收增长率
  netprofit_growthrate_3y?: number; // 净利润3年复合增长率
  income_growthrate_3y?: number; // 营收3年复合增长率
  predict_netprofit_ratio?: number; // 预测净利润同比增长
  predict_income_ratio?: number; // 预测营收同比增长
  basiceps_yoy_ratio?: number;   // 每股收益同比增长率
  total_profit_growthrate?: number; // 利润总额同比增长率
  operate_profit_growthrate?: number; // 营业利润同比增长率
  debt_asset_ratio?: number;     // 资产负债率
  equity_ratio?: number;         // 产权比率
  equity_multiplier?: number;    // 权益乘数
  current_ratio?: number;        // 流动比率
  speed_ratio?: number;          // 速动比率
  total_shares?: number;         // 总股本
  free_shares?: number;          // 流通股本
  holder_newest?: number;        // 最新股东户数
  holder_ratio?: number;         // 股东户数增长率
  hold_amount?: number;          // 户均持股金额
  avg_hold_num?: number;         // 户均持股数量
  holdnum_growthrate_3q?: number; // 户均持股数季度增长率
  holdnum_growthrate_hy?: number; // 户均持股数半年增长率
  hold_ratio_count?: number;     // 十大股东持股比例合计
  free_hold_ratio?: number;      // 十大流通股东比例合计
  macd_golden_fork?: boolean;    // MACD金叉日线
  macd_golden_forkz?: boolean;   // MACD金叉周线
  macd_golden_forky?: boolean;   // MACD金叉月线
  kdj_golden_fork?: boolean;     // KDJ金叉日线
  kdj_golden_forkz?: boolean;    // KDJ金叉周线
  kdj_golden_forky?: boolean;    // KDJ金叉月线
  break_through?: boolean;       // 放量突破
  low_funds_inflow?: boolean;    // 低位资金净流入
  high_funds_outflow?: boolean;  // 高位资金净流出
  breakup_ma_5days?: boolean;    // 向上突破均线5日
  breakup_ma_10days?: boolean;   // 向上突破均线10日
  breakup_ma_20days?: boolean;   // 向上突破均线20日
  breakup_ma_30days?: boolean;   // 向上突破均线30日
  breakup_ma_60days?: boolean;   // 向上突破均线60日
  long_avg_array?: boolean;      // 均线多头排列
  short_avg_array?: boolean;     // 均线空头排列
  upper_large_volume?: boolean;  // 连涨放量
  down_narrow_volume?: boolean;  // 下跌无量
  one_dayang_line?: boolean;     // 一根大阳线
  two_dayang_lines?: boolean;    // 两根大阳线
  rise_sun?: boolean;            // 旭日东升
  power_fulgun?: boolean;        // 强势多方炮
  restore_justice?: boolean;     // 拨云见日
  down_7days?: boolean;          // 七仙女下凡(七连阴)
  upper_8days?: boolean;         // 八仙过海(八连阳)
  upper_9days?: boolean;         // 九阳神功(九连阳)
  upper_4days?: boolean;         // 四串阳
  heaven_rule?: boolean;         // 天量法则
  upside_volume?: boolean;       // 放量上攻
  bearish_engulfing?: boolean;   // 穿头破脚
  reversing_hammer?: boolean;    // 倒转锤头
  shooting_star?: boolean;       // 射击之星
  evening_star?: boolean;        // 黄昏之星
  first_dawn?: boolean;          // 曙光初现
  pregnant?: boolean;            // 身怀六甲
  black_cloud_tops?: boolean;    // 乌云盖顶
  morning_star?: boolean;        // 早晨之星
  narrow_finish?: boolean;       // 窄幅整理
  limited_lift_f6m?: boolean;    // 限售解禁未来半年
  limited_lift_f1y?: boolean;    // 限售解禁未来1年
  limited_lift_6m?: boolean;     // 限售解禁近半年
  limited_lift_1y?: boolean;     // 限售解禁近1年
  directional_seo_1m?: boolean;  // 定向增发近1个月
  directional_seo_3m?: boolean;  // 定向增发近3个月
  directional_seo_6m?: boolean;  // 定向增发近6个月
  directional_seo_1y?: boolean;  // 定向增发近1年
  recapitalize_1m?: boolean;     // 资产重组近1个月
  recapitalize_3m?: boolean;     // 资产重组近3个月
  recapitalize_6m?: boolean;     // 资产重组近6个月
  recapitalize_1y?: boolean;     // 资产重组近1年
  equity_pledge_1m?: boolean;    // 股权质押近1个月
  equity_pledge_3m?: boolean;    // 股权质押近3个月
  equity_pledge_6m?: boolean;    // 股权质押近6个月
  equity_pledge_1y?: boolean;    // 股权质押近1年
  pledge_ratio?: number;         // 质押比例
  goodwill_scale?: number;       // 商誉规模
  goodwill_assets_ratro?: number;// 商誉占净资产比例
  predict_type?: string;         // 业绩预告
  par_dividend_pretax?: number;  // 每股股利税前
  par_dividend?: number;         // 每股红股
  par_it_equity?: number;        // 每股转增股本
  holder_change_3m?: number;     // 近3月股东增减比例
  executive_change_3m?: number;  // 近3月高管增减比例
  org_survey_3m?: number;        // 近3月机构调研
  org_rating?: string;           // 机构评级
  allcorp_num?: number;          // 机构持股家数合计
  allcorp_fund_num?: number;     // 基金持股家数
  allcorp_qs_num?: number;       // 券商持股家数
  allcorp_qfii_num?: number;     // QFII持股家数
  allcorp_bx_num?: number;       // 保险公司持股家数
  allcorp_sb_num?: number;       // 社保持股家数
  allcorp_xt_num?: number;       // 信托公司持股家数
  allcorp_ratio?: number;        // 机构持股比例合计
  allcorp_fund_ratio?: number;   // 基金持股比例
  allcorp_qs_ratio?: number;     // 券商持股比例
  allcorp_qfii_ratio?: number;   // QFII持股比例
  allcorp_bx_ratio?: number;     // 保险公司持股比例
  allcorp_sb_ratio?: number;     // 社保持股比例
  allcorp_xt_ratio?: number;     // 信托公司持股比例
  popularity_rank?: number;      // 股吧人气排名
  rank_change?: number;          // 人气排名变化
  upp_days?: number;             // 人气排名连涨
  down_days?: number;            // 人气排名连跌
  new_high?: number;             // 人气排名创新高
  new_down?: number;             // 人气排名创新低
  newfans_ratio?: number;        // 新晋粉丝占比
  bigfans_ratio?: number;        // 铁杆粉丝占比
  concern_rank_7days?: number;   // 7日关注排名
  browse_rank?: number;          // 今日浏览排名
  amplitude?: number;            // 振幅
  is_issue_break?: boolean;      // 破发股票
  is_bps_break?: boolean;        // 破净股票
  now_newhigh?: boolean;         // 今日创历史新高
  now_newlow?: boolean;          // 今日创历史新低
  high_recent_3days?: boolean;   // 近期创历史新高近3日
  high_recent_5days?: boolean;   // 近期创历史新高近5日
  high_recent_10days?: boolean;  // 近期创历史新高近10日
  high_recent_20days?: boolean;  // 近期创历史新高近20日
  high_recent_30days?: boolean;  // 近期创历史新高近30日
  low_recent_3days?: boolean;    // 近期创历史新低近3日
  low_recent_5days?: boolean;    // 近期创历史新低近5日
  low_recent_10days?: boolean;   // 近期创历史新低近10日
  low_recent_20days?: boolean;   // 近期创历史新低近20日
  low_recent_30days?: boolean;   // 近期创历史新低近30日
  win_market_3days?: boolean;    // 近期跑赢大盘近3日
  win_market_5days?: boolean;    // 近期跑赢大盘近5日
  win_market_10days?: boolean;   // 近期跑赢大盘近10日
  win_market_20days?: boolean;   // 近期跑赢大盘近20日
  win_market_30days?: boolean;   // 近期跑赢大盘近30日
  net_inflow?: number;           // 当日净流入额
  netinflow_3days?: number;      // 3日主力净流入
  netinflow_5days?: number;      // 5日主力净流入
  nowinterst_ratio?: number;     // 当日增仓占比
  nowinterst_ratio_3d?: number;  // 3日增仓占比
  nowinterst_ratio_5d?: number;  // 5日增仓占比
  ddx?: number;                  // 当日DDX
  ddx_3d?: number;               // 3日DDX
  ddx_5d?: number;               // 5日DDX
  ddx_red_10d?: number;          // 10日内DDX飘红天数
  changerate_3days?: number;     // 3日涨跌幅
  changerate_5days?: number;     // 5日涨跌幅
  changerate_10days?: number;    // 10日涨跌幅
  changerate_ty?: number;        // 今年以来涨跌幅
  upnday?: number;               // 连涨天数
  downnday?: number;             // 连跌天数
  listing_yield_year?: number;   // 上市以来年化收益率
  listing_volatility_year?: number; // 上市以来年化波动率
  mutual_netbuy_amt?: number;    // 沪深股通净买入金额
  hold_ratio?: number;           // 沪深股通持股比例
  secucode?: string;             // 全代码
}

