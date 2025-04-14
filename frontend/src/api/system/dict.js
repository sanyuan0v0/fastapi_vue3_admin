import request from "@/utils/request";

export function getDictTypeList(query) {
  return request({
    url: "/api/v1/system/dict/type/list",
    method: "get",
    params: query,
  });
}

export function getDictTypeOptionselect() {
  return request({
    url: "/api/v1/system/dict/type/optionselect",
    method: "get",
  });
}

export function getDictTypeDetail(query) {
  return request({
    url: "/api/v1/system/dict/type/detail",
    method: "get",
    params: query,
  });
}

export function createDictType(body) {
  return request({
    url: "/api/v1/system/dict/type/create",
    method: "post",
    data: body,
  });
}

export function updateDictType(body) {
  return request({
    url: "/api/v1/system/dict/type/update",
    method: "put",
    data: body,
  });
}

export function deleteDictType(query) {
  return request({
    url: "/api/v1/system/dict/type/delete",
    method: "delete",
    params: query,
  });
}

export function exportDictType(body) {
  return request({
    url: "/api/v1/system/dict/type/export",
    method: "post",
    data: body,
    responseType: "blob",
  });
}

export function getDictDataList(query) {
  return request({
    url: "/api/v1/system/dict/data/list",
    method: "get",
    params: query,
  });
}

export function getDictDataDetail(query) {
  return request({
    url: "/api/v1/system/dict/data/detail",
    method: "get",
    params: query,
  });
}

export function createDictData(body) {
  return request({
    url: "/api/v1/system/dict/data/create",
    method: "post",
    data: body,
  });
}

export function updateDictData(body) {
  return request({
    url: "/api/v1/system/dict/data/update",
    method: "put",
    data: body,
  });
}

export function deleteDictData(query) {
  return request({
    url: "/api/v1/system/dict/data/delete",
    method: "delete",
    params: query,
  });
}

export function exportDictData(body) {
  return request({
    url: "/api/v1/system/dict/data/export",
    method: "post",
    data: body,
    responseType: "blob",
  });
}

export function getDictTypeOption() {
  return request({
    url: "/api/v1/system/dict/type/data",
    method: "get",
  });
}

export function getDictDataByType(query) {
  return request({
    url: `/api/v1/system/dict/data/type/${query}`,
    method: "get",
  });
}
