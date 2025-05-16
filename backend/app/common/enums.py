from enum import Enum, unique
from typing import Dict

@unique
class EnvironmentEnum(str, Enum):
    DEV = "dev"
    PROD = "prod"


@unique
class BusinessType(Enum):
    """业务操作类型枚举"""
    GET = 0   # 查询
    CREATE = 1   # 新增
    UPDATE = 2   # 修改
    DELETE = 3   # 删除
    GRANT = 4    # 授权
    EXPORT = 5   # 导出
    IMPORT = 6   # 导入
    FORCE = 7    # 强退



@unique
class RedisInitKeyConfig(Enum):
    """系统内置Redis键名枚举"""

    ACCESS_TOKEN = {'key': 'access_token', 'remark': '登录令牌信息'}
    REFRESH_TOKEN = {'key': 'refresh_token', 'remark': '刷新令牌信息'}
    CAPTCHA_CODES = {'key': 'captcha_codes', 'remark': '图片验证码'}
    ONLINE_USER = {'key': 'online_user', 'remark': '在线用户信息'}
    System_Config = {'key': 'system_config', 'remark': '系统配置'}
    System_Dict = {'key': 'system_dict', 'remark': '数据字典'}
    
    @property
    def key(self) -> str:
        """获取Redis键名"""
        return self.value.get('key')

    @property 
    def remark(self) -> str:
        """获取Redis键名说明"""
        return self.value.get('remark')
