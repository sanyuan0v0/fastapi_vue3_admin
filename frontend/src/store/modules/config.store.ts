import { store } from "@/store";
import ConfigAPI, { ConfigTable } from "@/api/system/config";

interface ConfigState {
  sys_git_code: ConfigTable;
  sys_help_doc: ConfigTable;
  sys_keep_record: ConfigTable;
  sys_login_background: ConfigTable;
  sys_web_clause: ConfigTable;
  sys_web_copyright: ConfigTable;
  sys_web_description: ConfigTable;
  sys_web_favicon: ConfigTable;
  sys_web_logo: ConfigTable;
  sys_web_privacy: ConfigTable;
  sys_web_title: ConfigTable;
  sys_web_version: ConfigTable;
}

export const useConfigStore = defineStore("config", {
  state: () => ({
    configData: {} as ConfigState, // 存储系统配置
    isConfigLoaded: false, // 标记配置是否已加载
  }),

  actions: {
    async getConfig() {
      const response = await ConfigAPI.getInitConfig();
      response.data.data.forEach((item: ConfigTable) => {
        // 确保所有配置项都正确映射到 configData
        if (item.config_value !== undefined) {
          this.configData[item.config_key as keyof ConfigState] = item;
        }
      });
      this.isConfigLoaded = true;
    }
  },
  persist: true
});

export function useConfigStoreHook() {
  return useConfigStore(store);
}