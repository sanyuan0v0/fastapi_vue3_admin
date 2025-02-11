import request from "@/utils/request";

export function getSuiteList(query) {
  return request({
    url: "/api/v1/autotest/suite/list",
    method: "get",
    params: query,
  });
}

export function getSuiteDetail(query) {
  return request({
    url: "/api/v1/autotest/suite/detail",
    method: "get",
    params: query,
  });
}

export function createSuite(body) {
  return request({
    url: "/api/v1/autotest/suite/create",
    method: "post",
    data: body,
  });
}

export function updateSuite(body) {
  return request({
    url: "/api/v1/autotest/suite/update",
    method: "put",
    data: body,
  });
}

export function deleteSuite(query) {
  return request({
    url: "/api/v1/autotest/suite/delete",
    method: "delete",
    params: query,
  });
}

