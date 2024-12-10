<template>
  <div>
    <!-- 页面头部 -->
    <page-header />

    <!-- 表格搜索区域 -->
    <div class="table-search-wrapper">
      <a-card :bordered="false">
        <a-form :model="queryState" @finish="onFinish">
          <a-row>
            <a-col flex="0 1 450px">
              <a-form-item name="username" label="用户名" style="max-width: 300px;">
                <a-input v-model:value="queryState['username']" placeholder="请输入用户名" allowClear></a-input>
              </a-form-item>
            </a-col>
            <a-col flex="0 1 450px">
              <a-form-item name="name" label="姓名" style="max-width: 300px;">
                <a-input v-model:value="queryState['name']" placeholder="请输入姓名" allowClear></a-input>
              </a-form-item>
            </a-col>
            <a-col flex="0 1 450px">
              <a-form-item name="available" label="状态" style="max-width: 300px;">
                <a-select v-model:value="queryState['available']" placeholder="全部" allowClear>
                  <a-select-option value="true">启用</a-select-option>
                  <a-select-option value="false">停用</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>
          <a-row>
            <a-col>
              <a-button type="primary" html-type="submit" :loading="tableLoading">查询</a-button>
              <a-button style="margin: 0 8px" @click="resetFields">重置</a-button>
            </a-col>
          </a-row>
        </a-form>
      </a-card>
    </div>

    <!-- 表格区域 -->
    <div class="table-wrapper">
      <a-card title="用户列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
        :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 400px)' }">
        <template #extra>
          <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')" style="margin-right: 10px;">
            新建
          </a-button>
          <a-button type="primary" :icon="h(UploadOutlined)" @click="modalHandle('import')" style="margin-right: 10px;">
            导入
          </a-button>
          <a-button type="primary" :icon="h(DownOutlined)" @click="handleExport" style="margin-right: 10px;">
            导出
          </a-button>
          <a-dropdown>
            <template #overlay>
              <a-menu @click="handleMoreClick">
                <a-menu-item key="1"><span style="margin-right: 10px;">
                    <CheckOutlined />
                  </span><span>批量启用</span></a-menu-item>
                <a-menu-item key="2"><span style="margin-right: 10px;">
                    <StopOutlined />
                  </span><span>批量停用</span></a-menu-item>
              </a-menu>
            </template>
            <a-button>更多
              <DownOutlined />
            </a-button>
          </a-dropdown>
        </template>
        <a-table :rowKey="record => record.id" :columns="columns" :data-source="dataSource"
          :row-selection="rowSelection" :loading="tableLoading" @change="handleTableChange"
          :scroll="{ x: 500, y: 'calc(100vh - 500px)' }" :pagination="pagination" :style="{ minHeight: '500px' }">
          <template #bodyCell="{ column, record, index }">
            <template v-if="column.dataIndex === 'index'">
              <span>{{ (pagination.current - 1) * pagination.pageSize + index + 1 }}</span>
            </template>
            <template v-if="column.dataIndex === 'name'">
              <span :style="{ color: !record.available ? 'rgb(255, 77, 79)' : 'rgba(0, 0, 0, .88)' }">
                {{ record.name }}
              </span>
            </template>
            <template v-if="column.dataIndex === 'dept'">
              <span>{{ record.dept_name }}</span>
            </template>
            <template v-if="column.dataIndex === 'roles'">
              <span>{{ record.roleNames }}</span>
            </template>
            <template v-if="column.dataIndex === 'positions'">
              <span>{{ record.positionNames }}</span>
            </template>
            <template v-if="column.dataIndex === 'gender'">
              <a-tag :color="record.gender === 1 ? 'blue' : 'pink'">{{ record.gender === 1 ? '男' : '女' }}</a-tag>
            </template>
            <template v-if="column.dataIndex === 'available'">
              <span>
                <a-badge :color="record.available ? 'green' : 'red'" />
                {{ record.available ? '启用' : '禁用' }}
              </span>
            </template>
            <template v-if="column.dataIndex === 'is_superuser'">
              <span>
                <a-badge :color="record.is_superuser ? 'green' : 'red'" />
                {{ record.is_superuser ? '是' : '否' }}
              </span>
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <a-space size="middle">
                <a v-on:click="modalHandle('view', index)">查看</a>
                <a v-on:click="modalHandle('update', index)">修改</a>
                <a-popconfirm title="确定删除吗？" ok-text="确定" cancel-text="取消" @confirm="deleteRow(record)">
                  <a style="color: red;">删除</a>
                </a-popconfirm>
              </a-space>
            </template>
          </template>
        </a-table>
      </a-card>
    </div>

    <!-- 弹窗区域 -->
    <div class="modal-wrapper">
      <a-modal v-model:open="openModal" @ok="handleModalSumbit" :width="800" :destroyOnClose="true"
        :confirmLoading="modalSubmitLoading" style="top: 30px">
        <template #title>
          <span>{{ modalTitle === 'create' ? '新建用户' : (modalTitle === 'view' ? '查看用户' : (modalTitle === 'import' ? '导入用户' : '修改用户')) }}</span>
        </template>
        <div v-if="modalTitle === 'view'">
          <a-spin :spinning="detailStateLoading">
            <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }"
              bordered>
              <a-descriptions-item label="序号">{{ (pagination.current - 1) * pagination.pageSize + detailState.index + 1
                }}</a-descriptions-item>
              <a-descriptions-item label="用户名">{{ detailState.username }}</a-descriptions-item>
              <a-descriptions-item label="姓名">{{ detailState.name }}</a-descriptions-item>
              <a-descriptions-item label="性别">{{ detailState.gender === 1 ? '男' : '女' }}</a-descriptions-item>
              <a-descriptions-item label="部门" :span="2">{{ detailState.dept_name }}</a-descriptions-item>
              <a-descriptions-item label="角色" :span="2">{{ detailState.roleNames }}</a-descriptions-item>
              <a-descriptions-item label="岗位" :span="2">{{ detailState.positionNames }}</a-descriptions-item>
              <a-descriptions-item label="邮箱">{{ detailState.email }}</a-descriptions-item>
              <a-descriptions-item label="联系电话">{{ detailState.mobile }}</a-descriptions-item>
              <a-descriptions-item label="是否超管">
                <a-badge :color="detailState.is_superuser ? 'green' : 'red'" />{{ detailState.is_superuser ? '是' : '否'
                }}
              </a-descriptions-item>
              <a-descriptions-item label="状态">
                <a-badge :color="detailState.available ? 'green' : 'red'" />{{ detailState.available ? '启用' : '禁用' }}
              </a-descriptions-item>
              <a-descriptions-item label="上次登录时间">{{ detailState.last_login }}</a-descriptions-item>
              <a-descriptions-item label="创建人">{{ detailState.creator ? detailState.creator.name : '-'
                }}</a-descriptions-item>
              <a-descriptions-item label="创建时间">{{ detailState.created_at }}</a-descriptions-item>
              <a-descriptions-item label="修改时间">{{ detailState.updated_at }}</a-descriptions-item>
              <a-descriptions-item label="备注" :span="2">{{ detailState.description }}</a-descriptions-item>
            </a-descriptions>
          </a-spin>
        </div>
        <div v-else-if="modalTitle === 'import'">
          <!-- 用户导入对话框 -->
          <a-modal :title="upload.title" v-model:visible="upload.open" width="400px" centered>
            <a-upload ref="uploadRef" 
              :before-upload="beforeUpload" 
              :multiple="false" 
              :accept="'.xlsx, .xls'"
              :headers="upload.headers" 
              :action="upload.url + '?updateSupport=' + upload.updateSupport"
              :disabled="upload.isUploading" 
              :custom-request="customRequest" 
              :show-upload-list="false" drag>
              <p class="ant-upload-drag-icon">
                <upload-outlined />
              </p>
              <p class="ant-upload-text">点击或拖拽文件到此区域上传</p>
              <p class="ant-upload-hint">
                <a-checkbox v-model:checked="upload.updateSupport" /> 是否更新已存在的用户数据
              </p>
              <p class="ant-upload-hint">
                仅允许导入 xls、xlsx 格式的文件。
                <a :href="importUserTemplate" target="_blank"
                  style="font-size: 12px; vertical-align: baseline;">下载模板</a>
              </p>
            </a-upload>
            <template #footer>
              <a-button type="primary" @click="submitFileForm">确 定</a-button>
              <a-button @click="upload.open = false">取 消</a-button>
            </template>
          </a-modal>
        </div>
        <div v-else-if="modalTitle === 'create'">
          <a-form ref="createForm" :model="createState" v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
            <a-form-item name="username" label="用户名" :rules="[{ required: true, message: '请输入用户名' }]">
              <a-input v-model:value="createState.username" placeholder="请输入用户名" allowClear></a-input>
            </a-form-item>
            <a-form-item name="name" label="姓名" :rules="[{ required: true, message: '请输入姓名' }]">
              <a-input v-model:value="createState.name" placeholder="请输入姓名" allowClear></a-input>
            </a-form-item>
            <a-form-item name="dept_id" label="部门" :rules="[{ required: true, message: '请选择部门' }]">
              <a-tree-select v-model:value="createState.dept_id"
                :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }" :tree-data="deptTreeData"
                :field-names="{ children: 'children', label: 'name', value: 'id' }" placeholder="请选择部门"
                tree-node-filter-prop="name" style="width: 100%" show-search allow-clear></a-tree-select>
            </a-form-item>
            <a-form-item name="role_ids" label="角色">
              <a-select v-model:value="createState.roleNames" :open="false" @click="selectModalHandle('role')"
                placeholder="请选择角色">
                <template #suffixIcon>
                  <SearchOutlined />
                </template>
              </a-select>
            </a-form-item>
            <a-form-item name="position_ids" label="岗位">
              <a-select v-model:value="createState.positionNames" :open="false" @click="selectModalHandle('position')"
                placeholder="请选择岗位">
                <template #suffixIcon>
                  <SearchOutlined />
                </template>
              </a-select>
            </a-form-item>
            <a-form-item name="password" label="密码" :rules="[{ required: true, message: '请输入密码' }]">
              <a-input-password v-model:value="createState.password" placeholder="请输入密码" allowClear></a-input-password>
            </a-form-item>
            <a-form-item name="gender" label="性别" :rules="[{ required: true, message: '请选择性别' }]">
              <a-select v-model:value="createState.gender" placeholder="请选择性别" allowClear>
                <a-select-option :value="1">男</a-select-option>
                <a-select-option :value="2">女</a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item name="email" label="邮箱">
              <a-input v-model:value="createState.email" placeholder="请输入邮箱" allowClear></a-input>
            </a-form-item>
            <a-form-item name="mobile" label="联系电话">
              <a-input v-model:value="createState.mobile" placeholder="请输入电话" allowClear></a-input>
            </a-form-item>
            <a-form-item name="is_superuser" label="是否超管" :rules="[{ required: true, message: '请选择是否超管' }]">
              <a-radio-group v-model:value="createState.is_superuser">
                <a-radio :value="true">是</a-radio>
                <a-radio :value="false">否</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item name="available" label="状态" :rules="[{ required: true, message: '请选择状态' }]">
              <a-radio-group v-model:value="createState.available">
                <a-radio :value="true">启用</a-radio>
                <a-radio :value="false">停用</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item name="description" label="备注">
              <a-textarea v-model:value="createState.description" placeholder="请输入备注" :rows="4" allowClear />
            </a-form-item>
          </a-form>
        </div>
        <div v-else>
          <a-form ref="updateForm" :model="updateState" v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
            <a-form-item name="username" label="用户名" :rules="[{ required: true, message: '请输入用户名' }]">
              <a-input v-model:value="updateState.username" placeholder="请输入用户名" allowClear></a-input>
            </a-form-item>
            <a-form-item name="name" label="姓名" :rules="[{ required: true, message: '请输入姓名' }]">
              <a-input v-model:value="updateState.name" placeholder="请输入姓名" allowClear></a-input>
            </a-form-item>
            <a-form-item name="dept_id" label="部门" :rules="[{ required: true, message: '请选择部门' }]">
              <a-tree-select v-model:value="updateState.dept_id"
                :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }" :tree-data="deptTreeData"
                :field-names="{ children: 'children', label: 'name', value: 'id' }" placeholder="请选择部门"
                tree-node-filter-prop="name" style="width: 100%" show-search allow-clear></a-tree-select>
            </a-form-item>
            <a-form-item name="role_ids" label="角色">
              <a-select v-model:value="updateState.roleNames" :open="false" @click="selectModalHandle('role')"
                placeholder="请选择角色">
                <template #suffixIcon>
                  <SearchOutlined />
                </template>
              </a-select>
            </a-form-item>
            <a-form-item name="position_ids" label="岗位">
              <a-select v-model:value="updateState.positionNames" :open="false" @click="selectModalHandle('position')"
                placeholder="请选择岗位">
                <template #suffixIcon>
                  <SearchOutlined />
                </template>
              </a-select>
            </a-form-item>
            <a-form-item v-if="!showPasswordInput" label="修改密码">
              <a-checkbox v-model:checked="showPasswordInput"></a-checkbox>
            </a-form-item>
            <a-form-item v-else name="password" label="密码">
              <a-input-password v-model:value="updateState.password" placeholder="请输入密码" allowClear></a-input-password>
            </a-form-item>
            <a-form-item name="gender" label="性别" :rules="[{ required: true, message: '请选择性别' }]">
              <a-select v-model:value="updateState.gender" placeholder="请选择性别" allowClear>
                <a-select-option :value="1">男</a-select-option>
                <a-select-option :value="2">女</a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item name="email" label="邮箱">
              <a-input v-model:value="updateState.email" placeholder="请输入邮箱" allowClear></a-input>
            </a-form-item>
            <a-form-item name="mobile" label="联系电话">
              <a-input v-model:value="updateState.mobile" placeholder="请输入电话" allowClear></a-input>
            </a-form-item>
            <a-form-item name="is_superuser" label="是否超管" :rules="[{ required: true, message: '请选择是否超管' }]">
              <a-radio-group v-model:value="updateState.is_superuser">
                <a-radio :value="true">是</a-radio>
                <a-radio :value="false">否</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item name="available" label="状态" :rules="[{ required: true, message: '请选择状态' }]">
              <a-radio-group v-model:value="updateState.available">
                <a-radio :value="true">启用</a-radio>
                <a-radio :value="false">停用</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item name="description" label="备注">
              <a-textarea v-model:value="updateState.description" placeholder="请输入备注" :rows="4" allowClear />
            </a-form-item>
          </a-form>
        </div>
      </a-modal>
    </div>

    <!-- 选择器弹窗 -->
    <SelectorModal ref="selectorModal" @event="handleSelectorModalEvent" />
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, unref, onMounted, h } from 'vue';
import { Table, message, Modal } from 'ant-design-vue';
import type { TableColumnsType, MenuProps } from 'ant-design-vue';
import { PlusOutlined, DownOutlined, UploadOutlined, CheckOutlined, StopOutlined, SearchOutlined } from '@ant-design/icons-vue';
import { isEmpty, listToTree } from '@/utils/util';
import PageHeader from '@/components/PageHeader.vue';
import { getDeptList } from '@/api/system/dept'
import { getUserList, createUser, updateUser, deleteUser, batchAvailableUser, exportUser, importUserTemplate, importUserData } from '@/api/system/user'
import SelectorModal from './SelectorModal.vue'
import type { searchDataType, tableDataType, deptTreeType, roleSelectorType, positionSelectorType } from './types'
import XLSX from 'xlsx';
import store from '@/store';
import storage from 'store';

