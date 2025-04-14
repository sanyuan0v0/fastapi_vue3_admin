# -*- coding: utf-8 -*-

import json
from typing import Dict, List
from aioredis import Redis

from app.common.enums import RedisInitKeyConfig
from app.core.exceptions import CustomException
from app.api.v1.params.monitor.online_param import OnlineQueryParams
from app.api.v1.schemas.monitor.online_schema import OnlineOutSchema
from app.core.redis_crud import RedisCURD

class OnlineService:
    """在线用户管理模块服务层"""

    @classmethod
    async def get_online_list_service(cls, redis: Redis, search: OnlineQueryParams) -> List[Dict]:
        """获取在线用户列表信息"""
        # 获取所有在线用户信息
        token_keys = await RedisCURD(redis).get_keys(f'{RedisInitKeyConfig.ONLINE_USER.key}*')
        if not token_keys:
            return []
            
        # 批量获取在线用户信息
        online_values = await RedisCURD(redis).mget(*token_keys)
        online_list = []
        
        for online_value in online_values:
            # 将字符串解析为字典
            online_data = json.loads(online_value)
            online_info = OnlineOutSchema(
                session_id=online_data['session_id'],
                user_id=online_data['user_id'],
                name=online_data['name'], 
                user_name=online_data['user_name'], 
                ipaddr=online_data['ipaddr'],
                login_location=online_data['login_location'],
                os=online_data['os'],
                browser=online_data['browser'],
                login_time=online_data['login_time']
            ).model_dump(mode='json')  # 添加mode='json'参数以序列化datetime
            
            if cls._match_search_conditions(online_info, search):
                online_list.append(online_info)
        
        return online_list

    @classmethod
    async def delete_online_service(cls, redis: Redis, username: str) -> bool:
        """强制下线在线用户"""
        if not username:
            raise CustomException(msg='传入username不能为空')
            
        # 批量删除token

        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.ONLINE_USER.key}:{username}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{username}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{username}")
        return True
    
    @staticmethod
    def _match_search_conditions(online_info: Dict, search: OnlineQueryParams) -> bool:
        """检查是否匹配搜索条件"""
        # 根据params中的定义,需要进行模糊匹配
        if search.name:
            search_name = search.name[1].strip('%')  # 去掉like和%
            if search_name not in online_info['name']:
                return False
                
        if search.login_location:
            search_location = search.login_location[1].strip('%')
            if search_location not in online_info['login_location']:
                return False
                
        # ipaddr是精确匹配
        if search.ipaddr:
            if online_info['ipaddr'] != search.ipaddr[1]:  # 取eq后面的值
                return False
                
        return True
