import request from "@/utils/request";

const DeptAPI = {
  getDeptList(query?: DeptPageQuery) {
    return request<ApiResponse<PageResult<DeptTable[]>>>({
      url: `/system/dept/list`,
      method: "get",
      params: query,
    });
  },

  getDeptDetail(query: number) {
    return request<ApiResponse<DeptTable>>({
      url: `/system/dept/detail/${query}`,
      method: "get",
    });
  },

  createDept(body: DeptForm) {
    return request<ApiResponse>({
      url: `/system/dept/create`,
      method: "post",
      data: body,
    });
  },

  updateDept(body: DeptForm) {
    return request<ApiResponse>({
      url: `/system/dept/update`,
      method: "put",
      data: body,
    });
  },

  deleteDept(body: number[]) {
    return request<ApiResponse>({
      url: `/system/dept/delete`,
      method: "delete",
      data: body,
    });
  },

  batchAvailableDept(body: BatchType) {
    return request<ApiResponse>({
      url: `/system/dept/available/setting`,
      method: "patch",
      data: body,
    });
  },
};

export default DeptAPI;

export interface DeptPageQuery {
  name?: string;
  status?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface DeptTable {
  index?: number;
  id?: number;
  name?: string;
  order?: number;
  parent_id?: number;
  parent_name?: string;
  status?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  children?: DeptTable[];
  creator?: creatorType;
}

export interface DeptForm {
  id?: number;
  name?: string;
  order?: number;
  parent_id?: number;
  status?: boolean;
  description?: string;
}
