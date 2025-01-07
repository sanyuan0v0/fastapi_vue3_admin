import request from "@/utils/request";

export function getConfigList(params) {
  return request({
    url: "/api/v1/system/config/list",
    method: "get",
    params: params,
  });
}

export function getConfigDetail(params) {
  return request({
    url: "/api/v1/system/config/detail",
    method: "get",
    params: params,
  });
}

export function createConfig(body) {
  return request({
    url: "/api/v1/system/config/create",
    method: "post",
    data: body,
  });
}

export function updateConfig(body) {
  return request({
    url: "/api/v1/system/config/update",
    method: "put",
    data: body,
  });
}

export function deleteConfig(params) {
  return request({
    url: "/api/v1/system/config/delete",
    method: "delete",
    params: params,
  });
}

