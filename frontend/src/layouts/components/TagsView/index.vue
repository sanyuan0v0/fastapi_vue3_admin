<template>
  <div ref="tags-container" class="tags-container">
    <!-- 向左移动按钮 -->
    <el-icon class="btn" @click="scrollLeft">
      <DArrowLeft />
    </el-icon>

    <!-- 标签导航容器 -->
    <nav role="navigation" class="scroll-wrapper">

      <el-scrollbar ref="scrollbarRef" class="scroll-container" @wheel="handleScroll">
        <VueDraggable v-model="visitedViews" :animation="150">
          <router-link 
            v-for="tag in visitedViews" :key="tag.fullPath"
            :class="['tags-item', { active: tagsViewStore.isActive(tag) }]" :to="{ path: tag.path, query: tag.query }"
            @click.middle="handleMiddleClick(tag)">
            <el-dropdown 
              v-if="tagsViewStore.isActive(tag)" trigger="contextmenu"
              @visible-change="onContextMenuVisibleChange" @click.stop>
              <span class="tag-text">{{ translateRouteTitle(tag.title) }}</span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="refreshSelectedTag(tag)">
                    <el-icon>
                      <Refresh />
                    </el-icon>
                    {{ t("navbar.refresh") }}
                  </el-dropdown-item>
                  <el-dropdown-item :disabled="tag.affix || visitedViews.length <= 1" @click="closeSelectedTag(tag)">
                    <el-icon>
                      <Close />
                    </el-icon>
                    {{ t("navbar.close") }}
                  </el-dropdown-item>
                  <el-dropdown-item :disabled="isFirstView || !tagsViewStore.isActive(tag)" @click="closeLeftTags">
                    <el-icon>
                      <Back />
                    </el-icon>
                    {{ t("navbar.closeLeft") }}
                  </el-dropdown-item>
                  <el-dropdown-item :disabled="isLastView || !tagsViewStore.isActive(tag)" @click="closeRightTags">
                    <el-icon>
                      <Right />
                    </el-icon>
                    {{ t("navbar.closeRight") }}
                  </el-dropdown-item>
                  <el-dropdown-item 
                    :disabled="visitedViews.length <= 1 || !tagsViewStore.isActive(tag)"
                    @click="closeOtherTags">
                    <el-icon>
                      <Remove />
                    </el-icon>
                    {{ t("navbar.closeOther") }}
                  </el-dropdown-item>
                  <el-dropdown-item :disabled="visitedViews.length <= 1" @click="closeAllTags(tag)">
                    <el-icon>
                      <Minus />
                    </el-icon>
                    {{ t("navbar.closeAll") }}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <span v-else class="tag-text">{{ translateRouteTitle(tag.title) }}</span>
            <span v-if="!tag.affix" class="tag-close-btn" @click.prevent.stop="closeSelectedTag(tag)">
              <el-icon>
                <Close />
              </el-icon>
            </span>
          </router-link>
        </VueDraggable>

      </el-scrollbar>
    </nav>

    <!-- 向右移动按钮 -->
    <el-icon class="btn" @click="scrollRight">
      <DArrowRight />
    </el-icon>

    <!-- 刷新按钮 -->
    <el-icon class="btn" @click="refreshSelectedTag(selectedTag)">
      <RefreshRight />
    </el-icon>

    <!-- 设置按钮 -->
    <el-dropdown class="btn" trigger="click">
      <el-icon>
        <Setting />
      </el-icon>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="handleAction('refresh')">
            <el-icon>
              <Refresh />
            </el-icon>
            {{ t("navbar.refresh") }}
          </el-dropdown-item>

          <el-dropdown-item v-if="!selectedTag?.affix" @click="handleAction('close')">
            <el-icon>
              <Close />
            </el-icon>
            {{ t("navbar.close") }}
          </el-dropdown-item>

          <el-dropdown-item :disabled="isFirstView" @click="handleAction('closeLeft')">
            <el-icon>
              <Back />
            </el-icon>
            {{ t("navbar.closeLeft") }}
          </el-dropdown-item>

          <el-dropdown-item :disabled="isLastView" @click="handleAction('closeRight')">
            <el-icon>
              <Right />
            </el-icon>
            {{ t("navbar.closeRight") }}
          </el-dropdown-item>

          <el-dropdown-item :disabled="!selectedTag" @click="handleAction('closeOther')">
            <el-icon>
              <Remove />
            </el-icon>
            {{ t("navbar.closeOther") }}
          </el-dropdown-item>

          <el-dropdown-item @click="handleAction('closeAll')">
            <el-icon>
              <Minus />
            </el-icon>
            {{ t("navbar.closeAll") }}
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter, type RouteRecordRaw } from "vue-router";
import { resolve } from "path-browserify";
import { translateRouteTitle } from "@/utils/i18n";
import { usePermissionStore, useTagsViewStore } from "@/store";
import { VueDraggable } from "vue-draggable-plus";

