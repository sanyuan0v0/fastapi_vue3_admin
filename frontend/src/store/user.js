import { defineStore } from 'pinia';
import { getCurrentUserInfo } from "@/api/system/user";

export const useUserStore = defineStore('user', {
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
        this.basicInfo = Object.assign(this.basicInfo || {}, result.data);
      } catch (error) {
        console.error(error);
      }
    },
    setRoute(routers) {
      this.routeList = routers;
      this.hasGetRoute = true;
    },
    setAvatar(avatar) {
      this.basicInfo.avatar = avatar;
    },
    clearUserInfo() {
      this.basicInfo = {};
      this.routeList = [];
      this.hasGetRoute = false;
    },
  },
});