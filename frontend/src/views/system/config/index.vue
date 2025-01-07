<template>
    <div>
        <!-- 页面头部 -->
        <page-header />

        <!-- 搜索表单 -->
        <div class="tree-search-wrapper">
            <a-card :bordered="false">
                <a-form :model="queryState" @finish="onFinish">
                    <a-row>
                        <a-col flex="0 1 450px">
                            <a-form-item name="name" label="名称" style="max-width: 300px;">
                                <a-input v-model:value="queryState.name" placeholder="请输入名称" allowClear />
                            </a-form-item>
                        </a-col>
                    </a-row>
                    <a-row>
                        <a-col>
                            <a-space>
                                <a-button type="primary" html-type="submit" :loading="tableLoading">查询</a-button>
                                <a-button @click="resetFields">重置</a-button>
                            </a-space>
                        </a-col>
                    </a-row>
                </a-form>
            </a-card>
        </div>

        <!-- 表格区域 -->
        <div class="table-wrapper">
            <a-card title="配置列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
                :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 400px)' }">
                <template #extra>
                    <a-space>
                        <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')">新建</a-button>
                    </a-space>
                </template>

                <a-table :rowKey="record => record.id" :columns="columns" 
                    :data-source="dataSource"
                    :loading="tableLoading" 
                    :scroll="{ x: 500, y: 'calc(100vh - 500px)' }" 
                    :row-selection="rowSelection"
                    :pagination="false" :style="{ minHeight: '500px' }">
                    <template #bodyCell="{ column, record }">

                        <template v-if="column.dataIndex === 'action'">
                            <a-space size="middle">
                                <a @click="modalHandle('view', record)">查看</a>
                                <a @click="modalHandle('update', record)">修改</a>
                                <a-popconfirm title="确定要删除吗?" ok-text="确定" cancel-text="取消"
                                    @confirm="deleteRow(record)">
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
                    <span>{{ modalTitle === 'create' ? '新建配置' : (modalTitle === 'view' ? '查看配置' : '修改配置') }}</span>
                </template>

                <!-- 查看表单 -->
                <template v-if="modalTitle === 'view'">
                    <a-spin :spinning="detailStateLoading">
                        <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }" bordered>
                            <a-descriptions-item label="名称">{{ detailState.name }}</a-descriptions-item>
                            <a-descriptions-item label="排序">{{ detailState.order }}</a-descriptions-item>
                            <a-descriptions-item label="上级配置" :span="2">{{ detailState.parent_id}}</a-descriptions-item>
                            <a-descriptions-item label="键">{{ detailState.fied_key }}</a-descriptions-item>
                            <a-descriptions-item label="值">{{ detailState.fied_value }}</a-descriptions-item>
                        </a-descriptions>
                    </a-spin>
                </template>

                <!-- 新建表单 -->
                <template v-else-if="modalTitle === 'create'">
                    <a-form ref="createForm" :model="createState" :label-col="{ span: 5 }" :wrapper-col="{ span: 15 }">
                        <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
                            <a-input v-model:value="createState.name" placeholder="请输入名称" allowClear />
                        </a-form-item>

                        <a-form-item name="order" label="排序" :rules="[{ required: true, message: '请输入排序' }]">
                            <a-input-number v-model:value="createState.order" :min="1" />
                        </a-form-item>

                        <a-form-item name="parent_id" label="上级配置">
                            <a-tree-select
                                v-model:value="createState.parent_id"
                                :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
                                :tree-data="dataSource"
                                :field-names="{ children: 'children', label: 'name', value: 'id' }"
                                tree-node-filter-prop="name"
                                style="width: 100%"
                                show-search
                                allow-clear
                                placeholder="请选择上级配置"
                                />
                        </a-form-item>

                        <a-form-item name="fied_key" label="键" :rules="[{ required: true, message: '请输入键' }]">
                            <a-input v-model:value="createState.fied_key" placeholder="请输入键" allowClear />
                        </a-form-item>

                        <a-form-item name="fied_value" label="值">
                            <a-textarea v-model:value="createState.fied_value" placeholder="请输入值" :rows="4"allowClear />
                        </a-form-item>
                    </a-form>
                </template>

                <!-- 修改表单 -->
                <template v-else>
                    <a-form ref="updateForm" :model="updateState" :label-col="{ span: 5 }" :wrapper-col="{ span: 15 }">
                        <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
                            <a-input v-model:value="updateState.name" placeholder="请输入名称" allowClear />
                        </a-form-item>

                        <a-form-item name="order" label="排序" :rules="[{ required: true, message: '请输入排序' }]">
                            <a-input-number v-model:value="updateState.order" :min="1" />
                        </a-form-item>

                        <a-form-item name="parent_id" label="上级配置">
                            <a-tree-select
                                v-model:value="updateState.parent_id"
                                :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
                                :tree-data="dataSource"
                                :field-names="{ children: 'children', label: 'name', value: 'id' }"
                                tree-node-filter-prop="name"
                                style="width: 100%"
                                show-search
                                allow-clear
                                placeholder="请选择上级配置"
                                />
                        </a-form-item>

                        <a-form-item name="fied_key" label="键" :rules="[{ required: true, message: '请输入键' }]">
                            <a-input v-model:value="updateState.fied_key" placeholder="请输入键" allowClear />
                        </a-form-item>

                        <a-form-item name="fied_value" label="值">
                            <a-textarea v-model:value="updateState.fied_value" placeholder="请输入值" :rows="4"allowClear />
                        </a-form-item>
                    </a-form>
                </template>
            </a-modal>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted, h, unref } from 'vue';
