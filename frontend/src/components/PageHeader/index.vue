<template>
    <a-page-header 
        :style="headerStyle" 
        :title="getPageTitle" 
    >
        <!-- 可以添加更多插槽，让组件更灵活 -->
        <template #extra>
            <slot name="extra"></slot>
        </template>
    </a-page-header>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

// 定义 props
const props = defineProps<{
    title?: string;
    headerStyle?: string;
}>();

const route = useRoute();

// 计算属性获取页面标题
const getPageTitle = computed(() => {
    return props.title || route.meta.title?.toString() || '未命名';
});
</script>

<style scoped>

</style>