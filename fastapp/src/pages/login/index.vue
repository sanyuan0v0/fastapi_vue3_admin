<template>
  <view class="app-container">
    <!-- 背景图 -->
    <image src="/static/images/login-bg.svg" mode="aspectFill" class="login-bg" />

    <!-- Logo和标题区域 -->
    <view class="header">
      <image src="/static/logo.png" class="logo" mode="aspectFit" />
      <text class="title">FastApp管理系统</text>
      <text class="subtitle">欢迎使用移动端管理平台</text>
    </view>

    <view class="login-card">
      <view class="form-wrap">
        <!-- 账号密码登录表单 -->
        <wd-form v-if="loginType === 'account'" ref="loginFormRef" :model="loginFormData">
          <!-- 用户名输入框 -->
          <view class="form-item">
            <wd-icon
              name="user"
              size="22"
              :color="isDarkMode ? '#7AC5FF' : '#333'"
              class="input-icon"
            />
            <input
              v-model="loginFormData.username"
              class="form-input input-transparent"
              placeholder="请输入用户名"
              placeholder-class="input-placeholder"
              @confirm="handleAccountLogin"
            />
          </view>
          <view class="divider"></view>

          <!-- 密码输入框 -->
          <view class="form-item">
            <wd-icon
              name="lock-on"
              size="22"
              :color="isDarkMode ? '#7AC5FF' : '#333'"
              class="input-icon"
            />
            <input
              v-model="loginFormData.password"
              class="form-input input-transparent"
              type="text"
              :password="showPassword ? false : true"
              placeholder="请输入密码"
              placeholder-class="input-placeholder"
              @confirm="handleAccountLogin"
            />
            <wd-icon
              :name="showPassword ? 'eye-open' : 'eye-close'"
              size="18"
              :color="isDarkMode ? '#7AC5FF' : '#9ca3af'"
              class="eye-icon"
              @click="showPassword = !showPassword"
            />
          </view>
          <!-- 验证码输入框 -->
          <view v-if="captchaState.enable" class="form-item captcha-item">
            <wd-icon
              name="lock-on"
              size="22"
              :color="isDarkMode ? '#7AC5FF' : '#333'"
              class="input-icon"
            />
            <input
              v-model="loginFormData.captcha"
              class="form-input input-transparent captcha-input"
              type="text"
              placeholder="请输入验证码"
              placeholder-class="input-placeholder"
              @confirm="handleAccountLogin"
            />
            <image
              :src="captchaState.img_base"
              class="captcha-image"
              mode="aspectFit"
              @click="getLoginCaptcha"
            />
            <view
              v-if="!captchaState.img_base && captchaState.enable"
              class="captcha-placeholder"
              @click="getLoginCaptcha"
            >
              <text>点击加载</text>
            </view>
          </view>
          <view class="divider"></view>

          <!-- 登录按钮 -->
          <button
            class="login-btn"
            :disabled="loading || !isFormValid"
            :style="{ opacity: loading || !isFormValid ? 0.7 : 1 }"
            @click="handleAccountLogin"
          >
            <wd-loading v-if="loading" size="20" color="#fff" />
            {{ loading ? "登录中..." : "账号登录" }}
          </button>

          <!-- 切换登录方式 -->
          <view class="switch-login-type" @click="loginType = 'phone'">
            <text>使用手机号一键登录</text>
            <wd-icon name="arrow-right" size="12" />
          </view>
        </wd-form>

        <!-- 手机号登录 -->
        <view v-else class="phone-login-form">
          <view class="phone-login-title">微信一键登录</view>
          <view class="phone-login-subtitle">授权后将获取您的手机号</view>

          <button
            class="wechat-phone-btn"
            :disabled="loading"
            open-type="getPhoneNumber"
            @getphonenumber="handleWechatPhoneLogin"
          >
            <wd-icon name="weixin" size="24" color="#ffffff" />
            <text>微信一键登录</text>
          </button>

          <!-- 切换登录方式 -->
          <view class="switch-login-type" @click="loginType = 'account'">
            <text>使用账号密码登录</text>
            <wd-icon name="arrow-right" size="12" />
          </view>
        </view>

        <!-- 其他登录方式 -->
        <view class="other-login">
          <view class="other-login-title">
            <view class="line"></view>
            <text class="text">其他登录方式</text>
            <view class="line"></view>
          </view>

          <view class="wechat-login" @click="handleWechatLogin">
            <view class="wechat-icon-wrapper">
              <image src="/static/icons/weixin.png" class="wechat-icon" />
            </view>
          </view>
        </view>

        <!-- 底部协议 -->
        <view class="agreement">
          <text class="text">登录即同意</text>
          <text class="link" @click="navigateToUserAgreement">《用户协议》</text>
          <text class="text">和</text>
          <text class="link" @click="navigateToPrivacy">《隐私政策》</text>
        </view>
      </view>
    </view>

    <wd-toast />
  </view>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/modules/user.store";
