<template>
  <div>
    <!-- 搜索表单 -->
    <div class="table-search-wrapper">
      <a-card>
        <a-form :model="queryState" @finish="onFinish">
          <a-flex wrap="wrap" gap="middle">
            <a-form-item name="config_name" label="配置名称">
              <a-input v-model:value="queryState.config_name" placeholder="请输入配置名称" allowClear
                style="width: 200px;"></a-input>
            </a-form-item>
            <a-form-item name="config_key" label="配置键名">
              <a-input v-model:value="queryState.config_key" placeholder="请输入配置键名" allowClear
                style="width: 200px;"></a-input>
            </a-form-item>
            <a-form-item name="config_type" label="系统内置">
              <a-select v-model:value="queryState.config_type" placeholder="请选择是否系统内置" allowClear style="width: 200px;">
                <a-select-option value="true">是</a-select-option>
                <a-select-option value="false">否</a-select-option>
              </a-select>
            </a-form-item>
            <a-button type="primary" html-type="submit" :loading="tableLoading">查询</a-button>
            <a-button @click="resetFields">重置</a-button>
          </a-flex>
        </a-form>
      </a-card>
    </div>

    <!-- 表格区域 -->
    <div class="table-wrapper">
      <a-card title="系统配置列表">
        <template #extra>
          <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')"
            style="margin-right: 10px;">新建</a-button>
          <a-button type="primary" :icon="h(DownOutlined)" @click="handleExport" style="margin-right: 10px;">导出
          </a-button>
        </template>
        <a-table :rowKey="record => record.id" :columns="columns" :data-source="dataSource"
          :row-selection="rowSelection" :loading="tableLoading" @change="handleTableChange" :pagination="pagination"
          :scroll="{ x: 500, y: 'calc(100vh - 490px)' }" :style="{ minHeight: 'calc(100vh - 430px)' }">
          <template #bodyCell="{ column, record, index }">
            <template v-if="column.dataIndex === 'index'">
              <span>{{ (pagination.current - 1) * pagination.pageSize + index + 1 }}</span>
            </template>
            <template v-if="column.dataIndex === 'config_type'">
              <span>
                <a-badge :status="record.config_type ? 'processing' : 'error'" :text="record.config_type ? '是' : '否'" />
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
      <a-modal v-model:open="openModal" @ok="handleModalSumbit" :width="800" :destroyOnClose="true"
        :confirmLoading="modalSubmitLoading" style="top: 30px">
        <template #title>
          <span>
            {{ modalTitle === 'create' ? '新建系统配置' : (modalTitle === 'view' ? '查看系统配置' : '修改系统配置') }}
          </span>
        </template>
        <div v-if="modalTitle === 'view'">
          <a-spin :spinning="detailStateLoading">
            <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }"
              bordered>
              <a-descriptions-item label="序号">{{ (pagination.current - 1) * pagination.pageSize + detailState.index + 1
                }}</a-descriptions-item>
              <a-descriptions-item label="配置名称">{{ detailState.config_name }}</a-descriptions-item>
              <a-descriptions-item label="配置键名">{{ detailState.config_key }}</a-descriptions-item>
              <a-descriptions-item label="配置键值">{{ detailState.config_value }}</a-descriptions-item>
              <a-descriptions-item label="系统内置">
                <a-badge :status="detailState.config_type ? 'processing' : 'error'"
                  :text="detailState.config_type ? '是' : '否'" />
              </a-descriptions-item>
              <a-descriptions-item label="创建人">{{ detailState.creator ? detailState.creator.name : '-'
                }}</a-descriptions-item>
              <a-descriptions-item label="创建时间">{{ detailState.created_at }}</a-descriptions-item>
              <a-descriptions-item label="修改时间">{{ detailState.updated_at }}</a-descriptions-item>
              <a-descriptions-item label="备注">{{ detailState.description }}</a-descriptions-item>
            </a-descriptions>
          </a-spin>
        </div>
        <div v-else-if="modalTitle === 'create'">
          <a-form ref="createForm" :model="createState" v-bind="{ labelCol: { span: 8 }, wrapperCol: { span: 12 } }">
            <a-form-item name="config_name" label="配置名称" :rules="[{ required: true, message: '请输入配置名称' }]">
              <a-input v-model:value="createState.config_name" placeholder="请输入配置名称" allowClear></a-input>
            </a-form-item>
            <a-form-item name="config_key" label="配置键名" :rules="[{ required: true, message: '请选择配置键名' }]">
              <a-input v-model:value="createState.config_key" placeholder="请输入配置键名" allowClear></a-input>
            </a-form-item>
            <a-form-item name="config_value" label="配置键值" :rules="[{ required: true, message: '请选择任配置键值' }]">
              <a-input v-model:value="createState.config_value" placeholder="请输入配置键值" allowClear></a-input>
            </a-form-item>
            <a-form-item name="config_type" label="系统内置" :rules="[{ required: true, message: '请选择是否系统内置' }]">
              <a-radio-group v-model:value="createState.config_type">
                <a-radio :value="true">是</a-radio>
                <a-radio :value="false">否</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item name="description" label="备注">
              <a-textarea v-model:value="createState.description" placeholder="请输入备注" :rows="4" allowClear />
            </a-form-item>
          </a-form>
        </div>
        <div v-else>
          <a-form ref="updateForm" :model="updateState" v-bind="{ labelCol: { span: 8 }, wrapperCol: { span: 12 } }">
            <a-form-item name="config_name" label="配置名称" :rules="[{ required: true, message: '请输入配置名称' }]">
              <a-input v-model:value="updateState.config_name" placeholder="请输入配置名称" allowClear></a-input>
            </a-form-item>
            <a-form-item name="config_key" label="配置键名" :rules="[{ required: true, message: '请选择配置键名' }]">
              <a-input v-model:value="updateState.config_key" placeholder="请输入配置键名" allowClear></a-input>
            </a-form-item>
            <a-form-item name="config_value" label="配置键值" :rules="[{ required: true, message: '请选择任配置键值' }]">
              <a-input v-model:value="updateState.config_value" placeholder="请输入配置键值" allowClear></a-input>
            </a-form-item>
            <a-form-item name="config_type" label="系统内置" :rules="[{ required: true, message: '请选择是否系统内置' }]">
              <a-radio-group v-model:value="updateState.config_type">
                <a-radio :value="true">是</a-radio>
                <a-radio :value="false">否</a-radio>
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
import type { TableColumnsType } from 'ant-design-vue';
import { PlusOutlined, DownOutlined } from '@ant-design/icons-vue';
import { cloneDeep, isEmpty } from '@/utils/util';
import { getConfigList, createConfig, updateConfig, deleteConfig, exportConfig } from '@/api/system/config'
import type { searchType, tableType } from './types'

