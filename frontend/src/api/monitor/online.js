import request from "@/utils/request";

// 查询在线用户列表
export function getOnlineList(query) {
  return request({
    url: '/monitor/online/list',
    method: 'get',
    params: query
  })
}

// 强退用户
export function deleteOnline(body) {
  return request({
    url: "/monitor/online/delete",
    method: "delete",
    data: body,
  });
}
