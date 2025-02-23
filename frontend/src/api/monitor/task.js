import request from "@/utils/request";

export function getTaskList() {
  return request({
    url: "/api/v1/monitor/task/list",
    method: "get",
  });
}

export function getTaskDetail(taskId) {
  return request({
    url: `/api/v1/monitor/task/detail/${taskId}`,
    method: "get",
  });
}


export function createTask(body) {
  return request({
      url: "/api/v1/monitor/task/create",
      method: "post",
      data: body,
  });
}

export function cancelTask(taskId) {
  return request({
    url: `/api/v1/monitor/task/cancel/${taskId}`,
    method: "put",
  });
}

export function deleteTask(taskId) {
  return request({
    url: `/api/v1/monitor/task/delete/${taskId}`,
    method: "delete",
  });
}