import request from "@/utils/request";

export function getUIElementList(query) {
  return request({
    url: "/api/v1/autotest/uielement/list",
    method: "get",
    params: query,
  });
}

export function getUIElementDetail(query) {
  return request({
    url: "/api/v1/autotest/uielement/detail",
    method: "get",
    params: query,
  });
}

export function createUIElement(body) {
  return request({
    url: "/api/v1/autotest/uielement/create",
    method: "post",
    data: body,
  });
}

export function updateUIElement(body) {
  return request({
    url: "/api/v1/autotest/uielement/update",
    method: "put",
    data: body,
  });
}

export function deleteUIElement(query) {
  return request({
    url: "/api/v1/autotest/uielement/delete",
    method: "delete",
    params: query,
  });
}

