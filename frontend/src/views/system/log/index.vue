<!-- 日志管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryFormData" :inline="true">
        <el-form-item prop="request_path" label="请求路径">
          <el-input v-model="queryFormData.request_path" placeholder="请输入请求路径" clearable />
        </el-form-item>
        <el-form-item prop="creator_name" label="创建人">
          <el-input v-model="queryFormData.creator_name" placeholder="请输入创建人" clearable />
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <el-date-picker v-model="queryFormData.start_time" type="daterange" value-format="yyyy-MM-dd"
            range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" />
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
            <el-tooltip content="日志管理维护系统的日志。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            日志列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--actions">
          <el-button type="danger" icon="delete" :disabled="selectIds.length === 0"
            @click="handleDelete(selectIds)">批量删除</el-button>
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
      <el-table ref="dataTableRef" v-loading="loading" :data="pageTableData" highlight-current-row
        class="data-table__content" height="450" border stripe @selection-change="handleSelectionChange">
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'selection')?.show" prop='selection'
          type="selection" min-width="55" align="center" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'index')?.show" type="index" fixed label="序号"
          min-width="60" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'request_path')?.show" label="请求路径"
          prop="request_path" min-width="200" show-overflow-tooltip />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'request_method')?.show" label="请求方法"
          prop="request_method" min-width="100">
          <template #default="scope">
            <el-tag :type="getMethodType(scope.row.request_method)">
              {{ scope.row.request_method }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'response_code')?.show" label="状态码"
          prop="response_code" min-width="100">
          <template #default="scope">
            <el-tag :type="getStatusCodeType(scope.row.response_code)">
              {{ scope.row.response_code }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'request_ip')?.show" label="请求IP" prop="request_ip"
          min-width="150">
          <template #default="scope">
            <el-text>{{ scope.row.request_ip }}</el-text>
            <CopyButton v-if="scope.row.request_ip" :text="scope.row.request_ip" style="margin-left: 2px" />
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'process_time')?.show" label="处理时间"
          prop="process_time" min-width="200" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'request_browser')?.show" label="浏览器"
          prop="request_browser" min-width="100" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'request_os')?.show" label="系统" prop="request_os"
          min-width="100" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'description')?.show" label="描述" prop="description"
          min-width="120" show-overflow-tooltip />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'created_at')?.show" label="创建时间" prop="created_at"
          min-width="200" sortable />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'creator')?.show" label="创建人" prop="creator"
          min-width="120">
          <template #default="scope">
            {{ scope.row.creator?.name }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" min-width="150">
          <template #default="scope">
            <el-button type="primary" size="small" link icon="document"
              @click="handleOpenDialog('detail', scope.row.id)">详情</el-button>
            <el-button type="danger" size="small" link icon="delete"
              @click="handleDelete([scope.row.id])">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination v-model:total="total" v-model:page="queryFormData.page_no" v-model:limit="queryFormData.page_size"
          @pagination="loadingData" />
      </template>
    </el-card>

    <!-- 弹窗区域 -->
    <el-dialog v-model="dialogVisible.visible" :title="dialogVisible.title" @close="handleCloseDialog">
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="请求路径" :span="2">{{ detailFormData.request_path }}</el-descriptions-item>
          <el-descriptions-item label="请求方法" :span="2">
            <el-tag :type="getMethodType(detailFormData.request_method)">
              {{ detailFormData.request_method }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="响应状态码" :span="2">
            <el-tag :type="getStatusCodeType(detailFormData.response_code)">
              {{ detailFormData.response_code }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="请求IP" :span="2">{{ detailFormData.request_ip }}</el-descriptions-item>
          <el-descriptions-item label="请求参数" :span="4">
            <el-input v-model="detailFormData.request_payload" type="textarea" :rows="3" readonly
              class="long-text-editor" />
          </el-descriptions-item>
          <el-descriptions-item label="响应数据" :span="4">
            <!-- <el-input v-model="detailFormData.response_json" type="textarea" :rows="5" readonly
              class="long-text-editor" /> -->
            <el-scrollbar max-height="72vh">
              <div class="absolute z-36 right-5 top-2">
                <el-link type="primary" @click="handleCopyCode">
                  <el-icon>
                    <CopyDocument />
                  </el-icon>
                  一键复制
                </el-link>
              </div>

              <Codemirror ref="cmRef" v-model:value="code" placeholder="请输入代码" :options="cmOptions" border
                :readonly="true" :width="700" :height="100" />
            </el-scrollbar>
          </el-descriptions-item>
          <el-descriptions-item label="处理时间" :span="2">{{ detailFormData.process_time }}</el-descriptions-item>
          <el-descriptions-item label="浏览器" :span="2">{{ detailFormData.request_browser }}</el-descriptions-item>
          <el-descriptions-item label="操作系统" :span="2">{{ detailFormData.request_os }}</el-descriptions-item>
          <el-descriptions-item label="登录地点" :span="2">{{ detailFormData.login_location }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ detailFormData.description }}</el-descriptions-item>
          <el-descriptions-item label="创建人" :span="2">{{ detailFormData.creator?.name }}</el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">{{ detailFormData.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">{{ detailFormData.updated_at }}</el-descriptions-item>
        </el-descriptions>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button type="primary" @click="handleCloseDialog">确定</el-button>
          <el-button @click="handleCloseDialog">取消</el-button>
        </div>
      </template>
    </el-dialog>

  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Log",
  inheritAttrs: false,
});

