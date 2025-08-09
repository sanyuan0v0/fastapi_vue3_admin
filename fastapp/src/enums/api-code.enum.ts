/**
 * API响应码枚举
 */
export const enum ApiCode {
  /**
   * 成功
   */
  SUCCESS = "00000",

  /**
   * 通用错误
   */
  ERROR = "B0001",

  /**
   * 令牌无效或过期
   */
  TOKEN_INVALID = "A0230",

  /**
   * 令牌已过期
   */
  TOKEN_EXPIRED = "A0231",

  /**
   * 未授权访问
   */
  UNAUTHORIZED = "A0232",

  /**
   * 禁止访问
   */
  FORBIDDEN = "A0233",

  /**
   * 参数校验失败
   */
  PARAM_INVALID = "A0400",

  /**
   * 资源不存在
   */
  NOT_FOUND = "A0404",

  /**
   * 服务器内部错误
   */
  INTERNAL_ERROR = "B0500",
}
