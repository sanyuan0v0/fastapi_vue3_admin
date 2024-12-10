import request from "@/utils/request";

export function getCacheInfo(query) {
  return request({
    url: "/api/v1/monitor/cache/info",
    method: "get",
    params: query,
  });
}

export function getCacheNames() {
  return request({
    url: "/api/v1/monitor/cache/get/names",
    method: "get",
  });
}

export function getCacheKeys(cacheName) {
  return request({
    url: `/api/v1/monitor/cache/get/keys/${cacheName}`,
    method: "get",
  });
}

export function getCacheValue(cacheName, cacheKey) {
  return request({
    url: `/api/v1/monitor/cache/get/value/${cacheName}/${cacheKey}`,
    method: "get",
  });
}

export function deleteCacheName(cacheName) {
  return request({
    url: `/api/v1/monitor/cache/delete/name/${cacheName}`,
    method: "delete",
  });
}

export function deleteCacheKey(cacheKey) {
  return request({
    url: `/api/v1/monitor/cache/delete/key/${cacheKey}`,
    method: "delete",
  });
}

export function deleteCacheAll() {
  return request({
    url: "/api/v1/monitor/cache/delete/all",
    method: "delete",
  });
}
