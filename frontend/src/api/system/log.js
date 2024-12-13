import request from "@/utils/request";

export function getLogList(query) {
  return request({
    url: "/api/v1/system/log/list",
    method: "get",
    params: query,
  });
}

export function getLogDetail(query) {
  return request({
    url: "/api/v1/system/log/detail",
    method: "get",
    params: query,
  });
}

export function deleteLog(query) {
  return request({
    url: "/api/v1/system/log/delete",
    method: "delete",
    params: query,
  });
}

export function exportLog(query) {
  return request({
    url: '/api/v1/system/log/export',
    method: 'post',
    data: query,
    responseType: 'blob',
  })
}
