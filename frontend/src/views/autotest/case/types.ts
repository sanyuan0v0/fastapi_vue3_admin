export interface searchDataType {
    name?: string
    date_range?: [string, string];
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    status?: boolean;
    url?: string;
    method?: string;
    headers?: Record<string, string>;
    params?: Record<string, string>;
    body?: Record<string, any>;
    files?: Record<string, string>;
    parameter_need?:  boolean;
    expected?: Array<{
        type: 'status_code' | 'msg' | 'response';
        rule: 'equals' | 'not_equals' | 'contains' | 'not_contains' | 'jsonpath' | 'regex';
        expect: any;
    }>;
    project_id?: projectSelectorType['id'];
    description?: string;
    created_at?: string;
    updated_at?: string;
    creator?: {
        id?: number;
        name?: string;
        username?: string;
    };
    
    project?: projectSelectorType;
}


export interface  projectSelectorType {
    id?: number;
    name?: string;
    description?: string;
}