export interface searchDataType {
    name?: string
    available?: string
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    order?: number;
    parent_id?: number;
    parent_name?: string;
    available?: boolean;
    description?: string;
    children?: tableDataType[];
    created_at?: string;
    updated_at?: string;
    creator?: creatorType;
}

interface creatorType {
    id?: number;
    name?: string;
    username?: string;
}