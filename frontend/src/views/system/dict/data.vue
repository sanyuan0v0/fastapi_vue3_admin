<template>
    <div>


        <!-- 搜索表单 -->
        <div class="table-search-wrapper">
            <a-card :bordered="false">
                <a-form :model="queryState" @finish="onFinish">
                    
                    <a-flex wrap="wrap" gap="small">
                            <a-form-item name="dict_type" label="字典" >
                                <a-select v-model:value="queryState.dict_type" placeholder="请选择字典名称" allowClear @click="loadDictTypes">
                                    <a-select-option v-for="item in dictTypeOptions" :key="item.dict_type" :value="item.dict_type">
                                        {{ item.dict_name }}
                                    </a-select-option>
                                </a-select>
                            </a-form-item>
                            <a-form-item name="dict_name" label="标签" >
                                <a-input v-model:value="queryState.dict_label" placeholder="请输入字典数据标签"
                                    allowClear></a-input>
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
            <a-card title="数据字典列表"
                :bordered="false"
                :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
      :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 360px)' }">
                <template #extra>
                    <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')"
                        style="margin-right: 10px;">新建</a-button>
                    <a-button type="primary" :icon="h(DownOutlined)" @click="handleExport"
                        style="margin-right: 10px;">导出
                    </a-button>
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
                        <template v-if="column.dataIndex === 'is_default'">
                            <span>
                                <a-badge :status="record.is_default ? 'processing': 'error'" :text="record.is_default ? '是' : '否'" />
                            </span>
                        </template>
                        <template v-if="column.dataIndex === 'list_class'">
                            <span>
                                {{ dictStore.getDictLabel(DictDataStore['sys_dictdata_list_class'],record.list_class).dict_label }}
                            </span>
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
            <a-modal v-model:open="openModal" @ok="handleModalSumbit" :width="800" :destroyOnClose="true"
                :confirmLoading="modalSubmitLoading" style="top: 30px">
                <template #title>
                    <span>{{ modalTitle === 'create' ? '新建数据字典' : (modalTitle === 'view' ? '查看数据字典' : '修改数据字典')
                        }}</span>
                </template>
                <div v-if="modalTitle === 'view'">
                    <a-spin :spinning="detailStateLoading">
                        <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }"
                            :labelStyle="{ width: '140px' }" bordered>
                            <a-descriptions-item label="序号">{{ (pagination.current - 1) * pagination.pageSize +
                                detailState.index + 1 }}</a-descriptions-item>
                            <a-descriptions-item label="字典排序">{{ detailState.dict_sort }}</a-descriptions-item>
                            <a-descriptions-item label="字典标签">{{ detailState.dict_label }}</a-descriptions-item>
                            <a-descriptions-item label="字典键值">{{ detailState.dict_value }}</a-descriptions-item>
                            <a-descriptions-item label="字典类型">{{ detailState.dict_type }}</a-descriptions-item>
                            <a-descriptions-item label="样式属性">{{ detailState.css_class }}</a-descriptions-item>
                            <a-descriptions-item label="表格回显样式">
                                {{ dictStore.getDictLabel(DictDataStore['sys_dictdata_list_class'],detailState.list_class).dict_label }}
                            </a-descriptions-item>
                            <a-descriptions-item label="是否默认">
                                <a-badge :status="detailState.is_default ? 'processing': 'error'" :text="detailState.is_default ? '是' : '否'" />
                            </a-descriptions-item>
                            <a-descriptions-item label="状态">
                                <a-badge :status="detailState.available ? 'processing': 'error'" :text="detailState.available ? '启用' : '停用'" />
                            </a-descriptions-item>
                            <a-descriptions-item label="创建人">{{ detailState.creator ? detailState.creator.name : '-'
                                }}</a-descriptions-item>
                            <a-descriptions-item label="创建时间">{{ detailState.created_at }}</a-descriptions-item>
                            <a-descriptions-item label="修改时间">{{ detailState.updated_at }}</a-descriptions-item>
                            <a-descriptions-item label="备注" :span="2">{{ detailState.description
                                }}</a-descriptions-item>
                        </a-descriptions>
                    </a-spin>
                </div>
                <div v-else-if="modalTitle === 'create'">
                    <a-form ref="createForm" :model="createState"
                        v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
                        <a-form-item name="dict_type" label="字典类型">
                            <a-input v-model:value="createState.dict_type" placeholder="请输入字典类型" :disabled="true"></a-input>
                        </a-form-item>
                        <a-form-item name="dict_sort" label="字典排序" :rules="[{ required: true, message: '请输入字典排序', pattern: /^[0-9]*$/ }]">
                            <a-input-number v-model:value="createState.dict_sort" placeholder="请输入字典排序" :min="1" :precision="0" style="width: 100%"/>
                        </a-form-item>
                        <a-form-item name="dict_label" label="字典标签" :rules="[{ required: true, message: '请输入字典标签' }]">
                            <a-input v-model:value="createState.dict_label" placeholder="请输入字典标签" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="dict_value" label="字典键值" :rules="[{ required: true, message: '请输入字典键值' }]">
                            <a-input v-model:value="createState.dict_value" placeholder="请输入字典键值" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="css_class" label="样式属性" :rules="[{ required: false, message: '请输入样式属性' }]">
                            <a-input v-model:value="createState.css_class" placeholder="请输入样式属性" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="list_class" label="表格回显样式" :rules="[{ required: false, message: '请选择表格回显样式' }]">
                            <a-select v-model:value="createState.list_class" placeholder="请选择表格回显样式" allowClear>
                                <a-select-option v-for="item in DictDataStore['sys_dictdata_list_class']" :key="item.id" :value="item.dict_value">
                                    {{ item.dict_label }}
                                </a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="is_default" label="是否默认" :rules="[{ required: true, message: '请选择是否默认' }]">
                            <a-radio-group v-model:value="createState.is_default">
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
                            <a-textarea v-model:value="createState.description" placeholder="请输入备注" :rows="4"
                                allowClear />
                        </a-form-item>
                    </a-form>
                </div>
                <div v-else>
                    <a-form ref="updateForm" :model="updateState"
                        v-bind="{ labelCol: { span: 4 }, wrapperCol: { span: 15 } }">
                        <a-form-item name="dict_type" label="字典类型">
                            <a-input v-model:value="updateState.dict_type" placeholder="请输入字典类型" :disabled="true"></a-input>
                        </a-form-item>
                        <a-form-item name="dict_sort" label="字典排序" :rules="[{ required: true, message: '请输入字典排序', pattern: /^[0-9]*$/ }]">
                            <a-input-number v-model:value="updateState.dict_sort" placeholder="请输入字典排序" :min="1" :precision="0" style="width: 100%"/>
                        </a-form-item>
                        <a-form-item name="dict_label" label="字典标签" :rules="[{ required: true, message: '请输入字典标签' }]">
                            <a-input v-model:value="updateState.dict_label" placeholder="请输入字典标签" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="dict_value" label="字典键值" :rules="[{ required: true, message: '请输入字典键值' }]">
                            <a-input v-model:value="updateState.dict_value" placeholder="请输入字典键值" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="css_class" label="样式属性" :rules="[{ required: false, message: '请输入样式属性' }]">
                            <a-input v-model:value="updateState.css_class" placeholder="请输入样式属性" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="list_class" label="表格回显样式" :rules="[{ required: false, message: '请选择表格回显样式' }]">
                            <a-select v-model:value="updateState.list_class" placeholder="请选择表格回显样式" allowClear>
                                <a-select-option v-for="item in DictDataStore['sys_dictdata_list_class']" :key="item.id" :value="item.dict_value">
                                    {{ item.dict_label }}
                                </a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="is_default" label="是否默认" :rules="[{ required: true, message: '请选择是否默认' }]">
                            <a-radio-group v-model:value="updateState.is_default">
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
                            <a-textarea v-model:value="updateState.description" placeholder="请输入备注" :rows="4"
                                allowClear />
                        </a-form-item>
                    </a-form>
                </div>
            </a-modal>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, unref, onMounted, h } from 'vue';
