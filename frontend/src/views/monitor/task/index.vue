<template>
    <div>
        <!-- 页面头部 -->
        <page-header />

        <!-- 表格区域 -->
        <div class="table-wrapper">
            <a-card title="任务管理列表" 
                :bordered="false" 
                :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
                :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 250px)' }">
                <template #extra>
                    <a-button type="primary" :icon="h(PlusOutlined)" @click="handleOpenModal('create')" style="margin-right: 10px;">
                        新建
                    </a-button>
                </template>
                <a-table :rowKey="record => record.task_id" 
                    :columns="columns" 
                    :data-source="dataSource"
                    :loading="tableLoading" 
                    :scroll="{ x: 400 }" 
                    :style="{ minHeight: '420px' }">
                    <template #bodyCell="{ column, record }">
                        <template v-if="column.dataIndex === 'operation'">
                            <a-space size="middle">
                                <a @click="viewTaskDetail(record)">查看</a>
                                <a-popconfirm title="确定取消吗？" ok-text="确定" cancel-text="取消" @confirm="cancelTaskID(record.task_id)">
                                    <a style="color: blue;">取消</a>
                                </a-popconfirm>
                                <a-popconfirm title="确定删除吗？" ok-text="确定" cancel-text="取消" @confirm="deleteTaskID(record.task_id)">
                                    <a style="color: red;">删除</a>
                                </a-popconfirm>
                            </a-space>
                        </template>
                    </template>
                </a-table>
            </a-card>
        </div>

        <!-- 弹窗区域 -->
        <a-modal v-model:open="openModal" @ok="handleModalSubmit" :width="800" :destroyOnClose="true"
            :confirmLoading="modalSubmitLoading" style="top: 30px">
            <template #title>
                <span>{{ modalTitle === 'create' ? '新建任务' : '查看任务' }}</span>
            </template>
            <div v-if="modalTitle === 'view'">
                <a-spin :spinning="detailLoading">
                    <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }"
                        :labelStyle="{ width: '140px' }" bordered>
                        <a-descriptions-item label="任务编号">{{ taskDetail.task_id || '无' }}</a-descriptions-item>
                        <a-descriptions-item label="任务状态">{{ taskDetail.status || '无' }}</a-descriptions-item>
                        <a-descriptions-item label="任务结果">
                            {{ typeof taskDetail.result === 'object' ? JSON.stringify(taskDetail.result, null, 2) : taskDetail.result || '无' }}
                        </a-descriptions-item>
                        <a-descriptions-item label="任务完成日期">
                            {{ taskDetail.date_done ? dayjs(taskDetail.date_done).format('YYYY-MM-DD HH:mm:ss') : '无' }}
                        </a-descriptions-item>
                    </a-descriptions>
                </a-spin>
            </div>
            <div v-else-if="modalTitle === 'create'">
                <a-form ref="createForm" :model="createFormState"
                    :labelCol="{ span: 5 }" :wrapperCol="{ span: 15 }">
                    <a-form-item name="res" label="任务参数" :rules="[{ required: true, message: '请输入任务参数' }]">
                        <a-input v-model:value="createFormState.res" placeholder="请输入任务参数" allowClear />
                    </a-form-item>
                    <a-form-item name="is_cron" label="是否开启定时任务">
                        <a-switch v-model:checked="createFormState.is_cron" />
                    </a-form-item>
                    <a-form-item v-if="createFormState.is_cron" name="cron_expression" label="定时策略" :rules="[{ required: true, message: '请输入定时策略' }]">
                        <a-input v-model:value="createFormState.cron_expression" placeholder="请输入 Cron 表达式" allowClear />
                    </a-form-item>
                </a-form>
            </div>
        </a-modal>
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, h } from 'vue';
import { message } from 'ant-design-vue';
import type { TableColumnsType } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { cloneDeep, isEmpty } from '@/utils/util';
import PageHeader from '@/components/PageHeader.vue';
import { getTaskList, getTaskDetail, createTask, cancelTask, deleteTask } from '@/api/monitor/task';
import dayjs from 'dayjs';

