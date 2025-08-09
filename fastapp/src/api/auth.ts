import request, { publicRequest } from "@/utils/request";

const AUTH_BASE_URL = "/api/v1/auth";

export interface LoginData {
  username: string;
  password: string;
}

export interface WxLoginData {
  code: string;
  encryptedData?: string;
  iv?: string;
  phoneCode?: string;
}

export interface LoginResult {
  accessToken: string;
  refreshToken?: string;
  tokenType: string;
  expiresIn: number;
  isNewUser?: boolean;
  isProfileComplete?: boolean;
}

const AuthAPI = {
  /**
   * 账号密码登录
   * @param data 登录表单数据
   * @returns 登录结果
   */
  login(data: LoginData): Promise<LoginResult> {
    const formData = {
      username: data.username,
      password: data.password,
    };

    return publicRequest<LoginResult>({
      url: `${AUTH_BASE_URL}/login`,
      method: "POST",
      data: formData,
      header: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
  },

  /**
   * 微信小程序授权登录 (仅使用code获取OpenID)
   * @param code 微信登录凭证
   * @returns 登录结果
   */
  loginByWxMiniAppCode(code: string): Promise<LoginResult> {
    return publicRequest<LoginResult>({
      url: `${AUTH_BASE_URL}/wx/miniapp/code-login`,
      method: "POST",
      data: { code },
    });
  },

  /**
   * 微信小程序手机号授权登录
   * @param data 包含code、encryptedData、iv等手机号相关数据
   * @returns 登录结果
   */
  loginByWxMiniAppPhone(data: WxLoginData): Promise<LoginResult> {
    return publicRequest<LoginResult>({
      url: `${AUTH_BASE_URL}/wx/miniapp/phone-login`,
      method: "POST",
      data,
    });
  },

  /**
   * 检查会话有效性
   * @returns 会话是否有效
   */
  checkSession(): Promise<{ valid: boolean }> {
    return request<{ valid: boolean }>({
      url: `${AUTH_BASE_URL}/check-session`,
      method: "GET",
    });
  },

  /**
   * 登出
   * @returns 登出结果
   */
  logout(): Promise<any> {
    return request<any>({
      url: `${AUTH_BASE_URL}/logout`,
      method: "POST",
    });
  },

  /**
   * 刷新令牌
   * @param refreshToken 刷新令牌
   * @returns 新的访问令牌
   */
  refreshToken(refreshToken: string): Promise<{ accessToken: string; expiresIn: number }> {
    return publicRequest<{ accessToken: string; expiresIn: number }>({
      url: `${AUTH_BASE_URL}/refresh-token`,
      method: "POST",
      data: { refreshToken },
    });
  },
};

export default AuthAPI;
