import request from "@/utils/request";
import { MenuTable } from "@/api/system/menu";

export const UserAPI = {
  getCurrentUserInfo() {
    return request<ApiResponse<UserInfo>>({
      url: `/system/user/current/info`,
      method: "get",
    });
  },

  uploadCurrentUserAvatar(body: any) {
    return request<ApiResponse>({
      url: `/system/user/current/avatar/upload`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  updateCurrentUserInfo(body: any) {
    return request<ApiResponse>({
      url: `/system/user/current/info/update`,
      method: "put",
      data: body,
    });
  },

  changeCurrentUserPassword(body: any) {
    return request<ApiResponse>({
      url: `/system/user/current/password/change`,
      method: "put",
      data: body,
    });
  },

  registerUser(body: RegisterForm) {
    return request<ApiResponse>({
      url: `/system/user/register`,
      method: "post",
      data: body,
    });
  },

  forgetPassword(body: ForgetPasswordForm) {
    return request<ApiResponse>({
      url: `/system/user/forget/password`,
      method: "post",
      data: body,
    });
  },

  getUserList(query: any) {
    return request<ApiResponse>({
      url: `/system/user/list`,
      method: "get",
      params: query,
    });
  },

  getUserDetail(query: any) {
    return request<ApiResponse>({
      url: `/system/user/detail`,
      method: "get",
      params: query,
    });
  },

  createUser(body: any) {
    return request<ApiResponse>({
      url: `/system/user/create`,
      method: "post",
      data: body,
    });
  },

  updateUser(body: any) {
    return request<ApiResponse>({
      url: `/system/user/update`,
      method: "put",
      data: body,
    });
  },

  deleteUser(query: any) {
    return request<ApiResponse>({
      url: `/system/user/delete`,
      method: "delete",
      params: query,
    });
  },

  batchAvailableUser(body: any) {
    return request<ApiResponse>({
      url: `/system/user/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportUser(query: any) {
    return request<ApiResponse>({
      url: `/system/user/export`,
      method: "post",
      params: query,
      responseType: "blob",
    });
  },

  downloadTemplate() {
    return request<ApiResponse>({
      url: `/system/user/import/template`,
      method: "post",
      responseType: "blob",
    });
  },

  importUser(body: any) {
    return request<ApiResponse>({
      url: `/system/user/import/data`,
      method: "post",
      data: body,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

export default UserAPI;

export interface ForgetPasswordForm {
  username: string;
  new_password: string;
  confirmPassword: string;
}

export interface RegisterForm {
  username: string;
  password: string;
  confirmPassword: string;
}

export interface UserPageQuery extends PageQuery {
  username?: string;
  name?: string;
  status?: boolean;
  dept_id?: number;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface searchSelectDataType {
  name?: string;
  status?: string;
}

export interface UserInfo {
  index?: number;
  id?: number;
  username?: string;
  name?: string;
  avatar?: string;
  email?: string;
  mobile?: string;
  gender?: string;
  password?: string;
  menus?: MenuTable[];
  dept?: deptTreeType;
  dept_id?: deptTreeType["id"];
  dept_name?: deptTreeType["name"];
  roles?: roleSelectorType[];
  roleNames?: string;
  role_ids?: roleSelectorType["id"][];
  positions?: positionSelectorType[];
  positionNames?: string;
  position_ids?: positionSelectorType["id"][];
  is_superuser?: boolean;
  status?: boolean;
  description?: string;
  last_login?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface deptTreeType {
  id?: number;
  name?: string;
  parent_id?: number;
  children?: deptTreeType[];
}

export interface roleSelectorType {
  id?: number;
  name?: string;
  status?: boolean;
  description?: string;
}

export interface positionSelectorType {
  id?: number;
  name?: string;
  status?: boolean;
  description?: string;
}

export interface InfoFormState {
  name: string;
  gender: number;
  mobile: string;
  email: string;
  username: string;
  dept_name: string;
  positions: positionSelectorType[];
  roles: roleSelectorType[];
  avatar: string;
  created_at: string;
}

export interface PasswordFormState {
  oldPassword: string;
  newPassword: string;
  confirmPassword: string;
}

export interface UserForm {
  id: undefined;
  username: string;
  name: string;
  dept_id?: undefined | number;
  dept_name?: undefined | string;
  role_ids?: undefined | number[];
  roleNames?: undefined | string;
  position_ids?: undefined | number[];
  positionNames?: undefined | string;
  password: string;
  gender?: undefined | number;
  email?: string;
  mobile?: string;
  is_superuser?: boolean;
  status?: boolean;
  description?: string;
}
