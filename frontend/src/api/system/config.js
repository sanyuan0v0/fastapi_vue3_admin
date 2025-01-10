import request from "@/utils/request";

export function getConfigInfo() {
  return request({
    url: "/api/v1/system/config/info",
    method: "get",
  });
}


export function updateConfig(body) {
  return request({
    url: "/api/v1/system/config/update",
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
