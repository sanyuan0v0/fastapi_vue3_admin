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

export function batchConfig(body) {
  return request({
    url: "/api/v1/system/config/batch",
    method: "put",
    data: body,
  });
}

export function uploadFile(body) {
  return request({
    url: "/api/v1/system/config/upload",
    method: "post",
    data: body,
    headers: { "Content-Type": "multipart/form-data" },
  });
}

export function getInitConfig() {
  return request({
    url: "/api/v1/system/config/init",
    method: "get",
  });
}
