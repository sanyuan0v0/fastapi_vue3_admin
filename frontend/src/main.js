import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";
import VChart from "vue-echarts";
import "echarts";
import './style.css'
import { createPinia } from 'pinia';
import { useConfigStore } from "@/store/index";

import VueCron from 'vue-cron'; // 确保已经正确安装并定位到正确的路径
// import 'vue-cron/dist/vue-cron.css'; // 引入样式

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(VueCron);

const initConfig = async () => {
  const configStore = useConfigStore();
  await configStore.getConfig();

  const loginTitle = configStore.getConfigValue("title");
  const loginLogo = configStore.getConfigValue("favicon");

  if (loginTitle) {
    document.title = loginTitle;
  }

  if (loginLogo) {
    const favicon = document.querySelector('link[rel="icon"]');
    if (favicon) {
      favicon.href = loginLogo;
    }
  }
};

// 初始化配置并挂载应用
initConfig().then(() => {
  app.use(router);
  app.use(Antd);
  app.component("VChart", VChart);
  app.mount("#app");
});
