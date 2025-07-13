import request from "@/utils/request";

const JobAPI = {
  getJobList(query: any) {
    return request<ApiResponse>({
      url: `/system/job/list`,
      method: "get",
      params: query,
    });
  },

  getJobDetail(query: any) {
    return request<ApiResponse>({
      url: `/system/job/detail`,
      method: "get",
      params: query,
    });
  },

  createJob(body: any) {
    return request<ApiResponse>({
      url: `/system/job/create`,
      method: "post",
      data: body,
    });
  },

  updateJob(body: any) {
    return request<ApiResponse>({
      url: `/system/job/update`,
      method: "put",
      data: body,
    });
  },

  deleteJob(query: any) {
    return request<ApiResponse>({
      url: `/system/job/delete`,
      method: "delete",
      params: query,
    });
  },

  exportJob(body: any) {
    return request<ApiResponse>({
      url: `/system/job/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  clearJob() {
    return request<ApiResponse>({
      url: `/system/job/clear`,
      method: "delete",
    });
  },

  OptionJob(params: any) {
    return request<ApiResponse>({
      url: `/system/job/option`,
      method: "put",
      data: params,
    });
  },
};

export default JobAPI;

export interface JobPageQuery extends PageQuery {
  name?: string;
  status?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface JobTable {
  index?: number;
  id?: number;
  name?: string;
  func?: string;
  trigger?: string;
  args?: string;
  kwargs?: string;
  coalesce?: boolean;
  max_instances?: number;
  jobstore?: string;
  executor?: string;
  trigger_args?: string;
  start_date?: string;
  end_date?: string;
  status?: boolean;
  message?: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface JobForm {
  id?: number;
  name?: string;
  func?: string;
  trigger?: string;
  args?: string;
  kwargs?: string;
  coalesce?: boolean;
  max_instances?: number;
  jobstore?: string;
  executor?: string;
  trigger_args?: string;
  start_date?: string;
  end_date?: string;
  status?: boolean;
  message?: string;
  description?: string;
}