import { message, Modal, Table } from 'ant-design-vue';
import type { MenuProps, TableColumnsType } from 'ant-design-vue';
import { PlusOutlined, DownOutlined, CheckOutlined, StopOutlined } from '@ant-design/icons-vue';
import { listToTree, cloneDeep, isEmpty } from '@/utils/util';
import { getConfigList, createConfig, updateConfig, deleteConfig } from '@/api/system/config';
import PageHeader from '@/components/PageHeader.vue'
import type { searchDataType, tableDataType } from './types';

// 响应式数据
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
});
const createState = reactive<tableDataType>({
    name: '',
    order: 1,
    parent_id: undefined,
    fied_key: null,
    fied_value: '',

});
const updateState = reactive<tableDataType>({
    id: undefined,
    name: '',
    order: 1,
    parent_id: undefined,
    fied_key: null,
    fied_value: '',
});
const detailState = ref<tableDataType>({});

const columns = reactive<TableColumnsType>([
    {
        title: '配置名称',
        dataIndex: 'name',
        ellipsis: true,
        key: 'name',
        // width: 160
    },
    {
        title: '排序',
        dataIndex: 'order',
        key: 'order',
        // align: 'center',
        ellipsis: true,
        // width: 100
    },
    {
        title: '父级',
        dataIndex: 'parent_id',
        key: 'parent_id',
        ellipsis: true,
        // align: 'center',
        // width: 100
    },
    {
        title: '键',
        dataIndex: 'fied_key',
        key: 'fied_key',
        ellipsis: true,
        // align: 'center'
    },
    {
        title: '值',
        dataIndex: 'fied_value',
        key: 'fied_value',
        ellipsis: true,
        // align: 'center'
    },
    {
        title: '操作',
        dataIndex: 'action',
        key: 'action',
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
    loadingData();
};

// 加载表格数据
const loadingData = () => {
    tableLoading.value = true;

    let params = {};
    if (queryState.name) {
        params['name'] = queryState.name;
    }
    getConfigList(params).then(response => {
        const result = response.data;
        dataSource.value = listToTree(result.data.items);
    }).catch(error => {
        console.log(error);
    }).finally(() => {
        tableLoading.value = false;
    });
};

// 重置查询
const resetFields = () => {
    Object.keys(queryState).forEach((key: string) => {
        delete queryState[key];
    });
    loadingData();
};

// 删除
const deleteRow = (row: tableDataType) => {
    deleteConfig({ id: row.id }).then(response => {
        const result = response.data;
        message.success(result.msg);
        loadingData();
    }).catch(error => {
        console.log(error);
    });
};


// 弹窗关键字处理
const modalHandle = (modalType: string, record?: tableDataType) => {
    modalTitle.value = modalType;
    openModal.value = true;

    if (modalType === 'view' && record !== undefined) {
        detailStateLoading.value = true;
        detailState.value = record
        detailStateLoading.value = false;

    } else if (modalType === 'update' && record !== undefined) {
        Object.keys(updateState).forEach(key => {
            updateState[key] = record[key];
        })
    }
};

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
            });

            createConfig(createBody).then(response => {
                const result = response.data;
                modalSubmitLoading.value = false;
                openModal.value = false;
                Object.keys(createState).forEach(key => delete createState[key]);
                createState.order = 1;
                message.success(result.msg);
                loadingData();
            }).catch(error => {
                console.error(error);
            });
        }).catch(error => {
            modalSubmitLoading.value = false;
            console.error(error)
        })

    } else if (modalTitle.value === 'update') {
        updateForm.value.validate().then(() => {
            updateConfig(updateState).then(response => {
                modalSubmitLoading.value = false;
                openModal.value = false;
                const result = response.data;
                message.success(result.msg);
                loadingData();

            }).catch(error => {
                modalSubmitLoading.value = false;
                console.error(error)
            });

        }).catch(error => {
            modalSubmitLoading.value = false;
            console.error(error)
        })
    }
};

</script>

<style lang="scss" scoped>
.tree-search-wrapper {
    margin-block-end: 16px;
}
</style>