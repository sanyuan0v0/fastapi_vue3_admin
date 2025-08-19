import { getAccessToken } from "./auth";

// 请求配置
interface RequestOptions<T = any> {
  url: string;
  method: "GET" | "POST" | "PUT" | "DELETE";
  data?: T;
  headers?: Record<string, string>;
  timeout?: number;
  responseType?: "text" | "arraybuffer" | "blob" | "json";
  skipAuth?: boolean; // 标记是否跳过认证
}

/**
 * 请求拦截器 - 添加 Authorization 头
 */
function request<T = any>(options: RequestOptions): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    // 构建请求头
    const header = Object.assign({}, options.headers || {});

    // 检查是否需要添加认证令牌
    if (!options.skipAuth) {
      const accessToken = getAccessToken();
      if (accessToken) {
        header["Authorization"] = `Bearer ${accessToken}`;
      } else {
        // 需要认证但没有令牌，跳转到登录页
        // 防止循环跳转：检查当前页面是否已经是登录页
        const currentPages = getCurrentPages();
        const currentPage = currentPages[currentPages.length - 1];
        if (!currentPage || !currentPage.route || !currentPage.route.includes("login")) {
          uni.navigateTo({
            url: "/pages/login/index",
          });
        }
        return reject(new Error("请先登录"));
      }
    }

    // 根据平台决定URL前缀
    let requestUrl = options.url;
    // #ifdef MP-WEIXIN
    // 微信小程序环境，使用完整URL
    requestUrl = `${import.meta.env.VITE_API_BASE_URL}${options.url}`;
    // #endif

    // #ifndef MP-WEIXIN
    // 非微信小程序环境，使用代理前缀
    requestUrl = `${import.meta.env.VITE_APP_BASE_API}${options.url}`;
    // #endif

    let timeout = Number(import.meta.env.VITE_TIMEOUT);
    if (options.timeout) {
      timeout = options.timeout;
    }

    // 统一处理请求
    uni.request({
      url: requestUrl,
      method: options.method,
      data: options.data,
      header: header,
      timeout: timeout,
      responseType: options.responseType,
      success: (res: any) => {
        // 请求成功
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data.data);
        }
        // 未授权错误
        else if (res.statusCode === 401) {
          // 防止循环跳转：检查当前页面是否已经是登录页
          const currentPages = getCurrentPages();
          const currentPage = currentPages[currentPages.length - 1];
          if (!currentPage || !currentPage.route || !currentPage.route.includes("login")) {
            uni.navigateTo({
              url: "/pages/login/index",
            });
          }
          reject(new Error(res.data.message || "未授权，请重新登录"));
        }
        // 其他错误
        else {
          const errorMsg = res.data.message || `请求失败: ${res.statusCode}`;
          reject(new Error(errorMsg));
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg || "网络请求失败"));
      },
    });
  });
}

export default request;