const { t } = useI18n();

const router = useRouter();
const route = useRoute();

// 状态管理
const permissionStore = usePermissionStore();
const tagsViewStore = useTagsViewStore();


const { visitedViews } = storeToRefs(tagsViewStore);


// 当前选中的标签
const selectedTag = ref<TagView | null>(null);

// 滚动条引用
const scrollbarRef = ref();

// 路由映射缓存，提升查找性能
const routePathMap = computed(() => {
  const map = new Map<string, TagView>();
  visitedViews.value.forEach((tag) => {
    map.set(tag.path, tag);
  });
  return map;
});

// 判断是否为第一个标签
const isFirstView = computed(() => {
  if (!selectedTag.value) return false;
  return (
    selectedTag.value.path === "/dashboard" ||
    selectedTag.value.fullPath === visitedViews.value[1]?.fullPath
  );
});

// 判断是否为最后一个标签
const isLastView = computed(() => {
  if (!selectedTag.value) return false;
  return selectedTag.value.fullPath === visitedViews.value[visitedViews.value.length - 1]?.fullPath;
});

/**
 * 递归提取固定标签
 */
const extractAffixTags = (routes: RouteRecordRaw[], basePath = "/"): TagView[] => {
  const affixTags: TagView[] = [];

  const traverse = (routeList: RouteRecordRaw[], currentBasePath: string) => {
    routeList.forEach((route) => {
      const fullPath = resolve(currentBasePath, route.path);

      // 如果是固定标签，添加到列表
      if (route.meta?.affix) {
        affixTags.push({
          path: fullPath,
          fullPath,
          name: String(route.name || ""),
          title: route.meta.title || "no-name",
          affix: true,
          keepAlive: route.meta.keepAlive || false,
        });
      }

      // 递归处理子路由
      if (route.children?.length) {
        traverse(route.children, fullPath);
      }
    });
  };

  traverse(routes, basePath);
  return affixTags;
};

/**
 * 初始化固定标签
 */
const initAffixTags = () => {
  const affixTags = extractAffixTags(permissionStore.routes);

  affixTags.forEach((tag) => {
    if (tag.name) {
      tagsViewStore.addVisitedView(tag);
    }
  });
};

/**
 * 添加当前路由标签
 */
const addCurrentTag = () => {
  if (!route.meta?.title) return;

  tagsViewStore.addView({
    name: route.name as string,
    title: route.meta.title,
    path: route.path,
    fullPath: route.fullPath,
    affix: route.meta.affix || false,
    keepAlive: route.meta.keepAlive || false,
    query: route.query,
  });
};

/**
 * 更新当前标签
 */
const updateCurrentTag = () => {
  nextTick(() => {
    const currentTag = routePathMap.value.get(route.path);

    if (currentTag && currentTag.fullPath !== route.fullPath) {
      tagsViewStore.updateVisitedView({
        name: route.name as string,
        title: route.meta?.title || "",
        path: route.path,
        fullPath: route.fullPath,
        affix: route.meta?.affix || false,
        keepAlive: route.meta?.keepAlive || false,
        query: route.query,
      });
    }
  });
};

