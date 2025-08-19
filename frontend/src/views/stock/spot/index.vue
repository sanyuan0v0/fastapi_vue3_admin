<!-- 演示示例 -->
<template>
    <div class="app-container">
        <!-- 搜索区域 -->
        <div class="search-container">
            <el-form ref="queryFormRef" :model="queryFormData" :inline="true" label-suffix=":">
                <el-form-item prop="start_date" label="日期" :required="true">
                    <OnlyDatePicker
                        v-model="dateRange"
                        @update:model-value="handleDateRangeChange"
                    />
                </el-form-item>
                <el-form-item prop="name" label="名称">
                    <el-input v-model="queryFormData.name" placeholder="请输入名称" clearable />
                </el-form-item>
                <el-form-item prop="code" label="代码">
                    <el-input v-model="queryFormData.code" placeholder="请输入代码" clearable />
                </el-form-item>
                <!-- 查询、重置、展开/收起按钮 -->
                <el-form-item class="search-buttons">
                    <el-button type="primary" icon="search" @click="handleQuery">
                        查询
                    </el-button>
                    <el-button icon="refresh" @click="handleResetQuery">
                        重置
                    </el-button>
                </el-form-item>
            </el-form>
        </div>

        <!-- 内容区域 -->
        <el-card shadow="hover" class="data-table">
            <template #header>
                <div class="card-header">
                    <span>
                        <el-tooltip content="综合数据列表">
                            <QuestionFilled class="w-4 h-4 mx-1" />
                        </el-tooltip>
                        综合数据列表
                    </span>
                </div>
            </template>

            <!-- 功能区域 -->
            <div class="data-table__toolbar">
                <div class="data-table__toolbar--actions">
                </div>
                <div class="data-table__toolbar--tools">
                    <el-tooltip content="刷新">
                        <el-button type="primary" icon="refresh" circle @click="handleRefresh" />
                    </el-tooltip>
                    <el-tooltip content="列表筛选">
                        <el-dropdown trigger="click">
                            <el-button type="default" icon="operation" circle />
                            <template #dropdown>
                                <el-dropdown-menu style="height: 500px; overflow: auto;">
                                    <el-dropdown-item v-for="column in tableColumns" :key="column.prop"
                                        :command="column">
                                        <el-checkbox v-model="column.show">
                                            {{ column.label }}
                                        </el-checkbox>
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>
                    </el-tooltip>
                </div>
            </div>
            <!-- 表格区域：系统配置列表 -->
            <el-table ref="dataTableRef" v-loading="loading" :data="pageTableData" highlight-current-row
                class="data-table__content" height="450" border stripe @sort-change="handleSortChange"
>

                <template #empty>
                    <el-empty :image-size="80" description="暂无数据" />
                </template>

                <el-table-column 
                    v-for="column in activeTableColumns" 
                    :key="column.prop" 
                    :label="column.label" 
                    :prop="column.prop" 
                    :min-width="column.minWidth" 
                    :sortable="column.sortable" 
                    show-overflow-tooltip
                    >
                    <template #default="scope">
                        {{ formatField(scope.row[column.prop]) }}

                    </template>
                </el-table-column>
                <el-table-column fixed="right" label="操作" align="center" min-width="80">
                    <template #default="scope">
                        <el-button type="info" size="small" link icon="document"
                            @click="handleOpenDialog('detail', scope.row.date, scope.row.code)">详情</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页区域 -->
            <template #footer>
                <pagination v-model:total="total" v-model:page="queryFormData.page_no"
                    v-model:limit="queryFormData.page_size" @pagination="loadingData" />
            </template>
        </el-card>

        <!-- 弹窗区域 -->
        <el-dialog v-model="dialogVisible.visible" :title="dialogVisible.title" @close="handleCloseDialog">
            <!-- 详情 -->
            <el-tabs type="border-card" class="detail-tabs" >
            <el-tab-pane v-for="group in fieldGroups" :key="group" :label="group.name">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in group.fields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>
            </el-tabs>

            <template #footer>
                <div class="dialog-footer">
                    <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
                    <el-button @click="handleCloseDialog">取消</el-button>
                    <el-button v-if="dialogVisible.type !== 'detail'" type="primary"
                        @click="handleSubmit">确定</el-button>
                    <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
defineOptions({
    name: "Comprehensive",
    inheritAttrs: false,
});

import { ref, reactive, onMounted, computed } from "vue";
import { ResultEnum } from "@/enums/api/result.enum";
import SpotAPI, { SpotTable, SpotPageQuery } from "@/api/stock/spot";
import TradeTimeAPI, { TradeTimeTable } from "@/api/stock/tradeTime";
import OnlyDatePicker from "@/components/OnlyDatePicker/index.vue";
import { formatDate } from "@/utils/tools";


const emit = defineEmits(['import-success']);

const queryFormRef = ref();
const dataTableRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);


