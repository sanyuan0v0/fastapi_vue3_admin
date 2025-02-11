export interface searchDataType {
    name?: string
    date_range?: [string, string];
}

export interface tableDataType {
    id?: number;
    index?: number;
    test_type?: string;
    status?: string;
    logs?: string;
    screenshot_path?: string;
    actual_response?: string;
    test_case_id?: testCaseSeletorType['id'];
    project_id? : projectSeletorType['id'];
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
}

export interface testCaseSeletorType {
    id?: number;
    name?: string;
    description?: string;
}
