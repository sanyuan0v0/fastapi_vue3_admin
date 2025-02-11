export interface searchDataType {
    name?: string
    date_range?: [string, string];
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    task_id?: number;
    summary?: string;
    details?: string;
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
