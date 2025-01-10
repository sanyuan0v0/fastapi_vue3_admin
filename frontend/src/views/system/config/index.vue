<template>
  <div>
    <!-- 页面头部 -->
    <page-header />

    <!-- 配置项编辑区域 -->
    <div class="config-edit-wrapper">
      <a-card title="系统配置" :bordered="false">
        <!-- 动态生成配置项 -->
        <a-row :gutter="16">
          <a-col :span="12">
            <!-- 网站标题 -->
            <a-form-item label="网站标题">
              <a-input v-model:value="configData.title" placeholder="请输入网站标题" allowClear />
            </a-form-item>

            <!-- 网站图标 -->
            <a-form-item label="网站图标">
              <a-upload
                v-model:file-list="faviconFileList"
                list-type="picture-card"
                :before-upload="beforeUpload"
                :custom-request="(options) => handleUpload(options, 'favicon')"
              >
                <div v-if="!faviconFileList || faviconFileList.length === 0">
                  <plus-outlined />
                  <div style="margin-top: 8px">上传图标</div>
                </div>
              </a-upload>
            </a-form-item>

            <!-- 登录页Logo -->
            <a-form-item label="登录页Logo">
              <a-upload
                v-model:file-list="logoFileList"
                list-type="picture-card"
                :before-upload="beforeUpload"
                :custom-request="(options) => handleUpload(options, 'logo')"
              >
                <div v-if="!logoFileList || logoFileList.length === 0">
                  <plus-outlined />
                  <div style="margin-top: 8px">上传Logo</div>
                </div>
              </a-upload>
            </a-form-item>

            <!-- 登录页背景图 -->
            <a-form-item label="登录页背景图">
              <a-upload
                v-model:file-list="backgroundFileList"
                list-type="picture-card"
                :before-upload="beforeUpload"
                :custom-request="(options) => handleUpload(options, 'background')"
              >
                <div v-if="!backgroundFileList || backgroundFileList.length === 0">
                  <plus-outlined />
                  <div style="margin-top: 8px">上传背景图</div>
                </div>
              </a-upload>
            </a-form-item>

            <!-- 版权信息 -->
            <a-form-item label="网站描述">
              <a-input v-model:value="configData.description" placeholder="请输入版权信息" allowClear />
            </a-form-item>

            <!-- 版权信息 -->
            <a-form-item label="版权信息">
              <a-input v-model:value="configData.copyright" placeholder="请输入版权信息" allowClear />
            </a-form-item>

            <!-- 备案号 -->
            <a-form-item label="备案号">
              <a-input v-model:value="configData.keep_record" placeholder="请输入备案号" allowClear />
            </a-form-item>

            <!-- 帮助链接 -->
            <a-form-item label="帮助链接">
              <a-input v-model:value="configData.help_url" placeholder="请输入帮助链接" allowClear />
            </a-form-item>

            <!-- 隐私条款链接 -->
            <a-form-item label="隐私条款链接">
              <a-input v-model:value="configData.privacy_url" placeholder="请输入隐私条款链接" allowClear />
            </a-form-item>

            <!-- 服务条款链接 -->
            <a-form-item label="服务条款链接">
              <a-input v-model:value="configData.clause_url" placeholder="请输入服务条款链接" allowClear />
            </a-form-item>

            <!-- 代码仓库链接 -->
            <a-form-item label="代码仓库链接">
              <a-input v-model:value="configData.code_url" placeholder="请输入代码仓库链接" allowClear />
            </a-form-item>
          </a-col>
        </a-row>

        <!-- 保存按钮 -->
        <div style="text-align: right; margin-top: 24px;">
          <a-button type="primary" @click="handleSave">保存</a-button>
        </div>
      </a-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { getConfigInfo, updateConfig, uploadFile } from '@/api/system/config';
import PageHeader from '@/components/PageHeader.vue';
import type { tableDataType } from './types';

// 配置数据
const configData = reactive<tableDataType>({
    id: 1,
    title: 'FastAPI Vue Admin',
    favicon: 'http://example.com/favicon.png',
    logo: 'http://example.com/logo.png',
    background: 'http://example.com/background.png',
    description: 'FastAPI Vue Admin 是完全开源的权限管理系统',
    copyright: 'Copyright © 2021-2025 fastapi-vue-admin.com',
    keep_record: '晋ICP备18005113号-3',
    help_url: 'https://django-vue-admin.com',
    privacy_url: '/api/system/clause/privacy.html',
    clause_url: '/api/system/clause/terms_service.html',
    code_url: 'https://gitee.com/tao__tao/fastapi_vue_admin.git',
});

// 文件上传列表
const faviconFileList = ref<any[]>([]);
const logoFileList = ref<any[]>([]);
const backgroundFileList = ref<any[]>([]);

// 加载配置数据
const loadConfigData = async () => {
  try {
    const response = await getConfigInfo({});
    const data = response.data.data;

    // 填充配置数据
    Object.assign(configData, data);

    // 初始化文件上传列表
    if (data.favicon) {
      faviconFileList.value = [{ url: data.favicon }];
    }
    if (data.logo) {
      logoFileList.value = [{ url: data.logo }];
    }
    if (data.background) {
      backgroundFileList.value = [{ url: data.background }];
    }
  } catch (error) {
    console.error('加载配置数据失败:', error);
    message.error('加载配置数据失败');
  }
};

// 图片上传前的校验
const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/');
  if (!isImage) {
    message.error('只能上传图片文件！');
  }
  return isImage;
};

// 自定义上传逻辑
const handleUpload = async (options: any, type: string) => {
  const { file, onSuccess, onError } = options;

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await uploadFile(formData);
    const fileUrl = response.data.data.file_url;

    // 更新配置数据
    if (type === 'favicon') {
      configData.favicon = fileUrl;
      faviconFileList.value = [{ url: fileUrl }];
    } else if (type === 'logo') {
      configData.logo = fileUrl;
      logoFileList.value = [{ url: fileUrl }];
    } else if (type === 'background') {
      configData.background = fileUrl;
      backgroundFileList.value = [{ url: fileUrl }];
    }

    onSuccess(response, file);
    message.success('上传成功');
  } catch (error) {
    onError(error);
    console.error('上传失败:', error);
    message.error('上传失败');
  }
};

// 保存配置
const handleSave = async () => {
  try {
    // 调用更新配置接口
    await updateConfig(configData);
    message.success('配置保存成功');
    window.location.reload();
  } catch (error) {
    console.error('保存配置失败:', error);
    message.error('配置保存失败');
  }
};

// 生命周期钩子
onMounted(() => {
  loadConfigData();
});
</script>

<style lang="scss" scoped>
.config-edit-wrapper {
  margin-block-end: 16px;
}

.ant-card {
  margin-bottom: 24px;

  &:last-child {
    margin-bottom: 0;
  }
}
</style>