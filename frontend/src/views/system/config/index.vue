<!-- 系统配置 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryFormData" :inline="true">
        <el-form-item prop="config_name" label="配置名称">
          <el-input v-model="queryFormData.config_name" placeholder="请输入配置名称" clearable />
        </el-form-item>
        <el-form-item prop="config_key" label="配置键名">
          <el-input v-model="queryFormData.config_key" placeholder="请输入配置键名" clearable />
        </el-form-item>
        <el-form-item prop="config_type" label="系统内置">
          <el-select v-model="queryFormData.config_type" placeholder="请选择系统内置" clearable style="width: 160px">
            <el-option value="true" label="是" />
            <el-option value="false" label="否" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <el-date-picker v-model="queryFormData.start_time" type="daterange" value-format="yyyy-MM-dd" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" />
        </el-form-item>
        <el-form-item class="search-buttons">
          <el-button type="primary" icon="search" @click="handleQuery">查询</el-button>
          <el-button icon="refresh" @click="handleResetQuery">重置</el-button>
          <!-- 展开/收起 -->
          <template v-if="isExpandable">
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
              {{ isExpand ? "收起" : "展开" }}
              <el-icon>
                <template v-if="isExpand">
                  <ArrowUp />
                </template>
                <template v-else>
                  <ArrowDown />
                </template>
              </el-icon>
            </el-link>
          </template>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card shadow="hover" class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="配置管理，包括系统名称、系统描述、系统版本、系统logo等。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            系统配置列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--actions">
          <el-button type="success" icon="plus" @click="handleOpenDialog('create')">新增</el-button>
          <el-button type="danger" icon="delete" :disabled="selectIds.length === 0" @click="handleOperation('delete')">批量删除</el-button>
        </div>
        <div class="data-table__toolbar--tools">
          <el-tooltip content="导入">
            <el-button type="info" icon="upload" circle @click="handleOperation('import')" />
          </el-tooltip>
          <el-tooltip content="导出">
            <el-button type="warning" icon="download" circle @click="handleOperation('export')" />
          </el-tooltip>
          <el-tooltip content="刷新">
            <el-button type="primary" icon="refresh" circle @click="handleRefresh" />
          </el-tooltip>
          <el-tooltip content="列表筛选">
            <el-dropdown trigger="click">
              <el-button type="default" icon="operation" circle />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-for="column in tableColumns" :key="column.prop" :command="column">
                    <el-checkbox v-model="column.show">{{ column.label }}</el-checkbox>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-tooltip>
        </div>
      </div>

      <!-- 表格区域：系统配置列表 -->
      <el-table ref="dataTableRef" v-loading="loading" :data="pageTableData" highlight-current-row
        class="data-table__content" height="450" border stripe @selection-change="handleSelectionChange">
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'selection')?.show" type="selection" width="55" align="center" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'index')?.show" type="index" fixed label="序号" width="60" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'config_name')?.show" key="config_name" label="配置名称" prop="config_name" min-width="80" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'config_key')?.show" key="config_key" label="配置键" prop="config_key" min-width="120" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'config_value')?.show" key="config_value" label="配置值" prop="config_value" min-width="100" show-overflow-tooltip />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'config_type')?.show" key="config_type" label="系统内置" prop="config_type" min-width="60">
          <template #default="scope">
            <el-tag v-if="scope.row.config_type" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'description')?.show" key="description" label="描述" prop="description" min-width="100" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'created_at')?.show" key="created_at" label="创建时间" prop="created_at" min-width="120" sortable />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'updated_at')?.show" key="updated_at" label="更新时间" prop="updated_at" min-width="120" sortable />

        <el-table-column v-if="tableColumns.find(col => col.prop === 'operation')?.show" fixed="right" label="操作" min-width="120">
          <template #default="scope">
            <el-button type="info" size="small" link icon="document" @click="handleOpenDialog('detail', scope.row.id)">详情</el-button>
            <el-button type="primary" size="small" link icon="edit" @click="handleOpenDialog('update', scope.row.id)">编辑</el-button>
            <el-button type="danger" size="small" link icon="delete" @click="handleOperation('delete', scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination v-model:total="total" v-model:page="queryFormData.page_no" v-model:limit="queryFormData.page_size" @pagination="loadingData" />
      </template>
    </el-card>

    <!-- 弹窗区域 -->
    <el-dialog v-model="dialogVisible.visible" :title="dialogVisible.title" @close="handleCloseDialog">
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="配置名称" :span="2">{{ detailFormData.config_name }}</el-descriptions-item>
          <el-descriptions-item label="系统内置" :span="2">
            <el-tag v-if="detailFormData.config_type" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="配置键" :span="2">{{ detailFormData.config_key }}</el-descriptions-item>
          <el-descriptions-item label="配置值" :span="2">{{ detailFormData.config_value }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ detailFormData.description }}</el-descriptions-item>
          <el-descriptions-item label="创建人" :span="2">{{ detailFormData.creator?.name }}</el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">{{ detailFormData.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">{{ detailFormData.updated_at }}</el-descriptions-item>
        </el-descriptions>
      </template>
      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form ref="dataFormRef" :model="formData" :rules="rules" label-suffix=":" label-width="100px">
          <el-form-item label="配置名称" prop="config_name">
            <el-input v-model="formData.config_name" placeholder="请输入配置名称" :maxlength="50" />
          </el-form-item>
          <el-form-item label="配置键" prop="config_key">
            <el-input v-model="formData.config_key" placeholder="请输入配置键" :maxlength="50" />
          </el-form-item>
          <el-form-item label="配置值" prop="config_value">
            <el-input v-model="formData.config_value" placeholder="请输入配置值" :maxlength="100" />
          </el-form-item>
          <el-form-item label="系统内置" prop="config_type">
            <el-radio-group v-model="formData.config_type">
              <el-radio :value="true">是</el-radio>
              <el-radio :value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="formData.description" :rows="4" :maxlength="100" show-word-limit type="textarea" placeholder="请输入描述" />
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">确定</el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
          <el-button @click="handleCloseDialog">取消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 导出弹窗 -->
    <el-dialog v-model="exportsModalVisible" :align-center="true" title="导出数据" width="600px" style="padding-right: 0"
      @close="handleCloseExportsModal">
      <!-- 滚动 -->
      <el-scrollbar max-height="60vh">
        <!-- 表单 -->
        <el-form ref="exportsFormRef" style="padding-right: var(--el-dialog-padding-primary)" :model="exportsFormData"
          :rules="exportsFormRules">
          <el-form-item label="文件名" prop="filename">
            <el-input v-model="exportsFormData.filename" clearable />
          </el-form-item>
          <el-form-item label="工作表名" prop="sheetname">
            <el-input v-model="exportsFormData.sheetname" clearable />
          </el-form-item>
          <el-form-item label="数据源" prop="origin">
            <el-select v-model="exportsFormData.origin">
              <el-option label="当前数据 (当前页的数据)" :value="ExportsOriginEnum.CURRENT" />
              <el-option label="选中数据 (所有选中的数据)" :value="ExportsOriginEnum.SELECTED"
                :disabled="selectionData.length <= 0" />
              <el-option label="全量数据 (所有分页的数据)" :value="ExportsOriginEnum.REMOTE"
                :disabled="contentConfig.exportsAction === undefined" />
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
    <!-- 导入弹窗 -->
    <el-dialog v-model="importModalVisible" :align-center="true" title="导入数据" width="600px" style="padding-right: 0"
      @close="handleCloseImportModal">
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