/**
 * 处理中键点击
 */
const handleMiddleClick = (tag: TagView) => {
  if (!tag.affix) {
    closeSelectedTag(tag);
  }
};

/**
 * 处理滚轮事件（优化后）
 */
const handleScroll = (event: WheelEvent) => {

  const scrollWrapper = scrollbarRef.value?.wrapRef;
  if (!scrollWrapper) return;

  // 检查是否有水平或垂直滚动
  const hasHorizontalScroll = scrollWrapper.scrollWidth > scrollWrapper.clientWidth;
  const hasVerticalScroll = scrollWrapper.scrollHeight > scrollWrapper.clientHeight;

  if (!hasHorizontalScroll && !hasVerticalScroll) return;

  const deltaY = event.deltaY || -(event as any).wheelDelta || 0;
  const deltaX = event.deltaX || 0;

  // 计算新的滚动位置
  const newScrollLeft = Math.max(0, Math.min(scrollWrapper.scrollWidth - scrollWrapper.clientWidth, scrollWrapper.scrollLeft + deltaX));
  const newScrollTop = Math.max(0, Math.min(scrollWrapper.scrollHeight - scrollWrapper.clientHeight, scrollWrapper.scrollTop + deltaY));

  scrollbarRef.value.setScrollLeft(newScrollLeft);
  scrollbarRef.value.setScrollTop(newScrollTop); // 新增垂直滚动支持
};

/**
 * 刷新标签
 */
const refreshSelectedTag = (tag: TagView | null) => {
  // 总是使用当前路由对应的标签
  const currentTag = routePathMap.value.get(route.path);
  if (!currentTag) return;

  tagsViewStore.delCachedView(currentTag);
  nextTick(() => {
    router.replace("/redirect" + currentTag.fullPath);
  });
};

/**
 * 关闭标签
 */
const closeSelectedTag = (tag: TagView | null) => {
  // 总是使用当前路由对应的标签
  const currentTag = routePathMap.value.get(route.path);
  if (!currentTag) return;

  tagsViewStore.delView(currentTag).then((result: any) => {
    if (tagsViewStore.isActive(currentTag)) {
      tagsViewStore.toLastView(result.visitedViews, currentTag);
    }
  });
};

/**
 * 关闭左侧标签
 */
const closeLeftTags = () => {
  if (!selectedTag.value) return;

  tagsViewStore.delLeftViews(selectedTag.value).then((result: any) => {
    const hasCurrentRoute = result.visitedViews.some((item: TagView) => item.path === route.path);

    if (!hasCurrentRoute) {
      tagsViewStore.toLastView(result.visitedViews);
    }
  });
};

/**
 * 关闭右侧标签
 */
const closeRightTags = () => {
  if (!selectedTag.value) return;

  tagsViewStore.delRightViews(selectedTag.value).then((result: any) => {
    const hasCurrentRoute = result.visitedViews.some((item: TagView) => item.path === route.path);

    if (!hasCurrentRoute) {
      tagsViewStore.toLastView(result.visitedViews);
    }
  });
};

/**
 * 关闭其他标签
 */
const closeOtherTags = () => {
  if (!selectedTag.value) return;

  router.push(selectedTag.value);
  tagsViewStore.delOtherViews(selectedTag.value).then(() => {
    updateCurrentTag();
  });
};

/**
 * 关闭所有标签
 */
const closeAllTags = (tag: TagView | null) => {
  tagsViewStore.delAllViews().then((result: any) => {
    tagsViewStore.toLastView(result.visitedViews, tag || undefined);
  });
};

/**
 * 统一处理标签操作
 */
const handleAction = (action: string) => {
  // 总是使用当前路由对应的标签
  const currentTag = routePathMap.value.get(route.path);
  if (!currentTag) return;

  switch (action) {
    case 'refresh':
      refreshSelectedTag(currentTag);
      break;
    case 'close':
      closeSelectedTag(currentTag);
      break;
    case 'closeRight':
      closeRightTags();
      break;
    case 'closeLeft':
      closeLeftTags();
      break;
    case 'closeOther':
      closeOtherTags();
      break;
    case 'closeAll':
      closeAllTags(currentTag);
      break;
    default:
      console.warn(`Unknown action: ${action}`);
  }
};