import "codemirror/mode/javascript/javascript.js";
import Codemirror, { type CmComponentRef } from "codemirror-editor-vue3";
import type { EditorConfiguration } from "codemirror";

import LogAPI, { LogTable, LogPageQuery } from "@/api/system/log";
import { ElMessage, ElMessageBox } from "element-plus";
import { useDebounceFn } from "@vueuse/core";

const { copy, copied } = useClipboard();
const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);
const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<LogTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: 'selection', label: '选择框', show: true },
  { prop: 'index', label: '序号', show: true },
  { prop: 'request_path', label: '请求路径', show: true },
  { prop: 'request_method', label: '请求方法', show: true },
  { prop: 'response_code', label: '响应状态码', show: true },
  { prop: 'request_ip', label: '请求IP', show: true },
  { prop: 'process_time', label: '处理时间', show: true },
  { prop: 'request_browser', label: '浏览器', show: true },
  { prop: 'request_os', label: '操作系统', show: true },
  { prop: 'login_location', label: '登录地点', show: true },
  { prop: 'description', label: '描述', show: true },
  { prop: 'creator', label: '创建人', show: true },
  { prop: 'created_at', label: '创建时间', show: true },
  { prop: 'updated_at', label: '更新时间', show: true },
  { prop: 'operation', label: '操作', show: true }
])

// 详情表单
const detailFormData = ref<LogTable>({});

// 分页查询参数
const queryFormData = reactive<LogPageQuery>({
  page_no: 1,
  page_size: 10,
  request_path: undefined,
  creator_name: undefined,
  start_time: undefined,
  end_time: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: 'create' as 'create' | 'update' | 'detail',
});

// 刷新数据(防抖)
const handleRefresh = useDebounceFn(() => {
  loadingData();
  ElMessage.success("刷新成功");
}, 1000);

const getStatusCodeType = (code?: number) => {
  if (code === undefined) {
    return 'info';
  }
  if (code >= 200 && code < 300) {
    return 'success';
  } else if (code >= 300 && code < 400) {
    return 'warning';
  } else if (code >= 400 && code < 500) {
    return 'danger';
  } else {
    return 'danger';
  }
}

const getMethodType = (method?: string) => {
  if (method === undefined) {
    return 'info';
  }
  if (method === 'GET') {
    return 'info';
  } else if (method === 'POST') {
    return 'success';
  } else if (method === 'PUT' || method === 'PATCH') {
    return 'warning';
  } else if (method === 'DELETE') {
    return 'danger';
  } else {
    return 'info';
  }
}

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await LogAPI.getLogList(queryFormData);
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
  detailFormData.value.id = undefined;
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

// 打开日志详情弹窗
async function handleOpenDialog(type: 'create' | 'update' | 'detail', id: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await LogAPI.getLogDetail({ id });
    if (type === 'detail') {
      dialogVisible.title = "日志详情";
      Object.assign(detailFormData.value, response.data.data);
      code.value = response.data.data.response_json
    }
  }
  dialogVisible.visible = true;
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  if (!ids && !selectIds.value.length) {
    ElMessageBox.confirm("确认删除该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    }).then(async () => {
      try {
        loading.value = true;
        await LogAPI.deleteLog({ ids });
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

      const response = await LogAPI.exportLog(body);
      const blob = new Blob([JSON.stringify(response.data.data)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8' });
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

const cmOptions: EditorConfiguration = {
  mode: "text/javascript",
};
const code = ref();
const cmRef = ref<CmComponentRef>();

/** 一键复制 */
const handleCopyCode = () => {
  if (code.value) {
    copy(code.value);
  }
};

watch(copied, () => {
  if (copied.value) {
    ElMessage.success("复制成功");
  }
});

onMounted(() => {
  loadingData();
});
</script>

<style lang="scss" scoped></style>