const tableLoading = ref(false);
const openModal = ref(false);
const modalTitle = ref('');
const modalSubmitLoading = ref(false);
const detailStateLoading = ref(false);
const showPasswordInput = ref(false);
const createForm = ref();
const updateForm = ref();
const selectorModal = ref();
const dataSource = ref<tableDataType[]>([]);
const selectedRowKeys = ref<tableDataType['id'][]>([]);
const deptTreeData = ref<deptTreeType[]>([]);

const queryState = reactive<searchDataType>({
  username: null,
  name: null,
  available: null
});
const pagination = reactive({
  current: 1,
  pageSize: 10,
  defaultPageSize: 10,
  showSizeChanger: true,
  total: dataSource.value.length,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})
const createState = reactive<tableDataType>({
  username: '',
  name: '',
  dept_id: undefined,
  dept_name: '',
  role_ids: undefined,
  roleNames: undefined,
  position_ids: undefined,
  positionNames: undefined,
  password: '',
  gender: undefined,
  email: '',
  mobile: '',
  is_superuser: false,
  available: true,
  description: ''
})
const updateState = reactive<tableDataType>({
  id: undefined,
  username: '',
  name: '',
  dept_id: undefined,
  dept_name: '',
  role_ids: [],
  roleNames: undefined,
  position_ids: [],
  positionNames: undefined,
  password: '',
  gender: undefined,
  email: '',
  mobile: '',
  is_superuser: false,
  available: true,
  description: '',
})
const detailState = ref<tableDataType>({});

