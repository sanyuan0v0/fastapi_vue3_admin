import request from "@/utils/request";

export function getApiCaseList(query) {
  return request({
    url: "/api/v1/autotest/apicase/list",
    method: "get",
    params: query,
  });
}

export function getApiCaseDetail(query) {
  return request({
    url: "/api/v1/autotest/apicase/detail",
    method: "get",
    params: query,
  });
}

export function createApiCase(body) {
  return request({
    url: "/api/v1/autotest/apicase/create",
    method: "post",
    data: body,
  });
}

export function updateApiCase(body) {
  return request({
    url: "/api/v1/autotest/apicase/update",
    method: "put",
    data: body,
  });
}

export function deleteApiCase(query) {
  return request({
    url: "/api/v1/autotest/apicase/delete",
    method: "delete",
    params: query,
  });
}

