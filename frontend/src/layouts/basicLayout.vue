<template>
  <a-layout class="basic-layout">
    <!-- 左侧导航 -->
    <a-layout-sider class="layout-sider" :collapsed="menuState.collapsed" theme="light" :trigger="null" collapsible
      :width="240" :collapsedWidth="80">
      <!-- Logo 区域 -->
      <div class="logo-container">
        <a-image :src="initConfigState.web_favicon" :preview="false" :width="28" :height="28" />
        <h1 class="logo-title" v-show="!menuState.collapsed">{{ initConfigState.web_title }}</h1>
      </div>

      <a-menu class="side-menu" mode="inline" v-model:openKeys="menuState.openKeys"
        v-model:selectedKeys="menuState.selectedKeys" :items="menuState.menus" @click="handleMenuClick" />
    </a-layout-sider>

    <!-- 右侧布局 -->
    <a-layout class="layout-main" :class="{ collapsed: menuState.collapsed }">
      <!-- 顶部导航栏 -->
      <a-layout-header class="layout-header">

        <div class="header-left">
          <!-- 左侧折叠按钮 -->
          <a-button type="link" class="collapse-btn" @click="toggleCollapsed">
            <MenuFoldOutlined v-if="menuState.collapsed" />
            <MenuUnfoldOutlined v-else />
          </a-button>
          <topCrumb></topCrumb>
        </div>

        <!-- 右侧工具栏 -->
        <div class="header-right">
          <!-- 主题切换按钮 -->
          <a-tooltip :title="isDarkMode ? '切换亮色主题' : '切换暗色主题'" placement="bottom">
            <a-button type="link" @click="handleThemeChange" class="tool-btn">
              <component :is="isDarkMode ? BulbFilled : BulbOutlined" />
            </a-button>
          </a-tooltip>

          <!-- 文档按钮 -->
          <a-tooltip title="说明文档" placement="bottom">
            <a-button type="link" @click="openDocumentation" class="tool-btn">
              <QuestionCircleOutlined />
            </a-button>
          </a-tooltip>

          <!-- 通知按钮 -->
          <a-popover placement="bottom" trigger="hover" :autoAdjustOverflow="true">
            <template #content>
              <div class="notice-popover">
                <a-list :data-source="noticeState.notices" size="small">
                  <template #renderItem="{ item }">
                    <a-list-item>
                      <a-list-item-meta>
                        <template #title>
                          <span>
                            <a-tag :color="item.notice_type === 1 ? 'blue' : 'orange'">
                              {{ item.notice_type === 1 ? '通知' : '公告' }}
                            </a-tag>
                            {{ item.notice_title }}
                          </span>
                        </template>
                        <template #description>
                          <div class="notice-content">{{ item.notice_content }}</div>
                        </template>
                      </a-list-item-meta>
                    </a-list-item>
                  </template>
                  <template #header>
                    <div class="notice-header">
                      <icons.WarningOutlined style="color: #faad14" /> 公告通知
                    </div>
                  </template>
                </a-list>
              </div>
            </template>
            <a-badge :count="noticeState.total" :dot="noticeState.total > 99">
              <a-button type="link" class="tool-btn">
                <BellOutlined />
              </a-button>
            </a-badge>
          </a-popover>

          <!-- 用户信息下拉菜单 -->
          <a-dropdown>
            <div class="user-dropdown">
              <a-avatar v-if="userInfo.avatar" :src="userInfo.avatar" :size="32" />
              <a-avatar v-else :size="32">
                <template #icon>
                  <UserOutlined />
                </template>
              </a-avatar>
              <span class="username">{{ userInfo.username }}</span>
              <DownOutlined />
            </div>
            <template #overlay>
              <a-menu @click="handleUserMenuClick">
                <a-menu-item key="profile">
                  <template #icon>
                    <UserOutlined />
                  </template>
                  个人中心
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="logout">
                  <template #icon>
                    <LogoutOutlined />
                  </template>
                  退出登录
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </a-layout-header>
      <!-- 主内容区 -->
      <a-layout-content class="layout-content">
        <div class="header-tag">
          <topTags></topTags>
        </div>
        <div class="header-centent">
          <router-view v-slot="{ Component, route }">
            <transition name="fade" mode="out-in">
              <div :key="route.path">
                <keep-alive v-if="route.meta.keepAlive">
                  <component :is="Component" />
                </keep-alive>
                <component :is="Component" v-else />
              </div>
            </transition>
          </router-view>
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script lang="ts" setup>
import { reactive, computed, watch, onMounted, inject, type Ref } from "vue";
import type { MenuProps, ItemType } from "ant-design-vue";
import { useRouter, useRoute } from "vue-router";
import storage from 'store';
import * as icons from '@ant-design/icons-vue';
import { h } from 'vue';
import { listToTree } from '@/utils/util';

