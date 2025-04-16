import { request } from "../utils/request";

const contentTypes = {
    form: "application/x-www-form-urlencoded",
    json: "application/json",
    multipart: "multipart/form-data"
};


export function login(data) {
    return request({
        url: "/api/v1/system/auth/login",
        method: "post",
        data: data,
        header: { "Content-Type": contentTypes.form }
    });
}

export function get_captcha() {
    return request({
        url: "/api/v1/system/auth/captcha/get",
        method: "post",
    });
}

export function forgot_password(data) {
    return request({
        url: "/api/v1/system/user/forget/password",
        method: "post",
        data: data
    });
}

export function register(data) {
    return request({
        url: "/api/v1/system/user/register",
        method: "post",
        data: data
    });
}

export function logout(data) {
    return request({
        url: "/api/v1/system/auth/logout",
        method: "post",
        data: data
    });
}

export function getCurrentUserInfo() {
    return request({
        url: "/api/v1/system/user/current/info",
        method: "get",
    });
}
