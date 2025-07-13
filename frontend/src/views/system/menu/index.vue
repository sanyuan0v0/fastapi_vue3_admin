<!-- 菜单管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryFormData" :inline="true">
        <el-form-item prop="notice_title" label="标题">
          <el-input v-model="queryFormData.name" placeholder="请输入标题" clearable />
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select v-model="queryFormData.status" placeholder="请选择状态" clearable style="width: 160px">
            <el-option value="true" label="启用" />
            <el-option value="false" label="停用" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <el-date-picker v-model="queryFormData.start_time" type="daterange" value-format="yyyy-MM-dd"
            range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button type="primary" icon="search" @click="handleQuery">查询</el-button>
          <el-button icon="refresh" @click="handleResetQuery">重置</el-button>
          <!-- 展开/收起 -->
          <template v-if="isExpandable">
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
              {{ isExpand ? "收起" : "展开" }}
              <el-icon>
                <template v-if="isExpand">
                  <ArrowUp />
                </template>
                <template v-else>
                  <ArrowDown />
                </template>
              </el-icon>
            </el-link>
          </template>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card shadow="hover" class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="公告通知管理维护系统的公告和通知。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            公告通知列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--actions">
          <el-button type="success" icon="plus" @click="handleOpenDialog('create')">新增</el-button>
          <el-button type="danger" icon="delete" :disabled="selectIds.length === 0"
            @click="handleOperation('delete')">批量删除</el-button>
          <el-dropdown>
            <el-button type="default" :disabled="selectIds.length === 0" icon="ArrowDown">更多
            </el-button>
            <template #dropdown>
              <el-menu @click="handleMoreClick">
                <el-menu-item key="1">
                  <span>
                    <el-icon>
                      <Check />
                    </el-icon>
                    <span>批量启用</span>
                  </span>
                </el-menu-item>
                <el-menu-item key="2">
                  <span>
                    <el-icon>
                      <CircleClose />
                    </el-icon>
                    <span>批量停用</span>
                  </span>
                </el-menu-item>
              </el-menu>
            </template>
          </el-dropdown>
        </div>
        <div class="data-table__toolbar--tools">
          <el-tooltip content="导入">
            <el-button type="info" icon="upload" circle @click="handleOperation('import')" />
          </el-tooltip>
          <el-tooltip content="导出">
            <el-button type="warning" icon="download" circle @click="handleOperation('export')" />
          </el-tooltip>
          <el-tooltip content="刷新">
            <el-button type="primary" icon="refresh" circle @click="handleRefresh" />
          </el-tooltip>
          <el-tooltip content="列表筛选">
            <el-dropdown trigger="click">
              <el-button type="default" icon="operation" circle />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-for="column in tableColumns" :key="column.prop" :command="column">
                    <el-checkbox v-model="column.show">{{ column.label }}</el-checkbox>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-tooltip>
        </div>
      </div>

      <!-- 表格区域 -->
      <el-table ref="dataTableRef" v-loading="loading" row-key="id" :data="pageTableData" :tree-props="{
        children: 'children',
        hasChildren: 'hasChildren',
      }" class="data-table__content" height="450" border stripe @selection-change="handleSelectionChange"
        @row-click="handleRowClick">
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'selection')?.show" type="selection" width="55"
          align="center" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'index')?.show" type="index" fixed label="序号"
          width="60" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'name')?.show" key="name" label="菜单名称" prop="name"
          min-width="120">
          <template #default="scope">

            {{ scope.row.name }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'icon')?.show" key="icon" label="图标" prop="icon"
          min-width="80" align="center">
          <template #default="scope">
            <template v-if="scope.row.icon && scope.row.icon.startsWith('el-icon')">
              <el-icon style="vertical-align: -0.15em">
                <component :is="scope.row.icon.replace('el-icon-', '')" />
              </el-icon>
            </template>
            <template v-else-if="scope.row.icon">
              <div :class="`i-svg:${scope.row.icon}`" />
            </template>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'status')?.show" key="status" label="状态"
          prop="status" min-width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === true ? 'success' : 'danger'">
              {{ scope.row.status ? "启用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'type')?.show" key="type" label="类型" prop="type"
          min-width="80" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.type === MenuTypeEnum.CATALOG" type="warning">目录</el-tag>
            <el-tag v-if="scope.row.type === MenuTypeEnum.MENU" type="success">菜单</el-tag>
            <el-tag v-if="scope.row.type === MenuTypeEnum.BUTTON" type="danger">按钮</el-tag>
            <el-tag v-if="scope.row.type === MenuTypeEnum.EXTLINK" type="info">外链</el-tag>
          </template>
        </el-table-column>

        <el-table-column v-if="tableColumns.find(col => col.prop === 'order')?.show" key="order" label="排序" prop="order"
          min-width="80" align="center" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'permission')?.show" key="permission" label="权限标识"
          prop="permission" min-width="100" align="center" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'router_name')?.show" key="router_name"
          label="路由名称" prop="router_name" min-width="80" align="left" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'route_path')?.show" key="route_path" label="路由路径"
          prop="router_name" min-width="80" align="left" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'component_path')?.show" key="component_path"
          label="组件路径" prop="component_path" min-width="80" align="left" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'redirect')?.show" key="redirect" label="重定向"
          prop="redirect" min-width="80" align="left" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'keep_alive')?.show" key="keep_alive" label="是否缓存"
          prop="keep_alive" min-width="80" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.keep_alive" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'hidden')?.show" key="hidden" label="是否隐藏"
          prop="hidden" min-width="80" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.hidden" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'always_show')?.show" key="always_show"
          label="显示根路由" prop="always_show" min-width="80" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.always_show" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'title')?.show" key="title" label="菜单标题"
          prop="title" min-width="80" align="left" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'params')?.show" key="params" label="路由参数"
          prop="params" min-width="80" align="left" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'affix')?.show" key="affix" label="固定路由"
          prop="affix" min-width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.affix ? 'success' : 'danger'">
              {{ scope.row.affix ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column v-if="tableColumns.find(col => col.prop === 'description')?.show" key="description" label="描述"
          prop="description" min-width="100" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'created_at')?.show" key="created_at" label="创建时间"
          prop="created_at" min-width="120" sortable />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'updated_at')?.show" key="updated_at" label="更新时间"
          prop="updated_at" min-width="120" sortable />

        <el-table-column v-if="tableColumns.find(col => col.prop === 'operation')?.show" fixed="right" align="center"
          label="操作" min-width="220">
          <template #default="scope">
            <el-button v-if="scope.row.type == MenuTypeEnum.CATALOG || scope.row.type == MenuTypeEnum.MENU"
              type="primary" link size="small" icon="plus" @click.stop="handleOpenDialog(scope.row.id)">
              新增
            </el-button>

            <el-button type="info" size="small" link icon="document"
              @click.stop="handleOpenDialog('detail', scope.row.id)">详情</el-button>
            <el-button type="primary" size="small" link icon="edit"
              @click.stop="handleOpenDialog('update', scope.row.id)">编辑</el-button>
            <el-button type="danger" size="small" link icon="delete"
              @click.stop="handleOperation('delete', scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination v-if="total > 0" v-model:total="total" v-model:page="queryFormData.page_no" v-model:limit="queryFormData.page_size"
          @pagination="loadingData" />
      </template>
    </el-card>

    <!-- 弹窗区域 -->
    <el-drawer v-model="dialogVisible.visible" :title="dialogVisible.title" :size="drawerSize"
      @close="handleCloseDialog">
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="编号" :span="2">{{ detailFormData.id }}</el-descriptions-item>
          <el-descriptions-item label="菜单名称" :span="2">{{ detailFormData.name }}</el-descriptions-item>
          <el-descriptions-item label="菜单类型" :span="2">
            <el-tag v-if="detailFormData.type === MenuTypeEnum.CATALOG" type="warning">目录</el-tag>
            <el-tag v-if="detailFormData.type === MenuTypeEnum.MENU" type="success">菜单</el-tag>
            <el-tag v-if="detailFormData.type === MenuTypeEnum.BUTTON" type="danger">按钮</el-tag>
            <el-tag v-if="detailFormData.type === MenuTypeEnum.EXTLINK" type="info">外链</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="图标" :span="2">{{ detailFormData.icon }}</el-descriptions-item>
          <el-descriptions-item label="排序" :span="2">{{ detailFormData.order }}</el-descriptions-item>
          <el-descriptions-item label="权限标识" :span="2">{{ detailFormData.permission }}</el-descriptions-item>
          <el-descriptions-item label="路由名称" :span="2">{{ detailFormData.route_name }}</el-descriptions-item>
          <el-descriptions-item label="路由路径" :span="2">{{ detailFormData.route_path }}</el-descriptions-item>
          <el-descriptions-item label="组件路径" :span="2">{{ detailFormData.component_path }}</el-descriptions-item>
          <el-descriptions-item label="重定向" :span="2">{{ detailFormData.redirect }}</el-descriptions-item>
          <el-descriptions-item label="父级编号" :span="2">{{ detailFormData.parent_id }}</el-descriptions-item>
          <el-descriptions-item label="父级菜单" :span="2">{{ detailFormData.parent_name }}</el-descriptions-item>
          <el-descriptions-item label="是否缓存" :span="2">
            <el-tag :type="detailFormData.keep_alive ? 'success' : 'danger'">
              {{ detailFormData.keep_alive ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="是否显示" :span="2">
            <el-tag :type="detailFormData.hidden ? 'success' : 'danger'">
              {{ detailFormData.hidden ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="是否显示根路由" :span="2">
            <el-tag :type="detailFormData.always_show ? 'success' : 'danger'">
              {{ detailFormData.always_show ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="菜单标题" :span="2">{{ detailFormData.title }}</el-descriptions-item>
          <el-descriptions-item label="路由参数" :span="2">{{ detailFormData.params }}</el-descriptions-item>
          <el-descriptions-item label="是否固定路由" :span="2">
            <el-tag :type="detailFormData.affix ? 'success' : 'danger'">
              {{ detailFormData.affix ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="detailFormData.status ? 'success' : 'danger'">
              {{ detailFormData.status ? '启用' : '停用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="排序" :span="2">{{ detailFormData.order }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ detailFormData.description }}</el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">{{ detailFormData.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">{{ detailFormData.updated_at }}</el-descriptions-item>
        </el-descriptions>
      </template>

      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form ref="dataFormRef" :model="formData" :rules="rules" label-width="100px">
          <el-form-item label="父级菜单" prop="parent_id">
            <el-tree-select v-model="formData.parent_id" placeholder="选择上级菜单" :data="menuOptions" filterable
              check-strictly :render-after-expand="false" />
          </el-form-item>

          <el-form-item label="菜单名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入菜单名称" />
          </el-form-item>

          <el-form-item label="菜单类型" prop="type">
            <el-radio-group v-model="formData.type" @change="handleMenuTypeChange">
              <el-radio :value="MenuTypeEnum.CATALOG">目录</el-radio>
              <el-radio :value="MenuTypeEnum.MENU">菜单</el-radio>
              <el-radio :value="MenuTypeEnum.BUTTON">按钮</el-radio>
              <el-radio :value="MenuTypeEnum.EXTLINK">外链</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="formData.type == MenuTypeEnum.EXTLINK" label="外链地址" prop="path">
            <el-input v-model="formData.route_path" placeholder="请输入外链完整路径" />
          </el-form-item>

          <el-form-item v-if="formData.type == MenuTypeEnum.MENU" prop="routeName">
            <template #label>
              <div class="flex-y-center">
                路由名称
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    如果需要开启缓存，需保证页面 defineOptions 中的 name 与此处一致，建议使用驼峰。
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>
            <el-input v-model="formData.route_name" placeholder="User" />
          </el-form-item>

          <el-form-item v-if="formData.type == MenuTypeEnum.CATALOG || formData.type == MenuTypeEnum.MENU"
            prop="routePath">
            <template #label>
              <div class="flex-y-center">
                路由路径
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    定义应用中不同页面对应的 URL 路径，目录需以 / 开头，菜单项不用。例如：系统管理目录
                    /system，系统管理下的用户管理菜单 user。
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>
            <el-input v-if="formData.type == MenuTypeEnum.CATALOG" v-model="formData.route_path" placeholder="system" />
            <el-input v-else v-model="formData.route_path" placeholder="user" />
          </el-form-item>

          <el-form-item v-if="formData.type == MenuTypeEnum.MENU" prop="component">
            <template #label>
              <div class="flex-y-center">
                组件路径
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    组件页面完整路径，相对于 src/views/，如 system/user/index，缺省后缀 .vue
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>

            <el-input v-model="formData.component_path" placeholder="system/user/index" style="width: 95%">
              <template v-if="formData.type == MenuTypeEnum.MENU" #prepend>src/views/</template>
              <template v-if="formData.type == MenuTypeEnum.MENU" #append>.vue</template>
            </el-input>
          </el-form-item>

          <el-form-item v-if="formData.type == MenuTypeEnum.MENU">
            <template #label>
              <div class="flex-y-center">
                路由参数
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    组件页面使用 `useRoute().query.参数名` 获取路由参数值。
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>

            <div v-if="!formData.params || formData.params.length === 0">
              <el-button type="success" plain @click="formData.params = [{ key: '', value: '' }]">
                添加路由参数
              </el-button>
            </div>

            <div v-else>
              <div v-for="(item, index) in formData.params" :key="index">
                <el-input v-model="item.key" placeholder="参数名" style="width: 100px" />

                <span class="mx-1">=</span>

                <el-input v-model="item.value" placeholder="参数值" style="width: 100px" />

                <el-icon v-if="formData.params.indexOf(item) === formData.params.length - 1"
                  class="ml-2 cursor-pointer color-[var(--el-color-success)]" style="vertical-align: -0.15em"
                  @click="formData.params.push({ key: '', value: '' })">
                  <CirclePlusFilled />
                </el-icon>
                <el-icon class="ml-2 cursor-pointer color-[var(--el-color-danger)]" style="vertical-align: -0.15em"
                  @click="formData.params.splice(formData.params.indexOf(item), 1)">
                  <DeleteFilled />
                </el-icon>
              </div>
            </div>
          </el-form-item>

          <el-form-item v-if="formData.type !== MenuTypeEnum.BUTTON" prop="hidden" label="显示状态">
            <el-radio-group v-model="formData.hidden">
              <el-radio :value="true">显示</el-radio>
              <el-radio :value="false">隐藏</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="formData.type === MenuTypeEnum.CATALOG || formData.type === MenuTypeEnum.MENU">
            <template #label>
              <div class="flex-y-center">
                始终显示
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    选择"是"，即使目录或菜单下只有一个子节点，也会显示父节点。
                    <br />
                    选择"否"，如果目录或菜单下只有一个子节点，则只显示该子节点，隐藏父节点。
                    <br />
                    如果是叶子节点，请选择"否"。
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>

            <el-radio-group v-model="formData.always_show">
              <el-radio :value="true">是</el-radio>
              <el-radio :value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="formData.type === MenuTypeEnum.MENU" label="缓存页面">
            <el-radio-group v-model="formData.keep_alive">
              <el-radio :value="true">开启</el-radio>
              <el-radio :value="false">关闭</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="排序" prop="order">
            <el-input-number v-model="formData.order" style="width: 100px" controls-position="right" :min="0" />
          </el-form-item>

          <!-- 权限标识 -->
          <el-form-item v-if="formData.type == MenuTypeEnum.BUTTON" label="权限标识" prop="perm">
            <el-input v-model="formData.permission" placeholder="sys:user:add" />
          </el-form-item>

          <el-form-item v-if="formData.type !== MenuTypeEnum.BUTTON" label="图标" prop="icon">
            <!-- 图标选择器 -->
            <icon-select v-model="formData.icon" />
          </el-form-item>

          <el-form-item v-if="formData.type == MenuTypeEnum.CATALOG" label="跳转路由">
            <el-input v-model="formData.redirect" placeholder="跳转路由" />
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">确定</el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
          <el-button @click="handleCloseDialog">取消</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "SysMenu",
  inheritAttrs: false,
});

import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";

import MenuAPI, { MenuPageQuery, MenuForm, MenuTable } from "@/api/system/menu";
import { MenuTypeEnum } from "@/enums/system/menu.enum";
import { listToTree } from "@/utils/common";

const appStore = useAppStore();

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);

const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<MenuTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: 'selection', label: '选择框', show: true },
  { prop: 'index', label: '序号', show: true },
  { prop: 'name', label: '标题', show: true },
  { prop: 'type', label: '类型', show: true },
  { prop: 'icon', label: '图标', show: true },
  { prop: 'order', label: '排序', show: true },
  { prop: 'permission', label: '权限标识', show: true },
  { prop: 'route_name', label: '路由名称', show: true },
  { prop: 'route_path', label: '路由路径', show: true },
  { prop: 'component_path', label: '组件路径', show: true },
  { prop: 'redirect', label: '跳转路由', show: true },
  { prop: 'parent_id', label: '父级菜单', show: true },
  { prop: 'parent_name', label: '父级菜单名称', show: true },
  { prop: 'keep_alive', label: '缓存页面', show: true },
  { prop: 'hidden', label: '显示状态', show: true },
  { prop: 'always_show', label: '始终显示', show: true },
  { prop: 'title', label: '菜单标题', show: true },
  { prop: 'params', label: '路由参数', show: true },
  { prop: 'affix', label: '固定路由', show: true },
  { prop: 'status', label: '状态', show: true },
  { prop: 'description', label: '描述', show: true },
  { prop: 'created_at', label: '创建时间', show: true },
  { prop: 'updated_at', label: '更新时间', show: true },
  { prop: 'operation', label: '操作', show: true }
])

// 详情表单
const detailFormData = ref<MenuTable>({});

// 分页查询参数
const queryFormData = reactive<MenuPageQuery>({
  page_no: 1,
  page_size: 10,
  name: undefined,
  status: undefined,
  start_time: undefined,
  end_time: undefined,
});

// 编辑表单
const formData = reactive<MenuForm>({
  id: undefined,
  name: undefined,
  type: MenuTypeEnum.MENU,
  icon: undefined,
  order: undefined,
  permission: '',
  route_name: '',
  route_path: '',
  component_path: '',
  redirect: '',
  parent_id: undefined,
  keep_alive: undefined,
  hidden: undefined,
  always_show: undefined,
  title: '',
  params: '',
  affix: false,
  status: true,
  description: undefined,
})

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: 'create' as 'create' | 'update' | 'detail',
});

const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "600px" : "90%"));

