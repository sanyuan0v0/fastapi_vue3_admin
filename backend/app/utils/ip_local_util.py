# -*- coding: utf-8 -*-

import re
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
    def is_private_ip(cls, ip: str) -> bool:
        """
        校验IP是否为内网IP
        
        :param ip: IP地址
        :return: 是否为内网IP
        """
        ip_parts = list(map(int, ip.split('.')))
        
        # 检查是否为 10.0.0.0/8
        if ip_parts[0] == 10:
            return True
        
        # 检查是否为 172.16.0.0/12
        if ip_parts[0] == 172 and 16 <= ip_parts[1] <= 31:
            return True
        
        # 检查是否为 192.168.0.0/16
        if ip_parts[0] == 192 and ip_parts[1] == 168:
            return True
        
        # 检查是否为 127.0.0.0/8
        if ip_parts[0] == 127:
            return True
        
        return False

    @classmethod
    async def _make_api_request(cls, client, url):
        """
        单独的 API 请求方法，包含重试机制
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await client.get(url, timeout=10)
                if response.status_code == 200:
                    return response
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                logger.error(f"请求 {url} 失败: {e}")
        return None

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
        
        # 内网IP直接返回
        if cls.is_private_ip(ip):
            return '内网IP'
            
        try:
            # 使用ip-api.com API获取IP归属地信息
            async with httpx.AsyncClient() as client:
                # 尝试使用 ip9.com.cn API
                url = f'https://ip9.com.cn/get?ip={ip}'
                response = await cls._make_api_request(client, url)
                if response and response.json().get('ret') == 200:
                    result = response.json().get('data', {})
                    return f"{result.get('country','')}-{result.get('prov','')}-{result.get('city','')}-{result.get('area','')}-{result.get('isp','')}"

                # 尝试使用百度 API
                url = f'https://qifu-api.baidubce.com/ip/geo/v1/district?ip={ip}'
                response = await cls._make_api_request(client, url)
                if response and response.json().get('code') == "Success":
                    data = response.json().get('data', {})
                    # 修正原代码中的格式错误
                    return f"{data.get('country','')}-{data.get('prov','')}-{data.get('city','')}-{data.get('district','')}-{data.get('isp','')}"

        except Exception as e:
            logger.error(f"获取IP归属地失败: {e}")
            return "未知"
