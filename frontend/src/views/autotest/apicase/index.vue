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
            <a-card title="接口用例列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
                :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 400px)' }">
                <template #extra>
                    <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')"
                        style="margin-right: 10px;">新建
                    </a-button>
                </template>
                <!-- 使用 a-row 和 a-col 划分左右布局 -->
                <a-row :gutter="20">
                    <!-- 左侧部门树 -->
                    <a-col :span="5">
                        <a-card :bordered="false">
                            <template #title>项目模块</template>
                            <template #extra>
                                <a-button type="link" size="small" @click="modalHandle('create-module')">
                                    <template #icon>
                                        <PlusOutlined />
                                    </template>
                                    添加模块
                                </a-button>
                            </template>
                            <a-tree v-model:selectedKeys="selectedKeys" v-model:expandedKeys="expandedKeys"
                                v-if="treeData.length" :tree-data="treeData" @select="handleTreeSelect" :showLine="true"
                                :defaultExpandAll="true">
                                <template #title="{ title, type, id }">
                                    <span>{{ title }}</span>
                                    <span v-if="type === 'module'" class="module-actions">
                                        <a-tooltip title="查看">
                                            <EyeOutlined @click.stop="modalHandle('view-module', id)" />
                                        </a-tooltip>
                                        <a-tooltip title="编辑">
                                            <EditOutlined @click.stop="modalHandle('update-module', id)" />
                                        </a-tooltip>
                                        <a-tooltip title="删除">
                                            <DeleteOutlined @click.stop="handleDeleteModule(id)" />
                                        </a-tooltip>
                                    </span>
                                </template>
                            </a-tree>
                        </a-card>
                    </a-col>

                    <!-- 右侧用例列表 -->
                    <a-col :span="19">
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
                                        <a-popconfirm title="确定删除吗？" ok-text="确定" cancel-text="取消"
                                            @confirm="deleteRow(record)">
                                            <a style="color: red;">删除</a>
                                        </a-popconfirm>
                                        <a @click="handleDebug(record)">调试</a>
                                    </a-space>
                                </template>
                            </template>
                        </a-table>
                    </a-col>
                </a-row>

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
                            <a-descriptions-item label="接口用例名称">{{ detailState.name }}</a-descriptions-item>
                            <a-descriptions-item label="接口地址">{{ detailState.url }}</a-descriptions-item>
                            <a-descriptions-item label="请求方法">{{ detailState.method }}</a-descriptions-item>
                            <a-descriptions-item label="请求头">{{ detailState.headers }}</a-descriptions-item>
                            <a-descriptions-item label="参数类型">{{ detailState.data_type }}</a-descriptions-item>
                            <a-descriptions-item label="请求参数">{{ detailState.data }}</a-descriptions-item>
                            <a-descriptions-item label="预期状态码">{{ detailState.expected_status_code }}</a-descriptions-item>
                            <a-descriptions-item label="预期消息">{{ detailState.expected_msg }}</a-descriptions-item>
                            <a-descriptions-item label="预期响应">{{ detailState.expected_response }}</a-descriptions-item>
                            <a-descriptions-item label="状态码断言规则">{{ detailState.assertions_status_code }}</a-descriptions-item>
                            <a-descriptions-item label="消息断言规则">{{ detailState.assertions_msg }}</a-descriptions-item>
                            <a-descriptions-item label="响应断言规则">{{ detailState.assertions_response }}</a-descriptions-item>
                            <a-descriptions-item label="绑定模块">{{ moduleList.find(m => m.id ===
                                detailState.module_id)?.name || '-' }}</a-descriptions-item>
                            <a-descriptions-item label="绑定项目">{{ projectList.find(p => p.id ===
                                detailState.project_id)?.name || '-' }}</a-descriptions-item>
                            <a-descriptions-item label="绑定环境">{{ environmentList.find(e => e.id ===
                                detailState.environment_id)?.name || '-' }}</a-descriptions-item>
                            <a-descriptions-item label="绑定参数">{{ globalDataList.find(g => g.id ===
                                detailState.global_data_id)?.name || '-' }}</a-descriptions-item>
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
                        <a-form-item name="name" label="接口用例名称" :rules="[{ required: true, message: '请输入接口用例名称' }]">
                            <a-input v-model:value="createState.name" placeholder="请输入接口用例名称" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="url" label="接口地址" :rules="[{ required: true, message: '请输入接口地址' }]">
                            <a-input v-model:value="createState.url" placeholder="请输入接口地址" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="method" label="请求方法" :rules="[{ required: true, message: '请选择请求方法' }]">
                            <a-select v-model:value="createState.method" placeholder="请选择请求方法">
                                <a-select-option v-for="method in HTTP_METHODS" :key="method" :value="method">{{ method }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="headers" label="请求头" :rules="[{ required: true, message: '请输入请求头' }]">
                            <div>
                                <a-button type="link" @click="switchHeadersMode">切换为{{ isHeadersRaw ? 'KV模式' : 'Raw模式' }}</a-button>
                                <div v-if="!isHeadersRaw">
                                    <a-space style="display: flex; margin-bottom: 8px" v-for="(item, index) in headersKV" :key="index">
                                        <a-input v-model:value="item.key" placeholder="Key" style="width: 200px" />
                                        <a-input v-model:value="item.value" placeholder="Value" style="width: 200px" />
                                        <minus-circle-outlined @click="removeHeader(index)" />
                                    </a-space>
                                    <a-button type="dashed" block @click="addHeader">+ 添加请求头</a-button>
                                </div>
                                <a-input v-else v-model:value="createState.headers" type="textarea" :rows="4" placeholder="请输入请求头(JSON格式)" />
                            </div>
                        </a-form-item>
                        <a-form-item name="data_type" label="参数类型" :rules="[{ required: true, message: '请选择参数类型' }]">
                            <a-select v-model:value="createState.data_type" placeholder="请选择参数类型">
                                <a-select-option v-for="type in PARAMS_TYPES" :key="type" :value="type">{{ type }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="data" label="请求参数" :rules="[{ required: true, message: '请输入请求参数' }]">
                            <div>
                                <a-button type="link" @click="switchDataMode">切换为{{ isDataRaw ? 'KV模式' : 'Raw模式' }}</a-button>
                                <div v-if="!isDataRaw">
                                    <a-space style="display: flex; margin-bottom: 8px" v-for="(item, index) in dataKV" :key="index">
                                        <a-input v-model:value="item.key" placeholder="Key" style="width: 200px" />
                                        <a-input v-model:value="item.value" placeholder="Value" style="width: 200px" />
                                        <minus-circle-outlined @click="removeData(index)" />
                                    </a-space>
                                    <a-button type="dashed" block @click="addData">+ 添加参数</a-button>
                                </div>
                                <a-input v-else v-model:value="createState.data" type="textarea" :rows="4" placeholder="请输入请求参数(JSON格式)" />
                            </div>
                        </a-form-item>
                        <a-form-item name="expected_status_code" label="预期状态码"
                            :rules="[{ required: true, message: '请输入预期状态码' }]">
                            <a-input v-model:value="createState.expected_status_code" placeholder="请输入预期状态码"
                                allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="expected_msg" label="预期消息"
                            :rules="[{ required: true, message: '请输入预期消息' }]">
                            <a-input v-model:value="createState.expected_msg" placeholder="请输入预期消息"
                                allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="expected_response" label="预期响应"
                            :rules="[{ required: true, message: '请输入预期响应' }]">
                            <a-input v-model:value="createState.expected_response" placeholder="请输入预期响"
                                allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="assertions_status_code" label="状态码断言规则" :rules="[{ required: true, message: '请选择断言规则' }]">
                            <a-select v-model:value="createState.assertions_status_code" placeholder="请选择断言规则">
                                <a-select-option v-for="rule in ASSERTION_RULES" :key="rule" :value="rule">{{ rule }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="assertions_msg" label="消息断言规则" :rules="[{ required: true, message: '请选择消息断言规则' }]">
                            <a-select v-model:value="createState.assertions_msg" placeholder="请选择消息断言规则">
                                <a-select-option v-for="rule in ASSERTION_RULES" :key="rule" :value="rule">{{ rule }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="assertions_response" label="响应断言规则" :rules="[{ required: true, message: '请选择响应断言规则' }]">
                            <a-select v-model:value="createState.assertions_response" placeholder="请选择响应断言规则">
                                <a-select-option v-for="rule in ASSERTION_RULES" :key="rule" :value="rule">{{ rule }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="module_id" label="绑定模块" :rules="[{ required: true, message: '请选择绑定模块' }]">
                            <a-select v-model:value="createState.module_id" placeholder="请选择绑定模块">
                                <a-select-option v-for="module in moduleList" :key="module.id" :value="module.id">{{
                                    module.name }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="project_id" label="绑定项目" :rules="[{ required: true, message: '请选择绑定项目' }]">
                            <a-select v-model:value="createState.project_id" placeholder="请选择绑定项目">
                                <a-select-option v-for="project in projectList" :key="project.id" :value="project.id">{{
                                    project.name }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="environment_id" label="绑定环境" :rules="[{ required: true, message: '请选择绑定环境' }]">
                            <a-select v-model:value="createState.environment_id" placeholder="请选择绑定环境">
                                <a-select-option v-for="environment in environmentList" :key="environment.id" :value="environment.id">{{
                                    environment.name }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="global_data_id" label="绑定参数" :rules="[{ required: true, message: '请选择绑定参数' }]">
                            <a-select v-model:value="createState.global_data_id" placeholder="请选择绑定参数">
                                <a-select-option v-for="globalData in globalDataList" :key="globalData.id" :value="globalData.id">{{
                                    globalData.name }}</a-select-option>
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
                        <a-form-item name="name" label="接口用例名称" :rules="[{ required: true, message: '请输入接口用例名称' }]">
                            <a-input v-model:value="updateState.name" placeholder="请输入接口用例名称" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="url" label="接口地址" :rules="[{ required: true, message: '请输入接口地址' }]">
                            <a-input v-model:value="updateState.url" placeholder="请输入接口地址" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="method" label="请求方法" :rules="[{ required: true, message: '请选择请求方法' }]">
                            <a-input v-model:value="updateState.method" placeholder="请选择请求方法" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="headers" label="请求头" :rules="[{ required: true, message: '请输入请求头' }]">
                            <a-input v-model:value="updateState.headers" placeholder="请输入请求头" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="data_type" label="参数类型" :rules="[{ required: true, message: '请选择参数类型' }]">
                            <a-input v-model:value="updateState.data_type" placeholder="请选择参数类型" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="data" label="请求参数" :rules="[{ required: true, message: '请输入请求体' }]">
                            <a-input v-model:value="updateState.data" placeholder="请输入请求体" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="expected_status_code" label="预期状态码"
                            :rules="[{ required: true, message: '请输入预期状态码' }]">
                            <a-input v-model:value="updateState.expected_status_code" placeholder="请输入预期状态码"
                                allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="expected_msg" label="预期消息"
                            :rules="[{ required: true, message: '请输入预期消息' }]">
                            <a-input v-model:value="updateState.expected_msg" placeholder="请输入预期消息"
                                allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="expected_response" label="预期响应"
                            :rules="[{ required: true, message: '请输入预期响应' }]">
                            <a-input v-model:value="updateState.expected_response" placeholder="请输入预期响"
                                allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="assertions_status_code" label="状态码断言规则" :rules="[{ required: true, message: '请选择状态码断言规则' }]">
                            <a-input v-model:value="updateState.assertions_status_code" placeholder="请选择状态码断言规则" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="assertions_msg" label="消息断言规则" :rules="[{ required: true, message: '请选择消息断言规则' }]">
                            <a-input v-model:value="updateState.assertions_msg" placeholder="请选择消息断言规则" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="assertions_response" label="响应断言规则" :rules="[{ required: true, message: '请选择响应断言规则' }]">
                            <a-input v-model:value="updateState.assertions_response" placeholder="请选择响应断言规则" allowClear></a-input>
                        </a-form-item>
                        <a-form-item name="module_id" label="绑定模块" :rules="[{ required: true, message: '请选择绑定模块' }]">
                            <a-select v-model:value="updateState.module_id" placeholder="请选择绑定模块">
                                <a-select-option v-for="module in moduleList" :key="module.id" :value="module.id">{{
                                    module.name }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="project_id" label="绑定项目" :rules="[{ required: true, message: '请选择绑定项目' }]">
                            <a-select v-model:value="updateState.project_id" placeholder="请选择绑定项目">
                                <a-select-option v-for="project in projectList" :key="project.id" :value="project.id">{{
                                    project.name }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="environment_id" label="绑定环境" :rules="[{ required: true, message: '请选择绑定环境' }]">
                            <a-select v-model:value="updateState.environment_id" placeholder="请选择绑定环境">
                                <a-select-option v-for="environment in environmentList" :key="environment.id" :value="environment.id">{{
                                    environment.name }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="global_data_id" label="绑定参数" :rules="[{ required: true, message: '请选择绑定参数' }]">
                            <a-select v-model:value="updateState.global_data_id" placeholder="请选择绑定参数">
                                <a-select-option v-for="globalData in globalDataList" :key="globalData.id" :value="globalData.id">{{
                                    globalData.name }}</a-select-option>
                            </a-select>
                        </a-form-item>
                        <a-form-item name="description" label="备注">
                            <a-textarea v-model:value="updateState.description" placeholder="请输入备注" :rows="4"
                                allowClear />
                        </a-form-item>
                    </a-form>
                </div>
            </a-modal>

            <!-- 添加模块管理弹窗 -->
            <a-modal v-model:open="moduleModal.open" :title="moduleModal.title" @ok="handleModuleSubmit" :confirmLoading="moduleModal.loading" :width="800" style="top: 30px">
                <div v-if="moduleModal.type === 'view'">
                    <a-spin :spinning="detailStateLoading">
                        <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }" bordered>
                            <a-descriptions-item label="编号">{{ (moduleForm.id) }}</a-descriptions-item>
                            <a-descriptions-item label="模块名称">{{ moduleForm.name }}</a-descriptions-item>
                            <a-descriptions-item label="绑定项目">{{ projectList.find(p => p.id === moduleForm.project_id)?.name || '-' }}</a-descriptions-item>
                            <a-descriptions-item label="创建人">{{ moduleForm.creator ? moduleForm.creator.name : '-' }}</a-descriptions-item>
                            <a-descriptions-item label="创建时间">{{ moduleForm.created_at }}</a-descriptions-item>
                            <a-descriptions-item label="修改时间">{{ moduleForm.updated_at }}</a-descriptions-item>
                            <a-descriptions-item label="备注" :span="2">{{ moduleForm.description }}</a-descriptions-item>
                        </a-descriptions>
                    </a-spin>
                </div>
                <a-form v-else ref="moduleFormRef" :model="moduleForm"
                    v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
                    <a-form-item name="name" label="模块名称" :rules="moduleRules.name">
                        <a-input v-model:value="moduleForm.name" placeholder="请输入模块名称" allowClear />
                    </a-form-item>
                    <a-form-item name="project_id" label="绑定项目" :rules="moduleRules.project_id">
                        <a-select v-model:value="moduleForm.project_id" placeholder="请选择绑定项目">
                            <a-select-option v-for="project in projectList" :key="project.id" :value="project.id">{{ project.name }}</a-select-option>
                        </a-select>
                    </a-form-item>
                    <a-form-item name="description" label="备注">
                        <a-textarea v-model:value="moduleForm.description" placeholder="请输入备注" :rows="4" allowClear />
                    </a-form-item>
                </a-form>
            </a-modal>
        </div>

        <!-- 选择器弹窗 -->
        <DebugModel ref="debugModelRef" />
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, unref, onMounted, h } from 'vue';
import { Table, message, Modal } from 'ant-design-vue';
import type { TableColumnsType } from 'ant-design-vue';
import { PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined, MinusCircleOutlined } from '@ant-design/icons-vue';
import { cloneDeep, isEmpty } from '@/utils/util';
import PageHeader from '@/components/PageHeader.vue';
import { getProjectList } from '@/api/autotest/project'
import { getModuleList, createModule, updateModule, deleteModule  } from '@/api/autotest/module'
import { getEnvironmentList  } from '@/api/autotest/environment.js'
import { getGlobaldataList  } from '@/api/autotest/globaldata.js'
import { getApiCaseList, createApiCase, updateApiCase, deleteApiCase } from '@/api/autotest/apicase'
import type { searchDataType, tableDataType, projectSeletorType, moduleTableDataType, ModuleModalType, KeyValue, environmentTableDataType, globalDataTableDataType } from './types'
import DebugModel from './DebugModel.vue'

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
const projectList = ref<projectSeletorType[]>([]);
const moduleList = ref<moduleTableDataType[]>([]);
const environmentList = ref<environmentTableDataType[]>([]);
const globalDataList = ref<globalDataTableDataType[]>([]);
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
        title: '绑定模块',
        dataIndex: 'module_id',
        width: 80,
        ellipsis: true,
        customRender: ({ text }) => {
            const module = moduleList.value.find(m => m.id === text);
            return module ? module.name : '-';
        }
    },
    {
        title: '绑定环境',
        dataIndex: 'environment_id',
        width: 80,
        ellipsis: true,
        customRender: ({ text }) => {
            const environment = environmentList.value.find(m => m.id === text);
            return environment ? environment.name : '-';
        }
    },
    {
        title: '绑定参数',
        dataIndex: 'global_data_id',
        width: 80,
        ellipsis: true,
        customRender: ({ text }) => {
            const globalData = globalDataList.value.find(m => m.id === text);
            return globalData ? globalData.name : '-';
        }
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
    // {
    //     title: '备注',
    //     dataIndex: 'description',
    //     ellipsis: true,
    // },
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
    url: '',
    method: '',
    headers: '',
    data_type: '',
    data: '',
    expected_status_code: undefined,
    expected_msg: '',
    expected_response: '',
    assertions_status_code: '',
    assertions_msg: '',
    assertions_response: '',
    module_id: undefined,
    project_id: undefined,
    description: ''
})
const updateState = reactive<tableDataType>({
    id: undefined,
    name: '',
    url: '',
    method: '',
    headers: '',
    data_type: '',
    data: '',
    expected_status_code: undefined,
    expected_msg: '',
    expected_response: '',
    assertions_status_code: '',
    assertions_msg: '',
    assertions_response: '',
    module_id: undefined,
    project_id: undefined,
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

// 获取模块列表
const handModuleList = () => {
    tableLoading.value = true;
    let params = {};
    getModuleList(params).then(response => {
        const result = response.data;
        moduleList.value = result.data.items;
    }).catch(error => {
        console.log(error);
    }).finally(() => {
        tableLoading.value = false;
    });
}

// 获取环境列表
const handEnvironmentList = () => {
    tableLoading.value = true;
    let params = {};
    getEnvironmentList(params).then(response => {
        const result = response.data;
        environmentList.value = result.data.items;
    }).catch(error => {
        console.log(error);
    }).finally(() => {
        tableLoading.value = false;
    });
}

// 获取环境列表
const handGlobaldataList = () => {
    tableLoading.value = true;
    let params = {};
    getGlobaldataList(params).then(response => {
        const result = response.data;
        globalDataList.value = result.data.items;
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
    if (currentModuleId.value) {
        params['module_id'] = currentModuleId.value;
    }
    params['page_no'] = pagination.current
    params['page_size'] = pagination.pageSize

    getApiCaseList(params).then(response => {
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
    handModuleList(); // 新增：获取模块列表
    handEnvironmentList(); // 新增：获取环境列表
    handGlobaldataList(); // 新增：获取全局数据列表
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
    if (modalType === 'create-module') {
        moduleModal.title = '新建模块';
        moduleModal.type = 'create';
        moduleModal.open = true;
        // 使用类型定义的字段进行重置
        Object.assign(moduleForm, {
            id: null,
            name: '',
            project_id: undefined,
            description: '',
            created_at: '',
            updated_at: '',
            creator: null
        } as moduleTableDataType);
    } else if (modalType === 'update-module' && index) {
        const module = moduleList.value.find(m => m.id === index);
        if (module) {
            moduleModal.title = '修改模块';
            moduleModal.type = 'update';
            moduleModal.open = true;
            // 使用深拷贝来避免引用问题
            Object.assign(moduleForm, cloneDeep(module));
        }
    } else if (modalType === 'view-module' && index) {
        const module = moduleList.value.find(m => m.id === index);
        if (module) {
            moduleModal.title = '模块详情';
            moduleModal.type = 'view';
            moduleModal.open = true;
            // 使用深拷贝来避免引用问题
            Object.assign(moduleForm, cloneDeep(module));
        }
    } else {
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
}

// 删除
const deleteRow = (row: tableDataType) => {
    deleteApiCase({ id: row.id }).then(response => {
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

            createApiCase(createBody).then(response => {
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
            updateApiCase(updateState).then(response => {
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
const selectedKeys = ref<string[]>(['all']);
const currentProjectId = ref<number | null>(null);
const currentModuleId = ref<number | null>(null);
// 模块管理相关状态
const moduleModal = reactive({
    open: false,  
    title: '',
    loading: false,
    type: 'create' as ModuleModalType, // 使用类型断言
    id: null as number | null
});

const moduleForm = reactive<moduleTableDataType>({
    id: null,
    name: '',
    project_id: undefined,
    description: '',
    created_at: '',
    updated_at: '',
    creator: null
});

// 新增展开的keys
const expandedKeys = ref<string[]>([]);

// 优化树结构数据处理
const treeData = computed(() => {
    const data = [
        {
            title: '全部项目',
            key: 'all',
            children: projectList.value.map(project => ({
                title: project.name,
                key: `project-${project.id}`,
                type: 'project',
                children: moduleList.value
                    .filter(module => module.project_id === project.id)
                    .map(module => ({
                        title: module.name,
                        key: `module-${module.id}`,
                        type: 'module',
                        id: module.id
                    }))
            }))
        }
    ];

    // 计算需要展开的节点keys
    const keys = ['all'];
    data[0].children?.forEach(project => {
        keys.push(project.key);
        project.children?.forEach(module => {
            keys.push(module.key);
        });
    });
    expandedKeys.value = keys;

    return data;
});

// 修改项目选择处理逻辑
const handleTreeSelect = (selectedKeys: string[]) => {
    if (selectedKeys.length > 0) {
        const key = selectedKeys[0];
        if (key === 'all') {
            currentProjectId.value = null;
            currentModuleId.value = null;
        } else if (key.startsWith('project-')) {
            currentProjectId.value = Number(key.split('-')[1]);
            currentModuleId.value = null;
        } else if (key.startsWith('module-')) {
            const moduleId = Number(key.split('-')[1]);
            const module = moduleList.value.find(m => m.id === moduleId);
            if (module) {
                currentProjectId.value = module.project_id;
                currentModuleId.value = moduleId;
            }
        }
        loadingData();
    }
};

const handleModuleSubmit = () => {
    moduleModal.loading = true;
    if (moduleModal.type === 'create') {
        createModule(moduleForm)
            .then(response => {
                message.success('创建成功');
                moduleModal.open = false;
                // 使用类型定义的字段进行重置
                Object.assign(moduleForm, {
                    id: null,
                    name: '',
                    project_id: undefined,
                    description: '',
                    created_at: '',
                    updated_at: '',
                    creator: null
                } as moduleTableDataType);
                handModuleList();
            })
            .finally(() => {
                moduleModal.loading = false;
            });
    } else if (moduleModal.type === 'update') {
        updateModule(moduleForm)
            .then(response => {
                message.success('更新成功');
                moduleModal.open = false;
                handModuleList();
            })
            .finally(() => {
                moduleModal.loading = false;
            });
    }
};

const handleDeleteModule = (id: number) => {
    const module = moduleList.value.find(m => m.id === id);
    if (!module) return;

    Modal.confirm({
        title: '确认删除',
        content: `确定要删除模块"${module.name}"吗？删除后不可恢复,且会同时删除该模块下的所有接口用例。`,
        okText: '确认删除',
        okType: 'danger',
        cancelText: '取消',
        async onOk() {
            try {
                await deleteModule({ id });
                message.success('删除成功');
                
                // 如果删除的是当前选中的模块,重置选择
                if(currentModuleId.value === id) {
                    selectedKeys.value = ['all'];
                    currentModuleId.value = null;
                    currentProjectId.value = null;
                }
                
                await handModuleList();
                loadingData();
            } catch(error) {
                message.error('删除失败');
                console.error(error);
            }
        }
    });
};

// 优化模块表单校验规则
const moduleRules = {
    name: [
        { required: true, message: '请输入模块名称' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符' }
    ],
    project_id: [
        { required: true, message: '请选择所属项目' }
    ]
};

const debugModelRef = ref();

// 处理调试按钮点击
const handleDebug = (record: tableDataType) => {
    debugModelRef.value.debugModalState.open = true;

    // 初始化调试数据
    const debugRequest = debugModelRef.value.debugRequest;
    debugRequest.method = record.method || 'GET';
    debugRequest.url = record.url || '';

    // 处理Headers
    try {
        const headers = JSON.parse(record.headers || '{}');
        debugModelRef.value.headersList = Object.entries(headers).map(([key, value]) => ({
            key,
            value: String(value)
        }));
    } catch (e) {
        debugModelRef.value.headersList = [];
    }

    // 处理data
    if (record.data) {
        try {
            const body = JSON.parse(record.data);
            debugModelRef.value.bodyType = 'json';
            debugModelRef.value.jsonBody = JSON.stringify(body, null, 2);
        } catch (e) {
            debugModelRef.value.bodyType = 'none';
            debugModelRef.value.jsonBody = '';
        }
    } else {
        debugModelRef.value.bodyType = 'none';
    }
}

// 常量定义
const HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'];
const PARAMS_TYPES = ['params', 'data', 'json', 'file'];
const ASSERTION_RULES = ['=', '!=', '>', '<', '>=', '<=', 'in', 'not in'];

// KV相关状态
const isHeadersRaw = ref(true);
const isDataRaw = ref(true);
const headersKV = ref<KeyValue[]>([{ key: '', value: '' }]);
const dataKV = ref<KeyValue[]>([{ key: '', value: '' }]);

// KV操作函数
const addHeader = () => {
  headersKV.value.push({ key: '', value: '' });
};

const removeHeader = (index: number) => {
  headersKV.value.splice(index, 1);
};

const addData = () => {
  dataKV.value.push({ key: '', value: '' });
};

const removeData = (index: number) => {
  dataKV.value.splice(index, 1);
};

// 模式切换函数
const switchHeadersMode = () => {
  if (isHeadersRaw.value) {
    // Raw转KV
    try {
      const headersObj = JSON.parse(createState.headers || '{}');
      headersKV.value = Object.entries(headersObj).map(([key, value]) => ({
        key,
        value: String(value)
      }));
    } catch (e) {
      headersKV.value = [{ key: '', value: '' }];
    }
  } else {
    // KV转Raw
    const headersObj = {};
    headersKV.value.forEach(item => {
      if (item.key) {
        headersObj[item.key] = item.value;
      }
    });
    createState.headers = JSON.stringify(headersObj, null, 2);
  }
  isHeadersRaw.value = !isHeadersRaw.value;
};

const switchDataMode = () => {
  if (isDataRaw.value) {
    // Raw转KV
    try {
      const dataObj = JSON.parse(createState.data || '{}');
      dataKV.value = Object.entries(dataObj).map(([key, value]) => ({
        key,
        value: String(value)
      }));
    } catch (e) {
      dataKV.value = [{ key: '', value: '' }];
    }
  } else {
    // KV转Raw
    const dataObj = {};
    dataKV.value.forEach(item => {
      if (item.key) {
        dataObj[item.key] = item.value;
      }
    });
    createState.data = JSON.stringify(dataObj, null, 2);
  }
  isDataRaw.value = !isDataRaw.value;
};
</script>

<style lang="scss" scoped>
.table-search-wrapper {
    margin-block-end: 16px;
}

.module-actions {
    display: none;
    margin-left: 8px;
    
    .anticon {
        padding: 4px;
        margin-left: 4px;
        font-size: 14px;
        
        &:hover {
            color: #1890ff;
            background: rgba(24,144,255,0.1);
            border-radius: 4px;
        }
        
        &.anticon-delete:hover {
            color: #ff4d4f;
            background: rgba(255,77,79,0.1);
        }
    }
}

:deep(.ant-tree-node-content-wrapper:hover) {
    .module-actions {
        display: inline-flex;
        align-items: center;
    }
}

:deep(.ant-tree-treenode) {
    padding: 4px 0 !important;
    
    &:hover {
        background: #f5f5f5;
    }
}
</style>
