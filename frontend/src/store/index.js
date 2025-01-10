import { defineStore } from "pinia";
import { getCurrentUserInfo } from "@/api/system/user";
import { getInitConfig } from "@/api/system/config";


export const useUserStore = defineStore("user", {
  state: () => ({
    basicInfo: {},
    routeList: [],
    hasGetRoute: false,
  }),
  actions: {
    async getUserInfo() {
      try {
        const response = await getCurrentUserInfo();
        const result = response.data;
        const routers = result.data.menus;
        delete result.data.menus;
        this.setRoute(routers);
        this.basicInfo = { ...this.basicInfo, ...result.data };
      } catch (error) {
        console.error(error);
      }
    },
    setRoute(routers) {
      this.routeList = routers;
      this.hasGetRoute = true;
    },
    setAvatar(avatar) {
      this.basicInfo = { ...this.basicInfo, avatar };
    },
    clearUserInfo() {
      this.basicInfo = {};
      this.routeList = [];
      this.hasGetRoute = false;
    },
  },
});

export const useConfigStore = defineStore("config", {
  state: () => ({
    configData: {}, // 存储系统配置
    isConfigLoaded: false, // 标记配置是否已加载
  }),
  actions: {
    async fetchConfig() {
      try {
        const response = await getInitConfig();
        const { status_code, data } = response.data;
        if (status_code === 200) {
          this.configData = JSON.parse(data);
          console.log(this.configData);
          this.isConfigLoaded = true;
        }
      } catch (error) {
        console.error("获取系统配置失败", error);
      }
    },
    getConfigValue(key) {
      return this.configData[key] || null;
    },
  },
});
