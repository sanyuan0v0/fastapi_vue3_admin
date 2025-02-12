export interface searchDataType {
    name?: string
    date_range?: [string, string];
    environment_id?: number;
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    base_url?: string;
    headers?: {[key: string]: string}
    message?: {[key: string]: string}
    description?: string;
    created_at?: string;
    updated_at?: string;
    creator?: {
        id?: number;
        name?: string;
        username?: string;
    },
    cases?: {
        id?: number;
        name?: string;
    }[],
    tasks?: {
        id?: number;
        name?: string;
    }[],
}
