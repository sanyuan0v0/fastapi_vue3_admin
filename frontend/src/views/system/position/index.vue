<template>
  <div>


    <!-- 搜索表单 -->
    <div class="table-search-wrapper">
      <a-card :bordered="false">
        <a-form :model="queryState" @finish="onFinish">
          <a-flex wrap="wrap" gap="small">
              <a-form-item name="name" label="名称" >
                <a-input v-model:value="queryState.name" placeholder="请输入名称" allowClear></a-input>
              </a-form-item>
              <a-form-item name="available" label="状态" >
                <a-select v-model:value="queryState.available" placeholder="请选择状态" allowClear>
                  <a-select-option value="true">启用</a-select-option>
                  <a-select-option value="false">停用</a-select-option>
                </a-select>
              </a-form-item>
          </a-flex>
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
      <a-card title="岗位列表"
        :bordered="false"
        :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
      :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 360px)' }">
        <template #extra>
          <a-button type="primary"
            :icon="h(PlusOutlined)"
            @click="modalHandle('create')"
            style="margin-right: 10px;">
            新建
          </a-button>
          <a-button type="primary" :icon="h(DownOutlined)" @click="handleExport"
            style="margin-right: 10px;">
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
        <a-table :rowKey="record => record.id"
          :columns="columns"
          :data-source="dataSource"
          :row-selection="rowSelection"
          :loading="tableLoading"
          @change="handleTableChange"
          :scroll="{ x: 400 }"
          :pagination="pagination"
                    :style="{ minHeight: 'calc(100vh - 420px)' }"
                    >
          <template #bodyCell="{ column, record, index }">
            <template v-if="column.dataIndex === 'index'">
              <span>{{ (pagination.current - 1) * pagination.pageSize + index + 1 }}</span>
            </template>
            <template v-if="column.dataIndex === 'available'">
              <span>
                <a-badge :status="record.available ? 'processing': 'error'" :text="record.available ? '启用' : '停用'" />
              </span>
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <a-space size="middle">
                <a @click="modalHandle('view', index)">查看</a>
                <a @click="modalHandle('update', index)">修改</a>
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
      <a-modal
        v-model:open="openModal"
        @ok="handleModalSumbit"
        :width="800"
        :destroyOnClose="true"
        :confirmLoading="modalSubmitLoading"
        style="top: 30px"
      >
        <template #title>
          <span>{{ modalTitle === 'create' ? '新建岗位' : (modalTitle === 'view' ? '查看岗位' : '修改岗位') }}</span>
        </template>
        <div v-if="modalTitle === 'view'">
          <a-spin :spinning="detailStateLoading">
            <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }"
              bordered>
              <a-descriptions-item label="序号">{{ (pagination.current - 1) * pagination.pageSize + detailState.index + 1 }}</a-descriptions-item>
              <a-descriptions-item label="名称">{{ detailState.name }}</a-descriptions-item>
              <a-descriptions-item label="排序">{{ detailState.order }}</a-descriptions-item>
              <a-descriptions-item label="状态">
                <a-badge :status="detailState.available ? 'processing': 'error'" :text="detailState.available ? '启用' : '停用'" />
              </a-descriptions-item>
              <a-descriptions-item label="创建人">{{ detailState.creator ? detailState.creator.name : '-' }}</a-descriptions-item>
              <a-descriptions-item label="创建时间">{{ detailState.created_at }}</a-descriptions-item>
              <a-descriptions-item label="修改时间">{{ detailState.updated_at }}</a-descriptions-item>
              <a-descriptions-item label="备注" :span="2">{{ detailState.description }}</a-descriptions-item>
            </a-descriptions>
          </a-spin>
        </div>
        <div v-else-if="modalTitle === 'create'">
          <a-form ref="createForm" :model="createState" v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
            <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
              <a-input v-model:value="createState.name" placeholder="请输入名称" allowClear></a-input>
            </a-form-item>
            <a-form-item name="order" label="排序" :rules="[{ required: true, message: '请输入排序' }]">
              <a-input-number v-model:value="createState.order" :min="1" style="width: 100%"/>
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
            <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
              <a-input v-model:value="updateState.name" placeholder="请输入名称" allowClear></a-input>
            </a-form-item>
            <a-form-item name="order" label="排序" :rules="[{ required: true, message: '请输入排序' }]">
              <a-input-number v-model:value="updateState.order" :min="1" style="width: 100%"/>
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
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, unref, onMounted, h } from 'vue';
import { Table, message, Modal } from 'ant-design-vue';
import type { TableColumnsType, MenuProps } from 'ant-design-vue';
import { PlusOutlined, DownOutlined, CheckOutlined, StopOutlined } from '@ant-design/icons-vue';
import { cloneDeep, isEmpty } from '@/utils/util';
import { getPositionList, createPosition, updatePosition, deletePosition, batchAvailablePosition, exportPosition } from '@/api/system/position'
import type { searchDataType, tableDataType } from './types'

const createForm = ref();
const updateForm = ref();
const tableLoading = ref(false);
const openModal = ref(false);
const modalTitle = ref('');
const modalSubmitLoading = ref(false);
const detailStateLoading = ref(false);
const dataSource = ref<tableDataType[]>([]);
const selectedRowKeys = ref<tableDataType['id'][]>([]);

const queryState = reactive<searchDataType>({
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
  name: '',
  order: 1,
  available: true,
  description: ''
})
const updateState = reactive<tableDataType>({
  id: undefined,
  name: '',
  order: 1,
  available: true,
  description: ''
})
const detailState = ref<tableDataType>({})

