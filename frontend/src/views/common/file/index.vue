<template>
    <div>
        <!-- 页面头部 -->
        <page-header />

        <!-- 表格区域 -->
        <a-card title="文件列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }">
            <div class="file-manager">
                <!-- 工具栏 -->
                <div class="toolbar">
                    <a-space>
                        <a-button type="primary" @click="handleUpload">
                            <template #icon>
                                <UploadOutlined />
                            </template>
                            上传文件
                        </a-button>
                        <a-button @click="handleCreateFolder">
                            <template #icon>
                                <FolderAddOutlined />
                            </template>
                            新建文件夹
                        </a-button>
                        <a-button danger :disabled="!selectedRows.length" @click="handleBatchDelete">
                            <template #icon>
                                <DeleteOutlined />
                            </template>
                            批量删除
                        </a-button>
                        <a-button @click="handleRefresh">
                            <template #icon>
                                <ReloadOutlined />
                            </template>
                            刷新
                        </a-button>
                    </a-space>

                    <a-input-search v-model:value="searchText" placeholder="搜索文件名" style="width: 250px"
                        @search="onSearch" allow-clear enter-button />
                </div>

                <!-- 面包屑导航 -->
                <a-breadcrumb class="mb-4">
                    <a-breadcrumb-item>
                        <a @click="navigateToRoot">根目录</a>
                    </a-breadcrumb-item>
                    <a-breadcrumb-item v-for="(path, index) in currentPath" :key="index">
                        <a @click="navigateTo(index)">{{ path }}</a>
                    </a-breadcrumb-item>
                </a-breadcrumb>

                <!-- 文件列表 -->
                <a-table :columns="columns" 
                    :data-source="fileList"
                    :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }" 
                    :loading="loading"
                    :pagination="{
                        current: 1,
                        pageSize: 10,
                        showSizeChanger: true,
                        showQuickJumper: true,
                        total: fileList.length,
                        showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
                    }" 
                    :style="{ minHeight: '550px' }">
                    <!-- 文件名列 -->
                    <template #bodyCell="{ column, record }">
                        <template v-if="column.key === 'fileName'">
                            <span class="file-name" @click="handleFileClick(record)">
                                <component :is="getFileIcon(record.type)" class="mr-2" />
                                {{ record.name }}
                            </span>
                        </template>

                        <!-- 大小列 -->
                        <template v-if="column.key === 'size'">
                            {{ formatFileSize(record.size) }}
                        </template>

                        <!-- 操作列 -->
                        <template v-if="column.key === 'action'">
                            <a-space>
                                <!-- <a-tooltip title="预览" v-if="isPreviewable(record)"> -->
                                <a title="预览">
                                    <EyeOutlined @click="handlePreview(record)" /> <span
                                        style="color: #1890ff;">预览</span>
                                </a>
                                <a title="下载" v-if="record.type !== 'folder'">
                                    <DownloadOutlined @click="handleDownload(record)" style="color: blue;" /> <span
                                        style="color: blue;">下载</span>
                                </a>
                                <a title="重命名">
                                    <EditOutlined @click="handleRename(record)" style="color: blue;" /> <span
                                        style="color: blue;">重命名</span>
                                </a>
                                <a title="删除">
                                    <DeleteOutlined @click="handleDelete(record)" style="color: red;" /> <span
                                        style="color: red;">删除</span>
                                </a>
                            </a-space>
                        </template>
                    </template>
                </a-table>
            </div>
        </a-card>

        <!-- 上传文件对话框 -->
        <a-modal v-model:open="uploadModalVisible" title="上传文件" @ok="confirmUpload" @cancel="cancelUpload"
            :maskClosable="false">
            <a-upload-dragger v-model:fileList="uploadFileList" :multiple="true" :action="uploadApi"
                :headers="uploadHeaders" :before-upload="beforeUpload" @change="handleUploadChange">
                <p class="ant-upload-drag-icon">
                    <InboxOutlined />
                </p>
                <p class="ant-upload-text">点击或拖拽文件到此区域上传</p>
                <p class="ant-upload-hint">
                    支持单个或批量上传，单个文件大小不超过 {{ maxFileSize }}MB
                </p>
            </a-upload-dragger>
        </a-modal>

        <!-- 新建文件夹对话框 -->
        <a-modal v-model:open="folderModalVisible" title="新建文件夹" @ok="confirmCreateFolder" @cancel="cancelCreateFolder">
            <a-form :model="folderForm" :rules="folderRules">
                <a-form-item label="文件夹名称" name="name">
                    <a-input v-model:value="folderForm.name" placeholder="请输入文件夹名称" @pressEnter="confirmCreateFolder" />
                </a-form-item>
            </a-form>
        </a-modal>

        <!-- 重命名对话框 -->
        <a-modal v-model:open="renameModalVisible" title="重命名" @ok="confirmRename" @cancel="cancelRename">
            <a-form :model="renameForm" :rules="renameRules">
                <a-form-item label="新名称" name="newName">
                    <a-input v-model:value="renameForm.newName" placeholder="请输入新名称" @pressEnter="confirmRename" />
                </a-form-item>
            </a-form>
        </a-modal>

        <!-- 预览对话框 -->
        <a-modal v-model:open="previewModalVisible" title="文件预览" :footer="null" width="800px" :maskClosable="false">
            <div class="preview-content">
                <!-- 根据文件类型显示不同的预览内容 -->
                <img v-if="isImage" :src="previewUrl" style="max-width: 100%" />
                <video v-else-if="isVideo" :src="previewUrl" controls style="max-width: 100%" />
                <div v-else class="unsupported-preview">
                    该文件类型暂不支持预览
                </div>
            </div>
        </a-modal>
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, h, resolveComponent } from 'vue';
import { message, Modal } from 'ant-design-vue';
import {
    UploadOutlined,
    FolderAddOutlined,
    DeleteOutlined,
    DownloadOutlined,
    ReloadOutlined,
    EditOutlined,
    InboxOutlined,
    FileOutlined,
    FolderOutlined,
    EyeOutlined
} from '@ant-design/icons-vue';
import PageHeader from '@/components/PageHeader.vue';
import { getFileList, uploadFile, downloadFile, downloadFileResource, uploadFileOne, uploadFileMany } from '@/api/common/file';
import storage from 'store';

