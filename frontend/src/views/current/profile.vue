<template>
  <div class="profile-container">
    <page-header title="个人设置" />
    <div class="profile-content">
      <a-row :gutter="[24, 24]">
        <!-- 左侧信息卡片 -->
        <a-col :xs="24" :sm="24" :md="8" :lg="6">
          <a-card class="info-card" :bordered="false">
            <div class="user-info-header">
              <div class="avatar-wrapper">
                <a-avatar v-if="infoFormState.avatar" :src="infoFormState.avatar" :size="120" />
                <a-avatar v-else :size="120">
                  <template #icon><UserOutlined /></template>
                </a-avatar>
                <div class="avatar-upload-overlay">
                  <a-upload
                    name="file"
                    :show-upload-list="false"
                    :headers="uploadHeaders"
                    action="/api/v1/system/user/current/avatar/upload"
                    @change="avatarHandleChange"
                  >
                    <a-button type="link">
                      <template #icon><UploadOutlined /></template>
                      更换头像
                    </a-button>
                  </a-upload>
                </div>
              </div>
              <h2 class="user-name">{{ infoFormState.name }}</h2>
              <p class="user-role">{{ infoFormState.roles.join('、') }}</p>
            </div>
            
            <a-divider />
            
            <a-descriptions :column="1" size="small" class="user-details">
              <a-descriptions-item>
                <template #label>
                  <span class="detail-label">
                    <IdcardOutlined />
                    <span>账号</span>
                  </span>
                </template>
                {{ infoFormState.username }}
              </a-descriptions-item>
              <a-descriptions-item>
                <template #label>
                  <span class="detail-label">
                    <TeamOutlined />
                    <span>部门</span>
                  </span>
                </template>
                {{ infoFormState.deptName }}
              </a-descriptions-item>
              <a-descriptions-item>
                <template #label>
                  <span class="detail-label">
                    <ApartmentOutlined />
                    <span>岗位</span>
                  </span>
                </template>
                {{ infoFormState.positions.join('、') }}
              </a-descriptions-item>
              <a-descriptions-item>
                <template #label>
                  <span class="detail-label">
                    <PhoneOutlined />
                    <span>手机</span>
                  </span>
                </template>
                {{ infoFormState.mobile }}
              </a-descriptions-item>
              <a-descriptions-item>
                <template #label>
                  <span class="detail-label">
                    <MailOutlined />
                    <span>邮箱</span>
                  </span>
                </template>
                {{ infoFormState.email }}
              </a-descriptions-item>
              <a-descriptions-item>
                <template #label>
                  <span class="detail-label">
                    <ClockCircleOutlined />
                    <span>加入时间</span>
                  </span>
                </template>
                {{ infoFormState.created_at }}
              </a-descriptions-item>
            </a-descriptions>
          </a-card>
        </a-col>

        <!-- 右侧设置区域 -->
        <a-col :xs="24" :sm="24" :md="16" :lg="18">
          <a-card class="settings-card" :bordered="false">
            <a-tabs v-model:activeKey="selectedKeys[0]" @change="handleTabChange">
              <a-tab-pane key="1">
                <template #tab>
                  <span class="tab-label">
                    <UserOutlined />
                    <span>基本设置</span>
                  </span>
                </template>
                <div class="settings-form">
                  <a-form
                    layout="vertical"
                    :model="infoFormState"
                    @finish="onInfoFormFinish"
                    class="info-form"
                  >
                    <a-row :gutter="16">
                      <a-col :span="12">
                        <a-form-item
                          label="姓名"
                          name="name"
                          :rules="[{ required: true, message: '请输入姓名' }]"
                        >
                          <a-tooltip title="请输入您的真实姓名" placement="topLeft">
                            <a-input
                              v-model:value="infoFormState.name"
                              placeholder="请输入姓名"
                              allow-clear
                            >
                              <template #prefix><UserOutlined /></template>
                            </a-input>
                          </a-tooltip>
                        </a-form-item>
                      </a-col>
                      
                      <a-col :span="12">
                        <a-form-item
                          label="性别"
                          name="gender"
                          :rules="[{ required: true, message: '请选择性别' }]"
                        >
                          <a-radio-group v-model:value="infoFormState.gender" class="gender-group">
                                <a-radio v-for="item in DictDataStore['sys_user_sex']" :value="item.dict_value">
                                    {{ item.dict_label }}
                                </a-radio>
                            </a-radio-group>
                        </a-form-item>
                      </a-col>
                      
                      <a-col :span="12">
                        <a-form-item
                          label="手机号码"
                          name="mobile"
                          :rules="[
                            { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码' }
                          ]"
                        >
                          <a-tooltip title="用于接收系统通知" placement="topLeft">
                            <a-input
                              v-model:value="infoFormState.mobile"
                              placeholder="请输入手机号码"
                              allow-clear
                            >
                              <template #prefix><PhoneOutlined /></template>
                            </a-input>
                          </a-tooltip>
                        </a-form-item>
                      </a-col>
                      
                      <a-col :span="12">
                        <a-form-item
                          label="邮箱"
                          name="email"
                          :rules="[{ type: 'email', message: '请输入有效的邮箱地址' }]"
                        >
                          <a-tooltip title="用于接收重要通知" placement="topLeft">
                            <a-input
                              v-model:value="infoFormState.email"
                              placeholder="请输入邮箱"
                              allow-clear
                            >
                              <template #prefix><MailOutlined /></template>
                            </a-input>
                          </a-tooltip>
                        </a-form-item>
                      </a-col>
                    </a-row>

                    <a-form-item>
                      <a-button
                        type="primary"
                        html-type="submit"
                        :loading="infoSubmitting"
                        class="submit-button"
                      >
                        <template #icon><SaveOutlined /></template>
                        保存更改
                      </a-button>
                    </a-form-item>
                  </a-form>
                </div>
              </a-tab-pane>

              <a-tab-pane key="2">
                <template #tab>
                  <span class="tab-label">
                    <LockOutlined />
                    <span>安全设置</span>
                  </span>
                </template>
                <div class="settings-form">
                  <a-form
                    layout="vertical"
                    :model="passwordFormState"
                    @finish="onPasswordFormFinish"
                    class="password-form"
                  >
                    <a-form-item
                      label="当前密码"
                      name="oldPassword"
                      :rules="[{ required: true, message: '请输入当前密码' }]"
                    >
                      <a-input-password
                        v-model:value="passwordFormState.oldPassword"
                        placeholder="请输入当前密码"
                        allow-clear
                      >
                        <template #prefix><LockOutlined /></template>
                      </a-input-password>
                    </a-form-item>

                    <a-form-item
                      label="新密码"
                      name="newPassword"
                      :rules="[
                        { required: true, message: '请输入新密码' },
                        { min: 6, message: '密码长度不能小于6位' }
                      ]"
                    >
                      <a-input-password
                        v-model:value="passwordFormState.newPassword"
                        placeholder="请输入新密码"
                        allow-clear
                      >
                        <template #prefix><KeyOutlined /></template>
                      </a-input-password>
                    </a-form-item>

                    <a-form-item
                      label="确认新密码"
                      name="repeatPassword"
                      :rules="[
                        { required: true, message: '请确认新密码' },
                        { validator: validateRepeatPassword }
                      ]"
                    >
                      <a-input-password
                        v-model:value="passwordFormState.repeatPassword"
                        placeholder="请再次输入新密码"
                        allow-clear
                      >
                        <template #prefix><CheckOutlined /></template>
                      </a-input-password>
                    </a-form-item>

                    <a-form-item>
                      <a-button
                        type="primary"
                        html-type="submit"
                        :loading="passwordChanging"
                        class="submit-button"
                      >
                        <template #icon><SaveOutlined /></template>
                        更新密码
                      </a-button>
                    </a-form-item>
                  </a-form>
                </div>
              </a-tab-pane>
            </a-tabs>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script lang="ts" setup>
