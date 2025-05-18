<template>
  <div>


    <!-- 搜索表单 -->
    <div class="table-search-wrapper">
      <a-card :bordered="false">
        <a-form :model="queryState" @finish="onFinish">
          <a-flex wrap="wrap" gap="small">
              <a-form-item name="request_path" label="请求路径" >
                <a-input v-model:value="queryState.request_path" placeholder="请输入请求路径" allowClear></a-input>
              </a-form-item>
              <a-form-item name="creator" label="创建人" >
                <a-select v-model:value="queryState.creator_name" placeholder="请选择创建人" :open="false"
                  @click="selectModalHandle">
                  <template #suffixIcon>
                    <search-outlined />
                  </template>
                </a-select>
              </a-form-item>
              <a-form-item name="date-range-picker" label="创建日期" style="max-width: 350px;">
                <a-range-picker v-model:value="queryState.date_range" value-format="YYYY-MM-DD" />
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
      <a-card title="日志列表"
        :bordered="false"
        :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
      :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 360px)' }">
        <template #extra>
          <a-button type="primary" :icon="h(DownOutlined)" @click="handleExport"
            style="margin-right: 10px;">
            导出
          </a-button>
        </template>
        <a-table
          :rowKey="record => record.id"
          :columns="columns"
          :data-source="dataSource"
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
            <template v-if="column.dataIndex === 'request_method'">
              <a-tag :color="getRequestMethodColor(record.request_method)">{{ record.request_method }}</a-tag>
            </template>
            <template v-if="column.dataIndex === 'response_code'">
              <a-tag :color="record.response_code === 200 ? 'green' : 'red'">{{ record.response_code }}</a-tag>
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <a-space size="middle">
                <a v-on:click="modalHandle('view', record, index)">查看</a>
                <a-popconfirm title="确定要删除吗?" @confirm="deleteRow(record)">
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
      <a-modal v-model:open="openModal" @ok="openModal = false" :width="800" :destroyOnClose="true" style="top: 30px">
        <template #title>
          <span>查看日志</span>
        </template>
        <a-spin :spinning="detailStateLoading">
          <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }"
            bordered>
            <a-descriptions-item label="序号">{{ (pagination.current - 1) * pagination.pageSize + detailState.index + 1 }}</a-descriptions-item>
            <a-descriptions-item label="请求地址" >{{ detailState.request_path }}</a-descriptions-item>
            <a-descriptions-item label="请求方法">
              <a-tag :color="getRequestMethodColor(detailState.request_method)">{{ detailState.request_method }}</a-tag>
            </a-descriptions-item>
            <a-descriptions-item label="IP地址">{{ detailState.request_ip }}</a-descriptions-item>
            <a-descriptions-item label="登录地址">{{ detailState.login_location }}</a-descriptions-item>
            <a-descriptions-item label="浏览器">{{ detailState.request_browser }}</a-descriptions-item>
            <a-descriptions-item label="系统">{{ detailState.request_os }}</a-descriptions-item>
            <a-descriptions-item label="响应码" :span="2">
              <a-tag :color="detailState.response_code === 200 ? 'green' : 'red'">{{ detailState.response_code
                }}</a-tag>
            </a-descriptions-item>
            <a-descriptions-item label="请求体" :span="2">{{ detailState.request_payload }}</a-descriptions-item>
            <a-descriptions-item label="返回信息" :span="2">
              <div class="scrollable-content">{{ detailState.response_json }}</div>
            </a-descriptions-item>
            <a-descriptions-item label="处理时间" :span="2">{{ detailState.process_time }} </a-descriptions-item>
            <a-descriptions-item label="创建人">{{ detailState.creator ? detailState.creator.name : '-' }}</a-descriptions-item>
            <a-descriptions-item label="创建时间">{{ detailState.created_at }}</a-descriptions-item>
            <a-descriptions-item label="修改时间">{{ detailState.updated_at }}</a-descriptions-item>
            <a-descriptions-item label="备注">{{ detailState.description }}</a-descriptions-item>
          </a-descriptions>
        </a-spin>
      </a-modal>
    </div>

    <!-- 选择人弹窗 -->
    <SelectorModal ref="selectorModal" @event="handleSelectorModalEvent" />
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, h } from 'vue';
import type { TableColumnsType } from 'ant-design-vue';
import { SearchOutlined, DownOutlined, DownloadOutlined } from '@ant-design/icons-vue';
import { message, Modal } from 'ant-design-vue';
import type { searchDataType, tableDataType, creatorType } from './types'
import { getLogList, deleteLog, exportLog } from '@/api/system/log'
import SelectorModal from './SelectorModal.vue'
import XLSX from 'xlsx';

const tableLoading = ref(false);
const dataSource = ref<tableDataType[]>([]);
const detailStateLoading = ref(false);
const openModal = ref(false);
const selectorModal = ref();

