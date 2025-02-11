import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd());
  return {
    // 设置scss的api类型为modern-compiler
    css: {
      preprocessorOptions: {
        scss: {
          api: 'modern-compiler'
        }
      }
    },
    
    plugins: [vue()],
    server: {
      host: "0.0.0.0",
      port: 5180,
      proxy: {
        [env.VITE_APP_BASE_API]: {
          target: env.VITE_API_BASE_URL,
          secure: false, // 请求是否为https
          changeOrigin: true, // 是否跨域
          // rewrite: (path) => path.replace(/^\/api/, '')
        },
      },
    },
    resolve: {
      alias: {
        "@": resolve(__dirname, "./src"),
      },
    },
  };
});
