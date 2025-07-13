<template>
  <el-config-provider :locale="locale" :size="size">
    <!-- 开启水印 -->
    <el-watermark
      :font="{ color: fontColor }"
      :content="showWatermark ? defaultSettings.watermarkContent : ''"
      :z-index="9999"
      class="wh-full"
    >
      <router-view />
    </el-watermark>
  </el-config-provider>
</template>

<script setup lang="ts">
import { useAppStore, useSettingsStore } from "@/store";
import { defaultSettings } from "@/settings";
import { ThemeMode } from "@/enums/settings/theme.enum";
import { ComponentSize } from "@/enums/settings/layout.enum";
import { ElNotification } from 'element-plus'

const appStore = useAppStore();
const settingsStore = useSettingsStore();

const locale = computed(() => appStore.locale);
const size = computed(() => appStore.size as ComponentSize);
const showWatermark = computed(() => settingsStore.showWatermark);

// 明亮/暗黑主题水印字体颜色适配
const fontColor = computed(() => {
  return settingsStore.theme === ThemeMode.DARK ? "rgba(255, 255, 255, .15)" : "rgba(0, 0, 0, .15)";
});

ElNotification({
  title: '提示',
  type: 'warning',
  duration: 0,
  dangerouslyUseHTMLString: true,
  message:
    '<div><p><strong>遇事不决，请先查阅常见问题，说不定你能找到相关解答</strong></p><p><a href="https://gitee.com/tao__tao/fastapi_vue3_admin" target="_blank">链接地址</a></p></div>'
})
</script>