const columns = reactive<TableColumnsType>([
  {
    title: '序号',
    dataIndex: 'index',
    align: 'center',
    ellipsis: true,
    width: 80
  },
  {
    title: '用户名',
    dataIndex: 'username',
    ellipsis: true,
    align: 'center',
    width: 100
  },
  {
    title: '姓名',
    dataIndex: 'name',
    ellipsis: true,
    align: 'center',
    width: 80
  },
  {
    title: '是否超管',
    dataIndex: 'is_superuser',
    align: 'center',
    ellipsis: true,
    width: 100
  },
  {
    title: '部门',
    dataIndex: 'dept',
    ellipsis: true,
    align: 'center',
    width: 100
  },
  {
    title: '角色',
    dataIndex: 'roles',
    ellipsis: true,
    align: 'center',
    width: 100
  },
  {
    title: '岗位',
    dataIndex: 'positions',
    ellipsis: true,
    align: 'center',
    width: 100
  },
  {
    title: '邮箱',
    dataIndex: 'email',
    ellipsis: true,
    align: 'center',
    width: 160
  },
  {
    title: '联系电话',
    dataIndex: 'mobile',
    align: 'center',
    ellipsis: true,
    width: 120
  },
  {
    title: '性别',
    dataIndex: 'gender',
    align: 'center',
    ellipsis: true,
    width: 100
  },
  {
    title: '状态',
    dataIndex: 'available',
    align: 'center',
    ellipsis: true,
    width: 100
  },
  {
    title: '备注',
    dataIndex: 'description',
    ellipsis: true,
    align: 'center',
    // width: 200
  },
  {
    title: '操作',
    dataIndex: 'operation',
    fixed: 'right',
    ellipsis: true,
    align: 'center',
    width: 150
  }
]);

