# -*- coding: utf-8 -*-

import re
import requests

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
    def get_ip_location(cls, ip: str) -> str:
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
        if ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
            return '内网IP'
            
        try:
            # 优先使用百度API
            ip_result = requests.get(
                f'https://qifu-api.baidubce.com/ip/geo/v1/district?ip={ip}',
                timeout=5
            )
            if ip_result.status_code == 200:
                data = ip_result.json().get('data', {})
                prov = data.get('prov', '')
                city = data.get('city', '')
                if prov or city:
                    return f'{prov}-{city}'
                    
            # 备用淘宝API
            response = requests.get(
                f"http://ip.taobao.com/service/getIpInfo.php?ip={ip}",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json().get('data', {})
                country = data.get('country', '')
                region = data.get('region', '') 
                city = data.get('city', '')
                return f"{country}{region}{city}"
                
        except Exception as e:
            logger.error(f"获取IP归属地失败: {e}")
            
        return "未知"