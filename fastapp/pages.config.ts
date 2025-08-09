// pages.config.ts
import { defineUniPages } from "@uni-helper/vite-plugin-uni-pages";

export default defineUniPages({
  // 你也可以定义 pages 字段，它具有最高的优先级。
  pages: [],
  globalStyle: {
    // 导航栏配置
    navigationBarBackgroundColor: "@navBgColor",
    navigationBarTextStyle: "@navTxtStyle",
    navigationBarTitleText: "Wot-Demo",

    // 页面背景配置
    backgroundColor: "@bgColor",
    backgroundTextStyle: "@bgTxtStyle",
    backgroundColorTop: "@bgColorTop",
    backgroundColorBottom: "@bgColorBottom",

    // 下拉刷新配置
    enablePullDownRefresh: false,
    onReachBottomDistance: 50,

    // 动画配置
    animationType: "pop-in",
    animationDuration: 300,
  },

  tabBar: {
    custom: true,
    // #ifdef MP-ALIPAY
    customize: true,
    // 暂时不生效。4.71.2025061206-alpha已修复：https://uniapp.dcloud.net.cn/release-note-alpha.html#_4-71-2025061206-alpha，我们等正式版发布后更新。
    overlay: true,
    // #endif
    height: "0",
    color: "@tabColor",
    selectedColor: "@tabSelectedColor",
    backgroundColor: "@tabBgColor",
    borderStyle: "@tabBorderStyle",
    list: [
      {
        pagePath: "pages/index/index",
      },
      {
        pagePath: "pages/mine/index",
      },
    ],
  },
});
