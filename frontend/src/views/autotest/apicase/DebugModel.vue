<template>
  <a-modal v-model:open="debugModalState.open" 
    title="接口调试" 
    :width="1200" 
    :footer="null"
    :bodyStyle="{ padding: '16px', height: 'calc(100vh - 200px)', overflow: 'auto' }"
    :maskClosable="false"
    :keyboard="false"
    @cancel="handleCancel"
  >
    <!-- 原有的主体布局代码保持不变 -->
    <div class="debug-container">
      <!-- 1. 优化请求配置区域 -->
      <div class="request-section">
        <a-form layout="vertical">
          <!-- 优化URL输入区 -->
          <a-row :gutter="16">
            <a-col :span="3">
              <a-form-item label="请求方法">
                <a-select v-model:value="debugRequest.method" 
                  :dropdownMatchSelectWidth="false"
                  @change="handleMethodChange">
                  <a-select-option v-for="method in HTTP_METHODS" :key="method">
                    <span :class="getMethodClass(method)">{{ method }}</span>
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="17">
              <a-form-item label="请求地址">
                <a-input-group compact>
                  <a-select v-model:value="protocol" style="width: 100px">
                    <a-select-option value="http">http://</a-select-option>
                    <a-select-option value="https">https://</a-select-option>
                  </a-select>
                  <a-auto-complete
                    v-model:value="debugRequest.url"
                    :options="urlHistory"
                    style="width: calc(100% - 100px)"
                    placeholder="请输入完整的URL地址"
                    @select="handleUrlSelect"
                  />
                </a-input-group>
              </a-form-item>
            </a-col>
            <a-col :span="4">
              <a-form-item label=" ">
                <a-space>
                  <a-tooltip title="Ctrl + Enter">
                    <a-button type="primary" @click="sendRequest" :loading="loading">
                      发送请求
                      <template #icon><SendOutlined /></template>
                    </a-button>
                  </a-tooltip>
                  <a-dropdown>
                    <a-button>
                      更多 <DownOutlined />
                    </a-button>
                    <template #overlay>
                      <a-menu>
                        <a-menu-item key="save" @click="saveAsFavorite">
                          <StarOutlined /> 保存到收藏
                        </a-menu-item>
                        <a-menu-item key="copy" @click="copyRequest">
                          <CopyOutlined /> 复制请求
                        </a-menu-item>
                        <a-menu-item key="reset" @click="confirmReset">
                          <ReloadOutlined /> 重置
                        </a-menu-item>
                      </a-menu>
                    </template>
                  </a-dropdown>
                </a-space>
              </a-form-item>
            </a-col>
          </a-row>

          <!-- 2. 优化请求参数配置区 -->
          <a-tabs v-model:activeKey="activeTab" class="debug-tabs">
            <!-- Headers面板增加智能提示 -->
            <a-tab-pane key="headers" tab="Headers">
              <div class="tab-toolbar">
                <a-space>
                  <a-dropdown :trigger="['click']">
                    <a-button type="link">
                      常用Headers <DownOutlined />
                    </a-button>
                    <template #overlay>
                      <a-menu @click="addCommonHeader">
                        <a-menu-item v-for="header in commonHeaders" :key="header.key">
                          {{ header.key }}: {{ header.value }}
                        </a-menu-item>
                      </a-menu>
                    </template>
                  </a-dropdown>
                  <a-button type="link" @click="clearHeaders">清空</a-button>
                </a-space>
              </div>
              <div class="param-table">
                <div v-for="(item, index) in headersList" :key="index" class="param-row">
                  <a-input v-model:value="item.key" placeholder="Key" class="param-key" />
                  <a-input v-model:value="item.value" placeholder="Value" class="param-value" />
                  <a-button type="text" @click="removeHeader(index)" danger>
                    <DeleteOutlined />
                  </a-button>
                </div>
                <a-button type="link" @click="addHeader" class="add-btn">
                  <PlusOutlined /> 添加 Header
                </a-button>
              </div>
            </a-tab-pane>

            <!-- Query Params -->
            <a-tab-pane key="params" tab="Params">
              <div class="tab-toolbar">
                <a-button type="link" @click="validateParams">验证参数</a-button>
              </div>
              <div class="param-table">
                <div v-for="(item, index) in paramsList" :key="index" class="param-row">
                  <a-input v-model:value="item.key" placeholder="Key" class="param-key" />
                  <a-input v-model:value="item.value" placeholder="Value" class="param-value" />
                  <a-button type="text" @click="removeParam(index)" danger>
                    <DeleteOutlined />
                  </a-button>
                </div>
                <a-button type="link" @click="addParam" class="add-btn">
                  <PlusOutlined /> 添加参数
                </a-button>
              </div>
            </a-tab-pane>

            <!-- 3. 优化Body展示 -->
            <a-tab-pane key="body" tab="Body">
              <div class="body-section">
                <a-radio-group v-model:value="bodyType" class="body-type" button-style="solid">
                  <a-radio-button value="none">none</a-radio-button>
                  <a-radio-button value="form-data">form-data</a-radio-button>
                  <a-radio-button value="json">JSON</a-radio-button>
                  <a-radio-button value="raw">Raw</a-radio-button>
                </a-radio-group>

                <div v-if="bodyType === 'form-data'" class="param-table">
                  <div v-for="(item, index) in formDataList" :key="index" class="param-row">
                    <a-input v-model:value="item.key" placeholder="Key" class="param-key" />
                    <a-input v-model:value="item.value" placeholder="Value" class="param-value" />
                    <a-button type="text" @click="removeFormData(index)" danger>
                      <DeleteOutlined />
                    </a-button>
                  </div>
                  <a-button type="link" @click="addFormData" class="add-btn">
                    <PlusOutlined /> 添加字段
                  </a-button>
                </div>

                <div v-else-if="bodyType === 'json'" class="json-editor">
                  <MonacoEditor v-model:value="jsonBody" :options="editorOptions" language="json"
                    @change="formatJSON" />
                </div>

                <!-- 增加快捷操作栏 -->
                <div v-if="bodyType === 'json'" class="json-toolbar">
                  <a-space>
                    <a-button type="link" size="small" @click="formatJSON">
                      <FormatPainterOutlined /> 格式化
                    </a-button>
                    <a-button type="link" size="small" @click="compressJSON">
                      <CompressOutlined /> 压缩
                    </a-button>
                    <a-button type="link" size="small" @click="validateJSON">
                      <CheckOutlined /> 验证
                    </a-button>
                  </a-space>
                </div>
              </div>
            </a-tab-pane>

            <!-- Cookies -->
            <a-tab-pane key="cookies" tab="Cookies">
              <div class="param-table">
                <!-- ...类似headers的配置代码... -->
              </div>
            </a-tab-pane>
          </a-tabs>
        </a-form>

        <!-- 发送按钮区增加快捷键提示 -->
        <div class="action-bar">
          <a-space>
            <a-button type="primary" @click="sendRequest" :loading="loading">
              发送请求
              <template #icon>
                <SendOutlined />
              </template>
            </a-button>
            <a-button @click="resetForm">
              重置
              <template #icon>
                <ReloadOutlined />
              </template>
            </a-button>
            <span class="shortcut-tip">快捷键: Ctrl + Enter</span>
          </a-space>
        </div>
      </div>

      <!-- 4. 优化响应结果区域 -->
      <a-divider />
      <div v-if="response" class="response-section">
        <!-- 优化响应状态展示 -->
        <div class="response-header">
          <div :class="['status', getStatusClass(response.status)]">
            <a-badge :status="getStatusBadge(response.status)" />
            Status: {{ response.status }} {{ response.statusText }}
          </div>
          <div class="info">
            <a-space>
              <span>Time: {{ response.time }}ms</span>
              <a-divider type="vertical" />
              <span>Size: {{ response.size }}</span>
            </a-space>
          </div>
        </div>

        <!-- 优化响应内容展示 -->
        <a-tabs :animated="false">
          <a-tab-pane key="response" tab="Response">
            <div class="response-toolbar">
              <a-space>
                <a-tooltip title="复制到剪贴板">
                  <a-button type="link" @click="copyResponse">
                    <CopyOutlined /> 复制
                  </a-button>
                </a-tooltip>
                <a-button type="link" @click="downloadResponse">
                  <DownloadOutlined /> 下载
                </a-button>
                <a-button type="link" @click="searchResponse">
                  <SearchOutlined /> 搜索
                </a-button>
                <a-select v-model:value="responseView" style="width: 100px">
                  <a-select-option value="pretty">Pretty</a-select-option>
                  <a-select-option value="raw">Raw</a-select-option>
                  <a-select-option value="preview">Preview</a-select-option>
                </a-select>
              </a-space>
            </div>
            <MonacoEditor :value="formatResponse(response.data)" :options="viewerOptions" language="json"
              class="response-viewer" />
          </a-tab-pane>

          <a-tab-pane key="headers" tab="Headers">
            <a-descriptions bordered :column="1">
              <a-descriptions-item v-for="(value, key) in response.headers" :key="key" :label="key">
                {{ value }}
              </a-descriptions-item>
            </a-descriptions>
          </a-tab-pane>

          <a-tab-pane key="cookies" tab="Cookies">
            <!-- ...Cookie展示代码... -->
          </a-tab-pane>
        </a-tabs>
      </div>
      <a-empty v-else description="等待发送请求..." />
    </div>

    <!-- 5. 添加辅助功能弹窗 -->
    <a-drawer
      v-model:visible="searchDrawer.visible"
      title="搜索响应内容"
      placement="right"
      :width="300"
    >
      <a-form layout="vertical">
        <a-form-item label="搜索内容">
          <a-input v-model:value="searchDrawer.keyword" allow-clear @pressEnter="handleSearch" />
        </a-form-item>
        <a-form-item label="搜索选项">
          <a-checkbox v-model:checked="searchDrawer.caseSensitive">区分大小写</a-checkbox>
          <a-checkbox v-model:checked="searchDrawer.useRegex">使用正则</a-checkbox>
        </a-form-item>
      </a-form>
      <template #footer>
        <a-button type="primary" @click="handleSearch">搜索</a-button>
      </template>
    </a-drawer>
  </a-modal>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import { message, Modal } from 'ant-design-vue';
