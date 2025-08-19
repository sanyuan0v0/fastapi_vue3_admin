import request from "@/utils/request";

const SpotAPI = {
  getSpotList(query: SpotPageQuery) {
    return request<ApiResponse<PageResult<SpotTable[]>>>({
      url: `/stock/spot/list`,
      method: "get",
      params: query,
    });
  },

  getSpotDetail(date: string, code: string) {
    return request<ApiResponse<SpotTable>>({
      url: `/stock/spot/detail/${date}/${code}`,
      method: "get",
    });
  },
};

export default SpotAPI;

export interface SpotPageQuery extends PageQuery {
  /** 示例标题 */
  name?: string;
  /** 示例状态 */
  code?: string;
  /** 开始时间 */
  start_date?: string;
  /** 结束时间 */
  end_date?: string;
}

export interface SpotTable {
  date?: string;                  // 日期
  code?: string;                  // 代码
  name?: string;                  // 名称
  new_price?: number;             // 最新价
  change_rate?: number;           // 涨跌幅
  ups_downs?: number;             // 涨跌额
  volume?: number;                // 成交量
  deal_amount?: number;           // 成交额
  amplitude?: number;             // 振幅
  turnoverrate?: number;          // 换手率
  volume_ratio?: number;          // 量比
  open_price?: number;            // 今开
  high_price?: number;            // 最高
  low_price?: number;            // 最低
  pre_close_price?: number;       // 昨收
  speed_increase?: number;        // 涨速
  speed_increase_5?: number;      // 5分钟涨跌
  speed_increase_60?: number;     // 60日涨跌幅
  speed_increase_all?: number;    // 年初至今涨跌幅
  dtsyl?: number;                // 市盈率动
  pe9?: number;                  // 市盈率TTM
  pe?: number;                   // 市盈率静
  pbnewmrq?: number;             // 市净率
  basic_eps?: number;            // 每股收益
  bvps?: number;                // 每股净资产
  per_capital_reserve?: number;  // 每股公积金
  per_unassign_profit?: number;  // 每股未分配利润
  roe_weight?: number;          // 加权净资产收益率
  sale_gpr?: number;            // 毛利率
  debt_asset_ratio?: number;    // 资产负债率
  total_operate_income?: number;// 营业收入
  toi_yoy_ratio?: number;       // 营业收入同比增长
  parent_netprofit?: number;    // 归属净利润
  netprofit_yoy_ratio?: number; // 归属净利润同比增长
  report_date?: string;         // 报告期
  total_shares?: number;        // 总股本
  free_shares?: number;         // 已流通股份
  total_market_cap?: number;    // 总市值
  free_cap?: number;           // 流通市值
  industry?: string;           // 所处行业
  listing_date?: string;       // 上市时间
}