import PageHeader from '@/components/PageHeader.vue';
import { ref, reactive, onMounted, h, watch, computed } from 'vue';
import { message } from 'ant-design-vue';
import type { UploadChangeParam } from "ant-design-vue";
import { 
  UserOutlined, 
  LockOutlined,
  PhoneOutlined,
  MailOutlined,
  IdcardOutlined,
  TeamOutlined,
  ApartmentOutlined,
  UploadOutlined,
  KeyOutlined,
  CheckOutlined,
  SaveOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined
} from '@ant-design/icons-vue';
import { useUserStore } from "@/store/index";
import storage from 'store';
import { updateCurrentUserInfo, changeCurrentUserPassword, avatarHandleChange } from '@/api/system/user';
import type { InfoFormState, PasswordFormState } from './types';
import { useDictStore } from "@/store/index";

const dictStore = useDictStore();

const DictDataStore = computed(() => {
    return dictStore.dictObj;
})

const getOptions = async () => {
    const dictOptions = await dictStore.setDict(['sys_user_sex'])
    return dictOptions
}

// 状态定义
const passwordChanging = ref(false);
const infoSubmitting = ref(false);
const selectedKeys = ref<string[]>(['1']);

// 表单状态
const infoFormState = reactive<InfoFormState>({
  name: '',
  gender: null,
  mobile: '',
  email: '',
  username: '',
  deptName: '',
  positions: [],
  roles: [],
  avatar: '',
  created_at: ''
});

