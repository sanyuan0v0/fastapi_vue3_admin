import request from "@/utils/request";

const PositionAPI = {
  getPositionList(query: PositionPageQuery) {
    return request<ApiResponse<PageResult<PositionTable[]>>>({
      url: `/system/position/list`,
      method: "get",
      params: query,
    });
  },

  getPositionDetail(id: number) {
    return request<ApiResponse<PositionTable>>({
      url: `/system/position/detail`,
      method: "get",
      params: id,
    });
  },

  createPosition(body: PositionForm) {
    return request<ApiResponse>({
      url: `/system/position/create`,
      method: "post",
      data: body,
    });
  },

  updatePosition(body: PositionForm) {
    return request<ApiResponse>({
      url: `/system/position/update`,
      method: "put",
      data: body,
    });
  },

  deletePosition(query: DeleteType) {
    return request<ApiResponse>({
      url: `/system/position/delete`,
      method: "delete",
      params: query,
    });
  },

  batchAvailablePosition(body: BatchType) {
    return request<ApiResponse>({
      url: `/system/position/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportPosition(body: any[]) {
    return request<ApiResponse>({
      url: `/system/position/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },
};

export default PositionAPI;

export interface PositionPageQuery extends PageQuery {
  name?: string;
  status?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface PositionTable {
  index?: number;
  id?: number;
  name?: string;
  order?: number;
  status?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface PositionForm {
  id?: number;
  name?: string;
  order?: number;
  status?: boolean;
  description?: string;
}
