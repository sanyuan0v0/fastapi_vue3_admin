# -*- coding: utf-8 -*-

import io
from typing import Dict
from fastapi import UploadFile

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.base_schema import UploadResponseSchema, DownloadFileSchema
from app.core.logger import logger
from app.utils.excel_util import ExcelUtil
from app.utils.upload_util import UploadUtil

class FileService:
    """
    文件管理服务层
    """

    @classmethod
    async def upload_service(cls, base_url: str, file: UploadFile) -> Dict:
        """ 上传文件"""
        if not file:
            raise CustomException(msg="请选择要上传的文件")
        filename, filepath, file_url = await UploadUtil.upload_file(file=file, base_url=base_url)
        
        return UploadResponseSchema(
            file_path=f'{filepath}',
            file_name=filename,
            origin_name=file.filename,
            file_url=f'{file_url}',
        ).model_dump()
        

    @classmethod
    async def download_service(cls, file_path: str) -> DownloadFileSchema:
        """下载文件"""
        if not file_path:
            raise CustomException(msg="请选择要下载的文件")
        
        file_name = UploadUtil.download_file(file_path)

        return DownloadFileSchema(
            file_path=file_path,
            file_name=file_name,
        )