/**
 * 右键菜单显示状态变化处理函数
 */
const onContextMenuVisibleChange = (visible: boolean) => {
  if (visible) {
    // 总是获取最新的路由对应标签
    selectedTag.value = routePathMap.value.get(route.path) || null;
  } else {
    // 关闭菜单时清空选择
    selectedTag.value = null;
  }
};

/**
 * 向左滚动标签页
 */
const scrollLeft = () => {
  const scrollWrapper = scrollbarRef.value?.wrapRef
  if (!scrollWrapper) return

  const newScrollLeft = Math.max(0, scrollWrapper.scrollLeft - 200)
  scrollbarRef.value.setScrollLeft(newScrollLeft)
}

/**
 * 向右滚动标签页
 */
const scrollRight = () => {
  const scrollWrapper = scrollbarRef.value?.wrapRef
  if (!scrollWrapper) return

  const maxScrollLeft = scrollWrapper.scrollWidth - scrollWrapper.clientWidth
  const newScrollLeft = Math.min(maxScrollLeft, scrollWrapper.scrollLeft + 200)
  scrollbarRef.value.setScrollLeft(newScrollLeft)
}

// 监听路由变化
watch(
  route,
  () => {
    addCurrentTag();
    updateCurrentTag();
  },
  { immediate: true }
);

// 初始化
onMounted(() => {
  initAffixTags();
});

</script>

<style lang="scss" scoped>
.tags-container {
  display: flex;
  align-items: center;
  width: 100%;
  height: $tags-view-height;
  background-color: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  box-shadow: 0 1px 1px var(--el-box-shadow-light);

  .btn {
    top: 1px;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: $tags-view-height;
    height: $tags-view-height;
    cursor: pointer;
    border: 1px solid var(--el-border-color-light);
    

    &:hover {
      background-color: var(--el-fill-color-light);
      color: var(--el-color-primary);

      .el-icon {
        transform: scale(1.1);
      }
    }
  }

  .scroll-wrapper {
    flex: 1;
    overflow: hidden;
  }

  .scroll-container {
    white-space: nowrap;
  }

  .tags-item {
    position: relative;
    display: inline-flex;
    align-items: center;
    height: 26px;
    padding: 0 8px;
    margin-left: 5px;
    font-size: 12px;
    line-height: 26px;
    color: var(--el-text-color-primary);
    background: var(--el-bg-color);
    border: 1px solid var(--el-border-color);
    transition: all 0.2s ease;

    &:first-of-type {
      margin-left: 5px;
    }
    &:last-of-type {
      margin-right: 5px;
    }

    &:hover {
      background-color: var(--el-fill-color);
    }

    .tag-text {
      display: inline-block;
      vertical-align: middle;
    }

    .tag-close-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 16px;
      height: 16px;
      margin-left: 5px;
      font-size: 12px;
      font-weight: bold;
      color: var(--el-text-color-secondary);
      cursor: pointer;
      border-radius: 50%;
      transition: all 0.2s ease;

      &:hover {
        color: var(--el-color-white);
        background-color: var(--el-text-color-placeholder);
      }
    }

    &.active {
      color: var(--el-color-white);
      background-color: var(--el-color-primary);
      border-color: var(--el-color-primary);

      &::before {
        position: relative;
        display: inline-block;
        width: 8px;
        height: 8px;
        margin-right: 2px;
        content: "";
        background: var(--el-color-white);
        border-radius: 50%;
      }

      .tag-text {
        color: var(--el-color-white);
      }

      .tag-close-btn {
        color: var(--el-color-white);

        &:hover {
          color: var(--el-color-white);
          background-color: rgba(255, 255, 255, 0.3);
        }
      }
    }
  }
}
</style>
