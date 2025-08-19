import request from "@/utils/request";

const TradeTimeAPI = {
  getTradeTime(type: "last" | "first") {
    return request<ApiResponse<TradeTimeTable>>({
      url: `/stock/trade_time/${type}`,
      method: "get",
    });
  },
};

export default TradeTimeAPI;

export interface TradeTimeTable {
  trade_time?: string;
}