<script setup lang="ts">
defineOptions({
  name: "Config",
  inheritAttrs: false,
});

import ConfigAPI, { ConfigTable, ConfigForm, ConfigPageQuery } from "@/api/system/config";
import { ElMessage, ElMessageBox } from "element-plus";
import { useDebounceFn } from "@vueuse/core";

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);

const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<ConfigTable[]>([]);


// 表格列配置
const tableColumns = ref([
  { prop: 'selection', label: '选择框', show: true },
  { prop: 'index', label: '序号', show: true },
  { prop: 'config_name', label: '配置名称', show: true },
  { prop: 'config_key', label: '配置键', show: true },
  { prop: 'config_value', label: '配置值', show: true },
  { prop: 'config_type', label: '系统内置', show: true },
  { prop: 'description', label: '描述', show: true },
  { prop: 'created_at', label: '创建时间', show: true },
  { prop: 'updated_at', label: '更新时间', show: true },
  { prop: 'operation', label: '操作', show: true }
])

// 详情表单
const detailFormData = ref<ConfigTable>({});

// 分页查询参数
const queryFormData = reactive<ConfigPageQuery>({
  page_no: 1,
  page_size: 10,
  config_name: undefined,
  config_key: undefined,
  config_type: undefined,
  start_time: undefined,
  end_time: undefined,
});