// 顶级菜单下拉选项
const menuOptions = ref<OptionType[]>([]);

// 表单验证规则
const rules = reactive({
  name: [{ required: true, message: "请输入菜单名称", trigger: "blur" }],
  parent_id: [{ required: true, message: "请选择父级菜单", trigger: "blur" }],
  type: [{ required: true, message: "请选择菜单类型", trigger: "blur" }],
  order: [{ required: true, message: "请输入排序", trigger: "blur" }],
  permission: [{ required: true, message: "请输入权限标识", trigger: "blur" }],
  route_name: [{ required: true, message: "请输入路由名称", trigger: "blur" }],
  route_path: [{ required: true, message: "请输入路由路径", trigger: "blur" }],
  component_path: [{ required: true, message: "请输入组件路径", trigger: "blur" }],
  title: [{ required: true, message: "请输入菜单标题", trigger: "blur" }],
  keep_alive: [{ required: true, message: "请选择是否缓存", trigger: "change" }],
  hidden: [{ required: true, message: "请选择是否隐藏", trigger: "change" }],
  always_show: [{ required: true, message: "请选择始终显示", trigger: "change" }],
  status: [{ required: true, message: "请选择状态", trigger: "change" }],
});

// 选择表格的行菜单ID
const selectedMenuId = ref<number | undefined>();

