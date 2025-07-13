import request from "@/utils/request";

const AuthAPI = {
  login(body: LoginFormData) {
    return request<ApiResponse<LoginResult>>({
      url: `/system/auth/login`,
      method: "post",
      headers: {
        "Content-Type": "multipart/form-data",
      },
      data: body,
    });
  },

  refreshToken(body: RefreshToekenBody) {
    return request<ApiResponse<LoginResult>>({
      url: `/system/auth/token/refresh`,
      method: "post",
      data: body,
    });
  },

  getCaptcha() {
    return request<ApiResponse<CaptchaInfo>>({
      url: `/system/auth/captcha/get`,
      method: "get",
    });
  },

  logout(body: LogoutBody) {
    return request<ApiResponse>({
      url: `/system/auth/logout`,
      method: "post",
      data: body,
    });
  },
};

export default AuthAPI;

/** 登录表单数据 */
export interface LoginFormData {
  username: string;
  password: string;
  captcha_key: string;
  captcha: string;
  remember: boolean;
}

// 刷新令牌
export interface RefreshToekenBody {
  refresh_token: string;
}

/** 登录响应 */
export interface LoginResult {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

/** 验证码信息 */
export interface CaptchaInfo {
  enable: boolean;
  key: string;
  img_base: string;
}

/** 退出登录操作 */
export interface LogoutBody {
  token: string;
}
