# -*- coding: utf-8 -*-

import random
import mimetypes
from datetime import datetime
from typing import List, Dict, Tuple
import aiofiles
from fastapi import UploadFile
from pathlib import Path

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import logger

class UploadUtil:
    """
    上传工具类
    """

    @staticmethod
    def generate_random_number() -> str:
        """生成3位数字构成的字符串"""
        return f'{random.randint(1, 999):03}'

    @staticmethod
    def check_file_exists(filepath: Path) -> bool:
        """检查文件是否存在"""
        return filepath.exists()

    @staticmethod
    def check_file_extension(file: UploadFile) -> bool:
        """检查文件后缀是否合法"""
        file_extension = mimetypes.guess_extension(file.content_type)
        return file_extension in settings.ALLOWED_EXTENSIONS if file_extension else False

    @staticmethod
    def check_file_timestamp(filename: str) -> bool:
        """校验文件时间戳是否合法"""
        try:
            name_parts = filename.rsplit('.', 1)[0].split('_')
            timestamp = name_parts[-1].split(settings.UPLOAD_MACHINE)[0]
            datetime.strptime(timestamp, '%Y%m%d%H%M%S')
            return True
        except (ValueError, IndexError):
            return False

    @staticmethod
    def check_file_machine(filename: str) -> bool:
        """校验文件机器码是否合法"""
        try:
            name_without_ext = filename.rsplit('.', 1)[0]
            return len(name_without_ext) >= 4 and name_without_ext[-4] == settings.UPLOAD_MACHINE
        except IndexError:
            return False

    @staticmethod
    def check_file_random_code(filename: str) -> bool:
        """校验文件随机码是否合法"""
        try:
            code = filename.rsplit('.', 1)[0][-3:]
            return code.isdigit() and 1 <= int(code) <= 999
        except IndexError:
            return False

    @staticmethod
    def check_file_size(file: UploadFile) -> bool:
        """校验文件大小是否合法"""
        return file.size <= settings.MAX_FILE_SIZE

    @classmethod
    def generate_file_name(cls, filename: str) -> str:
        """生成文件名称"""
        name, ext = filename.rsplit(".", 1)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f'{name}_{timestamp}{settings.UPLOAD_MACHINE}{cls.generate_random_number()}.{ext}'
    
    @staticmethod
    def generate_file(filepath: Path, chunk_size: int = 8192):
        """根据文件生成二进制数据"""
        with filepath.open('rb') as f:
            while chunk := f.read(chunk_size):
                yield chunk

    @staticmethod
    def delete_file(filepath: Path) -> bool:
        """
        删除文件
        :return: 删除是否成功
        """
        try:
            filepath.unlink(missing_ok=True)
            return True
        except OSError:
            return False
    
    @classmethod
    async def upload_file(cls, file: UploadFile) -> Tuple[str, Path]:
        """
        文件上传
        :param file: 上传的文件对象
        :raises CustomException: 当文件类型不支持或大小超限时抛出
        :return: (文件名, 文件路径)的元组
        """
        # 文件校验
        if not all([cls.check_file_extension(file), cls.check_file_size(file)]):
            raise CustomException(msg='文件类型或大小不合法')
            
        try:
            # 构建相对路径: content_type/年/月/日
            relative_path = Path(file.content_type).joinpath(datetime.now().strftime("%Y/%m/%d"))
            # 构建完整的目录路径
            dir_path = settings.UPLOAD_FILE_PATH.joinpath(relative_path)
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # 生成文件名并保存
            filename = cls.generate_file_name(file.filename)
            filepath = dir_path / filename

            # 分块写入文件
            chunk_size = 8 * 1024 * 1024  # 8MB chunks
            async with aiofiles.open(filepath, 'wb') as f:
                while chunk := await file.read(chunk_size):
                    await f.write(chunk)

            # 返回相对路径
            return filename, filepath
            
        except Exception as e:
            logger.error(f"文件上传失败: {e}")
            raise CustomException(msg='文件上传失败')

    @staticmethod
    def get_file_tree(file_path: str) -> List[Dict]:
        """
        获取文件树结构
        :param file_path: 文件路径
        :return: 文件树列表
        """
        return [item for item in Path(file_path).iterdir()]
