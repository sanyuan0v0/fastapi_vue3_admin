export interface searchType {
    name?: string
    status?: boolean
    date_range?: [string, string];
}

export interface tableJobType {
    id?: number;
    index?: number;
    name?: string;
    func?: string;
    trigger?: string;
    args?: string;
    kwargs?: string;
    coalesce?: boolean;
    max_instances?: number;
    jobstore?: string;
    executor?: string;
    trigger_args?: string;
    start_date?: string;
    end_date?: string;
    status?: boolean;
    message?: string;
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

