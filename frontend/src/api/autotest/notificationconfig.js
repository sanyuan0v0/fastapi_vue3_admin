import request from "@/utils/request";

export function getNotificationConfigList(query) {
  return request({
    url: "/api/v1/autotest/notificationconfig/list",
    method: "get",
    params: query,
  });
}

export function getNotificationConfigDetail(query) {
  return request({
    url: "/api/v1/autotest/notificationconfig/detail",
    method: "get",
    params: query,
  });
}

export function createNotificationConfig(body) {
  return request({
    url: "/api/v1/autotest/notificationconfig/create",
    method: "post",
    data: body,
  });
}

export function updateNotificationConfig(body) {
  return request({
    url: "/api/v1/autotest/notificationconfig/update",
    method: "put",
    data: body,
  });
}

export function deleteNotificationConfig(query) {
  return request({
    url: "/api/v1/autotest/notificationconfig/delete",
    method: "delete",
    params: query,
  });
}

