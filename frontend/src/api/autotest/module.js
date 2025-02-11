import request from "@/utils/request";

export function getModuleList(query) {
  return request({
    url: "/api/v1/autotest/module/list",
    method: "get",
    params: query,
  });
}

export function getModuleDetail(query) {
  return request({
    url: "/api/v1/autotest/module/detail",
    method: "get",
    params: query,
  });
}

export function createModule(body) {
  return request({
    url: "/api/v1/autotest/module/create",
    method: "post",
    data: body,
  });
}

export function updateModule(body) {
  return request({
    url: "/api/v1/autotest/module/update",
    method: "put",
    data: body,
  });
}

export function deleteModule(query) {
  return request({
    url: "/api/v1/autotest/module/delete",
    method: "delete",
    params: query,
  });
}

