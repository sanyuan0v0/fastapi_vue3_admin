<template>
    <!-- 授权弹窗 -->
    <a-drawer v-model:open="openDrawer" :destroyOnClose="true" :title="`授权 - ${currentRole?.name || ''}`" placement="right" :width="1500"
        :bodyStyle="{ padding: 'none' }">
        <template #extra>
            <a-button type="primary" @click="handleDrawerSave" :loading="drawerSaving">保存</a-button>
        </template>

        <div style="display: flex;">
            <div style="min-width: 300px;">
                <div style="display: flex; gap: 10px; ">
                    <div style="width: 10px; background-color: #1677ff;"></div>
                    <div>
                        <span style="font-size: 16px;">数据授权</span>
                        <a-tooltip placement="right">
                            <template #title>
                                <span>授权用户可操作的数据范围</span>
                            </template>
                            <QuestionCircleOutlined style="margin-left: 5px;" />
                        </a-tooltip>
                    </div>
                </div>

                <a-select v-model:value="permissionState.data_scope" style="width: 80%; margin-top: 15px;">
                    <a-select-option :value="1">仅本人数据权限</a-select-option>
                    <a-select-option :value="2">本部门数据权限</a-select-option>
                    <a-select-option :value="3">本部门及以下数据权限</a-select-option>
                    <a-select-option :value="4">全部数据权限</a-select-option>
                    <a-select-option :value="5">自定义数据权限</a-select-option>
                </a-select>

                <a-tree v-if="permissionState.data_scope === 5 && deptTreeData.length"
                    :checkedKeys="permissionState.dept_ids"
                    :rowKey="record => record.id"
                    :tree-data="deptTreeData"
                    defaultExpandAll="true"
                    :scroll="{ y: 1000 }"
                    :field-names="{ children: 'children', title: 'name', key: 'id' }"
                    @check="deptTreeCheck" checkable checkStrictly style="margin-top: 15px;" />
            </div>

            <a-divider type="vertical" style="height: 80vh;" />

            <div>
                <div style="display: flex; gap: 10px;">
                    <div style="width: 10px; background-color: #1677ff;"></div>
                    <div>
                        <span style="font-size: 16px;">菜单授权</span>
                        <a-tooltip placement="right">
                            <template #title>
                                <span>授权用户在菜单中可操作的范围</span>
                            </template>
                            <QuestionCircleOutlined style="margin-left: 5px;" />
                        </a-tooltip>
                    </div>
                </div>

                <div style="margin-top: 15px;">
                    <a-table v-if="menuTreeData"
                        :rowKey="record => record.id"
                        :defaultExpandAllRows="true"
                        :columns="menuColumns"
                        :data-source="menuTreeData"
                        :row-selection="menuRowSelection"
                        :loading="tableLoading"
                        :scroll="{ y: 1000 }"
                        :pagination="false"
                        :style="{ minHeight: '700px' }"
                        :expandAll="true">
                        <template v-slot:bodyCell="{ column, record }">
                            <template v-if="column.dataIndex === 'type'">
                                <a-tag :color="record.type === 1 ? 'blue' : (record.type === 2 ? 'green' : 'orange')">
                                    {{ record.type === 1 ? '目录' : (record.type === 2 ? '功能' : '权限') }}
                                </a-tag>
                            </template>
                            <template v-if="column.dataIndex === 'available'">
                                <span>
                                    <a-badge :status="record.available ? 'processing': 'error'" :text="record.available ? '启用' : '停用'" />
                                </span>
                            </template>
                        </template>
                    </a-table>
                </div>
            </div>
        </div>

        <template #footer>
            <div style="height: 50px;"></div>
        </template>
    </a-drawer>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { listToTree } from '@/utils/util';
import { message } from 'ant-design-vue';
import type { TableColumnsType } from 'ant-design-vue';
import { QuestionCircleOutlined } from '@ant-design/icons-vue';
import type { tableDataType, permissionDataType, permissionDeptType, permissionMenuType } from './types'
import { getMenuList } from '@/api/system/menu';
import { getDeptList } from '@/api/system/dept';
import { setPermission } from '@/api/system/role';

const openDrawer = ref(false);
const currentRole = ref(null);
const permissionState = ref<permissionDataType>({
    role_ids: [],
    menu_ids: [],
    data_scope: 1,
    dept_ids: []
});

const deptTreeData = ref<permissionDeptType[]>([]);
const menuTreeData = ref<permissionMenuType[]>([]);
const tableLoading = ref(false);
const drawerSaving = ref(false);

const menuColumns: TableColumnsType = [
    {
        title: '菜单名称',
        dataIndex: 'name'
    },
    {
        title: '菜单类型',
        dataIndex: 'type',
        width: 100
    },
    {
        title: '权限标识',
        dataIndex: 'permission',
    },
    {
        title: '状态',
        dataIndex: 'available',
        width: 100
    },
    {
        title: '备注',
        dataIndex: 'description',
        ellipsis: true,
        width: 400
    }
];

// 初始化方法,用于打开抽屉并加载数据
const init = async (record: tableDataType) => {
    if (!record) {
        message.error('请选择角色')
        return
    }

    openDrawer.value = true;
    tableLoading.value = true;

    try {
        // 获取部门树
        const deptResponse = await getDeptList();
        deptTreeData.value = listToTree(deptResponse.data.data.items);

        // 获取菜单树
        const menuResponse = await getMenuList();
        menuTreeData.value = listToTree(menuResponse.data.data.items);

        currentRole.value = record;

        // 初始化权限状态
        permissionState.value = {
            role_ids: [record.id],
            menu_ids: record.menus?.map(menu => menu.id) || [],
            data_scope: record.data_scope || 1,
            dept_ids: record.depts?.map(dept => dept.id) || []
        }

    } catch (error) {
        console.error('获取权限数据失败:', error);
        message.error('获取权限数据失败');
    } finally {
        tableLoading.value = false;
    }
}

// 部门树选择回调
const deptTreeCheck = (checkedKeys) => {
    permissionState.value.dept_ids = checkedKeys.checked;
}

const emit = defineEmits(['event']);

// 保存权限设置
const handleDrawerSave = () => {
    drawerSaving.value = true;

    setPermission(permissionState.value).then(response => {
        message.success(response.data.msg);
        drawerSaving.value = false;
        openDrawer.value = false;
        emit('event');
    }).catch(error => {
        console.error('保存权限失败:', error);
        message.error('保存权限失败');
        drawerSaving.value = false;
    })
}

// 菜单选择变更回调
const onMenuSelectChange = (selectingRowKeys: permissionMenuType['id'][]) => {
    permissionState.value.menu_ids = selectingRowKeys;
}

// 菜单表格选择配置
const menuRowSelection = computed(() => {
    return {
        selectedRowKeys: permissionState.value.menu_ids,
        checkStrictly: false,
        onChange: onMenuSelectChange
    }
});

defineExpose({
    init,
    permissionState
});

</script>

<style lang="scss" scoped></style>