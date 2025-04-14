# mongo_curd.py
import datetime
import json
from typing import Any, List, Optional, Dict, Union
from bson import ObjectId
from bson.errors import InvalidId
from bson.json_util import dumps
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from app.core.exceptions import CustomException
from app.api.v1.schemas.system.operation_log_schema import OperationLogOutSchema

class MongoCURD:
    """
    MongoDB 数据库管理器
    """

    def __init__(
            self,
            db: AsyncIOMotorDatabase,
            collection: str,
            schema: Any = None
    ):
        """
        初始化 MongoDB CURD 类。

        :param db: 数据库连接
        :param collection: 集合名称
        :param schema: 序列化对象
        """
        self.db = db
        self.collection = db[collection]
        self.schema = schema

    async def get(self, _id: Optional[str] = None, **kwargs) -> Optional[Dict]:
        """
        获取单个数据，默认使用 ID 查询，否则使用关键词查询。

        :param _id: 数据 ID
        :param kwargs: 查询条件
        :return: 数据字典
        """
        try:
            if _id:
                kwargs["_id"] = ObjectId(_id)
            params = self.filter_condition(**kwargs)
            data = await self.collection.find_one(params)
            if not data:
                return None
            return jsonable_encoder(self.schema(**data)) if self.schema else data
        except InvalidId:
            raise CustomException(msg="无效的ID格式")
        except Exception as e:
            raise CustomException(msg=f"查询数据失败: {str(e)}")

    async def create(self, data: Union[Dict, Any]) -> InsertOneResult:
        """
        创建数据。

        :param data: 要创建的数据
        :return: 插入结果
        """
        try:
            if not isinstance(data, dict):
                data = jsonable_encoder(data)
            
            # 添加时间戳
            now = datetime.datetime.now()
            data.update({
                'created_at': now,
                'updated_at': now
            })
            
            result = await self.collection.insert_one(data)
            if not result.acknowledged:
                raise CustomException(msg="创建数据失败")
            return result
        except Exception as e:
            raise CustomException(msg=f"创建数据失败: {str(e)}")

    async def update(self, _id: str, data: Union[Dict, Any], upsert: bool = False) -> UpdateResult:
        """
        更新数据。

        :param _id: 数据 ID
        :param data: 要更新的数据
        :param upsert: 不存在是否插入
        :return: 更新结果
        """
        try:
            if not isinstance(data, dict):
                data = jsonable_encoder(data)
            
            # 更新时间戳
            data['updated_at'] = datetime.datetime.now()
            
            result = await self.collection.update_one(
                {'_id': ObjectId(_id)},
                {'$set': data},
                upsert=upsert
            )
            if result.matched_count == 0 and not upsert:
                raise CustomException(msg="更新失败，未找到对应数据")
            return result
        except InvalidId:
            raise CustomException(msg="无效的ID格式")
        except Exception as e:
            raise CustomException(msg=f"更新数据失败: {str(e)}")

    async def delete(self, _id: Union[str, List[str]]) -> DeleteResult:
        """
        删除数据，支持批量删除。

        :param _id: 单个ID或ID列表
        :return: 删除结果
        """
        try:
            if isinstance(_id, list):
                result = await self.collection.delete_many({'_id': {'$in': [ObjectId(i) for i in _id]}})
            else:
                result = await self.collection.delete_one({'_id': ObjectId(_id)})
            
            if result.deleted_count == 0:
                raise CustomException(msg="删除失败，未找到对应数据")
            return result
        except InvalidId:
            raise CustomException(msg="无效的ID格式")
        except Exception as e:
            raise CustomException(msg=f"删除数据失败: {str(e)}")

    async def list(
            self,
            page_no: Optional[int] = 1,
            page_size: Optional[int] = 10,
            order_by: Optional[List[Dict]] = None,
            **kwargs
    ) -> List[Dict]:
        """
        查询数据列表。

        :param page_no: 页码
        :param page_size: 每页数量
        :param order_by: 排序条件 [{'field': 'field_name', 'direction': 1}]
        :param kwargs: 查询条件
        :return: 数据列表
        """
        try:
            params = self.filter_condition(**kwargs)
            cursor = self.collection.find(params)

            # 排序处理
            if order_by:
                sort_conditions = [(item['field'], item['direction']) for item in order_by]
                cursor.sort(sort_conditions)

            # 分页处理
            if page_no and page_size:
                cursor.skip((page_no - 1) * page_size).limit(page_size)

            data_list = [json.loads(dumps(row)) async for row in cursor]
            return [jsonable_encoder(self.schema(**data)) for data in data_list] if self.schema else data_list
        except Exception as e:
            raise CustomException(msg=f"查询列表失败: {str(e)}")

    async def count(self, **kwargs) -> int:
        """
        获取数据总数。

        :param kwargs: 查询条件
        :return: 数据总数
        """
        try:
            params = self.filter_condition(**kwargs)
            return await self.collection.count_documents(params)
        except Exception as e:
            raise CustomException(msg=f"统计数据失败: {str(e)}")

    @staticmethod
    def filter_condition(**kwargs) -> Dict:
        """
        构建过滤条件。

        :param kwargs: 查询参数
        :return: 过滤条件字典
        """
        params = {}
        for k, v in kwargs.items():
            if not v:
                continue
            
            if isinstance(v, tuple):
                if v[0] == "like" and v[1]:
                    params[k] = {'$regex': v[1], '$options': 'i'}  # i表示不区分大小写
                elif v[0] == "between" and len(v[1]) == 2:
                    params[k] = {
                        '$gte': f"{v[1][0]} 00:00:00",
                        '$lt': f"{v[1][1]} 23:59:59"
                    }
                elif v[0] == "ObjectId" and v[1]:
                    try:
                        params[k] = ObjectId(v[1])
                    except InvalidId:
                        raise CustomException(msg="无效的ObjectId格式")
                elif v[0] == "in" and v[1]:
                    params[k] = {'$in': v[1]}
                elif v[0] == "gt":
                    params[k] = {'$gt': v[1]}
                elif v[0] == "gte":
                    params[k] = {'$gte': v[1]}
                elif v[0] == "lt":
                    params[k] = {'$lt': v[1]}
                elif v[0] == "lte":
                    params[k] = {'$lte': v[1]}
            else:
                params[k] = v
                
        return params


# class OperationRecordDal(MongoCURD):
#     """
#     操作记录数据访问层
#     """

#     def __init__(self, db: AsyncIOMotorDatabase):
#         """
#         初始化操作记录数据访问层。

#         :param db: 数据库连接
#         """
#         super().__init__(
#             db=db,
#             collection="system_operation_log",
#             schema=OperationLogOutSchema,
#         )

# 创建日志到mongodb(已测试成功，可以成功创建):暂时注释，是因为该中间保存日志到mongodb(已调试成功)，而我现在实现的是记录到mysql的log表
# if not settings.MONGO_DB_ENABLE:
#     return response
# document = OperationLogCreateSchema(
#     request_ip = request.client.host,
#     request_os = user_agent.os.family,
#     request_browser = user_agent.browser.family,
#     request_path = request.url.path,
#     request_method = request.method,
#     request_payload = oper_param,
#     response_code = response.status_code,
#     response_json = response_data.decode(),
#     description = route.name,
#     creator_id = creator_id
# )
# from app.core.mongo_curd import OperationRecordDal
# from app.core.dependencies import mongo_getter
# operation_record_dal = OperationRecordDal(db = await mongo_getter(request))
# await operation_record_dal.create(data=document.model_dump())