# -*- coding: utf-8 -*-

from typing import List
from app.common.constant import CommonConstant


class StringUtil:
    """
    字符串工具类
    """

    @classmethod
    def is_blank(cls, string: str) -> bool:
        """
        校验字符串是否为''或全空格

        :param string: 需要校验的字符串
        :return: 校验结果
        """
        if string is None:
            return True
        return not bool(string.strip())

    @classmethod
    def is_empty(cls, string) -> bool:
        """
        校验字符串是否为''或None

        :param string: 需要校验的字符串
        :return: 校验结果
        """
        return not bool(string)

    @classmethod
    def is_http(cls, link: str) -> bool:
        """
        判断是否为http(s)://开头

        :param link: 链接
        :return: 是否为http(s)://开头
        """
        if not link:
            return False
        return link.lower().startswith((CommonConstant.HTTP.lower(), CommonConstant.HTTPS.lower()))

    @classmethod
    def contains_ignore_case(cls, search_str: str, compare_str: str) -> bool:
        """
        查找指定字符串是否包含指定字符串同时串忽略大小写

        :param search_str: 查找的字符串
        :param compare_str: 比对的字符串
        :return: 查找结果
        """
        if not (search_str and compare_str):
            return False
        return compare_str.lower() in search_str.lower()

    @classmethod
    def contains_any_ignore_case(cls, search_str: str, compare_str_list: List[str]) -> bool:
        """
        查找指定字符串是否包含指定字符串列表中的任意一个字符串同时串忽略大小写

        :param search_str: 查找的字符串
        :param compare_str_list: 比对的字符串列表
        :return: 查找结果
        """
        if not (search_str and compare_str_list):
            return False
        search_str_lower = search_str.lower()
        return any(comp_str.lower() in search_str_lower for comp_str in compare_str_list if comp_str)

    @classmethod
    def startswith_case(cls, search_str: str, compare_str: str) -> bool:
        """
        查找指定字符串是否以指定字符串开头

        :param search_str: 查找的字符串
        :param compare_str: 比对的字符串
        :return: 查找结果
        """
        if not (search_str and compare_str):
            return False
        return search_str.startswith(compare_str)

    @classmethod
    def startswith_any_case(cls, search_str: str, compare_str_list: List[str]) -> bool:
        """
        查找指定字符串是否以指定字符串列表中的任意一个字符串开头

        :param search_str: 查找的字符串
        :param compare_str_list: 比对的字符串列表
        :return: 查找结果
        """
        if not (search_str and compare_str_list):
            return False
        return any(search_str.startswith(comp_str) for comp_str in compare_str_list if comp_str)
