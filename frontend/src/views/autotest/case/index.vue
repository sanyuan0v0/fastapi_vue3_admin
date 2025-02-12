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
            <a-card :bordered="false">
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
                    <span>{{ modalTitle === 'create' ? '新建接口用例' : (modalTitle === 'view' ? '查看接口用例' : '修改接口用例')
                        }}</span>
                </template>
                <div v-if="modalTitle === 'view'">
                    <a-spin :spinning="detailStateLoading">
                        <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }"
                            :labelStyle="{ width: '140px' }" bordered>
                            <a-descriptions-item label="序号">{{ (pagination.current - 1) * pagination.pageSize +
                                detailState.index + 1 }}</a-descriptions-item>
                            <a-descriptions-item label="接口名称">{{ detailState.name }}</a-descriptions-item>
                            <a-descriptions-item label="状态">{{ detailState.status ? '启用' : '禁用' }}</a-descriptions-item>
                            <a-descriptions-item label="接口地址">{{ detailState.url }}</a-descriptions-item>
                            <a-descriptions-item label="请求方法">{{ detailState.method }}</a-descriptions-item>
                            <a-descriptions-item label="请求头">{{ JSON.stringify(detailState.headers)
                                }}</a-descriptions-item>
                            <a-descriptions-item label="Query参数">{{ JSON.stringify(detailState.params)
                                }}</a-descriptions-item>
                            <a-descriptions-item label="请求体">{{ JSON.stringify(detailState.body)
                                }}</a-descriptions-item>
                            <a-descriptions-item label="上传文件">{{ JSON.stringify(detailState.files)
                                }}</a-descriptions-item>
                            <a-descriptions-item label="断言配置">{{ JSON.stringify(detailState.expected)
                                }}</a-descriptions-item>
                            <a-descriptions-item label="绑定项目">{{ detailState.project?.name || '-'
                                }}</a-descriptions-item>
                            <a-descriptions-item label="绑定参数">{{ detailState.parameter_need ? '是' : '否'
                                }}</a-descriptions-item>
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
                        <a-form-item name="name" label="接口名称" :rules="[{ required: true, message: '请输入接口名称' }]">
                            <a-input v-model:value="createState.name" placeholder="请输入接口名称" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="status" label="状态">
                            <a-switch v-model:checked="createState.status" />
                        </a-form-item>
                        <a-form-item name="url" label="接口地址" :rules="[{ required: true, message: '请输入接口地址' }]">
                            <a-input v-model:value="createState.url" placeholder="请输入接口地址" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="method" label="请求方法" :rules="[{ required: true, message: '请选择请求方法' }]">
                            <a-select v-model:value="createState.method" placeholder="请选择请求方法">
                                <a-select-option v-for="method in HTTP_METHODS" :key="method" :value="method">{{ method
                                    }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="headers" label="请求头">
                            <json-editor v-model:value="createState.headers" mode="code" />
                        </a-form-item>
                        <a-form-item name="params" label="Query参数">
                            <json-editor v-model:value="createState.params" mode="code" />
                        </a-form-item>
                        <a-form-item name="body" label="请求体">
                            <json-editor v-model:value="createState.body" mode="code" />
                        </a-form-item>
                        <a-form-item name="files" label="上传文件">
                            <json-editor v-model:value="createState.files" mode="code" />
                        </a-form-item>
                        <a-form-item name="expected" label="断言配置" :rules="[{ required: true, message: '请设置断言配置' }]">
                            <a-space v-for="(assertion, index) in createState.expected" :key="index"
                                style="display: flex; margin-bottom: 8px">
                                <a-select v-model:value="assertion.type" style="width: 120px">
                                    <a-select-option value="status_code">状态码</a-select-option>
                                    <a-select-option value="msg">消息</a-select-option>
                                    <a-select-option value="response">响应</a-select-option>
                                </a-select>
                                <a-select v-model:value="assertion.rule" style="width: 120px">
                                    <a-select-option value="equals">等于</a-select-option>
                                    <a-select-option value="not_equals">不等于</a-select-option>
                                    <a-select-option value="contains">包含</a-select-option>
                                    <a-select-option value="not_contains">不包含</a-select-option>
                                    <a-select-option value="jsonpath">JsonPath</a-select-option>
                                    <a-select-option value="regex">正则</a-select-option>
                                </a-select>
                                <a-input v-model:value="assertion.expect" style="width: 200px" placeholder="预期值" />
                                <minus-circle-outlined @click="removeAssertion(index)" />
                            </a-space>
                            <a-button type="dashed" block @click="addAssertion">+ 添加断言</a-button>
                        </a-form-item>
                        <a-form-item name="project_id" label="绑定项目" :rules="[{ required: true, message: '请选择项目' }]">
                            <a-select v-model:value="createState.project_id" placeholder="请选择项目">
                                <a-select-option v-for="item in projectList" :key="item.id" :value="item.id">{{
                                    item.name
                                    }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="parameter_need" label="绑定参数">
                            <a-switch v-model:checked="createState.parameter_need" />
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
                        <a-form-item name="name" label="接口名称" :rules="[{ required: true, message: '请输入接口名称' }]">
                            <a-input v-model:value="updateState.name" placeholder="请输入接口名称" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="status" label="状态">
                            <a-switch v-model:checked="updateState.status" />
                        </a-form-item>
                        <a-form-item name="url" label="接口地址" :rules="[{ required: true, message: '请输入接口地址' }]">
                            <a-input v-model:value="updateState.url" placeholder="请输入接口地址" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="method" label="请求方法" :rules="[{ required: true, message: '请选择请求方法' }]">
                            <a-select v-model:value="updateState.method" placeholder="请选择请求方法">
                                <a-select-option v-for="method in HTTP_METHODS" :key="method" :value="method">{{ method
                                    }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="headers" label="请求头">
                            <json-editor v-model:value="updateState.headers" mode="code" />
                        </a-form-item>
                        <a-form-item name="params" label="Query参数">
                            <json-editor v-model:value="updateState.params" mode="code" />
                        </a-form-item>
                        <a-form-item name="body" label="请求体">
                            <json-editor v-model:value="updateState.body" mode="code" />
                        </a-form-item>
                        <a-form-item name="files" label="上传文件">
                            <json-editor v-model:value="updateState.files" mode="code" />
                        </a-form-item>
                        <a-form-item name="expected" label="断言配置" :rules="[{ required: true, message: '请设置断言配置' }]">
                            <a-space v-for="(assertion, index) in updateState.expected" :key="index"
                                style="display: flex; margin-bottom: 8px">
                                <a-select v-model:value="assertion.type" style="width: 120px">
                                    <a-select-option value="status_code">状态码</a-select-option>
                                    <a-select-option value="msg">消息</a-select-option>
                                    <a-select-option value="response">响应</a-select-option>
                                </a-select>
                                <a-select v-model:value="assertion.rule" style="width: 120px">
                                    <a-select-option value="equals">等于</a-select-option>
                                    <a-select-option value="not_equals">不等于</a-select-option>
                                    <a-select-option value="contains">包含</a-select-option>
                                    <a-select-option value="not_contains">不包含</a-select-option>
                                    <a-select-option value="jsonpath">JsonPath</a-select-option>
                                    <a-select-option value="regex">正则</a-select-option>
                                </a-select>
                                <a-input v-model:value="assertion.expect" style="width: 200px" placeholder="预期值" />
                                <minus-circle-outlined @click="removeAssertion(index)" />
                            </a-space>
                            <a-button type="dashed" block @click="addAssertion">+ 添加断言</a-button>
                        </a-form-item>
                        <a-form-item name="project_id" label="绑定项目" :rules="[{ required: true, message: '请选择项目' }]">
                            <a-select v-model:value="updateState.project_id" placeholder="请选择项目">
                                <a-select-option v-for="item in projectList" :key="item.id" :value="item.id">{{
                                    item.name
                                    }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="parameter_need" label="绑定参数">
                            <a-switch v-model:checked="updateState.parameter_need" />
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
import { ref, reactive, computed, unref, onMounted, h, watch } from 'vue';
import { Table, message, Modal } from 'ant-design-vue';
import type { TableColumnsType } from 'ant-design-vue';
import { PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined, MinusCircleOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { cloneDeep, isEmpty } from '@/utils/util';
import PageHeader from '@/components/PageHeader.vue';
import { getProjectList } from '@/api/autotest/project'
import { getCaseList, createCase, updateCase, deleteCase } from '@/api/autotest/case'
import type { searchDataType, tableDataType, projectSelectorType } from './types'

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
const detailState = ref<tableDataType>({});
const projectList = ref<projectSelectorType[]>([]);
const HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'];
const columns: TableColumnsType = [
    {
        title: '序号',
        dataIndex: 'index',
        align: 'center',
        ellipsis: true,
        width: 80
    },
    {
        title: '用例名称',
        width: 80,
        dataIndex: 'name',
        ellipsis: true,
    },
    {
        title: '绑定项目',
        dataIndex: 'project_id',
        width: 80,
        ellipsis: true,
        customRender: ({ text }) => {
            const project = projectList.value.find(p => p.id === text);
            return project ? project.name : '-';
        }
    },
    {
        title: '绑定参数',
        dataIndex: 'parameter_need',
        width: 80,
        ellipsis: true,
        customRender: ({ text }) => text ? '是' : '否'
    },
    {
        title: '接口地址',
        dataIndex: 'url',
        ellipsis: true,
    },
    {
        title: '请求方法',
        dataIndex: 'method',
        width: 80,
        ellipsis: true,
    },
    {
        title: '状态',
        dataIndex: 'status',
        width: 80,
        ellipsis: true,
        customRender: ({ text }) => text ? '启用' : '禁用'
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
        width: 180
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
    status: true,
    url: '',
    method: 'GET',
    headers: {},
    params: {},
    body: {},
    files: {},
    expected: [],
    project_id: undefined,
    parameter_need: false,
    description: ''
})

const updateState = reactive<tableDataType>({
    id: undefined,
    name: '',
    status: true,
    url: '',
    method: '',
    headers: {},
    params: {},
    body: {},
    files: {},
    expected: [],
    project_id: undefined,
    parameter_need: false,
    description: ''
})

// 获取项目列表
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


// 新增项目选择相关变量
const currentProjectId = ref<number | null>(null);


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

    getCaseList(params).then(response => {
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

// 删除
const deleteRow = (row: tableDataType) => {
    deleteCase({ id: row.id }).then(response => {
        const result = response.data;
        message.success(result.msg);
        loadingData();
    }).catch(error => {
        console.log(error)
    })
}

// 格式化请求数据
const formatRequestData = (formData: tableDataType) => {
    const data = { ...formData };

    // 确保 expected 数组格式正确
    if (data.expected && Array.isArray(data.expected)) {
        data.expected = data.expected.map(item => ({
            type: item.type,
            rule: item.rule,
            expect: item.expect
        }));
    }

    return data;
};

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
};

// 弹窗提交（详情/新建/修改）
const handleModalSumbit = () => {
    modalSubmitLoading.value = true;

    const form = modalTitle.value === 'create' ? createForm.value : updateForm.value;
    form?.validate().then(() => {
        const formData = modalTitle.value === 'create' ? createState : updateState;
        const apiMethod = modalTitle.value === 'create' ? createCase : updateCase;

        const requestData = formatRequestData(formData);

        apiMethod(requestData).then(response => {
            message.success(response.data.msg);
            openModal.value = false;
            loadingData();
        }).catch(error => {
            console.error(error);
        }).finally(() => {
            modalSubmitLoading.value = false;
        });
    }).catch(error => {
        console.error(error);
        modalSubmitLoading.value = false;
    });
}

// 添加断言方法
const addAssertion = () => {
    if (!createState.expected) {
        createState.expected = [];
    }
    createState.expected.push({
        type: 'status_code',
        rule: 'equals',
        expect: ''
    });
};

// 移除断言方法
const removeAssertion = (index: number) => {
    createState.expected?.splice(index, 1);
};


</script>

<style lang="scss" scoped>
.table-search-wrapper {
    margin-block-end: 16px;
}
</style>