import { useToast } from "wot-design-uni";
import { useWechat } from "@/composables/useWechat";
import { useTheme } from "@/composables/useTheme";
import { computed, ref, reactive, watch } from "vue";
import AuthAPI, { type LoginFormData, type CaptchaInfo } from "@/api/auth";

const loginFormRef = ref();
const toast = useToast();
const userStore = useUserStore();
const showPassword = ref(false);
const loginType = ref<"account" | "phone">("account");
const { authState, getLoginCode, getPhoneNumber } = useWechat();
const { theme } = useTheme();

// 登录表单数据
const loginFormData = ref<LoginFormData>({
  username: "admin",
  password: "123456",
  captcha: "",
  captcha_key: "",
  remember: true,
});

// 验证码状态
const captchaState = reactive<CaptchaInfo>({
  enable: false,
  key: "",
  img_base: "",
});

// 防重复请求标志
const isCaptchaLoading = ref(false);

// 使用store的loading状态
const loading = computed(() => userStore.isLoggingIn || authState.value.isLogining);

// 表单验证
const isFormValid = computed(() => {
  const { username, password, captcha } = loginFormData.value;
  return !!(username?.trim() && password && (!captchaState.enable || (captcha && captcha.trim())));
});

// 获取验证码
const getLoginCaptcha = async () => {
  if (isCaptchaLoading.value) return;

  isCaptchaLoading.value = true;
  try {
    const result = await AuthAPI.getCaptcha();
    if (result && typeof result === "object") {
      captchaState.enable = Boolean(result.enable);
      captchaState.key = result.key || "";
      captchaState.img_base = result.img_base || result.img || "";
      if (captchaState.enable) {
        loginFormData.value.captcha = "";
        loginFormData.value.captcha_key = captchaState.key;
      }
    } else {
      captchaState.enable = false;
    }
  } catch (error: any) {
    toast.error(error?.message || "验证码获取失败");
    captchaState.img_base = "";
    captchaState.enable = false;
  } finally {
    isCaptchaLoading.value = false;
  }
};

// 统一的错误处理
const handleLoginError = (error: any, loginType: string) => {
  const message = error?.message || `${loginType}登录失败`;

  // 根据错误类型显示不同提示
  if (message.includes("验证码")) {
    toast.error("验证码错误，请重新输入");
    getLoginCaptcha(); // 刷新验证码
  } else if (message.includes("用户不存在") || message.includes("密码错误")) {
    toast.error("用户名或密码错误");
  } else if (message.includes("拒绝授权")) {
    toast.error("您已拒绝授权");
  } else {
    toast.error(message);
  }

  console.error(`${loginType}登录失败:`, error);
};

// 账号密码登录
const handleAccountLogin = async () => {
  if (!isFormValid.value) {
    if (!loginFormData.value.username.trim()) {
      toast.error("请输入用户名");
      return;
    }
    if (!loginFormData.value.password) {
      toast.error("请输入密码");
      return;
    }
    if (captchaState.enable && !loginFormData.value.captcha.trim()) {
      toast.error("请输入验证码");
      return;
    }
  }

  try {
    await userStore.login(loginFormData.value);
    toast.success("登录成功");

    // 登录成功后跳转到mine页面，确保用户信息及时更新
    uni.switchTab({ url: "/pages/mine/index" });
  } catch (error: any) {
    handleLoginError(error, "账号密码");
  }
};