import topTags from '@/components/TopTags/index.vue';
import topCrumb from '@/components/TopCrumb/index.vue';
import {
  QuestionCircleOutlined,
  BellOutlined,
  UserOutlined,
  LogoutOutlined,
  DownOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BulbOutlined,
  BulbFilled
} from '@ant-design/icons-vue';
import { useUserStore } from "@/store/index";
import { logout } from '@/api/system/auth';
import { useConfigStore, useNoticeStore } from "@/store/index";

const userStore = useUserStore();

// 路由相关
const router = useRouter();
const route = useRoute();

// 计算属性
const userInfo = computed(() => userStore.basicInfo);

// 菜单状态
const menuState = reactive({
  collapsed: false,
  rootSubmenuKeys: [],
  openKeys: [],
  selectedKeys: [route.path],
  menus: []
});

// 切换菜单折叠状态
const toggleCollapsed = () => {
  menuState.collapsed = !menuState.collapsed;
};

// 处理用户菜单点击
const handleUserMenuClick: MenuProps['onClick'] = ({ key }) => {
  switch (key) {
    case 'profile':
      router.push('/profile');
      break;
    case 'logout':
      handleLogout();
      break;
  }
};

// 处理退出登录
const handleLogout = async () => {
  try {
    await logout({ token: storage.get('Access-Token') });
    storage.remove('Access-Token');
    storage.remove('Refresh-Token');
    await userStore.clearUserInfo;
    router.push('/login');
  } catch (error) {
    console.error('退出登录失败:', error);
  }
};

// 处理菜单点击
const handleMenuClick: MenuProps['onClick'] = (menuInfo) => {
  menuState.openKeys = menuInfo.keyPath.slice(0, -1) as string[];
  router.push(menuInfo.key.toString());
};

// 监听路由变化
watch(() => route.path, (newPath) => {
  const routePath = userStore.routeList.map(item => item.route_path);
  if (!routePath.includes(newPath)) {
    menuState.openKeys = [];
    menuState.selectedKeys = [];
  } else {
    menuState.selectedKeys = [newPath];
  }
});

// 生成菜单项
const generateMenuItem = (item: any): ItemType => {
  const icon = item.icon ? () => h(icons[item.icon]) : null;
  const children = item.children?.length
    ? item.children
      .filter((child: any) => !child.hidden)
      .map(generateMenuItem)
    : undefined;

  return {
    key: item.route_path,
    title: item.name,
    label: item.name,
    icon: icon,
    children: children?.length ? children : undefined
  };
};

// 初始化菜单
const initMenu = () => {
  // 确保路由列表存在
  if (!userStore.routeList?.length) {
    return;
  }

  const menuTree = listToTree(userStore.routeList);
  menuState.menus = menuTree
    .filter(item => !item.hidden)
    .map(generateMenuItem)
    .filter(item => item !== null);

  // 设置当前选中的菜单
  const currentPath = route.path;
  menuState.selectedKeys = [currentPath];

  // 设置展开的菜单
  const findParentPath = (menus: any[], targetPath: string, parentPath: string[] = []): string[] => {
    for (const menu of menus) {
      if (menu.key === targetPath) {
        return parentPath;
      }
      if (menu.children?.length) {
        const result = findParentPath(menu.children, targetPath, [...parentPath, menu.key]);
        if (result.length) {
          return result;
        }
      }
    }
    return [];
  };

  menuState.openKeys = findParentPath(menuState.menus, currentPath);
};

// 打开文档
const openDocumentation = () => {
  window.open('/site/index.html', '_blank');
};

