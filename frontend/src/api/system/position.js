import request from "@/utils/request";

export function getPositionList(query) {
  return request({
    url: "/api/v1/system/position/list",
    method: "get",
    params: query,
  });
}

export function getPositionDetail(query) {
  return request({
    url: "/api/v1/system/position/detail",
    method: "get",
    params: query,
  });
}

export function createPosition(body) {
  return request({
    url: "/api/v1/system/position/create",
    method: "post",
    data: body,
  });
}

export function updatePosition(body) {
  return request({
    url: "/api/v1/system/position/update",
    method: "put",
    data: body,
  });
}

export function deletePosition(query) {
  return request({
    url: "/api/v1/system/position/delete",
    method: "delete",
    params: query,
  });
}

export function batchAvailablePosition(body) {
  return request({
    url: "/api/v1/system/position/available/setting",
    method: "patch",
    data: body,
  });
}

export function exportPosition(body) {
  return request({
    url: "/api/v1/system/position/export",
    method: "post",
    data: body,
    responseType: 'blob'
  });
}
