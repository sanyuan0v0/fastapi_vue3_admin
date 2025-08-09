<template>
  <view class="app-container">
    <wd-navbar title="个人信息" left-arrow @click-left="handleBack" />

    <wd-card v-if="userProfile" custom-style="margin-top: 20rpx">
      <wd-cell-group border>
        <wd-cell class="avatar-cell" title="头像" center is-link>
          <view class="avatar">
            <view v-if="!userProfile.avatar" class="img" @click="avatarUpload">
              <wd-icon name="fill-camera" custom-class="img-icon" />
            </view>
            <wd-img
              v-if="userProfile.avatar"
              round
              width="80px"
              height="80px"
              :src="userProfile.avatar"
              mode="aspectFit"
              custom-class="profile-img"
              @click="avatarUpload"
            />
          </view>
        </wd-cell>
        <wd-cell title="昵称" :value="userProfile.nickname" is-link @click="handleOpenDialog()" />
        <wd-cell
          title="性别"
          :value="userProfile.gender === 1 ? '男' : userProfile.gender === 2 ? '女' : '未知'"
          is-link
          @click="handleOpenDialog()"
        />
        <wd-cell title="用户名" :value="userProfile.username" />
        <wd-cell title="部门" :value="userProfile.deptName" />
        <wd-cell title="角色" :value="userProfile.roleNames" />
        <wd-cell title="创建日期" :value="userProfile.createTime" />
      </wd-cell-group>
    </wd-card>

    <!--头像裁剪-->
    <wd-img-cropper v-model="avatarShow" :img-src="originalSrc" @confirm="handleAvatarConfirm" />

    <!--用户信息编辑弹出框-->
    <wd-popup v-model="dialog.visible" position="bottom">
      <wd-form ref="userProfileFormRef" :model="userProfileForm" custom-class="edit-form">
        <wd-cell-group border>
          <wd-input
            v-model="userProfileForm.nickname"
            label="昵称"
            label-width="160rpx"
            placeholder="请输入昵称"
            prop="nickname"
            :rules="rules.nickname"
          />
          <wd-cell title="性别" title-width="160rpx" center prop="gender" :rules="rules.gender">
            <wd-radio-group v-model="userProfileForm.gender" shape="button" class="ef-radio-group">
              <wd-radio :value="1">男</wd-radio>
              <wd-radio :value="2">女</wd-radio>
            </wd-radio-group>
          </wd-cell>
        </wd-cell-group>
        <view class="p-6">
          <wd-button type="primary" size="large" block @click="handleSubmit">提交</wd-button>
        </view>
      </wd-form>
    </wd-popup>
  </view>
</template>
<script setup lang="ts">
import UserAPI, { type UserProfileVO, UserProfileForm } from "@/api/user";
import FileAPI, { type FileInfo } from "@/api/file";
import { checkLogin } from "@/utils/auth";

const originalSrc = ref<string>(""); //选取的原图路径
const avatarShow = ref<boolean>(false); //显示头像裁剪
const userProfile = ref<UserProfileVO>(); //用户信息

/** 加载用户信息 */
const loadUserProfile = async () => {
  userProfile.value = await UserAPI.getProfile();
};

// 头像选择
function avatarUpload() {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      originalSrc.value = res.tempFilePaths[0];
      avatarShow.value = true;
    },
  });
}
// 头像裁剪完成
function handleAvatarConfirm(event: any) {
  const { tempFilePath } = event;
  FileAPI.upload(tempFilePath).then((fileInfo: FileInfo) => {
    const avatarForm: UserProfileForm = {
      avatar: fileInfo.url,
    };
    // 头像路径保存至后端
    UserAPI.updateProfile(avatarForm).then(() => {
      uni.showToast({ title: "头像上传成功", icon: "none" });
      loadUserProfile();
    });
  });
}

// 本页面中所有的校验规则
const rules = reactive({
  nickname: [{ required: true, message: "请填写昵称" }],
  gender: [{ required: true, message: "请选择性别" }],
});

const dialog = reactive({
  visible: false,
});

const userProfileForm = reactive<UserProfileForm>({});
const userProfileFormRef = ref();

/**
 * 打开弹窗
 * @param type 弹窗类型 ACCOUNT: 账号资料 PASSWORD: 修改密码 MOBILE: 绑定手机 EMAIL: 绑定邮箱
 */
const handleOpenDialog = () => {
  dialog.visible = true;
  // 初始化表单数据
  userProfileForm.nickname = userProfile.value?.nickname;
  userProfileForm.gender = userProfile.value?.gender;
};

// 提交表单
function handleSubmit() {
  userProfileFormRef.value.validate().then(({ valid }: { valid: boolean }) => {
    if (valid) {
      UserAPI.updateProfile(userProfileForm).then(() => {
        uni.showToast({ title: "账号资料修改成功", icon: "none" });
        dialog.visible = false;
        loadUserProfile();
      });
    }
  });
}

// 检查登录状态
onLoad(() => {
  if (!checkLogin()) return;

  // #ifdef H5
  document.addEventListener("touchstart", touchstartListener, { passive: false });
  document.addEventListener("touchmove", touchmoveListener, { passive: false });
  // #endif
  loadUserProfile();
});

onMounted(() => {
  // 在onMounted中不再重复检查登录状态和加载用户信息
  // 如果需要检查登录状态和加载用户信息，请使用onLoad中的逻辑
});

// 页面销毁前移除事件监听
onBeforeUnmount(() => {
  // #ifdef H5
  document.removeEventListener("touchstart", touchstartListener);
  document.removeEventListener("touchmove", touchmoveListener);
  // #endif
});
// 禁用浏览器双指缩放，使头像裁剪时双指缩放能够起作用
function touchstartListener(event: TouchEvent) {
  if (event.touches.length > 1) {
    event.preventDefault();
  }
}
// 禁用浏览器下拉刷新，使头像裁剪时能够移动图片
function touchmoveListener(event: TouchEvent) {
  event.preventDefault();
}

function handleBack() {
  uni.navigateBack();
}
</script>
<style lang="scss" scoped>
.avatar-cell {
  :deep(.wd-cell__body) {
    align-items: center;
  }
  .avatar {
    display: flex;
    align-items: center;
    justify-content: right;
    .img {
      position: relative;
      width: 80px;
      height: 80px;
      background-color: rgba(0, 0, 0, 0.04);
      border-radius: 50%;
      .img-icon {
        position: absolute;
        top: 50%;
        left: 50%;
        color: #fff;
      }
    }
  }
}

.edit-form {
  padding-top: 40rpx;
  .ef-radio-group {
    line-height: 1;
    text-align: left;
  }
}
</style>