const passwordFormState = reactive<PasswordFormState>({
  oldPassword: '',
  newPassword: '',
  repeatPassword: ''
});

// 上传头像配置
const token = storage.get('Access-Token');
const uploadHeaders = token ? { Authorization: 'Bearer ' + token } : {};

// 监听selectedKeys变化
watch(selectedKeys, (newVal) => {
  if (newVal[0] === '1') {
    initInfoForm();
  } else {
    initPasswordForm();
  }
});

const userStore = useUserStore();

// 基本信息表单提交
const onInfoFormFinish = async (values: any) => {
  try {
    infoSubmitting.value = true;
    values.avatar = infoFormState.avatar;
    const response = await updateCurrentUserInfo(values);
    message.success({
      content: response.data.msg,
      icon: h(CheckCircleOutlined, { style: "color: #52c41a" })
    });
    
    await userStore.getUserInfo;
  } catch (error) {
    console.error(error);
    
  } finally {
    infoSubmitting.value = false;
  }
};

// 密码表单提交
const onPasswordFormFinish = async (values: any) => {
  try {
    if (values.newPassword !== values.repeatPassword) {
      message.error({
        content: '两次密码输入不一致',
        icon: h(CloseCircleOutlined, { style: "color: #ff4d4f" })
      });
      return;
    }

    passwordChanging.value = true;
    const data = { 
      old_password: values.oldPassword, 
      new_password: values.newPassword 
    };
    
    const response = await changeCurrentUserPassword(data);
    message.success({
      content: response.data.msg,
      icon: h(CheckCircleOutlined, { style: "color: #52c41a" })
    });
    initPasswordForm();
  } catch (error) {
    console.error('修改密码失败:', error);
    message.error({
      content: '修改密码失败',
      icon: h(CloseCircleOutlined, { style: "color: #ff4d4f" })
    });
  } finally {
    passwordChanging.value = false;
  }
};

// 头像上传处理
const avatarHandleChange = (info: UploadChangeParam) => {
  if (info.file.status === 'done') {
    const response = info.file.response;
    const apiUrl = import.meta.env.VITE_API_BASE_URL + import.meta.env.VITE_APP_BASE_API
    const newAvatar = apiUrl + '/' + response.data.file_path;
    infoFormState.avatar = newAvatar;
    message.success({
      content: '上传成功',
      icon: h(CheckCircleOutlined, { style: "color: #52c41a" })
    });
  } else if (info.file.status === 'error') {
    message.error({
      content: '上传失败',
      icon: h(CloseCircleOutlined, { style: "color: #ff4d4f" })
    });
  }
};

