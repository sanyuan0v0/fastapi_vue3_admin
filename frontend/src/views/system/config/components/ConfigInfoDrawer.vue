<template>
  <el-drawer v-model="drawerVisible" title="配置中心" :size="drawerSize">
    <el-form :model="configState" label-suffix=":" label-width="auto" label-position="right">
      <!-- 系统配置 -->
      <el-divider>系统配置</el-divider>
      <div v-for="(item, key) in systemConfigs" :key="key">
        <el-form-item :label="item.config_name">
          <span class="flex items-center gap-2 w-full">
            <el-input
              v-model="item.config_value"
              :placeholder="t('common.inputText')"
              clearable
              style="width: 100%"
              @input="markModified(key)"
            />
          </span>
        </el-form-item>
      </div>

      <!-- logo配置 -->
      <el-divider>logo配置</el-divider>
      <div v-for="(item, key) in logoConfigs" :key="key">
        <el-form-item :label="item.config_name">
          <div class="flex items-center gap-2 w-full">
            <SingleImageUpload
              v-model="item.config_value"
              :data="{ type: key }"
              :name="'file'"
              :max-file-size="item.maxFileSize"
              :file-list="fileLists[key] || []"
              @on-success="(fileInfo: UploadFilePath) => handleUploadSuccess(fileInfo, key)"
              @on-error="handleUploadError"
              @input="markModified(key)"
            />
          </div>
        </el-form-item>
      </div>      
    </el-form>

    <template #footer> 
      <!-- 操作按钮 -->
      <el-button @click="resetForm">取消</el-button>
      <el-button type="primary" :disabled="!hasChanges" @click="submitChanges" >保存</el-button>
    </template>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, computed } from 'vue';
import ConfigAPI, { type ConfigTable } from '@/api/system/config';
import { useConfigStore } from "@/store";
import { useI18n } from 'vue-i18n';
import { ElMessage, ElMessageBox } from 'element-plus';
import SingleImageUpload from '@/components/Upload/SingleImageUpload.vue';
import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";

// 文件列表类型定义
interface FileListItem {
  url: string;
}


const appStore = useAppStore();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "500px" : "90%"));

const t = useI18n().t;
const configStore = useConfigStore();

// 配置状态管理
const drawerVisible = ref<boolean>(false);
const configState = reactive<ConfigTable>({
  id: undefined,
  config_name: '',
  config_key: '',
  config_value: '',
  config_type: undefined,
  description: ''
});

// 存储文件上传列表
const fileLists = reactive<Record<string, FileListItem[]>>({});

// 记录修改过的字段
const modifiedFields = reactive<Record<string, boolean>>({});

// 标记字段为已修改
const markModified = (key: string) => {
  modifiedFields[key] = true;
};

// 判断是否有修改
const hasChanges = computed(() => Object.keys(modifiedFields).length > 0);

// 提交修改
const submitChanges = async () => {
  const keysToSubmit = Object.keys(modifiedFields);
  if (keysToSubmit.length === 0) return;

  try {
    // 并行处理所有修改请求，提高性能
    const updatePromises = keysToSubmit.map(key => {
      const item = systemConfigs.value[key as keyof typeof systemConfigs.value] || logoConfigs.value[key as keyof typeof logoConfigs.value];
      return item ? ConfigAPI.updateConfig({ ...item }) : Promise.resolve();
    });

    await Promise.all(updatePromises);
    ElMessage.success('保存成功');

    // 清除已提交的修改标记
    keysToSubmit.forEach(key => {
      delete modifiedFields[key];
    });
  } catch (error) {
    console.error('保存失败:', error);
    // 提供更详细的错误信息
    const errorMessage = error instanceof Error ? error.message : '更新配置时发生错误';
    ElMessage.error(`保存失败：${errorMessage}`);
  }
};

// 取消修改：重置所有修改字段的状态并恢复初始值
const resetForm = () => {
  const keysToReset = Object.keys(modifiedFields);
  for (const key of keysToReset) {
    if (systemConfigs.value[key as keyof typeof systemConfigs.value]) {
      systemConfigs.value[key as keyof typeof systemConfigs.value].config_value = configStore.configData[key as keyof typeof configStore.configData]?.config_value || '';
    } else if (logoConfigs.value[key as keyof typeof logoConfigs.value]) {
      logoConfigs.value[key as keyof typeof logoConfigs.value].config_value = configStore.configData[key as keyof typeof configStore.configData]?.config_value || '';
    }
    delete modifiedFields[key];
  }
  ElMessageBox.close();
};

// 系统配置项
const systemConfigs = computed(() => ({
  sys_web_title: configStore.configData.sys_web_title,
  sys_web_version: configStore.configData.sys_web_version,
  sys_help_doc: configStore.configData.sys_help_doc,
  sys_git_code: configStore.configData.sys_git_code,
  sys_keep_record: configStore.configData.sys_keep_record,
  sys_web_clause: configStore.configData.sys_web_clause,
  sys_web_copyright: configStore.configData.sys_web_copyright,
  sys_web_privacy: configStore.configData.sys_web_privacy,
  sys_web_description: configStore.configData.sys_web_description,
}));

// logo配置项
const logoConfigs = computed(() => ({
  sys_web_logo: {
    ...configStore.configData.sys_web_logo,
    maxFileSize: 5,
  },
  sys_web_favicon: {
    ...configStore.configData.sys_web_favicon,
    maxFileSize: 2,
  },
  sys_login_background: {
    ...configStore.configData.sys_login_background,
    maxFileSize: 10,
  },
}));

// 图片上传成功的回调处理
const handleUploadSuccess = (fileInfo: UploadFilePath, type: string) => {
  // 使用正确的file_url属性
  const fileUrl = fileInfo.file_url;
  
  // 更新store中的数据
  if (type in configStore.configData) {
    configStore.configData[type as keyof typeof configStore.configData].config_value = fileUrl;
  }
  
  // 更新对应的item.config_value，确保v-model绑定生效
  if (type in systemConfigs.value) {
    systemConfigs.value[type as keyof typeof systemConfigs.value].config_value = fileUrl;
  } else if (type in logoConfigs.value) {
    logoConfigs.value[type as keyof typeof logoConfigs.value].config_value = fileUrl;
  }
  
  // 更新文件列表
  fileLists[type] = [{ url: fileUrl }];
  
  // 标记为已修改
  markModified(type);
};

// 图片上传失败的回调处理
const handleUploadError = (error: any) => {
  console.error('上传失败:', error.message || '未知错误');
  ElMessage.error(`上传失败：${error.message || '请稍后重试'}`);
};

// 生命周期钩子
onMounted(() => {
  configStore.getConfig();
});
</script>

<style lang="scss" scoped>
.flex {
  display: flex;
}
.items-center {
  align-items: center;
}
.justify-end {
  justify-content: flex-end;
}
.gap-4 {
  gap: 1rem;
}
.mt-6 {
  margin-top: 1.5rem;
}
</style>
