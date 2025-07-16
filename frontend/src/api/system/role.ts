import request from "@/utils/request";

const RoleAPI = {
  getRoleList(query: TablePageQuery) {
    return request<ApiResponse<PageResult<RoleTable[]>>>({
      url: `/system/role/list`,
      method: "get",
      params: query,
    });
  },

  getRoleDetail(query: DetailType) {
    return request<ApiResponse<RoleTable>>({
      url: `/system/role/detail`,
      method: "get",
      params: query,
    });
  },

  createRole(body: RoleForm) {
    return request<ApiResponse>({
      url: `/system/role/create`,
      method: "post",
      data: body,
    });
  },

  updateRole(body: RoleForm) {
    return request<ApiResponse>({
      url: `/system/role/update`,
      method: "put",
      data: body,
    });
  },

  deleteRole(query: DeleteType) {
    return request<ApiResponse>({
      url: `/system/role/delete`,
      method: "delete",
      data: query,
    });
  },

  batchAvailableRole(body: BatchType) {
    return request<ApiResponse>({
      url: `/system/role/available/setting`,
      method: "patch",
      data: body,
    });
  },

  setPermission(body: permissionDataType) {
    return request<ApiResponse>({
      url: `/system/role/permission/setting`,
      method: "patch",
      data: body,
    });
  },

  exportRole(query: TablePageQuery) {
    return request<ApiResponse>({
      url: `/system/role/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },
};

export default RoleAPI;

export interface TablePageQuery extends PageQuery {
  name?: string;
  status?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface RoleTable {
  index?: number;
  id?: number;
  name?: string;
  order?: number;
  data_scope?: number;
  status?: boolean;
  menus?: permissionMenuType[];
  depts?: permissionDeptType[];
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface RoleForm {
  id?: number;
  name?: string;
  order?: number;
  status?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
  menus?: permissionMenuType[];
  depts?: permissionDeptType[];
}

export interface permissionDataType {
  role_ids?: RoleTable["id"][];
  menu_ids?: permissionMenuType["id"][];
  data_scope?: number;
  dept_ids?: number[];
}

export interface permissionDeptType {
  id?: number;
  name?: string;
  parent_id?: number;
  children?: permissionDeptType[];
}

export interface permissionMenuType {
  id?: number;
  name?: string;
  type?: number;
  permission?: string;
  parent_id?: number;
  status?: boolean;
  description?: string;
  children?: permissionMenuType[];
}