const pagination = reactive({
  current: 1,
  pageSize: 10,
  defaultPageSize: 10,
  showSizeChanger: true,
  total: dataSource.value.length,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
});
const queryState = reactive<searchDataType>({});
const detailState = ref<tableDataType>({});
const columns: TableColumnsType = [
  {
    title: '序号',
    dataIndex: 'index',
    align: 'center',
    width: 80
  },
  {
    title: '请求地址',
    dataIndex: 'request_path',
    ellipsis: true,
    // align: 'center',
    // width: 200
  },
  {
    title: '请求方法',
    dataIndex: 'request_method',
    ellipsis: true,
    // align: 'center',
    width: 80
  },
  {
    title: 'IP地址',
    dataIndex: 'request_ip',
    ellipsis: true,
    // align: 'center',
    width: 100
  },
  {
    title: '登录地点',
    dataIndex: 'login_location',
    ellipsis: true,
    // align: 'center',
    width: 120
  },
  {
    title: '浏览器',
    dataIndex: 'request_browser',
    ellipsis: true,
    // align: 'center',
    width: 80
  },
  {
    title: '系统',
    dataIndex: 'request_os',
    ellipsis: true,
    // align: 'center',
    width: 80
  },
  {
    title: '响应码',
    dataIndex: 'response_code',
    ellipsis: true,
    // align: 'center',
    width: 80
  },
  {
    title: '处理时间',
    dataIndex: 'process_time',
    ellipsis: true,
    // align: 'center',
    width: 120
  },
  {
    title: '描述',
    dataIndex: 'description',
    // align: 'center',
    ellipsis: true,
    width: 120
  },
  {
    title: '创建日期',
    dataIndex: 'created_at',
    // align: 'center',
    ellipsis: true,
    width: 180
  },
  {
    title: '操作',
    dataIndex: 'operation',
    align: 'center',
    fixed: 'right',
    width: 150
  }
];

// 生命周期钩子
onMounted(() => loadingData());

// 查询
const onFinish = () => {
  pagination.current = 1;
  loadingData();
};

// 加载表格数据
const loadingData = () => {
  tableLoading.value = true;

  let params = {};

  if (queryState.request_path) {
    params['request_path'] = queryState.request_path
  }

  if (queryState.creator) {
    params['creator'] = queryState.creator
  }

  if (queryState.date_range) {
    params['start_time'] = `${queryState.date_range[0]} 00:00:00`;
    params['end_time'] = `${queryState.date_range[1]} 23:59:59`;
  }
  params['page_no'] = pagination.current;
  params['page_size'] = pagination.pageSize;

  getLogList(params).then(response => {
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
};

// 获取请求方法颜色
const getRequestMethodColor = (method: string) => {
  const methodColors = {
    GET: 'green',
    POST: 'blue',
    PUT: 'orange',
    DELETE: 'red',
    PATCH: 'purple',
    HEAD: 'gray',
    OPTIONS: 'cyan',
  };
  return methodColors[method] || 'black'; // 默认颜色为黑色
};

// 重置查询
const resetFields = () => {
  Object.keys(queryState).forEach((key: string) => {
    delete queryState[key];
  });
  pagination.current = 1;
  loadingData();
};

// 删除
const deleteRow = (row: tableDataType) => {
  deleteLog({ id: row.id }).then(response => {
    const result = response.data;
    message.success(result.msg);
    loadingData();
  }).catch(error => {
    console.log(error)
  })
};

// 表格分页
const handleTableChange = (values: any) => {
  pagination.current = values.current;
  pagination.pageSize = values.pageSize;
  loadingData();
};

// 查看
const modalHandle = (modalType: string, record?: tableDataType, index?: number) => {
  if (modalType === 'view' && record !== undefined) {
    openModal.value = true;

    detailStateLoading.value = true;

    detailState.value = record;
    detailState.value.index = index;

    detailStateLoading.value = false;
  }
};

// 选择人弹窗
const selectModalHandle = () => {
  selectorModal.value.openModal = true;
  selectorModal.value.selectedRowKeys = [queryState.creator];
  selectorModal.value.selectedRowName = queryState.creator_name;
  selectorModal.value.loadingData();
};

// 选择人弹窗事件
const handleSelectorModalEvent = (selectedSelectorRowKeys?: creatorType['id'][], selectedSelectorRowName?: creatorType['name']) => {
  const creator = selectedSelectorRowKeys.length ? selectedSelectorRowKeys[0] : undefined;
  const creator_name = selectedSelectorRowName || undefined;

  queryState.creator = creator;
  queryState.creator_name = creator_name;
};

/** 导出按钮操作 */
const handleExport = () => {
  Modal.confirm({
    title: '警告',
    content: '是否确认导出所有日志数据?',
    onOk() {
      const body = {
        ...queryState,
        page_no: 1,
        page_size: pagination.total
      };
      message.loading('正在导出数据，请稍候...', 0);

      return exportLog(body).then(response => {
        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        // 从响应头获取文件名
        const contentDisposition = response.headers['content-disposition'];
        let fileName = '系统日志.xlsx';
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

.scrollable-content {
  max-height: 200px;
  /* 设置最大高度 */
  overflow-y: auto;
  /* 添加垂直滚动条 */
  white-space: pre-wrap;
  /* 保留换行符并允许文本换行 */
}

.json-viewer {
  max-height: 300px;
  overflow-y: auto;
}
</style>