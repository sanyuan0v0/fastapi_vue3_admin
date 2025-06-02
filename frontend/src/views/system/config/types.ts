export interface searchType {
    config_name?: string
    config_key?: string
    config_type?: boolean;
}


export interface tableType {
    id?: number; // id 是可选的，类型为 number
    index?: number;
    config_name?: string;
    config_key?: string;
    config_value?: string;
    config_type?: boolean;
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
