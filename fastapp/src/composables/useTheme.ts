import type { ConfigProviderThemeVars } from "wot-design-uni";
import { useThemeStore } from "@/store/modules/theme.store";

// 定义主题色选项
export interface ThemeColorOption {
  name: string;
  value: string;
  primary: string;
}

// 预定义的主题色选项
export const themeColorOptions: ThemeColorOption[] = [
  { name: "默认蓝", value: "blue", primary: "#4D7FFF" },
  { name: "活力橙", value: "orange", primary: "#FF7D00" },
  { name: "薄荷绿", value: "green", primary: "#07C160" },
  { name: "樱花粉", value: "pink", primary: "#FF69B4" },
  { name: "紫罗兰", value: "purple", primary: "#8A2BE2" },
  { name: "朱砂红", value: "red", primary: "#FF4757" },
  { name: "天空蓝", value: "sky", primary: "#00BFFF" },
  { name: "柠檬黄", value: "yellow", primary: "#FFD700" },
];

// 扩展的颜色选项，用于自定义颜色选择器
export const extendedColorOptions: ThemeColorOption[] = [
  ...themeColorOptions,
  { name: "珊瑚红", value: "coral", primary: "#FF6B6B" },
  { name: "薄荷绿", value: "mint", primary: "#4ECDC4" },
  { name: "黄金黄", value: "gold", primary: "#FFD166" },
  { name: "经典红", value: "classic-red", primary: "#CD5C5C" },
  { name: "自然绿", value: "nature-green", primary: "#228B22" },
  { name: "天蓝色", value: "sky-blue", primary: "#1890FF" },
  { name: "青绿色", value: "teal", primary: "#0FC6C2" },
  { name: "深紫色", value: "deep-purple", primary: "#722ED1" },
];

export interface ThemeState {
  theme: "light" | "dark";
  isDark: boolean;
  followSystem: boolean;
  hasUserSet: boolean;
  currentThemeColor: ThemeColorOption;
  showThemeColorSheet: boolean;
}