import { useRoute } from 'vue-router';
import { Table, message, Modal } from 'ant-design-vue';
import type { TableColumnsType, MenuProps } from 'ant-design-vue';
import { PlusOutlined, DownOutlined, CheckOutlined, StopOutlined } from '@ant-design/icons-vue';
import { cloneDeep, isEmpty } from '@/utils/util';
import { getDictTypeOptionselect, getDictTypeList,getDictTypeDetail,createDictType,updateDictType,deleteDictType,exportDictType,getDictDataList,getDictDataDetail,createDictData,updateDictData,deleteDictData,exportDictData,getDictTypeOption,getDictDataByType } from '@/api/system/dict'
import type { searchDictDataType, tableDictDataType } from './types'
import { useDictStore } from "@/store/index";

const dictStore = useDictStore();

const DictDataStore = computed(() => {
    return dictStore.dictObj;
})

const getOptions = async () => {
    const dictOptions = await dictStore.setDict(['sys_dictdata_list_class'])
    return dictOptions
}

const route = useRoute();
const createForm = ref();
const updateForm = ref();
const tableLoading = ref(false);
const openModal = ref(false);
const modalTitle = ref('');
const modalSubmitLoading = ref(false);
const detailStateLoading = ref(false);
const dataSource = ref<tableDictDataType[]>([]);
const selectedRowKeys = ref<tableDictDataType['id'][]>([]);

const queryState = reactive<searchDictDataType>({
    dict_label: null,
    dict_type: null,
    available: null
});

const dictTypeOptions = ref<any[]>([]);
const pagination = reactive({
    current: 1,
    pageSize: 10,
    defaultPageSize: 10,
    showSizeChanger: true,
    total: dataSource.value.length,
    showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})