// 常量定义
const maxFileSize = 100; // 最大文件大小(MB)
const supportedPreviewTypes = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'webm'];
const uploadApi = import.meta.env.VITE_APP_BASE_API + '/api/v1/file/upload';

// 表格列定义
const columns = [
    {
        title: '文件名',
        dataIndex: 'name',
        key: 'name',
        ellipsis: true,
        width: 200,
        customRender: ({ text, record }: { text: string, record: tableDataType }) => {
            return h('span', {}, [
                h(record.type === 'directory' ? FolderOutlined : FileOutlined, { style: 'margin-right: 8px' }),
                text
            ]);
        }
    },
    {
        title: '大小',
        dataIndex: 'size',
        key: 'size',
        width: 120,
        customRender: ({ text, record }: { text: number | null, record: tableDataType }) => {
            return record.type === 'directory' ? '-' : formatFileSize(text || 0);
        },
        sorter: (a: tableDataType, b: tableDataType) => {
            if (a.type === 'directory' && b.type === 'directory') return 0;
            if (a.type === 'directory') return -1;
            if (b.type === 'directory') return 1;
            return (a.size || 0) - (b.size || 0);
        },
    },
    {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
        width: 120,
        customRender: ({ text }: { text: string }) => text === 'directory' ? '文件夹' : '文件',
        sorter: (a: tableDataType, b: tableDataType) => (a.type || '').localeCompare(b.type || ''),
    },
    {
        title: '修改时间',
        dataIndex: 'modified_time',
        key: 'modified_time',
        width: 180,
        customRender: ({ text }: { text: string | null }) => formatTimestamp(text),
        sorter: (a: tableDataType, b: tableDataType) => {
            if (!a.modified_time || !b.modified_time) return 0;
            return new Date(a.modified_time).getTime() - new Date(b.modified_time).getTime();
        }
    },
    {
        title: '操作',
        key: 'action',
        width: 150,
        fixed: 'right',
        customRender: ({ record }: { record: tableDataType }) => {
            return h('div', { class: 'action-buttons' }, [
                h(resolveComponent('a-space'), {}, () => [
                    record.type !== 'directory' && h(resolveComponent('a-button'), {
                        type: 'link',
                        onClick: () => handleDownload(record)
                    }, () => '下载'),
                    h(resolveComponent('a-button'), {
                        type: 'link',
                        onClick: () => handleRename(record)
                    }, () => '重命名'),
                    h(resolveComponent('a-button'), {
                        type: 'link',
                        danger: true,
                        onClick: () => handleDelete([record])
                    }, () => '删除')
                ])
            ]);
        }
    }
];

// 状态定义
const loading = ref(false);
const searchText = ref('');
const fileList = ref<tableDataType[]>([]);
const selectedRowKeys = ref<string[]>([]);
const selectedRows = ref<tableDataType[]>([]);
const uploadModalVisible = ref(false);
const folderModalVisible = ref(false);
const renameModalVisible = ref(false);
const previewModalVisible = ref(false);
const uploadFileList = ref([]);
const currentPath = ref<string[]>([]);
const previewUrl = ref('');
const isImage = ref(false);
const isVideo = ref(false);

export interface tableDataType {
    name?: string;
    size?: number;
    type?: string;
    modified_time?: string;
}

// 表单状态
const folderForm = reactive({
    name: ''
});

const renameForm = reactive({
    newName: '',
    record: null as tableDataType
});

