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
        
        logger.info(f"获取IP归属地: {ip}")

        # 内网IP直接返回
        if ip == '127.0.0.1' or ip == 'localhost':
            return '内网IP'
            
        try:
            # 优先使用百度API
            ip_result = requests.get(
                f'https://qifu-api.baidubce.com/ip/geo/v1/district?ip={ip}',
                timeout=5
            )
            if ip_result.status_code == 200:
                
                data = ip_result.json().get('data', {})
                # "continent": "亚洲",
                # "country": "中国",
                # "zipcode": "710061",
                # "owner": "中国移动",
                # "isp": "中国移动",
                # "adcode": "610113",
                # "prov": "陕西省",
                # "city": "西安市",
                # "district": "雁塔区"
                country = data.get('country', '未知国家')
                owner = data.get('owner', '未知运营商')
                prov = data.get('prov', '未知省份')
                city = data.get('city', '未知城市')
                district = data.get('district', '未知地区')

                return f'【{owner}】-{country}-{prov}-{city}-{district}'

        except Exception as e:
            logger.error(f"获取IP归属地失败: {e}")
            return "未知"
