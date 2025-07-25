<!-- 字典 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryFormData" :inline="true"  label-suffix=":" >
        <el-form-item prop="dict_name" label="字典名称">
          <el-input v-model="queryFormData.dict_name" placeholder="请输入字典名称" clearable />
        </el-form-item>
        <el-form-item prop="dict_type" label="字典类型">
          <el-input v-model="queryFormData.dict_type" placeholder="请输入字典类型" clearable />
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select v-model="queryFormData.status" placeholder="请选择状态" style="width: 167.5px" clearable>
            <el-option value="true" label="启用" />
            <el-option value="false" label="停用" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <el-date-picker v-model="queryFormData.start_time" type="daterange" value-format="yyyy-MM-dd" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
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
            <el-tooltip content="字典管理维护系统的字典。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            字典列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--actions">
          <el-button type="success" icon="plus" @click="handleOpenDialog('create')">新增</el-button>
          <el-button type="danger" icon="delete" :disabled="selectIds.length === 0" @click="handleDelete(selectIds)">批量删除</el-button>
          <el-dropdown trigger="click">
            <el-button type="default" :disabled="selectIds.length === 0" icon="ArrowDown">
              更多
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item icon="Check" @click="handleMoreClick(true)">批量启用</el-dropdown-item>
                <el-dropdown-item icon="CircleClose" @click="handleMoreClick(false)">批量停用</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        <div class="data-table__toolbar--tools">
          <el-tooltip content="导出">
            <el-button type="warning" icon="download" circle @click="handleExport" />
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
      <el-table ref="dataTableRef" v-loading="loading" :data="pageTableData" highlight-current-row class="data-table__content" height="450" border stripe @selection-change="handleSelectionChange">
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'selection')?.show" type="selection" min-width="55" align="center" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'index')?.show" type="index" fixed label="序号" min-width="60">
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'dict_name')?.show" key="dict_name" label="字典名称" prop="dict_name" min-width="140" show-overflow-tooltip/>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'dict_type')?.show" key="dict_type" label="字典类型" prop="dict_type" min-width="180">
          <template #default="scope">
            <el-tag type="primary">{{ scope.row.dict_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'status')?.show" key="status" label="状态" prop="status" min-width="80">
          <template #default="scope">
            <el-tag :type="scope.row.status === true ? 'success' : 'danger'">
              {{ scope.row.status ? "启用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'description')?.show" key="description" label="描述" prop="description" min-width="140" show-overflow-tooltip/>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'created_at')?.show" key="created_at" label="创建时间" prop="created_at" min-width="200" sortable />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'updated_at')?.show" key="updated_at" label="更新时间" prop="updated_at" min-width="200" sortable />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'creator')?.show" label="创建人" prop="creator" min-width="120">
          <template #default="scope">
            {{ scope.row.creator?.name }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'operation')?.show" fixed="right" label="操作" align="center" min-width="260">
          <template #default="scope">
            <el-button type="warning" size="small" link icon="document" @click="handleDictDataDrawer(scope.row.dict_type, scope.row.dict_name)">字典</el-button>
            <el-button type="info" size="small" link icon="document" @click="handleOpenDialog('detail', scope.row.id)">详情</el-button>
            <el-button type="primary" size="small" link icon="edit" @click="handleOpenDialog('update', scope.row.id)">编辑</el-button>
            <el-button type="danger" size="small" link icon="delete" @click="handleDelete([scope.row.id])">删除</el-button>
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
        <el-descriptions :column="4" border>
          <el-descriptions-item label="字典名称" :span="2">{{ detailFormData.dict_name }}</el-descriptions-item>
          <el-descriptions-item label="字典类型" :span="2">
            <el-tag type="primary">{{ detailFormData.dict_type }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag v-if="detailFormData.status" type="success">启用</el-tag>
            <el-tag v-else type="danger">停用</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ detailFormData.description }}</el-descriptions-item>
          <el-descriptions-item label="创建人" :span="2">{{ detailFormData.creator?.name }}</el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">{{ detailFormData.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">{{ detailFormData.updated_at }}</el-descriptions-item>
        </el-descriptions>
      </template>
      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form ref="dataFormRef" :model="formData" :rules="rules" label-suffix=":" label-width="auto" label-position="right">
          <el-form-item label="字典名称" prop="dict_name">
            <el-input v-model="formData.dict_name" placeholder="请输入字典名称" :maxlength="50" />
          </el-form-item>
          <el-form-item label="字典类型" prop="dict_type">
            <el-input v-model="formData.dict_type" placeholder="请输入字典类型" :maxlength="50" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-radio-group v-model="formData.status">
              <el-radio :value="true">启用</el-radio>
              <el-radio :value="false">停用</el-radio>
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
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">确定</el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <DataDrawer v-if="drawerVisible" v-model="drawerVisible" :dict-type="currentDictType" :dict-label="currentDictLabel" />

  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Dict",
  inheritAttrs: false,
});

