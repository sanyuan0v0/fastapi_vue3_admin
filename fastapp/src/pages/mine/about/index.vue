<template>
  <view class="app-container">
    <wd-navbar title="关于我们" left-arrow @click-left="handleBack" />

    <!-- 顶部信息区域 -->
    <wd-card custom-style="margin-top: 20rpx">
      <view class="flex items-center p-2">
        <wd-img width="60px" height="60px" src="/static/logo.png" mode="aspectFit" class="mr-4" />
        <view class="flex-1">
          <text class="text-lg font-bold block mb-1">vue-uniapp-template</text>
          <text class="text-xs text-gray-500">版本 {{ version }}</text>
        </view>
      </view>
    </wd-card>

    <!-- 公司信息区域 -->
    <wd-card custom-style="margin-top: 20rpx">
      <view class="p-4">
        <view class="flex items-center mb-3">
          <wd-icon name="company" size="18" class="mr-2" />
          <text class="text-base font-medium">有来开源组织</text>
        </view>
        <text class="text-sm text-gray-500 block pl-6">专注于快速构建和高效开发的应用解决方案</text>
      </view>
    </wd-card>

    <!-- 项目列表 -->
    <wd-card title="优质项目" custom-style="margin-top: 20rpx">
      <wd-cell-group border>
        <wd-cell title="vue3-element-admin" icon="desktop">
          <view slot="label" class="text-xs text-gray-500 mt-1">
            基于 Vue3 + Vite5 + TypeScript5 + Element-Plus + Pinia 构建的中后台管理模板
          </view>
        </wd-cell>

        <wd-cell title="vue-uniapp-template" icon="mobile">
          <view slot="label" class="text-xs text-gray-500 mt-1">
            基于 uni-app + Vue 3 + TypeScript，集成多种工具的移动端应用模板
          </view>
        </wd-cell>

        <wd-cell title="youlai-boot" icon="server">
          <view slot="label" class="text-xs text-gray-500 mt-1">
            基于 Spring Boot 3 + Vue 3 构建的前后端分离单体权限管理系统
          </view>
        </wd-cell>
      </wd-cell-group>
    </wd-card>

    <!-- 联系方式 -->
    <wd-card title="联系我们" custom-style="margin-top: 20rpx">
      <wd-cell-group border>
        <wd-cell title="官方网站" value="www.youlai.tech" icon="link" />
        <wd-cell title="GitHub" value="github.com/youlaitech" icon="github" />
        <wd-cell title="联系邮箱" value="youlaitech@163.com" icon="mail" />
      </wd-cell-group>
    </wd-card>

    <!-- 底部版权信息 -->
    <view class="text-center py-4">
      <text class="block text-xs text-gray-400">Copyright © {{ getYear() }} 有来开源组织</text>
      <text class="block text-xs text-gray-400 mt-1">All Rights Reserved</text>
    </view>
  </view>
</template>

<script lang="ts" setup>
const version = ref("1.0.0");

const handleBack = () => {
  uni.navigateBack();
};

const getYear = () => {
  return new Date().getFullYear();
};

onMounted(() => {
  // #ifdef MP-WEIXIN
  version.value = uni.getSystemInfoSync().appVersion;
  // #endif
});
</script>

<style lang="scss" scoped>
:deep(.wd-card__header) {
  font-size: 30rpx;
  font-weight: 500;
  color: var(--wot-color-text, #333);
}

:deep(.wd-cell__icon) {
  font-size: 36rpx;
  color: var(--wot-color-theme, #409eff);
}
</style>
