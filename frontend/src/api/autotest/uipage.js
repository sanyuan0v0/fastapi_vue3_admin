import request from "@/utils/request";

export function getUIPageList(query) {
  return request({
    url: "/api/v1/autotest/uipage/list",
    method: "get",
    params: query,
  });
}

export function getUIPageDetail(query) {
  return request({
    url: "/api/v1/autotest/uipage/detail",
    method: "get",
    params: query,
  });
}

export function createUIPage(body) {
  return request({
    url: "/api/v1/autotest/uipage/create",
    method: "post",
    data: body,
  });
}

export function updateUIPage(body) {
  return request({
    url: "/api/v1/autotest/uipage/update",
    method: "put",
    data: body,
  });
}

export function deleteUIPage(query) {
  return request({
    url: "/api/v1/autotest/uipage/delete",
    method: "delete",
    params: query,
  });
}

