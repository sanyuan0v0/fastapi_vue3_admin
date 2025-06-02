import request from "@/utils/request";

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
    url: "/api/v1/system/config/info",
    method: "get",
  });
}


export function getConfigList(query) {
  return request({
    url: "/api/v1/system/config/list",
    method: "get",
    params: query,
  });
}

export function getConfigDetail(query) {
  return request({
    url: "/api/v1/system/config/detail",
    method: "get",
    params: query,
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

export function deleteConfig(query) {
  return request({
    url: "/api/v1/system/config/delete",
    method: "delete",
    params: query,
  });
}

export function exportConfig(body) {
  return request({
    url: "/api/v1/system/config/export",
    method: "post",
    data: body,
    responseType: "blob",
  });
}



