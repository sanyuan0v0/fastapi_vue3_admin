<template>


  <div class="app-container">
    <a-tabs>
      <!-- 监控信息 Tab -->
      <a-tab-pane key="monitor" tab="监控信息">
        <a-row :gutter="16">
          <!-- 基本信息 -->
          <a-col :span="24">
            <a-card>
              <template #title>
                <MonitorOutlined class="icon" /> 
                <span class="title">Redis监控信息</span>
              </template>
              <a-table :dataSource="[cache.info || {}]" :pagination="false" :bordered="true">
                <a-table-column key="redis_version" title="Redis版本" :customRender="({record}) => record?.redis_version || '-'" />
                <a-table-column key="redis_mode" title="运行模式" :customRender="({record}) => record?.redis_mode === 'standalone' ? '单机' : '集群'" />
                <a-table-column key="tcp_port" title="端口" :customRender="({record}) => record?.tcp_port || '-'" />
                <a-table-column key="connected_clients" title="客户端数" :customRender="({record}) => record?.connected_clients || 0" />
                <a-table-column key="uptime_in_days" title="运行时间(天)" :customRender="({record}) => record?.uptime_in_days || 0" />
                <a-table-column key="used_memory_human" title="使用内存" :customRender="({record}) => record?.used_memory_human || '-'" />
                <a-table-column key="used_cpu" title="使用CPU" :customRender="({record}) => record?.used_cpu_user_children ? parseFloat(record.used_cpu_user_children).toFixed(2) : '-'" />
                <a-table-column key="maxmemory_human" title="内存配置" :customRender="({record}) => record?.maxmemory_human || '-'" />
                <a-table-column key="aof_enabled" title="AOF是否开启" :customRender="({record}) => record?.aof_enabled === '0' ? '否' : '是'" />
                <a-table-column key="rdb_status" title="RDB是否成功" :customRender="({record}) => record?.rdb_last_bgsave_status || '-'" />
                <a-table-column key="dbSize" title="Key数量" :customRender="() => cache.db_size || 0" />
                <a-table-column key="network" title="网络入口/出口" :customRender="({record}) => `${record?.instantaneous_input_kbps || 0}kps/${record?.instantaneous_output_kbps || 0}kps`" />
              </a-table>
            </a-card>
          </a-col>

          <!-- 监控图表 -->
          <a-col :span="12" class="mt-4">
            <a-card>
              <template #title>
                <PieChartOutlined class="icon" />
                <span class="title">命令统计</span>
              </template>
              <div ref="commandstats" class="chart-container" />
            </a-card>
          </a-col>

          <a-col :span="12" class="mt-4">
            <a-card>
              <template #title>
                <DashboardOutlined class="icon" />
                <span class="title">内存信息</span>
              </template>
              <div ref="usedmemory" class="chart-container" />
            </a-card>
          </a-col>
        </a-row>
      </a-tab-pane>

      <!-- 缓存管理 Tab -->
      <a-tab-pane key="cache" tab="缓存管理">
        <a-row :gutter="16">
          <!-- 缓存列表 -->
          <a-col :span="8">
            <a-card :bodyStyle="{ height: tableContainerHeight, minHeight: '600px' }">
              <template #title>
                <SolutionOutlined class="icon" /> 
                <span class="title">缓存列表</span>
              </template>
              <template #extra>
                <a-button type="link" @click="refreshCacheNames">
                  <template #icon><RedoOutlined /></template>
                </a-button>
              </template>
              <a-table
                :loading="loading"
                :dataSource="cacheNames"
                :pagination="false"
                :scroll="{ y: 500 }"
                rowKey="cache_name"
              >
                <a-table-column key="cache_name" title="缓存名称" align="center" :ellipsis="true">
                  <template #default="{ record }">
                    <a @click="getCacheKeyList(record)">{{ record.cache_name }}</a>
                  </template>
                </a-table-column>
                <a-table-column key="remark" title="备注" align="center" :ellipsis="true" dataIndex="remark" />
                <a-table-column key="action" title="操作" width="60" align="center">
                  <template #customRender="{ record }">
                    <a-button type="link" danger @click.stop="handleClearCacheName(record)">
                      <template #icon><DeleteOutlined /></template>
                    </a-button>
                  </template>
                </a-table-column>
              </a-table>
            </a-card>
          </a-col>

          <!-- 键名列表 -->
          <a-col :span="8">
            <a-card :bodyStyle="{ height: tableContainerHeight, minHeight: '600px' }">
              <template #title>
                <KeyOutlined class="icon" />
                <span class="title">键名列表</span>
              </template>
              <template #extra>
                <a-button type="link" @click="refreshCacheKeys">
                  <template #icon><RedoOutlined /></template>
                </a-button>
              </template>
              <a-table
                :loading="subLoading"
                :dataSource="cacheKeys.map(key => ({ cacheKey: key }))"
                :pagination="false"
                :scroll="{ y: 500 }"
                rowKey="cacheKey"
              >
                <a-table-column key="cacheKey" title="缓存键名" align="center" :ellipsis="true">
                  <template #default="{ record }">
                    <a @click="handleCacheValue(record.cacheKey)">{{ record.cacheKey }}</a>
                  </template>
                </a-table-column>
                <a-table-column key="action" title="操作" width="60" align="center">
                  <template #customRender="{ record }">
                    <a-button type="link" danger @click.stop="handleClearCacheKey(record.cacheKey)">
                      <template #icon><DeleteOutlined /></template>
                    </a-button>
                  </template>
                </a-table-column>
              </a-table>
            </a-card>
          </a-col>

          <!-- 缓存内容 -->
          <a-col :span="8">
            <a-card :bodyStyle="{ height: tableContainerHeight, minHeight: '600px' }">
              <template #title>
                <FileOutlined class="icon" />
                <span class="title">缓存内容</span>
              </template>
              <template #extra>
                <a-button type="link" danger @click="handleClearCacheAll">清理全部</a-button>
              </template>
              <a-form :model="cacheForm" layout="vertical">
                <a-form-item label="缓存名称:" name="cache_name">
                  <a-input v-model:value="cacheForm.cache_name" readonly />
                </a-form-item>
                <a-form-item label="缓存键名:" name="cache_key">
                  <a-input v-model:value="cacheForm.cache_key" readonly />
                </a-form-item>
                <a-form-item label="缓存内容:" name="cache_value">
                  <a-textarea
                    v-model:value="cacheForm.cache_value"
                    :rows="15"
                    readonly
                  />
                </a-form-item>
              </a-form>
            </a-card>
          </a-col>
        </a-row>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { DeleteOutlined, RedoOutlined, LineChartOutlined, SolutionOutlined, KeyOutlined, FileOutlined, MonitorOutlined, PieChartOutlined, DashboardOutlined } from '@ant-design/icons-vue';
