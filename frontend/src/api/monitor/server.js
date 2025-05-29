import request from "@/utils/request";

// 获取服务信息
export function getServer() {
  return request({
    url: '/api/v1/monitor/server/info',
    method: 'get'
  })
}