// 主题相关
const isDarkMode = inject('isDarkMode') as Ref<boolean>
const toggleTheme = inject('toggleTheme') as (darkMode: boolean) => void

// 切换主题
const handleThemeChange = () => {
  toggleTheme(!isDarkMode.value)
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

const noticeStore = useNoticeStore();
// 通知状态管理
const noticeState = reactive({
  notices: computed(() => noticeStore.noticeList),
  total: computed(() => noticeStore.total),
  loading: false
});

const configStore = useConfigStore();

const initConfigState = reactive({
  web_title: computed(() => configStore.getConfigValue("title")),
  web_favicon: computed(() => configStore.getConfigValue("logo")),
});

// 在页面加载时获取通知列表
onMounted(() => {
  initMenu();
  noticeStore.getNotice();
});
</script>

<style lang="scss" scoped>
.header-centent {
  height: calc(100vh - 146px); // 减去header高度
}

// 调整内容区域的上边距
.layout-content {
  overflow-y: auto;
  overflow-x: hidden;
  padding: 16px;
}

.basic-layout {
  // height: 100vh;
  // background-size: cover;
  // min-height: 100vh;

  .layout-sider {
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 99;

    .logo-container {
      height: 64px;
      padding: 16px;
      display: flex;
      align-items: center;
      justify-content: center;

      .logo-title {
        margin: 0 0 0 12px;
        font-weight: 600;
        font-size: 18px;
        white-space: nowrap;
        overflow: hidden;
      }
    }

    .side-menu {
      height: calc(100vh - 64px);
      border-right: 0;
      padding: 4px 0;
      overflow-y: auto;
      overflow-x: hidden;
    }
  }

  .layout-main {
    margin-left: 240px;
    transition: all 0.3s;
    width: calc(100% - 240px);

    padding-top: 108px; // 等于header高度

    &.collapsed {
      margin-left: 80px;
      width: calc(100% - 80px);

      .layout-header {
        transition: left 0.2s;
        left: 80px; // 菜单折叠时调整头部左边距
      }

      .header-tag {
        transition: left 0.2s;
        left: 80px; // 菜单折叠时调整头部左边距
      }
    }

    .header-tag {
      background: var(--component-background);
      padding: 0px;

      // 新增样式，让头部固定在顶部
      position: fixed;
      top: 64px;
      left: 240px;
      right: 0;
      z-index: 98;
      transition: left 0.3s;
    }

    .layout-header {
      background: var(--component-background);
      padding: 6px;
      display: flex;

      // 新增样式，让头部固定在顶部
      position: fixed;
      top: 0;
      left: 240px;
      right: 0;
      z-index: 98;
      transition: left 0.3s;
    }

    .header-left {
      display: flex;
      align-items: center;

      .collapse-btn {
        padding: 0 6px;
        font-size: 18px;
        cursor: pointer;
        transition: color 0.3s;

        &:hover {
          color: var(--primary-color);
        }
      }
    }

    .header-right {
      display: flex;
      align-items: center;
      margin-left: auto;

      .tool-btn {
        padding: 0 12px;
        font-size: 16px;
        cursor: pointer;

        &:hover {
          color: var(--primary-color);
        }
      }

      .user-dropdown {
        display: flex;
        align-items: center;
        padding: 0 12px;
        cursor: pointer;

        .username {
          margin: 0 8px;
          color: var(--text-color);
          white-space: nowrap;
        }
      }
    }
  }
}

.notice-content {
  max-height: 100px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}

// 添加通知图标的hover效果
.tool-btn {
  &:hover {
    .anticon {
      color: var(--primary-color);
    }
  }
}

:deep(.ant-list-item-meta-title) {
  font-weight: 500;
  margin-bottom: 8px;
}

:deep(.ant-badge-status-dot) {
  margin-right: 8px;
}

// 添加通知弹出框样式
.notice-popover {
  width: 240px;
  max-height: 400px;

  .notice-header {
    font-size: 14px;
    font-weight: 500;
    padding: 4px 0;
  }

  .notice-content {
    margin-top: 4px;
    font-size: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  :deep(.ant-list-item) {
    padding: 8px 0;
  }

  :deep(.ant-list-item-meta-title) {
    margin-bottom: 0;
  }
}
</style>
