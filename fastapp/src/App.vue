<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import { useTheme } from "@/composables/useTheme";

const { initTheme } = useTheme();

onLaunch(() => {
  // 初始化主题
  initTheme();
});

onShow(() => {
  console.log("App Show");
});

onHide(() => {
  console.log("App Hide");
});
</script>

<style lang="scss"></style>
