  <!-- 角色授权 -->
<template>
  <!-- 分配权限弹窗 -->
  <el-drawer v-model="drawerVisible" :title="'【' + props.roleName + '】权限分配'" :size="drawerSize">
    <el-container>
      <!-- 数据权限 -->
      <el-aside >
        <div class="border-r-1 border-r-[#f0f0f0] b-r-solid h-[100%] p-[20px] box-border">
          <div class="flex items-center">
            <div style="display: flex; gap: 10px; ">
              <div style="width: 10px; background-color: #409eff;"></div>
              <div>
                <span style="font-size: 16px;">数据授权</span>
                <el-tooltip placement="right">
                  <template #content>
                    <span>授权用户可操作的数据范围</span>
                  </template>
                  <el-icon class="ml-1 inline-block cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </div>
          </div>
          <div class="mt-3">
            <el-form ref="dataFormRef" :model="permissionState">
              <el-form-item prop="data_scope">
                <el-select v-model="permissionState.data_scope">
                  <el-option :key="1" label="仅本人数据权限" :value="1" />
                  <el-option :key="2" label="本部门数据权限" :value="2" />
                  <el-option :key="3" label="本部门及以下数据权限" :value="3" />
                  <el-option :key="4" label="全部数据权限" :value="4" />
                  <el-option :key="5" label="自定义数据权限" :value="5" />
                </el-select>
                </el-form-item>
              </el-form>
              
              <div class="mt-5 max-h-[60vh] b-1 b-solid b-[#e5e7eb] p-10px overflow-auto box-border" v-if="permissionState.data_scope === 5 && deptTreeData.length">
                <el-input v-model="deptFilterText" placeholder="部门名称" />
                <el-tree 
                  ref="deptTreeRef"
                  node-key="value"
                  show-checkbox
                  :data="deptTreeData"
                  :filter-node-method="handleFilter"
                  default-expand-all
                  :highlight-current="true"
                  :check-strictly="!parentChildLinked"
                  @check="deptTreeCheck"
                  style="height: calc(100% - 60px); overflow-y: auto; margin-top: 10px;"
                  >
                  <template #empty>
                    <el-empty :image-size="80" description="暂无数据" />
                  </template>
                </el-tree>
              </div>
          </div>
        </div>
      </el-aside>

      <!-- 菜单权限 -->
      <el-main>
        <div style="display: flex; gap: 10px; ">
          <div style="width: 10px; background-color: #409eff;"></div>
          <div>
            <span style="font-size: 16px;">菜单授权</span>
            <el-tooltip placement="right">
              <template #content>
                <span>授权用户可操作的菜单权限</span>
              </template>
              <el-icon class="ml-1 inline-block cursor-pointer">
                <QuestionFilled />
              </el-icon>
            </el-tooltip>
          </div>
        </div>
        <div class="mt-3 flex-x-between">
          <el-input v-model="permFilterText" placeholder="菜单名称" />
          <div class="flex-center ml-5">
            <el-button type="primary" size="small" plain @click="togglePermTree">
              <template #icon>
                <Switch />
              </template>
              {{ isExpanded ? "收缩" : "展开" }}
            </el-button>
            <el-checkbox v-model="parentChildLinked" class="ml-5" @change="handleParentChildLinkedChange">
              父子联动
            </el-checkbox>

            <el-tooltip placement="bottom">
              <template #content>
                如果只需勾选菜单权限，不需要勾选子菜单或者按钮权限，请关闭父子联动
              </template>
              <el-icon class="ml-1 color-[--el-color-primary] inline-block cursor-pointer">
                <QuestionFilled />
              </el-icon>
            </el-tooltip>
          </div>
        </div>

        <div class="mt-5 max-h-[65vh] b-1 b-solid b-[#e5e7eb] p-10px overflow-auto box-border">
          <el-tree 
            ref="permTreeRef" 
            node-key="value" 
            show-checkbox 
            :data="menuTreeData"
            :filter-node-method="handleFilter" 
            default-expand-all
            :highlight-current="true"
            :check-strictly="!parentChildLinked"
            @check="menuTreeCheck"
            style="height: calc(100% - 60px); overflow: auto; margin-top: 10px;">
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
          </el-tree>
        </div>
      </el-main>
    </el-container>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel">取 消</el-button>
        <el-button type="primary" @click.stop="handleDrawerSave">确 定</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup lang="ts">
// 添加 props 来接收 dictType
const props = defineProps({
  roleName: {
    type: String,
    required: true
  },
  roleId: {
    type: Number,
    required: true
  },
  modelValue: {
    type: Boolean,
    required: true
  }
})

