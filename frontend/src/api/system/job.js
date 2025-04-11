import request from "@/utils/request";

export function getJobList(query) {
  return request({
    url: "/api/v1/system/job/list",
    method: "get",
    params: query,
  });
}

export function getJobDetail(query) {
  return request({
    url: "/api/v1/system/job/detail",
    method: "get",
    params: query,
  });
}

export function createJob(body) {
  return request({
    url: "/api/v1/system/job/create",
    method: "post",
    data: body,
  });
}

export function updateJob(body) {
  return request({
    url: "/api/v1/system/job/update",
    method: "put",
    data: body,
  });
}

export function deleteJob(query) {
  return request({
    url: "/api/v1/system/job/delete",
    method: "delete",
    params: query,
  });
}

export function exportJob(body) {
  return request({
    url: "/api/v1/system/job/export",
    method: "post",
    data: body,
    responseType: "blob",
  });
}


export function clearJob() {
  return request({
    url: "/api/v1/system/job/clear",
    method: "delete",
  });
}

export function OptionJob(params) {
  return request({
    url: "/api/v1/system/job/option",
    method: "put",
    params: params
  });
}