// 编辑表单
const formData = reactive<ConfigForm>({
  id: undefined,
  config_name: '',
  config_key: '',
  config_value: '',
  config_type: false,
  description: ''
})

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: 'create' as 'create' | 'update' | 'detail',
});

// 表单验证规则
const rules = reactive({
  config_name: [{ required: true, message: "请输入系统配置名称", trigger: "blur" }],
  config_key: [{ required: true, message: "请输入系统配置键", trigger: "blur" }],
  config_value: [{ required: true, message: "请输入系统配置值", trigger: "blur" }],
  config_type: [{ required: true, message: "请选择系统配置类型", trigger: "blur" }],
});

// 刷新数据(防抖)
const handleRefresh = useDebounceFn(() => {
  loadingData();
  ElMessage.success("刷新成功");
}, 1000);

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await ConfigAPI.getConfigList(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  }
  catch (error: any) {
    ElMessage.error(error.message);
  }
  finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  loadingData();
}

// 重置表单
async function resetForm() {
  dataFormRef.value.resetFields();
  dataFormRef.value.clearValidate();
  formData.id = undefined;
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开系统配置弹窗
async function handleOpenDialog(type: 'create' | 'update' | 'detail', id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await ConfigAPI.getConfigDetail({ id });
    if (type === 'detail') {
      dialogVisible.title = "系统配置详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === 'update') {
      dialogVisible.title = "修改系统配置";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增系统配置";
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

// 新增、编辑弹窗处理
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await ConfigAPI.updateConfig(formData)
          dialogVisible.visible = false;
          resetForm();
          handleResetQuery();
        } catch (error: any) {
          ElMessage.error(error.message);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await ConfigAPI.createConfig(formData)
          ElMessage.success("新增成功");
          dialogVisible.visible = false;
          resetForm();
          handleResetQuery();
        } catch (error: any) {
          ElMessage.error(error.message);
        } finally {
          loading.value = false;
        }
      }
    }
  });
}