const createState = reactive<tableDictDataType>({
    dict_sort: null,
    dict_label: '',
    dict_value: '',
    dict_type: '',
    css_class: '',
    list_class: null,
    is_default: false,
    available: true,
    description: ''
})
const updateState = reactive<tableDictDataType>({
    id: undefined,
    dict_sort: null,
    dict_label: '',
    dict_value: '',
    dict_type: '',
    css_class: '',
    list_class: null,
    is_default: false,
    available: true,
    description: ''
})
const detailState = ref<tableDictDataType>({})

const columns: TableColumnsType = [
    {
        title: '序号',
        dataIndex: 'index',
        align: 'center',
        ellipsis: true,
        width: 80
    },
    {
        title: '字典排序',
        dataIndex: 'dict_sort',
        ellipsis: true,
        // align: 'center'
    },
    {
        title: '字典标签',
        dataIndex: 'dict_label',
        ellipsis: true,
        // align: 'center'
    },
    {
        title: '字典键值',
        dataIndex: 'dict_value',
        ellipsis: true,
        // align: 'center'
    },
    {
        title: '字典类型',
        dataIndex: 'dict_type',
        ellipsis: true,
        // align: 'center'
    },
    // {
    //     title: '样式属性',
    //     dataIndex: 'css_class',
    //     ellipsis: true,
    //     // align: 'center'
    // },
    // {
    //     title: '表格回显样式',
    //     dataIndex: 'list_class',
    //     ellipsis: true,
    //     // align: 'center'
    // },
    {
        title: '是否默认',
        dataIndex: 'is_default',
        ellipsis: true,
        // align: 'center'
    },
    {
        title: '状态',
        dataIndex: 'available',
        // ellipsis: true,
        align: 'center'
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
        // width: 120
    },
    {
        title: '更新日期',
        dataIndex: 'updated_at',
        // align: 'center',
        ellipsis: true,
        // width: 120
    },
    {
        title: '操作',
        dataIndex: 'operation',
        align: 'center',
        fixed: 'right',
        ellipsis: true,
        width: 150
    }
];

// 表格选中配置
const rowSelection = computed(() => {
    return {
        selectedRowKeys: unref(selectedRowKeys),
        onChange: (selectingRowKeys: tableDictDataType['id'][]) => {
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

// 加载字典类型
const loadDictTypes = () => {
    getDictTypeOptionselect().then(response => {
        const result = response.data;
        dictTypeOptions.value = result.data;
        message.success(result.msg);
    }).catch(error => {
        console.log(error);
        message.error('获取字典类型失败');
    });
}

// 加载表格数据
const loadingData = () => {
    tableLoading.value = true;

    let params = {};
    if (queryState.dict_label) {
        params['dict_label'] = queryState.dict_label
    }
    if (queryState.dict_type) {
        params['dict_type'] = queryState.dict_type
    } else if (route.query.dict_type) {
        params['dict_type'] = Array.isArray(route.query.dict_type) ? route.query.dict_type[0] : route.query.dict_type
        queryState.dict_type = Array.isArray(route.query.dict_type) ? route.query.dict_type[0] : route.query.dict_type
    }
    if (queryState.available !== null && queryState.available !== undefined) {
    params['available'] = queryState.available;
  }
    params['page_no'] = pagination.current
    params['page_size'] = pagination.pageSize

    getDictDataList(params).then(response => {
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
onMounted(async () => {
    await getOptions();
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
        dict_sort: null,
        dict_label: '',
        dict_value: '',
        dict_type: route.query.dict_type || '',
        css_class: '',
        list_class: null,
        is_default: false,
        available: true,
        description: ''
    });

    Object.assign(updateState, {
        id: undefined,
        dict_sort: null,
        dict_label: '',
        dict_value: '',
        dict_type: '',
        css_class: '',
        list_class: null,
        is_default: false,
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
const deleteRow = (row: tableDictDataType) => {
    deleteDictData({ id: row.id }).then(response => {
        const result = response.data;
        message.success(result.msg);
        loadingData();
    }).catch(error => {
        console.log(error)
    })
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

            createDictData(createBody).then(response => {
                modalSubmitLoading.value = false;
                openModal.value = false;
                Object.keys(createState).forEach(key => delete createState[key]);
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
            updateDictData(updateState).then(response => {
                modalSubmitLoading.value = false;
                openModal.value = false;
                message.success(response.data.msg);
                loadingData();
            }).catch(error => {
                modalSubmitLoading.value = false;
                console.log(error)
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
        content: '是否确认导出所有数据字典数据?',
        onOk() {
            const body = {
                ...queryState,
                page_no: 1,
                page_size: pagination.total
            };
            message.loading('正在导出数据，请稍候...', 0);

            return exportDictData(body).then(response => {
                const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                // 从响应头获取文件名
                const contentDisposition = response.headers['content-disposition'];
                let fileName = '数据字典.xlsx';
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