import DictAPI, { DictTable, DictForm, DictPageQuery } from "@/api/system/dict";
import { ElMessage, ElMessageBox } from "element-plus";
import DataDrawer from "@/views/system/dict/components/DataDrawer.vue"

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);

const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<DictTable[]>([]);


// 表格列配置
const tableColumns = ref([
  { prop: 'selection', label: '选择框', show: true },
  { prop: 'index', label: '序号', show: true },
  { prop: 'dict_name', label: '字典名称', show: true },
  { prop: 'dict_type', label: '字典类型', show: true },
  { prop: 'status', label: '状态', show: true },
  { prop: 'description', label: '描述', show: true },
  { prop: 'creator', label: '创建人', show: true },
  { prop: 'created_at', label: '创建时间', show: true },
  { prop: 'updated_at', label: '更新时间', show: true },
  { prop: 'operation', label: '操作', show: true }
])

// 详情表单
const detailFormData = ref<DictTable>({});

// 分页查询参数
const queryFormData = reactive<DictPageQuery>({
  page_no: 1,
  page_size: 10,
  dict_name: undefined,
  dict_type: undefined,
  status: undefined,
  start_time: undefined,
  end_time: undefined,
});

// 编辑表单
const formData = reactive<DictForm>({
  id: undefined,
  dict_name: '',
  dict_type: '',
  status: true,
  description: undefined,
})

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: 'create' as 'create' | 'update' | 'detail',
});

// 表单验证规则
const rules = reactive({
  dict_name: [{ required: true, message: "请输入字典名称", trigger: "blur" }],
  dict_type: [{ required: true, message: "请选择字典类型", trigger: "blur" }],
  status: [{ required: true, message: "请选择字典状态", trigger: "blur" }],
});

// 列表刷新
async function handleRefresh () {
  await loadingData();
};


// 抽屉显隐
const drawerVisible = ref(false);

// 添加字典类型变量
const currentDictType = ref('');

// 添加字典名称变量
const currentDictLabel = ref('');

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await DictAPI.getDictTypeList(queryFormData);
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
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
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
    const response = await DictAPI.getDictTypeDetail(id);
    if (type === 'detail') {
      dialogVisible.title = "字典详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === 'update') {
      dialogVisible.title = "修改字典";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增字典";
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
          await DictAPI.updateDictType({ id, ...formData })
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
          await DictAPI.createDictType(formData)
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

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(async () => {
    try {
      loading.value = true;
      await DictAPI.deleteDictType(ids);
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

// 导出
async function handleExport() {
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

      const response = await DictAPI.exportDictType(body);
      const blob = new Blob([JSON.stringify(response.data.data)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8' });
      // 从响应头获取文件名
      const contentDisposition = response.headers['content-disposition'];
      let fileName = '字典类型.xlsx';
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

// 批量启用/停用
async function handleMoreClick(status: boolean) {
  if (selectIds.value.length) {
    ElMessageBox.confirm(`确认${status ? '启用' : '停用'}该项数据?`, "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    }).then(async () => {
      try {
        loading.value = true;
        await DictAPI.batchAvailableDict({ ids: selectIds.value, status });
        handleResetQuery();
      } catch (error: any) {
        ElMessage.error(error.message);
      } finally {
        loading.value = false;
      }
    }).catch(() => {
      ElMessage.info('已取消批量操作');
    });
  }
}

function handleDictDataDrawer(dictType: string, dictLabel: string) {
  currentDictType.value = dictType;
  currentDictLabel.value = dictLabel;
  drawerVisible.value = true;
}

onMounted(() => {
  loadingData();
});
</script>

<style lang="scss" scoped></style>
