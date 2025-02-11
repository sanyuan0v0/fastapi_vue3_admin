import request from "@/utils/request";

export function getEnvironmentList(query) {
  return request({
    url: "/api/v1/autotest/environment/list",
    method: "get",
    params: query,
  });
}

export function getEnvironmentDetail(query) {
  return request({
    url: "/api/v1/autotest/environment/detail",
    method: "get",
    params: query,
  });
}

export function createEnvironment(body) {
  return request({
    url: "/api/v1/autotest/environment/create",
    method: "post",
    data: body,
  });
}

export function updateEnvironment(body) {
  return request({
    url: "/api/v1/autotest/environment/update",
    method: "put",
    data: body,
  });
}

export function deleteEnvironment(query) {
  return request({
    url: "/api/v1/autotest/environment/delete",
    method: "delete",
    params: query,
  });
}

