# -*- coding: utf-8 -*-

from fastapi import Request

from app.common.enums import RedisInitKeyConfig
from app.api.v1.schemas.monitor.cache_schema import CacheMonitorSchema, CacheInfoSchema
from app.core.cache_crud import Cache

class CacheService:
    """
    缓存监控模块服务层
    """

    @classmethod
    async def get_cache_monitor_statistical_info_services(cls, request: Request)->dict:
        """
        获取缓存监控信息service

        :param request: Request对象
        :return: 缓存监控信息
        """
        info = await Cache(request).info()
        db_size = await Cache(request).db_size()
        command_stats_dict = await Cache(request).commandstats()

        command_stats = [
            dict(name=key.split('_')[1], value=str(value.get('calls'))) for key, value in command_stats_dict.items()
        ]
        result = CacheMonitorSchema(command_stats=command_stats, db_size=db_size, info=info)

        return result.model_dump()

    @classmethod
    async def get_cache_monitor_cache_name_services(cls)->list:
        """
        获取缓存名称列表信息service

        :return: 缓存名称列表信息
        """
        name_list = []
        for key_config in RedisInitKeyConfig:
            name_list.append(
                CacheInfoSchema(
                    cache_key='',
                    cache_name=key_config.key,
                    cache_value='',
                    remark=key_config.remark,
                ).model_dump()
            )

        return name_list

    @classmethod
    async def get_cache_monitor_cache_key_services(cls, request: Request, cache_name: str)->list:
        """
        获取缓存键名列表信息service

        :param request: Request对象
        :param cache_name: 缓存名称
        :return: 缓存键名列表信息
        """
        cache_keys = await Cache(request).get_keys(f'{cache_name}*')
        cache_key_list = [key.split(':', 1)[1] for key in cache_keys if key.startswith(f'{cache_name}:')]

        return cache_key_list

    @classmethod
    async def get_cache_monitor_cache_value_services(cls, request: Request, cache_name: str, cache_key: str)->dict:
        """
        获取缓存内容信息service

        :param request: Request对象
        :param cache_name: 缓存名称
        :param cache_key: 缓存键名
        :return: 缓存内容信息
        """
        cache_value = await Cache(request).get(f'{cache_name}:{cache_key}')

        return CacheInfoSchema(cache_key=cache_key, cache_name=cache_name, cache_value=cache_value, remark='').model_dump()

    @classmethod
    async def clear_cache_monitor_cache_name_services(cls, request: Request, cache_name: str)->bool:
        """
        清除缓存名称对应所有键值service

        :param request: Request对象
        :param cache_name: 缓存名称
        :return: 操作缓存响应信息
        """
        cache_keys = await Cache(request).get_keys(f'{cache_name}*')
        if cache_keys:
            await Cache(request).delete(*cache_keys)

        return True

    @classmethod
    async def clear_cache_monitor_cache_key_services(cls, request: Request, cache_key: str)->bool:
        """
        清除缓存名称对应所有键值service

        :param request: Request对象
        :param cache_key: 缓存键名
        :return: 操作缓存响应信息
        """
        cache_keys = await Cache(request).get_keys(f'*{cache_key}')
        if cache_keys:
            await Cache(request).delete(*cache_keys)

        return True

    @classmethod
    async def clear_cache_monitor_all_services(cls, request: Request)->bool:
        """
        清除所有缓存service

        :param request: Request对象
        :return: 操作缓存响应信息
        """
        cache_keys = await Cache(request).get_keys
        if cache_keys:
            await Cache(request).delete(*cache_keys)

        return True
