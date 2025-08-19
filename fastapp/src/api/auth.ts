import request from "@/utils/request";
import { ApiHeader } from "@/enums/api-header.enum";

const AUTH_BASE_URL = "/system/auth";

const AuthAPI = {
  /**
   * 登录
   * @param body 登录表单数据
   * @returns 登录结果
   */
  login(body: LoginFormData): Promise<LoginResult> {
    return request<LoginResult>({
      url: `${AUTH_BASE_URL}/login`,
      method: "POST",
      headers: { [ApiHeader.KEY]: ApiHeader.FORM },
      data: body,
      skipAuth: true,
    });
  },

  /**
   * 刷新令牌
   * @param body 刷新令牌请求体
   * @returns 新的访问令牌
   */
  refreshToken(body: RefreshToekenBody): Promise<any> {
    return request<LoginResult>({
      url: `${AUTH_BASE_URL}/token/refresh`,
      method: "POST",
      data: body,
    });
  },

  /**
   * 获取验证码
   * @returns 验证码信息
   */
  getCaptcha(): Promise<any> {
    return request<CaptchaInfo>({
      url: `${AUTH_BASE_URL}/captcha/get`,
      method: "GET",
      skipAuth: true,
    });
  },

  /**
   * 登出
   * @param body 登出请求体
   * @returns 登出结果
   */
  logout(body: LogoutBody): Promise<any> {
    return request<ApiResponse>({
      url: `${AUTH_BASE_URL}/logout`,
      method: "POST",
      data: body,
    });
  },

  /**
   * 微信小程序手机号授权登录
   * @param data 包含code、encryptedData、iv等手机号相关数据
   * @returns 登录结果
   */
  loginByWxMiniAppPhone(data: WxLoginData): Promise<LoginResult> {
    return request<LoginResult>({
      url: `${AUTH_BASE_URL}/wx/miniapp/phone-login`,
      method: "POST",
      data,
      skipAuth: true,
    });
  },

  /**
   * 微信小程序授权登录 (仅使用code获取OpenID)
   * @param code 微信登录凭证
   * @returns 登录结果
   */
  loginByWxMiniAppCode(code: string): Promise<LoginResult> {
    return request<LoginResult>({
      url: `${AUTH_BASE_URL}/wx/miniapp/code-login`,
      method: "POST",
      data: { code },
      skipAuth: true,
    });
  },
};

export default AuthAPI;

export interface WxLoginData {
  code: string;
  encryptedData?: string;
  iv?: string;
  phoneCode?: string;
}

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