// 刷新数据(防抖)
const handleRefresh = useDebounceFn(() => {
  loadingData();
  ElMessage.success("刷新成功");
}, 1000);

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await MenuAPI.getMenuList(queryFormData);
    pageTableData.value = listToTree(response.data.data.items);
    total.value = response.data.data.total;
  }
  catch (error: any) {
    ElMessage.error(error.message);
  }
  finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  handleQuery();
}

// 重置表单
async function resetForm() {
  dataFormRef.value.resetFields();
  dataFormRef.value.clearValidate();
  formData.id = undefined;
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
}

// 行点击事件
async function handleRowClick(row: MenuTable) {
  selectedMenuId.value = row.id;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

//打开弹窗
async function handleOpenDialog(type: 'create' | 'update' | 'detail', id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await MenuAPI.getMenuDetail({ id });
    if (type === 'detail') {
      dialogVisible.title = "菜单详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === 'update') {
      dialogVisible.title = "修改菜单";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增菜单";
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

// 菜单类型切换
function handleMenuTypeChange() {
  // 如果菜单类型改变
  if (formData.type !== formData.type) {
    if (formData.type === MenuTypeEnum.MENU) {
      // 目录切换到菜单时，清空组件路径
      formData.component_path = "";
    }
  }
}

// 提交表单
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await MenuAPI.updateMenu(formData)
          dialogVisible.visible = false;
          resetForm();
          handleResetQuery();
        } catch (error: any) {
          ElMessage.error(error.message);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await MenuAPI.createMenu(formData)
          dialogVisible.visible = false;
          resetForm();
          handleResetQuery();
        } catch (error: any) {
          ElMessage.error(error.message);
        } finally {
          loading.value = false;
        }
      }
    }
  });
}

