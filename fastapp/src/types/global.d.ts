declare global {
  /**
   * 分页查询参数
   */
  interface PageQuery {
    pageNum: number;
    pageSize: number;
  }

  /**
   * 分页响应对象
   */
  interface PageResult<T> {
    /** 数据列表 */
    list: T;
    /** 总数 */
    total: number;
  }

  /**
   * 组件数据源
   */
  interface OptionType {
    /** 值 */
    value: string | number;
    /** 文本 */
    label: string;
    /** 子列表  */
    children?: OptionType[];
  }

  /**
   * 响应数据
   */
  interface ResponseData<T = any> {
    code: string;
    data: T;
    msg: string;
  }
}
export {};
