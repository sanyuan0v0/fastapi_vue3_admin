import request from "@/utils/request";

export function getNoticeList(query) {
  return request({
    url: "/api/v1/system/notice/list",
    method: "get",
    params: query,
  });
}

export function getNoticeDetail(query) {
  return request({
    url: "/api/v1/system/notice/detail",
    method: "get",
    params: query,
  });
}

export function createNotice(body) {
  return request({
    url: "/api/v1/system/notice/create",
    method: "post",
    data: body,
  });
}

export function updateNotice(body) {
  return request({
    url: "/api/v1/system/notice/update",
    method: "put",
    data: body,
  });
}

export function deleteNotice(query) {
  return request({
    url: "/api/v1/system/notice/delete",
    method: "delete",
    params: query,
  });
}

export function batchAvailableNotice(body) {
  return request({
    url: "/api/v1/system/notice/available/setting",
    method: "patch",
    data: body,
  });
}

export function exportNotice(body) {
  return request({
    url: "/api/v1/system/notice/export",
    method: "post",
    data: body,
    responseType: 'blob'
  });
}
