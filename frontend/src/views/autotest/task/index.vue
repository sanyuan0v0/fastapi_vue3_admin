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
                            <a-form-item name="name" label="类型" style="max-width: 300px;">
                                <a-input v-model:value="queryState.name" placeholder="请输入类型" allowClear></a-input>
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
            <a-card title="任务列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
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
                        <template v-if="column.dataIndex === 'status'">
                            <a-tag :color="getStatusColor(record.status)">{{ record.status }}</a-tag>
                        </template>
                        <template v-if="column.dataIndex === 'summary'">
                            <span>通过率: {{ record.summary?.pass_rate }}</span><br/>
                            <span>耗时: {{ record.summary?.duration }}</span>
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
                    <span>{{ modalTitle === 'create' ? '新建任务' : (modalTitle === 'view' ? '查看任务' : '修改任务')
                        }}</span>
                </template>
                <!-- 详情弹窗 -->
                <div v-if="modalTitle === 'view'">
                    <a-spin :spinning="detailStateLoading">
                        <a-descriptions :column="2" bordered>
                            <a-descriptions-item label="任务名称">{{ detailState.name }}</a-descriptions-item>
                            <a-descriptions-item label="所属项目">{{ detailState.project?.name }}</a-descriptions-item>
                            <a-descriptions-item label="执行状态">
                                <a-tag :color="getStatusColor(detailState.status)">{{ detailState.status }}</a-tag>
                            </a-descriptions-item>
                            <a-descriptions-item label="开始时间">{{ detailState.start_time }}</a-descriptions-item>
                            <a-descriptions-item label="结束时间">{{ detailState.end_time }}</a-descriptions-item>
                            <a-descriptions-item label="测试概要" :span="2">
                                <div v-if="detailState.summary">
                                    <p>用例总数: {{ detailState.total_count }}</p>
                                    <p>成功数量: {{ detailState.success_count }}</p>
                                    <p>失败数量: {{ detailState.fail_count }}</p>
                                    <p>跳过数量: {{ detailState.skip_count }}</p>
                                    <p>错误数量: {{ detailState.error_count }}</p>
                                    <p>通过率: {{ detailState.summary.pass_rate }}</p>
                                    <p>执行时长: {{ detailState.summary.duration }}</p>
                                </div>
                            </a-descriptions-item>
                            <a-descriptions-item label="执行日志" :span="2">
                                <a-collapse v-if="detailState.logs?.length">
                                    <a-collapse-panel v-for="(log, index) in detailState.logs" 
                                        :key="index" :header="`日志 ${index + 1}`">
                                        <pre>{{ log }}</pre>
                                    </a-collapse-panel>
                                </a-collapse>
                            </a-descriptions-item>
                            <a-descriptions-item label="实际响应" :span="2">
                                <pre>{{ detailState.actual_response }}</pre>
                            </a-descriptions-item>
                            <a-descriptions-item label="备注说明">{{ detailState.description }}</a-descriptions-item>
                            <a-descriptions-item label="创建时间">{{ detailState.created_at }}</a-descriptions-item>
                            <a-descriptions-item label="更新时间">{{ detailState.updated_at }}</a-descriptions-item>
                        </a-descriptions>
                    </a-spin>
                </div>

                <!-- 新增弹窗 -->
                <div v-else-if="modalTitle === 'create'">
                    <a-form 
                        ref="createForm" 
                        :model="createState" 
                        :label-col="{ span: 5 }" 
                        :wrapper-col="{ span: 16 }"
                    >
                        <a-form-item name="name" label="任务名称" :rules="[{ required: true }]">
                            <a-input v-model:value="createState.name" placeholder="请输入任务名称" allowClear />
                        </a-form-item>

                        <a-form-item name="project_id" label="所属项目" :rules="[{ required: true }]">
                            <a-select v-model:value="createState.project_id" placeholder="请选择项目">
                                <a-select-option v-for="project in projectList" :key="project.id" :value="project.id">
                                    {{ project.name }}
                                </a-select-option>
                            </a-select>
                        </a-form-item>

                        <a-form-item name="description" label="备注说明">
                            <a-textarea v-model:value="createState.description" placeholder="请输入备注" :rows="4" allowClear />
                        </a-form-item>
                    </a-form>
                </div>

                <!-- 编辑弹窗 -->
                <div v-else>
                    <a-form 
                        ref="updateForm" 
                        :model="updateState"
                        :label-col="{ span: 5 }" 
                        :wrapper-col="{ span: 16 }"
                    >
                        <a-form-item name="name" label="任务名称" :rules="[{ required: true }]">
                            <a-input v-model:value="updateState.name" placeholder="请输入任务名称" allowClear />
                        </a-form-item>

                        <a-form-item name="project_id" label="所属项目" :rules="[{ required: true }]">
                            <a-select v-model:value="updateState.project_id" placeholder="请选择项目">
                                <a-select-option v-for="project in projectList" :key="project.id" :value="project.id">
                                    {{ project.name }}
                                </a-select-option>
                            </a-select>
                        </a-form-item>


                        <a-form-item name="description" label="备注说明">
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
import { Table, message } from 'ant-design-vue';
import type { TableColumnsType } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { cloneDeep, isEmpty } from '@/utils/util';
import PageHeader from '@/components/PageHeader.vue';
import { getProjectList } from '@/api/autotest/project'
import { getTaskList, getTaskDetail, createTask, updateTask, deleteTask } from '@/api/autotest/task'
import type { searchDataType, tableDataType, projectSelectorType } from './types'

// 只保留核心字段在列表中展示
const columns: TableColumnsType = [
    {
        title: '序号',
        dataIndex: 'index',
        align: 'center',
        width: 80
    },
    {
        title: '任务名称',
        dataIndex: 'name',
        ellipsis: true,
    },
    {
        title: '所属项目', 
        dataIndex: 'project.name',
        width: 120,
        ellipsis: true,
        customRender: ({ record }) => record.project?.name || '-'
    },
    {
        title: '状态',
        dataIndex: 'status',
        width: 80,
        ellipsis: true,
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
    project_id: undefined,
    description: '',
})
const updateState = reactive<tableDataType>({
    id: undefined,
    name: '',
    project_id: undefined,
    description: '',
})
const detailState = ref<tableDataType>({})
const projectList = ref<projectSelectorType[]>([]);


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

    getTaskList(params).then(response => {
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

const loadProjectList = () => {
    tableLoading.value = true;
    let params = {};
    getProjectList(params).then(response => {
        const result = response.data;
        projectList.value = result.data.items;
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
    loadProjectList()
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
            updateState[key] = selected[key];
        })
    }
}

// 删除
const deleteRow = (row: tableDataType) => {
    deleteTask({ id: row.id }).then(response => {
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

            createTask(createBody).then(response => {
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
            updateTask(updateState).then(response => {
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

// 获取状态颜色
const getStatusColor = (status: string) => {
    switch (status) {
        case 'running': return 'processing';
        case 'completed': return 'success';
        case 'failed': return 'error';
        default: return 'default';
    }
};

</script>

<style lang="scss" scoped>
.table-search-wrapper {
    margin-block-end: 16px;
}
</style>