<template>
  <view class="app-container">
    <wd-navbar title="账号和安全" left-arrow @click-left="handleBack" />

    <wd-card custom-style="margin-top: 20rpx">
      <wd-cell-group border>
        <wd-cell
          title="账户密码"
          label="定期修改密码有助于保护账户安全"
          value="修改"
          is-link
          @click="handleOpenDialog(DialogType.PASSWORD)"
        />
        <wd-cell
          title="绑定手机"
          :value="userProfile?.mobile"
          is-link
          @click="handleOpenDialog(DialogType.MOBILE)"
        />
        <wd-cell
          title="绑定邮箱"
          :value="userProfile?.email ? userProfile.email : '未绑定邮箱'"
          is-link
          @click="handleOpenDialog(DialogType.EMAIL)"
        />
      </wd-cell-group>
    </wd-card>

    <!--用户信息编辑弹出框-->
    <wd-popup v-model="dialog.visible" position="bottom">
      <wd-form
        v-if="dialog.type === DialogType.PASSWORD"
        ref="passwordChangeFormRef"
        :model="passwordChangeForm"
        custom-class="edit-form"
      >
        <wd-cell-group border>
          <wd-input
            v-model="passwordChangeForm.oldPassword"
            label="原密码"
            label-width="160rpx"
            show-password
            clearable
            placeholder="请输入原密码"
            prop="oldPassword"
            :rules="rules.oldPassword"
          />
          <wd-input
            v-model="passwordChangeForm.newPassword"
            label="新密码"
            label-width="160rpx"
            show-password
            clearable
            placeholder="请输入新密码"
            prop="newPassword"
            :rules="rules.newPassword"
          />
          <wd-input
            v-model="passwordChangeForm.confirmPassword"
            label="确认密码"
            label-width="160rpx"
            show-password
            clearable
            placeholder="请确认新密码"
            prop="confirmPassword"
            :rules="rules.confirmPassword"
          />
        </wd-cell-group>
        <view class="p-6">
          <wd-button type="primary" size="large" block @click="handleSubmit">提交</wd-button>
        </view>
      </wd-form>
      <wd-form
        v-if="dialog.type === DialogType.MOBILE"
        ref="mobileBindingFormRef"
        :model="mobileBindingForm"
        custom-class="edit-form"
      >
        <wd-cell-group border>
          <wd-input
            v-model="mobileBindingForm.mobile"
            label="手机号码"
            label-width="160rpx"
            clearable
            placeholder="请输入手机号码"
            prop="mobile"
            :rules="rules.mobile"
          />
          <wd-input
            v-model="mobileBindingForm.code"
            label="验证码"
            label-width="160rpx"
            clearable
            placeholder="请输入验证码"
            prop="code"
            :rules="rules.code"
          >
            <template #suffix>
              <wd-button
                plain
                :disabled="mobileCountdown > 0"
                @click="handleSendVerificationCode('MOBILE')"
              >
                {{ mobileCountdown > 0 ? `${mobileCountdown}s后重新发送` : "发送验证码" }}
              </wd-button>
            </template>
          </wd-input>
        </wd-cell-group>
        <view class="p-6">
          <wd-button type="primary" size="large" block @click="handleSubmit">提交</wd-button>
        </view>
      </wd-form>
      <wd-form
        v-if="dialog.type === DialogType.EMAIL"
        ref="emailBindingFormRef"
        :model="emailBindingForm"
        custom-class="edit-form"
      >
        <wd-cell-group border>
          <wd-input
            v-model="emailBindingForm.email"
            label="邮箱"
            label-width="160rpx"
            clearable
            placeholder="请输入邮箱"
            prop="email"
            :rules="rules.email"
          />
          <wd-input
            v-model="emailBindingForm.code"
            label="验证码"
            label-width="160rpx"
            clearable
            placeholder="请输入验证码"
            prop="code"
            :rules="rules.code"
          >
            <template #suffix>
              <wd-button
                plain
                :disabled="emailCountdown > 0"
                @click="handleSendVerificationCode('EMAIL')"
              >
                {{ emailCountdown > 0 ? `${emailCountdown}s后重新发送` : "发送验证码" }}
              </wd-button>
            </template>
          </wd-input>
        </wd-cell-group>
        <view class="p-6">
          <wd-button type="primary" size="large" block @click="handleSubmit">提交</wd-button>
        </view>
      </wd-form>
    </wd-popup>
  </view>
</template>
<script setup lang="ts">
import UserAPI, {
  PasswordChangeForm,
  MobileBindingForm,
  EmailBindingForm,
  UserProfileVO,
} from "@/api/user";

