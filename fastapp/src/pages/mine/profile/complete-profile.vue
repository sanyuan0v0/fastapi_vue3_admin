<template>
  <view class="app-container">
    <wd-navbar title="完善个人信息" left-arrow @click-left="handleBack" />

    <!-- 头部标题 -->
    <view class="header">
      <view class="title">完善个人信息</view>
      <view class="subtitle">为了给您提供更好的服务，请完善以下信息</view>
    </view>

    <!-- 表单区域 -->
    <view class="form-container">
      <wd-form ref="profileFormRef" :model="profileForm">
        <!-- 微信小程序专用头像昵称组件 -->
        <!-- #ifdef MP-WEIXIN -->
        <view class="form-section">
          <view class="section-title">基本信息</view>

          <!-- 内联WechatProfile组件的内容 -->
          <view class="wechat-profile">
            <!-- 头像选择 -->
            <view class="avatar-section">
              <view class="section-title">头像</view>
              <button class="avatar-button" open-type="chooseAvatar" @chooseavatar="onChooseAvatar">
                <image
                  v-if="profileForm.avatar"
                  :src="profileForm.avatar"
                  class="avatar-image"
                  mode="aspectFill"
                />
                <view v-else class="avatar-placeholder">
                  <wd-icon name="camera" size="40" color="#999" />
                  <text class="placeholder-text">选择头像</text>
                </view>
              </button>
            </view>

            <!-- 昵称输入 -->
            <view class="nickname-section">
              <view class="section-title">昵称</view>
              <input
                v-model="profileForm.nickname"
                type="nickname"
                class="nickname-input"
                placeholder="请输入昵称"
                :maxlength="20"
              />
            </view>

            <!-- 性别选择 -->
            <view class="gender-section">
              <view class="section-title">性别</view>
              <wd-radio-group v-model="profileForm.gender" shape="button" class="gender-group">
                <wd-radio :value="1" class="gender-radio">男</wd-radio>
                <wd-radio :value="2" class="gender-radio">女</wd-radio>
              </wd-radio-group>
            </view>
          </view>
        </view>
        <!-- #endif -->

        <!-- 其他平台的头像上传 -->
        <!-- #ifndef MP-WEIXIN -->
        <!-- 头像上传 -->
        <view class="form-section">
          <view class="section-title">头像</view>
          <view class="avatar-upload" @click="chooseAvatar">
            <view v-if="!profileForm.avatar" class="avatar-placeholder">
              <wd-icon name="camera" size="40" color="#999" />
              <text class="placeholder-text">点击上传头像</text>
            </view>
            <image v-else :src="profileForm.avatar" class="avatar-preview" mode="aspectFill" />
          </view>
        </view>

        <!-- 昵称输入 -->
        <view class="form-section">
          <view class="section-title">
            昵称
            <text class="required">*</text>
          </view>
          <wd-input
            v-model="profileForm.nickname"
            placeholder="请输入昵称"
            prop="nickname"
            :rules="rules.nickname"
            custom-class="nickname-input"
          />
        </view>

        <!-- 性别选择 -->
        <view class="form-section">
          <view class="section-title">性别</view>
          <wd-radio-group v-model="profileForm.gender" shape="button" class="gender-group">
            <wd-radio :value="1" class="gender-radio">男</wd-radio>
            <wd-radio :value="2" class="gender-radio">女</wd-radio>
          </wd-radio-group>
        </view>
        <!-- #endif -->

        <!-- 手机号授权 -->
        <view class="form-section">
          <view class="section-title">
            手机号
            <text class="required">*</text>
          </view>
          <view v-if="!profileForm.mobile" class="phone-auth">
            <button
              class="phone-auth-btn"
              open-type="getPhoneNumber"
              :disabled="phoneAuthLoading"
              @getphonenumber="onGetPhoneNumber"
            >
              <wd-icon name="phone" size="20" color="#165DFF" />
              <text class="auth-text">{{ phoneAuthLoading ? "授权中..." : "授权获取手机号" }}</text>
            </button>
          </view>
          <view v-else class="phone-display">
            <wd-icon name="phone" size="20" color="#52c41a" />
            <text class="phone-number">{{ formatPhoneNumber(profileForm.mobile) }}</text>
            <text class="change-phone" @click="changePhone">更换</text>
          </view>
        </view>
      </wd-form>
    </view>

    <!-- 底部按钮 -->
    <view class="footer">
      <wd-button
        class="complete-btn"
        type="primary"
        size="large"
        block
        :disabled="!canComplete || loading"
        :loading="loading"
        @click="handleComplete"
      >
        完成
      </wd-button>
      <view class="skip-btn" @click="handleSkip">
        <text>暂时跳过</text>
      </view>
    </view>

    <!-- 头像裁剪 -->
    <wd-img-cropper
      v-model="cropperVisible"
      :img-src="originalImageSrc"
      @confirm="handleAvatarConfirm"
    />

    <wd-toast />
  </view>
</template>

<script lang="ts" setup>
import { ref, reactive, computed } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { useToast } from "wot-design-uni";
import { useUserStore } from "@/store/modules/user.store";
import UserAPI, { type UserProfileForm } from "@/api/user";
import FileAPI, { type FileInfo } from "@/api/file";

