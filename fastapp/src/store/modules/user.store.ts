import { defineStore } from "pinia";
import AuthAPI, { type LoginData, type WxLoginData } from "@/api/auth";
import UserAPI, { type UserInfo } from "@/api/user";
import { setAccessToken, clearTokens } from "@/utils/auth";
import { getUserInfo, setUserInfo } from "@/utils/storage";
import { USER_INFO_KEY } from "@/constants";
import { Storage } from "@/utils/storage";

export const useUserStore = defineStore("user", () => {
  const userInfo = ref<UserInfo | undefined>(getUserInfo());

  // 账号密码登录
  const login = (data: LoginData) => {
    return new Promise((resolve, reject) => {
      AuthAPI.login(data)
        .then((data) => {
          setAccessToken(data.accessToken);
          resolve(data);
        })
        .catch((error) => {
          console.error("登录失败", error);
          reject(error);
        });
    });
  };

  // 微信基础授权登录
  const loginWithWxCode = (code: string) => {
    return new Promise((resolve, reject) => {
      AuthAPI.loginByWxMiniAppCode(code)
        .then((data) => {
          setAccessToken(data.accessToken);
          resolve(data);
        })
        .catch((error: any) => {
          console.error("微信授权登录失败", error);
          reject(error);
        });
    });
  };

  // 微信手机号授权登录
  const loginWithWxPhone = (data: WxLoginData): Promise<any> => {
    return new Promise((resolve, reject) => {
      AuthAPI.loginByWxMiniAppPhone(data)
        .then((result: any) => {
          setAccessToken(result.accessToken);
          resolve(result);
        })
        .catch((error: any) => {
          console.error("微信手机号登录失败", error);
          reject(error);
        });
    });
  };

  // 检查会话状态
  const checkSession = (): Promise<boolean> => {
    return new Promise((resolve) => {
      AuthAPI.checkSession()
        .then((result) => {
          resolve(result.valid);
        })
        .catch(() => {
          resolve(false);
        });
    });
  };

  // 获取用户信息
  const getInfo = () => {
    return new Promise((resolve, reject) => {
      UserAPI.getUserInfo()
        .then((data) => {
          setUserInfo(data);
          userInfo.value = data;
          resolve(data);
        })
        .catch((error) => {
          console.error("获取用户信息失败", error);
          reject(error);
        });
    });
  };

  // 登出
  const logout = async () => {
    try {
      await AuthAPI.logout(); // 调用后台注销接口
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

    return !!(userInfo.value.nickname && userInfo.value.avatar);
  };

  return {
    userInfo,
    login,
    loginWithWxCode,
    loginWithWxPhone,
    logout,
    getInfo,
    checkSession,
    isUserInfoComplete,
  };
});
