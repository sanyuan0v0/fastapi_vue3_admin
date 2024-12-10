import request from "@/utils/request";

export function login(body) {
  return request({
    url: "/api/v1/system/auth/login",
    method: "post",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    data: body,
  });
}

export function getNewToken(body) {
  return request({
    url: "/api/v1/system/auth/token/refresh",
    method: "post",
    data: body,
  });
}

export function getCaptcha() {
  return request({
    url: "/api/v1/system/auth/captcha/get",
    method: "post",
  });
}

export function logout(body) {
  return request({
    url: "/api/v1/system/auth/logout",
    method: "post",
    data: body,
  });
}
