<template>
  <view class="app-container">
    <wd-navbar title="网络测试" left-arrow @click-left="handleBack" />

    <!-- 网络状态展示 -->
    <wd-card title="网络状态" custom-style="margin: 20rpx">
      <wd-cell-group border>
        <wd-cell title="网络状态">
          <wd-tag :type="networkType ? 'success' : 'danger'" size="small">
            {{ networkType ? "在线" : "离线" }}
          </wd-tag>
        </wd-cell>
        <wd-cell title="网络类型" :value="networkType || '未知'" />
        <wd-cell title="网络强度" :value="signalStrength" />
      </wd-cell-group>
    </wd-card>

    <!-- 网络测试 -->
    <wd-card title="网络测试" custom-style="margin: 20rpx">
      <view slot="extra">
        <text class="text-gray-500 text-sm">测试服务器连接情况</text>
      </view>

      <wd-cell-group border>
        <wd-cell title="延迟">
          <view class="flex items-center">
            <text class="mr-10">{{ pingResult.delay }}ms</text>
            <wd-tag v-if="getPingStatus" :type="getPingStatusType" size="small">
              {{ pingResult.status }}
            </wd-tag>
          </view>
        </wd-cell>
      </wd-cell-group>

      <wd-progress
        v-if="testing"
        :percentage="progress"
        stroke-width="4"
        custom-style="margin: 30rpx 0"
      />

      <wd-button block type="primary" :loading="testing" @click="startTest">
        {{ testing ? "测试中..." : "开始测试" }}
      </wd-button>
    </wd-card>
  </view>
</template>

<script lang="ts" setup>
import request from "@/utils/request";

interface PingResult {
  delay: string | number;
  status: string;
}

// 声明全局 wx 对象
declare const wx: any;

// 响应式状态
const networkType = ref("");
const signalStrength = ref("获取中...");
const testing = ref(false);
const progress = ref(0);
const pingResult = ref<PingResult>({
  delay: "--",
  status: "未测试",
});
const networkListener = ref<any>(null);

// 计算属性
const getPingStatus = computed(() => {
  if (pingResult.value.delay === "--") return "";
  // 将 delay 转换为数字进行比较
  const delay = Number(pingResult.value.delay);
  if (isNaN(delay)) return "";
  if (delay < 100) return "good";
  if (delay < 300) return "normal";
  return "bad";
});

// 计算状态对应的Tag类型
const getPingStatusType = computed(() => {
  const status = getPingStatus.value;
  if (status === "good") return "success";
  if (status === "normal") return "warning";
  if (status === "bad") return "danger";
  return "primary";
});

// 方法
const getNetworkType = async () => {
  try {
    const res = await uni.getNetworkType();
    networkType.value = res.networkType;

    // 微信小程序支持获取信号强度
    // #ifdef MP-WEIXIN
    if (wx?.getNetworkWeakness) {
      const weaknessRes = await wx.getNetworkWeakness();
      signalStrength.value = `${weaknessRes.weaknessLevel}%`;
    } else {
      signalStrength.value = "不支持";
    }
    // #endif

    // H5环境
    // #ifdef H5
    signalStrength.value = (navigator as any).connection
      ? `${(navigator as any).connection.effectiveType || "未知"}`
      : "不支持";
    // #endif
  } catch {
    networkType.value = "获取失败";
    signalStrength.value = "获取失败";
  }
};

// 监听网络状态变化
const listenNetworkStatus = () => {
  // #ifdef MP-WEIXIN
  networkListener.value = wx?.onNetworkStatusChange((res: any) => {
    networkType.value = res.networkType;
    getNetworkType();
  });
  // #endif

  // #ifdef H5
  window.addEventListener("online", getNetworkType);
  window.addEventListener("offline", () => {
    networkType.value = "";
    signalStrength.value = "离线";
  });
  // #endif
};

// 开始网络测试
const startTest = async () => {
  if (testing.value) return;

  testing.value = true;
  progress.value = 0;
  pingResult.value.delay = "--";
  pingResult.value.status = "测试中";

  const progressTimer = setInterval(() => {
    if (progress.value < 90) {
      progress.value += 10;
    }
  }, 200);

  try {
    const startTime = Date.now();
    // #ifdef H5
    await uni.request({
      url: "/api/v1/auth/captcha",
      timeout: 5000,
    });
    // #endif
    // #ifndef H5
    await request({
      url: "/api/v1/auth/captcha",
      timeout: 5000,
    });
    // #endif
    const endTime = Date.now();
    const delay = endTime - startTime;

    pingResult.value.delay = delay;
    pingResult.value.status = delay < 300 ? "正常" : "较慢";
  } catch {
    pingResult.value.delay = "--";
    pingResult.value.status = "连接失败";
  } finally {
    clearInterval(progressTimer);
    progress.value = 100;
    setTimeout(() => {
      testing.value = false;
      progress.value = 0;
    }, 500);
  }
};

// 返回
const handleBack = () => {
  uni.navigateBack();
};

// 生命周期钩子
onMounted(() => {
  getNetworkType();
  listenNetworkStatus();
});

onBeforeUnmount(() => {
  // #ifdef MP-WEIXIN
  if (networkListener.value?.clear) {
    networkListener.value.clear();
  }
  // #endif

  // #ifdef H5
  window.removeEventListener("online", getNetworkType);
  window.removeEventListener("offline", getNetworkType);
  // #endif
});
</script>

<style lang="scss" scoped>
.mr-10 {
  margin-right: 10rpx;
}

.text-gray-500 {
  color: #9e9e9e;
}

.text-sm {
  font-size: 24rpx;
}

.flex {
  display: flex;
}

.items-center {
  align-items: center;
}
</style>
