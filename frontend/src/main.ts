import { createApp } from "vue";
import App from "./App.vue";
import setupPlugins from "@/plugins";

// 暗黑主题样式
import "element-plus/theme-chalk/dark/css-vars.css";
import "element-plus/dist/index.css";
// 暗黑模式自定义变量
import "@/styles/dark/css-vars.css";
import "@/styles/index.scss";
import "uno.css";

// 过渡动画
import "animate.css";

// import { useConfigStore } from "@/store";

const app = createApp(App);
// 注册插件
app.use(setupPlugins);
app.mount("#app");

// 封装设置 title 和 favicon 的函数
// const setTitleAndFavicon = async () => {
//   try {
//     const configStore = useConfigStore();
//     await configStore.getConfig();
//     console.log('配置数据获取成功:', configStore.configData);

//     const loginTitle = configStore.configData.sys_web_title;
//     console.log('sys_web_title:', loginTitle);
//     const loginLogo = configStore.configData.sys_web_favicon;
//     console.log('sys_web_favicon:', loginLogo);

//     if (loginTitle) {
//       document.title = loginTitle;
//     }

//     if (loginLogo) {
//       const favicon = document.querySelector('link[rel="icon"]');
//       if (favicon instanceof HTMLLinkElement) {
//         favicon.href = loginLogo;
//       }
//     }
//   } catch (error) {
//     console.error('获取配置数据失败:', error);
//   }
// };

// // 在 App 组件挂载后执行设置逻辑
// onMounted(setTitleAndFavicon);
