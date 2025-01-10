import { defineStore } from 'pinia';
import { getInitConfig } from "@/api/system/config";

export const useConfigStore = defineStore('config', {
  state: () => ({
    systemConfig: {},
  }),
  actions: {
    async getConfigInfo() {
      try {
        const response = await getInitConfig();
        const result = response.data;
        const configData = JSON.parse(result.data);
        this.systemConfig = configData;
      } catch (error) {
        console.error(error);
      }
    },
    setSystemConfig(config) {
      this.systemConfig = config;
    },
    clearConfigInfo() {
      this.systemConfig = {};
    },
  },
});