const validatorConfirmPassword = (value: string) => {
  if (!value) {
    return Promise.reject("请确认密码");
  } else {
    if (value !== passwordChangeForm.newPassword) {
      return Promise.reject("两次输入的密码不一致");
    } else {
      return Promise.resolve();
    }
  }
};
// 本页面中所有的校验规则
const rules = reactive({
  oldPassword: [{ required: true, message: "请填写原密码" }],
  newPassword: [{ required: true, message: "请填写新密码" }],
  confirmPassword: [{ required: true, message: "请确认密码", validator: validatorConfirmPassword }],
  mobile: [{ required: true, pattern: /^1[3-9]\d{9}$/, message: "请填写正确的手机号码" }],
  code: [{ required: true, message: "请填写验证码" }],
  email: [
    {
      required: true,
      pattern: /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/,
      message: "请填写正确的邮箱地址",
    },
  ],
});

enum DialogType {
  PASSWORD = "password",
  MOBILE = "mobile",
  EMAIL = "email",
}

const dialog = reactive({
  visible: false,
  type: "" as DialogType, // 修改账号资料,修改密码、绑定手机、绑定邮箱
});

const userProfile = ref<UserProfileVO>(); //用户信息
const passwordChangeForm = reactive<PasswordChangeForm>({});
const mobileBindingForm = reactive<MobileBindingForm>({});
const emailBindingForm = reactive<EmailBindingForm>({});
const passwordChangeFormRef = ref();
const mobileBindingFormRef = ref();
const emailBindingFormRef = ref();

const mobileCountdown = ref(0);
const mobileTimer = ref<ReturnType<typeof setInterval> | null>(null);

const emailCountdown = ref(0);
const emailTimer = ref<ReturnType<typeof setTimeout> | null>(null);

// 处理返回按钮点击
const handleBack = () => {
  uni.navigateBack();
};

/** 加载用户信息 */
const loadUserProfile = async () => {
  userProfile.value = await UserAPI.getProfile();
};

/**
 * 打开弹窗
 * @param type 弹窗类型 ACCOUNT: 账号资料 PASSWORD: 修改密码 MOBILE: 绑定手机 EMAIL: 绑定邮箱
 */
const handleOpenDialog = (type: DialogType) => {
  dialog.type = type;
  dialog.visible = true;
  switch (type) {
    case DialogType.PASSWORD:
      passwordChangeForm.oldPassword = "";
      passwordChangeForm.newPassword = "";
      passwordChangeForm.confirmPassword = "";
      break;
    case DialogType.MOBILE:
      mobileBindingForm.mobile = "";
      mobileBindingForm.code = "";
      break;
    case DialogType.EMAIL:
      emailBindingForm.email = "";
      emailBindingForm.code = "";
      break;
  }
};

/**
 *  发送验证码
 *
 * @param contactType 联系方式类型 MOBILE: 手机号码  EMAIL: 邮箱
 */
const handleSendVerificationCode = async (contactType: string) => {
  if (contactType === "MOBILE") {
    mobileBindingFormRef.value.validate("mobile").then(({ valid }: { valid: boolean }) => {
      if (valid) {
        UserAPI.sendVerificationCode(mobileBindingForm.mobile!, "MOBILE").then(() => {
          uni.showToast({ title: "验证码已发送", icon: "none" });
          mobileCountdown.value = 60;
          mobileTimer.value = setInterval(() => {
            if (mobileCountdown.value > 0) {
              mobileCountdown.value -= 1;
            } else {
              clearInterval(mobileTimer.value!);
            }
          }, 1000);
        });
      }
    });
  } else if (contactType === "EMAIL") {
    emailBindingFormRef.value.validate("email").then(({ valid }: { valid: boolean }) => {
      if (valid) {
        UserAPI.sendVerificationCode(emailBindingForm.email!, "EMAIL").then(() => {
          uni.showToast({ title: "验证码已发送", icon: "none" });
          emailCountdown.value = 60;
          emailTimer.value = setInterval(() => {
            if (emailCountdown.value > 0) {
              emailCountdown.value -= 1;
            } else {
              clearInterval(emailTimer.value!);
            }
          }, 1000);
        });
      }
    });
  }
};

// 提交表单
function handleSubmit() {
  if (dialog.type === DialogType.PASSWORD) {
    passwordChangeFormRef.value.validate().then(({ valid }: { valid: boolean }) => {
      if (valid) {
        UserAPI.changePassword(passwordChangeForm).then(() => {
          uni.showToast({ title: "密码修改成功", icon: "none" });
          dialog.visible = false;
        });
      }
    });
  } else if (dialog.type === DialogType.MOBILE) {
    mobileBindingFormRef.value.validate().then(({ valid }: { valid: boolean }) => {
      if (valid) {
        UserAPI.bindMobile(mobileBindingForm).then(() => {
          uni.showToast({ title: "手机号绑定成功", icon: "none" });
          dialog.visible = false;
          loadUserProfile();
        });
      }
    });
  } else if (dialog.type === DialogType.EMAIL) {
    emailBindingFormRef.value.validate().then(({ valid }: { valid: boolean }) => {
      if (valid) {
        UserAPI.bindEmail(emailBindingForm).then(() => {
          uni.showToast({ title: "邮箱绑定成功", icon: "none" });
          dialog.visible = false;
          loadUserProfile();
        });
      }
    });
  }
}

onMounted(() => {
  loadUserProfile();
});
</script>
<style lang="scss" scoped></style>