import { listToTree, formatTree } from "@/utils/common";
import RoleAPI, { permissionDataType, permissionDeptType, permissionMenuType } from "@/api/system/role";
import DeptAPI from "@/api/system/dept";
import MenuAPI from "@/api/system/menu";
import type { TreeInstance } from 'element-plus'
import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";

const appStore = useAppStore();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "800px" : "90%"));
const emit = defineEmits(['update:modelValue'])

const permTreeRef = ref<TreeInstance>();
const deptTreeRef = ref<TreeInstance>()
const deptFilterText = ref("")
const permFilterText = ref("");
const dataFormRef = ref();
const drawerVisible = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emit('update:modelValue', value)
  }
})
const isExpanded = ref(true);
const parentChildLinked = ref(true)
const loading = ref<boolean>(false);
const deptTreeData = ref<permissionDeptType[]>([]);
const menuTreeData = ref<permissionMenuType[]>([]);
const permissionState = ref<permissionDataType>({
  role_ids: [],
  menu_ids: [],
  data_scope: 1,
  dept_ids: []
});

// 初始化方法,用于打开抽屉并加载数据
const init = async () => {
  loading.value = true;

  try {
    // 获取全部部门树
    const deptResponse = await DeptAPI.getDeptList();
    deptTreeData.value = formatTree(listToTree(deptResponse.data.data.items));

    // 获取全部菜单树
    const menuResponse = await MenuAPI.getMenuList();
    menuTreeData.value = formatTree(listToTree(menuResponse.data.data.items));

    // 获取角色详情
    const roleResponse = await RoleAPI.getRoleDetail(props.roleId);

    // 更新权限状态
    permissionState.value = {
      role_ids: [props.roleId],
      menu_ids: roleResponse.data.data.menus?.map(menu => menu.id) || [],
      data_scope: roleResponse.data.data.data_scope || 1,
      dept_ids: roleResponse.data.data.depts?.map(dept => dept.id) || []
    };

    // 回显菜单树选中项
    if (permTreeRef.value) {
      await permTreeRef.value.setCheckedKeys(permissionState.value.menu_ids);
    }

    // 修改：增加对 deptTreeRef.value 的存在性判断，并添加日志
    if (permissionState.value.data_scope === 5 && deptTreeRef.value) {
      // await 一定不能丢，否则到导致初始化时候deptTreeRef.value 为 undefined
      await deptTreeRef.value.setCheckedKeys(permissionState.value.dept_ids);
    }

  } catch (error: any) {
    ElMessage.error('获取权限数据失败: ' + error.message);
  } finally {
    loading.value = false;
    // handleCancel()
  }
}

// 取消按钮处理函数
function handleCancel() {
  drawerVisible.value = false;
}

// 保存权限设置
async function handleDrawerSave () {
  try {
    loading.value = true;

    // 构造提交数据
    const submitData : permissionDataType = {
      role_ids: [props.roleId],
      menu_ids: (permTreeRef.value?.getCheckedKeys() || []).map(key => Number(key)),
      data_scope: permissionState.value.data_scope,
      dept_ids: (deptTreeRef.value?.getCheckedKeys() || []).map(key => Number(key))
    };

    await RoleAPI.setPermission(submitData)
    
  } catch (error: any) {
    console.error('保存失败:', error);
    ElMessage.error('保存失败: ' + error.message);
  } finally {
    loading.value = false;
    drawerVisible.value = false;
  }
}

// 部门树选择回调
const deptTreeCheck = (checkedIds: number[]) => {
  permissionState.value.dept_ids = checkedIds;
}

// 菜单选择变更回调
const menuTreeCheck = (checkedIds: number[]) => {
  permissionState.value.menu_ids = checkedIds;
}

// 展开/收缩 菜单权限树
function togglePermTree() {
  isExpanded.value = !isExpanded.value;
  if (permTreeRef.value) {
    Object.values(permTreeRef.value.store.nodesMap).forEach((node: any) => {
      if (isExpanded.value) {
        node.expand();
      } else {
        node.collapse();
      }
    });
  }
}

// 部门筛选
watch(deptFilterText, (val) => {
  deptTreeRef.value!.filter(val);
})

// 菜单筛选
watch(permFilterText, (val) => {
  permTreeRef.value!.filter(val);
});

// 树节点过滤
function handleFilter(
  value: string,
  data: {[key: string]: any;}
) {
  if (!value) return true;
  return data.label.includes(value);
}

// 父子菜单节点是否联动
function handleParentChildLinkedChange(val: any) {
  parentChildLinked.value = val;
}

onMounted(async () => {
  await init();
})
</script>

<style lang="scss" scoped></style>
