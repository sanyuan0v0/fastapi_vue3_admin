/**
 * 微信授权服务
 * 处理微信登录授权、获取用户信息等功能
 */

import { ref } from "vue";
import { getAccessToken } from "@/utils/auth";

export function useWechat() {
  // 定义微信授权状态
  const authState = ref({
    isLogining: false,
    authDenied: false,
  });

  /**
   * 获取微信登录凭证code
   * @returns Promise 返回登录凭证code
   */
  const getLoginCode = (): Promise<string> => {
    return new Promise((resolve, reject) => {
      // #ifdef MP-WEIXIN
      uni.login({
        provider: "weixin",
        success: (res) => {
          if (res.code) {
            resolve(res.code);
          } else {
            reject(new Error("获取微信登录凭证失败"));
          }
        },
        fail: (err) => {
          reject(err);
        },
      });
      // #endif

      // #ifndef MP-WEIXIN
      reject(new Error("当前环境不支持微信登录"));
      // #endif
    });
  };

  /**
   * 获取微信用户手机号
   * @param e 微信授权返回的事件对象
   * @returns Promise 返回包含手机号加密数据的对象
   */
  const getPhoneNumber = (
    e: any
  ): Promise<{ code: string; encryptedData?: string; iv?: string }> => {
    return new Promise((resolve, reject) => {
      authState.value.isLogining = true;

      // 判断授权是否成功
      if (e.detail.errMsg !== "getPhoneNumber:ok") {
        authState.value.isLogining = false;
        authState.value.authDenied = true;
        reject(new Error("用户拒绝授权"));
        return;
      }

      // 获取登录凭证code
      getLoginCode()
        .then((code) => {
          // 在微信小程序环境下，可以获取encryptedData和iv
          // #ifdef MP-WEIXIN
          resolve({
            code,
            encryptedData: e.detail.encryptedData,
            iv: e.detail.iv,
          });
          // #endif

          // 其他环境或新版本接口
          // #ifndef MP-WEIXIN
          resolve({
            code,
            // 新版本接口在e.detail.code中包含手机号获取凭证
            ...(e.detail.code ? { phoneCode: e.detail.code } : {}),
          });
          // #endif
        })
        .catch((err) => {
          reject(err);
        })
        .finally(() => {
          authState.value.isLogining = false;
        });
    });
  };

  /**
   * 检查会话有效性
   * @returns Promise 返回会话是否有效
   */
  const checkSession = (): Promise<boolean> => {
    return new Promise((resolve) => {
      const token = getAccessToken();

      if (!token) {
        resolve(false);
        return;
      }

      // 调用后端接口验证token有效性
      uni.request({
        url: "/api/v1/auth/check-session",
        method: "GET",
        header: {
          Authorization: `Bearer ${token}`,
        },
        success: (res: any) => {
          if (res.statusCode === 200 && res.data.valid) {
            resolve(true);
          } else {
            resolve(false);
          }
        },
        fail: () => {
          resolve(false);
        },
      });
    });
  };

  /**
   * 获取用户头像昵称
   * 注意：此接口已于2021年弃用，仅作为兼容保留
   * 推荐使用button组件的open-type="chooseAvatar"让用户选择头像
   */
  const getUserProfile = (): Promise<any> => {
    return new Promise((resolve, reject) => {
      // #ifdef MP-WEIXIN
      uni.getUserProfile({
        desc: "用于完善用户资料",
        success: (res) => {
          resolve(res.userInfo);
        },
        fail: (err) => {
          reject(err);
        },
      });
      // #endif

      // #ifndef MP-WEIXIN
      reject(new Error("当前环境不支持获取用户信息"));
      // #endif
    });
  };

  return {
    authState,
    getLoginCode,
    getPhoneNumber,
    checkSession,
    getUserProfile,
  };
}
