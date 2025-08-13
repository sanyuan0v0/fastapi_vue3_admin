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
            <!-- 1. 基础信息 -->
            <el-tab-pane label="基础信息">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in basicInfoFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>

            <!-- 2. 市场数据 -->
            <el-tab-pane label="市场数据">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in marketDataFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>

            <!-- 3. 财务指标 -->
            <el-tab-pane label="财务指标">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in financialFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>

            <!-- 4. 估值指标 -->
            <el-tab-pane label="估值指标">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in valuationFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>

            <!-- 5. 成长能力 -->
            <el-tab-pane label="成长能力">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in growthFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>

            <!-- 6. 盈利能力 -->
            <el-tab-pane label="盈利能力">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in profitabilityFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>

            <!-- 7. 技术指标 -->
            <el-tab-pane label="技术指标">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in technicalFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>

            <!-- 8. 资金流向 -->
            <el-tab-pane label="资金流向">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in capitalFlowFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>

            <!-- 9. 股东机构 -->
            <el-tab-pane label="股东机构">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in shareholderFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
                    </el-descriptions-item>
                </template>
                </el-descriptions>
            </el-tab-pane>

            <!-- 10. 市场表现 -->
            <el-tab-pane label="市场表现">
                <el-descriptions :column="2" border class="detail-descriptions">
                <template v-for="field in marketPerformanceFields" :key="field">
                    <el-descriptions-item 
                    :label="fieldLabels[field]"
                    >
                    {{ formatField(field, detailFormData[field]) }}
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
import { ElMessage, TableColumnCtx} from "element-plus";
import { ResultEnum } from "@/enums/api/result.enum";
import ComprehensiveAPI, { ComprehensiveTable, ComprehensivePageQuery } from "@/api/stock/comprehensive";
import OnlyDatePicker from "@/components/OnlyDatePicker/index.vue";
import { formatDate, addDays } from "@/utils/tools";


const emit = defineEmits(['import-success']);

const queryFormRef = ref();
const dataTableRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);


// 分页表单
const pageTableData = ref<ComprehensiveTable[]>([]);

// 表格列配置
const tableColumns = ref([
    { prop: 'date', label: '日期', show: true , minWidth: '100', sortable: false },
    { prop: 'code', label: '代码', show: true , minWidth: '100', sortable: false },
    { prop: 'name', label: '名称', show: true , minWidth: '100', sortable: false },
    { prop: 'new_price', label: '最新价', show: true , minWidth: '100', sortable: false },
    { prop: 'change_rate', label: '涨跌幅', show: true , minWidth: '100', sortable: "custom" },
    { prop: 'volume_ratio', label: '量比', show: true , minWidth: '100', sortable: "custom" },
    { prop: 'high_price', label: '最高价', show: true , minWidth: '100', sortable: false },
    { prop: 'low_price', label: '最低价', show: true , minWidth: '100', sortable: false },
    { prop: 'pre_close_price', label: '昨收价', show: true , minWidth: '100', sortable: false },
    { prop: 'volume', label: '成交量', show: true , minWidth: '100', sortable: "custom" },
    { prop: 'deal_amount', label: '成交额', show: true , minWidth: '130', sortable: "custom" },
    { prop: 'turnoverrate', label: '换手率', show: true , minWidth: '100', sortable: "custom" },
    { prop: 'listing_date', label: '上市时间', show: true , minWidth: '100', sortable: false },
    { prop: 'industry', label: '行业', show: true , minWidth: '100', sortable: false },
    { prop: 'area', label: '地区', show: true , minWidth: '100', sortable: false },
    { prop: 'concept', label: '概念', show: true , minWidth: '200', sortable: false },
    { prop: 'style', label: '板块', show: true , minWidth: '200', sortable: false },
])
const activeTableColumns = computed(() => {
    return tableColumns.value.filter(item => item.show);
});

// 详情表单
const detailFormData = ref<ComprehensiveTable>({});

