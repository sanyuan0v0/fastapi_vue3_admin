<template>
  <div>
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
    
  </div>
</template>

<script lang="ts" setup>
import UserAPI from "@/api/system/user";
import { ResultEnum } from "@/enums/api/result.enum";
import { useDateFormat, useThrottleFn } from "@vueuse/core";
import {
  ElMessage,
  type FormInstance,
  type FormRules,
} from "element-plus";
import ExcelJS from "exceljs";
import { reactive, ref } from "vue";

const emit = defineEmits(["export-success"]);
// const exportsModalVisible = ref(false);
const exportsModalVisible = defineModel("modelValue", {
  type: Boolean,
  required: true,
  default: false,
});

export type IObject = Record<string, any>;

export interface IContentConfig<T = any> {
  // 后端导出的网络请求函数(需返回promise)
  exportAction?: (queryParams: T) => Promise<any>;
  // 前端全量导出的网络请求函数(需返回promise)
  exportsAction?: (queryParams: T) => Promise<IObject[]>;
  // table组件列属性(额外的属性templet,operat,slotName)
  cols: Array<{
    type?: "default" | "selection" | "index" | "expand";
    label?: string;
    prop?: string;
    width?: string | number;
    align?: "left" | "center" | "right";
    columnKey?: string;
    reserveSelection?: boolean;
    // 列是否显示
    show?: boolean;
    // 模板
    templet?:
      | "image"
      | "list"
      | "url"
      | "switch"
      | "input"
      | "price"
      | "percent"
      | "icon"
      | "date"
      | "tool"
      | "custom";
    // image模板相关参数
    imageWidth?: number;
    imageHeight?: number;
    // list模板相关参数
    selectList?: IObject;
    // switch模板相关参数
    activeValue?: boolean | string | number;
    inactiveValue?: boolean | string | number;
    activeText?: string;
    inactiveText?: string;
    // input模板相关参数
    inputType?: string;
    // price模板相关参数
    priceFormat?: string;
    // date模板相关参数
    dateFormat?: string;
    // filter值拼接符
    filterJoin?: string;
    [key: string]: any;
    // 初始化数据函数
    initFn?: (item: IObject) => void;
    // 是否禁用
    disabled?: boolean;
  }>;
}
// 定义接收的属性
const props = defineProps<{ contentConfig: IContentConfig }>();

// 表格列
const cols = ref(
  props.contentConfig.cols.map((col) => {
    if (col.initFn) {
      col.initFn(col);
    }
    if (col.show === undefined) {
      col.show = true;
    }
    if (col.prop !== undefined && col.columnKey === undefined && col["column-key"] === undefined) {
      col.columnKey = col.prop;
    }
    if (
      col.type === "selection" &&
      col.reserveSelection === undefined &&
      col["reserve-selection"] === undefined
    ) {
      // 配合表格row-key实现跨页多选
      col.reserveSelection = true;
    }
    return col;
  })
);

// 列表数据
const pageData = ref<IObject[]>([]);

// 行选中
const selectionData = ref<IObject[]>([]);

// 导出表单
const fields: string[] = [];
cols.value.forEach((item) => {
  if (item.prop !== undefined) {
    fields.push(item.prop);
  }
});

// 导出类型
const enum ExportsOriginEnum {
  CURRENT = "current",
  SELECTED = "selected",
  REMOTE = "remote",
}

const exportsFormRef = ref<FormInstance>();
const exportsFormData = reactive({
  filename: "",
  sheetname: "",
  fields,
  origin: ExportsOriginEnum.CURRENT,
});
const exportsFormRules: FormRules = {
  fields: [{ required: true, message: "请选择字段" }],
  origin: [{ required: true, message: "请选择数据源" }],
};

// 导出确认
const handleExportsSubmit = useThrottleFn(() => {
  exportsFormRef.value?.validate((valid: boolean) => {
    if (valid) {
      handleExports();
      handleCloseExportsModal();
    }
  });
}, 3000);

// 关闭导出弹窗
function handleCloseExportsModal() {
  exportsModalVisible.value = false;
  exportsFormRef.value?.resetFields();
  nextTick(() => {
    exportsFormRef.value?.clearValidate();
  });
}

// 导出
function handleExports() {
  const filename = exportsFormData.filename;
  const sheetname = exportsFormData.sheetname ? exportsFormData.sheetname : "sheet";
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet(sheetname);
  const columns: Partial<ExcelJS.Column>[] = [];
  cols.value.forEach((col) => {
    if (col.label && col.prop && exportsFormData.fields.includes(col.prop)) {
      columns.push({ header: col.label, key: col.prop });
    }
  });
  worksheet.columns = columns;
  if (exportsFormData.origin === ExportsOriginEnum.REMOTE) {
    if (props.contentConfig.exportsAction) {
      props.contentConfig.exportsAction(lastFormData).then((res) => {
        worksheet.addRows(res);
        workbook.xlsx
          .writeBuffer()
          .then((buffer) => {
            saveXlsx(buffer, filename as string);
          })
          .catch((error) => console.log(error));
      });
    } else {
      ElMessage.error("未配置exportsAction");
    }
  } else {
    worksheet.addRows(
      exportsFormData.origin === ExportsOriginEnum.SELECTED ? selectionData.value : pageData.value
    );
    workbook.xlsx
      .writeBuffer()
      .then((buffer) => {
        saveXlsx(buffer, filename as string);
      })
      .catch((error) => console.log(error));
  }
}

// 获取分页数据
let lastFormData = {};

// 浏览器保存文件
function saveXlsx(fileData: any, fileName: string) {
  const fileType =
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8";

  const blob = new Blob([fileData], { type: fileType });
  const downloadUrl = window.URL.createObjectURL(blob);

  const downloadLink = document.createElement("a");
  downloadLink.href = downloadUrl;
  downloadLink.download = fileName;

  document.body.appendChild(downloadLink);
  downloadLink.click();

  document.body.removeChild(downloadLink);
  window.URL.revokeObjectURL(downloadUrl);
}

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