const rowSelection = computed(() => {
  return {
    selectedRowKeys: unref(selectedRowKeys),
    onChange: (selectingRowKeys: tableDataType['id'][]) => {
      selectedRowKeys.value = selectingRowKeys;
    },
    hideDefaultSelections: true,
    selections: [
      Table.SELECTION_ALL,
      Table.SELECTION_INVERT,
      Table.SELECTION_NONE
    ]
  }
});

// 生命周期钩子
onMounted(() => loadingData());

// 查询
const onFinish = () => {
  pagination.current = 1;
  loadingData();
};

// 加载表格数据
const loadingData = () => {
  tableLoading.value = true;

  let params = {};
  if (queryState.username) {
    params['username'] = queryState.username
  }
  if (queryState.name) {
    params['name'] = queryState.name
  }
  if (queryState.available) {
    params['available'] = queryState.available == "true" ? true : false;
  }
  params['page_no'] = pagination.current
  params['page_size'] = pagination.pageSize

  getDeptList().then(response => {
    const result = response.data;
    deptTreeData.value = listToTree(result.data.items);
  })

  getUserList(params).then(response => {
    const result = response.data;
    dataSource.value = result.data.items.map((item: tableDataType) => {
      item.roleNames = item.roles ? item.roles.map(item => item.name).join("，") : undefined;
      item.positionNames = item.positions ? item.positions.map(item => item.name).join("，") : undefined;
      return item;
    });
    pagination.total = result.data.total;
    pagination.current = result.data.page_no;
    pagination.pageSize = result.data.page_size;
  }).catch(error => {
    console.log(error);
  }).finally(() => {
    tableLoading.value = false;
  });
}