// 日期范围临时变量
const defaultDate = addDays(new Date(), -1);
const dateRange = ref<[Date, Date] | []>([defaultDate, defaultDate]);


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
const queryFormData = reactive<ComprehensivePageQuery>({
    page_no: 1,
    page_size: 10,
    name: undefined,
    code: undefined,
    start_date: formatDate(defaultDate), // 默认查询昨天数据
    end_date: formatDate(defaultDate), // 默认查询昨天的数据
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

// 加载表格数据
async function loadingData() {
    loading.value = true;
    try {
        const response = await ComprehensiveAPI.getComprehensiveList(queryFormData);
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
    queryFormData.page_no = 1;
    queryFormData.order_by = undefined
    loadingData();
}

// 重置查询
async function handleResetQuery() {
    const resetDate = addDays(new Date(), -1);
    queryFormRef.value.resetFields();
    dataTableRef.value.clearSort()
    queryFormData.page_no = 1;
    // 重置日期范围选择器
    dateRange.value = [resetDate, resetDate];
    queryFormData.start_date = formatDate(resetDate); // 默认查询昨天数据
    queryFormData.end_date = formatDate(resetDate); // 默认查询昨天的数据
    queryFormData.order_by = undefined;
    loadingData();
}

interface ElementSortParam {
  prop: string;
  order: 'ascending' | 'descending' | null;
}

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
        const response = await ComprehensiveAPI.getComprehensiveDetail(date, code);
        if (type === 'detail') {
            dialogVisible.title = "详情";
            Object.assign(detailFormData.value, response.data.data);
        }
    }
    dialogVisible.visible = true;
}

// 完整的字段分组配置（206个字段）
const basicInfoFields = [
    'date', 'code', 'name', 'industry', 'area', 'concept', 'style',
    'listing_date', 'is_hs300', 'is_sz50', 'is_zz500', 'is_zz1000',
    'is_cy50', 'secucode'
];

const marketDataFields = [
    'new_price', 'change_rate', 'volume_ratio', 'high_price', 'low_price',
    'pre_close_price', 'volume', 'deal_amount', 'turnoverrate', 'amplitude',
    'upnday', 'downnday'
];

const financialFields = [
    'total_market_cap', 'free_cap', 'parent_netprofit', 'deduct_netprofit',
    'total_operate_income', 'basic_eps', 'bvps', 'per_netcash_operate',
    'per_fcfe', 'per_capital_reserve', 'per_unassign_profit',
    'per_surplus_reserve', 'per_retained_earning'
];

const valuationFields = [
    'pe9', 'pbnewmrq', 'pettmdeducted', 'ps9', 'pcfjyxjl9', 'dtsyl', 'ycpeg',
    'enterprise_value_multiple', 'predict_pe_syear', 'predict_pe_nyear'
];

const growthFields = [
    'netprofit_yoy_ratio', 'deduct_netprofit_growthrate', 'toi_yoy_ratio',
    'netprofit_growthrate_3y', 'income_growthrate_3y', 'predict_netprofit_ratio',
    'predict_income_ratio', 'basiceps_yoy_ratio', 'total_profit_growthrate',
    'operate_profit_growthrate'
];

const profitabilityFields = [
    'roe_weight', 'jroa', 'roic', 'sale_gpr', 'sale_npr', 'zxgxl'
];

const technicalFields = [
    'macd_golden_fork', 'macd_golden_forkz', 'macd_golden_forky',
    'kdj_golden_fork', 'kdj_golden_forkz', 'kdj_golden_forky',
    'break_through', 'low_funds_inflow', 'high_funds_outflow',
    'breakup_ma_5days', 'breakup_ma_10days', 'breakup_ma_20days',
    'breakup_ma_30days', 'breakup_ma_60days', 'long_avg_array',
    'short_avg_array', 'upper_large_volume', 'down_narrow_volume',
    'one_dayang_line', 'two_dayang_lines', 'rise_sun', 'power_fulgun',
    'restore_justice', 'down_7days', 'upper_8days', 'upper_9days',
    'upper_4days', 'heaven_rule', 'upside_volume', 'bearish_engulfing',
    'reversing_hammer', 'shooting_star', 'evening_star', 'first_dawn',
    'pregnant', 'black_cloud_tops', 'morning_star', 'narrow_finish'
];

const capitalFlowFields = [
    'net_inflow', 'netinflow_3days', 'netinflow_5days', 'nowinterst_ratio',
    'nowinterst_ratio_3d', 'nowinterst_ratio_5d', 'ddx', 'ddx_3d', 'ddx_5d',
    'ddx_red_10d', 'mutual_netbuy_amt', 'hold_ratio'
];

const shareholderFields = [
    'total_shares', 'free_shares', 'holder_newest', 'holder_ratio',
    'hold_amount', 'avg_hold_num', 'holdnum_growthrate_3q',
    'holdnum_growthrate_hy', 'hold_ratio_count', 'free_hold_ratio',
    'allcorp_num', 'allcorp_fund_num', 'allcorp_qs_num', 'allcorp_qfii_num',
    'allcorp_bx_num', 'allcorp_sb_num', 'allcorp_xt_num', 'allcorp_ratio',
    'allcorp_fund_ratio', 'allcorp_qs_ratio', 'allcorp_qfii_ratio',
    'allcorp_bx_ratio', 'allcorp_sb_ratio', 'allcorp_xt_ratio'
];

const marketPerformanceFields = [
    'changerate_3days', 'changerate_5days', 'changerate_10days',
    'changerate_ty', 'is_issue_break', 'is_bps_break', 'now_newhigh',
    'now_newlow', 'high_recent_3days', 'high_recent_5days',
    'high_recent_10days', 'high_recent_20days', 'high_recent_30days',
    'low_recent_3days', 'low_recent_5days', 'low_recent_10days',
    'low_recent_20days', 'low_recent_30days', 'win_market_3days',
    'win_market_5days', 'win_market_10days', 'win_market_20days',
    'win_market_30days', 'listing_yield_year', 'listing_volatility_year',
    'popularity_rank', 'rank_change', 'upp_days', 'down_days',
    'new_high', 'new_down', 'newfans_ratio', 'bigfans_ratio',
    'concern_rank_7days', 'browse_rank'
];

// 完整的字段标签映射（206个）
const fieldLabels = {
    date: '日期',
    code: '代码',
    name: '名称',
    industry: '行业',
    area: '地区',
    concept: '概念',
    style: '板块',
    listing_date: '上市时间',
    is_hs300: '沪深300',
    is_sz50: '上证50',
    is_zz500: '中证500',
    is_zz1000: '中证1000',
    is_cy50: '创业板50',
    secucode: '证券全代码',
    new_price: '最新价',
    change_rate: '涨跌幅',
    volume_ratio: '量比',
    high_price: '最高价',
    low_price: '最低价',
    pre_close_price: '昨收价',
    volume: '成交量',
    deal_amount: '成交额',
    turnoverrate: '换手率',
    amplitude: '振幅',
    upnday: '连涨天数',
    downnday: '连跌天数',
    total_market_cap: '总市值',
    free_cap: '流通市值',
    parent_netprofit: '归属净利润',
    deduct_netprofit: '扣非净利润',
    total_operate_income: '营业总收入',
    basic_eps: '每股收益',
    bvps: '每股净资产',
    per_netcash_operate: '每股经营现金流',
    per_fcfe: '每股自由现金流',
    per_capital_reserve: '每股资本公积',
    per_unassign_profit: '每股未分配利润',
    per_surplus_reserve: '每股盈余公积',
    per_retained_earning: '每股留存收益',
    pe9: '市盈率(TTM)',
    pbnewmrq: '市净率(MRQ)',
    pettmdeducted: '市盈率扣非(TTM)',
    ps9: '市销率(TTM)',
    pcfjyxjl9: '市现率(TTM)',
    dtsyl: '动态市盈率',
    ycpeg: '预测PEG',
    enterprise_value_multiple: '企业价值倍数',
    predict_pe_syear: '预测市盈率(今年)',
    predict_pe_nyear: '预测市盈率(明年)',
    netprofit_yoy_ratio: '净利润同比增长',
    deduct_netprofit_growthrate: '扣非净利润增长',
    toi_yoy_ratio: '营收同比增长',
    netprofit_growthrate_3y: '净利润3年复合增长',
    income_growthrate_3y: '营收3年复合增长',
    predict_netprofit_ratio: '预测净利润增长',
    predict_income_ratio: '预测营收增长',
    basiceps_yoy_ratio: '每股收益增长',
    total_profit_growthrate: '利润总额增长',
    operate_profit_growthrate: '营业利润增长',
    roe_weight: '净资产收益率(ROE)',
    jroa: '总资产净利率(ROA)',
    roic: '投入资本回报率(ROIC)',
    sale_gpr: '毛利率',
    sale_npr: '净利率',
    zxgxl: '最新股息率',
    macd_golden_fork: 'MACD金叉(日)',
    macd_golden_forkz: 'MACD金叉(周)',
    macd_golden_forky: 'MACD金叉(月)',
    kdj_golden_fork: 'KDJ金叉(日)',
    kdj_golden_forkz: 'KDJ金叉(周)',
    kdj_golden_forky: 'KDJ金叉(月)',
    break_through: '放量突破',
    low_funds_inflow: '低位资金流入',
    high_funds_outflow: '高位资金流出',
    breakup_ma_5days: '突破5日均线',
    breakup_ma_10days: '突破10日均线',
    breakup_ma_20days: '突破20日均线',
    breakup_ma_30days: '突破30日均线',
    breakup_ma_60days: '突破60日均线',
    long_avg_array: '均线多头排列',
    short_avg_array: '均线空头排列',
    upper_large_volume: '连涨放量',
    down_narrow_volume: '下跌无量',
    one_dayang_line: '单日大阳线',
    two_dayang_lines: '双日大阳线',
    rise_sun: '旭日东升',
    power_fulgun: '强势多方炮',
    restore_justice: '拨云见日',
    down_7days: '七连阴',
    upper_8days: '八连阳',
    upper_9days: '九连阳',
    upper_4days: '四连阳',
    heaven_rule: '天量法则',
    upside_volume: '放量上攻',
    bearish_engulfing: '穿头破脚',
    reversing_hammer: '倒转锤头',
    shooting_star: '射击之星',
    evening_star: '黄昏之星',
    first_dawn: '曙光初现',
    pregnant: '身怀六甲',
    black_cloud_tops: '乌云盖顶',
    morning_star: '早晨之星',
    narrow_finish: '窄幅整理',
    net_inflow: '当日净流入',
    netinflow_3days: '3日净流入',
    netinflow_5days: '5日净流入',
    nowinterst_ratio: '当日增仓比',
    nowinterst_ratio_3d: '3日增仓比',
    nowinterst_ratio_5d: '5日增仓比',
    ddx: '当日DDX',
    ddx_3d: '3日DDX',
    ddx_5d: '5日DDX',
    ddx_red_10d: '10日DDX飘红',
    mutual_netbuy_amt: '沪深股通净买额',
    hold_ratio: '沪深股通持股比',
    total_shares: '总股本',
    free_shares: '流通股本',
    holder_newest: '股东户数',
    holder_ratio: '股东户数变化',
    hold_amount: '户均持股市值',
    avg_hold_num: '户均持股数',
    holdnum_growthrate_3q: '户均持股季度增长',
    holdnum_growthrate_hy: '户均持股半年增长',
    hold_ratio_count: '十大股东持股比',
    free_hold_ratio: '十大流通股东持股比',
    allcorp_num: '机构持股家数',
    allcorp_fund_num: '基金持股家数',
    allcorp_qs_num: '券商持股家数',
    allcorp_qfii_num: 'QFII持股家数',
    allcorp_bx_num: '保险持股家数',
    allcorp_sb_num: '社保持股家数',
    allcorp_xt_num: '信托持股家数',
    allcorp_ratio: '机构持股比例',
    allcorp_fund_ratio: '基金持股比例',
    allcorp_qs_ratio: '券商持股比例',
    allcorp_qfii_ratio: 'QFII持股比例',
    allcorp_bx_ratio: '保险持股比例',
    allcorp_sb_ratio: '社保持股比例',
    allcorp_xt_ratio: '信托持股比例',
    changerate_3days: '3日涨跌幅',
    changerate_5days: '5日涨跌幅',
    changerate_10days: '10日涨跌幅',
    changerate_ty: '今年以来涨跌幅',
    is_issue_break: '是否破发',
    is_bps_break: '是否破净',
    now_newhigh: '今日创新高',
    now_newlow: '今日创新低',
    high_recent_3days: '近3日创新高',
    high_recent_5days: '近5日创新高',
    high_recent_10days: '近10日创新高',
    high_recent_20days: '近20日创新高',
    high_recent_30days: '近30日创新高',
    low_recent_3days: '近3日创新低',
    low_recent_5days: '近5日创新低',
    low_recent_10days: '近10日创新低',
    low_recent_20days: '近20日创新低',
    low_recent_30days: '近30日创新低',
    win_market_3days: '近3日跑赢大盘',
    win_market_5days: '近5日跑赢大盘',
    win_market_10days: '近10日跑赢大盘',
    win_market_20days: '近20日跑赢大盘',
    win_market_30days: '近30日跑赢大盘',
    listing_yield_year: '上市年化收益',
    listing_volatility_year: '上市年化波动',
    popularity_rank: '股吧人气排名',
    rank_change: '排名变化',
    upp_days: '排名连涨天数',
    down_days: '排名连跌天数',
    new_high: '排名新高',
    new_down: '排名新低',
    newfans_ratio: '新粉丝占比',
    bigfans_ratio: '铁粉占比',
    concern_rank_7days: '7日关注排名',
    browse_rank: '浏览排名'
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

onMounted(() => {
    loadingData();
});
</script>

<style lang="scss" scoped></style>
