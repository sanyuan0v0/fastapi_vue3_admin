<template>
    <div>
        <!-- 页面头部 -->
        <page-header />

        <!-- 主体内容区域 -->
        <div class="main-content">


            <div class="environment-list">
                <!-- 搜索表单 -->
                <div class="table-search-wrapper">
                    <a-card :bordered="false">
                        <a-form :model="queryState" @finish="onFinish">
                            <a-row>
                                <a-col flex="0 1 450px">
                                    <a-form-item name="name" label="名称" style="max-width: 300px;">
                                        <a-input v-model:value="queryState.name" placeholder="请输入名称"
                                            allowClear></a-input>
                                    </a-form-item>
                                </a-col>
                                <a-col flex="0 1 450px">
                                    <a-form-item name="date-range-picker" label="创建日期" style="max-width: 350px;">
                                        <a-range-picker v-model:value="queryState.date_range"
                                            value-format="YYYY-MM-DD" />
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
                    <a-card title="环境列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
                        :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 400px)' }">
                        <template #extra>
                            <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')"
                                style="margin-right: 10px;">新建
                            </a-button>
                        </template>
                        <!-- 使用 a-row 和 a-col 划分左右布局 -->
                        <a-row :gutter="16">
                            <!-- 左侧部门树 -->
                            <a-col :span="4">
                                <a-tree v-model:selectedKeys="selectedProject" v-if="treeData.length" 
                                    :tree-data="treeData"
                                    @select="handleProjectSelect" 
                                    :showLine="true"
                                    :defaultExpandAll="true" 
                                    />
                            </a-col>

                            <!-- 右侧用户列表 -->
                            <a-col :span="20">
                                <a-table :rowKey="record => record.id" :columns="columns" :data-source="dataSource"
                                    :row-selection="rowSelection" :loading="tableLoading" @change="handleTableChange"
                                    :scroll="{ x: 400 }" :pagination="pagination" :style="{ minHeight: '420px' }">
                                    <template #bodyCell="{ column, record, index }">
                                        <template v-if="column.dataIndex === 'index'">
                                            <span>{{ (pagination.current - 1) * pagination.pageSize + index + 1
                                                }}</span>
                                        </template>
                                        <template v-if="column.dataIndex === 'operation'">
                                            <a-space size="middle">
                                                <a @click="modalHandle('view', index)">查看</a>
                                                <a @click="modalHandle('update', index)">修改</a>
                                                <a-popconfirm title="确定删除吗？" ok-text="确定" cancel-text="取消"
                                                    @confirm="deleteRow(record)">
                                                    <a style="color: red;">删除</a>
                                                </a-popconfirm>
                                            </a-space>
                                        </template>
                                    </template>
                                </a-table>
                            </a-col>
                        </a-row>

                    </a-card>
                </div>
            </div>
        </div>

        <!-- 弹窗区域 -->
        <div class="modal-wrapper">
            <a-modal v-model:open="openModal" @ok="handleModalSumbit" :width="800" :destroyOnClose="true"
                :confirmLoading="modalSubmitLoading" style="top: 30px">
                <template #title>
                    <span>{{ modalTitle === 'create' ? '新建环境' : (modalTitle === 'view' ? '查看环境' : '修改环境')
                        }}</span>
                </template>
                <div v-if="modalTitle === 'view'">
                    <a-spin :spinning="detailStateLoading">
                        <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }"
                            :labelStyle="{ width: '140px' }" bordered>
                            <a-descriptions-item label="序号">{{ (pagination.current - 1) * pagination.pageSize +
                                detailState.index + 1 }}</a-descriptions-item>
                            <a-descriptions-item label="环境名称">{{ detailState.name }}</a-descriptions-item>
                            <a-descriptions-item label="环境地址">{{ detailState.base_url }}</a-descriptions-item>
                            <a-descriptions-item label="绑定项目" :span="1">
                                {{ projectList.find(p => p.id === detailState.project_id)?.name || '-' }}
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
                        <a-form-item name="name" label="环境名称" :rules="[{ required: true, message: '请输入环境名称' }]">
                            <a-input v-model:value="createState.name" placeholder="请输入环境名称" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="base_url" label="环境地址" :rules="[{ required: true, message: '请输入环境地址' }]">
                            <a-input v-model:value="createState.base_url" placeholder="请输入环境地址" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="project_id" label="绑定项目" :rules="[{ required: true, message: '请选择绑定项目' }]">
                            <a-select v-model:value="createState.project_id" placeholder="请选择绑定项目">
                                <a-select-option v-for="project in projectList" :key="project.id" :value="project.id">{{
                                    project.name }}</a-select-option>
                            </a-select>
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
                        <a-form-item name="name" label="环境名称" :rules="[{ required: true, message: '请输入环境名称' }]">
                            <a-input v-model:value="updateState.name" placeholder="请输入环境名称" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="base_url" label="环境地址" :rules="[{ required: true, message: '请输入环境地址' }]">
                            <a-input v-model:value="updateState.base_url" placeholder="请输入环境地址" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="project_id" label="绑定项目" :rules="[{ required: true, message: '请选择绑定项目' }]">
                            <a-select v-model:value="updateState.project_id" placeholder="请选择绑定项目">
                                <a-select-option v-for="project in projectList" :key="project.id" :value="project.id">{{
                                    project.name }}</a-select-option>
                            </a-select>
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
import { getProjectList } from '@/api/autotest/project'
import { getEnvironmentList, getEnvironmentDetail, createEnvironment, updateEnvironment, deleteEnvironment } from '@/api/autotest/environment'
import type { searchDataType, tableDataType, projectSeletorType } from './types'

