<template>
    <view class="login-container" :style="{ backgroundImage: BACKGROUND_IMAGE }">
        <!-- 登录表单 -->
        <up-image class="logo" :src="LOGO_PATH" shape="circle" width="100" height="100" mode="aspectFit" />
        <up-text class="logo-text" :bold="true" align="center" size="24" lineHeight="40" text="用户管理系统" />
        <up-form ref="loginForm" class="auth-form" :model="formData" :rules="rules">
            <!-- 用户名 -->
            <up-form-item prop="username">
                <up-input v-model="formData.username" placeholder="请输入账号" prefix-icon="account" clearable />
            </up-form-item>

            <!-- 密码 -->
            <up-form-item prop="password">
                <up-input v-model="formData.password" type="password" placeholder="请输入密码" prefix-icon="lock" clearable />
            </up-form-item>

            <!-- 验证码 -->
            <up-form-item prop="captcha">
                <up-input v-model="formData.captcha" placeholder="请输入验证码" prefix-icon="fingerprint" clearable >
                    <template #suffix>
                        <up-image :src="captchaState.img_base" @click="requestCaptcha" :preview="false" width="100" height="30" />
                    </template>
                </up-input>
            </up-form-item>

            <!-- 登录按钮 -->
            <up-button class="login-btn" type="primary" text="登录" :loading="loading" @click="handleSubmit" />
        </up-form>

        <!-- 底部链接 - 左右分开 -->
        <view class="footer-links">
            <up-text type="primary" @click="navigateTo('register')" text="用户注册" align="left"></up-text>
            <up-text type="primary" @click="navigateTo('forget')" text="忘记密码" align="right"></up-text>
        </view>
    </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { onReady, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '../../stores/index'
import { login, get_captcha } from '@/api/apis'

onReady(() => {
    requestCaptcha();
})

const LOGO_PATH = '/static/logo.png'
const BACKGROUND_IMAGE = '/static/background.png'
const loading = ref(false)
const loginForm = ref(null)

const formData = ref({
    username: '',
    password: '',
    captcha: '', 
    captcha_key: ''
})

const captchaState = ref({
    key: '',
    img_base: '' 
})

const rules = {
    username: { required: true, message: '请输入账号',trigger: ['change','blur'] },
    password: { required: true, message: '请输入密码',trigger: ['change','blur'] },
    captcha: { required: true, message: '请输入验证码',trigger: ['change','blur'] },
}

const handleSubmit = async () => {
    await loginForm.value.validate()
    loading.value = true

    formData.value.captcha_key = captchaState.value.key;
    login(formData.value).then(response => {
        const data  = response.data;
        useUserStore().setToken(data.access_token, data.refresh_token)
        console.log('登录成功', response)
        uni.switchTab({ url: '/pages/home/home' })
    }).catch(error => {
        console.error('登录失败', error)
        requestCaptcha();
    })
    .finally(() => loading.value = false);
}

const requestCaptcha = async () => {
    const response = await get_captcha()
    console.log('获取验证码', response);
    const data  = response.data;
    captchaState.value = data;
};
const navigateTo = (page) => {
    uni.showToast({
        title: page+'功能开发中',
        icon: "none",
        mask: true,
    });
}

</script>

<style scoped lang="scss">
.login-container {
    padding: 60rpx;
    display: flex;
    flex-direction: column;
    align-items: center;

    .auth-form {
        margin-top: 40rpx;
        width: 100%;

        .login-btn {
            margin-top: 40rpx;
        }

    }

    .footer-links {
        margin-top: 40rpx;
        display: flex;
        width: 100%;
    }
}
</style>