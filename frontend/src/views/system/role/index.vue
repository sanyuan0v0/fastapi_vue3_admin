<!-- 岗位管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryFormData" :inline="true">
        <el-form-item prop="name" label="岗位名称">
          <el-input v-model="queryFormData.name" placeholder="请输入岗位名称" clearable />
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select v-model="queryFormData.status" placeholder="请选择状态" clearable style="width: 160px">
            <el-option value="true" label="启用" />
            <el-option value="false" label="停用" />
          </el-select>
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
            <el-tooltip content="角色管理维护系统的角色和权限。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            角色管理列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--actions">
          <el-button type="success" icon="plus" @click="handleOpenDialog('create')">新增</el-button>
          <el-button type="danger" icon="delete" :disabled="selectIds.length === 0"
            @click="handleOperation('delete')">批量删除</el-button>
          <el-dropdown>
            <el-button type="default" :disabled="selectIds.length === 0" icon="ArrowDown">更多
            </el-button>
            <template #dropdown>
              <el-menu @click="handleMoreClick">
                <el-menu-item key="1">
                  <span>
                    <el-icon>
                      <Check />
                    </el-icon>
                    <span>批量启用</span>
                  </span>
                </el-menu-item>
                <el-menu-item key="2">
                  <span>
                    <el-icon>
                      <CircleClose />
                    </el-icon>
                    <span>批量停用</span>
                  </span>
                </el-menu-item>
              </el-menu>
            </template>
          </el-dropdown>
        </div>
        <div class="data-table__toolbar--tools">
          <el-tooltip content="导入">
            <el-button type="info" icon="upload" circle @click="handleOperation('import')"/>
          </el-tooltip>
          <el-tooltip content="导出">
            <el-button type="warning" icon="download" circle @click="handleOperation('export')"/>
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

      <el-table ref="dataTableRef" v-loading="loading" :data="pageTableData" highlight-current-row
        class="data-table__content" height="450" border stripe @selection-change="handleSelectionChange">
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'selection')?.show" type="selection" width="55"
          align="center" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'index')?.show" type="index" fixed label="序号"
          width="60" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'name')?.show" key="name" label="角色名称" prop="name"
          min-width="80" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'data_scope')?.show" key="data_scope" label="数据权限"
          prop="data_scope" min-width="80" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'order')?.show" key="order" label="岗位排序"
          prop="order" min-width="100" show-overflow-tooltip />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'status')?.show" key="status" label="状态"
          prop="status" min-width="60">
          <template #default="scope">
            <el-tag :type="scope.row.status === true ? 'success' : 'danger'">
              {{ scope.row.status === true ? "启用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'description')?.show" key="description" label="描述"
          prop="description" min-width="100" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'created_at')?.show" key="created_at" label="创建时间"
          prop="created_at" min-width="120" sortable />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'updated_at')?.show" key="updated_at" label="更新时间"
          prop="updated_at" min-width="120" sortable />

        <el-table-column v-if="tableColumns.find(col => col.prop === 'operation')?.show" fixed="right" label="操作"
          min-width="220">
          <template #default="scope">
            <el-button type="primary" size="small" link icon="position"
              @click="handleOpenAssignPermDialog(scope.row)">分配权限</el-button>
            <el-button type="info" size="small" link icon="document"
              @click="handleOpenDialog('detail', scope.row.id)">详情</el-button>
            <el-button type="primary" size="small" link icon="edit"
              @click="handleOpenDialog('update', scope.row.id)">编辑</el-button>
            <el-button type="danger" size="small" link icon="delete"
              @click="handleOperation('delete', scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination v-model:total="total" v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size" @pagination="loadingData" />
      </template>
    </el-card>

    <!-- 角色表单弹窗 -->
    <el-dialog v-model="dialogVisible.visible" :title="dialogVisible.title" width="500px" @close="handleCloseDialog">
      <el-form ref="roleFormRef" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入角色名称" />
        </el-form-item>

        <el-form-item label="排序" prop="order">
          <el-input-number v-model="formData.order" controls-position="right" :min="0" style="width: 100px" />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :value="true">启用</el-radio>
            <el-radio :value="false">停用</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input v-model="formData.description" :rows="4" :maxlength="100" show-word-limit type="textarea"
            placeholder="请输入描述" />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="handleSubmit">确 定</el-button>
          <el-button @click="handleCloseDialog">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 分配权限弹窗 -->
    <el-drawer v-model="assignPermDialogVisible" :title="'【' + checkedRole.name + '】权限分配'" :size="drawerSize">
      <div style="min-width: 300px;">
        <div style="display: flex; gap: 10px; ">
          <div style="width: 10px; background-color: #1677ff;"></div>
          <div>
            <span style="font-size: 16px;">数据授权</span>
            <a-tooltip placement="right">
              <template #title>
                <span>授权用户可操作的数据范围</span>
              </template>
              <QuestionCircleOutlined style="margin-left: 5px;" />
            </a-tooltip>
          </div>
        </div>

        <el-form ref="roleFormRef" :model="formData" :rules="rules" label-width="100px">
          <el-form-item label="数据权限" prop="data_scope">
            <el-select v-model="permissionState.data_scope">
              <el-option :key="1" label="全部数据" :value="1" />
              <el-option :key="2" label="部门及子部门数据" :value="2" />
              <el-option :key="3" label="本部门数据" :value="3" />
              <el-option :key="4" label="本人数据" :value="4" />
              <el-option :key="5" label="自定义数据" :value="5" />
            </el-select>
          </el-form-item>
        </el-form>

        <el-tree v-if="permissionState.data_scope === 5 && deptTreeData.length" :checked-keys="permissionState.dept_ids"
          :row-key="record => record.id" :tree-data="deptTreeData" :default-expand-all=true
          :field-names="{ children: 'children', title: 'name', key: 'id' }" checkable check-strictly
          style="margin-top: 15px;" @check="deptTreeCheck" />
      </div>



      <div class="flex-x-between">
        <div style="width: 10px; background-color: #1677ff;"></div>
        <span style="font-size: 16px;">菜单授权</span>
        <el-input v-model="permKeywords" clearable class="w-[150px]" placeholder="菜单权限名称">
          <template #prefix>
            <Search />
          </template>
        </el-input>

        <div class="flex-center ml-5">
          <el-button type="primary" size="small" plain @click="togglePermTree">
            <template #icon>
              <Switch />
            </template>
            {{ isExpanded ? "收缩" : "展开" }}
          </el-button>
          <el-checkbox v-model="parentChildLinked" class="ml-5" @change="handleparentChildLinkedChange">
            父子联动
          </el-checkbox>

          <el-tooltip placement="bottom">
            <template #content>
              如果只需勾选菜单权限，不需要勾选子菜单或者按钮权限，请关闭父子联动
            </template>
            <el-icon class="ml-1 color-[--el-color-primary] inline-block cursor-pointer">
              <QuestionFilled />
            </el-icon>
          </el-tooltip>
        </div>
      </div>

      <el-tree ref="permTreeRef" node-key="value" show-checkbox :data="menuPermOptions"
        :filter-node-method="handlePermFilter" :default-expand-all="true" :check-strictly="!parentChildLinked"
        class="mt-5">
        <template #default="{ data }">
          {{ data.label }}
        </template>
      </el-tree>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="handleAssignPermSubmit">确 定</el-button>
          <el-button @click="assignPermDialogVisible = false">取 消</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from "element-plus";
