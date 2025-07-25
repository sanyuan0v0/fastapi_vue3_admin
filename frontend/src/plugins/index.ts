import type { App } from "vue";

import { setupI18n } from "@/lang";
import { setupRouter } from "@/router";
import { setupStore } from "@/store";
import { setupElIcons } from "./icons";
import { setupPermission } from "./permission";
import { InstallCodeMirror } from "codemirror-editor-vue3";
import ElementPlus from 'element-plus'

export default {
  install(app: App<Element>) {
    // 路由(router)
    setupRouter(app);
    // 状态管理(store)
    setupStore(app);
    // 国际化
    setupI18n(app);
    // Element-plus图标
    setupElIcons(app);
    // 路由守卫
    setupPermission();
    // 注册 CodeMirror
    app.use(InstallCodeMirror);
    // 注册 ElementPlus
    app.use(ElementPlus);
  },
};
