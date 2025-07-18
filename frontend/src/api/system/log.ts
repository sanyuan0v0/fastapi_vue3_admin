import request from "@/utils/request";

const LogAPI = {
  getLogList(query: LogPageQuery) {
    return request<ApiResponse<PageResult<LogTable[]>>>({
      url: `/system/log/list`,
      method: "get",
      params: query,
    });
  },

  getLogDetail(query: number) {
    return request<ApiResponse<LogTable>>({
      url: `/system/log/detail/${query}`,
      method: "get",
    });
  },

  deleteLog(body: number[]) {
    return request<ApiResponse>({
      url: `/system/log/delete`,
      method: "delete",
      data: body,
    });
  },

  exportLog(query: LogPageQuery) {
    return request<ApiResponse>({
      url: `/system/log/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },
};

export default LogAPI;

export interface LogPageQuery extends PageQuery {
  request_path?: string;
  creator_name?: string;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface LogTable {
  id?: number;
  request_path?: string;
  request_method?: string;
  request_ip?: string;
  login_location?: string;
  request_browser?: string;
  request_os?: string;
  response_code?: number;
  request_payload?: string;
  response_json?: string;
  process_time?: number;
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}
