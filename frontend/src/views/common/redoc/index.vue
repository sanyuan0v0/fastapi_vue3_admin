<template>

    <a-spin :spinning="loading">
        <div :style="'height:' + height">
            <iframe :src="url" frameborder="no" style="width: 100%; height: 100%" scrolling="auto" />
        </div>
    </a-spin>

</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
const height = ref(document.documentElement.clientHeight - 94.5 + "px;")
const loading = ref(true)
const url = ref(import.meta.env.VITE_APP_BASE_API + "/redoc")

onMounted(() => {
    setTimeout(() => {
        loading.value = false;
    }, 300);
    window.onresize = () => {
        height.value = document.documentElement.clientHeight - 94.5 + "px;";
    };
})
onBeforeUnmount(() => {
    window.onresize = null;
})
</script>
