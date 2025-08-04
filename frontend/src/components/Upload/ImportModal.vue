<template>
  <div>
    <!-- 导入弹窗 -->
    <el-dialog v-model="importModalVisible" :align-center="true" :title="props.title" :width="props.width" @close="handleClose">
      <!-- 滚动 -->
      <el-scrollbar :max-height="props.maxHeight">
        <!-- 表单 -->
        <el-form ref="importFormRef" style="padding-right: var(--el-dialog-padding-primary)" :model="importFormData" :rules="importFormRules">
          <el-form-item label="文件名" prop="files">
            <el-upload 
              ref="uploadRef" 
              v-model:file-list="importFormData.files" 
              class="w-full" 
              :accept="props.accept" 
              :drag="true" 
              :limit="props.limit" 
              :auto-upload="false" 
              :on-exceed="handleFileExceed"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                {{ props.dropText || '将文件拖到此处，或' }}
                <em>{{ props.browseText || '点击上传' }}</em>
              </div>
              <template #tip>
                <div class="el-upload__tip flex flex-wrap gap-2">
                  <el-text v-if="props.note" type="warning" class="mx-1">{{ props.note }}</el-text>
                  <el-text v-if="props.fileTypeWarning" type="danger" class="mx-1">{{ props.fileTypeWarning }}</el-text>
                  <el-link v-if="props.showTemplateDownload" class="mx-1" type="primary" icon="download" underline="never" @click="handleDownloadTemplate">
                    {{ props.templateDownloadText || '下载模板' }}
                  </el-link>
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <el-button @click="handleClose">{{ props.cancelButtonText || '取 消' }}</el-button>
          <el-button
            type="primary"
            :disabled="importFormData.files.length === 0 || loading"
            @click="handleUpload"
          >
            <el-icon v-if="loading"><Loading /></el-icon>
            {{ props.confirmButtonText || '确 定' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ElMessage, type UploadUserFile } from "element-plus";
import { ref, reactive } from "vue";

// 定义props
const props = defineProps({
  /**
   * 弹窗标题
   */
  title: {
    type: String,
    default: "导入数据"
  },

  /**
   * 弹窗宽度
   */
  width: {
    type: String,
    default: "600px"
  },

  /**
   * 最大高度
   */
  maxHeight: {
    type: String,
    default: "60vh"
  },

  /**
   * 接受的文件类型
   */
  accept: {
    type: String,
    default: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
  },

  /**
   * 文件数量限制
   */
  limit: {
    type: Number,
    default: 1
  },

  /**
   * 是否显示下载模板按钮
   */
  showTemplateDownload: {
    type: Boolean,
    default: true
  },

  /**
   * 拖放提示文本
   */
  dropText: {
    type: String,
    default: undefined
  },

  /**
   * 浏览按钮文本
   */
  browseText: {
    type: String,
    default: undefined
  },

  /**
   * 模板下载按钮文本
   */
  templateDownloadText: {
    type: String,
    default: undefined
  },

  /**
   * 取消按钮文本
   */
  cancelButtonText: {
    type: String,
    default: undefined
  },

  /**
   * 确认按钮文本
   */
  confirmButtonText: {
    type: String,
    default: undefined
  },

  /**
   * 注意事项文本
   */
  note: {
    type: String,
    default: "注意事项："
  },

  /**
   * 文件类型警告文本
   */
  fileTypeWarning: {
    type: String,
    default: "格式为*.xlsx / *.xls，文件不超过 5MB"
  },

  /**
   * 上传文件的参数名
   */
  uploadFileName: {
    type: String,
    default: "file"
  },

  /**
   * 上传请求的额外参数
   */
  uploadData: {
    type: Object,
    default: () => ({})
  }
});

// 定义模型值（控制弹窗显示/隐藏）
const importModalVisible = defineModel("modelValue", {
  type: Boolean,
  required: true,
  default: false
});

// 定义事件
const emit = defineEmits(["import-success", "import-fail", "close", "download-template", "upload"]);

// 引用
const importFormRef = ref(null);
const uploadRef = ref(null);
const loading = ref(false);

// 表单数据
const importFormData = reactive<{
  files: UploadUserFile[];
}>({
  files: []
});

// 表单规则
const importFormRules = {
  files: [{ required: true, message: "文件不能为空", trigger: "blur" }]
};

// 文件超出个数限制
const handleFileExceed = () => {
  ElMessage.warning(`只能上传${props.limit}个文件`);
};

// 下载导入模板 - 由父组件实现具体逻辑
const handleDownloadTemplate = () => {
  emit("download-template");
};

// 上传文件 - 由父组件实现具体逻辑
const handleUpload = async () => {
  if (!importFormData.files.length) {
    ElMessage.warning("请选择文件");
    return;
  }

  try {
    loading.value = true;
    const file = importFormData.files[0].raw as File;
    const formData = new FormData();
    formData.append(props.uploadFileName, file);

    // 添加额外参数
    Object.keys(props.uploadData).forEach(key => {
      formData.append(key, props.uploadData[key]);
    });

    // 触发上传事件，由父组件处理具体上传逻辑
    emit("upload", formData, file);
  } catch (error: any) {
    console.error(error);
    ElMessage.error("上传失败：" + error);
    emit("import-fail", error);
  } finally {
    loading.value = false;
  }
};

// 关闭弹窗
const handleClose = () => {
  importFormData.files.length = 0;
  importModalVisible.value = false;
  emit("close");
};

// 提供给父组件的方法
defineExpose({
  handleClose
});
</script>