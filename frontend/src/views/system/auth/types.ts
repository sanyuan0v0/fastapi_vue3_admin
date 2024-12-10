export interface LoginForm {
    username: string;
    password: string;
    captcha: string;
    captcha_key: string;
    remember: boolean;
}

export interface CaptchaState {
    enable: boolean;
    key: string;
    img_base: string;
}

export interface ForgetPasswordForm {
    username: string;
    mobile: string;
    new_password: string;
}

export interface RegisterForm {
    username: string;
    name: string;
    password: string;
    mobile: string;
    email: string;
    gender: number;
}
