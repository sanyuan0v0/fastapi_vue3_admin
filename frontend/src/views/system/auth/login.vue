<template>
  <a-layout>
    <!-- 页面主体 -->
    <div class="container" :style="{ backgroundImage: `url(${initConfigState.background})` }">
      <a-layout-content :style="contentStyle">
        <div class="header">
          <div class="logo">
            <a-image :src="initConfigState.logo" :preview="false" />
          </div>
          <div class="title">{{ initConfigState.title }}</div>
        </div>
        <div class="desc">{{ initConfigState.description }}</div>

        <div class="login-main" style="width: 330px; margin: 0 auto;">
          <a-tabs centered>
            <a-tab-pane :key="1" tab="账户密码登录">
              <a-form :model="loginForm" @finish="onFinish">
                <a-form-item name="username" :rules="[{ required: true, message: '用户名是必填项！' }]">
                  <a-input v-model:value="loginForm.username" placeholder="用户名: admin or demo" allow-clear>
                    <template #prefix>
                      <UserOutlined />
                    </template>
                  </a-input>
                </a-form-item>

                <a-form-item name="password" :rules="[{ required: true, message: '密码是必填项！' }]">
                  <a-input-password v-model:value="loginForm.password" placeholder="密码: gitee 或 github 查看" allow-clear>
                    <template #prefix>
                      <LockOutlined />
                    </template>
                  </a-input-password>
                </a-form-item>

                <a-form-item v-if="captchaState.enable" name="captcha" :rules="[{ required: true, message: '验证码是必填项！' }]">
                  <a-input v-model:value="loginForm.captcha" placeholder="验证码" allow-clear>
                    <template #addonAfter>
                      <div class="login-form-captcha" @click="requestCaptcha">
                        <a-image :src="captchaState.img_base" :preview="false" />
                      </div>
                    </template>
                  </a-input>
                </a-form-item>

                <a-form-item>
                  <a-checkbox v-model:checked="loginForm.remember">自动登录</a-checkbox>
                  <a class="login-form-forgot" @click="showModal('forgetPassword')">忘记密码</a>
                </a-form-item>

                <a-form-item>
                  <a-button type="primary" html-type="submit" class="login-form-button" :loading="loginFlag">
                    登录
                  </a-button>
                  <div class="register-link">
                    还没有账号? <a @click="showModal('register')">立即注册</a>
                  </div>
                </a-form-item>
              </a-form>
            </a-tab-pane>
          </a-tabs>
        </div>
      </a-layout-content>

      <!-- 页面底部 -->
      <a-layout-footer :style="footerStyle">
        <div class="footer-content">
          <div class="footer-links">
            <a-button type="link" :href="initConfigState.code_url">
              <icon-font type="icon-copyright" :style="{ fontSize: '16px' }" />
              {{ initConfigState.copyright }} |
            </a-button>
            <a-button type="link" :href="initConfigState.help_url">
              帮助 |
            </a-button>
            <a-button type="link" :href="initConfigState.privacy_url">
              隐私 |
            </a-button>
            <a-button type="link" :href="initConfigState.clause_url">
              条款
            </a-button>
          </div>
          <div class="footer-record">
            {{ initConfigState.keep_record }}
          </div>
        </div>
      </a-layout-footer>
    
    </div>

    <!-- 弹窗区域 -->
    <div class="modal-wrapper">
      <a-modal 
        v-model:open="modalVisible" 
        :title="modalType === 'forgetPassword' ? '忘记密码' : '用户注册'" 
        @ok="onSubmit" 
        :confirmLoading="modalLoading">

        <!-- 忘记密码表单 -->
        <a-form v-if="modalType === 'forgetPassword'" 
          :model="forgetPasswordForm" 
          ref="forgetPasswordFormRef" 
          :rules="{
          username: [{ required: true, message: '请输入用户名!' }],
          mobile: [{ required: true, message: '请输入手机号!', pattern: /^1[3-9]\d{9}$/ }],
          new_password: [{ required: true, message: '请输入新密码!', min: 6 }]
        }">
          <a-form-item label="用户名" name="username">
            <a-input v-model:value="forgetPasswordForm.username" placeholder="请输入用户名" allow-clear/>
          </a-form-item>
          <a-form-item label="手机号" name="mobile">
            <a-input v-model:value="forgetPasswordForm.mobile" placeholder="请输入手机号" allow-clear/>
          </a-form-item>
          <a-form-item label="新密码" name="new_password">
            <a-input-password v-model:value="forgetPasswordForm.new_password" placeholder="请输入新密码" allow-clear/>
          </a-form-item>
        </a-form>

        <!-- 注册表单 -->
        <a-form v-else
          :model="registerForm" 
          ref="registerFormRef" 
          :rules="{
          name: [{ required: true, message: '请输入用户名!', min: 2 }],
          username: [{ required: true, message: '请输入用户名!', min: 4 }],
          password: [{ required: true, message: '请输入密码!', min: 6 }],
          mobile: [{ required: true, pattern: /^1[3-9]\d{9}$/, message: '请输入手机号!' }],
        }">
          <a-form-item label="姓名" name="name">
            <a-input v-model:value="registerForm.name" placeholder="请输入用户名" allow-clear/>
          </a-form-item>
          <a-form-item label="账号" name="username">
            <a-input v-model:value="registerForm.username" placeholder="请输入用户名" allow-clear/>
          </a-form-item>
          <a-form-item label="手机号" name="mobile">
            <a-input v-model:value="registerForm.mobile" placeholder="请输入手机号" allow-clear/>
          </a-form-item>
          <a-form-item label="密码" name="password">
            <a-input-password v-model:value="registerForm.password" placeholder="请输入密码" allow-clear/>
          </a-form-item>
          <a-form-item label="备注" name="description">
            <a-textarea v-model:value="registerForm.description" placeholder="请输入备注信息" :rows="4" :maxlength="250" showCount allow-clear/>
          </a-form-item>
        </a-form>
      </a-modal>
    </div>
  </a-layout>
