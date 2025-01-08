<template>
  <div class="app-container">
    <a-row :gutter="16">
      <a-col :span="12" class="mb-4">
        <a-card :loading="loading" :bordered="false" class="shadow-sm" :bodyStyle="{ padding: '24px', height: '360px' }">
          <template #title>
            <div class="flex items-center">
              <DesktopOutlined class="text-primary text-lg mr-2" />
              <span class="font-medium">CPU使用情况</span>
              <a-tooltip title="展示CPU核心数及使用率">
                <QuestionCircleOutlined class="ml-2 text-gray-400" />
              </a-tooltip>
            </div>
          </template>
          <div class="grid grid-cols-2 gap-4">
            <div class="border rounded-lg p-4">
              <div class="text-center mb-4">
                <div class="text-lg font-bold">CPU核心数</div>
                <a-tooltip title="CPU核心数">
                  <a-progress type="circle" :percent="100" :format="() => server.cpu?.cpu_num || 0" status="normal"/>
                </a-tooltip>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span>用户使用率:</span>
                  <span class="font-medium">{{ (server.cpu?.used || 0).toFixed(1) }}%</span>
                </div>
                <div class="flex justify-between">
                  <span>系统使用率:</span>
                  <span class="font-medium">{{ (server.cpu?.sys || 0).toFixed(1) }}%</span>
                </div>
                <div class="flex justify-between">
                  <span>当前空闲率:</span>
                  <span class="font-medium">{{ (server.cpu?.free || 0).toFixed(1) }}%</span>
                </div>
              </div>
            </div>
            <div class="border rounded-lg p-4">
              <div class="text-center mb-4">
                <div class="text-lg font-bold">CPU使用率</div>
                <a-tooltip title="CPU使用率">
                  <a-progress type="circle" :percent="server.cpu?.used || 0" :status="server.cpu?.used > 80 ? 'exception' : 'normal'"/>
                </a-tooltip>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span>总核心数:</span>
                  <span class="font-medium">{{ server.cpu?.cpu_num || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span>已用核心:</span>
                  <span class="font-medium">{{ Math.floor((server.cpu?.used || 0) * server.cpu?.cpu_num / 100) }}</span>
                </div>
                <div class="flex justify-between">
                  <span>空闲核心:</span>
                  <span class="font-medium">{{ Math.floor((server.cpu?.free || 0) * server.cpu?.cpu_num / 100) }}</span>
                </div>
              </div>
            </div>
          </div>
        </a-card>
      </a-col>

      <a-col :span="12" class="mb-4">
        <a-card :loading="loading" :bordered="false" class="shadow-sm" :bodyStyle="{ padding: '24px', height: '360px' }">
          <template #title>
            <div class="flex items-center">
              <FileTextOutlined class="text-primary text-lg mr-2" />
              <span class="font-medium">内存使用情况</span>
              <a-tooltip title="展示系统内存和Python程序内存使用情况">
                <QuestionCircleOutlined class="ml-2 text-gray-400" />
              </a-tooltip>
            </div>
          </template>
          <div class="grid grid-cols-2 gap-4">
            <div class="border rounded-lg p-4">
              <div class="text-center mb-4">
                <div class="text-lg font-bold">系统内存</div>
                <a-tooltip title="系统内存">
                  <a-progress type="circle" :percent="server.mem?.usage || 0" :status="server.mem?.usage > 80 ? 'exception' : 'normal'"/>
                </a-tooltip>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span>总内存:</span>
                  <span class="font-medium">{{ server.mem?.total }}</span>
                </div>
                <div class="flex justify-between">
                  <span>已用内存:</span>
                  <span class="font-medium">{{ server.mem?.used }}</span>
                </div>
                <div class="flex justify-between">
                  <span>空闲内存:</span>
                  <span class="font-medium">{{ server.mem?.free }}</span>
                </div>
              </div>

            </div>
            <div class="border rounded-lg p-4">
              <div class="text-center mb-4">
                <div class="text-lg font-bold">Python内存</div>
                <a-tooltip title="Python内存">
                  <a-progress type="circle" :percent="server.py?.memory_usage || 0" :status="server.py?.memory_usage > 80 ? 'exception' : 'normal'" />
                </a-tooltip>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span>总内存:</span>
                  <span class="font-medium">{{ server.py?.memory_total }}</span>
                </div>
                <div class="flex justify-between">
                  <span>已用内存:</span>
                  <span class="font-medium">{{ server.py?.memory_used }}</span>
                </div>
                <div class="flex justify-between">
                  <span>空闲内存:</span>
                  <span class="font-medium">{{ server.py?.memory_free }}</span>
                </div>
              </div>
            </div>
          </div>
        </a-card>
      </a-col>

      <a-col :span="24" class="mb-4">
        <a-card :loading="loading" :bordered="false" class="shadow-sm" :bodyStyle="{ padding: '24px' }">
          <template #title>
            <div class="flex items-center">
              <MonitorOutlined class="text-primary text-lg mr-2" />
              <span class="font-medium">服务器基本信息</span>
              <a-tooltip title="展示服务器基本配置信息">
                <QuestionCircleOutlined class="ml-2 text-gray-400" />
              </a-tooltip>
            </div>
          </template>
          <a-descriptions :column="2" bordered>
            <a-descriptions-item label="服务器名称">{{ server.sys?.computer_name || '-' }}</a-descriptions-item>
            <a-descriptions-item label="操作系统">{{ server.sys?.os_name || '-' }}</a-descriptions-item>
            <a-descriptions-item label="服务器IP">{{ server.sys?.computer_ip || '-' }}</a-descriptions-item>
            <a-descriptions-item label="系统架构">{{ server.sys?.os_arch || '-' }}</a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>

      <a-col :span="24" class="mb-4">
        <a-card :loading="loading" :bordered="false" class="shadow-sm" :bodyStyle="{ padding: '24px' }">
          <template #title>
            <div class="flex items-center">
              <CodeOutlined class="text-primary text-lg mr-2" />
              <span class="font-medium">Python运行环境</span>
              <a-tooltip title="展示Python环境配置及运行状态">
                <QuestionCircleOutlined class="ml-2 text-gray-400" />
              </a-tooltip>
            </div>
          </template>
          <a-descriptions :column="3" bordered>
            <a-descriptions-item label="Python名称">{{ server.py?.name || '-' }}</a-descriptions-item>
            <a-descriptions-item label="Python版本">{{ server.py?.version || '-' }}</a-descriptions-item>
            <a-descriptions-item label="启动时间">{{ server.py?.start_time || '-' }}</a-descriptions-item>
            <a-descriptions-item label="运行时长">{{ server.py?.run_time || '-' }}</a-descriptions-item>
            <a-descriptions-item label="安装路径">{{ server.py?.home || '-' }}</a-descriptions-item>
            <a-descriptions-item label="项目路径">{{ server.sys?.user_dir || '-' }}</a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>

      <a-col :span="24">
        <a-card :loading="loading" :bordered="false" class="shadow-sm" :bodyStyle="{ padding: '24px' }">
          <template #title>
            <div class="flex items-center">
              <HddOutlined class="text-primary text-lg mr-2" />
              <span class="font-medium">磁盘使用情况</span>
              <a-tooltip title="展示磁盘空间使用详情">
                <QuestionCircleOutlined class="ml-2 text-gray-400" />
              </a-tooltip>
            </div>
          </template>
          <a-table 
            :dataSource="server.disks" 
            :pagination="false" 
            :bordered="true" 
            :scroll="{ x: 500 }"
            :rowKey="(record) => record.dir_name"
          >
            <a-table-column 
              key="dir_name" 
              title="盘符路径" 
              dataIndex="dir_name" 
              :ellipsis="true"
              :width="100"
            />
            <a-table-column 
              key="sys_type_name" 
              title="文件系统" 
              dataIndex="sys_type_name" 
              align="center"
              :width="100"
            />
            <a-table-column 
              key="type_name" 
              title="盘符名称" 
              dataIndex="type_name" 
              :width="300"
            />
            <a-table-column 
              key="usage" 
              title="使用率" 
              align="center" 
              :width="120"
              :customRender="({record}) => {
                // 从record中获取usage值,确保是数字类型
                const usageValue = Number(record.usage);
                // 修改status的类型以匹配Progress组件的要求
                const status = usageValue > 80 ? 'exception' : usageValue > 60 ? 'normal' : 'normal';
                const strokeColor = usageValue > 80 ? '#ff4d4f' : usageValue > 60 ? '#faad14' : '#1677ff';
                return h('div', { style: { padding: '0 10px' }}, [
                  h(AProgress, {
                    percent: usageValue,
                    size: 'small',
                    status,
                    strokeColor,
                    style: { marginBottom: '4px' }
                  }),
                ]);
              }" 
            />
            <a-table-column 
              key="total" 
              title="总大小" 
              dataIndex="total" 
              align="center"
              :width="100"
            />
            <a-table-column 
              key="free" 
              title="可用大小" 
              dataIndex="free" 
              align="center"
              :width="100"
            />
            <a-table-column 
              key="used" 
              title="已用大小" 
              dataIndex="used" 
              align="center"
              :width="100"
            />
          </a-table>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, h } from 'vue';
