import { defineStore } from "pinia";
import { getCurrentUserInfo } from "../api/apis";


export const useUserStore = defineStore('user', {
    state: () => ({
        basic_info: {},
        access_token: uni.getStorageSync('access_token') || '',
        refresh_token: uni.getStorageSync('refresh_token') || null
    }),
    
    getters: {
        baseInfo: (state) => state.basic_info,
        accessToken: (state) => state.access_token,
        refreshToken: (state) => state.refresh_token
    },
    
    actions: {
        async getUserInfo() {
            try {
                const response = await getCurrentUserInfo();
                console.log("获取当前用户", response);
                const result = response.data;
                this.basic_info = { ...this.basic_info, ...result };
            } catch (error) {
                console.error(error);
            }
        },
        
        setToken(new_access_token, new_refresh_token) {
            if (!new_access_token || !new_refresh_token) return false;
            try {
                this.access_token = new_access_token;
                uni.setStorageSync('access_token', new_access_token);
                uni.setStorageSync('refresh_token', new_refresh_token);
                return true;
            } catch (error) {
                console.error('存储token失败:', error);
                return false;
            }
        },
        
        clear() {
            this.basicInfo = {};
            this.access_token = null;
            this.refresh_token = null;
            try {
                uni.removeStorageSync('access_token');
                uni.removeStorageSync('refresh_token');
            } catch (error) {
                console.error('清除存储信息失败:', error);
            }
        }
    }
});