const toast = useToast();
const userStore = useUserStore();

// 页面参数
const redirect = ref("/pages/index/index");

// 表单数据
const profileForm = reactive<UserProfileForm & { mobile?: string }>({
  nickname: "",
  avatar: "",
  gender: 1,
  mobile: "",
});

// 表单验证规则
const rules = {
  nickname: [
    { required: true, message: "请输入昵称" },
    { required: true, min: 2, max: 20, message: "昵称长度为2-20个字符" },
  ],
};

// 状态管理
const loading = ref(false);
const phoneAuthLoading = ref(false);
const cropperVisible = ref(false);
const originalImageSrc = ref("");
const profileFormRef = ref();

// 计算属性
const canComplete = computed(() => {
  return profileForm.nickname && profileForm.mobile;
});

// 页面加载
onLoad((options: any) => {
  if (options?.redirect) {
    redirect.value = decodeURIComponent(options.redirect);
  }

  // 如果用户已有部分信息，预填充
  const userInfo = userStore.userInfo;
  if (userInfo) {
    profileForm.nickname = userInfo.nickname || "";
    profileForm.avatar = userInfo.avatar || "";
    // 注意：UserInfo接口可能没有gender字段，这里需要安全访问
    profileForm.gender = (userInfo as any).gender || 1;
  }
});

// 微信小程序头像选择处理
const onChooseAvatar = async (e: any) => {
  try {
    const { avatarUrl } = e.detail;

    // 上传头像到服务器
    uni.showLoading({ title: "上传中..." });

    const fileInfo: FileInfo = await FileAPI.upload(avatarUrl);
    profileForm.avatar = fileInfo.url;

    uni.hideLoading();
    uni.showToast({ title: "头像上传成功", icon: "success" });
  } catch (error) {
    uni.hideLoading();
    console.error("头像上传失败:", error);
    uni.showToast({ title: "头像上传失败", icon: "error" });
  }
};

// 选择头像
const chooseAvatar = () => {
  // #ifdef MP-WEIXIN
  // 微信小程序使用头像昵称填写能力
  uni.chooseMedia({
    count: 1,
    mediaType: ["image"],
    sourceType: ["album", "camera"],
    success: (res) => {
      originalImageSrc.value = res.tempFiles[0].tempFilePath;
      cropperVisible.value = true;
    },
    fail: (err) => {
      console.error("选择图片失败:", err);
      toast.error("选择图片失败");
    },
  });
  // #endif

  // #ifndef MP-WEIXIN
  uni.chooseImage({
    count: 1,
    sourceType: ["album", "camera"],
    success: (res) => {
      originalImageSrc.value = res.tempFilePaths[0];
      cropperVisible.value = true;
    },
    fail: (err) => {
      console.error("选择图片失败:", err);
      toast.error("选择图片失败");
    },
  });
  // #endif
};

// 头像裁剪确认
const handleAvatarConfirm = async (event: any) => {
  try {
    const { tempFilePath } = event;
    toast.loading("上传中...");

    const fileInfo: FileInfo = await FileAPI.upload(tempFilePath);
    profileForm.avatar = fileInfo.url;

    toast.success("头像上传成功");
  } catch (error) {
    console.error("头像上传失败:", error);
    toast.error("头像上传失败");
  }
};

// 获取手机号授权
const onGetPhoneNumber = async (e: any) => {
  console.log("手机号授权回调:", e);

  if (e.detail.errMsg === "getPhoneNumber:ok") {
    phoneAuthLoading.value = true;

    try {
      // 调用后端接口解析手机号
      const phoneData = await UserAPI.getPhoneNumber({
        code: e.detail.code,
        encryptedData: e.detail.encryptedData,
        iv: e.detail.iv,
      });

      profileForm.mobile = phoneData.phoneNumber;
      toast.success("手机号授权成功");
    } catch (error: any) {
      console.error("手机号授权失败:", error);
      toast.error(error?.message || "手机号授权失败");
    } finally {
      phoneAuthLoading.value = false;
    }
  } else {
    toast.error("手机号授权失败");
  }
};

// 更换手机号
const changePhone = () => {
  profileForm.mobile = "";
};

// 格式化手机号显示
const formatPhoneNumber = (phone: string) => {
  if (!phone) return "";
  return phone.replace(/(\d{3})\d{4}(\d{4})/, "$1****$2");
};

// 完成信息填写
const handleComplete = async () => {
  try {
    // 表单验证
    const { valid } = await profileFormRef.value.validate();
    if (!valid) return;

    if (!profileForm.mobile) {
      toast.error("请先授权获取手机号");
      return;
    }

    loading.value = true;

    // 更新用户信息
    await UserAPI.updateProfile({
      nickname: profileForm.nickname,
      avatar: profileForm.avatar,
      gender: profileForm.gender,
    });

    // 如果有手机号，绑定手机号
    if (profileForm.mobile) {
      await UserAPI.bindMobile({
        mobile: profileForm.mobile,
      });
    }

    // 重新获取用户信息
    await userStore.getInfo();

    toast.success("信息完善成功");

    // 跳转到目标页面
    setTimeout(() => {
      uni.reLaunch({
        url: redirect.value,
      });
    }, 1000);
  } catch (error: any) {
    console.error("完善信息失败:", error);
    toast.error(error?.message || "完善信息失败");
  } finally {
    loading.value = false;
  }
};