const columns: TableColumnsType = [
    {
        title: '序号',
        dataIndex: 'index',
        align: 'center',
        ellipsis: true,
        width: 80
    },
    {
        title: '环境名称',
        dataIndex: 'name',
        ellipsis: true,
    },
    {
        title: '环境地址',
        dataIndex: 'base_url',
        ellipsis: true,
    },
    {
        title: '绑定项目',
        dataIndex: 'project_id',
        ellipsis: true,
        customRender: ({ text }) => {
            const project = projectList.value.find(p => p.id === text);
            return project ? project.name : '-';
        }
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
    project_id: undefined,
    description: ''
})
const updateState = reactive<tableDataType>({
    id: undefined,
    name: '',
    base_url: '',
    project_id: undefined,
    description: ''
})
const detailState = ref<tableDataType>({})

const projectList = ref<projectSeletorType[]>([]);

const handProjectList = () => {
    tableLoading.value = true;
    let params = {};
    getProjectList(params).then(response => {
        const result = response.data;
        projectList.value = result.data.items;

    }).catch(error => {
        console.log(error);
    }).finally(() => {
        tableLoading.value = false;
    });
}

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
    if (currentProjectId.value) {
        params['project_id'] = currentProjectId.value;
    }
    params['page_no'] = pagination.current
    params['page_size'] = pagination.pageSize

    getEnvironmentList(params).then(response => {
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
    handProjectList(); // 新增：获取项目列表
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
    deleteEnvironment({ id: row.id }).then(response => {
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

            createEnvironment(createBody).then(response => {
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
            updateEnvironment(updateState).then(response => {
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

// 新增项目选择相关变量
const selectedProject = ref<string[]>(['all']);
const currentProjectId = ref<number | null>(null);

// 添加树结构数据处理
const treeData = computed(() => {
    return [
        {
            title: '全部项目',
            key: 'all',
            children: projectList.value.map(project => ({
                title: project.name,
                key: String(project.id)
            }))
        }
    ];
});

// 修改项目选择处理逻辑
const handleProjectSelect = (selectedKeys: string[]) => {
    if (selectedKeys.length > 0) {
        const key = selectedKeys[0];
        currentProjectId.value = key === 'all' ? null : Number(key);
        selectedProject.value = [key];
        pagination.current = 1;
        loadingData();
    }
};

</script>

<style lang="scss" scoped>

.table-search-wrapper {
    margin-block-end: 16px;
}
</style>