import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";

import RoleAPI, { RoleTable, RoleForm, TablePageQuery, permissionDataType, permissionDeptType, permissionMenuType } from "@/api/system/role";
import MenuAPI from "@/api/system/menu";

defineOptions({
  name: "Role",
  inheritAttrs: false,
});

const appStore = useAppStore();

const queryFormRef = ref();
const dataFormRef = ref();
const roleFormRef = ref();
const permTreeRef = ref();
const selectIds = ref<number[]>([]);
const loading = ref(false);
const ids = ref<number[]>([]);
const total = ref(0);
const isExpand = ref(false);
const isExpandable = ref(true);


const permissionState = ref<permissionDataType>({
  role_ids: [],
  menu_ids: [],
  data_scope: 1,
  dept_ids: []
});
const deptTreeData = ref<permissionDeptType[]>([]);
const menuTreeData = ref<permissionMenuType[]>([]);

// 分页表单
const pageTableData = ref<RoleTable[]>([]);

// 菜单权限下拉
const menuPermOptions = ref<OptionType[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: 'selection', label: '选择框', show: true },
  { prop: 'index', label: '序号', show: true },
  { prop: 'name', label: '角色名称', show: true },
  { prop: 'data_scope', label: '数据权限', show: true },
  { prop: 'order', label: '排序', show: true },
  { prop: 'status', label: '状态', show: true },
  { prop: 'description', label: '描述', show: true },
  { prop: 'created_at', label: '创建时间', show: true },
  { prop: 'updated_at', label: '更新时间', show: true },
  { prop: 'operation', label: '操作', show: true }
])

const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "600px" : "90%"));

// 详情表单
const detailFormData = ref<RoleTable>({});