import { PlusOutlined, DeleteOutlined, SendOutlined, ReloadOutlined, DownOutlined, StarOutlined, CopyOutlined, FormatPainterOutlined, CompressOutlined, CheckOutlined, DownloadOutlined, SearchOutlined } from '@ant-design/icons-vue';
import type { DebugModalState } from './types';
import axios from 'axios';

// 常量定义
const HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'];

// 状态定义
const debugModalState = reactive<DebugModalState>({
    open: false,
    loading: false
});

const loading = ref(false);
const activeTab = ref('headers');
const bodyType = ref('none');
const jsonBody = ref('');
const response = ref(null);

// Monaco编辑器配置
const editorOptions = {
    minimap: { enabled: false },
    lineNumbers: 'on',
    scrollBeyondLastLine: false,
    automaticLayout: true,
    tabSize: 2,
    fontSize: 14,
    theme: 'vs-dark'
};

const viewerOptions = {
    ...editorOptions,
    readOnly: true
};

// Headers管理
const headersList = ref([]);
const addHeader = () => headersList.value.push({ key: '', value: '' });
const removeHeader = (index) => headersList.value.splice(index, 1);

// Params管理  
const paramsList = ref([]);
const addParam = () => paramsList.value.push({ key: '', value: '' });
const removeParam = (index) => paramsList.value.splice(index, 1);

