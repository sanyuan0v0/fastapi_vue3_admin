<template>
	<app-layout>
		<template #main>
			<view class="work-container">
				<!-- 通知栏 -->
				<up-notice-bar :text="noticeText" bg-color="#f0f7ff" color="#2979ff"></up-notice-bar>

				<!-- 轮播图 -->
				<view class="swiper-box">
					<up-swiper :list="swiperList" indicator indicator-pos="bottomCenter" radius="8" />
				</view>

				<!-- 常用功能 -->
				<view class="section-card">
					<view class="section-header">
						<up-row customStyle="margin-bottom: 10px">
							<up-col span="6">
								<up-text text="常用功能" bold align="left"></up-text>
							</up-col>
							<up-col span="6">
								<up-text type="primary" text="更多" class="more" @click="navigateToMore" align="right" />
							</up-col>
						</up-row>
					</view>
					<up-grid :col="4" :border="false" align="center">
						<up-grid-item v-for="(item, index) in commonFunctions" :key="index"
							@click="handleFunctionClick(item)">
							<view class="function-item">
								<up-icon :name="item.icon" :size="22" :color="item.color || '#2979ff'" />
								<text class="grid-text" margin-top="8" >{{ item.name }}</text>
							</view>
						</up-grid-item>
					</up-grid>
				</view>

				<!-- 应用分类 -->
				<view class="section-card">
					<up-text text="全部功能" bold></up-text>
					<view class="section-header">
						<up-tabs :list="appTabs" @click="handleTabChange" active-color="#2979ff"></up-tabs>
					</view>

					<!-- 对应分类内容 -->
					<up-grid :col="4" :border="false" align="center">
						<up-grid-item v-for="(app, index) in currentApps" :key="index" @click="handleAppClick(app)">
							<view class="app-item">
								<up-icon :name="app.icon" :size="22"  :color="app.color || '#2979ff'"/>
								<text class="grid-text" margin-top="8" >{{ app.name }}</text>
							</view>
						</up-grid-item>
					</up-grid>
				</view>
			</view>
		</template>
	</app-layout>
</template>

<script setup>
import { ref, computed } from 'vue';

// 常量数据
const noticeText = ref('体验公司全系产品 畅谈你的想法');
const swiperList = ref([
	'/static/banner/banner01.jpg',
	'/static/banner/banner02.jpg',
	'/static/banner/banner03.jpg'
]);

// 常用功能
const commonFunctions = ref([
	{ name: '审批', icon: 'file-text', color: '#52c41a' },
	{ name: '公告', icon: 'bell', color: '#faad14' },
	{ name: '日报', icon: 'edit-pen', color: '#13c2c2' },
	{ name: '周报', icon: 'calendar', color: '#2f54eb' },
	{ name: '工资单', icon: 'rmb', color: '#f5222d' },
	{ name: '待办', icon: 'list-dot', color: '#722ed1' },
	{ name: '打卡', icon: 'checkmark-circle', color: '#eb2f96' },
	{ name: '添加', icon: 'plus-circle', color: '#1890ff' }
]);

// 应用分类数据
const appTabs = ref([  
    { name: '关注' },  
    { name: '推荐' },  
    { name: '电影' },  
    { name: '科技' },  
    { name: '音乐' },  
    { name: '美食' },  
    { name: '文化' },  
    { name: '财经' },  
    { name: '手工' }  
]);  

const allApps = ref({
	office: [
		{ name: '审批', icon: 'checkmark-circle', color: '#52c41a' },
		{ name: '日报', icon: 'edit-pen' , color: '#faad14'},
		{ name: '周报', icon: 'list-dot' , color: '#13c2c2' },
		{ name: '云文档', icon: 'file-text' , color: '#2f54eb'},
		{ name: '项目管理', icon: 'grid' , color: '#f5222d'},
		{ name: '设计工具', icon: 'photo' , color: '#722ed1'},
		{ name: '分贝通', icon: 'coupon' , color: '#eb2f96'},
		{ name: '飞书提醒', icon: 'bell', color: '#1890ff' }
	],
	collab: [
		{ name: '项目管理', icon: 'grid', color: '#52c41a' },
		{ name: '设计工具', icon: 'photo' , color: '#52c41a'},
		{ name: '分贝通', icon: 'coupon' , color: '#52c41a'},
		{ name: '飞书提醒', icon: 'bell' , color: '#52c41a'}
	],
	finance: [
		{ name: '工资单', icon: 'rmb' , color: '#2f54eb'},
		{ name: '报销', icon: 'wallet' , color: '#2f54eb'},
		{ name: '预算', icon: 'pie-chart' , color: '#2f54eb'}
	],
	other: [
		{ name: '通讯录', icon: 'account' , color: '#eb2f96'},
		{ name: '设置', icon: 'settings', color: '#eb2f96' }
	]
});

// 当前选中标签
const currentTab = ref(0);
const currentApps = computed(() => {
  // 假设 appTabs 里有 type 属性对应 allApps 的键
  const type = appTabs.value[currentTab.value].type || 'office';
  return allApps.value[type] || [];
});

// 事件处理
const handleTabChange = (index) => {
	currentTab.value = index;
};

const handleFunctionClick = (item) => {
	console.log('点击功能:', item.name);
};

const handleAppClick = (app) => {
	console.log('点击应用:', app.name);
};

const navigateToMore = () => {
	console.log('跳转到更多页面');
};
</script>

<style lang="scss" scoped>
.work-container {
	padding: 20rpx;
}

.search-box {
	padding: 20rpx;
	background: #fff;
	margin: 20rpx;
	border-radius: 12rpx;
}

.swiper-box {
	margin: 20rpx;
	border-radius: 12rpx;
	overflow: hidden;
}

.section-card {
	background: #fff;
	margin: 20rpx;
	border-radius: 12rpx;
	padding: 24rpx;
	box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);

	.section-header {
		margin-bottom: 24rpx;
	}
}

.function-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 20rpx 0;
}

.app-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 16rpx 0;
}

.grid-text {
	font-size: 14px;
	color: #909399;
	padding: 10rpx 0 20rpx 0rpx;
	/* #ifndef APP-PLUS */
	box-sizing: border-box;
	/* #endif */
}

/* 调整tabs样式 */
::v-deep .up-tabs__wrapper {
	padding: 0 20rpx;
}

::v-deep .up-tabs__item {
	font-size: 28rpx !important;
	padding: 20rpx 0 !important;
}
</style>