// 分页表单
const pageTableData = ref<SpotTable[]>([]);

// 表格列配置
const tableColumns = ref([
    { prop: 'date', label: '日期', show: true , minWidth: '100', sortable: false },
    { prop: 'code', label: '代码', show: true , minWidth: '100', sortable: false },
    { prop: 'name', label: '名称', show: true , minWidth: '100', sortable: false },
    { prop: 'new_price', label: '最新价', show: true , minWidth: '100', sortable: false },
    { prop: 'change_rate', label: '涨跌幅', show: true , minWidth: '100', sortable: "custom" },
    { prop: 'ups_downs', label: '涨跌额', show: true , minWidth: '100', sortable: "custom" },
    { prop: 'volume', label: '成交量', show: true , minWidth: '100', sortable: "custom" },
    { prop: 'deal_amount', label: '成交额', show: true , minWidth: '130', sortable: "custom" },
    { prop: 'amplitude', label: '振幅', show: true , minWidth: '130', sortable: "custom" },
    { prop: 'turnoverrate', label: '换手率', show: true , minWidth: '100', sortable: "custom" },
    { prop: 'volume_ratio', label: '量比', show: true , minWidth: '100', sortable: "custom" },
    { prop: 'open_price', label: '今开价', show: true , minWidth: '100', sortable: false },
    { prop: 'high_price', label: '最高价', show: true , minWidth: '100', sortable: false },
    { prop: 'low_price', label: '最低价', show: true , minWidth: '100', sortable: false },
    { prop: 'pre_close_price', label: '昨收价', show: true , minWidth: '100', sortable: false },
    { prop: 'speed_increase', label: '涨速', show: true , minWidth: '100', sortable: false },
    { prop: 'industry', label: '行业', show: true , minWidth: '100', sortable: false },
    { prop: 'listing_date', label: '上市时间', show: true , minWidth: '100', sortable: false },
])
const activeTableColumns = computed(() => {
    return tableColumns.value.filter(item => item.show);
});

// 详情表单
const detailFormData = ref<SpotTable>({});

// 交易日历
const tradeTimeTableData = ref<TradeTimeTable>({});

// 日期范围临时变量
const dateRange = ref<[Date, Date] | []>([]);

// 处理日期范围变化
function handleDateRangeChange(range: [Date, Date]) {
    dateRange.value = range;
    if (range && range.length === 2) {
        queryFormData.start_date = formatDate(range[0]);
        queryFormData.end_date = formatDate(range[1]);
    } else {
        queryFormData.start_date = undefined;
        queryFormData.end_date = undefined;
    }
}

// 分页查询参数
const queryFormData = reactive<SpotPageQuery>({
    page_no: 1,
    page_size: 10,
    name: undefined,
    code: undefined,
    start_date: formatDate(new Date()),
    end_date: formatDate(new Date()),
    order_by: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
    title: "",
    visible: false,
    type: 'create' as 'create' | 'update' | 'detail',
});

// 列表刷新
async function handleRefresh() {
    await loadingData();
};


// 获取交易日历
async function getTradeTime() {
    try {
        const response = await TradeTimeAPI.getTradeTime("last");
        tradeTimeTableData.value = response.data.data;
        // console.log(tradeTimeTableData.value);
        // console.log('trade_time交易日历数据:', tradeTimeTableData.value.trade_time);
        dateRange.value = [tradeTimeTableData.value.trade_time, tradeTimeTableData.value.trade_time];
        queryFormData.start_date = tradeTimeTableData.value.trade_time;
        queryFormData.end_date = tradeTimeTableData.value.trade_time;
        // console.log('dateRange.value', dateRange.value);
    }
    catch (error: any) {
        console.error(error);
    }
}

// 加载表格数据
async function loadingData() {
    loading.value = true;
    try {
        const response = await SpotAPI.getSpotList(queryFormData);
        pageTableData.value = response.data.data.items;
        total.value = response.data.data.total;
    }
    catch (error: any) {
        console.error(error);
    }
    finally {
        loading.value = false;
    }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
    dataTableRef.value.clearSort()
    queryFormData.page_no = 1;
    queryFormData.order_by = undefined
    loadingData();
}

// 重置查询
async function handleResetQuery() {
    queryFormRef.value.resetFields();
    dataTableRef.value.clearSort()
    queryFormData.page_no = 1;
    // 重置日期范围选择器
    await getTradeTime()
    queryFormData.order_by = undefined;
    loadingData();
}

interface ElementSortParam {
  prop: string;
  order: 'ascending' | 'descending' | null;
};

type TargetSortParam = Array<Record<string, 'asc' | 'desc'>>;


// 当前排序状态
const currentSorts = ref<ElementSortParam[]>([]);

// 转换函数
const convertSortParams = (sortParams: ElementSortParam[]): TargetSortParam => {
    return sortParams
        .filter(param => param.order !== null)
        .map(param => ({
        [param.prop]: param.order === 'ascending' ? 'asc' : 'desc'
        }));
};