// 表单校验规则
const folderRules = {
    name: [
        { required: true, message: '请输入文件夹名称' },
        { max: 50, message: '文件夹名称不能超过50个字符' },
        { pattern: /^[^\\/:*?"<>|]+$/, message: '文件夹名称不能包含特殊字符' }
    ]
};

const renameRules = {
    newName: [
        { required: true, message: '请输入新名称' },
        { max: 100, message: '名称不能超过100个字符' },
        { pattern: /^[^\\/:*?"<>|]+$/, message: '名称不能包含特殊字符' }
    ]
};

// 上传相关
const uploadHeaders = {
    Authorization: 'Bearer ' + storage.get('Access-Token')
};

// 生命周期钩子
onMounted(() => {
    loadFileList();
});

// 方法定义
const loadFileList = async () => {
    loading.value = true;
    try {
        const res = await getFileList({
            path: currentPath.value.join('/')
        });
        // 确保数据符合 tableDataType 接口
        fileList.value = (res.data.data || []).map((item: any) => ({
            name: item.name || '',
            size: typeof item.size === 'number' ? item.size : null,
            type: item.type || '',
            modified_time: item.modified_time || null
        }));
    } catch (error) {
        message.error('获取文件列表失败');
        console.error('获取文件列表失败:', error);
    } finally {
        loading.value = false;
    }
};

const handleRefresh = () => {
    loadFileList();
};

const formatFileSize = (size: number) => {
    if (!size) return '-';
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let index = 0;
    while (size >= 1024 && index < units.length - 1) {
        size /= 1024;
        index++;
    }
    return size.toFixed(2) + ' ' + units[index];
};

const formatTimestamp = (timestamp: string | null) => {
    if (!timestamp) return '-';
    return new Date(timestamp).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
};

const isPreviewable = (record: tableDataType) => {
    if (record.type === 'folder') return false;
    const ext = record.name.split('.').pop()?.toLowerCase();
    return supportedPreviewTypes.includes(ext || '');
};

const handlePreview = (record: tableDataType) => {
    previewModalVisible.value = true;
    // previewUrl.value = record.url;
    const ext = record.name.split('.').pop()?.toLowerCase();
    isImage.value = ['jpg', 'jpeg', 'png', 'gif'].includes(ext || '');
    isVideo.value = ['mp4', 'webm'].includes(ext || '');
};

const beforeUpload = (file: File) => {
    const isLt100M = file.size / 1024 / 1024 < maxFileSize;
    if (!isLt100M) {
        message.error(`文件大小不能超过 ${maxFileSize}MB!`);
    }
    return isLt100M;
};

const handleFileClick = (record: tableDataType) => {
    if (record.type === 'folder') {
        currentPath.value.push(record.name);
        loadFileList();
    }
};

const navigateToRoot = () => {
    currentPath.value = [];
    loadFileList();
};

const navigateTo = (index: number) => {
    currentPath.value = currentPath.value.slice(0, index + 1);
    loadFileList();
};

const handleBatchDelete = () => {
    Modal.confirm({
        title: '确认删除',
        content: `确定要删除选中的 ${selectedRows.value.length} 个文件/文件夹吗？`,
        okText: '确认',
        cancelText: '取消',
        onOk: () => handleDelete(selectedRows.value)
    });
};

const handleUpload = () => {
    uploadModalVisible.value = true;
};

const handleCreateFolder = () => {
    folderModalVisible.value = true;
};

const handleDelete = async (records: tableDataType[]) => {
    // TODO: 实现删除逻辑
};

const handleDownload = async (record: tableDataType) => {
    // TODO: 实现下载逻辑
};

const handleRename = (record: tableDataType) => {
    renameModalVisible.value = true;
    renameForm.record = record;
    renameForm.newName = record.name;
};

const confirmUpload = () => {
    uploadModalVisible.value = false;
    loadFileList();
};

const cancelUpload = () => {
    uploadModalVisible.value = false;
    uploadFileList.value = [];
};

const confirmCreateFolder = async () => {
    // TODO: 实现创建文件夹逻辑
};

const cancelCreateFolder = () => {
    folderModalVisible.value = false;
    folderForm.name = '';
};

const confirmRename = async () => {
    // TODO: 实现重命名逻辑
};

const cancelRename = () => {
    renameModalVisible.value = false;
    renameForm.newName = '';
    renameForm.record = null;
};

const handleUploadChange = (info: any) => {
    // TODO: 实现上传状态变化处理逻辑
};

const onSearch = (value: string) => {
    // TODO: 实现搜索逻辑
};

const onSelectChange = (keys: string[], rows: tableDataType[]) => {
    selectedRowKeys.value = keys;
    selectedRows.value = rows;
};

const getFileIcon = (type: string) => {
    return type === 'folder' ? FolderOutlined : FileOutlined;
};

</script>

<style lang="scss" scoped>
.file-manager {
    .toolbar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 16px;
    }

    .file-name {
        display: flex;
        align-items: center;
        cursor: pointer;

        &:hover {
            color: #1890ff;
        }
    }
}

.preview-content {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 200px;

    .unsupported-preview {
        color: #999;
        font-size: 16px;
    }
}
</style>
