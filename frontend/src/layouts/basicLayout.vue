<template>
  <a-layout class="basic-layout">
    <!-- 左侧导航 -->
    <a-layout-sider class="layout-sider"
      :collapsed="menuState.collapsed"
      theme="light"
      :trigger="null"
      collapsible
      :width="240"
      :collapsedWidth="80"
    >
      <!-- Logo 区域 -->
      <div class="logo-container">
        <a-image src="/logo.png" :preview="false" :width="28" :height="28" />
        <h1 class="logo-title" v-show="!menuState.collapsed">fastapi-vue-admin</h1>
      </div>
      
      <a-menu
        class="side-menu"
        mode="inline"
        theme="light"
        v-model:openKeys="menuState.openKeys"
        v-model:selectedKeys="menuState.selectedKeys"
        :items="menuState.menus"
        @click="handleMenuClick"
      />
    </a-layout-sider>

    <!-- 右侧布局 -->
    <a-layout class="layout-main" :class="{ collapsed: menuState.collapsed }">
      <!-- 顶部导航栏 -->
      <a-layout-header class="layout-header" >
          
          <div class="header-left" >
            <!-- 左侧折叠按钮 -->
            <a-button 
              type="link" 
              class="collapse-btn"
              @click="toggleCollapsed"
            >
              <MenuFoldOutlined v-if="menuState.collapsed" />
              <MenuUnfoldOutlined v-else />
            </a-button>
            
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
            <a-badge :count="unreadCount" :dot="unreadCount > 99">
              <a-button type="link" @click="openNotification" class="tool-btn">
                <BellOutlined />
              </a-button>
            </a-badge>

            <!-- 用户信息下拉菜单 -->
            <a-dropdown>
              <div class="user-dropdown">
                <a-avatar :src="userAvatar" :size="32" />
                <span class="username">{{ username }}</span>
                <DownOutlined />
              </div>
              <template #overlay>
                <a-menu @click="handleUserMenuClick">
                  <a-menu-item key="profile">
                    <template #icon><UserOutlined /></template>
                    个人中心
                  </a-menu-item>
                  <a-menu-divider />
                  <a-menu-item key="logout">
                    <template #icon><LogoutOutlined /></template>
                    退出登录
                  </a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </div>
      </a-layout-header>
      
      <!-- 主内容区 -->
      <a-layout-content class="layout-content">
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
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script lang="ts" setup>
import { reactive, computed, watch, onMounted, inject, type Ref } from "vue";
import type { MenuProps, ItemType } from "ant-design-vue";
import { useRouter, useRoute } from "vue-router";
import storage from 'store';
import store from '@/store';
import * as icons from '@ant-design/icons-vue';
import { h } from 'vue';
import { listToTree } from '@/utils/util';
import { logout } from '@/api/system/auth';
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

// 路由相关
const router = useRouter();
const route = useRoute();

// 计算属性
const username = computed(() => store.state.user.basicInfo.username);
const userAvatar = computed(() => store.state.user.basicInfo.avatar);
const unreadCount = computed(() => 5); // 这里可以替换为实际的未读消息数量

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
    await store.dispatch('clearUserInfo');
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
  const routePath = store.state.user.routeList.map(item => item.route_path);
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
  if (!store.state.user.routeList?.length) {
    return;
  }

  const menuTree = listToTree(store.state.user.routeList);
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

// 打开通知面板
const openNotification = () => {
  console.log('打开通知面板');
};

// 主题相关
const isDarkMode = inject('isDarkMode') as Ref<boolean>
const toggleTheme = inject('toggleTheme') as (darkMode: boolean) => void

// 切换主题
const handleThemeChange = () => {
  toggleTheme(!isDarkMode.value)
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

onMounted(() => {
  initMenu();
});
</script>

<style lang="scss" scoped>
.basic-layout {
  min-height: 100vh;
  display: flex;
  
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
      border-bottom: 1px solid var(--border-color);
      
      .logo-title {
        margin: 0 0 0 12px;
        color: var(--text-color);
        font-weight: 600;
        font-size: 18px;
        white-space: nowrap;
        overflow: hidden;
      }
    }
    
    .side-menu {
      height: calc(100vh - 64px);
      border-right: 0;
      padding: 16px 0;
      overflow-y: auto;
      overflow-x: hidden;
      
      :deep(.ant-menu-item) {
        margin: 4px 8px;
        padding: 0 16px;
        border-radius: 4px;
        
        &.ant-menu-item-selected {
          background: rgba(24, 144, 255, 0.1);
          color: var(--primary-color);
          font-weight: 500;
        }
      }
    }
  }

  .layout-main {
    margin-left: 240px;
    transition: all 0.3s;
    width: calc(100% - 240px);
    
    &.collapsed {
      margin-left: 80px;
      width: calc(100% - 80px);
    }

    .layout-header {
      background: var(--component-background);
      padding: 16px;
      display: flex;

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

    .layout-content {
      padding: 24px;
      min-height: calc(100vh - var(--header-height));
    }
  }
}

</style>