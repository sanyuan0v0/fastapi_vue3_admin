# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Dict, List

from app.core.logger import logger
from app.config.setting import settings
from app.core.base_model import ModelBase
from app.core.database import async_engine, async_session
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
    job_model
)

class InitializeData:
    """
    初始化数据库和基础数据
    """

    def __init__(self) -> None:
        self.engine = async_engine
        self.session = async_session()
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

    async def __init_model(self) -> None:
        """初始化数据库表结构"""
        try:
            async with self.engine.begin() as conn:
                # 使用事务确保原子性
                await conn.run_sync(ModelBase.metadata.drop_all)
                logger.info("已清空所有表结构")
                await conn.run_sync(ModelBase.metadata.create_all)
                logger.info("已重新创建所有表结构")
        except Exception as e:
            logger.error(f"初始化数据库表结构失败: {str(e)}")
            raise

    async def __init_data(self) -> None:
        """初始化基础数据"""
        try:
            async with self.session as session:
                logger.info("开始初始化基础数据...")
                # for model in ModelBase.__subclasses__():
                for model in self.prepare_init_models:
                    table_name = model.__tablename__
                    data = self.__get_data(table_name)
                    if not data:
                        logger.info(f"跳过 {table_name} 表,无初始化数据")
                        continue

                    try:
                        async with session.begin():
                            objs = [model(**item) for item in data]
                            session.add_all(objs)
                            await session.flush()  # 立即刷新以检查约束
                            logger.info(f"已向 {table_name} 表写入 {len(objs)} 条记录")
                    except Exception as e:
                        logger.error(f"初始化 {table_name} 表数据失败: {str(e)}")
                        raise

                logger.info("基础数据初始化完成")
        except Exception as e:
            logger.error(f"初始化基础数据失败: {str(e)}")
            raise

    def __get_data(self, filename: str) -> List[Dict]:
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

    async def run(self) -> None:
        """
        执行完整初始化流程
        """
        logger.info("开始执行数据库初始化...")
        await self.__init_model()
        await self.__init_data()
        logger.info("数据库初始化完成")
