export interface searchDataType {
    name?: string
    date_range?: [string, string];
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    base_url?: string;
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
    id: number;
    name: string;
    description: string;
}
