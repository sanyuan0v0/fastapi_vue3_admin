import request from "@/utils/request";

export function getFileList(query) {
  return request({
    url: "/api/v1/common/file/list",
    method: "get",
    params: query,
  });
}

export function uploadFile(body) {
  return request({
    url: "/api/v1/common/file/upload",
    method: "post",
    data: body,
  });
}

export function downloadFile(query) {
  return request({
    url: "/api/v1/common/file/download",
    method: "get",
    params: query,
  });
}

export function downloadFileResource(query) {
  return request({
    url: "/api/v1/common/file/download/resource",
    method: "get",
    params: query,
  });
}

export function uploadFileOne(body) {
  return request({
    url: "/api/v1/common/file/upload/one",
    method: "post",
    data: body,
  });
}

export function uploadFileMany(body) {
  return request({
    url: "/api/v1/common/file/upload/many",
    method: "post",
    data: body,
  });
}
