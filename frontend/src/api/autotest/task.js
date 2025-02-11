import request from "@/utils/request";

export function getTaskList(query) {
  return request({
    url: "/api/v1/autotest/task/list",
    method: "get",
    params: query,
  });
}

export function getTaskDetail(query) {
  return request({
    url: "/api/v1/autotest/task/detail",
    method: "get",
    params: query,
  });
}

export function createTask(body) {
  return request({
    url: "/api/v1/autotest/task/create",
    method: "post",
    data: body,
  });
}

export function updateTask(body) {
  return request({
    url: "/api/v1/autotest/task/update",
    method: "put",
    data: body,
  });
}

export function deleteTask(query) {
  return request({
    url: "/api/v1/autotest/task/delete",
    method: "delete",
    params: query,
  });
}

