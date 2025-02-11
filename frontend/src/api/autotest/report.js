import request from "@/utils/request";

export function getReportList(query) {
  return request({
    url: "/api/v1/autotest/report/list",
    method: "get",
    params: query,
  });
}

export function getReportDetail(query) {
  return request({
    url: "/api/v1/autotest/report/detail",
    method: "get",
    params: query,
  });
}

export function createReport(body) {
  return request({
    url: "/api/v1/autotest/report/create",
    method: "post",
    data: body,
  });
}

export function updateReport(body) {
  return request({
    url: "/api/v1/autotest/report/update",
    method: "put",
    data: body,
  });
}

export function deleteReport(query) {
  return request({
    url: "/api/v1/autotest/report/delete",
    method: "delete",
    params: query,
  });
}

