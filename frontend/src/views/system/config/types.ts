export interface tableDataType {
    id?: number;
    name?: string;
    order?: number;
    fied_key?: string;
    fied_value?: string;
    parent_id?: number;
    fileList?: any[];
    children?: tableDataType[];
}