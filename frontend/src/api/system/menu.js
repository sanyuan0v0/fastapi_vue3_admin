import request from "@/utils/request";

export function getMenuList(query) {
  return request({
    url: "/api/v1/system/menu/list",
    method: "get",
    params: query,
  });
}

export function getMenuDetail(query) {
  return request({
    url: "/api/v1/system/menu/detail",
    method: "get",
    params: query,
  });
}

export function createMenu(body) {
  return request({
    url: "/api/v1/system/menu/create",
    method: "post",
    data: body,
  });
}

export function updateMenu(body) {
  return request({
    url: "/api/v1/system/menu/update",
    method: "put",
    data: body,
  });
}

export function deleteMenu(query) {
  return request({
    url: "/api/v1/system/menu/delete",
    method: "delete",
    params: query,
  });
}

export function batchAvailableMenu(body) {
  return request({
    url: "/api/v1/system/menu/available/setting",
    method: "patch",
    data: body,
  });
}

