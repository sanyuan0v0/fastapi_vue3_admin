<!-- 用户管理 -->
<template>
  <div class="app-container">
    <el-row :gutter="12">
      <!-- 部门树 -->
      <el-col :lg="4" :xs="24">
        <DeptTree v-model="queryFormData.dept_id" class="h-full" @node-click="handleQuery"  />
      </el-col>

      <!-- 用户列表 -->
      <el-col :lg="20" :xs="24">
        <!-- 搜索区域 -->
        <div class="search-container">
          <el-form ref="queryFormRef" :model="queryFormData" :inline="true">
            <el-form-item prop="username" label="账号">
              <el-input v-model="queryFormData.username" placeholder="请输入账号" clearable />
            </el-form-item>
            <el-form-item prop="name" label="姓名">
              <el-input v-model="queryFormData.name" placeholder="请输入姓名" clearable />
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

        <el-card shadow="hover" class="data-table">
          <template #header>
            <div class="card-header">
              <span>
                <el-tooltip content="用户管理系统用户">
                  <QuestionFilled class="w-4 h-4 mx-1" />
                </el-tooltip>
                用户列表
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
              <el-tooltip content="导入">
                <!-- <el-button type="info" icon="upload" circle @click="handleOperation('import')" /> -->
                <el-button type="info" icon="upload" circle @click="handleOpenImportDialog" />
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

          <!-- 表格区域 -->
          <el-table ref="dataTableRef" v-loading="loading" :data="pageTableData" highlight-current-row class="data-table__content" height="450" border stripe @selection-change="handleSelectionChange">
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column v-if="tableColumns.find(col => col.prop === 'selection')?.show" type="selection" min-width="55" align="center" />
            <el-table-column v-if="tableColumns.find(col => col.prop === 'index')?.show" type="index" fixed label="序号" align="center" min-width="60" >
              <template #default="scope">
                {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column v-if="tableColumns.find(col => col.prop === 'avatar')?.show" label="头像" prop="avatar" min-width="80" align="center">
              <template #default="scope">
                <el-avatar size="small" :src="scope.row.avatar" />
              </template>
            </el-table-column>
            <el-table-column v-if="tableColumns.find(col => col.prop === 'username')?.show" label="账号" prop="username" min-width="100" />
            <el-table-column v-if="tableColumns.find(col => col.prop === 'name')?.show" label="用户名" prop="name" min-width="100" />
            <el-table-column v-if="tableColumns.find(col => col.prop === 'status')?.show" label="状态" prop="status" min-width="100">
              <template #default="scope">
                <el-tag :type="scope.row.status === true ? 'success' : 'danger'">
                  {{ scope.row.status === true ? "启用" : "停用" }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column v-if="tableColumns.find(col => col.prop === 'is_superuser')?.show" label="是否超管" prop="is_superuser" min-width="100">
              <template #default="scope">
                <el-tag :type="scope.row.is_superuser ? 'success' : 'info'">
                  {{ scope.row.is_superuser ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column v-if="tableColumns.find(col => col.prop === 'gender')?.show" label="性别" min-width="100">
              <template #default="scope">
                <el-tag v-if="scope.row.gender ==='0'" type="success">男</el-tag>
                <el-tag v-else-if="scope.row.gender ==='1'" type="warning">女</el-tag>
                <el-tag v-else type="info">未知</el-tag>
              </template>
            </el-table-column>

            <el-table-column v-if="tableColumns.find(col => col.prop === 'mobile')?.show" label="手机号" prop="mobile" min-width="160" />
            <el-table-column v-if="tableColumns.find(col => col.prop === 'email')?.show" label="邮箱" prop="email" min-width="160" />
            <el-table-column v-if="tableColumns.find(col => col.prop === 'created_at')?.show" label="创建时间" prop="created_at" min-width="200" />
            <el-table-column v-if="tableColumns.find(col => col.prop === 'updated_at')?.show" label="更新时间" prop="updated_at" min-width="200" />
            <el-table-column v-if="tableColumns.find(col => col.prop === 'creator')?.show" key="creator" label="创建人" min-width="120">
              <template #default="scope">
                {{ scope.row.creator?.name }}
              </template>
            </el-table-column>
            <el-table-column v-if="tableColumns.find(col => col.prop === 'operation')?.show" fixed="right" label="操作" align="center" min-width="280">
              <template #default="scope">
                <el-button type="warning" icon="RefreshLeft" size="small" link @click="hancleResetPassword(scope.row)">重置密码</el-button>
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
      </el-col>
    </el-row>

    <!-- 弹窗区域 -->
    <el-drawer v-model="dialogVisible.visible" :title="dialogVisible.title" append-to-body :size="drawerSize" @close="handleCloseDialog">
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="编号" :span="2">{{ detailFormData.id }}</el-descriptions-item>
          <el-descriptions-item label="头像" :span="2">
            <el-avatar :src="detailFormData.avatar" size="small"></el-avatar>
          </el-descriptions-item>
          <el-descriptions-item label="账号" :span="2">{{ detailFormData.username }}</el-descriptions-item>
          <el-descriptions-item label="用户名" :span="2">{{ detailFormData.name }}</el-descriptions-item>
          <el-descriptions-item label="性别" :span="2">
            <el-tag v-if="detailFormData.gender ==='0'" type="success">男</el-tag>
            <el-tag v-else-if="detailFormData.gender ==='1'" type="warning">女</el-tag>
            <el-tag v-else type="info">未知</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="部门" :span="2">{{ detailFormData.dept_name }}</el-descriptions-item>
          <el-descriptions-item label="角色" :span="2">{{ detailFormData.roles ? detailFormData.roles.map(item => item.name).join('、') : '' }}</el-descriptions-item>
          <el-descriptions-item label="岗位" :span="2">{{ detailFormData.positions ? detailFormData.positions.map(item => item.name).join('、') : '' }}</el-descriptions-item>  
          <el-descriptions-item label="邮箱" :span="2">{{ detailFormData.email }}</el-descriptions-item>
          <el-descriptions-item label="手机号" :span="2">{{ detailFormData.mobile }}</el-descriptions-item>
          <el-descriptions-item label="是否超管" :span="2">
            <el-tag :type="detailFormData.is_superuser ? 'success' : 'info'">
              {{ detailFormData.is_superuser ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="detailFormData.status ? 'success' : 'danger'">
              {{ detailFormData.status ? '启用' : '停用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="上次登录时间" :span="2">{{ detailFormData.last_login }}</el-descriptions-item>
          <el-descriptions-item label="创建人" :span="2">{{ detailFormData.creator?.name }}</el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">{{ detailFormData.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">{{ detailFormData.updated_at }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="4">{{ detailFormData.description }}</el-descriptions-item>
        </el-descriptions>
      </template>
      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form ref="dataFormRef" :model="formData" :rules="rules" label-width="80px">
          <el-form-item label="账号" prop="username">
            <el-input v-model="formData.username" :readonly="!!formData.id" placeholder="请输入账号" />
          </el-form-item>

          <el-form-item label="用户名" prop="name">
            <el-input v-model="formData.name" placeholder="请输入用户名" />
          </el-form-item>

          <el-form-item label="性别" prop="gender">
            <el-select v-model="formData.gender" placeholder="请选择性别">
              <el-option label="男" value="0" />
              <el-option label="女" value="1" />
              <el-option label="未知" value="2" />
            </el-select>
          </el-form-item>

          <el-form-item label="手机号码" prop="mobile">
            <el-input v-model="formData.mobile" placeholder="请输入手机号码" maxlength="11" />
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input v-model="formData.email" placeholder="请输入邮箱" maxlength="50" />
          </el-form-item>

          <el-form-item label="部门" prop="dept_id">
            <el-tree-select v-model="formData.dept_id" placeholder="请选择上级部门" :data="deptOptions" filterable check-strictly :render-after-expand="false" />
          </el-form-item>

          <el-form-item label="角色" prop="role_ids">
            <el-select v-model="formData.role_ids" multiple placeholder="请选择角色">
              <el-option v-for="item in roleOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>

          <el-form-item label="岗位" prop="position_ids">
            <el-select v-model="formData.position_ids" multiple placeholder="请选择岗位">
              <el-option v-for="item in positionOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input v-model="formData.password" placeholder="请输入密码" type="password" show-password clearable />
          </el-form-item>

          <el-form-item label="是否超管" prop="is_superuser">
            <el-switch v-model="formData.is_superuser" />
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

          <template #footer>
            <div class="dialog-footer">
              <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
              <el-button v-if="dialogVisible.type === 'create' || dialogVisible.type === 'update'" type="primary" @click="handleSubmit">确定</el-button>
              <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
              <el-button @click="handleCloseDialog">取消</el-button>
            </div>
          </template>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="handleSubmit">确 定</el-button>
          <el-button @click="handleCloseDialog">取 消</el-button>
        </div>
      </template>
    </el-drawer>

    <!-- 用户导入 -->
    <UserImport v-model="importDialogVisible" @import-success="handleQuery()" />

  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "User",
  inheritAttrs: false,
});

import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { ElMessage, ElMessageBox } from "element-plus";

import UserAPI, { type UserForm, type UserInfo, type UserPageQuery } from "@/api/system/user";
import { listToTree, formatTree } from "@/utils/common";
import PositionAPI from "@/api/system/position";
import DeptAPI from "@/api/system/dept";
import RoleAPI from "@/api/system/role";

import DeptTree from "./components/DeptTree.vue";
import UserImport from "./components/UserImport.vue";

const appStore = useAppStore();

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const loading = ref(false);
const isExpand = ref(false);
const isExpandable = ref(true);
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "450px" : "90%"));
// 选中的用户ID
const selectIds = ref<number[]>([]);
// 部门下拉数据源
const deptOptions = ref<OptionType[]>();
// 角色下拉数据源
const roleOptions = ref<OptionType[]>();
// 岗位下拉数据源
const positionOptions = ref<OptionType[]>();
// 导入弹窗显示状态
const importDialogVisible = ref(false);
// 分页表单
const pageTableData = ref<UserInfo[]>([]);
// 详情表单
const detailFormData = ref<UserInfo>({});

// 表格列配置
const tableColumns = ref([
  { prop: 'selection', label: '选择框', show: true },
  { prop: 'index', label: '序号', show: true },
  { prop: 'avatar', label: '头像', show: true },
  { prop: 'username', label: '账号', show: true },
  { prop: 'name', label: '用户名', show: true },
  { prop: 'gender', label: '性别', show: true },
  { prop: 'email', label: '邮箱', show: true },
  { prop: 'mobile', label: '手机号', show: true },
  { prop: 'is_superuser', label: '是否超管', show: true },
  { prop: 'status', label: '状态', show: true },
  { prop: 'description', label: '描述', show: true },
  { prop: 'created_at', label: '创建时间', show: true },
  { prop: 'updated_at', label: '更新时间', show: true },
  { prop: 'creator', label: '创建人', show: true },
  { prop: 'operation', label: '操作', show: true }
])

// 分页查询参数
const queryFormData = reactive<UserPageQuery>({
  page_no: 1,
  page_size: 10,
  username: undefined,
  name: undefined,
  status: undefined,
  dept_id: undefined,
  start_time: undefined,
  end_time: undefined,
});

// 表单
const formData = reactive<UserForm>({
  id: undefined,
  username: undefined,
  name: undefined,
  dept_id: undefined,
  dept_name: undefined,
  role_ids: undefined,
  roleNames: undefined,
  position_ids: undefined,
  positionNames: undefined,
  password: undefined,
  gender: undefined,
  email: undefined,
  mobile: undefined,
  is_superuser: undefined,
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
  username: [{ required: true, message: "请输入账号", trigger: "blur" }],
  name: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
  gender: [{ required: true, message: "请选择性别", trigger: "blur" }],
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    {
      pattern: /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/,
      message: "请输入正确的邮箱地址",
      trigger: "blur",
    },
  ],
  mobile: [
    { required: true, message: "请输入手机号", trigger: "blur" },
    {
      pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/,
      message: "请输入正确的手机号码",
      trigger: "blur",
    },
  ],
  is_superuser: [{ required: true, message: "请选择是否超管", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

// 列表刷新
async function handleRefresh () {
  await loadingData();
};

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await UserAPI.getUserList(queryFormData);
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

// 选中项发生变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
}

// 重置密码
function hancleResetPassword(row: UserInfo) {
  ElMessageBox.prompt("请输入用户【" + row.username + "】的新密码", "重置密码", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
  }).then(
    ({ value }) => {
      if (!value || value.length < 6) {
        ElMessage.warning("密码至少需要6位字符，请重新输入");
        return false;
      }
      UserAPI.resetUserPassword({id: row.id!, password: value}).then(() => {
        ElMessage.success("密码重置成功，新密码是：" + value);
      });
    },
    () => {
      ElMessage.info("已取消重置密码");
    }
  );
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开弹窗
async function handleOpenDialog(type: 'create' | 'update' | 'detail', id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await UserAPI.getUserDetail(id);
    if (type === 'detail') {
      dialogVisible.title = "用户详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === 'update') {
      dialogVisible.title = "修改用户";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增用户";
    formData.id = undefined;
  }
  dialogVisible.visible = true;

  // 获取部门树
  const deptResponse = await DeptAPI.getDeptList(queryFormData);
  const treeData = listToTree(deptResponse.data.data.items);
  deptOptions.value = formatTree(treeData);

  // 获取角色列表
  const roleResponse = await RoleAPI.getRoleList();
  roleOptions.value = roleResponse.data.data.items
    .filter(item => item.id !== undefined && item.name !== undefined)
    .map(item => ({
      value: item.id as number,
      label: item.name as string
    }));

  // 获取岗位列表
  const positionResponse = await PositionAPI.getPositionList();
  positionOptions.value = positionResponse.data.data.items
    .filter(item => item.id !== undefined && item.name !== undefined)
    .map(item => ({
      value: item.id as number,
      label: item.name as string
    }));
}

// 提交表单（防抖）
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await UserAPI.updateUser({ id, ...formData })
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          ElMessage.error(error.message);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await UserAPI.createUser(formData)
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
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
async function handleOperation(type: 'import' | 'export') {
  if (type === 'import') {
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
          await UserAPI.importUser(formData);
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
    ElMessageBox.confirm('是否确认导出当前查询结果用户数据?', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      try {
        loading.value = true;

        ElMessage.warning('正在导出数据，请稍候...');

        UserAPI.exportUser(queryFormData).then((response: any) => {
          // const fileData = JSON.stringify(response.data.data;
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
          ElMessage.success('导出成功');
          document.body.removeChild(downloadLink);
          window.URL.revokeObjectURL(downloadUrl);
        });

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

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(async () => {
    try {
      loading.value = true;
      await UserAPI.deleteUser(ids);
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

// 批量启用/停用
async function handleMoreClick(status: boolean) {
  if (selectIds.value.length) {
    ElMessageBox.confirm("确认启用或停用该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    }).then(async () => {
      try {
        loading.value = true;
        await UserAPI.batchAvailableUser({ ids: selectIds.value, status });
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

// 打开导入弹窗
function handleOpenImportDialog() {
  importDialogVisible.value = true;
}


onMounted(() => {
  handleQuery();
});
</script>
