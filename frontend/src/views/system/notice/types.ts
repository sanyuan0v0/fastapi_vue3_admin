export interface searchDataType {
    notice_title?: string
    available?: boolean;
}

export interface tableDataType {
    id?: number;
    index?: number;
    notice_title?: string;
    notice_type?: string;
    notice_content?: string;
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