// FormData管理
const formDataList = ref([]);
const addFormData = () => formDataList.value.push({ key: '', value: '' });
const removeFormData = (index) => formDataList.value.splice(index, 1);

// 请求数据管理
const debugRequest = reactive({
    method: 'GET',
    url: '',
    headers: {},
    params: {},
    data: null
});

// JSON格式化
const formatJSON = (value) => {
    try {
        const formatted = JSON.stringify(JSON.parse(value), null, 2);
        jsonBody.value = formatted;
    } catch (e) {
        // 保持原值
    }
};

// 发送请求
const sendRequest = async () => {
    if (!debugRequest.url) {
        message.error('请输入请求地址');
        return;
    }

    loading.value = true;
    try {
        // 构建请求配置
        const config = {
            url: debugRequest.url,
            method: debugRequest.method,
            headers: {},
            params: {},
            data: null
        };

        // 处理Headers
        headersList.value.forEach(item => {
            if (item.key && item.value) {
                config.headers[item.key] = item.value;
            }
        });

        // 处理Params  
        paramsList.value.forEach(item => {
            if (item.key && item.value) {
                config.params[item.key] = item.value;
            }
        });

        // 处理Body
        if (bodyType.value === 'json') {
            try {
                config.data = JSON.parse(jsonBody.value);
            } catch (e) {
                throw new Error('JSON格式错误');
            }
        } else if (bodyType.value === 'form-data') {
            const formData = new FormData();
            formDataList.value.forEach(item => {
                if (item.key && item.value) {
                    formData.append(item.key, item.value);
                }
            });
            config.data = formData;
        }

        // 发送请求并记录时间
        const startTime = Date.now();
        const res = await axios(config);
        const endTime = Date.now();

        // 计算响应大小
        const size = JSON.stringify(res.data).length;
        const sizeStr = size > 1024 ? `${(size / 1024).toFixed(2)} KB` : `${size} B`;

        // 设置响应数据
        response.value = {
            status: res.status,
            statusText: res.statusText,
            headers: res.headers,
            data: res.data,
            time: endTime - startTime,
            size: sizeStr
        };

    } catch (error) {
        response.value = {
            status: error.response?.status || 500,
            statusText: error.message,
            headers: error.response?.headers || {},
            data: error.response?.data || error.message,
            time: 0,
            size: '0 B'
        };
        message.error('请求失败: ' + error.message);
    } finally {
        loading.value = false;
    }
};