// 跳过完善信息
const handleSkip = () => {
  uni.showModal({
    title: "提示",
    content: "跳过信息完善可能会影响部分功能使用，确定要跳过吗？",
    success: (res) => {
      if (res.confirm) {
        uni.reLaunch({
          url: redirect.value,
        });
      }
    },
  });
};

// 返回
function handleBack() {
  uni.navigateBack();
}
</script>

<style lang="scss" scoped>
.header {
  margin-bottom: 60rpx;
  text-align: center;

  .title {
    margin-bottom: 20rpx;
    font-size: 48rpx;
    font-weight: bold;
    color: #fff;
  }

  .subtitle {
    font-size: 28rpx;
    line-height: 1.5;
    color: rgba(255, 255, 255, 0.8);
  }
}

.form-container {
  padding: 40rpx;
  margin-bottom: 40rpx;
  background: #fff;
  border-radius: 24rpx;
  box-shadow: 0 8rpx 40rpx rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 40rpx;

  &:last-child {
    margin-bottom: 0;
  }
}

.section-title {
  margin-bottom: 20rpx;
  font-size: 32rpx;
  font-weight: 600;
  color: #333;

  .required {
    color: #ff4757;
  }
}

.avatar-upload {
  display: flex;
  justify-content: center;

  .avatar-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 160rpx;
    height: 160rpx;
    background: #f8f9fa;
    border: 2rpx dashed #ddd;
    border-radius: 50%;

    .placeholder-text {
      margin-top: 10rpx;
      font-size: 24rpx;
      color: #999;
    }
  }

  .avatar-preview {
    width: 160rpx;
    height: 160rpx;
    border: 4rpx solid #f0f0f0;
    border-radius: 50%;
  }
}

.nickname-input {
  :deep(.wd-input__inner) {
    padding: 24rpx 20rpx;
    background: #f8f9fa;
    border: 1rpx solid #e9ecef;
    border-radius: 12rpx;
  }
}

.gender-group {
  display: flex;
  gap: 20rpx;

  .gender-radio {
    flex: 1;

    :deep(.wd-radio) {
      justify-content: center;
      width: 100%;
    }
  }
}

.phone-auth {
  .phone-auth-btn {
    display: flex;
    gap: 12rpx;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 88rpx;
    font-size: 28rpx;
    color: #fff;
    background: linear-gradient(90deg, #165dff, #4080ff);
    border: none;
    border-radius: 12rpx;

    &[disabled] {
      opacity: 0.6;
    }

    .auth-text {
      font-size: 28rpx;
    }
  }
}

.phone-display {
  display: flex;
  gap: 12rpx;
  align-items: center;
  padding: 24rpx 20rpx;
  background: #f0f9ff;
  border: 1rpx solid #bae6fd;
  border-radius: 12rpx;

  .phone-number {
    flex: 1;
    font-size: 28rpx;
    color: #333;
  }

  .change-phone {
    font-size: 26rpx;
    color: #165dff;
  }
}

.footer {
  .complete-btn {
    margin-bottom: 30rpx;

    :deep(.wd-button) {
      height: 88rpx;
      font-size: 32rpx;
      font-weight: 600;
      border-radius: 44rpx;
    }
  }

  .skip-btn {
    text-align: center;

    text {
      font-size: 28rpx;
      color: rgba(255, 255, 255, 0.8);
      text-decoration: underline;
    }
  }
}

/* 内联WechatProfile组件的样式 */
.wechat-profile {
  padding: 20rpx;

  .avatar-section {
    margin-bottom: 40rpx;

    .avatar-button {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 160rpx;
      height: 160rpx;
      padding: 0;
      margin: 0 auto;
      overflow: hidden;
      background: transparent;
      border: none;
      border-radius: 50%;

      &::after {
        border: none;
      }
    }

    .avatar-image {
      width: 100%;
      height: 100%;
      border-radius: 50%;
    }

    .avatar-placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
      background: var(--wot-color-bg-light);
      border: 2rpx dashed var(--wot-color-border);
      border-radius: 50%;

      .placeholder-text {
        margin-top: 10rpx;
        font-size: 24rpx;
        color: var(--wot-color-text-secondary);
      }
    }
  }

  .nickname-section {
    margin-bottom: 40rpx;

    .nickname-input {
      box-sizing: border-box;
      width: 100%;
      height: 80rpx;
      padding: 0 20rpx;
      font-size: 28rpx;
      background: var(--wot-color-bg-light);
      border: 1rpx solid var(--wot-color-border);
      border-radius: 12rpx;
    }
  }

  .gender-section {
    .gender-group {
      display: flex;
      gap: 20rpx;

      .gender-radio {
        flex: 1;

        :deep(.wd-radio) {
          justify-content: center;
          width: 100%;
        }
      }
    }
  }
}
</style>
