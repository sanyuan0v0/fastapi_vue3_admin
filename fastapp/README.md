## 项目介绍

基于 uni-app + Vue 3 + TypeScript 移动端跨平台开发模板，集成了 ESLint、Prettier、Stylelint、Husky 和 Commitlint 等工具，确保代码规范与质量。

## 项目截图

![](https://www.youlai.tech/storage/blog/2025/04/30/app.jpg)

## 项目文档

[从0到1构建 UniApp + Vue3 + TypeScript 移动端跨平台开源脚手架](https://juejin.cn/post/7448963032993038376)

## 项目启动

安装依赖

```
pnpm install
```

h5启动

```
pnpm run dev:h5
```

访问 [http://localhost:4096](http://localhost:4096)

## 组件结构

项目组件分为以下几类：

- **基础组件**：`src/components` 下的通用组件
- **业务组件**：`src/components/business` 下的业务相关组件
  - `WechatProfile.vue`: 微信小程序环境下的头像、昵称和性别选择组件

使用业务组件：

```vue
<template>
  <WechatProfile v-model="profileData" @change="onProfileChange" />
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { WechatProfile } from "@/components/business";

const profileData = ref({
  avatar: "",
  nickname: "",
  gender: 1,
});

const onProfileChange = (data) => {
  console.log("个人资料变更:", data);
};
</script>
```
