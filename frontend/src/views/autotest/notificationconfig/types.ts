export interface searchDataType {
    name?: string;
    date_range?: [string, string];
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    config?: { [key: string]: string };
    project_id?: number;
    description?: string;
    created_at?: string;
    updated_at?: string;
    creator?: {
        id?: number;
        name?: string;
        username?: string;
    };
}

export interface projectSeletorType {
    id: number;
    name: string;
    description: string;
}