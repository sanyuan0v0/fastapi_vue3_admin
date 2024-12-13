import request from "@/utils/request";

export function getCurrentUserInfo() {
  return request({
    url: "/api/v1/system/user/current/info",
    method: "get",
  });
}

export function uploadCurrentUserAvatar(body) {
  return request({
    url: "/api/v1/system/user/current/avatar/upload",
    method: "post",
    data: body,
    headers: { "Content-Type": "multipart/form-data" },
  });
}

export function updateCurrentUserInfo(body) {
  return request({
    url: "/api/v1/system/user/current/info/update",
    method: "put",
    data: body,
  });
}

export function changeCurrentUserPassword(body) {
  return request({
    url: "/api/v1/system/user/current/password/change",
    method: "put",
    data: body,
  });
}

export function registerUser(body) {
  return request({
    url: "/api/v1/system/user/register",
    method: "post",
    data: body,
  });
}

export function forgetPassword(body) {
  return request({
    url: "/api/v1/system/user/forget/password",
    method: "post",
    data: body,
  });
}

export function getUserList(query) {
  return request({
    url: "/api/v1/system/user/list",
    method: "get",
    params: query,
  });
}

export function getUserDetail(query) {
  return request({
    url: "/api/v1/system/user/detail",
    method: "get",
    params: query,
  });
}

export function createUser(body) {
  return request({
    url: "/api/v1/system/user/create",
    method: "post",
    data: body,
  });
}

export function updateUser(body) {
  return request({
    url: "/api/v1/system/user/update",
    method: "put",
    data: body,
  });
}

export function deleteUser(query) {
  return request({
    url: "/api/v1/system/user/delete",
    method: "delete",
    params: query,
  });
}

export function batchAvailableUser(body) {
  return request({
    url: "/api/v1/system/user/available/setting",
    method: "patch",
    data: body,
  });
}

export function exportUser(query) {
  return request({
    url: '/api/v1/system/user/export',
    method: 'post',
    params: query,
    responseType: 'blob'
  })
}

export function downloadTemplate() {
  return request({
    url: '/api/v1/system/user/import/template',
    method: 'post',
    responseType: 'blob'
  })
}

export function importUser(data) {
  return request({
    url: '/api/v1/system/user/import/data',
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
