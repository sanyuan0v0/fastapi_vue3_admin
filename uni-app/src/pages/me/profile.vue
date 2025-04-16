<template>
    <view class="detail-container">
        <up-cell-group>
            <up-cell title="头像" :border="true">
                <template #right-icon>
                    <up-avatar :src="formData.avatar" shape="circle" size="40" mode="scaleToFill"
                        bgColor="#c0c4cc" color="#ffffff" fontSize="35px" name="level">
                    </up-avatar>
                </template>
            </up-cell>
            <up-cell title="编号" :value="formData.id" :border="true"></up-cell>
            <up-cell title="用户名" :value="formData.name" :border="true"></up-cell>
            <up-cell title="账号" :value="formData.username" :border="true"></up-cell>
            <up-cell title="状态">
                <template #value>
                    <up-tag :text="formData.available ? '启用' : '禁用'" :type="formData.available ? 'success' : 'warning'" plain plainFill></up-tag>
                </template>
            </up-cell>
            <up-cell title="类型">
                <template #value>
                    <up-tag :text="formData.is_superuser ? '管理员' : '普通用户'" :type="formData.is_superuser ? 'error' : 'primary'" plain plainFill ></up-tag>
                </template>
            </up-cell>
            <up-cell title="部门" :value="formData.dept_name" :border="true"></up-cell>
            <up-cell title="邮箱" :value="formData.email" :border="true"></up-cell>
            <up-cell title="手机号" :value="formData.mobile" :border="true"></up-cell>
            <up-cell title="性别">
                <template #value>
                    <up-tag :text="formData.gender==0? '男' : formData.gender==1? '女' : '未知'" :type="formData.gender==0? 'success' : formData.gender==1? 'warning' : 'info'" plain plainFill></up-tag>
                </template>
            </up-cell>
            <up-cell title="描述" :value="formData.description || '暂无描述'" :border="true"></up-cell>
            <up-cell title="创建时间" :value="formData.created_at" :border="true"></up-cell>
            <up-cell title="更新时间" :value="formData.updated_at" :border="true"></up-cell>
        </up-cell-group>
    </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '../../stores/index';

const userStore = useUserStore();
const loading = ref(false);
const formData = ref({
	id: null,
	name: "",
	username: "",
	available: null,
	is_superuser: null,
	avatar: "",
	dept_name: "",
	email: "",
	mobile: "",
	gender: null, // 0男 1女 2未知
	description: "",
	created_at: "",
	updated_at: "",
});


onLoad(async () => {
    loading.value = true;
	await userStore.getUserInfo();
	formData.value = userStore.basic_info;
	loading.value = false;
})

</script>

<style lang="scss" scoped>
.detail-container {
    padding: 60rpx 60rpx;
}
</style>
