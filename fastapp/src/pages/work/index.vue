<template>
  <view class="app-container">
    <wd-status-tip type="search" tip="建设中..." />
  </view>
</template>

<script setup lang="ts"></script>

<route lang="json">
{
  "name": "work",
  "style": {
    "navigationBarTitleText": "工作台"
  },
  "meta": {
    "requireAuth": true
  }
}
</route>

<style lang="scss"></style>