import { message, Modal } from 'ant-design-vue';
import { getCacheInfo, getCacheNames, getCacheKeys, getCacheValue, deleteCacheName, deleteCacheKey, deleteCacheAll } from "@/api/monitor/cache";
import * as echarts from 'echarts';
import type { CacheInfo, CacheForm, CacheMonitor, RedisInfo } from './types';

// 响应式状态定义
const cacheNames = ref<CacheInfo[]>([]);
const cacheKeys = ref<string[]>([]);
const cacheForm = ref<CacheForm>({
  cache_name: '',
  cache_key: '', 
  cache_value: ''
});
const loading = ref(true);
const subLoading = ref(false);
const nowCacheName = ref('');
const cache = ref<CacheMonitor>({
  info: {} as RedisInfo,
  command_stats: [],
  db_size: 0
});
const commandstats = ref<HTMLElement | null>(null);
const usedmemory = ref<HTMLElement | null>(null);

let commandstatsInstance: echarts.ECharts | null = null;
let usedmemoryInstance: echarts.ECharts | null = null;

// 计算属性
const tableContainerHeight = computed(() => `calc(100vh - 300px)`);

const resetCacheForm = () => {
  cacheKeys.value = [];
  cacheForm.value = {
    cache_name: '',
    cache_key: '',
    cache_value: ''
  };
};

// 缓存名称相关方法
const getCacheNameList = () => {
  loading.value = true;
  getCacheNames()
    .then(({ data: result }) => {
      if (result.status_code === 200) {
        cacheNames.value = result.data || [];
        resetCacheForm();
      } else {
        message.error(result.msg)
      }
    })
    .catch(error => {
      console.error('获取缓存列表出错:', error);
      message.error('获取缓存列表失败');
    })
    .finally(() => {
      loading.value = false;
    });
};

// 刷新缓存列表
const refreshCacheNames = () => {
  getCacheNameList();
  message.success('刷新缓存列表成功');
};

// 清理缓存名称
const handleClearCacheName = (row: CacheInfo) => {
  Modal.confirm({
    title: '确认清理',
    content: `确定要清理缓存名称[${row.cache_name}]吗？`,
    onOk() {
      deleteCacheName(row.cache_name)
        .then(({ data: result }) => {
          if (result.status_code === 200) {
            message.success(result.msg);
            getCacheNameList();
          } else {
            message.error(result.msg)
          }
        })
        .catch(error => {
          console.error('清理缓存失败:', error);
          message.error('清理缓存失败');
        });
    }
  });
};

