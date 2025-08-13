// 时间常量
const MILLISECONDS_IN_A_DAY = 24 * 60 * 60 * 1000;
const MILLISECONDS_IN_AN_HOUR = 60 * 60 * 1000;
const MILLISECONDS_IN_A_MINUTE = 60 * 1000;

/**
 * 格式化日期为 YYYY-MM-DD 格式
 * @param date Date对象或可转换为Date的值
 * @returns 格式化后的日期字符串，如 "2023-05-15"
 */
export function formatDate(date: Date | string | number): string {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * 格式化日期时间为 YYYY-MM-DD HH:mm:ss 格式
 * @param date Date对象或可转换为Date的值
 * @returns 格式化后的日期时间字符串，如 "2023-05-15 14:30:45"
 */
export function formatDateTime(date: Date | string | number): string {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hour = String(d.getHours()).padStart(2, '0');
  const minute = String(d.getMinutes()).padStart(2, '0');
  const second = String(d.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

/**
 * 获取两个日期之间的天数差
 * @param start 开始日期
 * @param end 结束日期
 * @returns 天数差（绝对值）
 */
export function getDaysBetween(start: Date, end: Date): number {
  const diff = Math.abs(end.getTime() - start.getTime());
  return Math.floor(diff / MILLISECONDS_IN_A_DAY);
}

/**
 * 在日期上添加指定天数
 * @param date 原始日期
 * @param days 要添加的天数（可为负数）
 * @returns 新的Date对象
 */
export function addDays(date: Date, days: number): Date {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}


/**
 * 检查是否为同一天
 * @param date1 第一个日期
 * @param date2 第二个日期
 * @returns 如果是同一天返回true
 */
export function isSameDay(date1: Date, date2: Date): boolean {
  return (
    date1.getFullYear() === date2.getFullYear() &&
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate()
  );
}

/**
 * 获取当天的开始时间（00:00:00）
 * @param date 日期
 * @returns 当天开始的Date对象
 */
export function getStartOfDay(date: Date): Date {
  const result = new Date(date);
  result.setHours(0, 0, 0, 0);
  return result;
}

/**
 * 获取当天的结束时间（23:59:59.999）
 * @param date 日期
 * @returns 当天结束的Date对象
 */
export function getEndOfDay(date: Date): Date {
  const result = new Date(date);
  result.setHours(23, 59, 59, 999);
  return result;
}
