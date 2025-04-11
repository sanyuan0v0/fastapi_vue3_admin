# -*- coding: utf-8 -*-

from enum import Enum


class RET(Enum):
    """
    系统返回码枚举
    
    0~200: 成功状态码
    400~600: HTTP标准错误码
    4000+: 自定义业务错误码
    """

    # 成功状态码
    OK = (0, "成功")
    SUCCESS = (200, "操作成功")
    CREATED = (201, "创建成功")
    ACCEPTED = (202, "请求已接受")
    NO_CONTENT = (204, "操作成功,无返回数据")

    # HTTP标准错误码
    ERROR = (1, "请求错误")
    BAD_REQUEST = (400, "参数错误")
    UNAUTHORIZED = (401, "未授权")
    FORBIDDEN = (403, "访问受限")
    NOT_FOUND = (404, "资源不存在")
    BAD_METHOD = (405, "不支持的请求方法")
    NOT_ACCEPTABLE = (406, "不接受的请求")
    CONFLICT = (409, "资源冲突")
    GONE = (410, "资源已删除")
    PRECONDITION_FAILED = (412, "前提条件失败")
    UNSUPPORTED_MEDIA_TYPE = (415, "不支持的媒体类型")
    UNPROCESSABLE_ENTITY = (422, "无法处理的实体")
    TOO_MANY_REQUESTS = (429, "请求过于频繁")

    # 服务器错误码
    INTERNAL_SERVER_ERROR = (500, "服务器内部错误")
    NOT_IMPLEMENTED = (501, "功能未实现")
    BAD_GATEWAY = (502, "网关错误")
    SERVICE_UNAVAILABLE = (503, "服务不可用")
    GATEWAY_TIMEOUT = (504, "网关超时")
    HTTP_VERSION_NOT_SUPPORTED = (505, "HTTP版本不支持")

    # 自定义业务错误码
    EXCEPTION = (-1, "系统异常")
    DATAEXIST = (4003, "数据已存在")
    DATAERR = (4004, "数据错误")
    PARAMERR = (4103, "参数错误")
    IOERR = (4302, "IO错误")
    SERVERERR = (4500, "服务错误")
    UNKOWNERR = (4501, "未知错误")
    TIMEOUT = (4502, "请求超时")
    RATE_LIMIT_EXCEEDED = (4503, "访问频率超限")
    
    # Token相关错误码
    INVALID_TOKEN = (4504, "无效令牌")
    EXPIRED_TOKEN = (4505, "令牌过期")
    
    # 认证授权错误码
    INVALID_CREDENTIALS = (4506, "无效凭证")
    INVALID_REQUEST = (4507, "无效请求")
    INVALID_FORMAT = (4508, "格式错误")
    INVALID_INPUT = (4509, "输入错误")
    INVALID_STATE = (4510, "状态错误")
    INVALID_OPERATION = (4511, "操作错误")
    INVALID_PERMISSION = (4512, "权限错误")
    INVALID_RESOURCE = (4513, "资源错误")
    INVALID_CONFIGURATION = (4514, "配置错误")
    
    # 会话安全错误码
    INVALID_SESSION = (4515, "会话错误")
    INVALID_LICENSE = (4516, "许可证错误")
    INVALID_CERTIFICATE = (4517, "证书错误")
    INVALID_SIGNATURE = (4518, "签名错误")
    INVALID_ENCRYPTION = (4519, "加密错误")
    INVALID_DECRYPTION = (4520, "解密错误")
    INVALID_COMPRESSION = (4521, "压缩错误")
    INVALID_DECOMPRESSION = (4522, "解压错误")
    
    # 权限相关错误码
    INVALID_AUTHENTICATION = (4523, "认证错误")
    INVALID_AUTHORIZATION = (4524, "授权错误")
    INVALID_ACCESS = (4525, "访问错误")
    INVALID_SECURITY = (4526, "安全错误")
    
    # 系统组件错误码
    INVALID_NETWORK = (4527, "网络错误")
    INVALID_DATABASE = (4528, "数据库错误")
    INVALID_CACHE = (4529, "缓存错误")
    INVALID_QUEUE = (4530, "队列错误")
    INVALID_LOCK = (4531, "锁错误")
    INVALID_TRANSACTION = (4532, "事务错误")
    INVALID_LOG = (4533, "日志错误")
    INVALID_MONITORING = (4534, "监控错误")
    INVALID_NOTIFICATION = (4535, "通知错误")
    
    # 任务调度错误码
    INVALID_SCHEDULING = (4536, "调度错误")
    INVALID_TASK = (4537, "任务错误")
    INVALID_JOB = (4538, "作业错误")
    INVALID_WORKFLOW = (4539, "工作流错误")
    
    # 开发相关错误码
    INVALID_SCRIPT = (4540, "脚本错误")
    INVALID_PLUGIN = (4541, "插件错误")
    INVALID_MODULE = (4542, "模块错误")
    INVALID_PACKAGE = (4543, "包错误")
    INVALID_CLASS = (4544, "类错误")
    INVALID_FUNCTION = (4545, "函数错误")
    INVALID_METHOD = (4546, "方法错误")
    INVALID_PROPERTY = (4547, "属性错误")
    INVALID_VARIABLE = (4548, "变量错误")
    INVALID_CONSTANT = (4549, "常量错误")
    INVALID_ENUM = (4550, "枚举错误")
    INVALID_INTERFACE = (4551, "接口错误")
    INVALID_PROTOCOL = (4552, "协议错误")
    
    # 服务相关错误码
    INVALID_SERVICE = (4553, "服务错误")
    INVALID_CLIENT = (4554, "客户端错误")
    INVALID_SERVER = (4555, "服务器错误")
    INVALID_SYSTEM = (4556, "系统错误")
    
    # 用户权限错误码
    INVALID_USER = (4557, "用户错误")
    INVALID_GROUP = (4558, "用户组错误")
    INVALID_ROLE = (4559, "角色错误")
    INVALID_PERMISSION_GROUP = (4560, "权限组错误")
    INVALID_PERMISSION_ROLE = (4561, "权限角色错误")
    INVALID_PERMISSION_USER = (4562, "权限用户错误")
    INVALID_PERMISSION_RESOURCE = (4563, "权限资源错误")
    INVALID_PERMISSION_ACTION = (4564, "权限操作错误")
    INVALID_PERMISSION_SCOPE = (4565, "权限范围错误")
    INVALID_PERMISSION_LEVEL = (4566, "权限级别错误")
    INVALID_PERMISSION_TYPE = (4567, "权限类型错误")
    INVALID_PERMISSION_STATUS = (4568, "权限状态错误")
    INVALID_PERMISSION_TIME = (4569, "权限时间错误")
    INVALID_PERMISSION_CONDITION = (4570, "权限条件错误")
    INVALID_PERMISSION_POLICY = (4571, "权限策略错误")
    INVALID_PERMISSION_RULE = (4572, "权限规则错误")
    INVALID_PERMISSION_EXCEPTION = (4573, "权限异常错误")
    INVALID_PERMISSION_VALIDATION = (4574, "权限验证错误")
    INVALID_PERMISSION_AUTHENTICATION = (4575, "权限认证错误")
    INVALID_PERMISSION_AUTHORIZATION = (4576, "权限授权错误")
    INVALID_PERMISSION_ACCESS = (4577, "权限访问错误")
    INVALID_PERMISSION_SECURITY = (4578, "权限安全错误")
    INVALID_PERMISSION_NETWORK = (4579, "权限网络错误")
    INVALID_PERMISSION_DATABASE = (4580, "权限数据库错误")
    INVALID_PERMISSION_CACHE = (4581, "权限缓存错误")
    INVALID_PERMISSION_QUEUE = (4582, "权限队列错误")
    INVALID_PERMISSION_LOCK = (4583, "权限锁错误")
    INVALID_PERMISSION_TRANSACTION = (4584, "权限事务错误")
    INVALID_PERMISSION_LOG = (4585, "权限日志错误")
    INVALID_PERMISSION_MONITORING = (4586, "权限监控错误")
    INVALID_PERMISSION_NOTIFICATION = (4587, "权限通知错误")
    INVALID_PERMISSION_SCHEDULING = (4588, "权限调度错误")
    INVALID_PERMISSION_TASK = (4589, "权限任务错误")
    INVALID_PERMISSION_JOB = (4590, "权限作业错误")
    INVALID_PERMISSION_WORKFLOW = (4591, "权限工作流错误")
    INVALID_PERMISSION_SCRIPT = (4592, "权限脚本错误")
    INVALID_PERMISSION_PLUGIN = (4593, "权限插件错误")
    INVALID_PERMISSION_MODULE = (4594, "权限模块错误")
    INVALID_PERMISSION_PACKAGE = (4595, "权限包错误")
    INVALID_PERMISSION_CLASS = (4596, "权限类错误")
    INVALID_PERMISSION_FUNCTION = (4597, "权限函数错误")
    INVALID_PERMISSION_METHOD = (4598, "权限方法错误")
    INVALID_PERMISSION_PROPERTY = (4599, "权限属性错误")
    INVALID_PERMISSION_VARIABLE = (4600, "权限变量错误")
    INVALID_PERMISSION_CONSTANT = (4601, "权限常量错误")
    INVALID_PERMISSION_ENUM = (4602, "权限枚举错误")
    INVALID_PERMISSION_INTERFACE = (4603, "权限接口错误")
    INVALID_PERMISSION_PROTOCOL = (4604, "权限协议错误")
    INVALID_PERMISSION_SERVICE = (4605, "权限服务错误")
    INVALID_PERMISSION_CLIENT = (4606, "权限客户端错误")
    INVALID_PERMISSION_SERVER = (4607, "权限服务器错误")
    INVALID_PERMISSION_SYSTEM = (4608, "权限系统错误")

    def __init__(self, code: int, msg: str):
        """
        初始化返回码
        
        :param code: 错误码
        :param msg: 错误信息
        """
        self._code = code
        self._msg = msg

    @property
    def code(self) -> int:
        """获取错误码"""
        return self._code

    @property
    def msg(self) -> str:
        """获取错误信息"""
        return self._msg


