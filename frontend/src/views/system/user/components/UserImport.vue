<template>
  <div>
    <!-- 导入弹窗预留 -->
    <el-dialog v-model="importModalVisible" :align-center="true" title="导入数据" width="600px" @close="handleClose">
      <!-- 滚动 -->
      <el-scrollbar max-height="60vh">
        <!-- 表单 -->
        <el-form ref="importFormRef" style="padding-right: var(--el-dialog-padding-primary)" :model="importFormData" :rules="importFormRules">
          <el-form-item label="文件名" prop="files">
            <el-upload ref="uploadRef" v-model:file-list="importFormData.files" class="w-full" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" :drag="true" :limit="1" :auto-upload="false" :on-exceed="handleFileExceed">
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或
                <em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  格式为*.xlsx / *.xls，文件不超过一个
                  <el-link type="primary" icon="download" underline="never" @click="handleDownloadTemplate">
                    下载模板
                  </el-link>
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <el-button v-if="resultData.length > 0" type="primary" @click="handleShowResult">
            错误信息
          </el-button>
          <el-button @click="handleClose">取 消</el-button>
          <el-button
            type="primary"
            :disabled="importFormData.files.length === 0"
            @click="handleUpload"
          >
            确 定
          </el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="resultVisible" title="导入结果" width="600px">
      <el-alert
        :title="`导入结果：${invalidCount}条无效数据，${validCount}条有效数据`"
        type="warning"
        :closable="false"
      />
      <el-table :data="resultData" style="width: 100%; max-height: 400px">
        <el-table-column prop="index" align="center" width="100" type="index" label="序号" />
        <el-table-column prop="message" label="错误信息" width="400">
          <template #default="scope">
            {{ scope.row }}
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCloseResult">关闭</el-button>
        </div>
      </template>
    </el-dialog>    
  </div>
</template>

<script lang="ts" setup>
import { ElMessage, type UploadUserFile } from "element-plus";
import UserAPI from "@/api/system/user";
import { ResultEnum } from "@/enums/api/result.enum";

const emit = defineEmits(["import-success"]);
const importModalVisible = defineModel("modelValue", {
  type: Boolean,
  required: true,
  default: false,
});

const resultVisible = ref(false);
const resultData = ref<string[]>([]);
const invalidCount = ref(0);
const validCount = ref(0);

const importFormRef = ref(null);
const uploadRef = ref(null);

const importFormData = reactive<{
  files: UploadUserFile[];
}>({
  files: [],
});

watch(importModalVisible, (newValue) => {
  if (newValue) {
    resultData.value = [];
    resultVisible.value = false;
    invalidCount.value = 0;
    validCount.value = 0;
  }
});

const importFormRules = {
  files: [{ required: true, message: "文件不能为空", trigger: "blur" }],
};

// 文件超出个数限制
const handleFileExceed = () => {
  ElMessage.warning("只能上传一个文件");
};

// 下载导入模板
const handleDownloadTemplate = () => {
  UserAPI.downloadTemplate().then((response: any) => {
    const fileData = response.data.data;
    const fileName = decodeURI(response.headers["content-disposition"].split(";")[1].split("=")[1]);
    const fileType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8";

    const blob = new Blob([fileData], { type: fileType });
    const downloadUrl = window.URL.createObjectURL(blob);

    const downloadLink = document.createElement("a");
    downloadLink.href = downloadUrl;
    downloadLink.download = fileName;

    document.body.appendChild(downloadLink);
    downloadLink.click();

    document.body.removeChild(downloadLink);
    window.URL.revokeObjectURL(downloadUrl);
  });
};

// 上传文件
const handleUpload = async () => {
  if (!importFormData.files.length) {
    ElMessage.warning("请选择文件");
    return;
  }

  try {
    const response = await UserAPI.importUser(importFormData.files[0].raw as File);
    if (response.data.code === ResultEnum.SUCCESS) {
      ElMessage.success("导入成功，导入数据：" + response.data.data.count + "条");
      emit("import-success");
      handleClose();
    } else {
      ElMessage.error("上传失败");
      resultVisible.value = true;
      resultData.value = response.data.data.messageList;
      invalidCount.value = response.data.data.invalidCount;
      validCount.value = response.data.data.validCount;
    }
  } catch (error: any) {
    console.error(error);
    ElMessage.error("上传失败：" + error);
  }
};

// 显示错误信息
const handleShowResult = () => {
  resultVisible.value = true;
};

// 关闭错误信息弹窗
const handleCloseResult = () => {
  resultVisible.value = false;
};

// 关闭弹窗
const handleClose = () => {
  importFormData.files.length = 0;
  importModalVisible.value = false;
};

</script>
