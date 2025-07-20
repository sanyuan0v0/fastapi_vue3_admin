import request from "@/utils/request";

const OnlineAPI = {
  // 查询在线用户列表
  getOnlineList(query: OnlineUserPageQuery) {
    return request<ApiResponse<PageResult<OnlineUserTable[]>>>({
      url: `/monitor/online/list`,
      method: "get",
      params: query,
    });
  },

  // 强退用户
  deleteOnline(body: string) {
    return request<ApiResponse>({
      url: `/monitor/online/delete`,
      method: "delete",
      data: body,
    });
  },

  // 强退用户
  clearOnline() {
    return request<ApiResponse>({
      url: `/monitor/online/clear`,
      method: "delete",
    });
  },
};

export default OnlineAPI;

export interface OnlineUserPageQuery extends PageQuery {
  ipaddr?: string;
  name?: string;
  login_location?: string;
}

export interface OnlineUserTable {
  session_id: string;
  user_id: number;
  name: string;
  user_name: string;
  ipaddr: string;
  login_location: string;
  os: string;
  browser: string;
  login_time: string;
}
