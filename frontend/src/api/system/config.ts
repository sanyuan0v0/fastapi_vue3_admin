import request from "@/utils/request";

const ConfigAPI = {
  uploadFile(body: any) {
    return request<ApiResponse<UploadFilePath>>({
      url: `/system/config/upload`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  getInitConfig() {
    return request<ApiResponse<ConfigTable[]>>({
      url: `/system/config/info`,
      method: "get",
    });
  },

  getConfigList(query: ConfigPageQuery) {
    return request<ApiResponse<PageResult<ConfigTable[]>>>({
      url: `/system/config/list`,
      method: "get",
      params: query,
    });
  },

  getConfigDetail(query: number) {
    return request<ApiResponse<ConfigTable>>({
      url: `/system/config/detail/${query}`,
      method: "get",
    });
  },

  createConfig(body: ConfigForm) {
    return request<ApiResponse>({
      url: `/system/config/create`,
      method: "post",
      data: body,
    });
  },

  updateConfig(body: ConfigForm) {
    return request<ApiResponse>({
      url: `/system/config/update`,
      method: "put",
      data: body,
    });
  },

  deleteConfig(body: number[]) {
    return request<ApiResponse>({
      url: `/system/config/delete`,
      method: "delete",
      data: body,
    });
  },

  exportConfig(body: ConfigPageQuery) {
    return request<ApiResponse>({
      url: `/system/config/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },
};

export default ConfigAPI;

export interface ConfigPageQuery extends PageQuery {
  /** 配置名称 */
  config_name?: string;
  /** 配置键 */
  config_key?: string;
  /** 配置类型 */
  config_type?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface ConfigTable {
  id?: number;
  config_name?: string;
  config_key?: string;
  config_value?: string;
  config_type?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface ConfigForm {
  id?: number;
  config_name?: string;
  config_key?: string;
  config_value?: string;
  config_type?: boolean;
  description?: string;
}
