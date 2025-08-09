<template>
  <!-- 内容区域 -->
  <view class="app-container">
    <wd-navbar title="主题设置" left-arrow @click-left="handleBack" />

    <!-- 页面标题 -->
    <wd-card custom-class="page-header">
      <text class="page-title">主题设置</text>
      <view class="page-subtitle">个性化您的应用外观</view>
    </wd-card>

    <!-- 暗黑模式设置 -->
    <wd-card class="mb-3">
      <view class="flex-between py-2">
        <text>暗黑模式</text>
        <wd-switch :model-value="theme === 'dark'" @change="toggleTheme" />
      </view>
    </wd-card>
    <!-- 主题色选择 -->
    <wd-card title="主题色" class="mb-3">
      <view class="color-grid">
        <view
          v-for="item in colorColumns"
          :key="item.value"
          class="color-item"
          :class="{ active: currentThemeColor === item.value }"
          @click="setThemeColor(item.value)"
        >
          <view class="color-box" :style="{ backgroundColor: item.value }">
            <wd-icon v-if="currentThemeColor === item.value" name="check" size="16" color="#fff" />
          </view>
          <text class="color-label">{{ item.label }}</text>
        </view>
      </view>
    </wd-card>
    <!-- 自定义颜色 -->
    <wd-card class="mb-3">
      <view class="flex-between items-center py-2" @click="showCustomColorPopup = true">
        <view class="flex-start gap-2 items-center">
          <wd-icon name="edit" size="20" :color="currentThemeColor" />
          <text>自定义颜色</text>
        </view>
        <view class="flex-start gap-2 items-center">
          <view class="color-box small" :style="{ backgroundColor: currentThemeColor }"></view>
          <text class="text-sm text-gray-500">{{ currentThemeColor }}</text>
          <wd-icon name="arrow-right" size="14" color="#999" />
        </view>
      </view>
    </wd-card>
    <!-- 预览效果 -->
    <wd-card title="预览效果" class="mb-3">
      <view class="py-2">
        <view class="flex-start gap-2">
          <wd-button type="primary" size="small">主要按钮</wd-button>
          <wd-button type="primary" plain size="small">次要按钮</wd-button>
          <wd-tag type="primary">标签</wd-tag>
        </view>
      </view>
    </wd-card>
    <!-- 重置按钮 -->
    <view class="mt-5 mx-3">
      <wd-button plain block @click="handleReset">恢复默认</wd-button>
    </view>

    <!-- 自定义颜色弹窗 -->
    <wd-popup v-model="showCustomColorPopup" position="bottom" closeable>
      <view class="custom-color-popup">
        <view class="text-center mb-5"><text class="text-lg font-bold">自定义主题色</text></view>
        <view class="mb-5">
          <view class="color-preview-large" :style="{ backgroundColor: customColor }"></view>
          <wd-input v-model="customColor" placeholder="请输入颜色值，如 #FF6B6B" clearable />
          <text class="input-tip">支持 HEX 格式颜色值</text>
        </view>
        <view class="flex gap-2">
          <wd-button type="info" block @click="showCustomColorPopup = false">取消</wd-button>
          <wd-button type="primary" block @click="applyCustomColor">应用</wd-button>
        </view>
      </view>
    </wd-popup>
  </view>
</template>
<script lang="ts" setup>
import { onShow, onLoad } from "@dcloudio/uni-app";
import { useTheme } from "@/composables/useTheme";

const { theme, currentThemeColor, colorColumns, toggleTheme, setThemeColor, resetTheme } =
  useTheme();

// 自定义颜色相关
const showCustomColorPopup = ref(false);
const customColor = ref(currentThemeColor.value);

// 动态设置页面标题
onLoad(() => {
  uni.setNavigationBarTitle({
    title: "主题设置",
  });
});

// 应用自定义颜色
const applyCustomColor = () => {
  const colorRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;

  if (!colorRegex.test(customColor.value)) {
    uni.showToast({
      title: "请输入正确的颜色格式",
      icon: "none",
    });
    return;
  }

  setThemeColor(customColor.value);
  showCustomColorPopup.value = false;
  uni.showToast({
    title: "主题色已更新",
    icon: "success",
  });
};

// 重置主题
const handleReset = () => {
  uni.showModal({
    title: "提示",
    content: "确定要恢复默认主题吗？",
    success: (res) => {
      if (res.confirm) {
        resetTheme();
        customColor.value = currentThemeColor.value;
        uni.showToast({
          title: "已恢复默认",
          icon: "success",
        });
      }
    },
  });
};

// 处理返回按钮点击
const handleBack = () => {
  uni.navigateBack();
};

// 页面显示时更新自定义颜色值
onShow(() => {
  customColor.value = currentThemeColor.value;
});
</script>
<style lang="scss" scoped>
.page-header {
  padding: 40rpx 20rpx;
  margin-top: 20rpx;
  text-align: center;
  background: linear-gradient(135deg, var(--wot-color-theme) 0%, var(--primary-color-light) 100%);

  .page-title {
    display: block;
    margin-bottom: 10rpx;
    font-size: 36rpx;
    font-weight: bold;
    color: #fff;
  }

  .page-subtitle {
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.8);
  }
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24rpx 20rpx;
}

.color-item {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  align-items: center;
  padding: 8rpx;
  cursor: pointer;

  &.active .color-box {
    box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.15);
    transform: scale(1.1);
  }

  .color-box {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60rpx;
    height: 60rpx;
    border-radius: 12rpx;
    transition: all 0.3s ease;

    &.small {
      width: 40rpx;
      height: 40rpx;
    }
  }

  .color-label {
    font-size: 22rpx;
    color: var(--wot-color-text-secondary);
    text-align: center;
    white-space: nowrap;
  }
}

.custom-color-popup {
  padding: 40rpx 30rpx;
  background-color: var(--wot-color-bg-container);

  .color-preview-large {
    width: 100%;
    height: 120rpx;
    margin-bottom: 30rpx;
    border: 2rpx solid var(--wot-color-border);
    border-radius: 16rpx;
  }

  .input-tip {
    display: block;
    margin-top: 15rpx;
    font-size: 24rpx;
    color: var(--wot-color-text-placeholder);
    text-align: center;
  }
}
</style>