// 类型定义
interface Task {
    task_id?: string;
    result?: string;
    status?: string;
    date_done?: string;
    res?: string;
    is_cron?: boolean;
    cron_expression?: string;
}

// 状态管理
const tableLoading = ref(false);
const openModal = ref(false);
const modalTitle = ref<'create' | 'view'>('create');
const modalSubmitLoading = ref(false);
const detailLoading = ref(false);
const dataSource = ref<Task[]>([]);
const taskDetail = ref<Task>({});
const createFormState = reactive<Task>({
    res: '',
    is_cron: false,
    cron_expression: '',
});

const createForm = ref(); // 表单引用

// 表格列配置
const columns: TableColumnsType = [
    {
        title: '任务编号',
        dataIndex: 'task_id',
        ellipsis: true,
    },
    {
        title: '任务状态',
        dataIndex: ['result', 'status'],
        ellipsis: true,
    },
    {
        title: '任务结果',
        dataIndex: ['result', 'result'],
        ellipsis: true,
        customRender: ({ text }) => {
            if (text && text.exc_type) {
                return `异常: ${text.exc_type} - ${text.exc_message.join(', ')}`;
            }
            return text || '无';
        },
    },
    {
        title: '完成时间',
        dataIndex: ['result', 'date_done'],
        ellipsis: true,
        customRender: ({ text }) => {
            return text ? dayjs(text).format('YYYY-MM-DD HH:mm:ss') : '无';
        },
    },
    {
        title: '操作',
        dataIndex: 'operation',
        align: 'center',
        fixed: 'right',
        ellipsis: true,
        width: 180,
    },
];

// 加载表格数据
const loadTableData = async () => {
    tableLoading.value = true;
    try {
        const response = await getTaskList();
        dataSource.value = response.data.data; // 移除 index 字段
    } catch (error) {
        message.error('加载任务列表失败');
    } finally {
        tableLoading.value = false;
    }
};

// 查看任务详情
const viewTaskDetail = async (record: Task) => {
    detailLoading.value = true;
    try {
        const response = await getTaskDetail(record.task_id!);
        taskDetail.value = response.data.data;
        modalTitle.value = 'view';
        openModal.value = true;
    } catch (error) {
        message.error('获取任务详情失败');
    } finally {
        detailLoading.value = false;
    }
};

// 取消任务
const cancelTaskID = async (taskId: string) => {
    try {
        const response = await cancelTask(taskId);
        message.success(response.data.msg);
        loadTableData();
    } catch (error) {
        message.error('取消任务失败');
    }
};

// 删除任务
const deleteTaskID = async (taskId: string) => {
    try {
        const response = await deleteTask(taskId);
        message.success(response.data.msg);
        loadTableData();
    } catch (error) {
        message.error('删除任务失败');
    }
};

// 提交新建任务
const handleModalSubmit = async () => {
    try {
        await createForm.value.validate(); // 确保表单验证通过
        const createBody = cloneDeep(createFormState);

        // 如果未开启定时任务，移除 cron_expression 字段
        if (!createBody.is_cron) {
            delete createBody.cron_expression;
        }

        // 提交任务
        const response = await createTask(createBody);
        message.success(response.data.msg);
        openModal.value = false;
        createForm.value.resetFields(); // 重置表单
        loadTableData();
    } catch (error) {
        if (error.errorFields) {
            message.error('请填写完整任务参数');
        } else {
            message.error('创建任务失败');
        }
    }
};

// 打开弹窗
const handleOpenModal = (type: 'create' | 'view') => {
    modalTitle.value = type;
    openModal.value = true;
    if (type === 'create') {
        createForm.value?.resetFields(); // 重置表单
    }
};

// 生命周期钩子
onMounted(() => loadTableData());

</script>

<style lang="scss" scoped>
.table-wrapper {
    margin-block-end: 16px;
}
</style>