// 缓存键名相关方法
const getCacheKeyList = (row?: CacheInfo) => {
  const cacheName = row?.cache_name || nowCacheName.value;
  if (!cacheName) return;
  
  subLoading.value = true;
  getCacheKeys(cacheName)
    .then(({ data: result }) => {
      if (result.status_code === 200) {
        cacheKeys.value = result.data || [];
        nowCacheName.value = cacheName;
        cacheForm.value = {
          cache_name: cacheName,
          cache_key: '',
          cache_value: ''
        };
        message.success(result.msg);
      } else {
        message.error(result.msg)
      }
    })
    .catch(error => {
      console.error('获取缓存键名列表失败:', error);
      message.error('获取缓存键名列表失败');
    })
    .finally(() => {
      subLoading.value = false;
    });
};

// 刷新键名列表
const refreshCacheKeys = () => {
  getCacheKeyList();
  message.success('刷新键名列表成功');
};

// 清理缓存键名
const handleClearCacheKey = (cacheKey: string) => {
  Modal.confirm({
    title: '确认清理',
    content: `确定要清理缓存键名[${cacheKey}]吗？`,
    onOk() {
      deleteCacheKey(cacheKey)
        .then(({ data: result }) => {
          if (result.status_code === 200) {
            message.success(result.msg);
            getCacheKeyList();
          } else {
            message.error(result.msg)
          }
        })
        .catch(error => {
          console.error('清理缓存键名失败:', error);
          message.error('清理缓存键名失败');
        });
    }
  });
};

// 缓存内容相关方法
const handleCacheValue = (cacheKey: string) => {
  getCacheValue(nowCacheName.value, cacheKey)
    .then(({ data: result }) => {
      if (result.status_code === 200) {
        cacheForm.value = result.data;
        message.success(result.msg);
      } else {
        message.error(result.msg)
      }
    })
    .catch(error => {
      console.error('获取缓存内容失败:', error);
      message.error('获取缓存内容失败');
    });
};

// 清理全部缓存
const handleClearCacheAll = () => {
  Modal.confirm({
    title: '确认清理',
    content: '确定要清理全部缓存吗？',
    onOk() {
      deleteCacheAll()
        .then(({ data: result }) => {
          if (result.status_code === 200) {
            message.success(result.msg);
            getCacheNameList();
          } else {
            message.error(result.msg)
          }
        })
        .catch(error => {
          console.error('清理全部缓存失败:', error);
          message.error('清理全部缓存失败');
        });
    }
  });
};

// 监控数据获取
const getInfo = () => {
  getCacheInfo()
    .then(({ data: result }) => {
      if (result.status_code === 200) {
        cache.value = result.data || {
          info: {},
          command_stats: [],
          dbSize: 0
        };
        initCharts();
        message.success(result.msg || '获取缓存监控数据成功');
      } else {
        message.error(result.msg || '获取缓存监控数据失败');
      }
    })
    .catch(error => {
      message.error('获取缓存监控数据失败:', error);
    });
};

// 图表初始化
const initCharts = () => {
  if (!commandstats.value || !usedmemory.value) return;

  commandstatsInstance = echarts.init(commandstats.value, 'macarons');
  usedmemoryInstance = echarts.init(usedmemory.value, 'macarons');

  const commandStatsOption = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    series: [{
      name: '命令',
      type: 'pie',
      roseType: 'radius',
      radius: [15, 95],
      center: ['50%', '38%'],
      data: cache.value.command_stats || [],
      animationEasing: 'cubicInOut',
      animationDuration: 1000
    }]
  };

  const usedMemory = cache.value.info?.used_memory_human || '0';
  const usedMemoryOption = {
    tooltip: {
      formatter: `{b} <br/>{a} : ${usedMemory}`
    },
    series: [{
      name: '峰值',
      type: 'gauge',
      min: 0,
      max: 1000,
      detail: {
        formatter: usedMemory
      },
      data: [{
        value: parseFloat(usedMemory) || 0,
        name: '内存消耗'
      }]
    }]
  };

  commandstatsInstance.setOption(commandStatsOption);
  usedmemoryInstance.setOption(usedMemoryOption);
};

// 生命周期钩子
onMounted(() => {
  getCacheNameList();
  getInfo();
});

onUnmounted(() => {
  commandstatsInstance?.dispose();
  usedmemoryInstance?.dispose();
});
</script>

<style scoped>
.icon {
  width: 1em;
  height: 1em;
  vertical-align: middle;
}

.title {
  vertical-align: middle;
  margin-left: 8px;
}

.mt-4 {
  margin-top: 16px;
}

.chart-container {
  height: 420px;
}
</style>
