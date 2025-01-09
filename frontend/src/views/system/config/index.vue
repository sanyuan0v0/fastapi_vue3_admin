<template>
  <div>
    <!-- 页面头部 -->
    <page-header />

    <!-- 配置项编辑区域 -->
    <div class="config-edit-wrapper">
      <a-card title="系统配置" :bordered="false">
        <!-- 动态生成配置项 -->
        <template v-for="group in updateState" :key="group.id">
          <a-card :title="group.name" :bordered="false" style="margin-bottom: 24px;">
            <a-row :gutter="16">
              <template v-for="config in group.children" :key="config.id">
                <a-col :span="12">
                  <!-- 图片上传类型 -->
                  <a-form-item v-if="config.fied_key === 'web_favicon' || config.fied_key === 'login_logo' || config.fied_key === 'login_background'" :label="config.name">
                    <a-upload
                      v-model:file-list="config.fileList"
                      list-type="picture-card"
                      :before-upload="beforeUpload"
                      :custom-request="(options) => handleUpload(options, config)"
                    >
                      <div v-if="!config.fileList || config.fileList.length === 0">
                        <plus-outlined />
                        <div style="margin-top: 8px">上传图片</div>
                      </div>
                    </a-upload>
                  </a-form-item>

                  <!-- 输入框类型 -->
                  <a-form-item v-else :label="config.name">
                    <a-input v-model:value="config.fied_value" :placeholder="`请输入${config.name}`" allowClear />
                  </a-form-item>
                </a-col>
              </template>
            </a-row>
          </a-card>
        </template>

        <!-- 保存按钮 -->
        <div style="text-align: right; margin-top: 24px;">
          <a-button type="primary" @click="handleSave">保存</a-button>
        </div>
      </a-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { getConfigList, batchConfig, uploadFile } from '@/api/system/config';
import PageHeader from '@/components/PageHeader.vue';
import type { tableDataType } from './types'

interface ConfigGroup extends tableDataType {
  children: tableDataType[];
  fileList?: any[];
}

const updateState = reactive<ConfigGroup[]>([]);

// 加载配置数据
const loadConfigData = async () => {
  try {
    const response = await getConfigList({});
    const items = response.data.data.items;

    // 将配置项按父级分组
    const groups = items
      .filter(item => item.parent_id === null) // 获取顶级配置项
      .map(group => ({
        ...group,
        children: items.filter(item => item.parent_id === group.id) // 获取子配置项
      }));

    // 初始化图片上传列表
    groups.forEach(group => {
      group.children.forEach(config => {
        if (config.fied_key === 'web_favicon' || config.fied_key === 'login_logo' || config.fied_key === 'login_background') {
          config.fileList = config.fied_value ? [{ url: config.fied_value }] : [];
        }
      });
    });

    // 避免直接修改 reactive 对象，使用重新赋值的方式
    updateState.length = 0; // 清空数组
    updateState.push(...groups); // 添加新数据
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
const handleUpload = async (options: any, config: any) => {
  const { file, onSuccess, onError } = options;

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await uploadFile(formData);
    const fileUrl = response.data.data.file_url; // 使用 file_url 更新配置项的值

    // 更新配置项的值
    config.fied_value = fileUrl;
    config.fileList = [{ url: fileUrl }]; // 更新文件列表显示

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
    // 提取所有配置项（包括父级和子级）
    const configs = updateState.flatMap(group => [
      {
        id: group.id,
        name: group.name,
        order: group.order,
        fied_key: group.fied_key,
        fied_value: group.fied_value,
        parent_id: group.parent_id,
      },
      ...group.children.map(config => ({
        id: config.id,
        name: config.name,
        order: config.order,
        fied_key: config.fied_key,
        fied_value: config.fied_value,
        parent_id: config.parent_id,
      })),
    ]);

    // 调用批量保存接口，直接发送数组
    await batchConfig(configs); // 修改为直接发送数组
    message.success('配置保存成功');
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