// 初始化表单
const initInfoForm = () => {
  const basicInfo = userStore.basicInfo;
  console.log("basicInfo", basicInfo);
  Object.assign(infoFormState, {
    name: basicInfo.name,
    gender: basicInfo.gender,
    mobile: basicInfo.mobile,
    email: basicInfo.email,
    username: basicInfo.username,
    deptName: basicInfo.dept_name,
    positions: basicInfo.positions.map(item => item.name),
    roles: basicInfo.roles.map(item => item.name),
    avatar: basicInfo.avatar,
    created_at: basicInfo.created_at
  });
};

const initPasswordForm = () => {
  Object.assign(passwordFormState, {
    oldPassword: '',
    newPassword: '',
    repeatPassword: ''
  });
};

// 新增密码验证函数
const validateRepeatPassword = async (_rule: any, value: string) => {
  if (value !== passwordFormState.newPassword) {
    return Promise.reject('两次输入的密码不一致');
  }
  return Promise.resolve();
};

// 替换菜单点击为标签页切换
const handleTabChange = (key: string) => {
  selectedKeys.value = [key];
  if (key === '1') {
    initInfoForm();
  } else {
    initPasswordForm();
  }
};

onMounted(async () => {
  await getOptions();
  initInfoForm();
});
</script>

<style lang="scss" scoped>
.profile-container {
  min-height: 90vh;
  
  .profile-content {
    padding: 24px;
    
    @media (max-width: 768px) {
      padding: 16px;
    }
  }

  .info-card {
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
    transition: all var(--transition-duration);
    
    &:hover {
      box-shadow: 0 3px 6px -4px rgba(0, 0, 0, 0.12);
    }

    .user-info-header {
      text-align: center;
      padding: 24px 0;

      .avatar-wrapper {
        position: relative;
        width: 120px;
        height: 120px;
        margin: 0 auto 16px;
        border-radius: 50%;
        overflow: hidden;
        
        &::after {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          opacity: 0;
          transition: opacity var(--transition-duration);
        }
        
        .avatar-upload-overlay {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          background: var(--hover-bg-color);
          padding: 12px 0;
          opacity: 0;
          transition: all var(--transition-duration);
          transform: translateY(100%);
          z-index: 1;
          
          .ant-btn {
            color: #fff;
            font-weight: 500;
            font-size: 14px;
            
            &:hover {
              color: #40a9ff;
            }
            
            .anticon {
              margin-right: 4px;
              font-size: 16px;
            }
          }
        }

        &:hover {
          &::after {
            opacity: 1;
          }
          
          .avatar-upload-overlay {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .ant-avatar {
          width: 100%;
          height: 100%;
        }
      }

      .user-name {
        margin: 8px 0 4px;
        font-size: 20px;
        line-height: 28px;
        font-weight: 500;
      }

      .user-role {
        font-size: 14px;
      }
    }

    .user-details {
      :deep(.ant-descriptions-item) {
        padding-bottom: 12px;

        .detail-label {
          display: inline-flex;
          align-items: center;
          white-space: nowrap;
          
          .anticon {
            margin-right: 8px;
            font-size: 16px;
          }
        }

        .ant-descriptions-item-content {
          display: inline-block;
        }

        .ant-descriptions-item-colon {
          display: inline-block;
          margin: 0 8px;
        }
      }
    }
  }

  .settings-card {
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
    
    :deep(.ant-tabs-nav) {
      margin-bottom: 24px;
    }

    .settings-form {
      max-width: 800px;
      margin: 0 auto;
      padding: 24px;
      
      @media (max-width: 768px) {
        padding: 16px 0;
      }

      .submit-button {
        min-width: 120px;
      }
    }

    .info-form, .password-form {
      .ant-form-item {
        margin-bottom: 24px;
      }

      .ant-input-affix-wrapper {
        border-radius: 4px;
        
        &:hover, &:focus {
          border-color: var(--primary-color);
        }
      }

      .gender-group {
        width: 100%;
      }
    }

    .password-form {
      max-width: 400px;
    }

    .tab-label {
      display: flex;
      align-items: center;
      
      .anticon {
        margin-right: 8px;
        font-size: 16px;
      }
    }
  }
}

// 添加过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>