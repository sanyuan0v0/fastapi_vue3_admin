<template>
    <a-breadcrumb :routes="routes">
        <template #itemRender="{ route, routes }">
            <span v-if="isLastRoute(route, routes)">{{ route.breadcrumbName }}</span>
            <router-link v-else :to="route.path">{{ route.breadcrumbName }}</router-link>
        </template>
    </a-breadcrumb>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';
import { useRoute } from "vue-router";

interface BreadcrumbRoute {
    path: string;
    breadcrumbName?: string;
}

const route = useRoute();
const routes = ref<BreadcrumbRoute[]>([]);

const isLastRoute = (currentRoute: BreadcrumbRoute, allRoutes: BreadcrumbRoute[]) => {
    return allRoutes.indexOf(currentRoute) === allRoutes.length - 1;
};

const getBreadcrumb = () => {
    const matchedRoutes = route.matched
        .filter((_, index) => index > 0) // 跳过第一个匹配项
        .map(item => ({
            path: item.path,
            breadcrumbName: item.meta.title?.toString()
        }));
    
    routes.value = matchedRoutes.length > 1 ? matchedRoutes : [];
};

// 初始化并监听路由变化
watch(() => route.path, getBreadcrumb, { immediate: true });
</script>

<style scoped>
/* 可以添加一些样式优化 */
.a-breadcrumb {
    margin: 12px 0;
}
</style>