// 处理表格排序变化
const handleSortChange = ({column, prop, order }: {column, prop: string; order: 'ascending' | 'descending' | null }) => {
    currentSorts.value = [{prop, order}]
    const targetSorts = convertSortParams(currentSorts.value);
    // console.log('转换后的排序参数:', JSON.stringify(targetSorts));
    // 更新查询参数
    queryFormData.page_no = 1; // 重置页码
    queryFormData.order_by =  targetSorts.length > 0 ? JSON.stringify(targetSorts) : undefined;
    // console.log('转换后的排序参数:', queryFormData.order_by);
    // 重新加载数据
    loadingData();
};


// 关闭弹窗
async function handleCloseDialog() {
    dialogVisible.visible = false;
}

// 打开弹窗
async function handleOpenDialog(type: 'create' | 'update' | 'detail', date?: string, code?: string) {
    dialogVisible.type = type;
    if (date && code) {
        const response = await SpotAPI.getSpotDetail(date, code);
        if (type === 'detail') {
            dialogVisible.title = "详情";
            Object.assign(detailFormData.value, response.data.data);
        }
    }
    dialogVisible.visible = true;
}

// 精简后的字段分组配置 (41个字段，大核心分组)
interface GroupParams {
    name: string,
    fields: string[],
};

const fieldGroups : GroupParams[] = [
  {
    name: '基础信息与行情',
    fields: [
      'code', 'name', 'industry', 'listing_date',  // 基础标识
      'date', 'new_price', 'open_price', 'high_price', 'low_price', // 行情数据
      'pre_close_price', 'change_rate', 'ups_downs', 'speed_increase'  // 涨跌指标
    ]
  },
  {
    name: '量能与市场表现',
    fields: [
      'volume', 'deal_amount', 'turnoverrate', 'volume_ratio', // 量能指标
      'amplitude', 'speed_increase_5', 'speed_increase_60', // 波动表现
      'speed_increase_all', 'report_date', // 周期表现
      'total_market_cap', 'free_cap' // 市值数据
    ]
  },
  {
    name: '财务与估值',
    fields: [
      'dtsyl', 'pe9', 'pe', 'pbnewmrq', // 估值指标
      'basic_eps', 'bvps', 'per_capital_reserve', 'per_unassign_profit', // 每股指标
      'roe_weight', 'sale_gpr', 'debt_asset_ratio' // 财务健康度
    ]
  },
  {
    name: '经营与股本',
    fields: [
      'total_operate_income', 'toi_yoy_ratio', // 营收数据
      'parent_netprofit', 'netprofit_yoy_ratio', // 利润数据
      'total_shares', 'free_shares' // 股本结构
    ]
  }
];

// 完整的字段标签映射（41个）
const fieldLabels = {
    date: '日期',
    code: '代码',
    name: '名称',
    new_price: '最新价',
    change_rate: '涨跌幅',
    ups_downs: '涨跌额',
    volume: '成交量',
    deal_amount: '成交额',
    amplitude: '振幅',
    turnoverrate: '换手率',
    volume_ratio: '量比',
    open_price: '今开',
    high_price: '最高',
    low_price: '最低',
    pre_close_price: '昨收',
    speed_increase: '涨速',
    speed_increase_5: '5分钟涨跌',
    speed_increase_60: '60日涨跌幅',
    speed_increase_all: '年初至今涨跌幅',
    dtsyl: '市盈率动',
    pe9: '市盈率TTM',
    pe: '市盈率静',
    pbnewmrq: '市净率',
    basic_eps: '每股收益',
    bvps: '每股净资产',
    per_capital_reserve: '每股公积金',
    per_unassign_profit: '每股未分配利润',
    roe_weight: '加权净资产收益率',
    sale_gpr: '毛利率',
    debt_asset_ratio: '资产负债率',
    total_operate_income: '营业收入',
    toi_yoy_ratio: '营业收入同比增长',
    parent_netprofit: '归属净利润',
    netprofit_yoy_ratio: '归属净利润同比增长',
    report_date: '报告期',
    total_shares: '总股本',
    free_shares: '已流通股份',
    total_market_cap: '总市值',
    free_cap: '流通市值',
    industry: '行业',
    listing_date: '上市时间'
};

// 检查字段是否有有效值
const hasValue = (value: any) => {
    return value !== undefined && value !== null && value !== '';
};

// 智能格式化字段值
const formatField = (value: any) => {
    if (!hasValue(value)) return '-';

    // 布尔值处理
    if (typeof value === 'boolean') return value ? '是' : '否';
    // 千分位处理
    if (typeof value === 'number') {
        return value.toLocaleString();
    }
    return value;
};

onMounted(async () => {
    await getTradeTime();
    loadingData();
});
</script>

<style lang="scss" scoped></style>
