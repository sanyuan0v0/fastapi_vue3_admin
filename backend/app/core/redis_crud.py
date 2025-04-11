# -*- coding: utf-8 -*-

import pickle
from typing import Any, Optional
from aioredis import Redis

from app.core.logger import logger


class RedisCURD:
    """缓存工具类"""

    def __init__(self, redis: Redis):
        """初始化"""
        self.redis = redis
        
    async def mget(self, *keys: list)-> list:
        """批量获取缓存
        
        Args:
            *keys: 可变参数,接收多个键名
            
        Returns:
            list: 返回缓存值列表
        """
        try:
            data = await self.redis.mget(keys)
            return data
        except Exception as e:
            logger.error(f"批量获取缓存失败: {str(e)}")
            return []
    
    async def get_keys(self, pattern: str = "*") -> list:
        """获取缓存键名"""
        try:
            keys = await self.redis.keys(f"{pattern}")
            return keys
        except Exception as e:
            logger.error(f"获取缓存键名失败: {str(e)}")
            return []
        
    
    async def get(self, key: str) -> Any:
        """获取缓存"""
        try:
            data = await self.redis.get(f"{key}")
            
            if data is None:
                return None

            return data

        except Exception as e:
            logger.error(f"获取缓存失败: {str(e)}")
            return None

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """设置缓存"""
        try:
            if expire is None:
                expire = 300
                
            # 根据数据类型选择序列化方式
            if isinstance(value, (int, float, str)):
                data = str(value).encode('utf-8')
            else:
                try:
                    data = pickle.dumps(value)
                except Exception as e:
                    logger.error(f"序列化数据失败: {str(e)}")
                    return False
                    
            await self.redis.set(
                name = key,
                value = data,
                ex=expire
            )
            return True
            
        except Exception as e:
            logger.error(f"设置缓存失败: {str(e)}")
            return False

    async def delete(self, *keys: str) -> bool:
        """删除缓存"""
        try:
            await self.redis.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"删除缓存失败: {str(e)}")
            return False

    async def clear(self, pattern: str = "*") -> bool:
        """清空缓存"""
        try:
            keys = await self.redis.keys(f"{pattern}")
            if keys:
                await self.redis.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"清空缓存失败: {str(e)}")
            return False

    async def exists(self, key: str) -> bool:
        """判断缓存是否存在"""
        try:
            return await self.redis.exists(f"{key}")
        except Exception as e:
            logger.error(f"判断缓存是否存在失败: {str(e)}")
            return False

    async def ttl(self, key: str) -> int:
        """获取缓存过期时间"""
        try:
            return await self.redis.ttl(f"{key}")
        except Exception as e:
            logger.error(f"获取缓存过期时间失败: {str(e)}")
            return -1

    async def expire(self, key: str, expire: int) -> bool:
        """设置缓存过期时间"""
        try:
            return await self.redis.expire(f"{key}", expire)
        except Exception as e:
            logger.error(f"设置缓存过期时间失败: {str(e)}")
            return False
    
    async def info(self) -> dict:
        """获取缓存信息"""
        try:
            return await self.redis.info()
        except Exception as e:
            logger.error(f"获取缓存信息失败: {str(e)}")
            return {}
        
    async def db_size(self) -> int:
        """获取数据库大小"""
        try:
            return await self.redis.dbsize()
        except Exception as e:
            logger.error(f"获取数据库大小失败: {str(e)}")
            return 0
    async def commandstats(self):
        """获取命令统计信息"""
        try:
            return await self.redis.info("commandstats")
        except Exception as e:
            logger.error(f"获取命令统计信息失败: {str(e)}")
            return {}