export function useTheme() {
  // 状态定义
  const theme = ref<"light" | "dark">("light");
  const followSystem = ref(true); // 是否跟随系统主题
  const hasUserSet = ref(false); // 用户是否手动设置过主题
  const currentThemeColor = ref<ThemeColorOption>(themeColorOptions[0]);
  const showThemeColorSheet = ref(false);

  // 主题变量
  const themeVars = reactive<ConfigProviderThemeVars>({
    darkBackground: "#0f0f0f",
    darkBackground2: "#1a1a1a",
    darkBackground3: "#242424",
    darkBackground4: "#2f2f2f",
    darkBackground5: "#3d3d3d",
    darkBackground6: "#4a4a4a",
    darkBackground7: "#606060",
    darkColor: "#ffffff",
    darkColor2: "#e0e0e0",
    darkColor3: "#a0a0a0",
    colorTheme: themeColorOptions[0].primary,
  });

  // 计算属性
  const isDark = computed(() => theme.value === "dark");

  // 主题状态
  const themeState = computed(() => ({
    theme: theme.value,
    isDark: isDark.value,
    followSystem: followSystem.value,
    hasUserSet: hasUserSet.value,
    currentThemeColor: currentThemeColor.value,
    showThemeColorSheet: showThemeColorSheet.value,
  }));

  /* 手动切换主题 */
  function toggleTheme(mode?: "light" | "dark") {
    theme.value = mode || (theme.value === "light" ? "dark" : "light");
    hasUserSet.value = true;
    followSystem.value = false;
    setNavigationBarColor();
    saveThemeSettings();

    // 实时应用主题变化
    applyThemeModeToApp();
  }

  /* 实时应用主题模式到应用 */
  function applyThemeModeToApp() {
    // 更新CSS变量
    if (typeof document !== "undefined") {
      document.documentElement.setAttribute("data-theme", theme.value);
    }

    // 更新导航栏颜色
    setNavigationBarColor();
  }

  /* 设置是否跟随系统主题 */
  function setFollowSystem(follow: boolean) {
    followSystem.value = follow;
    if (follow) {
      hasUserSet.value = false;
      initTheme();
    }
    saveThemeSettings();

    // 实时应用主题变化
    applyThemeModeToApp();
  }

  /* 设置主题色 */
  function setCurrentThemeColor(color: ThemeColorOption) {
    currentThemeColor.value = color;
    themeVars.colorTheme = color.primary;
    hasUserSet.value = true;
    saveThemeSettings();

    // 实时应用主题色到全局
    applyThemeColorToApp(color.primary);
  }

  /* 设置自定义主题色 */
  function setCustomThemeColor(color: string) {
    const customTheme: ThemeColorOption = {
      name: "自定义",
      value: "custom",
      primary: color,
    };
    setCurrentThemeColor(customTheme);
  }

  /* 重置主题 */
  function resetTheme() {
    setCurrentThemeColor(themeColorOptions[0]);
    theme.value = "light";
    followSystem.value = true;
    hasUserSet.value = false;
    initTheme();
  }

  /* 保存主题设置到本地存储 */
  function saveThemeSettings() {
    try {
      uni.setStorageSync("theme_settings", {
        theme: theme.value,
        currentThemeColor: currentThemeColor.value,
        followSystem: followSystem.value,
        hasUserSet: hasUserSet.value,
      });
    } catch (error) {
      console.warn("保存主题设置失败:", error);
    }
  }

  /* 从本地存储加载主题设置 */
  function loadThemeSettings() {
    try {
      const settings = uni.getStorageSync("theme_settings");
      if (settings) {
        if (settings.theme && (settings.theme === "light" || settings.theme === "dark")) {
          theme.value = settings.theme;
        }
        if (settings.currentThemeColor) {
          const savedColor =
            themeColorOptions.find((c) => c.value === settings.currentThemeColor.value) ||
            extendedColorOptions.find((c) => c.value === settings.currentThemeColor.value) ||
            settings.currentThemeColor;
          if (savedColor) {
            currentThemeColor.value = savedColor;
            themeVars.colorTheme = savedColor.primary;
          }
        }
        followSystem.value = settings.followSystem !== false;
        hasUserSet.value = settings.hasUserSet === true;
      }
    } catch (error) {
      console.warn("加载主题设置失败:", error);
    }
  }

  /* 获取系统主题 */
  function getSystemTheme(): "light" | "dark" {
    try {
      // #ifdef MP-WEIXIN
      const appBaseInfo = uni.getAppBaseInfo();
      if (appBaseInfo?.theme) {
        return appBaseInfo.theme as "light" | "dark";
      }
      // #endif

      // #ifndef MP-WEIXIN
      const systemInfo = uni.getSystemInfoSync();
      if (systemInfo?.theme) {
        return systemInfo.theme as "light" | "dark";
      }
      // #endif
    } catch (error) {
      console.warn("获取系统主题失败:", error);
    }
    return "light";
  }

  /* 设置导航栏颜色 */
  function setNavigationBarColor() {
    // #ifndef H5
    uni.setNavigationBarColor({
      frontColor: theme.value === "light" ? "#000000" : "#ffffff",
      backgroundColor: theme.value === "light" ? "#ffffff" : "#000000",
    });
    // #endif
  }

  /* 实时应用主题色到应用 */
  function applyThemeColorToApp(color: string) {
    // 更新Wot Design组件库主题色
    themeVars.colorTheme = color;

    // 更新CSS变量
    if (typeof document !== "undefined") {
      document.documentElement.style.setProperty("--wot-color-theme", color);
      document.documentElement.style.setProperty("--primary-color", color);
      document.documentElement.style.setProperty("--primary-color-light", color + "20");
      document.documentElement.style.setProperty("--primary-color-dark", color);
    }

    // 同步到主题存储
    const themeStore = useThemeStore();
    themeStore.setPrimaryColor(color);

    // 通过事件总线通知全局主题变化
    uni.$emit("theme-color-changed", color);

    // 强制刷新页面样式
    setTimeout(() => {
      uni.$emit("force-theme-refresh");
    }, 50);
  }

  /* 初始化主题 */
  function initTheme() {
    if (hasUserSet.value && !followSystem.value) {
      setNavigationBarColor();
      applyThemeColorToApp(currentThemeColor.value.primary);
      return;
    }

    const systemTheme = getSystemTheme();
    if (!hasUserSet.value || followSystem.value) {
      theme.value = systemTheme;
    }

    setNavigationBarColor();
    applyThemeColorToApp(currentThemeColor.value.primary);
  }

  /* 主题色选择器相关 */
  function openThemeColorPicker() {
    showThemeColorSheet.value = true;
  }

  function closeThemeColorPicker() {
    showThemeColorSheet.value = false;
  }

  function selectThemeColor(option: ThemeColorOption) {
    setCurrentThemeColor(option);
    closeThemeColorPicker();
  }

  // 生命周期
  onBeforeMount(() => {
    loadThemeSettings();
    initTheme();

    // #ifdef MP-WEIXIN
    if (uni.onThemeChange) {
      uni.onThemeChange((res: any) => {
        if (followSystem.value) {
          theme.value = res.theme;
          setNavigationBarColor();
        }
      });
    }
    // #endif

    // #ifndef MP-WEIXIN
    if (uni.onThemeChange) {
      uni.onThemeChange((res: any) => {
        if (followSystem.value) {
          theme.value = res.theme;
          setNavigationBarColor();
        }
      });
    }
    // #endif
  });

  onUnmounted(() => {
    // 清理监听器
    if (uni.offThemeChange) {
      uni.offThemeChange(() => {});
    }
  });

  return {
    // 状态
    theme: computed(() => theme.value),
    isDark,
    followSystem: computed(() => followSystem.value),
    hasUserSet: computed(() => hasUserSet.value),
    currentThemeColor: computed(() => currentThemeColor.value),
    showThemeColorSheet: computed(() => showThemeColorSheet.value),
    themeState,

    // 主题选项
    themeColorOptions,
    extendedColorOptions,

    // 主题变量
    themeVars,

    // 方法
    toggleTheme,
    setFollowSystem,
    setCurrentThemeColor,
    setCustomThemeColor,
    resetTheme,
    initTheme,

    // 主题色选择器
    openThemeColorPicker,
    closeThemeColorPicker,
    selectThemeColor,

    // 工具方法
    saveThemeSettings,
    loadThemeSettings,
  };
}
