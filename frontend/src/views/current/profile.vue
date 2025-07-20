<template>
  <div class="app-container">
    <el-row :gutter="12">
      <!-- 左侧信息卡片 -->
      <el-col :span="6" class="mb-4">
        <el-card :loading="loading" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
            </div>
          </template>
          <div class="user-info-header">
            <div class="avatar-wrapper">
              <el-avatar v-if="infoFormState.avatar" :src="infoFormState.avatar" :size="120" />
              <el-avatar v-else :size="120">
                <template #icon>
                  <User />
                </template>
              </el-avatar>
              <el-button type="info" class="avatar-edit-btn" circle icon="Camera" size="small" @click="handleUpload" />
              <div class="avatar-upload-overlay">
                <el-upload v-model:file-list="fileList" name="avatar" list-type="picture-card" :show-upload-list="false" :before-upload="beforeUpload" :custom-request="handleUploadCustomRequest">
                  <div>
                    <!-- <loading-outlined v-if="loading"></loading-outlined>
                    <plus-outlined v-else></plus-outlined> -->
                    <div style="margin-top: 8px">上传头像</div>
                  </div>
                </el-upload>
              </div>
            </div>
            <span class="user-name">
              {{ infoFormState.name }}
              <el-button type="primary" link :loading="infoSubmitting" icon="edit" @click="handleOpenDialog(DialogType.ACCOUNT)" />
            </span>

            <el-text>{{infoFormState.roles.map(item => item.name).join('、')}}</el-text>
          </div>

          <el-divider />

          <el-descriptions :column="1" size="small" class="user-details">

            <el-descriptions-item>
              <template #label>
                <el-icon style="vertical-align: middle;">
                  <User />
                </el-icon>
                <span style="vertical-align: middle;">账号</span>
              </template>
              <span style="vertical-align: middle;">{{ infoFormState.username }}</span>
            </el-descriptions-item>

            <el-descriptions-item>
              <template #label>
                <el-icon style="vertical-align: middle;">
                  <Coordinate />
                </el-icon>
                <span style="vertical-align: middle;">部门</span>
              </template>
              <span style="vertical-align: middle;">{{ infoFormState.dept_name }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <el-icon style="vertical-align: middle;">
                  <OfficeBuilding />
                </el-icon>
                <span style="vertical-align: middle;">岗位</span>
              </template>
              <span style="vertical-align: middle;">{{infoFormState.positions.map(item => item.name).join('、')}}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <el-icon style="vertical-align: middle;">
                  <Phone />
                </el-icon>
                <span style="vertical-align: middle;">手机</span>
              </template>
              <span style="vertical-align: middle;">{{ infoFormState.mobile }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <el-icon style="vertical-align: middle;">
                  <Message />
                </el-icon>
                <span style="vertical-align: middle;">邮箱</span>
              </template>
              <span style="vertical-align: middle;">{{ infoFormState.email }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <el-icon style="vertical-align: middle;">
                  <Clock />
                </el-icon>
                <span style="vertical-align: middle;">加入时间</span>
              </template>
              <span style="vertical-align: middle;">{{ infoFormState.created_at }}</span>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <!-- 右侧设置区域 -->
      <el-col :span="18" class="mb-4">
        <el-card :loading="loading" shadow="hover">
          <el-tabs type="border-card">
            <el-tab-pane>
              <template #label>
                <el-icon>
                  <User />
                </el-icon>
                <span>基本设置</span>
              </template>
              <div>
                <el-form ref="ruleFormRef" :model="infoFormState" :rules="rules" label-width="auto" :inline="true">
                  
                  <el-form-item label="姓名" name="name">
                    <el-input v-model:value="infoFormState.name" placeholder="请输入姓名" allow-clear>
                      <template #prefix>
                        <User />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="手机号" name="mobile">
                    <el-input v-model:value="infoFormState.mobile" placeholder="请输入手机号码" allow-clear>
                      <template #prefix>
                        <Phone />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="邮箱" name="email">
                    <el-input v-model:value="infoFormState.email" placeholder="请输入邮箱" allow-clear>
                      <template #prefix>
                        <Message />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="性别" name="gender">
                    <el-radio-group v-model:value="infoFormState.gender">
                      <el-radio v-for="item in DictDataStore['sys_user_sex']" :key="item.dict_value" :value="item.dict_value" >
                        {{ item.dict_label }}
                      </el-radio>
                    </el-radio-group>
                  </el-form-item>

                  <el-form-item>
                    <el-button type="primary" :loading="infoSubmitting" icon="edit">保存更改</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>

            <el-tab-pane>
              <template #label>
                <el-icon>
                  <Lock />
                </el-icon>
                <span>安全设置</span>
              </template>
              <div>
                <el-form ref="ruleFormRef" :model="passwordFormState" :rules="resetPasswordRules" label-width="auto">
                  <el-form-item label="当前密码" name="oldPassword">
                    <el-input v-model.trim="passwordFormState.oldPassword" :placeholder="t('login.password')" type="password" show-password clearable>
                      <template #prefix>
                        <Lock />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="新密码" name="newPassword">
                    <el-input v-model.trim="passwordFormState.newPassword" type="password" :placeholder="t('login.newPassword')" show-password clearable>
                      <template #prefix>
                        <Key />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="确认新密码" name="confirmPassword">
                    <el-input v-model.trim="passwordFormState.confirmPassword" type="password" :placeholder="t('login.message.password.confirm')" show-password clearable>
                      <template #prefix>
                        <Check />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item>
                    <el-button type="primary" :loading="passwordChanging" icon="edit">更新密码</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
import type { FormInstance } from 'element-plus'
import UserAPI, { type InfoFormState, type PasswordFormState } from '@/api/system/user';
import { useUserStore, useDictStore } from "@/store";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const userStore = useUserStore();
const dictStore = useDictStore();
const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);

const DictDataStore = computed(() => {
  return dictStore.dictData;
});

// 字典数据
const getOptions = async () => {
  const dictOptions = await dictStore.getDict(['sys_user_sex']);
  return dictOptions;
};

// 状态定义
const passwordChanging = ref(false);
const infoSubmitting = ref(false);

// 用户基础信息表单
const infoFormState = reactive<InfoFormState>({
  name: '',
  gender: 1,
  mobile: '',
  email: '',
  username: '',
  dept_name: '',
  positions: [],
  roles: [],
  avatar: '',
  created_at: ''
});

// 修改密码表单
const passwordFormState = reactive<PasswordFormState>({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
});

// 头像上传处理优化
const fileList = ref<any[]>([]);

// 上传文件处理
const handleUploadCustomRequest = async (options: any) => {
  const { file, onSuccess, onError } = options;
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await UserAPI.uploadCurrentUserAvatar(formData);
    const fileUrl = response.data.data.file_url;
    infoFormState.avatar = fileUrl;
    fileList.value = [{ url: fileUrl }];

    onSuccess(response, file);
  } catch (error) {
    onError(error);
    console.error('上传失败:', error);
  }
};

// 邮箱校验规则优化
const rules = {
  name: [
    { required: true, message: "请输入姓名", trigger: "blur" },
  ],
  mobile: [
    { required: true, message: "请输入手机号", trigger: "blur" },
    {
      pattern: /^1[3-9]\d{9}$/,
      message: "手机号格式不正确，请输入有效的中国大陆手机号",
      trigger: "blur",
    },
  ],
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    {
      pattern: /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/,
      message: "邮箱格式不正确，请输入有效的邮箱地址",
      trigger: "blur",
    },
  ],
};


