import { defineConfig, type UserConfig, type ConfigEnv, loadEnv } from "vite";
import uni from "@dcloudio/vite-plugin-uni";
import AutoImport from "unplugin-auto-import/vite";
import UniLayouts from "@uni-helper/vite-plugin-uni-layouts";
import UniPages from "@uni-helper/vite-plugin-uni-pages";
import Components from "@uni-helper/vite-plugin-uni-components";
import { WotResolver } from "@uni-helper/vite-plugin-uni-components/resolvers";

export default defineConfig(async ({ mode }: ConfigEnv): Promise<UserConfig> => {
  const UnoCss = await import("unocss/vite").then((i) => i.default);
  const env = loadEnv(mode, process.cwd());

  return {
    base: "/app",
    server: {
      host: true,
      port: Number(env.VITE_APP_PORT),
      open: true,
      proxy: {
        [env.VITE_APP_BASE_API]: {
          changeOrigin: true,
          target: env.VITE_API_BASE_URL,
          // rewrite: (path) => path.replace(new RegExp("^" + env.VITE_APP_BASE_API), ""),
        },
      },
    },
    build: {
      target: "es6",
      cssTarget: "chrome61",
    },
    optimizeDeps: {
      include: ["wot-design-uni"],
      exclude: ["vue-demi"],
    },
    plugins: [
      // make sure put it before `Uni()`
      UnoCss(),
      UniLayouts(),
      UniPages(),

      Components({
        resolvers: [WotResolver()],
      }),

      AutoImport({
        imports: [
          "vue",
          "uni-app",
          "pinia",
          {
            from: "uni-mini-router",
            imports: ["createRouter", "useRouter", "useRoute"],
          },
          {
            from: "wot-design-uni",
            imports: ["useToast", "useMessage", "useNotify", "CommonUtil"],
          },
        ],
        dts: "src/types/auto-imports.d.ts", // 自动生成的类型声明文件
        dirs: ["src/composables", "src/store", "src/utils", "src/api"],
        vueTemplate: true,
      }),

      uni(),
    ],
  };
});
