import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";
import VChart from "vue-echarts";
import "echarts";
import './style.css'

import { getInitConfig } from "@/api/system/config"

const app = createApp(App);

const initConfig = () => {
    return getInitConfig()
        .then((response) => {
            const { status_code, data } = response.data;
            if (status_code === 200) {
                const configData = JSON.parse(data);
                configData.forEach((item) => {
                    if (item.fied_key === "login_title") {
                        document.title = item.fied_value || "fastapi vue admin";
                    } else if (item.fied_key === "login_logo") {
                        const favicon = document.querySelector('link[rel="icon"]');
                        if (favicon) {
                            favicon.href = item.fied_value || "/logo.png";
                    }
                }
            });
        }
    })
    .catch((error) => {
        message.error("获取系统配置失败");
        console.error(error); // 打印错误信息以便调试
    });
};

// 初始化配置并挂载应用
initConfig().then(() => {
    app.use(router);
    app.use(Antd);
    app.component("VChart", VChart);
    app.mount("#app");
});
