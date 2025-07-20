<template>
  <div>
    <el-dialog
      v-model="visible"
      :align-center="true"
      title="导入数据"
      width="600px"
      @close="handleClose"
    >
      <el-scrollbar max-height="60vh">
        <el-form
          ref="importFormRef"
          style="padding-right: var(--el-dialog-padding-primary)"
          :model="importFormData"
          :rules="importFormRules"
        >
          <el-form-item label="文件名" prop="files">
            <el-upload
              ref="uploadRef"
              v-model:file-list="importFormData.files"
              class="w-full"
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
              :drag="true"
              :limit="1"
              :auto-upload="false"
              :on-exceed="handleFileExceed"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或
                <em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  格式为*.xlsx / *.xls，文件不超过一个
                  <el-link
                    type="primary"
                    icon="download"
                    underline="never"
                    @click="handleDownloadTemplate"
                  >
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
          <el-button
            type="primary"
            :disabled="importFormData.files.length === 0"
            @click="handleUpload"
          >
            确 定
          </el-button>
          <el-button @click="handleClose">取 消</el-button>
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

    <!-- 导出弹窗预留 -->
    <el-dialog v-model="exportsModalVisible" :align-center="true" title="导出数据" width="600px" style="padding-right: 0" @close="handleCloseExportsModal">
      <!-- 滚动 -->
      <el-scrollbar max-height="60vh">
        <!-- 表单 -->
        <el-form ref="exportsFormRef" style="padding-right: var(--el-dialog-padding-primary)" :model="exportsFormData" :rules="exportsFormRules">
          <el-form-item label="文件名" prop="filename">
            <el-input v-model="exportsFormData.filename" clearable />
          </el-form-item>
          <el-form-item label="工作表名" prop="sheetname">
            <el-input v-model="exportsFormData.sheetname" clearable />
          </el-form-item>
          <el-form-item label="数据源" prop="origin">
            <el-select v-model="exportsFormData.origin">
              <el-option label="当前数据 (当前页的数据)" :value="ExportsOriginEnum.CURRENT" />
              <el-option label="选中数据 (所有选中的数据)" :value="ExportsOriginEnum.SELECTED" :disabled="selectionData.length <= 0" />
              <el-option label="全量数据 (所有分页的数据)" :value="ExportsOriginEnum.REMOTE" :disabled="contentConfig.exportsAction === undefined" />
            </el-select>
          </el-form-item>
          <el-form-item label="字段" prop="fields">
            <el-checkbox-group v-model="exportsFormData.fields">
              <template v-for="col in cols" :key="col.prop">
                <el-checkbox v-if="col.prop" :value="col.prop" :label="col.label" />
              </template>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <!-- 弹窗底部操作按钮 -->
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <el-button type="primary" @click="handleExportsSubmit">确 定</el-button>
          <el-button @click="handleCloseExportsModal">取 消</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 导入弹窗预留 -->
    <el-dialog v-model="importModalVisible" :align-center="true" title="导入数据" width="600px" style="padding-right: 0" @close="handleCloseImportModal">
      <!-- 滚动 -->
      <el-scrollbar max-height="60vh">
        <!-- 表单 -->
        <el-form ref="importFormRef" style="padding-right: var(--el-dialog-padding-primary)" :model="importFormData"
          :rules="importFormRules">
          <el-form-item label="文件名" prop="files">
            <el-upload ref="uploadRef" v-model:file-list="importFormData.files" class="w-full"
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
              :drag="true" :limit="1" :auto-upload="false" :on-exceed="handleFileExceed">
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                <span>将文件拖到此处，或</span>
                <em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  *.xlsx / *.xls
                  <el-link v-if="contentConfig.importTemplate" type="primary" icon="download" underline="never"
                    @click="handleDownloadTemplate">
                    下载模板
                  </el-link>
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <!-- 弹窗底部操作按钮 -->
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <el-button type="primary" :disabled="importFormData.files.length === 0" @click="handleImportSubmit">
            确 定
          </el-button>
          <el-button @click="handleCloseImportModal">取 消</el-button>
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
const visible = defineModel("modelValue", {
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

watch(visible, (newValue) => {
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
    const response = await UserAPI.importUser("1", importFormData.files[0].raw as File);
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
  visible.value = false;
};


// // 导出
// function handleExport() {
//   const filename = exportsFormData.filename
//     ? exportsFormData.filename
//     : props.contentConfig.permPrefix || "export";
//   const sheetname = exportsFormData.sheetname ? exportsFormData.sheetname : "sheet";
//   const workbook = new ExcelJS.Workbook();
//   const worksheet = workbook.addWorksheet(sheetname);
//   const columns: Partial<ExcelJS.Column>[] = [];
//   cols.value.forEach((col) => {
//     if (col.label && col.prop && exportsFormData.fields.includes(col.prop)) {
//       columns.push({ header: col.label, key: col.prop });
//     }
//   });
//   worksheet.columns = columns;
//   if (exportsFormData.origin === ExportsOriginEnum.REMOTE) {
//     if (props.contentConfig.exportsAction) {
//       props.contentConfig.exportsAction(lastFormData).then((res) => {
//         worksheet.addRows(res);
//         workbook.xlsx
//           .writeBuffer()
//           .then((buffer) => {
//             saveXlsx(buffer, filename as string);
//           })
//           .catch((error) => console.log(error));
//       });
//     } else {
//       ElMessage.error("未配置exportsAction");
//     }
//   } else {
//     worksheet.addRows(
//       exportsFormData.origin === ExportsOriginEnum.SELECTED ? selectionData.value : pageData.value
//     );
//     workbook.xlsx
//       .writeBuffer()
//       .then((buffer) => {
//         saveXlsx(buffer, filename as string);
//       })
//       .catch((error) => console.log(error));
//   }
// }

// // 下载导入模板
// function handleDownloadTemplate() {
//   const importTemplate = props.contentConfig.importTemplate;
//   if (typeof importTemplate === "string") {
//     window.open(importTemplate);
//   } else if (typeof importTemplate === "function") {
//     importTemplate().then((response) => {
//       const fileData = response.data;
//       const fileName = decodeURI(
//         response.headers["content-disposition"].split(";")[1].split("=")[1]
//       );
//       saveXlsx(fileData, fileName);
//     });
//   } else {
//     ElMessage.error("未配置importTemplate");
//   }
// }

// // 导入
// function handleImport() {
//   const importsAction = props.contentConfig.importsAction;
//   if (importsAction === undefined) {
//     ElMessage.error("未配置importsAction");
//     return;
//   }
//   // 获取选择的文件
//   const file = importFormData.files[0].raw as File;
//   // 创建Workbook实例
//   const workbook = new ExcelJS.Workbook();
//   // 使用FileReader对象来读取文件内容
//   const fileReader = new FileReader();
//   // 二进制字符串的形式加载文件
//   fileReader.readAsArrayBuffer(file);
//   fileReader.onload = (ev) => {
//     if (ev.target !== null && ev.target.result !== null) {
//       const result = ev.target.result as ArrayBuffer;
//       // 从 buffer中加载数据解析
//       workbook.xlsx
//         .load(result)
//         .then((workbook) => {
//           // 解析后的数据
//           const data = [];
//           // 获取第一个worksheet内容
//           const worksheet = workbook.getWorksheet(1);
//           if (worksheet) {
//             // 获取第一行的标题
//             const fields: any[] = [];
//             worksheet.getRow(1).eachCell((cell) => {
//               fields.push(cell.value);
//             });
//             // 遍历工作表的每一行（从第二行开始，因为第一行通常是标题行）
//             for (let rowNumber = 2; rowNumber <= worksheet.rowCount; rowNumber++) {
//               const rowData: IObject = {};
//               const row = worksheet.getRow(rowNumber);
//               // 遍历当前行的每个单元格
//               row.eachCell((cell, colNumber) => {
//                 // 获取标题对应的键，并将当前单元格的值存储到相应的属性名中
//                 rowData[fields[colNumber - 1]] = cell.value;
//               });
//               // 将当前行的数据对象添加到数组中
//               data.push(rowData);
//             }
//           }
//           if (data.length === 0) {
//             ElMessage.error("未解析到数据");
//             return;
//           }
//           importsAction(data).then(() => {
//             ElMessage.success("导入数据成功");
//             handleCloseImportModal();
//             handleRefresh(true);
//           });
//         })
//         .catch((error) => console.log(error));
//     } else {
//       ElMessage.error("读取文件失败");
//     }
//   };
// }
</script>
