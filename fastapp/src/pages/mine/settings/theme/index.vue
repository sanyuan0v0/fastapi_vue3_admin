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
        <view>
          <text class="font-medium">暗黑模式</text>
        </view>
        <wd-switch v-model:model-value="isDark" active-color="var(--wot-color-theme)" @change="toggleTheme" />
      </view>
    </wd-card>

    <!-- 跟随系统主题 -->
    <wd-card class="mb-3">
      <view class="flex-between py-2">
        <view>
          <text class="font-medium">跟随系统</text>
        </view>
        <wd-switch :model-value="followSystem" active-color="var(--wot-color-theme)" @change="setFollowSystem" />
      </view>
    </wd-card>

    <!-- 主题色选择 -->
    <wd-card title="主题色" class="mb-3">
      <view class="color-grid">
        <view v-for="item in themeColorOptions" :key="item.value" class="color-item"
          :class="{ active: currentThemeColor.value === item.value }" @click="handleSelectColor(item)">
          <view class="color-box" :style="{ backgroundColor: item.primary }">
            <wd-icon v-if="currentThemeColor.value === item.value" name="check" size="16" color="#fff" />
          </view>
          <text class="color-label">{{ item.name }}</text>
        </view>
      </view>
    </wd-card>

    <!-- 自定义颜色 -->
    <wd-card class="mb-3">
      <view class="flex-between items-center py-2" @click="showCustomColorPopup = true">
        <view class="flex-start gap-2 items-center">
          <wd-icon name="edit" size="20" :color="currentThemeColor.primary" />
          <view>
            <text class="font-medium">自定义颜色</text>
          </view>
        </view>
        <view class="flex-start gap-2 items-center">
          <view class="color-box small" :style="{ backgroundColor: currentThemeColor.primary }"></view>
          <text class="text-sm text-gray-500 font-mono">{{ currentThemeColor.primary }}</text>
          <wd-icon name="arrow-right" size="14" color="#999" />
        </view>
      </view>
    </wd-card>

    <!-- 预览效果 -->
    <wd-card title="预览效果" class="mb-3">
      <view class="py-4">
        <view class="flex-start gap-3 mb-4">
          <wd-button type="primary" size="small">主要按钮</wd-button>
          <wd-button type="primary" plain size="small">次要按钮</wd-button>
          <wd-tag type="primary">标签</wd-tag>
        </view>
        <view class="preview-card" :style="{ backgroundColor: currentThemeColor.primary + '20' }">
          <text class="text-sm text-gray-600">当前主题色预览</text>
          <view class="mt-2 h-8 rounded" :style="{ backgroundColor: currentThemeColor.primary }"></view>
        </view>
      </view>
    </wd-card>

    <!-- 重置按钮 -->
    <view class="mt-5 mx-3">
      <wd-button plain block :disabled="currentThemeColor.value === themeColorOptions[0].value &&
        theme === 'light' &&
        followSystem
        " @click="handleReset">
        恢复默认
      </wd-button>
    </view>

    <!-- 自定义颜色弹窗 -->
    <wd-popup v-model="showCustomColorPopup" position="bottom" closeable>
      <view class="custom-color-popup">
        <view class="text-center mb-5">
          <text class="text-lg font-bold">自定义主题色</text>
          <text class="block text-sm text-gray-500 mt-1">输入任意 HEX 颜色值</text>
        </view>

        <view class="mb-5">
          <view class="color-preview-large mb-4" :style="{ backgroundColor: customColor }"></view>

          <view class="mb-3">
            <text class="text-sm font-medium mb-2 block">颜色值</text>
            <wd-input v-model="customColor" placeholder="例如: #FF6B6B 或 #F00" clearable :maxlength="7" />
          </view>

          <view class="grid grid-cols-6 gap-2 mb-3">
            <view v-for="color in quickColors" :key="color" class="w-10 h-10 rounded cursor-pointer"
              :style="{ backgroundColor: color }" @click="customColor = color"></view>
          </view>

          <text class="input-tip">支持 #RRGGBB 或 #RGB 格式</text>
        </view>

        <view class="flex gap-2">
          <wd-button type="info" block @click="showCustomColorPopup = false">取消</wd-button>
          <wd-button type="primary" block :disabled="!isValidColor(customColor)" @click="applyCustomColor">
            应用
          </wd-button>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from "vue";
import { onShow, onLoad } from "@dcloudio/uni-app";
import { useTheme } from "@/composables/useTheme";
import type { ThemeColorOption } from "@/composables/useTheme";

const {
  theme,
  currentThemeColor,
  themeColorOptions,
  toggleTheme,
  selectThemeColor,
  resetTheme,
  setCustomThemeColor,
  followSystem,
  setFollowSystem,
  isDark,
} = useTheme();

// 自定义颜色相关
const showCustomColorPopup = ref(false);
const customColor = ref(currentThemeColor.value.primary);

// 快速颜色选择
const quickColors = [
  "#FF6B6B",
  "#4ECDC4",
  "#45B7D1",
  "#96CEB4",
  "#FECA57",
  "#FF9FF3",
  "#54A0FF",
  "#5F27CD",
  "#00D2D3",
  "#FF9F43",
  "#10AC84",
  "#EE5A24",
  "#009432",
  "#0652DD",
  "#9980FA",
];