// 删除系统配置
async function handleOperation(type: 'delete' | 'import' | 'export', id?: number) {
  if (type === 'delete' && !id && !selectIds.value.length) {
    ElMessageBox.confirm("确认删除该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    }).then(async () => {
      try {
        loading.value = true;
        await ConfigAPI.deleteConfig({ id: id ? id : selectIds.value });
        ElMessage.success("删除成功");
        handleResetQuery();
      } catch (error: any) {
        ElMessage.error(error.message);
      } finally {
        loading.value = false;
      }
    }).catch(() => {
      ElMessage.info('已取消删除');
    });
  }
  else if (type === 'import') {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx, .xls';
    input.click();

    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        try {
          loading.value = true;
          await ConfigAPI.uploadFile(formData);
          ElMessage.success('导入成功');
          handleResetQuery();
        } catch (error: any) {
          ElMessage.error(error.message);
        } finally {
          loading.value = false;
        }
      }
    }
  }
  else if (type === 'export') {
    ElMessageBox.confirm('是否确认导出当前系统配置?', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      try {
        loading.value = true;
        const body = {
          ...queryFormData,
          page_no: 1,
          page_size: total.value
        };
        ElMessage.warning('正在导出数据，请稍候...');

        const response = await ConfigAPI.exportConfig(body);
        const blob = new Blob([JSON.stringify(response.data)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8' });
        // 从响应头获取文件名
        const contentDisposition = response.headers['content-disposition'];
        let fileName = '系统配置.xlsx';
        if (contentDisposition) {
          const fileNameMatch = contentDisposition.match(/filename=(.*?)(;|$)/);
          if (fileNameMatch) {
            fileName = decodeURIComponent(fileNameMatch[1]);
          }
        }
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        ElMessage.success('导出成功');
      } catch (error: any) {
        ElMessage.error('文件处理失败', error.message);
        console.error('导出错误:', error);
      } finally {
        loading.value = false;
      }
    }).catch(() => {
      ElMessage.info('已取消导出');
    });
  }
  else {
    ElMessage.error('未知操作类型');
  }
}

// 导出
function handleExport() {
  const filename = exportsFormData.filename
    ? exportsFormData.filename
    : props.contentConfig.permPrefix || "export";
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

// 下载导入模板
function handleDownloadTemplate() {
  const importTemplate = props.contentConfig.importTemplate;
  if (typeof importTemplate === "string") {
    window.open(importTemplate);
  } else if (typeof importTemplate === "function") {
    importTemplate().then((response) => {
      const fileData = response.data;
      const fileName = decodeURI(
        response.headers["content-disposition"].split(";")[1].split("=")[1]
      );
      saveXlsx(fileData, fileName);
    });
  } else {
    ElMessage.error("未配置importTemplate");
  }
}

// 导入
function handleImport() {
  const importsAction = props.contentConfig.importsAction;
  if (importsAction === undefined) {
    ElMessage.error("未配置importsAction");
    return;
  }
  // 获取选择的文件
  const file = importFormData.files[0].raw as File;
  // 创建Workbook实例
  const workbook = new ExcelJS.Workbook();
  // 使用FileReader对象来读取文件内容
  const fileReader = new FileReader();
  // 二进制字符串的形式加载文件
  fileReader.readAsArrayBuffer(file);
  fileReader.onload = (ev) => {
    if (ev.target !== null && ev.target.result !== null) {
      const result = ev.target.result as ArrayBuffer;
      // 从 buffer中加载数据解析
      workbook.xlsx
        .load(result)
        .then((workbook) => {
          // 解析后的数据
          const data = [];
          // 获取第一个worksheet内容
          const worksheet = workbook.getWorksheet(1);
          if (worksheet) {
            // 获取第一行的标题
            const fields: any[] = [];
            worksheet.getRow(1).eachCell((cell) => {
              fields.push(cell.value);
            });
            // 遍历工作表的每一行（从第二行开始，因为第一行通常是标题行）
            for (let rowNumber = 2; rowNumber <= worksheet.rowCount; rowNumber++) {
              const rowData: IObject = {};
              const row = worksheet.getRow(rowNumber);
              // 遍历当前行的每个单元格
              row.eachCell((cell, colNumber) => {
                // 获取标题对应的键，并将当前单元格的值存储到相应的属性名中
                rowData[fields[colNumber - 1]] = cell.value;
              });
              // 将当前行的数据对象添加到数组中
              data.push(rowData);
            }
          }
          if (data.length === 0) {
            ElMessage.error("未解析到数据");
            return;
          }
          importsAction(data).then(() => {
            ElMessage.success("导入数据成功");
            handleCloseImportModal();
            handleRefresh(true);
          });
        })
        .catch((error) => console.log(error));
    } else {
      ElMessage.error("读取文件失败");
    }
  };
}

onMounted(() => {
  loadingData();
});
</script>

<style lang="scss" scoped></style>
