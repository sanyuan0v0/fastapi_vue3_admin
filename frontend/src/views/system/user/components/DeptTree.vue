<!-- 部门树 -->
<template>
  <el-card shadow="hover">
    <el-input v-model="deptName" placeholder="部门名称" clearable>
      <template #prefix>
        <el-icon>
          <Search />
        </el-icon>
      </template>
    </el-input>

    <el-tree ref="deptTreeRef" class="mt-2" :data="deptList"
      :props="{ children: 'children', label: 'label', disabled: '' }" :expand-on-click-node="false"
      :filter-node-method="handleFilter" default-expand-all @node-click="handleNodeClick" />
  </el-card>
</template>

<script setup lang="ts">
import DeptAPI, { DeptPageQuery } from "@/api/system/dept";
import { listToTree } from "@/utils/common";

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: undefined,
  },
});

const deptList = ref<OptionType[]>(); // 部门列表
const deptTreeRef = ref(); // 部门树
const deptName = ref(); // 部门名称

const emits = defineEmits(["node-click"]);

const deptId = useVModel(props, "modelValue", emits);

watchEffect(
  () => {
    deptTreeRef.value.filter(deptName.value);
  },
  {
    flush: "post", // watchEffect会在DOM挂载或者更新之前就会触发，此属性控制在DOM元素更新后运行
  }
);

/**
 * 部门筛选
 */
function handleFilter(value: string, data: any) {
  if (!value) {
    return true;
  }
  return data.label.indexOf(value) !== -1;
}

/** 部门树节点 Click */
function handleNodeClick(data: { [key: string]: any }) {
  deptId.value = data.value;
  emits("node-click");
}

const queryFormData = reactive<DeptPageQuery>({
  page_no: 1,
  page_size: 9999,
  name: undefined,
  status: undefined,
  start_time: undefined,
  end_time: undefined,
});

const loading = ref(true);

onBeforeMount(() => {
  loading.value = true;
  DeptAPI.getDeptList(queryFormData).then((response) => {
    deptList.value = listToTree(response.data.data.items);
  }).finally(() => {
    loading.value = false;
  });
});
</script>
