export interface searchDataType {
    name?: string
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    order?: number;
    fied_key?: string;
    fied_value?: string;
    parent_id?: number;
    parent_name?: string;
    children?: tableDataType[];
}
