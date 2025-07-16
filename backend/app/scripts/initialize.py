# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Dict, List
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.base_model import ModelBase
from app.core.logger import logger
from app.config.setting import settings
from app.api.v1.models.system import (
    user_model,
    dept_model,
    role_model,
    menu_model,
    position_model,
    operation_log_model,
    notice_model,
    config_model,
    dict_model,
)
from app.api.v1.models.monitor import (
    job_model
)

class InitializeData:
    """
    初始化数据库和基础数据
    """

    def __init__(self) -> None:
        self.prepare_init_models = [
            dept_model.DeptModel,
            menu_model.MenuModel,
            user_model.UserModel,
            position_model.PositionModel,
            user_model.UserPositionsModel,
            role_model.RoleModel,
            user_model.UserRolesModel,
            role_model.RoleDeptsModel,
            role_model.RoleMenusModel,
            notice_model.NoticeModel,
            config_model.ConfigModel,
            operation_log_model.OperationLogModel,
            dict_model.DictTypeModel,
            dict_model.DictDataModel,
            job_model.JobModel,
        ]
        self.created_tables = set()
    async def __get_existing_tables(self, db: AsyncSession) -> List[str]:
        return await db.run_sync(
            lambda sync_db: inspect(sync_db.get_bind()).get_table_names()
        )

    async def __init_model(self, db: AsyncSession) -> None:
        """初始化数据库表结构"""
        try:
            # 获取所有模型元数据
            metadata = ModelBase.metadata
            

            # 只创建不存在的表
            for table in metadata.sorted_tables:
                if table.name not in await self.__get_existing_tables(db):
                    await db.run_sync(lambda sync_db: table.create(sync_db.bind))
                    self.created_tables.add(table.name)
                    logger.info(f"已创建表: {table.name}")

            await self.__init_data(db)
        except Exception as e:
            logger.error(f"初始化数据库结构失败: {str(e)}")
            raise

    async def __init_data(self, db: AsyncSession) -> None:
        """初始化基础数据"""
        for model in self.prepare_init_models:
            table_name = model.__tablename__
            # 如果表不是本次新建的，跳过初始化
            if table_name not in self.created_tables:
                logger.warning(f"跳过 {table_name} 表数据初始化（表已存在）")
                continue

            data = await self.__get_data(table_name)
            if not data:
                logger.warning(f"跳过 {table_name} 表，无初始化数据")
                continue
            
            try:
                # 新建的表一定为空，无需查主键去重，直接插入全部数据
                objs = [model(**item) for item in data]
                db.add_all(objs)
                await db.flush()
                logger.info(f"已向 {table_name} 表写入 {len(objs)} 条记录")

            except Exception as e:
                logger.error(f"初始化 {table_name} 表数据失败: {str(e)}")
                raise


    async def __get_data(self, filename: str) -> List[Dict]:
        """读取初始化数据文件"""
        json_path = Path.joinpath(settings.SCRIPT_DIR, f'{filename}.json')
        if not json_path.exists():
            return []

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.loads(f.read())
        except json.JSONDecodeError as e:
            logger.error(f"解析 {json_path} 失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"读取 {json_path} 失败: {str(e)}")
            raise

    async def init_db(self, db: AsyncSession) -> None:
        """
        执行完整初始化流程
        """
        await self.__init_model(db)

