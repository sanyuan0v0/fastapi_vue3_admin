# -*- coding: utf-8 -*-

from passlib.context import CryptContext
from typing import Optional

# 密码加密配置
PwdContext = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # 设置加密轮数,增加安全性
)


class PwdUtil:
    """
    密码工具类,提供密码加密和验证功能
    """

    @classmethod
    def verify_password(cls, plain_password: str, password_hash: str) -> bool:
        """
        校验密码是否匹配

        Args:
            plain_password: 明文密码
            password_hash: 加密后的密码哈希值

        Returns:
            bool: 密码是否匹配
        """
        return PwdContext.verify(plain_password, password_hash)

    @classmethod 
    def set_password_hash(cls, password: str) -> str:
        """
        对密码进行加密

        Args:
            password: 明文密码

        Returns:
            str: 加密后的密码哈希值
        """
        return PwdContext.hash(password)

    @classmethod
    def check_password_strength(cls, password: str) -> Optional[str]:
        """
        检查密码强度

        Args:
            password: 明文密码

        Returns:
            str: 如果密码强度不够返回提示信息,否则返回None
        """
        if len(password) < 6:
            return "密码长度至少6位"
        if not any(c.isupper() for c in password):
            return "密码需要包含大写字母"
        if not any(c.islower() for c in password):
            return "密码需要包含小写字母" 
        if not any(c.isdigit() for c in password):
            return "密码需要包含数字"
        return None
