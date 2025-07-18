import request from "@/utils/request";

const MenuAPI = {
  getMenuList(query: MenuPageQuery) {
    return request<ApiResponse<PageResult<MenuTable[]>>>({
      url: `/system/menu/list`,
      method: "get",
      params: query,
    });
  },

  getMenuDetail(query: number) {
    return request<ApiResponse<MenuTable>>({
      url: `/system/menu/detail/${query}`,
      method: "get",
    });
  },

  createMenu(body: MenuForm) {
    return request<ApiResponse>({
      url: `/system/menu/create`,
      method: "post",
      data: body,
    });
  },

  updateMenu(body: MenuForm) {
    return request<ApiResponse>({
      url: `/system/menu/update`,
      method: "put",
      data: body,
    });
  },

  deleteMenu(body: number[]) {
    return request<ApiResponse>({
      url: `/system/menu/delete`,
      method: "delete",
      data: body,
    });
  },

  batchAvailableMenu(body: BatchType) {
    return request<ApiResponse>({
      url: `/system/menu/available/setting`,
      method: "patch",
      data: body,
    });
  },
};

export default MenuAPI;

export interface MenuPageQuery extends PageQuery {
  name?: string;
  status?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface MenuTable {
  index?: number;
  id?: number;
  name?: string;
  type?: number;
  icon?: string;
  order?: number;
  permission?: string;
  route_name?: string;
  route_path?: string;
  component_path?: string;
  redirect?: string;
  parent_id?: number;
  parent_name?: string;
  keep_alive?: boolean;
  hidden?: boolean;
  always_show?: boolean;
  title?: string;
  params?: string;
  affix?: boolean;
  status?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  children?: MenuTable[];
}

export interface MenuForm {
  id?: number;
  name?: string;
  type?: number;
  icon?: string;
  order?: number;
  permission?: string;
  route_name?: string;
  route_path?: string;
  component_path?: string;
  redirect?: string;
  parent_id?: number;
  keep_alive?: boolean;
  hidden?: boolean;
  always_show?: boolean;
  title?: string;
  params?: string;
  affix?: boolean;
  status?: boolean;
  description?: string;
}
