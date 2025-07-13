import { store, useTagsViewStore, usePermissionStoreHook } from "@/store";

import AuthAPI, {type LoginFormData } from "@/api/system/auth";
import UserAPI, {type UserInfo }  from "@/api/system/user";
import type { MenuTable } from "@/api/system/menu";

import { Auth } from "@/utils/auth";

export const useUserStore = defineStore("user", {
  state: () => ({
    basicInfo: {} as UserInfo,
    routeList: [] as MenuTable[],
    hasGetRoute: false,

    // 记住我状态
    rememberMe: ref(Auth.getRememberMe()),
  }),

  getters: {
    getBasicInfo: (state) => state.basicInfo,
    getRouteList: (state) => state.routeList,
    getHasGetRoute: (state) => state.hasGetRoute,
  },

  actions: {
    // 获取用户信息
    async getUserInfo() {
      const response = await UserAPI.getCurrentUserInfo();
      const routers = response.data.data.menus;
      delete response.data.data.menus;
      this.setRoute(routers);
      this.basicInfo = { ...this.basicInfo, ...response.data.data };
    },

    setRoute(routers: any) {
      this.routeList = routers;
      this.hasGetRoute = true;
    },
    setAvatar(avatar: string) {
      this.basicInfo = { ...this.basicInfo, avatar };
    },
    clearUserInfo() {
      this.basicInfo = {};
      this.routeList = [];
      this.hasGetRoute = false;
    },
    
    // 登录
    login(LoginFormData: LoginFormData) {
      return new Promise<void>((resolve, reject) => {
        AuthAPI.login(LoginFormData)
          .then((response) => {
            // 保存记住我状态和token
            this.rememberMe = LoginFormData.remember;
            Auth.setTokens(response.data.data.access_token, response.data.data.refresh_token, this.rememberMe);
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },

    // 登出
    logout() {
      return new Promise<void>((resolve, reject) => {
        AuthAPI.logout({token: Auth.getAccessToken()})
          .then(() => {
            // 重置所有系统状态
            this.resetAllState();
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },

    // 重置所有状态
    resetAllState() {
      // 重置用户状态
      Auth.clearAuth();
      // 重置路由
      usePermissionStoreHook().resetRouter();
      // 清除标签视图
      useTagsViewStore().delAllViews();

      return Promise.resolve();
    },

    // 刷新token
    refreshToken() {
      const refreshToken = Auth.getRefreshToken();

      if (!refreshToken) {
        return Promise.reject(new Error("没有有效的刷新令牌"));
      }

      return new Promise<void>((resolve, reject) => {
        AuthAPI.refreshToken({refresh_token: refreshToken})
          .then((data) => {
            // 更新令牌，保持当前记住我状态
            Auth.setTokens(data.access_token, data.refresh_token, Auth.getRememberMe());
            resolve();
          })
          .catch((error) => {
            console.log(" refreshToken  刷新失败", error);
            reject(error);
          });
      });
    }
  },

  persist: true

});


/**
 * 在组件外部使用UserStore的钩子函数
 * @see https://pinia.vuejs.org/core-concepts/outside-component-usage.html
 */
export function useUserStoreHook() {
  return useUserStore(store);
}
