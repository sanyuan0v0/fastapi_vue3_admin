# 主题系统使用指南

## 概述

本项目基于 Wot Design Uni 的 ConfigProvider 组件实现了完整的主题系统，支持：

- 🌙 暗黑/浅色模式切换
- 🎨 12种预设主题色
- 🎯 自定义主题色
- 💾 主题设置持久化存储
- 📱 多平台兼容（H5、小程序）

## 核心文件

### 1. useTheme Composable (`src/composables/useTheme.ts`)

主题管理的核心逻辑，提供：

```typescript
const {
  theme, // 当前主题模式 'light' | 'dark'
  themeVars, // ConfigProviderThemeVars 主题变量
  toggleTheme, // 切换主题模式
  setThemeColor, // 设置主题色
  resetTheme, // 重置主题
  initTheme, // 初始化主题
  colorColumns, // 预设主题色列表
} = useTheme();
```

### 2. 布局文件

#### Tabbar 布局 (`src/layouts/tabbar.vue`)

```vue
<template>
  <wd-config-provider
    :theme="theme"
    :theme-vars="themeVars"
    custom-style="min-height: 100vh"
    :class="{ 'wot-theme-dark': theme === 'dark' }"
  >
    <!-- 页面内容 -->
  </wd-config-provider>
</template>
```

#### Default 布局 (`src/layouts/default.vue`)

```vue
<template>
  <wd-config-provider
    :theme="theme"
    :theme-vars="themeVars"
    custom-style="background-color: #f5f5f5;min-height: 100vh"
    :class="{ 'wot-theme-dark': theme === 'dark' }"
  >
    <!-- 页面内容 -->
  </wd-config-provider>
</template>
```

### 3. 主题设置页面 (`src/pages/mine/settings/theme/index.vue`)

提供用户界面来：

- 切换暗黑/浅色模式
- 选择预设主题色
- 输入自定义主题色
- 预览主题效果
- 重置主题设置

## 主题变量

### 支持的 ConfigProviderThemeVars

根据 Wot Design Uni 文档，主要使用：

```typescript
interface ConfigProviderThemeVars {
  colorTheme?: string; // 主题色
  buttonPrimaryBgColor?: string; // 主按钮背景色
  buttonPrimaryColor?: string; // 主按钮文字色
  // ... 更多变量
}
```

### 预设主题色

```typescript
const colorColumns = [
  { value: "#165DFF", label: "蓝色" },
  { value: "#0FC6C2", label: "青绿色" },
  { value: "#722ED1", label: "紫色" },
  { value: "#F5222D", label: "红色" },
  { value: "#FA8C16", label: "橙色" },
  { value: "#FADB14", label: "黄色" },
  { value: "#52C41A", label: "绿色" },
  { value: "#EB2F96", label: "粉色" },
  { value: "#13C2C2", label: "青色" },
  { value: "#1890FF", label: "天蓝色" },
  { value: "#CD5C5C", label: "经典红" },
  { value: "#228B22", label: "自然绿" },
];
```

## 暗黑模式实现

### 1. ConfigProvider 主题切换

```vue
<wd-config-provider :theme="theme">
  <!-- theme 为 'dark' 时自动应用暗黑模式 -->
</wd-config-provider>
```

### 2. 全局样式适配

在 `src/uni.scss` 中定义：

```scss
.wot-theme-dark {
  background-color: #1a1a1a !important;
  color: #f5f5f5 !important;

  /* H5 环境 body 样式 */
  body {
    background-color: #1a1a1a !important;
    color: #f5f5f5 !important;
  }

  /* 其他组件暗黑模式适配 */
}
```

### 3. 动态 Body 样式

在 `useTheme` 中自动处理：

```typescript
const applyDarkModeBodyStyle = (isDark: boolean) => {
  // #ifdef H5
  if (typeof document !== "undefined") {
    const body = document.body;
    if (isDark) {
      body.style.backgroundColor = "#1a1a1a";
      body.style.color = "#f5f5f5";
      body.classList.add("wot-theme-dark");
    } else {
      body.style.backgroundColor = "#f8f8f8";
      body.style.color = "#333";
      body.classList.remove("wot-theme-dark");
    }
  }
  // #endif
};
```

## 持久化存储

主题设置自动保存到本地存储：

```typescript
// 存储键名
const THEME_STORAGE_KEY = "app_theme_mode";
const THEME_COLOR_STORAGE_KEY = "app_theme_color";

// 自动监听变化并保存
watch(
  theme,
  (newTheme) => {
    saveThemeToStorage(newTheme);
    applyDarkModeBodyStyle(newTheme === "dark");
  },
  { immediate: true }
);
```

## 使用示例

### 在页面中使用主题

```vue
<template>
  <view>
    <wd-button type="primary">主题色按钮</wd-button>
    <text :style="{ color: themeVars.colorTheme }">主题色文本</text>
  </view>
</template>

<script setup>
import { useTheme } from "@/composables/useTheme";

const { theme, themeVars, toggleTheme, setThemeColor } = useTheme();

// 切换主题模式
const handleToggleTheme = () => {
  toggleTheme();
};

// 设置主题色
const handleSetColor = (color: string) => {
  setThemeColor(color);
};
</script>
```

### 在组件中响应主题变化

```vue
<template>
  <view :class="{ 'dark-mode': isDark }">
    <!-- 组件内容 -->
  </view>
</template>

<script setup>
import { computed } from "vue";
import { useTheme } from "@/composables/useTheme";

const { theme } = useTheme();

const isDark = computed(() => theme.value === "dark");
</script>

<style>
.dark-mode {
  background-color: #2a2a2a;
  color: #f5f5f5;
}
</style>
```

## 最佳实践

### 1. 组件开发

- 使用 Wot Design Uni 组件时，主题色会自动应用
- 自定义组件需要手动适配暗黑模式
- 使用 `:class="{ 'wot-theme-dark': theme === 'dark' }"` 来应用暗黑模式样式

### 2. 样式编写

```scss
.my-component {
  background-color: #fff;
  color: #333;

  // 暗黑模式适配
  .wot-theme-dark & {
    background-color: #2a2a2a;
    color: #f5f5f5;
  }
}
```

### 3. 主题色使用

```vue
<template>
  <!-- 直接使用主题色 -->
  <view :style="{ borderColor: themeVars.colorTheme }">
    <!-- 内容 -->
  </view>
</template>
```

## 注意事项

1. **ConfigProvider 包裹**：确保页面被 ConfigProvider 包裹才能应用主题
2. **样式优先级**：暗黑模式样式需要足够的优先级，必要时使用 `!important`
3. **平台兼容**：小程序和 H5 的样式处理略有不同，使用条件编译处理
4. **性能考虑**：主题切换时避免频繁的 DOM 操作

## 扩展功能

### 添加新的主题色

在 `colorColumns` 中添加新的颜色：

```typescript
export const colorColumns = [
  // ... 现有颜色
  { value: "#FF6B6B", label: "珊瑚红" },
  { value: "#4ECDC4", label: "薄荷绿" },
];
```

### 添加更多主题变量

```typescript
const themeVars = ref<ConfigProviderThemeVars>({
  colorTheme: getStoredThemeColor(),
  buttonPrimaryBgColor: getStoredThemeColor(),
  // 添加更多变量
});
```

### 自定义暗黑模式样式

在 `uni.scss` 中添加更多组件的暗黑模式适配：

```scss
.wot-theme-dark {
  // 新组件的暗黑模式样式
  .my-custom-component {
    background-color: #2a2a2a;
    color: #f5f5f5;
  }
}
```
