export interface QueryState {
    ipaddr?: string;
    user_name?: string;
    login_location?: string;
}

export interface OnlineUser {
    session_id: string;
    user_id: number;
    user_name: string;
    ipaddr: string;
    login_location: string;
    os: string;
    browser: string;
    login_time: string;
}