const createForm = ref();
const updateForm = ref();
const tableLoading = ref(false);
const openModal = ref(false);
const modalTitle = ref('');
const modalSubmitLoading = ref(false);
const detailStateLoading = ref(false);
const dataSource = ref<tableType[]>([]);
const selectedRowKeys = ref<tableType['id'][]>([]);
const queryState = reactive<searchType>({});
const pagination = reactive({
    current: 1,
    pageSize: 10,
    defaultPageSize: 10,
    showSizeChanger: true,
    total: dataSource.value.length,
    showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})
const createState = reactive<tableType>({
    config_name: '',
    config_key: '',
    config_value: '',
    config_type: null,
    description: ''
})
const updateState = reactive<tableType>({
    id: undefined,
    config_name: '',
    config_key: '',
    config_value: '',
    config_type: null,
    description: ''
})
const detailState = ref<tableType>({})
const columns: TableColumnsType = [
    {
        title: '序号',
        dataIndex: 'index',
        align: 'center',
        width: 80
    },
    {
        title: '配置名称',
        dataIndex: 'config_name',
        ellipsis: true,
        width: 100
    },
    {
        title: '配置键名',
        dataIndex: 'config_key',
        ellipsis: true,
        width: 160
    },
    {
        title: '配置键值',
        dataIndex: 'config_value',
        ellipsis: true,
    },
    {
        title: '系统内置',
        dataIndex: 'config_type',
        ellipsis: true,
        width: 80,
    },
    {
        title: '备注',
        dataIndex: 'description',
        ellipsis: true,
        width: 100,
    },
    {
        title: '创建时间',
        dataIndex: 'created_at',
        ellipsis: true,
        width: 180
    },
    {
        title: '操作',
        dataIndex: 'operation',
        align: 'center',
        fixed: 'right',
        width: 200
    }
];
const rowSelection = computed(() => {
    return {
        selectedRowKeys: unref(selectedRowKeys),
        onChange: (selectingRowKeys: tableType['id'][]) => {
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
const loadingData = async () => {
  
  try {
    tableLoading.value = true;
    let params = {};
    
    if (queryState.config_name) {
      params['config_name'] = queryState.config_name
    }
    
    if (queryState.config_key) {
      params['config_key'] = queryState.config_key
    }
    
    if (queryState.config_type !== null && queryState.config_type !== undefined) {
      params['config_type'] = queryState.config_type;
    }
    
    params['page_no'] = pagination.current
    params['page_size'] = pagination.pageSize

    const response = await getConfigList(params)
    const result = response.data;
    dataSource.value = result.data.items;
    pagination.total = result.data.total;
    pagination.current = result.data.page_no;
    pagination.pageSize = result.data.page_size;
  } catch (error) {
    console.log(error);
  } finally {
    tableLoading.value = false;
  }
}

// 生命周期钩子
onMounted(async() => {
    loadingData();
});

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
    queryState.config_name = null
    queryState.config_key = null
    queryState.config_type = null

    loadingData();
}

const handleTableChange = (values: any) => {
    pagination.current = values.current;
    pagination.pageSize = values.pageSize;
    loadingData();
}

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
            updateState[key] = selected[key];
        })
    } 
}

