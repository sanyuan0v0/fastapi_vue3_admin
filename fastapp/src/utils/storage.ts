/**
 * 存储工具类
 * 提供localStorage和sessionStorage操作方法
 */

/**
 * localStorage 存储
 */
function set(key: string, value: any): void {
  uni.setStorageSync(key, JSON.stringify(value));
}

function get<T>(key: string, defaultValue?: T): T {
  const value = uni.getStorageSync(key);
  if (!value) return defaultValue as T;

  try {
    return JSON.parse(value);
  } catch {
    // 如果解析失败，返回原始字符串
    return value as unknown as T;
  }
}

function remove(key: string): void {
  uni.removeStorageSync(key);
}

export const Storage = {
  set,
  get,
  remove,
};

// 为了向后兼容，导出具体的函数
import { ACCESS_TOKEN_KEY, USER_INFO_KEY } from "@/constants";

/**
 * 获取令牌
 */
export function getToken(): string | null {
  return Storage.get<string>(ACCESS_TOKEN_KEY) || null;
}

/**
 * 设置令牌
 */
export function setToken(token: string): void {
  Storage.set(ACCESS_TOKEN_KEY, token);
}

/**
 * 获取用户信息
 */
export function getUserInfo<T = any>(): T | undefined {
  return Storage.get<T>(USER_INFO_KEY);
}

/**
 * 设置用户信息
 */
export function setUserInfo(userInfo: any): void {
  Storage.set(USER_INFO_KEY, userInfo);
}

/**
 * 清除所有数据
 */
export function clearAll(): void {
  Storage.remove(ACCESS_TOKEN_KEY);
  Storage.remove(USER_INFO_KEY);
}
