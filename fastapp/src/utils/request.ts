import { getAccessToken } from "./auth";

// 请求配置
interface RequestOptions<T = any> {
  url: string;
  method: "GET" | "POST" | "PUT" | "DELETE";
  data?: T;
  header?: Record<string, string>;
  timeout?: number;
  responseType?: "text" | "arraybuffer";
  skipAuth?: boolean; // 标记是否跳过认证
}

// 请求函数
function request<T = any>(options: RequestOptions): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    // 构建请求头
    const header = Object.assign({}, options.header || {});

    // 检查是否需要添加认证令牌
    if (!options.skipAuth) {
      const token = getAccessToken();
      if (token) {
        header["Authorization"] = `Bearer ${token}`;
      } else {
        // 需要认证但没有令牌，跳转到登录页
        uni.navigateTo({
          url: "/pages/login/index",
        });
        return reject(new Error("请先登录"));
      }
    }

    // 根据平台决定URL前缀
    let requestUrl = options.url;
    // #ifdef MP-WEIXIN
    // 微信小程序环境，使用完整URL
    requestUrl = `${import.meta.env.VITE_APP_API_URL}${options.url}`;
    // #endif

    // #ifndef MP-WEIXIN
    // 非微信小程序环境，使用代理前缀
    requestUrl = `${import.meta.env.VITE_APP_BASE_API}${options.url}`;
    // #endif

    // 统一处理请求
    uni.request({
      url: requestUrl,
      method: options.method,
      data: options.data,
      header,
      timeout: options.timeout || 30000,
      responseType: options.responseType,
      success: (res: any) => {
        // 请求成功
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data.data);
        }
        // 未授权错误
        else if (res.statusCode === 401) {
          // 如果需要认证且未授权，跳转到登录页
          if (!options.skipAuth) {
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

/**
 * 无需认证的请求
 * @param options 请求配置
 */
export function publicRequest<T = any>(options: RequestOptions): Promise<T> {
  return request<T>({
    ...options,
    skipAuth: true,
  });
}

export default request;