// 删除
const deleteRow = async (row: tableType) => {
  try {
    tableLoading.value = true;
    await deleteConfig({ id: row.id })
    loadingData();
  } catch (error) {
    console.log(error)
  } finally {
    tableLoading.value = false;
  }
}

// 弹窗提交（详情/新建/修改）
const handleModalSumbit = async () => {
  modalSubmitLoading.value = true;

  if (modalTitle.value === 'view') {
    modalSubmitLoading.value = false;
    openModal.value = false;
  } else if (modalTitle.value === 'create') {
    try {
      await createForm.value.validate();
      const createBody = cloneDeep(createState);
      Object.keys(createBody).forEach(key => {
        if (isEmpty(createBody[key])) {
          delete createBody[key];
        }
      })
      await createConfig(createBody)
      openModal.value = false;
      Object.keys(createState).forEach(key => delete createState[key]);
      loadingData();
    } catch (error) {
      console.log(error)
    } finally {
      modalSubmitLoading.value = false;
      tableLoading.value = false;
    }
  } else if (modalTitle.value === 'update') {
    try {
      await updateForm.value.validate();
      await updateConfig(updateState)
      openModal.value = false;
      loadingData();
    } catch (error) {
      console.log(error)
    } finally {
      modalSubmitLoading.value = false;
      tableLoading.value = false;
    }
  }
}

// 导出按钮操作
const handleExport = () => {
    Modal.confirm({
        title: '警告',
        content: '是否确认导出当前系统配置?',
        onOk() {
            const body = {
                ...queryState,
                page_no: 1,
                page_size: pagination.total
            };
            message.loading('正在导出数据，请稍候...', 0);

            return exportConfig(body).then(response => {
                const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
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