// 重置查询
const resetFields = () => {
  Object.keys(queryState).forEach((key: string) => {
    delete queryState[key];
  });
  pagination.current = 1;
  queryState.available = null
  loadingData();
}

// 删除
const deleteRow = (row: tableDataType) => {
  deleteUser({ id: row.id }).then(response => {
    const result = response.data;
    message.success(result.msg);
    loadingData();

  }).catch(error => {
    console.log(error);
  })
}

// 批量启用/停用
const handleMoreClick: MenuProps['onClick'] = e => {
  if (!selectedRowKeys.value || !(selectedRowKeys.value.length > 0)) {
    message.warning('请先勾选数据');
    return;
  }

  Modal.confirm({
    title: '提示',
    content: e.key == 1 ? '是否确定启用选择项？' : '是否确定停用选择项？',
    onOk() {
      const body = { ids: selectedRowKeys.value, available: e.key == 1 ? true : false };
      batchAvailableUser(body).then(response => {
        const result = response.data;
        message.success(result.msg);
        selectedRowKeys.value = [];
        loadingData();
      }).catch(error => {
        console.log(error);
      })
    }
  });
}

// 表格分页
const handleTableChange = (values: any) => {
  pagination.current = values.current;
  pagination.pageSize = values.pageSize;
  loadingData();
}

