import type { App } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const store = createPinia();

store.use(piniaPluginPersistedstate)

// 全局注册 store
export function setupStore(app: App<Element>) {
  app.use(store);
}

export * from "./modules/app.store";
export * from "./modules/settings.store";
export * from "./modules/tags-view.store";
export * from "./modules/lock.store";
export * from "./modules/permission.store";
export * from "./modules/user.store";
export * from "./modules/dict.store";
export * from "./modules/config.store";
export * from "./modules/notice.store";
export { store };
