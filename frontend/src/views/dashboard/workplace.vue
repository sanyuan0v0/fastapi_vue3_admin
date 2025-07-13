<template>
  <div class="app-container">
    <div>
      <ElCard shadow="hover">
        <div class="flex flex-wrap justify-between items-center">
          <div class="flex items-center  md:mb-0">
            <ElAvatar size="large" :src="currentUser.avatar" class="mr-20px" />
            <div>
              <div class="text-20px font-bold">
                {{ timefix }}{{ currentUser.name }}，{{ welcome }}
              </div>
              <el-text>
                {{ currentUser.username }} | {{ currentUser.dept_name }} | {{ currentUser.description }}
              </el-text>
            </div>
          </div>
          <!-- 最近登录时间 -->
          <div class="statItem text-14px text-gray-600 text-right">
            <el-text>最近登录时间</el-text>
            <div class="mt-5px text-20px">{{ currentUser.last_login }}</div>
          </div>
        </div>
      </ElCard>
    </div>

    <div class="mt-4">
      <ElRow :gutter="16" justify="space-between">
        <!-- 左侧：进行中的项目 + 动态 -->
        <ElCol :xl="16" :lg="16" :md="24" :sm="24" :xs="24">
          <!-- 进行中的项目 -->
          <ElCard shadow="hover" title="进行中的项目">
            <template #header>
              <span class="font-bold">进行中的项目</span>
              <ElLink href="" type="primary" underline="never" style="float: right">全部项目</ElLink>
            </template>
            <ElRow>
              <ElCol v-for="item in projectNotice" :key="`card-${item.id}`" :xl="8" :lg="8" :md="12" :sm="24" :xs="24">
                <ElCard :key="item.id" shadow="hover">
                  <ElDescriptions :column="1">
                    <ElDescriptionsItem>
                      <div class="flex items-center">
                        <ElAvatar :src="item.avatar" size="small" class="mr-20px" />
                        <ElLink :href="item.href" underline="never">{{ item.title }}</ElLink>
                      </div>
                    </ElDescriptionsItem>

                    <ElDescriptionsItem>
                      <el-tooltip placement="top" :content="item.description">
                        <el-text line-clamp=1 class="truncate-text">{{ item.description }}</el-text>
                      </el-tooltip>
                    </ElDescriptionsItem>

                    <ElDescriptionsItem>
                      <div class="flex justify-between items-center">
                        <ElLink :href="item.memberLink" underline="never">{{ item.member || "" }}</ElLink>
                        <span>{{ item.updatedAt }}</span>
                      </div>
                    </ElDescriptionsItem>
                  </ElDescriptions>
                </ElCard>
              </ElCol>
            </ElRow>
          </ElCard>
          <!-- 动态 -->
          <ElCard shadow="hover" title="动态" class="mt-4">
            <template #header>
              <span class="font-bold">动态</span>
              <ElLink href="" type="primary" underline="never" style="float: right">更多</ElLink>
            </template>
            <ElTimeline>
              <ElTimelineItem v-for="item in activities" :key="item.id">
                <div class="flex justify-between items-center">
                  <div class="flex items-center">
                    <ElAvatar :src="item.user.avatar" size="small" class="mr-20px">{{ item.user?.name }}</ElAvatar>
                    <span>{{ item.template1 }}</span>
                    <span>&nbsp;</span>
                    <ElLink :href="item.group?.link" type="primary" underline="never">{{ item?.group?.name }}</ElLink>
                    <span>&nbsp;</span>
                    <span>{{ item.template2 }}</span>
                    <span>&nbsp;</span>
                    <ElLink :href="item.project?.link" type="primary" underline="never">{{ item?.project?.name }}
                    </ElLink>
                  </div>
                  <span>{{ item.updatedAt }}</span>
                </div>
              </ElTimelineItem>
            </ElTimeline>
          </ElCard>
        </ElCol>

        <!-- 右侧：快速开始 / 便捷导航 + XX 指数 + 团队 -->
        <ElCol :xl="8" :lg="8" :md="12" :sm="12" :xs="24">
          <!-- 快速开始 / 便捷导航 -->
          <ElCard class="mb-4 font-bold">
            <template #header>
              <span class="font-bold">快速开始 / 便捷导航</span>
              <ElButton size="small" type="primary" plain style="float: right">
                <el-icon>
                  <Plus />
                </el-icon> {{ t('common.add') }}
              </ElButton>
            </template>
            <div class="linkGroup">
              <ElLink v-for="(item, index) in links" :key="index" underline="never" :href="item.href">
                {{ item.title }}
              </ElLink>
            </div>
          </ElCard>

          <!-- XX 指数 -->
          <ElCard class="mb-4 font-bold" header="XX 指数">
            <ECharts class="chart" :options="chartOptions" height="450px" autoresize :init-options="{ renderer: 'canvas' }" />
          </ElCard>

          <!-- 团队 -->
          <ElCard class="mb-4 font-bold" header="团队">
            <div class="members">
              <ElRow :gutter="48">
                <ElCol v-for="item in projectNotice" :key="`members-item-${item.id}`" :span="12">
                  <ElLink underline="never" :href="item.href">
                    <ElAvatar :src="item.avatar" size="small" />
                    <span class="member">{{ item.member }}</span>
                  </ElLink>
                </ElCol>
              </ElRow>
            </div>
          </ElCard>
        </ElCol>
      </ElRow>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Plus } from "@element-plus/icons-vue";