// 弹窗关键字处理
const modalHandle = (modalType: string, index?: number) => {
  modalTitle.value = modalType;
  openModal.value = true;

  if (modalType === 'view' && index !== undefined) {
    detailStateLoading.value = true;

    detailState.value = dataSource.value[index];
    detailState.value.index = index;

    detailStateLoading.value = false;

  } else if (modalType === 'update' && index !== undefined) {
    const selected = dataSource.value[index];

    Object.keys(updateState).forEach(key => {
      if (selected[key] !== undefined) {
        updateState[key] = selected[key];
      }
    })

    if (selected['roles']) {
      updateState.role_ids = selected.roles.map(role => role.id);
    }
    if (selected['positions']) {
      updateState.position_ids = selected.positions.map(position => position.id);
    }
  }else if (modalType === 'import' && index !== undefined) {
    
  }
}

// 弹窗提交（详情/新建/修改）
const handleModalSumbit = () => {
  modalSubmitLoading.value = true;

  if (modalTitle.value === 'view') {
    modalSubmitLoading.value = false;
    openModal.value = false;

  } else if (modalTitle.value === 'create') {
    createForm.value.validate().then(() => {
      const createBody = {
        username: createState.username,
        name: createState.name,
        password: createState.password,
        dept_id: createState.dept_id,
        role_ids: createState.role_ids,
        position_ids: createState.position_ids,
        gender: createState.gender,
        email: createState.email,
        mobile: createState.mobile,
        available: createState.available,
        description: createState.description,
        is_superuser: createState.is_superuser
      }
      Object.keys(createBody).forEach(key => {
        if (isEmpty(createBody[key])) {
          delete createBody[key];
        }
      })

      createUser(createBody).then(response => {
        const result = response.data;
        modalSubmitLoading.value = false;
        openModal.value = false;
        Object.keys(createState).forEach(key => delete createState[key]);
        message.success(result.msg);
        loadingData();

      }).catch(error => {
        modalSubmitLoading.value = false;
        console.error(error);
      })

    }).catch(error => {
      modalSubmitLoading.value = false;
      console.error(error);
    })

  } else if (modalTitle.value === 'update') {
    updateForm.value.validate().then(() => {
      const updateBody = {
        id: updateState.id,
        username: updateState.username,
        name: updateState.name,
        dept_id: updateState.dept_id,
        role_ids: updateState.role_ids,
        position_ids: updateState.position_ids,
        gender: updateState.gender,
        email: updateState.email,
        mobile: updateState.mobile,
        available: updateState.available,
        description: updateState.description,
        is_superuser: updateState.is_superuser
      }
      if (showPasswordInput.value && updateState.password) {
        updateBody['password'] = updateState.password;
      }

      updateUser(updateBody).then(response => {
        const result = response.data;
        modalSubmitLoading.value = false;
        openModal.value = false;
        message.success(result.msg);
        loadingData();

      }).catch(error => {
        modalSubmitLoading.value = false;
        console.error(error)
      })

    }).catch(error => {
      modalSubmitLoading.value = false;
      console.error(error)
    })
  } else if (modalTitle.value === 'import') {

  }
}

