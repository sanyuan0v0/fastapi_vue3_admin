# -*- coding: utf-8 -*-

import re
import requests
import httpx

from app.core.logger import logger


class IpLocalUtil:
    """
    获取IP归属地工具类
    """
    
    @classmethod
    def is_valid_ip(cls, ip: str) -> bool:
        """
        校验IP格式是否合法
        
        :param ip: IP地址
        :return: 是否合法
        """
        ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(ip_pattern, ip))

    @classmethod
    async def get_ip_location(cls, ip: str) -> str:
        """
        获取IP归属地信息
        
        :param ip: IP地址
        :return: IP归属地信息
        """
        # 校验IP格式
        if not cls.is_valid_ip(ip):
            logger.error(f"IP格式不合法: {ip}")
            return "未知"
        
        logger.info(f"获取IP归属地: {ip}, 类型: {type(ip)}")

        # 内网IP直接返回
        if ip == '127.0.0.1' or ip == 'localhost':
            return '内网IP'
            
        try:
            # 百度API失败，使用其他API
            # async with httpx.AsyncClient() as client:
            #     response = await client.get(
            #         f'https://qifu-api.baidubce.com/ip/geo/v1/district?ip={ip}',
            #         timeout=5
            #     )
            #     if response.status_code == 200:
            #         data = response.json().get('data', {})
            #         return f"【{data.get('owner','')}】-{data.get('country','')}-{data.get('prov','')}-{data.get('city','')}-{data.get('district','')}"

            # 使用ip-api.com API获取IP归属地信息
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'http://ip-api.com/json/{ip}?lang=zh-CN',
                    timeout=10
                )
                if response.status_code == 200:
                    result = response.json()
                    return f"{result.get('country','')}-{result.get('regionName','')}-{result.get('city','')}"

        except Exception as e:
            logger.error(f"获取IP归属地失败: {e}")
            return "未知"