const resetPasswordRules = {
    oldPassword: [
      {
        required: true,
        trigger: "blur",
        message: t("login.password"),
      },
    ],
    newPassword: [
      {
        required: true,
        trigger: "blur",
        message: t("login.message.password.required"),
      },
      {
        min: 6,
        message: t("login.message.password.min"),
        trigger: "blur",
      },
    ],
    confirmPassword: [
      {
        required: true,
        trigger: "blur",
        message: t("login.message.password.required"),
      },
      {
        min: 6,
        message: t("login.message.password.min"),
        trigger: "blur",
      },
      {
        validator: (_: any, value: string) => {
          return value === passwordFormState.newPassword;
        },
        trigger: "blur",
        message: t("login.message.password.inconformity"),
      },
    ],
};

// 初始化表单
const initInfoForm = () => {
  const basicInfo = userStore.basicInfo;
  Object.assign(infoFormState, { ...basicInfo });
};

// 初始化密码表单
const initPasswordForm = () => {
  Object.assign(passwordFormState, {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
};

onMounted(async () => {
  await getOptions();
  initInfoForm();
});
</script>

<style lang="scss" scoped>
/* 样式调整 */
.user-info-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;

  .avatar-wrapper {
    position: relative;
    margin-bottom: 16px;

    .avatar-edit-btn {
      position: absolute;
      bottom: 0;
      right: 0;
      background-color: rgba(0, 0, 0, 0.5);
      border-radius: 50%;
      cursor: pointer;
    }

    .avatar-upload-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: none;
      z-index: 10;
    }

    &:hover .avatar-upload-overlay {
      display: block;
    }
  }

}
</style>