// 微信一键登录（通过手机号）
const handleWechatPhoneLogin = async (e: any) => {
  if (!e.detail?.encryptedData) {
    toast.error("获取手机号失败");
    return;
  }

  try {
    const phoneData = await getPhoneNumber(e);
    await userStore.loginWithWxPhone(phoneData);
    toast.success("登录成功");

    // 登录成功后跳转到mine页面，确保用户信息及时更新
    uni.switchTab({ url: "/pages/mine/index" });
  } catch (error: any) {
    handleLoginError(error, "微信手机号");
  }
};

// 微信授权登录
const handleWechatLogin = async () => {
  try {
    // #ifdef MP-WEIXIN
    const code = await getLoginCode();
    await userStore.loginWithWxCode(code);
    toast.success("登录成功");

    // 登录成功后跳转到mine页面，确保用户信息及时更新
    uni.switchTab({ url: "/pages/mine/index" });
    // #endif

    // #ifndef MP-WEIXIN
    toast.error("当前环境不支持微信登录");
    // #endif
  } catch (error: any) {
    handleLoginError(error, "微信授权");
  }
};

// 监听验证码状态变化
watch(
  () => captchaState.enable,
  (newVal) => {
    if (newVal && !captchaState.img_base) {
      getLoginCaptcha();
    }
  }
);

// 是否暗黑模式
const isDarkMode = computed(() => theme.value === "dark");

// 导航函数
const navigateToUserAgreement = () => {
  uni.navigateTo({ url: "/pages/mine/settings/agreement/index" });
};

const navigateToPrivacy = () => {
  uni.navigateTo({ url: "/pages/mine/settings/privacy/index" });
};

// 页面加载时获取验证码
onLoad(() => {
  uni.setNavigationBarTitle({ title: "用户登录" });
  getLoginCaptcha();
});
</script>

<style lang="scss" scoped>
.app-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  overflow: hidden;
  background-color: var(--wot-color-bg-container);
}

.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  width: 100%;
  height: 100%;
}

.loading-overlay {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
}

.loading-content {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  align-items: center;
}

.loading-text {
  font-size: 28rpx;
  color: #fff;
}
.header {
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 80rpx;
}

.logo {
  width: 140rpx;
  height: 140rpx;
  margin-bottom: 20rpx;
}

.title {
  margin-bottom: 10rpx;
  font-size: 48rpx;
  font-weight: bold;
  color: #ffffff;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
}

.subtitle {
  font-size: 28rpx;
  color: #ffffff;
  text-align: center;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
}

.login-card {
  z-index: 2;
  display: flex;
  flex-direction: column;
  width: 95%;
  margin-top: 80rpx;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 24rpx;
  box-shadow: 0 8rpx 40rpx rgba(0, 0, 0, 0.1);

  .wot-theme-dark & {
    background-color: rgba(31, 31, 31, 0.95);
    box-shadow: 0 8rpx 40rpx rgba(0, 0, 0, 0.5);
  }
}

.form-wrap {
  padding: 40rpx;
}

.form-item {
  position: relative;
  display: flex;
  align-items: center;
  padding: 24rpx 0;
  background-color: transparent;

  .wot-theme-dark & {
    background-color: transparent;
  }
}

.input-icon {
  margin-right: 20rpx;
}

/* 强制所有输入元素为透明背景 */
input,
.form-input,
.input-transparent {
  flex: 1;
  height: 60rpx;
  font-size: 28rpx;
  line-height: 60rpx;
  color: #333;
  background-color: transparent !important;
  -webkit-box-shadow: none !important;
  box-shadow: none !important;

  .wot-theme-dark & {
    color: #f5f5f5;
    background-color: transparent !important;
  }
}

/* 修复webkit浏览器自动填充问题 */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
  caret-color: var(--wot-color-text);
  background-color: transparent !important;
  -webkit-box-shadow: 0 0 0 1000px transparent inset !important;
  transition: background-color 5000s;
  -webkit-text-fill-color: var(--wot-color-text) !important;

  .wot-theme-dark & {
    -webkit-text-fill-color: #f5f5f5 !important;
    background-color: transparent !important;
    -webkit-box-shadow: 0 0 0 1000px rgba(31, 31, 31, 0) inset !important;
  }
}