</template>

<script lang="ts" setup>
import type { CSSProperties } from "vue";
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { UserOutlined, LockOutlined, createFromIconfontCN } from '@ant-design/icons-vue';
import { save_token } from "@/utils/util"
import { message, Form } from 'ant-design-vue';
import { login, getCaptcha } from "@/api/system/auth"
import { registerUser, forgetPassword } from "@/api/system/user"
import type { LoginForm, CaptchaState, ForgetPasswordForm, RegisterForm } from './types'
import { useConfigStore } from "@/store/index";

const useForm = Form.useForm;

const router = useRouter();
const loginFlag = ref(false);
const IconFont = createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_8d5l8fzk5b87iudi.js',
});

const contentStyle: CSSProperties = {
  minHeight: 900,
  height: "900px",
  background: "none",
  padding: "200px 0",
};

const footerStyle: CSSProperties = {
  textAlign: "center",
  background: "none",
  flex: "0 0 60px",
};

// 统一的弹窗控制
const modalVisible = ref(false);
const modalLoading = ref(false);
const modalType = ref<'forgetPassword' | 'register'>('forgetPassword');

// 忘记密码相关
const forgetPasswordFormRef = ref();
const forgetPasswordForm = reactive<ForgetPasswordForm>({
  username: '',
  mobile: '',
  new_password: ''
});

// 注册相关
const registerFormRef = ref();
const registerForm = reactive<RegisterForm>({
  username: '',
  name: '',
  password: '',
  mobile: '',
  // email: '',
  // gender: 1
  description: ''
});

const loginForm = reactive<LoginForm>({
  username: "",
  password: "",
  captcha: "",
  captcha_key: "",
  remember: true
});

const captchaState = reactive<CaptchaState>({
  enable: true,
  key: "",
  img_base: ""
});

const showModal = (type: 'forgetPassword' | 'register') => {
  modalType.value = type;
  modalVisible.value = true;
};

const onSubmit = async () => {
  modalLoading.value = true;
  try {
    if (modalType.value === 'forgetPassword') {
      // 验证忘记密码表单
      if (!forgetPasswordFormRef.value) {
        message.error('表单引用未正确初始化');
        return;
      }
      await forgetPasswordFormRef.value.validate();
      await forgetPassword({ ...forgetPasswordForm });
      Object.keys(forgetPasswordForm).forEach(key => delete forgetPasswordForm[key]);
      modalVisible.value = false;
    } else {
      
      // 验证注册表单
      if (!registerFormRef.value) {
        message.error('表单引用未正确初始化');
        return;
      }
      await registerFormRef.value.validate();
      await registerUser({ ...registerForm });
      Object.keys(registerForm).forEach(key => delete registerForm[key]);
      modalVisible.value = false;
    }
  } catch (error) {
    console.error('操作出错:', error);
  } finally {
    // 无论成功或失败，都关闭加载状态
    modalLoading.value = false;
  }
};

const onFinish = (values: LoginForm) => {
  loginFlag.value = true;
  values.captcha_key = captchaState.key;
  
  login(values)
    .then(response => {
      const { status_code, data } = response.data;
      if (status_code === 200) {
        save_token(data.access_token, data.refresh_token, data.expires_in);
        router.push('/');
      }
    })
    .catch(error => {
      if (error.response?.data?.status_code === 500) {
        requestCaptcha();
      }
    })
    .finally(() => loginFlag.value = false);
};

const requestCaptcha = async () => {
  const response = await getCaptcha();
  const { data } = response.data;
  captchaState.enable = data.enable;
  captchaState.key = data.key;
  captchaState.img_base = data.img_base;
};

const configStore = useConfigStore();

const initConfigState = reactive({
  title:  configStore.getConfigValue("sys_web_title"),
  description:  configStore.getConfigValue("sys_web_description"),
  logo:  configStore.getConfigValue("sys_web_logo"),
  background:  configStore.getConfigValue("sys_login_background"),
  copyright:  configStore.getConfigValue("sys_web_copyright"),
  keep_record:  configStore.getConfigValue("sys_keep_record"),
  help_url:  configStore.getConfigValue("sys_help_doc"),
  privacy_url:  configStore.getConfigValue("sys_web_privacy"),
  clause_url:  configStore.getConfigValue("sys_web_clause"),
  code_url:  configStore.getConfigValue("sys_git_code"),
});


onMounted(() => {
  requestCaptcha();
});
</script>

<style lang="scss" scoped>
.ant-btn-link {
  margin-inline-end: 8px;
  padding: 0;
}

.container {
  height: 100vh;
  background-size: cover;
  background-position: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 0; // 允许容器高度收缩
  overflow-y: auto; // 当内容超出时显示垂直滚动条

  .desc {
    text-align: center;
    font-size: 15px;
    margin: 12px 0 40px;
  }

  .header {
    display: flex;
    line-height: 44px;
    justify-content: center;
    align-items: center;

    .logo {
      width: 44px;
      height: 44px;
      margin-inline-end: 16px;
    }

    .title {
      font-size: 33px;
      font-weight: 650;
    }
  }
}

.login-form {
  &-button {
    width: 100%;
  }

  &-captcha {
    width: 80px;
    cursor: pointer;
  }

  &-forgot {
    float: right;
    color: #1890ff;
    cursor: pointer;
  }
}

.register-link {
  text-align: center;
  margin-top: 16px;
  
  a {
    color: #1890ff;
    cursor: pointer;
  }
}

:deep(.ant-input-group .ant-input-group-addon) {
  padding: 0;
}
</style>