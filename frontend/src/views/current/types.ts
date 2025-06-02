export interface InfoFormState {
    name: string;
    gender: number | null;
    mobile: string;
    email: string;
    username: string;
    deptName: string;
    positions: [];
    roles: [];
    avatar: string;
    created_at: string;
}

export interface PasswordFormState {
    oldPassword: string;
    newPassword: string;
    repeatPassword: string;
}

export interface tableDataType {
    id?: number; 
    config_name?: string;
    config_key?: string;
    config_value?: string;
    config_type?: boolean;
    description?: string;
}
