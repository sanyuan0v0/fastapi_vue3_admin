/**
 * 小程序主题工具类
 * 用于解决小程序环境中CSS变量不能动态设置的问题
 */

// 注入小程序环境的全局样式
export function applyThemeToMiniProgram(primaryColor: string) {
  // 确保在小程序环境中执行
  if (typeof document !== "undefined") return;

  try {
    // 设置TabBar样式
    uni.setTabBarStyle({
      color: "#000000",
      selectedColor: primaryColor,
      backgroundColor: "#ffffff",
      borderStyle: "black",
    });

    console.log("小程序主题色已应用:", primaryColor);
  } catch (error) {
    console.error("应用小程序主题色失败:", error);
  }
}

// 在页面展示时应用主题
export function applyThemeOnPageShow(primaryColor: string) {
  // 各平台小程序可能需要不同处理
  const platform = uni.getSystemInfoSync().platform;
  console.log(`当前平台: ${platform}, 应用主题色: ${primaryColor}`);

  // 某些平台可能需要特定处理
}
