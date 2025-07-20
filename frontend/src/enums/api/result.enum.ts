/**
 * 响应码枚举
 */
export const enum ResultEnum {
  /**
   * 成功
   */
  SUCCESS = 0,
  /**
   * 错误
   */
  ERROR = 1,
  /**
   * 异常
   */
  EXCEPTION = -1,

  /**
   * 访问令牌无效或过期
   */
  ACCESS_TOKEN_INVALID = 401,

  /**
   * 拒绝访问
   */
  ACCESS_DENIED = 403,
}
