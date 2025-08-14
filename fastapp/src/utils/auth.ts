import { useUserStore } from "@/store/modules/user.store";
import { Storage } from "./storage";
import { ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY } from "@/constants";

/**
 * 认证工具函数
 *
 * 使用示例：
 *
 * 1. 检查登录状态并自动跳转：
 *    if (!checkLogin()) return; // 未登录会自动跳转到登录页
 *
 * 2. 静默检查登录状态：
 *    if (!isLoggedIn()) {
 *      // 处理未登录逻辑，不会自动跳转
 *    }
 *
 * 3. 强制要求登录：
 *    requireLogin(); // 清除无效状态并跳转到登录页
 */

/**
 * 获取访问令牌
 * @returns 返回访问令牌，如果不存在则返回null
 */
export function getAccessToken(): string {
  return Storage.get<string>(ACCESS_TOKEN_KEY);
}

/**
 * 设置访问令牌
 * @param token 访问令牌
 */
export function setAccessToken(token: string): void {
  Storage.set(ACCESS_TOKEN_KEY, token);
}

/**
 * 获取刷新令牌
 * @returns 返回刷新令牌，如果不存在则返回null
 */
export function getRefreshToken(): string | null {
  return Storage.get<string>(REFRESH_TOKEN_KEY) || null;
}

/**
 * 设置刷新令牌
 * @param token 刷新令牌
 */
export function setRefreshToken(token: string): void {
  Storage.set(REFRESH_TOKEN_KEY, token);
}

/**
 * 清除所有令牌
 */
export function clearTokens(): void {
  Storage.remove(ACCESS_TOKEN_KEY);
  Storage.remove(REFRESH_TOKEN_KEY);
}

/**
 * 检查用户登录状态，未登录则跳转到登录页面
 * @param silent 是否静默检查，不跳转登录页面
 * @returns 返回用户是否已登录
 */
export function checkLogin(silent: boolean = false): boolean {
  const userStore = useUserStore();
  const accessToken = getAccessToken();

  // 检查 token 和用户信息是否都存在
  const isLoggedIn = !!(accessToken && userStore.userInfo);

  if (!isLoggedIn && !silent) {
    try {
      // 获取当前页面路径
      let currentPagePath = "/pages/index/index"; // 默认路径

      const pages = getCurrentPages();
      if (pages && pages.length > 0) {
        const currentPage = pages[pages.length - 1];
        if (currentPage && currentPage.route) {
          currentPagePath = `/${currentPage.route}`;

          // 处理页面参数 - 使用类型断言
          const pageOptions = (currentPage as any).options;
          if (pageOptions && Object.keys(pageOptions).length > 0) {
            const params = new URLSearchParams(pageOptions as Record<string, string>);
            currentPagePath += `?${params.toString()}`;
          }
        }
      }

      // 跳转到登录页面
      uni.navigateTo({
        url: `/pages/login/index?redirect=${encodeURIComponent(currentPagePath)}`,
        fail: (error) => {
          console.error("跳转登录页面失败:", error);
          // 如果 navigateTo 失败，尝试使用 reLaunch
          uni.reLaunch({
            url: "/pages/login/index",
          });
        },
      });
    } catch (error) {
      console.error("检查登录状态时发生错误:", error);
      // 发生错误时，尝试直接跳转到登录页
      uni.reLaunch({
        url: "/pages/login/index",
      });
    }
  }

  return isLoggedIn;
}

/**
 * 检查用户是否已登录（静默检查，不跳转）
 * @returns 返回用户是否已登录
 */
export function isLoggedIn(): boolean {
  return checkLogin(true);
}

/**
 * 强制用户登录，清除无效的登录状态
 */
export function requireLogin(): void {
  const userStore = useUserStore();
  const accessToken = getAccessToken();

  if (!accessToken || !userStore.userInfo) {
    // 清除可能存在的无效状态
    clearTokens();
    userStore.logout();

    // 跳转到登录页
    uni.reLaunch({
      url: "/pages/login/index",
    });
  }
}
