import type { RouteRecordRaw } from "vue-router";
import router, { constantRoutes } from "@/router";
import { store, useUserStore } from "@/store";
import { listToTree } from "@/utils/common";
import { MenuTable } from "@/api/system/menu";

const modules = import.meta.glob("../../views/**/**.vue");
const Layout = () => import("@/layouts/index.vue");


export interface Meta {
  /** 【目录】只有一个子路由是否始终显示 */
  alwaysShow?: boolean;
  /** 是否隐藏(true-是 false-否) */
  hidden?: boolean;
  /** ICON */
  icon?: string;
  /** 【菜单】是否开启页面缓存 */
  keepAlive?: boolean;
  /** 路由title */
  title?: string;
  /** 排序 */
  order?: number;
  /** 参数 */
  params?: { key: string; value: string; }[];
  /** 是否固定路由 */
  affix?: boolean;
}

// 修改 component 类型，使其能接受动态导入函数
export interface RouteVO {
  /** 子路由列表 */
  children: RouteVO[];
  /** 组件路径或组件导入函数 */
  component?: string | (() => Promise<Component>);
  /** 路由属性 */
  meta?: Meta;
  /** 路由名称 */
  name?: string;
  /** 路由路径 */
  path?: string;
  /** 跳转链接 */
  redirect?: string;
}

export const generator = (routers: MenuTable[]): RouteVO[] => {
    return routers.map((item) => {
      const currentRouter: RouteVO = {
        children: [],
        path: item.route_path,
        name: item.route_name,
        component: item.component_path,
        redirect: item.redirect,
        meta: {
          title: item.title,
          icon: item.icon || undefined,
          keepAlive: item.keep_alive,
          hidden: item.hidden,
          order: item.order,
          alwaysShow: item.always_show,
          params: item.params,
          affix: item.affix,
        },
      };
      if (item.children && item.children.length > 0) {
        currentRouter.children = item.children ? generator(item.children) : [];
      }
      return currentRouter;
    });
};

// router.beforeEach(async (to) => {
//   const accessToken = Auth.getAccessToken();
  
//   const userStore = useUserStore();

//   if (!accessToken && to.name !== "Login") {
//     return { name: "Login" };
//   } else if (accessToken && to.name === "Login") {
//     return { name: "Index" };
//   } else if (accessToken && !userStore.hasGetRoute) {
//     await userStore.getUserInfo();
//     const routersTree = listToTree(userStore.routeList);
//     const routerMap = generator(routersTree);
//     constantRoutes[0].children = [...(constantRoutes[0].children || []), ...routerMap].filter(Boolean) as RouteRecordRaw[];
//     router.addRoute(constantRoutes[0]);
//     return to.fullPath;
//   }
// });

export const usePermissionStore = defineStore("permission", () => {
  // 存储所有路由，包括静态路由和动态路由
  const routes = ref<RouteRecordRaw[]>([]);
  // 混合模式左侧菜单路由
  const sideMenuRoutes = ref<RouteRecordRaw[]>([]);
  // 路由是否加载完成
  const routesLoaded = ref(false);

  /**
   * 获取后台动态路由数据，解析并注册到全局路由
   *
   * @returns Promise<RouteRecordRaw[]> 解析后的动态路由列表
   */
  async function generateRoutes() {
    try {
      const userStore = useUserStore();
      // 确保获取用户信息和路由列表
      if (!userStore.hasGetRoute) {
        await userStore.getUserInfo();
      }

      const routersTree = listToTree(userStore.routeList);
      const routerMap = generator(routersTree);

      // 从用户绑定的路由列表获取数据
      const dynamicRoutes = parseDynamicRoutes(routerMap);

      // 重置路由，移除旧的动态路由
      resetRouter();
      
      // 重新添加所有路由
      constantRoutes.forEach(route => {
        router.addRoute(route);
      });

      routes.value = [...constantRoutes, ...dynamicRoutes];
      
      routesLoaded.value = true;

      return dynamicRoutes;
    } catch (error: any) {
      // 即使失败也要设置状态，避免无限重试
      routesLoaded.value = false;

      throw error;
    }
  }

  /**
   * 根据父菜单路径设置侧边菜单
   *
   * @param parentPath 父菜单的路径，用于查找对应的菜单项
   */
  const updateSideMenu = (parentPath: string) => {
    const matchedItem = routes.value.find((item) => item.path === parentPath);
    if (matchedItem && matchedItem.children) {
      sideMenuRoutes.value = matchedItem.children;
    }
  };

  /**
   * 重置路由
   */
  const resetRouter = () => {
    // 创建常量路由名称集合，用于O(1)时间复杂度的查找
    const constantRouteNames = new Set(constantRoutes.map((route) => route.name).filter(Boolean));

    // 从 router 实例中移除动态路由
    routes.value.forEach((route) => {
      if (route.name && !constantRouteNames.has(route.name)) {
        router.removeRoute(route.name);
      }
    });

    // 重置为仅包含常量路由
    routes.value = [...constantRoutes];
    sideMenuRoutes.value = [];
    routesLoaded.value = false;
  };

  return {
    routes,
    sideMenuRoutes,
    routesLoaded,
    generateRoutes,
    updateSideMenu,
    resetRouter,
  };
});

/**
 * 解析后端返回的路由数据并转换为 Vue Router 兼容的路由配置
 *
 * @param rawRoutes 后端返回的原始路由数据
 * @returns 解析后的路由集合
 */
const parseDynamicRoutes = (rawRoutes: RouteVO[]): RouteRecordRaw[] => {
  const parsedRoutes: RouteRecordRaw[] = [];

  rawRoutes.forEach((route) => {
    const normalizedRoute = { ...route } as RouteRecordRaw;
    // http://localhost:5180/#/dashboard/workplace
    // http://localhost:5180/#/dashboard/workplace

    // 处理组件路径
    normalizedRoute.component =
      !normalizedRoute.component
        ? Layout
        : modules[`../../views/${normalizedRoute.component}.vue`] ||
          modules["../../views/error/404.vue"];

    // 递归解析子路由
    if (normalizedRoute.children) {
      normalizedRoute.children = parseDynamicRoutes(route.children);
    }

    parsedRoutes.push(normalizedRoute);
  });

  return parsedRoutes;
};

/**
 * 导出此hook函数用于在非组件环境(如其他store、工具函数等)中获取权限store实例
 *
 * 在组件中可直接使用usePermissionStore()，但在组件外部需要传入store实例
 * 此函数简化了这个过程，避免每次都手动传入store参数
 */
export function usePermissionStoreHook() {
  return usePermissionStore(store);
}
