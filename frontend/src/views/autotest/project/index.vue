<template>
    <div>
        <!-- 页面头部 -->
        <page-header />

        <!-- 搜索表单 -->
        <div class="table-search-wrapper">
            <a-card :bordered="false">
                <a-form :model="queryState" @finish="onFinish">
                    <a-row>
                        <a-col flex="0 1 450px">
                            <a-form-item name="name" label="名称" style="max-width: 300px;">
                                <a-input v-model:value="queryState.name" placeholder="请输入名称" allowClear></a-input>
                            </a-form-item>
                        </a-col>
                        <a-col flex="0 1 450px">
                            <a-form-item name="date-range-picker" label="创建日期" style="max-width: 350px;">
                                <a-range-picker v-model:value="queryState.date_range" value-format="YYYY-MM-DD" />
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
            <a-card title="项目列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
                :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 400px)' }">
                <template #extra>
                    <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')"
                        style="margin-right: 10px;">新建
                    </a-button>
                </template>
                <a-table :rowKey="record => record.id" :columns="columns" :data-source="dataSource"
                    :row-selection="rowSelection" :loading="tableLoading" @change="handleTableChange"
                    :scroll="{ x: 400 }" :pagination="pagination" :style="{ minHeight: '420px' }">
                    <template #bodyCell="{ column, record, index }">
                        <template v-if="column.dataIndex === 'index'">
                            <span>{{ (pagination.current - 1) * pagination.pageSize + index + 1 }}</span>
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
                    <span>{{ modalTitle === 'create' ? '新建项目' : (modalTitle === 'view' ? '查看项目' : '修改项目')
                        }}</span>
                </template>
                <div v-if="modalTitle === 'view'">
                    <a-spin :spinning="detailStateLoading">
                        <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }"
                            :labelStyle="{ width: '140px' }" bordered>
                            <a-descriptions-item label="序号">{{ (pagination.current - 1) * pagination.pageSize +
                                detailState.index + 1 }}</a-descriptions-item>
                            <a-descriptions-item label="项目名称">{{ detailState.name }}</a-descriptions-item>
                            <a-descriptions-item label="基础URL">{{ detailState.base_url }}</a-descriptions-item>
                            <a-descriptions-item label="请求头">{{ Object.keys(detailState.headers).map(key => `${key}:
                                ${detailState.headers[key]}`).join(', ') }}</a-descriptions-item>
                            <a-descriptions-item label="消息">{{ Object.keys(detailState.message).map(key => `${key}:
                                ${detailState.message[key]}`).join(', ') }}</a-descriptions-item>
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
                        <a-form-item name="name" label="项目名称" :rules="[{ required: true, message: '请输入项目名称' }]">
                            <a-input v-model:value="createState.name" placeholder="请输入项目名称" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="base_url" label="基础URL">
                            <a-input v-model:value="createState.base_url" placeholder="请输入基础URL" allowClear></a-input>
                        </a-form-item>
                        <a-form-item label="请求头">
                            <div v-for="(value, key) in createState.headers" :key="key">
                                <a-row :gutter="16">
                                    <a-col :span="10">
                                        <a-input v-model:value="createState.headers[key]" placeholder="Value"
                                            allowClear />
                                    </a-col>
                                    <a-col :span="10">
                                        <a-input v-model:value="key" placeholder="Key" allowClear disabled />
                                    </a-col>
                                    <a-col :span="4">
                                        <a-button type="link" @click="removeHeader(key.toString())">删除</a-button>
                                    </a-col>
                                </a-row>
                            </div>
                            <a-button type="dashed" block @click="addHeader">添加请求头</a-button>
                        </a-form-item>
                        <a-form-item label="消息">
                            <div v-for="(value, key) in createState.message" :key="key">
                                <a-row :gutter="16">
                                    <a-col :span="10">
                                        <a-input v-model:value="createState.message[key]" placeholder="Value"
                                            allowClear />
                                    </a-col>
                                    <a-col :span="10">
                                        <a-input v-model:value="key" placeholder="Key" allowClear disabled />
                                    </a-col>
                                    <a-col :span="4">
                                        <a-button type="link" @click="removeMessage(key.toString())">删除</a-button>
                                    </a-col>
                                </a-row>
                            </div>
                            <a-button type="dashed" block @click="addMessage">添加消息</a-button>
                        </a-form-item>
                        <a-form-item name="description" label="备注">
                            <a-textarea v-model:value="createState.description" placeholder="请输入备注" :rows="4"
                                allowClear />
                        </a-form-item>
                    </a-form>
                </div>
                <div v-else>
                    <a-form ref="updateForm" :model="updateState"
                        v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
                        <a-form-item name="name" label="项目名称" :rules="[{ required: true, message: '请输入项目名称' }]">
                            <a-input v-model:value="updateState.name" placeholder="请输入项目名称" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="base_url" label="基础URL">
                            <a-input v-model:value="updateState.base_url" placeholder="请输入基础URL" allowClear></a-input>
                        </a-form-item>
                        <a-form-item label="请求头">
                            <div v-for="(value, key) in updateState.headers" :key="key">
                                <a-row :gutter="16">
                                    <a-col :span="10">
                                        <a-input v-model:value="updateState.headers[key]" placeholder="Value"
                                            allowClear />
                                    </a-col>
                                    <a-col :span="10">
                                        <a-input v-model:value="key" placeholder="Key" allowClear disabled />
                                    </a-col>
                                    <a-col :span="4">
                                        <a-button type="link" @click="removeHeader(key.toString())">删除</a-button>
                                    </a-col>
                                </a-row>
                            </div>
                            <a-button type="dashed" block @click="addHeader">添加请求头</a-button>
                        </a-form-item>
                        <a-form-item label="消息">
                            <div v-for="(value, key) in updateState.message" :key="key">
                                <a-row :gutter="16">
                                    <a-col :span="10">
                                        <a-input v-model:value="updateState.message[key]" placeholder="Value"
                                            allowClear />
                                    </a-col>
                                    <a-col :span="10">
                                        <a-input v-model:value="key" placeholder="Key" allowClear disabled />
                                    </a-col>
                                    <a-col :span="4">
                                        <a-button type="link" @click="removeMessage(key.toString())">删除</a-button>
                                    </a-col>
                                </a-row>
                            </div>
                            <a-button type="dashed" block @click="addMessage">添加消息</a-button>
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
import { Table, message } from 'ant-design-vue';
import type { TableColumnsType } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { cloneDeep, isEmpty } from '@/utils/util';
import PageHeader from '@/components/PageHeader.vue';
import { getProjectList, createProject, updateProject, deleteProject } from '@/api/autotest/project'
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

