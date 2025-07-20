<!-- 接口文档 -->
<template>
  <div class="app-container">
    <Frame :src="url" />
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Redoc",
  inheritAttrs: false,
});

const url = ref(import.meta.env.VITE_APP_BASE_API + "/redoc")

onBeforeUnmount(() => {
    window.onresize = null;
})
</script>

<style lang="scss" scoped>
/** 关闭tag标签  */
.app-container {
  /* 50px = navbar = 50px */
  height: calc(100vh - 50px);
}

/** 开启tag标签  */
.hasTagsView {
  .app-container {
    /* 84px = navbar + tags-view = 50px + 34px */
    height: calc(100vh - 84px);
  }
}
</style>