class CommonConstant:
    """
    常用常量
    """

    # 域名相关
    WWW = 'www.'
    HTTP = 'http://'
    HTTPS = 'https://'
    
    # 远程调用
    LOOKUP_RMI = 'rmi:'
    LOOKUP_LDAP = 'ldap:'
    LOOKUP_LDAPS = 'ldaps:'
    
    # 系统标识
    YES = 'Y'
    NO = 'N'
    
    # 部门状态
    DEPT_NORMAL = '0'  # 正常
    DEPT_DISABLE = '1' # 停用
    
    # 唯一性校验
    UNIQUE = True
    NOT_UNIQUE = False


class JobConstant:
    """
    定时任务常量

    JOB_ERROR_LIST: 定时任务禁止调用模块及违规字符串列表
    JOB_WHITE_LIST: 定时任务允许调用模块列表
    """

    JOB_ERROR_LIST = [
        'app',
        'config',
        'exceptions',
        'import ',
        'middlewares',
        'module_admin',
        'open(',
        'os.',
        'server',
        'sub_applications',
        'subprocess.',
        'sys.',
        'utils',
        'while ',
        '__import__',
        '"',
        "'",
        ',',
        '?',
        ':',
        ';',
        '/',
        '|',
        '+',
        '-',
        '=',
        '~',
        '!',
        '#',
        '$',
        '%',
        '^',
        '&',
        '*',
        '<',
        '>',
        '(',
        ')',
        '[',
        ']',
        '{',
        '}',
        ' ',
    ]
    JOB_WHITE_LIST = ['module_task']


# if __name__ == "__main__":
#     print(RET.OK.msg)  # 输出: 成功