const columns: TableColumnsType = [
  {
    title: '序号',
    dataIndex: 'index',
    align: 'center',
    ellipsis: true,
    width: 80
  },
  {
    title: '名称',
    dataIndex: 'name',
    ellipsis: true,
    // align: 'center'
  },
  {
    title: '排序',
    dataIndex: 'order',
    ellipsis: true,
    // align: 'center'
  },
  {
    title: '状态',
    dataIndex: 'available',
    ellipsis: true,
    // align: 'center'
  },
  {
    title: '备注',
    dataIndex: 'description',
    // align: 'center',
    ellipsis: true,
    // width: 500
  },
  {
    title: '创建日期',
    dataIndex: 'created_at',
    // align: 'center',
    ellipsis: true,
    width: 200
  },
  {
    title: '更新日期',
    dataIndex: 'updated_at',
    // align: 'center',
    ellipsis: true,
    width: 200
  },
  {
    title: '操作',
    dataIndex: 'operation',
    align: 'center',
    fixed: 'right',
    width: 150
  }
];

// 表格选中配置
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

// 加载表格数据
const loadingData = () => {
  tableLoading.value = true;

  let params = {};
  if (queryState.name) {
    params['name'] = queryState.name
  }
  if (queryState.available !== null && queryState.available !== undefined) {
    params['available'] = queryState.available;
  }
  params['page_no'] = pagination.current
  params['page_size'] = pagination.pageSize

  getPositionList(params).then(response => {
    const result = response.data;
    dataSource.value = result.data.items;
    pagination.total = result.data.total;
    pagination.current = result.data.page_no;
    pagination.pageSize = result.data.page_size;
  }).catch(error => {
    console.log(error);
  }).finally(() => {
    tableLoading.value = false;
  });
}

// 生命周期钩子
onMounted(() => loadingData());

// 查询
const onFinish = () => {
  pagination.current = 1;
  loadingData();
};

// 重置查询
const resetFields = () => {
  Object.keys(queryState).forEach((key: string) => {
    delete queryState[key];
  });
  pagination.current = 1;
  queryState.available = null
  loadingData();
}

// 表格分页处理
const handleTableChange = (values: any) => {
  pagination.current = values.current;
  pagination.pageSize = values.pageSize;
  loadingData();
}

// 弹窗关键字处理
const modalHandle = (modalType: string, index?: number) => {
  modalTitle.value = modalType;
  openModal.value = true;

  // 重新创建 createState 和 updateState 以重置为初始状态
  Object.assign(createState, {
    name: '',
    order: 1,
    available: true,
    description: ''
  });

  Object.assign(updateState, {
    id: undefined,
    name: '',
    order: 1,
    available: true,
    description: ''
  });

  if (modalType === 'view' && index !== undefined) {
    detailStateLoading.value = true;

    detailState.value = dataSource.value[index];
    detailState.value.index = index;

    detailStateLoading.value = false;

  } else if (modalType === 'update' && index !== undefined) {
    const selected = dataSource.value[index];
    Object.keys(updateState).forEach(key => {
      updateState[key] = selected[key];
    })
  }
}

// 删除
const deleteRow = (row: tableDataType) => {
  deletePosition({ id: row.id }).then(response => {
    const result = response.data;
    message.success(result.msg);
    loadingData();
  }).catch(error => {
    console.log(error)
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
      batchAvailablePosition(body).then(response => {
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

// 弹窗提交（详情/新建/修改）
const handleModalSumbit = () => {
  modalSubmitLoading.value = true;

  if (modalTitle.value === 'view') {
    modalSubmitLoading.value = false;
    openModal.value = false;

  } else if (modalTitle.value === 'create') {
    createForm.value.validate().then(() => {
      const createBody = cloneDeep(createState);
      Object.keys(createBody).forEach(key => {
        if (isEmpty(createBody[key])) {
          delete createBody[key];
        }
      })

      createPosition(createBody).then(response => {
        modalSubmitLoading.value = false;
        openModal.value = false;
        Object.keys(createState).forEach(key => delete createState[key]);
        createState.order = 1;
        const result = response.data;
        message.success(result.msg);
        loadingData();

      }).catch(error => {
        modalSubmitLoading.value = false;
        console.log(error)
      })

    }).catch(error => {
      modalSubmitLoading.value = false;
      console.log(error)
    })

  } else if (modalTitle.value === 'update') {
    updateForm.value.validate().then(() => {
      updatePosition(updateState).then(response => {
        modalSubmitLoading.value = false;
        openModal.value = false;
        message.success(response.data.msg);
        loadingData();
      })

    }).catch(error => {
      modalSubmitLoading.value = false;
      console.log(error)
    })
  }
}

// 导出按钮操作
const handleExport = () => {
    Modal.confirm({
        title: '警告',
        content: '是否确认导出所有岗位数据?',
        onOk() {
            const body = {
                ...queryState,
                page_no: 1,
                page_size: pagination.total
            };
            message.loading('正在导出数据，请稍候...', 0);

            return exportPosition(body).then(response => {
                const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                // 从响应头获取文件名
                const contentDisposition = response.headers['content-disposition'];
                let fileName = '岗位.xlsx';
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
                message.destroy();
                message.success('导出成功');
            }).catch((error) => {
        message.destroy();
        console.error('导出错误:', error);
        message.error('文件处理失败');
      });
    },
    onCancel() {
        message.info('已取消导出');
    }
    });
};
</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}
</style>