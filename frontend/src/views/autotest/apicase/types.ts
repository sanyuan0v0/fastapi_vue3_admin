export interface searchDataType {
    name?: string
    date_range?: [string, string];
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    url?: string;
    method?: string;
    headers?: string;
    data_type?: string;
    data?: string;
    expected_status_code?: number;
    expected_msg?: string;
    expected_response?: string;
    assertions_status_code?: string;
    assertions_msg?: string;
    assertions_response?: string;
    module_id?: moduleTableDataType['id'];
    project_id? : projectSeletorType['id'];
    environment_id?: environmentTableDataType['id'];
    global_data_id?: globalDataTableDataType['id'];
    description?: string;
    created_at?: string;
    updated_at?: string;
    creator?: creatorType;
}

interface creatorType {
    id?: number;
    name?: string;
    username?: string;
}

export interface projectSeletorType {
    id?: number;
    name?: string;
    description?: string;
    created_at?: string;
    updated_at?: string;
    creator?: creatorType;
}

export interface moduleTableDataType {
    id?: number;
    name?: string;
    project_id? : projectSeletorType['id'];
    description?: string;
    created_at?: string;
    updated_at?: string;
    creator?: creatorType;
}

export interface environmentTableDataType {
  id?: number;
  name?: string;
  base_url?: string;
  project_id? : projectSeletorType['id'];
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface globalDataTableDataType {
  id?: number;
  name?: string;
  value?: string;
  project_id? : projectSeletorType['id'];
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

// 添加模块弹窗类型定义
export type ModuleModalType = 'create' | 'update' | 'view';

export interface ModuleModalState {
    open: boolean;
    title: string;
    loading: boolean;
    type: ModuleModalType;
    id: number | null;
}

// 请求方法类型
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'HEAD' | 'OPTIONS';

// k-v 格式定义
export interface KeyValue {
  key: string;
  value: string;
}

// 参数类型定义
export type ParamsType = 'params' | 'data' | 'json' | 'file';

// 断言规则定义
export type AssertionRule = '=' | '!=' | '>' | '<' | '>=' | '<=' | 'in' | 'not in';

// 调试窗口状态
export interface DebugModalState {
  open: boolean;
  loading: boolean;
}

// 调试请求参数
export interface DebugRequestType {
  method: HttpMethod;
  url: string;
  headers: Record<string, string>;
  params: Record<string, string>;
  body: any;
}

// 调试响应结果
export interface DebugResponseType {
  status: number;
  statusText: string;
  headers: Record<string, string>;
  data: any;
  time: number;
  size: string;
}