<template>
    <a-result status="403" title="403" sub-title="抱歉,您没有权限访问该页面">
        <template #extra>
            <a-button type="primary" @click="toHome">返回首页</a-button>
        </template>
    </a-result>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";

const router = useRouter();
const toHome = () => {
    router.push('/');
};
</script>

<style lang="scss" scoped>
.ant-result {
    padding: 48px 32px;
}
</style>