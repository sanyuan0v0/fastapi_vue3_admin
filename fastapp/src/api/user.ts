import request from "@/utils/request";

const USER_BASE_URL = "/api/v1/system/user";

const UserAPI = {
  /**
   * 个人中心用户信息
   *
   * @returns 登录用户昵称、头像信息，包括角色和权限
   */
  getCurrentUserInfo(): Promise<UserInfo> {
    return request<UserInfo>({
      url: `${USER_BASE_URL}/current/info`,
      method: "GET",
    });
  },

  /**
   * 当前用户头像上传
   *
   * @param body
   * @returns 上传后的文件路径
   */
  uploadCurrentUserAvatar(body: any): Promise<UploadFilePath> {
    return request<UploadFilePath>({
      url: `${USER_BASE_URL}/current/avatar/upload`,
      method: "POST",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  /**
   * 修改个人中心用户信息
   *
   * @param body
   * @returns 修改后的用户信息
   */
  updateCurrentUserInfo(body: UserProfileForm): Promise<UserInfo> {
    return request<UserInfo>({
      url: `${USER_BASE_URL}/current/info/update`,
      method: "PUT",
      data: body,
    });
  },

  /**
   * 修改个人中心用户密码
   *
   * @param body
   * @returns 修改后的用户信息
   */
  changeCurrentUserPassword(body: PasswordChangeForm): Promise<ApiResponse> {
    return request<ApiResponse>({
      url: `${USER_BASE_URL}/current/password/change`,
      method: "PUT",
      data: body,
    });
  },

  /**
   * 注册用户
   *
   * @param body
   * @returns 忘记密码结果
   */
  registerUser(body: RegisterForm): Promise<ApiResponse> {
    return request<ApiResponse>({
      url: `${USER_BASE_URL}/register`,
      method: "POST",
      data: body,
    });
  },

  /**
   * 忘记密码
   *
   * @param body
   * @returns 忘记密码结果
   */
  forgetPassword(body: ForgetPasswordForm): Promise<ApiResponse> {
    return request<ApiResponse>({
      url: `${USER_BASE_URL}/forget/password`,
      method: "POST",
      data: body,
    });
  },

  /**
   * 获取用户分页列表
   *POST
   * @param queryParams 查询参数
   */
  getUserPage(queryParams: UserPageQuery): Promise<PageResult<UserInfo[]>> {
    return request<PageResult<UserInfo[]>>({
      url: `${USER_BASE_URL}/list`,
      method: "GET",
      data: queryParams,
    });
  },

  /**
   * 获取用户表单详情
   *
   * @param userId 用户ID
   * @returns 用户表单详情
   */
  getUserDetail(userId: number): Promise<UserForm> {
    return request<UserForm>({
      url: `${USER_BASE_URL}/detail/${userId}`,
      method: "GET",
    });
  },

  /**
   * 添加用户
   *
   * @param body 用户表单数据
   */
  addUser(body: UserForm): Promise<ApiResponse> {
    return request<ApiResponse>({
      url: `${USER_BASE_URL}/create`,
      method: "POST",
      data: body,
    });
  },

  /**
   * 修改用户
   *
   * @param body 用户表单数据
   */
  updateUser(body: UserForm): Promise<ApiResponse> {
    return request({
      url: `${USER_BASE_URL}/update`,
      method: "PUT",
      data: body,
    });
  },

  /**
   * 删除用户
   *
   * @param ids 用户ID数组
   */
  deleteUser(ids: number[]): Promise<ApiResponse> {
    return request<ApiResponse>({
      url: `/system/user/delete`,
      method: "DELETE",
      data: ids,
    });
  },
};

export default UserAPI;

/* 忘记密码表单 */
export interface ForgetPasswordForm {
  username: string;
  new_password: string;
  confirmPassword: string;
}

/* 注册表单 */
export interface RegisterForm {
  username: string;
  password: string;
  confirmPassword: string;
}

/* 分页查询表单 */
export interface UserPageQuery extends PageQuery {
  username?: string;
  name?: string;
  status?: boolean;
  dept_id?: number;
  start_time?: string;
  end_time?: string;
}

/* 搜索选择器数据类型 */
export interface searchSelectDataType {
  name?: string;
  status?: string;
}

/* 用户表单 */
export interface UserForm {
  id?: number;
  username?: string;
  name?: string;
  dept_id?: number;
  dept_name?: string;
  role_ids?: number[];
  roleNames?: string[];
  position_ids?: number[];
  positionNames?: string[];
  password?: string;
  gender?: number;
  email?: string;
  mobile?: string;
  is_superuser?: boolean;
  status?: boolean;
  description?: string;
}

/* 登录用户信息 */
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
  roleNames?: roleSelectorType["name"][];
  role_ids?: roleSelectorType["id"][];
  positions?: positionSelectorType[];
  positionNames?: positionSelectorType["name"][];
  position_ids?: positionSelectorType["id"][];
  is_superuser?: boolean;
  status?: boolean;
  description?: string;
  last_login?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

/* 菜单表 */
export interface MenuTable {
  index?: number;
  id?: number;
  name?: string;
  type?: number;
  icon?: string;
  order?: number;
  permission?: string;
  route_name?: string;
  route_path?: string;
  component_path?: string;
  redirect?: string;
  parent_id?: number;
  parent_name?: string;
  keep_alive?: boolean;
  hidden?: boolean;
  always_show?: boolean;
  title?: string;
  params?: { key: string; value: string }[];
  affix?: boolean;
  status?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  children?: MenuTable[];
}

/* 部门树 */
export interface deptTreeType {
  id?: number;
  name?: string;
  parent_id?: number;
  children?: deptTreeType[];
}

/* 角色选择器 */
export interface roleSelectorType {
  id?: number;
  name?: string;
  status?: boolean;
  description?: string;
}

/* 职位选择器 */
export interface positionSelectorType {
  id?: number;
  name?: string;
  status?: boolean;
  description?: string;
}

/* 个人中心用户信息表单 */
export interface UserProfileForm {
  id?: number;
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

/* 修改密码表单 */
export interface PasswordChangeForm {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

/* 重置密码表单 */
export interface ResetPasswordForm {
  id: number;
  password: string;
}

/* 修改手机表单 */
export interface MobileBindingForm {
  /** 手机号 */
  mobile?: string;
  /** 验证码 */
  code?: string;
}

/* 修改邮箱表单 */
export interface EmailBindingForm {
  /** 邮箱 */
  email?: string;
  /** 验证码 */
  code?: string;
}

/* 微信手机号授权数据 */
export interface WechatPhoneData {
  /** 微信授权码 */
  code: string;
  /** 加密数据 */
  encryptedData?: string;
  /** 初始向量 */
  iv?: string;
}

/* 手机号获取结果 */
export interface PhoneNumberResult {
  /** 手机号 */
  phoneNumber: string;
  /** 纯手机号（去除+86） */
  purePhoneNumber?: string;
  /** 国家代码 */
  countryCode?: string;
}