// 删除、导入、导出
async function handleOperation(type: 'delete' | 'import' | 'export', id?: number) {
  if (type === 'delete' && !id && !selectIds.value.length) {
    ElMessageBox.confirm("确认删除该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    }).then(async () => {
      try {
        loading.value = true;
        await MenuAPI.deleteMenu({ id: id ? id : selectIds.value });
        ElMessage.success("删除成功");
        handleResetQuery();
      } catch (error: any) {
        ElMessage.error(error.message);
      } finally {
        loading.value = false;
      }
    }).catch(() => {
      ElMessage.info('已取消删除');
    });
  }
  else if (type === 'import') {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx, .xls';
    input.click();

    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        try {
          loading.value = true;
          await MenuAPI.uploadFile(formData);
          ElMessage.success('导入成功');
          handleResetQuery();
        } catch (error: any) {
          ElMessage.error(error.message);
        } finally {
          loading.value = false;
        }
      }
    }
  }
  else if (type === 'export') {
    ElMessageBox.confirm('是否确认导出当前系统配置?', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      try {
        loading.value = true;
        const body = {
          ...queryFormData,
          page_no: 1,
          page_size: total.value
        };
        ElMessage.warning('正在导出数据，请稍候...');

        const response = await MenuAPI.exportMenu(body);
        const blob = new Blob([JSON.stringify(response.data)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8' });
        // 从响应头获取文件名
        const contentDisposition = response.headers['content-disposition'];
        let fileName = '系统配置.xlsx';
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
        ElMessage.success('导出成功');
      } catch (error: any) {
        ElMessage.error('文件处理失败', error.message);
        console.error('导出错误:', error);
      } finally {
        loading.value = false;
      }
    }).catch(() => {
      ElMessage.info('已取消导出');
    });
  }
  else {
    ElMessage.error('未知操作类型');
  }
}

onMounted(() => {
  handleQuery();
});
</script>