import { EChartsOption } from 'echarts'
import { useUserStore } from "@/store/index";
import { greetings } from '@/utils/common';

const { t } = useI18n();

const userStore = useUserStore();
const timefix = greetings();

defineOptions({
  name: "DashBoard",
});

const welcome = '祝你开心每一天！';

const currentUser = {
  avatar: userStore.basicInfo.avatar || "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
  name: userStore.basicInfo.name || "吴彦祖",
  username: userStore.basicInfo.username || "账号信息",
  description: userStore.basicInfo.description || "用户说明",
  dept_name: userStore.basicInfo.dept_name || "软件专业部",
  last_login: userStore.basicInfo.last_login || "2023-01-01 00:00:00",
};

const projectNotice = [
  {
    id: "xxx1",
    title: "Mysql",
    avatar: "https://labs.mysql.com/common/themes/sakila/favicon.ico",
    description: "最流行的关系型数据库",
    updatedAt: "几秒前",
    member: "科学搬砖组",
    href: "https://www.mysql.com/",
    memberLink: "",
  },
  {
    id: "xxx2",
    title: "Fastapi",
    avatar: "https://fastapi.tiangolo.com/img/favicon.png",
    description: "一个现代、快速(高性能)的 web 框架",
    updatedAt: "6 年前",
    member: "全组都是吴彦祖",
    href: "https://fastapi.tiangolo.com/zh/",
    memberLink: "",
  },
  {
    id: "xxx3",
    title: "Element-plus",
    avatar: "https://element-plus.org/images/element-plus-logo-small.svg",
    description: "面向设计师和开发者的组件库",
    updatedAt: "几秒前",
    member: "中二少女团",
    href: "https://element-plus.org/zh-CN/",
    memberLink: "",
  },
  {
    id: "xxx4",
    title: "Vue",
    avatar: "https://cn.vuejs.org/logo.svg",
    description: "渐进式 JavaScript 框架",
    updatedAt: "6 年前",
    member: "程序员日常",
    href: "https://cn.vuejs.org/",
    memberLink: "",
  },
  {
    id: "xxx5",
    title: "Vite",
    avatar: "https://vitejs.cn/vite3-cn/logo.svg",
    description: "Vite 下一代的前端工具链",
    updatedAt: "6 年前",
    member: "高逼格设计天团",
    href: "https://cn.vitejs.dev/",
    memberLink: "",
  },
  {
    id: "xxx6",
    title: "Python",
    avatar: "https://python.p2hp.com/static/favicon.ico",
    description: "一种解释型、面向对象类型编程语言",
    updatedAt: "6 年前",
    member: "骗你来学计算机",
    href: "",
    memberLink: "",
  },
];

