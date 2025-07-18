import { store } from "@/store";
import NoticeAPI, { NoticeTable } from "@/api/system/notice";


export const useNoticeStore = defineStore("notice", {
  state: () => ({
    noticeList: [] as NoticeTable[], // 存储系统配置
    total: 0, // 存储系统配置
    isNoticeLoaded: false, // 标记配置是否已加载
  }),
  actions: {
    async getNotice() {
      const response = await NoticeAPI.getNoticeListAvailable();
      console.log('获取我的通知公告', response);
      this.noticeList = response.data.data.items;
      this.total = response.data.data.total;
      this.isNoticeLoaded = true;
    },
    clearUserInfo() {
      this.noticeList = [];
      this.total = 0;
      this.isNoticeLoaded = false;
    },
  },
  persist: true
});

export function useNoticeStoreHook() {
  return useNoticeStore(store);
}
