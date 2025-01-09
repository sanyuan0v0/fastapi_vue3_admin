# -*- coding: utf-8 -*-

import json
from typing import Dict, List
from fastapi import Request

from app.common.enums import RedisInitKeyConfig
from app.core.exceptions import CustomException
from app.api.v1.params.monitor.online_param import OnlineQueryParams
from app.api.v1.schemas.monitor.online_schema import OnlineOutSchema
from app.core.cache_crud import Cache

class OnlineService:
    """在线用户管理模块服务层"""

    @classmethod
    async def get_online_list(cls, request: Request, search: OnlineQueryParams) -> List[Dict]:
        """获取在线用户列表信息"""
        # 获取所有在线用户信息
        token_keys = await Cache(request.app.state.redis).get_keys(f'{RedisInitKeyConfig.ONLINE_USER.key}*')
        if not token_keys:
            return []
            
        # 批量获取在线用户信息
        online_values = await Cache(request.app.state.redis).mget(*token_keys)
        online_list = []
        
        for online_value in online_values:
            # 将字符串解析为字典
            online_data = json.loads(online_value)
            online_info = OnlineOutSchema(
                session_id=online_data['session_id'],
                user_id=online_data['user_id'],
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
    async def delete_online(cls, request: Request, ids: str) -> bool:
        """强制下线在线用户"""
        if not ids:
            raise CustomException(msg='传入ids不能为空')
            
        # 批量删除token
        token_ids = ids.split(',')
        for token_id in token_ids:
            await Cache(request.app.state.redis).delete(f"{RedisInitKeyConfig.ONLINE_USER.key}:{token_id}")
            await Cache(request.app.state.redis).delete(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{token_id}")
        return True
    
    @staticmethod
    def _match_search_conditions(online_info: Dict, search: OnlineQueryParams) -> bool:
        """检查是否匹配搜索条件"""
        # 根据params中的定义,需要进行模糊匹配
        if search.user_name:
            search_name = search.user_name[1].strip('%')  # 去掉like和%
            if search_name not in online_info['user_name']:
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
