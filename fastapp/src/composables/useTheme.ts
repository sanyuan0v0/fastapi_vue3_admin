import type { ConfigProviderThemeVars } from "wot-design-uni";

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
];

export function useTheme() {
  // 状态定义
  const theme = ref<"light" | "dark">("light");
  const followSystem = ref(true); // 是否跟随系统主题
  const hasUserSet = ref(false); // 用户是否手动设置过主题
  const currentThemeColor = ref<ThemeColorOption>(themeColorOptions[0]);
  const showThemeColorSheet = ref(false);

  const colorColumns = [
    { value: "#165DFF", label: "蓝色" },
    { value: "#0FC6C2", label: "青绿色" },
    { value: "#722ED1", label: "紫色" },
    { value: "#F5222D", label: "红色" },
    { value: "#FA8C16", label: "橙色" },
    { value: "#FADB14", label: "黄色" },
    { value: "#52C41A", label: "绿色" },
    { value: "#EB2F96", label: "粉色" },
    { value: "#13C2C2", label: "青色" },
    { value: "#1890FF", label: "天蓝色" },
    { value: "#CD5C5C", label: "经典红" },
    { value: "#228B22", label: "自然绿" },
    { value: "#FF6B6B", label: "珊瑚红" },
    { value: "#4ECDC4", label: "薄荷绿" },
    { value: "#FFD166", label: "黄金黄色" },
  ];

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

  /* 手动切换主题 */
  function toggleTheme(mode?: "light" | "dark") {
    theme.value = mode || (theme.value === "light" ? "dark" : "light");
    hasUserSet.value = true; // 标记用户已手动设置
    followSystem.value = false; // 不再跟随系统
    setNavigationBarColor();
  }

  /* 设置是否跟随系统主题 */
  function setFollowSystem(follow: boolean) {
    followSystem.value = follow;
    if (follow) {
      hasUserSet.value = false;
      initTheme(); // 重新获取系统主题
    }
  }

  /* 设置导航栏颜色 */
  function setNavigationBarColor() {
    uni.setNavigationBarColor({
      frontColor: theme.value === "light" ? "#000000" : "#ffffff",
      backgroundColor: theme.value === "light" ? "#ffffff" : "#000000",
    });
  }

  /* 设置主题色 */
  function setCurrentThemeColor(color: ThemeColorOption) {
    currentThemeColor.value = color;
    themeVars.colorTheme = color.primary;
  }

  /* 获取系统主题 */
  function getSystemTheme(): "light" | "dark" {
    try {
      // #ifdef MP-WEIXIN
      // 微信小程序使用 getAppBaseInfo
      const appBaseInfo = uni.getAppBaseInfo();
      if (appBaseInfo && appBaseInfo.theme) {
        return appBaseInfo.theme as "light" | "dark";
      }
      // #endif

      // #ifndef MP-WEIXIN
      // 其他平台使用 getSystemInfoSync
      const systemInfo = uni.getSystemInfoSync();
      if (systemInfo && systemInfo.theme) {
        return systemInfo.theme as "light" | "dark";
      }
      // #endif
    } catch (error) {
      console.warn("获取系统主题失败:", error);
    }
    return "light"; // 默认返回 light
  }

  /* 初始化主题 */
  function initTheme() {
    // 如果用户已手动设置且不跟随系统，保持当前主题
    if (hasUserSet.value && !followSystem.value) {
      console.log("使用用户设置的主题:", theme.value);
      setNavigationBarColor();
      return;
    }

    // 获取系统主题
    const systemTheme = getSystemTheme();

    // 如果是首次启动或跟随系统，使用系统主题
    if (!hasUserSet.value || followSystem.value) {
      theme.value = systemTheme;
      if (!hasUserSet.value) {
        followSystem.value = true;
      } else {
        console.log("跟随系统主题:", theme.value);
      }
    }

    setNavigationBarColor();
  }

  /* 打开主题色选择 */
  function openThemeColorPicker() {
    showThemeColorSheet.value = true;
  }

  /* 关闭主题色选择 */
  function closeThemeColorPicker() {
    showThemeColorSheet.value = false;
  }

  /* 选择主题色 */
  function selectThemeColor(option: ThemeColorOption) {
    setCurrentThemeColor(option);
    closeThemeColorPicker();
  }

  // 检查函数是否存在的工具函数
  const isFunction = (fn: any): boolean => typeof fn === "function";

  onBeforeMount(() => {
    initTheme();
    if (isFunction(uni.onThemeChange)) {
      uni.onThemeChange((res) => {
        toggleTheme(res.theme);
      });
    }
  });

  onUnmounted(() => {
    if (isFunction(uni.offThemeChange)) {
      uni.offThemeChange((res) => {
        toggleTheme(res.theme);
      });
    }
  });

  return {
    theme: computed(() => theme.value),
    isDark,
    colorColumns,
    followSystem: computed(() => followSystem.value),
    hasUserSet: computed(() => hasUserSet.value),
    currentThemeColor: computed(() => currentThemeColor.value),
    showThemeColorSheet,
    themeVars,
    themeColorOptions,
    initTheme,
    toggleTheme,
    setFollowSystem,
    openThemeColorPicker,
    closeThemeColorPicker,
    selectThemeColor,
  };
}
