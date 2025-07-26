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
              <el-avatar 
                v-if="infoFormState.avatar"
                :src="infoFormState.avatar" 
                :size="120"
              />
              <el-avatar 
                v-else
                icon="UserFilled" 
                :size="120"
              />
                
              <el-upload
                  class="el-upload"
                  v-model:file-list="fileList"
                  name="avatar"
                  :show-file-list="false"
                  :before-upload="handleBeforeUpload"
                  :on-success="handleUploadSuccess"
                  :disabled="loading"
                  :limit="1"
                  :auto-upload="false"
                  action="/api/upload/avatar"
                >
                  <template #trigger>
                    <el-button type="primary" :icon="Camera" class="upload-trigger"  />
                  </template>
                </el-upload>
            </div>
            <span class="user-name">
              {{ infoFormState.name }}
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
                <el-form ref="ruleFormRef" :model="infoFormState" :rules="rules" :inline="true" label-suffix=":">
                  
                  <el-form-item label="姓名" name="name">
                    <el-input v-model="infoFormState.name" placeholder="请输入姓名" prefix-icon="User" clearable />
                  </el-form-item>

                  <el-form-item label="手机号" name="mobile">
                    <el-input v-model="infoFormState.mobile" placeholder="请输入手机号码" prefix-icon="Phone" clearable />
                  </el-form-item>

                  <el-form-item label="邮箱" name="email">
                    <el-input v-model="infoFormState.email" placeholder="请输入邮箱" prefix-icon="Message" clearable />
                  </el-form-item>

                  <el-form-item label="性别" name="gender">
                    <el-radio-group v-model="infoFormState.gender">
                      <el-radio v-for="item in dictDataStore['sys_user_sex']" :key="item.dict_value" :value="item.dict_value" >
                        {{ item.dict_label }}
                      </el-radio>
                    </el-radio-group>
                  </el-form-item>

                  <el-form-item>
                    <el-button type="primary" :loading="infoSubmitting" icon="edit" @click="handleSave">保存更改</el-button>
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
                <el-form ref="ruleFormRef" :model="passwordFormState" :rules="resetPasswordRules"  label-suffix=":">
                  <el-form-item label="当前密码" name="old_password">
                    <el-input v-model.trim="passwordFormState.old_password" :placeholder="t('login.password')" type="password" show-password clearable>
                      <template #prefix>
                        <Lock />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="新密码" name="new_password">
                    <el-input v-model.trim="passwordFormState.new_password" type="password" :placeholder="t('login.newPassword')" show-password clearable>
                      <template #prefix>
                        <Key />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item label="确认新密码" name="confirm_password">
                    <el-input v-model.trim="passwordFormState.confirm_password" type="password" :placeholder="t('login.message.password.confirm')" show-password clearable>
                      <template #prefix>
                        <Check />
                      </template>
                    </el-input>
                  </el-form-item>

                  <el-form-item>
                    <el-button type="primary" :loading="passwordChanging" icon="edit" @click="handlePasswordChange">更新密码</el-button>
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
import { useUserStoreHook } from "@/store/modules/user.store";
import { Camera } from '@element-plus/icons-vue';
import { useI18n } from "vue-i18n";
import router from "@/router";

const { t } = useI18n();
const userStore = useUserStore();
const dictStore = useDictStore();
const ruleFormRef = ref<FormInstance>();
const loading = ref<boolean>(false);

const dictDataStore = computed(() => dictStore.dictData);

// 字典数据
const getOptions = async () => {
  return await dictStore.getDict(['sys_user_sex']);;
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
  old_password: '',
  new_password: '',
  confirm_password: ''
});

// 头像上传处理优化
const fileList = ref<any[]>([]);

// 文件上传前校验
const handleBeforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/');
  if (!isImage) {
    ElMessage.error('只能上传图片文件');
    return false;
  }
  return true;
};

// 上传成功回调
const handleUploadSuccess = (response: any) => {
  updateAvatar(response.data.file_url);
  ElMessage.success('头像上传成功');
};

// 更新头像信息
const updateAvatar = (fileUrl: string) => {
  infoFormState.avatar = fileUrl;
  fileList.value = [{ url: fileUrl }];
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
          return value === passwordFormState.new_password;
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

// 基本信息表单提交
const handleSave = async () => {
  try {
    infoSubmitting.value = true;
    infoFormState.avatar = infoFormState.avatar;
    const response = await UserAPI.updateCurrentUserInfo(infoFormState);
    await userStore.setUserInfo(response.data.data);
  } catch (error) {
    console.error(error);
  } finally {
    infoSubmitting.value = false;
  }
};

// 修改密码
const handlePasswordChange = async () => {
  try {
    passwordChanging.value = true;
    const response = await UserAPI.changeCurrentUserPassword(passwordFormState);
    initPasswordForm();
    await redirectToLogin(response.data.msg);
  } catch (error) {
    console.error(error);
  } finally {
    passwordChanging.value = false;
  }
};

/**
 * 重定向到登录页面
 */
async function redirectToLogin(message: string = "请重新登录"): Promise<void> {
  try {
    ElNotification({
      title: "提示",
      message,
      type: "warning",
      duration: 3000,
    });

    await useUserStoreHook().resetAllState();

    // 跳转到登录页，保留当前路由用于登录后跳转
    const currentPath = router.currentRoute.value.fullPath;
    await router.push(`/login?redirect=${encodeURIComponent(currentPath)}`);
  } catch (error: any) {
    ElMessage.error(error.message);
  }
}

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

  .avatar-wrapper {
    margin-bottom: 16px;
    position: relative;

    .el-upload {

      &:hover {
        opacity: 0.8; /* 鼠标悬浮时稍微降低透明度 */
      }
    }

    .upload-trigger {
      // top: 50%;
      // left: 50%;
      position: absolute;
      transform: translate(-50%, -50%);
      opacity: 0;
      border-radius: 50%;
      width: 28px;
      height: 28px;
      background: var(--el-color-primary);
    }

    /* 提升 hover 样式优先级 */
    &:hover .upload-trigger {
      opacity: 1 !important; /* 强制生效 */
    }
  }
}
</style>