// 动态设置页面标题
onLoad(() => {
  uni.setNavigationBarTitle({
    title: "主题设置",
  });
});

// 监听主题变化，确保实时生效
onShow(() => {
  // 强制应用当前主题色
  setTimeout(() => {
    customColor.value = currentThemeColor.value.primary;
  }, 50);
});

// 监听主题更新事件
onMounted(() => {
  uni.$on('theme-color-changed', (color: string) => {
    customColor.value = color;
  });
});

onUnmounted(() => {
  uni.$off('theme-color-changed');
});

// 验证颜色格式
const isValidColor = (color: string): boolean => {
  return /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(color);
};

// 应用自定义颜色
const applyCustomColor = () => {
  if (!isValidColor(customColor.value)) {
    uni.showToast({
      title: "请输入正确的颜色格式",
      icon: "none",
    });
    return;
  }

  setCustomThemeColor(customColor.value);
  showCustomColorPopup.value = false;
  uni.showToast({
    title: "主题颜色已更新",
    icon: "success",
  });

  // 强制刷新当前页面样式
  setTimeout(() => {
    uni.$emit('theme-updated');
  }, 50);
};

// 选择主题色
const handleSelectColor = (colorOption: ThemeColorOption) => {
  selectThemeColor(colorOption);
  uni.showToast({
    title: "主题色已更新",
    icon: "success",
  });

  // 强制刷新当前页面样式
  setTimeout(() => {
    customColor.value = currentThemeColor.value.primary;
    uni.$emit('theme-updated');
  }, 50);
};

// 重置主题
const handleReset = () => {
  uni.showModal({
    title: "提示",
    content: "确定要恢复默认主题吗？",
    success: (res) => {
      if (res.confirm) {
        resetTheme();
        customColor.value = currentThemeColor.value.primary;
        uni.showToast({
          title: "已恢复默认",
          icon: "success",
        });

        // 强制刷新当前页面样式
        setTimeout(() => {
          uni.$emit('theme-updated');
        }, 50);
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
  customColor.value = currentThemeColor.value.primary;
});
</script>

<style lang="scss" scoped>
.page-header {
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
  gap: 24rpx;
  padding: 32rpx 0;
}

.color-item {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  align-items: center;
  cursor: pointer;
  border-radius: 16rpx;
  transition: all 0.2s ease;

  &.active {
    color: white;

    .color-label {
      color: white;
    }
  }

  &:active {
    transform: scale(0.95);
  }

  .color-box {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64rpx;
    height: 64rpx;
    border-radius: 50%;

    &.small {
      box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.1);
    }

    &.ring-2 {
      box-shadow:
        0 0 0 2rpx var(--wot-color-theme),
        0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    }
  }

  .color-label {
    font-size: 24rpx;
    color: var(--wot-color-text-secondary);
    transition: color 0.2s ease;
  }
}

.custom-color-popup {
  padding: 48rpx 40rpx;
  background-color: var(--wot-color-bg);
  border-radius: 32rpx 32rpx 0 0;

  .color-preview-large {
    width: 100%;
    height: 120rpx;
    border: 2rpx solid var(--wot-color-border);
    border-radius: 16rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  }

  .preview-card {
    padding: 24rpx;
    border: 2rpx solid var(--wot-color-border);
    border-radius: 16rpx;
  }

  .input-tip {
    display: block;
    margin-top: 12rpx;
    font-size: 24rpx;
    color: var(--wot-color-secondary);
  }
}

.grid {
  display: grid;
}

.grid-cols-6 {
  grid-template-columns: repeat(6, 1fr);
}

.gap-2 {
  gap: 16rpx;
}

.gap-3 {
  gap: 24rpx;
}

.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.flex-start {
  display: flex;
  align-items: center;
}

.items-center {
  align-items: center;
}

.py-4 {
  padding-top: 32rpx;
  padding-bottom: 32rpx;
}

.text-sm {
  font-size: 24rpx;
}

.text-lg {
  font-size: 32rpx;
}

.text-gray-500 {
  color: var(--wot-color-secondary);
}

.text-gray-600 {
  color: var(--wot-color-secondary);
}

.font-medium {
  font-weight: 500;
}

.font-bold {
  font-weight: 600;
}

.font-mono {
  font-family:
    "ui-monospace", SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
}

.cursor-pointer {
  cursor: pointer;
}

.w-8 {
  width: 64rpx;
}

.w-10 {
  width: 80rpx;
}

.h-8 {
  height: 64rpx;
}

.h-10 {
  height: 80rpx;
}

.rounded {
  border-radius: 8rpx;
}

.rounded-full {
  border-radius: 50%;
}

.ring-2 {
  --tw-ring-offset-width: 2px;
}

.ring-offset-2 {
  --tw-ring-offset-width: 2px;
}

.ring-current {
  --tw-ring-color: currentColor;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.transition-all {
  transition: all 0.2s ease;
}

.duration-200 {
  transition-duration: 200ms;
}

.ease-in-out {
  transition-timing-function: ease-in-out;
}

.block {
  display: block;
}
</style>
