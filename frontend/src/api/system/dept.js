import request from "@/utils/request";

export function getDeptList(query) {
  return request({
    url: "/api/v1/system/dept/list",
    method: "get",
    params: query,
  });
}

export function getDeptDetail(query) {
  return request({
    url: "/api/v1/system/dept/detail",
    method: "get",
    params: query,
  });
}

export function createDept(body) {
  return request({
    url: "/api/v1/system/dept/create",
    method: "post",
    data: body,
  });
}

export function updateDept(body) {
  return request({
    url: "/api/v1/system/dept/update",
    method: "put",
    data: body,
  });
}

export function deleteDept(query) {
  return request({
    url: "/api/v1/system/dept/delete",
    method: "delete",
    params: query,
  });
}

export function batchAvailableDept(body) {
  return request({
    url: "/api/v1/system/dept/available/setting",
    method: "patch",
    data: body,
  });
}