/* 尝试通过更强的选择器覆盖自动填充 */
.form-item input,
input.form-input,
input.input-transparent {
  -webkit-appearance: none;
  appearance: none;
  background: none !important;
  background-color: transparent !important;
  border: none !important;
}

.clear-icon,
.eye-icon {
  padding: 10rpx;
}

.captcha-item {
  display: flex;
  gap: 20rpx;
  align-items: center;
}

.captcha-input {
  flex: 1;
  min-width: 0;
}

.captcha-image {
  flex-shrink: 0;
  width: 160rpx;
  height: 60rpx;
  cursor: pointer;
  border-radius: 8rpx;
}

.captcha-placeholder {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 160rpx;
  height: 60rpx;
  font-size: 24rpx;
  color: #666;
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8rpx;
}

.divider {
  height: 1px;
  margin: 0;
  background-color: rgba(0, 0, 0, 0.06);

  .wot-theme-dark & {
    background-color: rgba(255, 255, 255, 0.15);
  }
}

.login-btn {
  width: 100%;
  height: 88rpx;
  margin-top: 60rpx;
  font-size: 32rpx;
  font-weight: 500;
  line-height: 88rpx;
  color: #fff;
  text-align: center;
  background-color: var(--wot-color-theme);
  border: none;
  border-radius: 44rpx;
}

.switch-login-type {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 30rpx;
  font-size: 26rpx;
  color: var(--wot-color-theme);
}

.phone-login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx 0;
}

.phone-login-title {
  margin-bottom: 16rpx;
  font-size: 36rpx;
  font-weight: bold;
  color: #333;

  .wot-theme-dark & {
    color: #f5f5f5;
  }
}

.phone-login-subtitle {
  margin-bottom: 60rpx;
  font-size: 28rpx;
  color: #666;

  .wot-theme-dark & {
    color: #c0c0c0;
  }
}

.wechat-phone-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 88rpx;
  font-size: 32rpx;
  color: #ffffff;
  background-color: #07c160;
  border: none;
  border-radius: 44rpx;

  text {
    margin-left: 16rpx;
  }
}

.other-login {
  margin-top: 60rpx;
}

.other-login-title {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 40rpx;
}

.line {
  width: 80rpx;
  height: 1rpx;
  background-color: rgba(0, 0, 0, 0.1);

  .wot-theme-dark & {
    background-color: rgba(255, 255, 255, 0.2);
  }
}

.text {
  margin: 0 20rpx;
  font-size: 26rpx;
  color: rgba(0, 0, 0, 0.4);

  .wot-theme-dark & {
    color: rgba(255, 255, 255, 0.6);
  }
}

.wechat-login {
  display: flex;
  justify-content: center;
}

.wechat-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80rpx;
  height: 80rpx;
  background-color: #07c160;
  border-radius: 50%;

  .wot-theme-dark & {
    box-shadow: 0 4rpx 12rpx rgba(7, 193, 96, 0.3);
  }
}

.wechat-icon {
  width: 40rpx;
  height: 40rpx;
}

.agreement {
  display: flex;
  justify-content: center;
  margin-top: 60rpx;
  font-size: 24rpx;
}

.link {
  color: var(--wot-color-theme);
}

.input-placeholder {
  color: rgba(0, 0, 0, 0.3);

  .wot-theme-dark & {
    color: rgba(255, 255, 255, 0.4);
  }
}

/* 加强输入框透明度 - 暗黑模式特别处理 */
.wot-theme-dark {
  :deep(input) {
    background: none !important;
    background-color: transparent !important;
    -webkit-box-shadow: none !important;
    box-shadow: none !important;
  }

  .form-input,
  input {
    background: none !important;
    background-color: transparent !important;
    background-image: none !important;
  }
}

/* 修复Android Chrome输入框背景色问题 */
@supports (-webkit-appearance: none) {
  input {
    -webkit-appearance: none;
    appearance: none;
    background: transparent !important;
    background-color: transparent !important;
  }
}
</style>