import { getServer } from '@/api/monitor/server'
import { message } from 'ant-design-vue';
import { QuestionCircleOutlined, DesktopOutlined, FileTextOutlined, MonitorOutlined, CodeOutlined, HddOutlined } from '@ant-design/icons-vue';
import { Progress as AProgress } from 'ant-design-vue';
import type { ServerInfo } from './types';

const loading = ref(false);
const server = ref<ServerInfo>({
  cpu: {
    cpu_num: 0,
    used: 0,
    sys: 0,
    free: 0
  },
  mem: {
    total: '',
    used: '',
    free: '',
    usage: 0
  },
  sys: {
    computer_name: '',
    os_name: '',
    computer_ip: '',
    os_arch: '',
    user_dir: ''
  },
  py: {
    name: '',
    version: '',
    start_time: '',
    run_time: '',
    home: '',
    memory_total: '',
    memory_used: '',
    memory_free: '',
    memory_usage: 0
  },
  disks: []
});

async function getList() {
  loading.value = true;
  try {
    const response = await getServer();
    server.value = response.data.data;
  } catch (error) {
    message.error('获取服务器信息失败');
    console.error(error);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  getList();
});
</script>

<style scoped>
.app-container {
  padding: 20px;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.text-primary {
  color: #1677ff;
}

.text-warning {
  color: #faad14;
}

.text-gray-400 {
  color: #9ca3af;
}

.text-gray-500 {
  color: #6b7280;
}

.mb-4 {
  margin-bottom: 1rem;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.ml-2 {
  margin-left: 0.5rem;
}

.mr-2 {
  margin-right: 0.5rem;
}

.p-4 {
  padding: 1rem;
}

.flex {
  display: flex;
}

.grid {
  display: grid;
}

.grid-cols-2 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.gap-4 {
  gap: 1rem;
}

.space-y-2 > * + * {
  margin-top: 0.5rem;
}

.items-center {
  align-items: center;
}

.justify-between {
  justify-content: space-between;
}

.justify-around {
  justify-content: space-around;
}

.text-center {
  text-align: center;
}

.font-medium {
  font-weight: 500;
}

.font-bold {
  font-weight: 600;
}

.text-lg {
  font-size: 1.125rem;
}

.rounded-lg {
  border-radius: 0.5rem;
}

.border {
  border: 1px solid #e5e7eb;
}
</style>
