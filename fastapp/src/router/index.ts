import { pages, subPackages } from "virtual:uni-pages";
import { isLoggedIn } from "@/utils/auth";
import { createRouter } from "uni-mini-router";

// 生成路由配置
function generateRoutes() {
  const routes = pages.map((page: { path: string; [key: string]: any }) => {
    const newPath = `/${page.path}`;
    return { ...page, path: newPath };
  });

  // 处理分包路由
  if (subPackages && subPackages.length > 0) {
    subPackages.forEach((subPackage: { root: string; pages: any[] }) => {
      const subRoutes = subPackage.pages.map((page: any) => {
        const newPath = `/${subPackage.root}/${page.path}`;
        return { ...page, path: newPath };
      });
      routes.push(...subRoutes);
    });
  }
  return routes;
}

// 创建路由实例
const router = createRouter({
  routes: generateRoutes(),
});

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 检查页面是否需要登录
  if (to.meta && to.meta.requireAuth && !isLoggedIn()) {
    uni.showModal({
      title: "提示",
      content: "该功能需要登录后使用",
      confirmText: "去登录",
      cancelText: "返回",
      success: (res) => {
        if (res.confirm) {
          // 记住原来要去的页面
          uni.setStorageSync("redirect", to.fullPath);
          // 使用 uni 原生导航而不是 router
          uni.navigateTo({
            url: "/pages/login/index",
          });
        } else {
          // 取消则返回首页
          uni.switchTab({
            url: "/pages/index/index",
          });
        }
      },
      // 确保在取消弹窗时也能调用 next
      fail: () => {
        next(false);
      },
    });
  } else {
    // 继续导航
    next();
  }
});

router.afterEach((to) => {
  console.log("路由跳转完成:", to.path);
});

export default router;
