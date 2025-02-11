import request from "@/utils/request";

export function getProjectList(query) {
  return request({
    url: "/api/v1/autotest/project/list",
    method: "get",
    params: query,
  });
}

export function getProjectDetail(query) {
  return request({
    url: "/api/v1/autotest/project/detail",
    method: "get",
    params: query,
  });
}

export function createProject(body) {
  return request({
    url: "/api/v1/autotest/project/create",
    method: "post",
    data: body,
  });
}

export function updateProject(body) {
  return request({
    url: "/api/v1/autotest/project/update",
    method: "put",
    data: body,
  });
}

export function deleteProject(query) {
  return request({
    url: "/api/v1/autotest/project/delete",
    method: "delete",
    params: query,
  });
}

