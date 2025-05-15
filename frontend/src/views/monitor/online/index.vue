<template>


  <!-- 搜索表单 -->
  <div class="table-search-wrapper">
    <a-card :bordered="false">
      <a-form :model="queryState" @finish="handleQuery">
        
        <a-flex wrap="wrap" gap="small">
            <a-form-item name="ipaddr" label="主机" >
              <a-input v-model:value="queryState.ipaddr" placeholder="请输入主机地址" allowClear></a-input>
            </a-form-item>
            <a-form-item name="user_name" label="用户名" >
              <a-input v-model:value="queryState.name" placeholder="请输入登陆用户名称" allowClear></a-input>
            </a-form-item>
            <a-form-item name="login_location" label="登陆地点" >
              <a-input v-model:value="queryState.login_location" placeholder="请输入登陆地点" allowClear></a-input>
            </a-form-item>

        </a-flex>
        <a-row>
          <a-col>
            <a-button type="primary" html-type="submit" :loading="loading">查询</a-button>
            <a-button style="margin: 0 8px" @click="resetQuery">重置</a-button>
          </a-col>
        </a-row>
      </a-form>
    </a-card>
  </div>

  <div class="table-wrapper">
    <a-card title="在线用户列表"
      :bordered="false"
      :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
      :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 360px)' }">
      <a-table
        :rowKey="record => record.session_id"
        :columns="columns"
        :data-source="tableData"
        :loading="loading"
        :scroll="{ x: 400 }"
        :pagination="pagination"
                    :style="{ minHeight: 'calc(100vh - 420px)' }"
                    >
        <template #bodyCell="{ column, record, index }">
          <template v-if="column.dataIndex === 'index'">
            <span>{{ (pagination.current - 1) * pagination.pageSize + index + 1 }}</span>
          </template>
          <template v-if="column.dataIndex === 'operation'">
            <a-button type="link" @click="handleForceLogout(record)" danger>
              <template #icon>
                <DeleteOutlined />
                强退
              </template>
            </a-button>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>

</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { DeleteOutlined } from '@ant-design/icons-vue';
import { Modal, message } from 'ant-design-vue';
import { getOnlineList, deleteOnline} from "@/api/monitor/online";
import type { QueryState, OnlineUser } from './types';

const onlineList = ref<OnlineUser[]>([]);
const loading = ref(false);
const total = ref(0);
const pageNum = ref(1);
const pageSize = ref(10);

const queryState = ref<QueryState>({
  ipaddr: undefined,
  name: undefined
});

const columns = [
  { title: '会话编号', dataIndex: 'session_id', key: 'sessionId', ellipsis: true },
  { title: '登录名称', dataIndex: 'name', key: 'name', align: 'center', ellipsis: true },
  { title: '用户账号', dataIndex: 'user_name', key: 'userName', align: 'center', ellipsis: true },
  { title: '主机', dataIndex: 'ipaddr', key: 'ipaddr', align: 'center', ellipsis: true },
  { title: '登录地点', dataIndex: 'login_location', key: 'loginLocation', align: 'center', ellipsis: true },
  { title: '操作系统', dataIndex: 'os', key: 'os', align: 'center', ellipsis: true },
  { title: '浏览器', dataIndex: 'browser', key: 'browser', align: 'center', ellipsis: true },
  { title: '登录时间', dataIndex: 'login_time', key: 'loginTime', align: 'center', ellipsis: true, width: 180 },
  { title: '操作', dataIndex: 'operation', key: 'operation', align: 'center', width: 120 }
];

const pagination = reactive({
  current: 1,
  pageSize: 10,
  defaultPageSize: 10,
  showSizeChanger: true,
  total: onlineList.value.length,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})

const tableData = computed(() => {
  if (!onlineList.value) return [];
  const start = (pageNum.value - 1) * pageSize.value;
  return onlineList.value.slice(start, start + pageSize.value);
});

const getList = async () => {
  try {
    loading.value = true;
    const response = await getOnlineList(queryState.value);
    onlineList.value = response?.data?.data?.items || [];
    total.value = response?.data?.data?.total || 0;
  } catch (error) {
    message.error('获取数据失败');
    onlineList.value = [];
    total.value = 0;
  } finally {
    loading.value = false;
  }
};

const handleQuery = () => {
  pageNum.value = 1;
  getList();
};


const resetQuery = () => {
  Object.keys(queryState.value).forEach((key: string) => {
    delete queryState.value[key];
  });
  pagination.current = 1;
  getList();
};

const handleForceLogout = (row: OnlineUser) => {
  if (!row?.user_name) return;
  Modal.confirm({
    title: '确认提示',
    content: `是否确认强退名称为"${row.user_name}"的用户?`,
    async onOk() {
      try {
        await deleteOnline(row.user_name);
        await getList();
        message.success('强退成功');
      } catch (error) {
        message.error('强退失败');
      }
    }
  });
};

const handlePageChange = (page: number, size: number) => {
  pageNum.value = page;
  pageSize.value = size;
};

const handlePageSizeChange = (current: number, size: number) => {
  pageSize.value = size;
  pageNum.value = 1;
};

onMounted(() => {
  getList();
});
</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}
</style>
