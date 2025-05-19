import { createRouter, createWebHistory } from "vue-router";
import storage from "store";

import BasicLayout from "@/layouts/basicLayout.vue";
import { listToTree } from "@/utils/util";
import { useUserStore } from "@/store/index";

const modules = import.meta.glob("../views/**/**.vue");

export const generator = (routers) => {
  return routers.map((item) => {
    const currentRouter = {
      path: item.route_path,
      name: item.route_name,
      component: item.component_path
        ? modules[`../views/${item.component_path}.vue`]
        : null,
      redirect: item.redirect,
      meta: {
        title: item.name,
        icon: item.icon || undefined,
        keepAlive: item.cache,
        hidden: item.hidden,
        order: item.order,
      },
    };
    if (item.children && item.children.length > 0) {
      currentRouter.children = generator(item.children);
    }
    return currentRouter;
  });
};


const routes = [
  { path: "/login", 
    name: "Login", 
    component: () => import("../views/system/auth/login.vue"), },
  {
    path: "/403",
    name: "403",
    meta: { title: "403" },
    component: () => import("../views/exception/403.vue"),
  },
  {
    path: "/404",
    name: "404",
    meta: { title: "404" },
    component: () => import("../views/exception/404.vue"),
  },
  {
    path: "/500",
    name: "500",
    meta: { title: "500" },
    component: () => import("../views/exception/500.vue"),
  },
  {
    path: "/:catchAll(.*)",
    name: "404",
    meta: { title: "404" },
    component: () => import("../views/exception/404.vue"),
  },
];

const rootRouter = {
  path: "/",
  name: "Index",
  redirect: "/dashboard",
  component: BasicLayout,
  children: [
    {
      path: "/profile",
      name: "Profile",
      meta: {
        title: "个人中心",
        keepAlive: true,
      },
      component: () => import("../views/current/profile.vue"),
    },
  ],
};

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const token = storage.get("Access-Token");
  const userStore = useUserStore();

  if (!token && to.name !== "Login") {
    return { name: "Login" };
  } else if (token && to.name === "Login") {
    return { name: "Index" };
  } else if (token && !userStore.hasGetRoute) {
    await userStore.getUserInfo();
    const routersTree = listToTree(userStore.routeList);
    const routerMap = generator(routersTree);
    rootRouter.children = [...rootRouter.children, ...routerMap];
    router.addRoute(rootRouter);
    return to.fullPath;
  }
});
export default router;
