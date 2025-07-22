import { store } from "@/store";
import DictAPI, { DictDataTable } from "@/api/system/dict";

export const useDictStore = defineStore("dict", {
  state: () => ({
    dictData: {} as Record<string, DictDataTable[]>,
    isLoaded: false,
  }),
  getters: {
    getDictData(): Record<string, DictDataTable[]> {
      return this.dictData;
    },
  },
  actions: {
    // 批量获取字典数据
    async getDict(types: string[]) {
      try {
        for (const type of types) {
          const response = await DictAPI.getInitDict(type);
          this.dictData[type] = response.data.data as DictDataTable[];
          this.isLoaded = true;
        }
      } catch (error) {
        console.error("获取字典数据失败", error);
      }
    },

    getDictLabel(type: string, value: string) {
      const result = this.dictData[type].find((item) => item.dict_value === value);
      if (!result) {
        return value;
      }
      const dict_data = {
        id: result.id,
        dict_value: result.dict_value,
        dict_label: result.dict_label,
        dict_type: result.dict_type,
        css_class: result.css_class,
        list_class: result.list_class,
        is_default: result.is_default,
      };
      return dict_data;
    },
  },
  persist: true,
});

export function useDictStoreHook() {
  return useDictStore(store);
}
