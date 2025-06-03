<template>
  <div class="config-container">
    <!-- 文本配置项卡片 -->
    <a-card title="文本配置项" style="max-width: 1100px; flex: 1;">
      <a-list :data-source="textDataSource" :grid="{ gutter: 16, column: 1 }">
        <template #renderItem="{ item }">
          <a-list-item>
            <div class="config-item">
                <span class="config-name">{{ item.config_name }}:
                </span>
                <a-input
                  v-model:value="configData[item.config_key]"
                  :placeholder="`请输入${item.config_name}`"
                  allowClear
                  class="long-input"
                />
                <a-button
                  type="primary"
                  @click="handleSave(item)"
                  :disabled="!configData[item.config_key]"
                  :loading="isSaving[item.config_key]"
                  size="small"
                  class="save-button"
                >
                  保存
                </a-button>
            </div>
          </a-list-item>
        </template>
      </a-list>
    </a-card>

    <!-- 图片配置项卡片 -->
    <a-card title="图片配置项" style="flex: 1; max-width: 400px; ">
      <a-list :data-source="imageDataSource" :grid="{ gutter: 16, column: 1 }">
        <template #renderItem="{ item }">
          <a-list-item>
            <div class="config-item">
              <div class="config-name">{{ item.config_name }}</div>
              <div class="config-value">
                <a-upload
                  :name="item.config_key"
                  v-model:file-list="fileLists[item.config_key]"
                  list-type="picture-card"
                  :before-upload="beforeUpload"
                  :custom-request="(options) => handleUpload(options, item.config_key)"
                  class="image-upload"
                >
                  <div v-if="!fileLists[item.config_key] || fileLists[item.config_key].length === 0">
                    <plus-outlined />
                    <div style="margin-top: 8px">上传{{ item.config_name }}</div>
                  </div>
                </a-upload>
              </div>
              <div class="config-action">
                <a-button
                  type="primary"
                  @click="handleSave(item)"
                  :disabled="!fileLists[item.config_key]?.length"
                  :loading="isSaving[item.config_key]"
                  size="small"
                  class="save-button"
                >
                  保存
                </a-button>
              </div>
            </div>
          </a-list-item>
        </template>
      </a-list>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { getInitConfig, updateConfig, uploadFile } from '@/api/system/config';
import type { tableDataType } from './types';
import { PlusOutlined } from '@ant-design/icons-vue';
// 定义 configData
const configData = reactive<Record<string, any>>({});

const dataSource = ref<tableDataType[]>([]);
const textDataSource = ref<tableDataType[]>([]);
const imageDataSource = ref<tableDataType[]>([]);
const configState = reactive<tableDataType>({
  id: undefined,
  config_name: '',
  config_key: '',
  config_value: '',
  config_type: null,
  description: ''
});

// 存储文件上传列表
const fileLists = reactive<Record<string, any[]>>({});

// 定义图片类型的配置项键名
const imageKeys = ['sys_web_favicon', 'sys_web_logo', 'sys_login_background'];
// 定义需要展示的配置项键名
const requiredKeys = [
  'sys_web_title',
  'sys_web_description',
  'sys_web_favicon',
  'sys_web_logo',
  'sys_login_background',
  'sys_web_copyright',
  'sys_keep_record',
  'sys_help_doc',
  'sys_web_privacy',
  'sys_web_clause',
  'sys_git_code'
];

// 保存状态管理
const isSaving = reactive<Record<string, boolean>>({});

// 编辑状态管理
const isEditing = reactive<Record<string, boolean>>({});

// 加载配置数据
const loadConfigData = async () => {
  try {
    const response = await getInitConfig({});
    // 过滤出需要展示的数据
    dataSource.value = response.data.data.filter((item: any) => requiredKeys.includes(item.config_key));

    // 根据键名分离文本和图片配置项
    textDataSource.value = dataSource.value.filter(item => !imageKeys.includes(item.config_key));
    imageDataSource.value = dataSource.value.filter(item => imageKeys.includes(item.config_key));

    // 将数组转为 key-value 形式
    const dataMap: Record<string, any> = {};
    dataSource.value.forEach((item: any) => {
      dataMap[item.config_key] = item.config_value;
    });

    // 更新 configData
    Object.assign(configData, dataMap);

    // 初始化 fileLists，确保图片类型的配置项能够正确显示
    imageDataSource.value.forEach((item: any) => {
      if (item.config_value) {
        fileLists[item.config_key] = [{ url: item.config_value }];
      }
    });
  } catch (error) {
    console.error('加载配置数据失败:', error);
  }
};

// 自定义上传逻辑
const handleUpload = async (options: any, type: string) => {
  const { file, onSuccess, onError } = options;

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await uploadFile(formData);
    // 确保从响应中正确获取 file_url
    const fileUrl = response.data.data.file_url;

    // 更新 fileLists，确保视图能够正确响应
    fileLists[type] = [{ url: fileUrl }];

    // 触发视图更新
    configData[type] = fileUrl;

    onSuccess(response);
  } catch (error) {
    onError(error);
    console.error('上传失败:', error);
  }
};

// 保存配置
const handleSave = async (item: any) => {
  isSaving[item.config_key] = true; // 设置保存状态
  const tempConfigState = {
    ...configState,
    id: item.id,
    config_name: item.config_name,
    config_key: item.config_key,
    // 确保从 fileLists 中获取正确的图片 URL
    config_value: imageKeys.includes(item.config_key)
      ? fileLists[item.config_key][0]?.url || configData[item.config_key]
      : configData[item.config_key],
    config_type: item.config_type,
    description: item.description
  };

  try {
    await updateConfig(tempConfigState);
    message.success(`${item.config_name} 保存成功`);
    isEditing[item.config_key] = false; // 退出编辑模式
  } catch (error) {
    message.error(`${item.config_name} 保存失败: ${error.message}`);
  } finally {
    isSaving[item.config_key] = false; // 重置保存状态
  }
};

// 图片上传前的校验
const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/');
  if (!isImage) {
    message.error('只能上传图片文件！');
    return false; // 确保返回 false 阻止非法文件上传
  }
  return true;
};

// 编辑操作
const handleEdit = (configKey: string) => {
  isEditing[configKey] = true;
};

// 取消操作
const handleCancel = (configKey: string) => {
  isEditing[configKey] = false;
};

// 生命周期钩子
onMounted(() => {
  loadConfigData();
});
</script>

<style lang="scss" scoped>
.config-container {
  display: flex;
  justify-content: space-between;
  gap: 16px; /* 添加间距 */
}

.config-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.config-name {
  white-space: nowrap; /* 防止换行 */
  font-weight: bold; /* 加粗显示 */
}
</style>


