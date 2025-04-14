import { defineStore, createPinia } from "pinia";
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import { getCurrentUserInfo } from "@/api/system/user";
import { getInitConfig } from "@/api/system/config";
import { getNoticeList } from '@/api/system/notice'
import { getDictDataByType } from '@/api/system/dict'

// pinia-plugin-persistedstate 持久化存储官方文档：https://prazdevs.github.io/pinia-plugin-persistedstate/zh/guide/
const store = createPinia()

store.use(piniaPluginPersistedstate)


export const useNoticeStore = defineStore("notice", {
  state: () => ({
    noticeList: [], // 存储系统配置
    total: 0, // 存储系统配置
    isNoticeLoaded: false, // 标记配置是否已加载
  }),
  actions: {
    async getNotice() {
      try {
        const response = await getNoticeList({ available: true });
        const { status_code, data } = response.data;
        if (status_code === 200) {
          this.noticeList = data.items;
          this.total = data.total;
          this.isNoticeLoaded = true;
        }
      } catch (error) {
        console.error("获取通知失败", error);
      }
    },
    clearUserInfo() {
      this.noticeList = [];
      this.total = 0;
      this.isNoticeLoaded = false;
    },
  },
});

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
    async getConfig() {
      try {
        const response = await getInitConfig();
        const { status_code, data } = response.data;
        if (status_code === 200) {
          this.configData = data;
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

export const useDictStore = defineStore('dict', {
  state: () => ({
    dictObj: {},
    isLoaded: false,
  }),
  getters: {
    getDictObjData() {
      return this.dictObj
    }
  },
  actions: {
    // 批量获取字典数据
    async setDict(types) {
      try {
        for (const type of types) {
          const response = await getDictDataByType(type)
          const result = response.data;
          if (result.status_code === 200) {
            console.log("参数:",type, "根据字典类型获取字典数据:",result.data);
            // 格式化数据
            this.dictObj[type] = result.data;
            this.isLoaded = true;
          }
        }
      } catch (error) {
        console.error("获取字典数据失败", error);
      }
    },

    getDictLabel(datas, value) {
        const result = datas.find((item) => item.dict_value === value);
        const dict_data = {
          id: result.id,
          dict_value: result.dict_value,
          dict_label: result.dict_label,
          dict_type: result.dict_type,
          css_class: result.css_class,
          list_class: result.list_class,
          is_default: result.is_default,
        }
        return dict_data;
    }
  },
  persist: true
})

