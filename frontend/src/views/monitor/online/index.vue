<template>


  <!-- 搜索表单 -->
  <div class="table-search-wrapper">
    <a-card :bordered="false">
      <a-form :model="queryState" @finish="onFinish" >
        <a-flex wrap="wrap" gap="middle">
            <a-form-item name="ipaddr" label="主机" >
              <a-input v-model:value="queryState.ipaddr" placeholder="请输入主机地址" allowClear style="width: 200px;"></a-input>
            </a-form-item>
            <a-form-item name="user_name" label="用户名" >
              <a-input v-model:value="queryState.name" placeholder="请输入登陆用户名称" allowClear style="width: 200px;"></a-input>
            </a-form-item>
            <a-form-item name="login_location" label="登陆地点" >
              <a-input v-model:value="queryState.login_location" placeholder="请输入登陆地点" allowClear style="width: 200px;"></a-input>
            </a-form-item>
            <a-button type="primary" html-type="submit" :loading="loading">查询</a-button>
            <a-button @click="resetQuery">重置</a-button>
        </a-flex>
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
        :data-source="dataSource"
        :loading="loading"
        @change="handlePageChange"
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
import { ref, reactive, onMounted } from 'vue';
import { DeleteOutlined } from '@ant-design/icons-vue';
import { Modal, message } from 'ant-design-vue';
import { getOnlineList, deleteOnline} from "@/api/monitor/online";
import type { searchType, OnlineUser } from './types';

const dataSource = ref<OnlineUser[]>([]);
const loading = ref(false);
const queryState = reactive<searchType>({});

const columns = [
  { title: '会话编号', width: 320, dataIndex: 'session_id', key: 'sessionId', ellipsis: true },
  { title: '登录名称', width: 80, dataIndex: 'name', key: 'name', align: 'center', ellipsis: true },
  { title: '用户账号', width: 80, dataIndex: 'user_name', key: 'userName', align: 'center', ellipsis: true },
  { title: '主机', width: 100, dataIndex: 'ipaddr', key: 'ipaddr', align: 'center', ellipsis: true },
  { title: '登录地点', dataIndex: 'login_location', key: 'loginLocation', align: 'center', ellipsis: true },
  { title: '操作系统', dataIndex: 'os', key: 'os', align: 'center', ellipsis: true },
  { title: '登录时间', dataIndex: 'login_time', key: 'loginTime', align: 'center', ellipsis: true, width: 180 },
  { title: '操作', dataIndex: 'operation', key: 'operation', align: 'center', width: 120 }
];

const pagination = reactive({
  current: 1,
  pageSize: 10,
  defaultPageSize: 10,
  showSizeChanger: true,
  total: dataSource.value.length,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})

const onFinish = () => {
  pagination.current = 1;
  loadingData();
};

const loadingData = async () => {
  loading.value = true;

  let params = {};

  if (queryState.ipaddr) {
    params['ipaddr'] = queryState.ipaddr
  }

  if (queryState.name) {
    params['name'] = queryState.name
  }

  if (queryState.login_location) {
    params['login_location'] = queryState.login_location
  }

  params['page_no'] = pagination.current;
  params['page_size'] = pagination.pageSize;

  getOnlineList(params).then(response => {
    const result = response.data;
    dataSource.value = result.data.items;
    pagination.total = result.data.total;
    pagination.current = result.data.page_no;
    pagination.pageSize = result.data.page_size;
  }).catch(error => {
    console.log(error);
  }).finally(() => {
    loading.value = false;
  });
};

const resetQuery = () => {
  Object.keys(queryState).forEach((key: string) => {
    delete queryState[key];
  });
  pagination.current = 1;
  loadingData();
};

const handleForceLogout = (row: OnlineUser) => {
  if (!row?.session_id) return;
  Modal.confirm({
    title: '确认提示',
    content: `是否确认强退名称为"${row.user_name}"的用户?`,
    async onOk() {
      try {
        await deleteOnline(row.session_id);
        await loadingData();
      } catch (error) {
        console.error('强退失败:', error);
      }
    }
  });
};

const handlePageChange = (values: any) => {
  pagination.current = values.current;
  pagination.pageSize = values.pageSize;
  loadingData();
};


onMounted(() => loadingData());

</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}
</style>