// 重置表单
const resetForm = () => {
    debugRequest.method = 'GET';
    debugRequest.url = '';
    headersList.value = [];
    paramsList.value = [];
    formDataList.value = [];
    jsonBody.value = '';
    bodyType.value = 'none';
    response.value = null;
};

// 格式化响应数据
const formatResponse = (data) => {
    try {
        return typeof data === 'object' ? JSON.stringify(data, null, 2) : data;
    } catch (e) {
        return data;
    }
};

// 快捷键处理
onMounted(() => {
    document.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
    document.removeEventListener('keydown', handleKeyDown);
});

const handleKeyDown = (e: KeyboardEvent) => {
    if (e.ctrlKey && e.key === 'Enter') {
        sendRequest();
    }
};

// 新增方法
const handleCancel = () => {
    Modal.confirm({
        title: '确认关闭',
        content: '关闭后将丢失未保存的修改,是否继续?',
        onOk: () => {
            debugModalState.open = false;
            resetForm();
        }
    });
};

const addCommonHeaders = () => {
    headersList.value.push(
        { key: 'Content-Type', value: 'application/json' },
        { key: 'Accept', value: '*/*' }
    );
};

const clearHeaders = () => {
    Modal.confirm({
        title: '确认清空',
        content: '是否清空所有Headers?',
        onOk: () => {
            headersList.value = [];
        }
    });
};

const validateParams = () => {
    // ...参数验证逻辑
};

const validateJSON = () => {
    try {
        JSON.parse(jsonBody.value);
        message.success('JSON格式正确');
    } catch (e) {
        message.error('JSON格式错误:' + e.message);
    }
};

const copyResponse = () => {
    // ...复制响应内容
};

const downloadResponse = () => {
    // ...下载响应内容
};

const searchResponse = () => {
    // ...搜索响应内容
};

const protocol = ref('http');
const urlHistory = ref<Array<{value: string, label: string}>>([]);
const responseView = ref('pretty');
const commonHeaders = [
  { key: 'Content-Type', value: 'application/json' },
  { key: 'Accept', value: '*/*' },
  { key: 'Authorization', value: 'Bearer ' }
  // 更多常用headers...
];

// 搜索抽屉状态
const searchDrawer = reactive({
  visible: false,
  keyword: '',
  caseSensitive: false,
  useRegex: false
});

// 方法扩展
const getMethodClass = (method: string) => {
  const classes = {
    GET: 'method-get',
    POST: 'method-post',
    PUT: 'method-put',
    DELETE: 'method-delete'
  };
  return classes[method] || '';
};

const getStatusClass = (status: number) => {
  if (status < 300) return 'success';
  if (status < 400) return 'warning';
  return 'error';
};

const getStatusBadge = (status: number) => {
  if (status < 300) return 'success';
  if (status < 400) return 'warning';
  return 'error';
};

const handleMethodChange = (method: string) => {
  // 根据方法自动添加相关headers
  if (method === 'POST' || method === 'PUT') {
    addCommonHeader({ key: 'Content-Type' });
  }
};

const handleUrlSelect = (url: string) => {
  // 保存到历史记录
  if (!urlHistory.value.find(item => item.value === url)) {
    urlHistory.value.unshift({ value: url, label: url });
    if (urlHistory.value.length > 10) {
      urlHistory.value.pop();
    }
  }
};

const confirmReset = () => {
  Modal.confirm({
    title: '确认重置',
    content: '是否清空所有已配置的请求参数？',
    onOk: resetForm
  });
};

defineExpose({
    debugModalState,
    debugRequest,
    headersList,
    paramsList,
    formDataList,
    jsonBody,
    bodyType,
    resetForm
});
</script>

<style lang="scss" scoped>
.debug-container {
  // ... 原有样式 ...

  // 新增样式
  .method-get { color: #52c41a; }
  .method-post { color: #1890ff; }
  .method-put { color: #faad14; }
  .method-delete { color: #ff4d4f; }

  .json-toolbar {
    position: absolute;
    right: 8px;
    top: 8px;
    z-index: 1;
    background: rgba(255,255,255,0.9);
    padding: 4px;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }

  .response-header {
    .status {
      display: flex;
      align-items: center;
      gap: 8px;

      &.warning { color: #faad14; }
      &.error { color: #ff4d4f; }
    }
  }

  // ...其他原有样式...
}
</style>
``` 