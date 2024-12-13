import request from "@/utils/request";

export function getRoleList(query) {
  return request({
    url: "/api/v1/system/role/list",
    method: "get",
    params: query,
  });
}

export function getRoleDetail(query) {
  return request({
    url: "/api/v1/system/role/detail",
    method: "get",
    params: query,
  });
}

export function createRole(body) {
  return request({
    url: "/api/v1/system/role/create",
    method: "post",
    data: body,
  });
}

export function updateRole(body) {
  return request({
    url: "/api/v1/system/role/update",
    method: "put",
    data: body,
  });
}

export function deleteRole(query) {
  return request({
    url: "/api/v1/system/role/delete",
    method: "delete",
    params: query,
  });
}

export function batchAvailableRole(body) {
  return request({
    url: "/api/v1/system/role/available/setting",
    method: "patch",
    data: body,
  });
}

export function setPermission(body) {
  return request({
    url: "/api/v1/system/role/permission/setting",
    method: "patch",
    data: body,
  });
}

export function exportRole(body) {
  return request({
    url: "/api/v1/system/role/export",
    method: "post",
    data: body,
    responseType: 'blob'
  });
}
