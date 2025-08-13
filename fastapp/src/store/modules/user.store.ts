import { defineStore } from "pinia";
import AuthAPI, {
  type LoginFormData,
  type WxLoginData,
  type LoginResult,
  type LogoutBody,
} from "@/api/auth";
import UserAPI, { type UserInfo } from "@/api/user";
import { getAccessToken, setAccessToken, clearTokens } from "@/utils/auth";
import { getUserInfo, setUserInfo } from "@/utils/storage";
import { USER_INFO_KEY } from "@/constants";
import { Storage } from "@/utils/storage";

export const useUserStore = defineStore("user", () => {
  const userInfo = ref<UserInfo | undefined>(getUserInfo());

  // 账号密码登录
  const login = async (data: LoginFormData) => {
    return new Promise((resolve, reject) => {
      AuthAPI.login(data)
        .then((data: LoginResult) => {
          setAccessToken(data.access_token);
          resolve(data);
        })
        .catch((error) => {
          console.error("登录失败", error);
          reject(error);
        });
    });
  };

  // 微信基础授权登录
  const loginWithWxCode = async (code: string) => {
    try {
      const data = await AuthAPI.loginByWxMiniAppCode(code);
      setAccessToken(data.access_token);
      return data;
    } catch (error: any) {
      console.error("微信授权登录失败", error);
      throw error;
    }
  };

  // 微信手机号授权登录
  const loginWithWxPhone = async (data: WxLoginData): Promise<any> => {
    try {
      const result = await AuthAPI.loginByWxMiniAppPhone(data);
      setAccessToken(result.access_token);
      return result;
    } catch (error: any) {
      console.error("微信手机号登录失败", error);
      throw error;
    }
  };

  // 获取用户信息
  const getInfo = async () => {
    try {
      const userInfo = await UserAPI.getCurrentUserInfo();
      setUserInfo(userInfo);
      return userInfo;
    } catch (error) {
      console.error("获取用户信息失败", error);
      return null;
    }
  };

  // 登出
  const logout = async () => {
    try {
      const logoutBody: LogoutBody = {
        token: getAccessToken(),
      };
      await AuthAPI.logout(logoutBody); // 调用后台注销接口
    } catch (error) {
      console.error("登出失败", error);
    } finally {
      clearTokens(); // 清除本地的 token
      Storage.remove(USER_INFO_KEY); // 清除用户信息缓存
      userInfo.value = undefined; // 清空用户信息
      // 跳转到登录页面
      uni.reLaunch({
        url: "/pages/login/index",
      });
    }
  };

  // 判断用户信息是否完整
  const isUserInfoComplete = (): boolean => {
    if (!userInfo.value) return false;
    return !!(userInfo.value.username && userInfo.value.avatar);
  };

  return {
    userInfo,
    login,
    loginWithWxCode,
    loginWithWxPhone,
    logout,
    getInfo,
    isUserInfoComplete,
  };
});
