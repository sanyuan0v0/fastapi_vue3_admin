export interface searchDataType {
    name?: string
    available?: boolean
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    order?: number;
    available?: boolean;
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