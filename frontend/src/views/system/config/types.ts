export interface tableDataType {
    id?: number; // id 是可选的，类型为 number
    title: string; // 网站标题
    favicon: string; // 网站图标
    logo: string; // 登录页Logo
    background: string; // 登录页背景图
    description: string; // 网站描述
    copyright: string; // 版权信息
    keep_record: string; // 备案号
    help_url: string; // 帮助链接
    privacy_url: string; // 隐私条款链接
    clause_url: string; // 服务条款链接
    code_url: string; // 代码仓库链接
}
