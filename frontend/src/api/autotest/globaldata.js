import request from "@/utils/request";

export function getGlobaldataList(query) {
  return request({
    url: "/api/v1/autotest/globaldata/list",
    method: "get",
    params: query,
  });
}

export function getGlobaldataDetail(query) {
  return request({
    url: "/api/v1/autotest/globaldata/detail",
    method: "get",
    params: query,
  });
}

export function createGlobaldata(body) {
  return request({
    url: "/api/v1/autotest/globaldata/create",
    method: "post",
    data: body,
  });
}

export function updateGlobaldata(body) {
  return request({
    url: "/api/v1/autotest/globaldata/update",
    method: "put",
    data: body,
  });
}

export function deleteGlobaldata(query) {
  return request({
    url: "/api/v1/autotest/globaldata/delete",
    method: "delete",
    params: query,
  });
}