const queryState = reactive<searchDataType>({});
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
    base_url: '',
    headers: {},
    message: {},
    description: ''
})
const updateState = reactive<tableDataType>({
    id: undefined,
    name: '',
    base_url: '',
    headers: {},
    message: {},
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
        title: '项目名称',
        dataIndex: 'name',
        ellipsis: true,
    },
    {
        title: '基础URL',
        dataIndex: 'base_url',
        ellipsis: true,
    },
    {
        title: '请求头',
        dataIndex: 'headers',
        ellipsis: true,
        customRender: ({ text }) => Object.keys(text).map(key => `${key}: ${text[key]}`).join(', ')
    },
    {
        title: '消息',
        dataIndex: 'message',
        ellipsis: true,
        customRender: ({ text }) => Object.keys(text).map(key => `${key}: ${text[key]}`).join(', ')
    },
    {
        title: '备注',
        dataIndex: 'description',
        ellipsis: true,
    },
    {
        title: '创建日期',
        dataIndex: 'created_at',
        ellipsis: true,
    },
    {
        title: '更新日期',
        dataIndex: 'updated_at',
        ellipsis: true,
    },
    {
        title: '创建人',
        dataIndex: 'creator',
        ellipsis: true,
        customRender: ({ text }) => text ? text.name : '-'
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
    if (queryState.date_range) {
        params['start_time'] = `${queryState.date_range[0]} 00:00:00`;
        params['end_time'] = `${queryState.date_range[1]} 23:59:59`;
    }
    params['page_no'] = pagination.current
    params['page_size'] = pagination.pageSize

    getProjectList(params).then(response => {
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
onMounted(() => {
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

    if (modalType === 'view' && index !== undefined) {
        detailStateLoading.value = true;

        detailState.value = dataSource.value[index];
        detailState.value.index = index;

        detailStateLoading.value = false;

    } else if (modalType === 'update' && index !== undefined) {
        const selected = dataSource.value[index];
        Object.keys(updateState).forEach(key => {
            if (key === 'headers') {
                updateState[key] = cloneDeep(selected[key]) || {};
            } else {
                updateState[key] = selected[key];
            }
        });
    }
}

// 删除
const deleteRow = (row: tableDataType) => {
    deleteProject({ id: row.id }).then(response => {
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

            createProject(createBody).then(response => {
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
            updateProject(updateState).then(response => {
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

const addHeader = () => {
    const newKey = `header_${Object.keys(createState.headers).length}`;
    createState.headers[newKey] = '';
};

const removeHeader = (key: string | number) => {
    delete createState.headers[key];
};


const addMessage = () => {
    const newKey = `msg_${Object.keys(createState.message).length}`;
    createState.message[newKey] = '';
};

const removeMessage = (key: string | number) => {
    delete createState.message[key];
};

</script>

<style lang="scss" scoped>
.table-search-wrapper {
    margin-block-end: 16px;
}
</style>