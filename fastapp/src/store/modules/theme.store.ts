import { defineStore } from "pinia";
import { ref } from "vue";
import { applyThemeToMiniProgram } from "@/utils/theme";

// 从缓存获取主题色
const getThemeColor = (): string => {
  const savedColor = uni.getStorageSync("themeColor");
  return savedColor || "#165DFF"; // 默认Arco蓝色
};

// 保存主题色到缓存
const setThemeColorCache = (color: string) => {
  uni.setStorageSync("themeColor", color);
};

export const useThemeStore = defineStore("theme", () => {
  // 主题色
  const primaryColor = ref<string>(getThemeColor());

  // 设置主题色
  const setPrimaryColor = (color: string) => {
    primaryColor.value = color;
    setThemeColorCache(color);

    // 检测运行环境，区分处理
    if (typeof document !== "undefined") {
      // H5环境
      document.documentElement.style.setProperty("--primary-color", color);
      document.documentElement.style.setProperty("--wot-color-theme", color);

      // 设置简单的衍生色（不依赖外部工具函数）
      document.documentElement.style.setProperty("--primary-color-light", color + "80"); // 添加透明度
      document.documentElement.style.setProperty("--primary-color-dark", color);
    } else {
      // 小程序环境
      applyThemeToMiniProgram(color);
    }
  };

  // 初始化，应用主题色
  const initTheme = () => {
    setPrimaryColor(primaryColor.value);
  };

  return {
    primaryColor,
    setPrimaryColor,
    initTheme,
  };
});
