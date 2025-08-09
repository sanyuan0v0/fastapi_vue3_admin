<template>
  <view class="app-container">
    <wd-navbar title="意见反馈" left-arrow @click-left="handleBack" />

    123
    <wd-text size="small">选填，最多上传3张图片</wd-text>
    <wd-form ref="formRef" :model="formData" :rules="rules">
      <!-- 问题类型选择 -->
      <wd-form-item label="问题类型" prop="feedbackType">
        <wd-radio-group v-model="formData.feedbackType" inline>
          <wd-radio v-for="item in feedbackTypes" :key="item.value" :value="item.value">
            {{ item.label }}
          </wd-radio>
        </wd-radio-group>
      </wd-form-item>

      <!-- 问题描述 -->
      <wd-form-item label="问题描述" prop="description">
        <wd-textarea
          v-model="formData.description"
          placeholder="请详细描述您遇到的问题或建议..."
          :maxlength="120"
          show-word-limit
        />
      </wd-form-item>

      <!-- 图片上传 -->
      <wd-form-item label="相关截图" prop="fileList">
        <wd-upload
          v-model="formData.fileList"
          :max-count="3"
          :before-read="beforeRead"
          @delete="handleDelete"
        />
      </wd-form-item>

      <!-- 联系方式 -->
      <wd-form-item label="联系方式" prop="contact">
        <wd-input v-model="formData.contact" placeholder="请输入您的手机号或邮箱" clearable />
        <wd-text size="small">选填，便于我们与您联系</wd-text>
      </wd-form-item>

      <!-- 提交按钮 -->
      <view class="submit-btn">
        <wd-button type="primary" block :loading="submitting" @click="handleSubmit">
          提交反馈
        </wd-button>
      </view>
    </wd-form>
  </view>
</template>

<script setup lang="ts">
import { checkLogin } from "@/utils/auth";
import { useToast } from "wot-design-uni";
import { FormRules } from "wot-design-uni/components/wd-form/types";

const toast = useToast();
const formRef = ref();

// 检查登录状态
onLoad(() => {
  if (!checkLogin()) return;
});

// 问题类型选项
const feedbackTypes = [
  { label: "功能异常", value: "bug" },
  { label: "优化建议", value: "suggestion" },
  { label: "其他问题", value: "other" },
];

// 表单数据
const formData = reactive({
  feedbackType: "bug",
  description: "",
  fileList: [] as Array<Record<string, any>>,
  contact: "",
});

// 表单验证规则
const rules: FormRules = {
  description: [
    {
      required: true,
      message: "请描述您遇到的问题",
      validator: (value) => {
        if (value && value.trim()) {
          return Promise.resolve();
        } else {
          return Promise.reject("请描述您遇到的问题");
        }
      },
    },
  ],
  contact: [
    {
      required: false,
      validator: (value) => {
        if (!value) return Promise.resolve(); // 非必填
        const emailReg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
        const phoneReg = /^1[3456789]\d{9}$/;
        return emailReg.test(value) || phoneReg.test(value)
          ? Promise.resolve()
          : Promise.reject("请输入正确的手机号或邮箱");
      },
      message: "请输入正确的手机号或邮箱",
      trigger: "blur",
    },
  ],
};

// 提交状态
const submitting = ref(false);

// 图片上传前的校验
const beforeRead = (file: Record<string, any>) => {
  // 验证文件类型
  const validTypes = ["image/jpeg", "image/png", "image/gif"];
  if (!validTypes.includes(file.type)) {
    toast.error("请上传 jpg、png 或 gif 格式的图片");
    return false;
  }
  // 验证文件大小（限制为 5MB）
  if (file.size > 5 * 1024 * 1024) {
    toast.error("图片大小不能超过 5MB");
    return false;
  }
  return true;
};

// 删除图片
const handleDelete = (detail: { index: number }) => {
  const index = detail.index;
  formData.fileList.splice(index, 1);
};

// 提交反馈
const handleSubmit = async () => {
  // 表单验证
  try {
    const { valid } = await formRef.value.validate();

    if (valid) {
      submitting.value = true;
      try {
        // TODO: 调用提交反馈的接口
        await new Promise((resolve) => setTimeout(resolve, 1500)); // 模拟提交
        toast.success("提交成功");

        // 重置表单
        formRef.value.reset();
        formData.feedbackType = "bug";
        formData.description = "";
        formData.fileList = [];
        formData.contact = "";

        // 延迟返回上一页
        setTimeout(() => {
          uni.navigateBack();
        }, 1500);
      } catch (_error) {
        toast.error("提交失败，请重试");
      } finally {
        submitting.value = false;
      }
    }
  } catch (_error) {
    // 表单验证失败
    console.log("表单验证失败");
  }
};

// 返回
const handleBack = () => {
  uni.navigateBack();
};
</script>

<style lang="scss" scoped>
:deep(.wd-form-item) {
  margin-bottom: 12rpx;
}

.submit-btn {
  margin: 40rpx 30rpx;
}
</style>
