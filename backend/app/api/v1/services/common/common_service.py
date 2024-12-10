# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, List
from fastapi import BackgroundTasks, Request, UploadFile

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.api.v1.schemas.common.common_schema import UploadResponseSchema, FileListResponseSchema
from app.utils.upload_util import UploadUtil


class CommonService:
    """通用模块服务层"""

    @classmethod
    async def get_file_list_services(cls, request: Request) -> List[Dict]:
        """获取文件列表service"""
        file_list_tree = UploadUtil.get_file_tree(settings.STATIC_ROOT)
        file_list = []
        for item in file_list_tree:
            file_list.append(FileListResponseSchema(
                name=item.name,
                type='directory' if item.is_dir() else 'file',
                size=item.stat().st_size if item.is_file() else None,
                modified_time=datetime.fromtimestamp(item.stat().st_mtime).isoformat()
            ).model_dump())
        return file_list
    
    @classmethod
    async def upload_service(cls, request: Request, file: UploadFile) -> Dict:
        """
        通用上传service
        :param request: Request对象
        :param file: 上传文件对象
        :return: 上传结果字典
        """
        filename, filepath = await UploadUtil.upload_file(file)
        
        return UploadResponseSchema(
            file_path=f'{filepath}',
            file_name=filename,
            origin_name=file.filename,
            file_url=f'{request.base_url}{filepath}',
        ).model_dump()

    @classmethod
    async def download_services(cls, file_name: str) -> Generator:
        """
        下载下载目录文件service

        :param background_tasks: 后台任务对象
        :param file_name: 下载的文件名称
        :param delete: 是否在下载完成后删除文件
        :return: 文件二进制流
        """
        if '..' in file_name:
            raise CustomException(msg='文件名称不合法')
            
        filepath = settings.DOWNLOAD_FILE_PATH.joinpath(file_name)
        if not UploadUtil.check_file_exists(filepath):
            raise CustomException(msg='文件不存在')
            
        return UploadUtil.generate_file(filepath)

    @classmethod
    async def download_resource_services(cls, resource: str) -> Generator:
        """
        下载上传目录文件service
        :param resource: 下载的文件路径
        :return: 文件二进制流
        """
        filepath = Path(resource).joinpath(settings.UPLOAD_FILE_PATH)
        filename = filepath.name

        if '..' in filename:
            raise CustomException(msg='文件名称不合法')
            
        if not all([
            UploadUtil.check_file_timestamp(filename),
            UploadUtil.check_file_machine(filename),
            UploadUtil.check_file_random_code(filename)
        ]):
            raise CustomException(msg='文件名称不合法')
            
        if not UploadUtil.check_file_exists(filepath):
            raise CustomException(msg='文件不存在')
            
        return UploadUtil.generate_file(filepath)
