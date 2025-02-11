import request from "@/utils/request";

export function getUICaseList(query) {
  return request({
    url: "/api/v1/autotest/uicase/list",
    method: "get",
    params: query,
  });
}

export function getUICaseDetail(query) {
  return request({
    url: "/api/v1/autotest/uicase/detail",
    method: "get",
    params: query,
  });
}

export function createUICase(body) {
  return request({
    url: "/api/v1/autotest/uicase/create",
    method: "post",
    data: body,
  });
}

export function updateUICase(body) {
  return request({
    url: "/api/v1/autotest/uicase/update",
    method: "put",
    data: body,
  });
}

export function deleteUICase(query) {
  return request({
    url: "/api/v1/autotest/uicase/delete",
    method: "delete",
    params: query,
  });
}