const queryFormData = reactive<TablePageQuery>({
  page_no: 1,
  page_size: 10,
  name: '',
  status: undefined,
  start_time: undefined,
  end_time: undefined,
});

// 新增、编辑表单
const formData = reactive<RoleForm>({
  id: undefined,
  name: undefined,
  order: 1,
  status: true,
  description: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: 'create' as 'create' | 'update' | 'detail',
});

// 表单验证规则
const rules = reactive({
  name: [{ required: true, message: "请输入角色名称", trigger: "blur" }],
  order: [{ required: true, message: "请输入角色排序", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

// 选中的角色
interface CheckedRole {
  id?: number;
  name?: string;
}

const checkedRole = ref<CheckedRole>({});
const assignPermDialogVisible = ref(false);

const permKeywords = ref("");
const isExpanded = ref(true);

const parentChildLinked = ref(true);

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await RoleAPI.getRoleList(queryFormData);
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

// 刷新数据(防抖)
const handleRefresh = useDebounceFn(() => {
  loadingData();
  ElMessage.success("刷新成功");
}, 1000);

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

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
}

// 重置表单
async function resetForm() {
  dataFormRef.value.resetFields();
  dataFormRef.value.clearValidate();
  formData.id = undefined;
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
    const response = await RoleAPI.getRoleDetail({ id });
    if (type === 'detail') {
      dialogVisible.title = "岗位详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === 'update') {
      dialogVisible.title = "修改岗位";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增岗位";
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
          await RoleAPI.updateRole(formData)
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
          await RoleAPI.createRole(formData)
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

// 删除、导入、导出
async function handleOperation(type: 'delete' | 'import' | 'export', id?: number) {
  if (type === 'delete' && !id && !selectIds.value.length) {
    ElMessageBox.confirm("确认删除该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    }).then(async () => {
      try {
        loading.value = true;
        await RoleAPI.deleteRole({ id: id ? id : selectIds.value });
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
          await RoleAPI.uploadFile(formData);
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
    ElMessageBox.confirm('是否确认导出岗位?', '警告', {
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

        const response = await RoleAPI.exportRole(body);
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

// 批量启用/停用
async function handleMoreClick(id: number) {
  if (id && !selectIds.value.length) {
    ElMessageBox.confirm("确认删除启用或停用该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    }).then(async () => {
      try {
        loading.value = true;
        await RoleAPI.batchAvailableRole({ id: id ? id : selectIds.value });
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

// 打开分配菜单权限弹窗
async function handleOpenAssignPermDialog(row: RoleTable) {
  const roleId = row.id;
  if (roleId) {
    assignPermDialogVisible.value = true;
    loading.value = true;

    checkedRole.value.id = roleId;
    checkedRole.value.name = row.name;

    // 获取所有的菜单
    menuPermOptions.value = await MenuAPI.getOptions();

    // 回显角色已拥有的菜单
    RoleAPI.getRoleMenuIds(roleId)
      .then((data) => {
        const checkedMenuIds = data;
        checkedMenuIds.forEach((menuId) => permTreeRef.value!.setChecked(menuId, true, false));
      })
      .finally(() => {
        loading.value = false;
      });
  }
}

// 分配菜单权限提交
function handleAssignPermSubmit() {
  const roleId = checkedRole.value.id;
  if (roleId) {
    const checkedMenuIds: number[] = permTreeRef
      .value!.getCheckedNodes(false, true)
      .map((node: any) => node.value);

    loading.value = true;
    RoleAPI.updateRoleMenus(roleId, checkedMenuIds)
      .then(() => {
        ElMessage.success("分配权限成功");
        assignPermDialogVisible.value = false;
        handleResetQuery();
      })
      .finally(() => {
        loading.value = false;
      });
  }
}

// 展开/收缩 菜单权限树
function togglePermTree() {
  isExpanded.value = !isExpanded.value;
  if (permTreeRef.value) {
    Object.values(permTreeRef.value.store.nodesMap).forEach((node: any) => {
      if (isExpanded.value) {
        node.expand();
      } else {
        node.collapse();
      }
    });
  }
}

// 权限筛选
watch(permKeywords, (val) => {
  permTreeRef.value!.filter(val);
});

function handlePermFilter(
  value: string,
  data: {
    [key: string]: any;
  }
) {
  if (!value) return true;
  return data.label.includes(value);
}

// 父子菜单节点是否联动
function handleparentChildLinkedChange(val: any) {
  parentChildLinked.value = val;
}

onMounted(() => {
  loadingData();
});
</script>

<style lang="scss" scoped></style>
