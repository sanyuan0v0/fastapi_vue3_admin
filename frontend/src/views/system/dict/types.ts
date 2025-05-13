export interface searchDataType {
    dict_name?: string
    dict_type?: string
    available?: boolean;
}

export interface searchDictDataType {
    dict_label?: string
    dict_type?: string
    available?: boolean;
}

export interface tableDictType {
    id?: number;
    index?: number;
    dict_name?: string;
    dict_type?: string;
    available?: boolean;
    description?: string;
    created_at?: string;
    updated_at?: string;
    creator?: creatorType;
}

export interface tableDictDataType {
    id?: number;
    index?: number;
    dict_sort?: number;
    dict_label?: string;
    dict_value?: string;
    dict_type?: string;
    css_class?: string;
    list_class?: string;
    is_default?: boolean;
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

