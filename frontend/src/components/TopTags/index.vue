<template>
    <a-tabs 
        v-model:activeKey="activeKey" 
        hide-add 
        :animated="false"
        type="editable-card" 
        @edit="onEdit" 
        @change="onChange"
    >
        <a-tab-pane 
            v-for="pane in panes" 
            :key="pane.key" 
            :tab="pane.title" 
            :closable="pane.closable"
        />
    </a-tabs>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from "vue-router";
interface Pane {
    title: string;
    path: string;
    key: string;
    closable?: boolean;
}

const router = useRouter();
const route = useRoute();

const panes = ref<Pane[]>([
    { 
        title: '工作台', 
        path: '/dashboard/workplace', 
        key: '/dashboard/workplace', 
        closable: false 
    }
]);

const activeKey = ref(panes.value[0].key);

const getRoute = () => {
    const existingPane = panes.value.some(pane => pane.key === route.path);
    if (!existingPane) {
        panes.value.push({
            title: route.meta.title?.toString() || '未命名',
            path: route.path,
            key: route.path,
            closable: true
        });
    }
    activeKey.value = route.path;
}

const removePane = (targetKey: string) => {
    const paneIndex = panes.value.findIndex(pane => pane.key === targetKey);
    panes.value = panes.value.filter(pane => pane.key !== targetKey);
    
    if (activeKey.value === targetKey && panes.value.length) {
        const newIndex = Math.max(0, paneIndex - 1);
        activeKey.value = panes.value[newIndex].key;
        router.push(activeKey.value);
    }
};

const onEdit = (targetKey: string | MouseEvent, action: string) => {
    if (action === 'remove') {
        removePane(targetKey as string);
    }
};

const onChange = (targetKey: string) => {
    router.push(targetKey);
};

onMounted(getRoute);
watch(() => route.path, getRoute);
</script>

<style scoped>
/* 添加以下样式 */
:deep(.ant-tabs-nav) {
    will-change: transform;
    backface-visibility: hidden;
    margin: 0;
}

:deep(.ant-tabs-tab) {
    transition: none !important;
}

:deep(.ant-tabs-ink-bar) {
    transition: transform 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
}
</style>