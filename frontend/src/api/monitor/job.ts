import request from "@/utils/request";

const JobAPI = {
  getJobList(query: JobPageQuery) {
    return request<ApiResponse<PageResult<JobTable[]>>>({
      url: `/monitor/job/list`,
      method: "get",
      params: query,
    });
  },

  getJobDetail(query: number) {
    return request<ApiResponse<JobTable>>({
      url: `/monitor/job/detail/${query}`,
      method: "get",
    });
  },

  createJob(body: JobForm) {
    return request<ApiResponse>({
      url: `/monitor/job/create`,
      method: "post",
      data: body,
    });
  },

  updateJob(body: JobForm) {
    return request<ApiResponse>({
      url: `/monitor/job/update`,
      method: "put",
      data: body,
    });
  },

  deleteJob(body: number[]) {
    return request<ApiResponse>({
      url: `/monitor/job/delete`,
      method: "delete",
      data: body,
    });
  },

  exportJob(body: JobPageQuery) {
    return request<ApiResponse>({
      url: `/monitor/job/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  clearJob() {
    return request<ApiResponse>({
      url: `/monitor/job/clear`,
      method: "delete",
    });
  },

  OptionJob(params: JobOptionData) {
    return request<ApiResponse>({
      url: `/monitor/job/option`,
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

export interface JobOptionData {
  id?: number;
  option?: number; //操作类型 1: 暂停 2: 恢复 3: 重启
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
