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
            v-model="passwordChangeForm.old_password"
            label="原密码"
            label-width="160rpx"
            show-password
            clearable
            placeholder="请输入原密码"
            prop="old_password"
            :rules="rules.oldPassword"
          />
          <wd-input
            v-model="passwordChangeForm.new_password"
            label="新密码"
            label-width="160rpx"
            show-password
            clearable
            placeholder="请输入新密码"
            prop="new_password"
            :rules="rules.newPassword"
          />
          <wd-input
            v-model="passwordChangeForm.confirm_password"
            label="确认密码"
            label-width="160rpx"
            show-password
            clearable
            placeholder="请确认新密码"
            prop="confirm_password"
            :rules="rules.confirmPassword"
          />
        </wd-cell-group>
        <view class="p-6">
          <wd-button type="primary" size="large" block @click="handleSubmit">提交</wd-button>
        </view>
      </wd-form>
    </wd-popup>
  </view>
</template>
<script setup lang="ts">
import UserAPI, { PasswordChangeForm, UserInfo } from "@/api/user";

const validatorConfirmPassword = (value: string) => {
  if (!value) {
    return Promise.reject("请确认密码");
  } else {
    if (value !== passwordChangeForm.new_password) {
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
}

const dialog = reactive({
  visible: false,
  type: "" as DialogType, // 修改账号资料,修改密码、绑定手机、绑定邮箱
});

const userProfile = ref<UserInfo>(); //用户信息
const passwordChangeForm = reactive<PasswordChangeForm>({
  old_password: "",
  new_password: "",
  confirm_password: "",
});
const passwordChangeFormRef = ref();

// 处理返回按钮点击
const handleBack = () => {
  uni.navigateBack();
};

/** 加载用户信息 */
const loadUserProfile = async () => {
  userProfile.value = await UserAPI.getCurrentUserInfo();
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
      passwordChangeForm.old_password = "";
      passwordChangeForm.new_password = "";
      passwordChangeForm.confirm_password = "";
      break;
  }
};

// 提交表单
function handleSubmit() {
  if (dialog.type === DialogType.PASSWORD) {
    passwordChangeFormRef.value.validate().then(({ valid }: { valid: boolean }) => {
      if (valid) {
        UserAPI.changeCurrentUserPassword(passwordChangeForm).then(() => {
          uni.showToast({ title: "密码修改成功", icon: "none" });
          dialog.visible = false;
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