const activities = [
  {
    id: "trend-1",
    updatedAt: "几秒前",
    user: {
      name: "曲丽丽",
      avatar:
        "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
    },
    group: {
      name: "高逼格设计天团",
      link: "http://github.com/",
    },
    project: {
      name: "六月迭代",
      link: "http://github.com/",
    },
    template1: "在",
    template2: "新建项目",
  },
  {
    id: "trend-2",
    updatedAt: "几分钟前",
    user: {
      name: "付小小",
      avatar:
        "https://gw.alipayobjects.com/zos/rmsportal/cnrhVkzwxjPwAaCfPbdc.png",
    },
    group: {
      name: "高逼格设计天团",
      link: "http://github.com/",
    },
    project: {
      name: "六月迭代",
      link: "http://github.com/",
    },
    template1: "在",
    template2: "新建项目",
  },
  {
    id: "trend-3",
    updatedAt: "10 分钟前",
    user: {
      name: "林东东",
      avatar:
        "https://gw.alipayobjects.com/zos/rmsportal/gaOngJwsRYRaVAuXXcmB.png",
    },
    group: {
      name: "中二少女团",
      link: "http://github.com/",
    },
    project: {
      name: "六月迭代",
      link: "http://github.com/",
    },
    template1: "在",
    template2: "新建项目",
  },
  {
    id: "trend-4",
    updatedAt: "1小时前",
    user: {
      name: "周星星",
      avatar:
        "https://gw.alipayobjects.com/zos/rmsportal/WhxKECPNujWoWEFNdnJE.png",
    },
    group: {
      name: "5 月日常迭代",
      link: "http://github.com/",
    },
    template1: "将",
    template2: "更新至已发布状态",
  },
  {
    id: "trend-5",
    updatedAt: "1周前",
    user: {
      name: "朱偏右",
      avatar:
        "https://gw.alipayobjects.com/zos/rmsportal/ubnKSIfAJTxIgXOKlciN.png",
    },
    group: {
      name: "工程效能",
      link: "http://github.com/",
    },
    project: {
      name: "留言",
      link: "http://github.com/",
    },
    template1: "在",
    template2: "发布了",
  },
  {
    id: "trend-6",
    updatedAt: "1个月前",
    user: {
      name: "乐哥",
      avatar:
        "https://gw.alipayobjects.com/zos/rmsportal/jZUIxmJycoymBprLOUbT.png",
    },
    group: {
      name: "程序员日常",
      link: "http://github.com/",
    },
    project: {
      name: "品牌迭代",
      link: "http://github.com/",
    },
    template1: "在",
    template2: "新建项目",
  },
];

const chartOptions = reactive<EChartsOption>({
  tooltip: { trigger: 'item' },
  legend: { data: ['个人', '团队', '部门'] },
  radar: {
    shape: 'circle',
    indicator: [
      { name: '引用', max: 10 },
      { name: '热度', max: 10 },
      { name: '贡献', max: 10 },
      { name: '产量', max: 10 },
      { name: '口碑', max: 10 }
    ]
  },
  series: [{
    name: 'Budget vs spending',
    type: 'radar',
    areaStyle: {},
    symbol: 'none',
    emphasis: { focus: 'self' },
    data: [
      { value: [10, 7, 5, 4, 8], name: '个人' },
      { value: [3, 1, 3, 6, 9], name: '团队' },
      { value: [4, 7, 5, 6, 1], name: '部门' }
    ]
  }]
});

const links = [
  {
    title: "操作一",
    href: "",
  },
  {
    title: "操作二",
    href: "",
  },
  {
    title: "操作三",
    href: "",
  },
  {
    title: "操作四",
    href: "",
  },
  {
    title: "操作五",
    href: "",
  },
  {
    title: "操作六",
    href: "",
  },
];

</script>

<style lang="scss" scoped>
.members {
  a {
    display: block;
    height: 24px;
    margin: 8px 0;
    transition: all 0.3s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    .member {
      margin-left: 8px;
      font-size: 14px;
      line-height: 24px;
      vertical-align: top;
    }

    &:hover {
      color: #1890ff;
    }
  }
}

.linkGroup {
  padding: 20px 0 8px 24px;
  font-size: 0;

  &>a {
    display: inline-block;
    width: 25%;
    margin-bottom: 13px;
    font-size: 14px;

    &:hover {
      color: #1890ff;
    }
  }
}
</style>
