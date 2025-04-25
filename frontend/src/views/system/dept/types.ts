export interface searchDataType {
    name?: string
    available?: number
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
    created_at?: string;
    updated_at?: string;
    children?: tableDataType[];
}