// 选择器弹窗
const selectModalHandle = (subject: string) => {
  selectorModal.value.subject = subject;
  selectorModal.value.openModal = true;

  const ids_key = subject === 'role' ? 'role_ids' : 'position_ids';
  const names_key = subject === 'role' ? 'roleNames' : 'positionNames';

  const selectedKeys = modalTitle.value === 'create' ? createState[ids_key] : updateState[ids_key];
  const selectedRowItemNames = modalTitle.value === 'create' ? (createState[names_key] ?? '') : (updateState[names_key] ?? '');

  selectorModal.value.selectedRowKeys = selectedKeys;
  selectorModal.value.selectedRowItemNames = selectedRowItemNames.split(', ');

  selectorModal.value.loadingData();
}

// 选择器弹窗事件
const handleSelectorModalEvent = (
  subject: string,
  selectedSelectorRowKeys: roleSelectorType['id'][] | positionSelectorType['id'][],
  selectedSelectorRowNames: roleSelectorType['name'][] | positionSelectorType['name'][]
) => {
  const ids_key = subject === 'role' ? 'role_ids' : 'position_ids';
  const names_key = subject === 'role' ? 'roleNames' : 'positionNames';

  if (modalTitle.value === 'create') {
    createState[ids_key] = selectedSelectorRowKeys;
    createState[names_key] = selectedSelectorRowNames.join(', ');
  } else {
    updateState[ids_key] = selectedSelectorRowKeys;
    updateState[names_key] = selectedSelectorRowNames.join(', ');
  }
}

// 上传头像配置
const token = storage.get('Access-Token');

// 用户导入参数
const upload = reactive({
  title: '用户导入',
  open: false,
  headers: token ? { Authorization: 'Bearer ' + token } : {},
  url: importUserData, // 假设这是上传接口地址
  // url: import.meta.env.VITE_APP_BASE_API + "/system/user/import/data",
  isUploading: false,
  updateSupport: false,
});


// 导出按钮操作
const handleExport = () => {
  // 构建查询参数
  const params = {
    ...queryState,
    page_no: 1,
    page_size: pagination.total // 导出所有数据
  };

  // 调用 exportLog 接口
  exportUser(params).then(response => {
    const blob = new Blob([response.data], { type: 'application/vnd.ms-excel' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `user_${new Date().getTime()}.xlsx`; // 设置下载文件名
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    message.success('导出成功');
  }).catch(error => {
    console.error('导出失败:', error);
    message.error('导出失败');
  });
};

// 下载模板
const downloadTemplate = () => {
  window.location.href = importUserTemplate; // 假设这是模板下载地址
};

// 导入
const beforeUpload = (file: File) => {
  const isExcel = file.type === 'application/vnd.ms-excel' || file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
  if (!isExcel) {
    message.error('只能上传 Excel 文件!');
  }
  return isExcel;
};
const customRequest = ({ file, onSuccess, onError }: any) => {
  upload.isUploading = true;
  const formData = new FormData();
  formData.append('file', file);
  formData.append('updateSupport', upload.updateSupport.toString());
  importUserData(formData)
    .then((response) => {
      upload.isUploading = false;
      upload.open = false;
      message.success('用户导入成功');
      onSuccess(response);
      loadingData(); // 刷新数据
    })
    .catch((error) => {
      upload.isUploading = false;
      onError(error);
      message.error('用户导入失败');
    });
};
/** 提交上传文件 */
const submitFileForm = () => {
  uploadRef.value.upload();
};
</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}
</style>