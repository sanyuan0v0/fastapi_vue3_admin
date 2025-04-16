<template>
	<app-layout>
		<template #main>
			<view class="me-container">
				<!-- 个人信息卡片 -->
				<up-card padding="40rpx" margin="0 0 30rpx 0" :shadow="3" :borderRadius="20" :show-head="false">
					<template #body>
						<view class="user-info-container">
							<up-avatar :src="formData.avatar || '/static/logo.png'" shape="circle"
								size="80" class="user-avatar"></up-avatar>
							<view class="user-details">
								<up-text :text="formData.name" bold size="20"></up-text>
								<up-text :text="formData.username" type="info" margin="10rpx 0 0 0"
									prefix-icon="account"></up-text>
								<up-text :text="formData.mobile" type="info" margin="10rpx 0 0 0"
									prefix-icon="phone"></up-text>
							</view>
							<up-button type="primary" size="small" text="个人主页" @click="handleToProfile(formData.id)" class="profile-button"></up-button>
						</view>
					</template>
				</up-card>

				<!-- 数据统计 -->
				<up-grid :border="false" col="4" align="center" class="stats-grid">
					<up-grid-item v-for="item in dataItems" :key="item.title" :border="true" class="stats-item">
						<view class="stats-content">
							<view class="stats-value">
								<up-text :text="item.value" size="22" bold></up-text>
							</view>
							<view class="stats-title">
								<up-text :text="item.title" type="info" ></up-text>
							</view>
						</view>
					</up-grid-item>
				</up-grid>

				<!-- 功能菜单 -->
				<view class="menu-section">
					<up-cell-group>
						<up-cell title="个人资料" icon="account" isLink @click="handleToDetail(formData.id)"></up-cell>
						<up-cell title="系统设置" icon="setting" isLink @click="handleToUpdate(formData.id)"></up-cell>
						<up-cell title="安全中心" icon="lock" isLink @click="handletoPassword()"></up-cell>
						<up-cell title="消息中心" icon="bell" isLink @click="showContact = true"></up-cell>
					</up-cell-group>
				</view>

				<!-- 退出登录按钮 -->
				<view class="logout-btn">
					<up-button type="error" text="退出登录" :loading="loading" @click="handleLogout"></up-button>
				</view>
			</view>
		</template>
	</app-layout>
</template>

<script setup>
import { ref, computed, reactive } from 'vue';
import { onLoad, onReady, onShow } from '@dcloudio/uni-app';
import { logout } from "@/api/apis";
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
	last_login: "",
});
// 数据统计
const dataItems = ref([
	{ title: '待办事项', value: '5' },
	{ title: '消息通知', value: '3' },
	{ title: '收藏项目', value: '8' },
	{ title: '已完成', value: '12' }
]);


onReady(async () => {
	loading.value = true;
	await userStore.getUserInfo();
	formData.value = userStore.basic_info;
	loading.value = false;
});

// 添加onShow生命周期钩子
onShow(() => {
	formData.value = userStore.basic_info;
});


// 弹窗控制
const showContact = ref(false)

// 退出登录
const handleLogout = async () => {
	loading.value = true;
	logout({ token: userStore.access_token }).then(response => {
		if (response.status_code == 200) {
			useUserStore().clear();
			uni.reLaunch({ url: '/pages/login/login' });
		}
	}).catch(error => {
		console.error('退出登录失败', error)
	})
		.finally(() => loading.value = false);
};

// 个人主页按钮点击事件
const handleToProfile = () => {
	uni.navigateTo({ url: `/pages/me/profile` });
};

</script>

<style lang="scss" scoped>
.me-container {
	padding: 40rpx;
}

.user-info-container {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 20rpx;
}

.user-avatar {
	margin-right: 20rpx;
}

.user-details {
	flex: 1;
}

.profile-button {
	margin-left: 0;
	margin-right: 0;
	border-radius: 40rpx 0 0 40rpx;
	width: 160rpx;
	padding-right: 20rpx;
	position: absolute;
	right: 0;
}

.stats-item {
	position: relative;
	padding: 20rpx;
	
	&::after {
		content: '';
		position: absolute;
		right: 0;
		top: 20%;
		width: 1px;
		height: 60%;
		background: #ebedf0;
	}
}

.stats-content {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 12rpx;
}

.stats-value {
	margin: 8rpx 0;
	display: flex;
}

.stats-title {
	text-align: center;
}

.menu-section {
	margin: 40rpx 0;
	background: #ffffff;
	border-radius: 20rpx;
	box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.logout-btn {
	padding: 20rpx 0;
}

.contact-popup {
	width: 600rpx;
	padding: 40rpx;
	background: #fff;
	border-radius: 20rpx;
	position: relative;
	z-index: 100;

	.popup-header {
		display: flex;
	}


	.popup-footer {
		text-align: center;
		padding: 20rpx 0 0;
		border-top: 1px solid #eee;
	}
}
</style>