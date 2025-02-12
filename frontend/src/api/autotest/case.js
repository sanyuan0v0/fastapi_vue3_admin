import request from "@/utils/request";

export function getCaseList(query) {
  return request({
    url: "/api/v1/autotest/case/list",
    method: "get",
    params: query,
  });
}

export function getCaseDetail(query) {
  return request({
    url: "/api/v1/autotest/case/detail",
    method: "get",
    params: query,
  });
}

export function createCase(body) {
  return request({
    url: "/api/v1/autotest/case/create",
    method: "post",
    data: body,
  });
}

export function updateCase(body) {
  return request({
    url: "/api/v1/autotest/case/update",
    method: "put",
    data: body,
  });
}

export function deleteCase(query) {
  return request({
    url: "/api/v1/autotest/case/delete",
    method: "delete",
    params: query,
  });
}

