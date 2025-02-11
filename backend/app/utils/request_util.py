# -*- coding: utf-8 -*-

import requests

from app.core.exceptions import CustomException


class Requests:

    def __init__(self):
        """
        单例模式保证测试过程中使用的都是一个session对象
        """
        self.session = requests.Session()

    def send_request(self,
                     url: str,
                     method: str,
                     data_type: str,
                     headers: dict = None,
                     data: dict = None
                     ):
        """
        :param url: 请求url
        :param method: 请求方法
        :param data_type: 入参关键字， params(查询参数类型，明文传输，一般在url?参数名=参数值), data(一般用于form表单类型参数), json(一般用于json类型请求参数)
        :param headers: 请求头
        :param data: 参数数据，默认等于None
        :return: 返回res对象
        """
        res = None
        try:
            if data_type == 'params':
                res = self.session.request(
                    method=method,
                    url=url,
                    params=data,
                    headers=headers)
            elif data_type == 'data':
                res = self.session.request(
                    method=method,
                    url=url,
                    data=data,
                    headers=headers)
            elif data_type == 'json':
                res = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=headers)
            elif data_type == 'file':
                res = self.session.request(
                    method=method,
                    url=url,
                    files=data,
                    headers=headers)
            else:
                raise CustomException(msg='parametric_key为params、json、data、file, 不支持其他类型')
            
            response_dicts = dict()
            # 响应状态码
            response_dicts['code'] = int(res.status_code)
            # 响应body
            response_dicts['body'] = str(res.json())
            # 响应秒时间
            response_dicts['time_total'] = res.elapsed.total_seconds()  # 秒为单位
        except Exception as e:
            raise CustomException(msg=f"发送请求异常:{e}")
        return response_dicts

