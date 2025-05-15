# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.cruds.system.dept_crud import DeptCRUD
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.dept_schema import (
    DeptCreateSchema,
    DeptUpdateSchema,
    DeptOutSchema
)
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.common_util import (
    get_parent_id_map,
    get_parent_recursion,
    get_child_id_map,
    get_child_recursion
)
from app.api.v1.params.system.dept_param import DeptQueryParams


class DeptService:
    """
    部门管理模块服务层
    """

    @classmethod
    async def get_dept_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """
        获取部门详情service
        
        :param auth: 认证对象
        :param id: 部门ID
        :return: 部门详情对象
        """
        dept = await DeptCRUD(auth).get_by_id_crud(id=id)
        return DeptOutSchema.model_validate(dept).model_dump()

    @classmethod
    async def get_dept_list_service(cls, auth: AuthSchema, search: DeptQueryParams, order_by: List[Dict] = None) -> List[Dict]:
        """
        获取部门列表service
        
        :param auth: 认证对象
        :param search: 查询参数对象
        :param order_by: 排序参数
        :return: 部门列表对象
        """
        if order_by:
            order_by = eval(order_by)
        else:
            order_by = [{"order": "asc"}]
        dept_list = await DeptCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [DeptOutSchema.model_validate(dept).model_dump() for dept in dept_list]

    @classmethod
    async def create_dept_service(cls, auth: AuthSchema, data: DeptCreateSchema) -> Dict:
        """
        创建部门service
        
        :param auth: 认证对象
        :param data: 部门创建对象
        :return: 新创建的部门对象
        """
        dept = await DeptCRUD(auth).get(name=data.name)
        if dept:
            raise CustomException(msg='创建失败，该部门已存在')
        dept = await DeptCRUD(auth).create(data=data)
        return DeptOutSchema.model_validate(dept).model_dump()

    @classmethod
    async def update_dept_service(cls, auth: AuthSchema, data: DeptUpdateSchema) -> Dict:
        """
        更新部门service
        
        :param auth: 认证对象
        :param data: 部门更新对象
        :return: 更新后的部门对象
        """
        dept = await DeptCRUD(auth).get_by_id_crud(id=data.id)
        if not dept:
            raise CustomException(msg='更新失败，该部门不存在')
        exist_dept = await DeptCRUD(auth).get(name=data.name)
        if exist_dept and exist_dept.id != data.id:
            raise CustomException(msg='更新失败，部门名称重复')
        dept = await DeptCRUD(auth).update(id=data.id, data=data)
        if data.available:
            await cls.batch_set_available_service(auth=auth, data=BatchSetAvailable(ids=[data.id], available=True))
        else:
            await cls.batch_set_available_service(auth=auth, data=BatchSetAvailable(ids=[data.id], available=False))
        return DeptOutSchema.model_validate(dept).model_dump()

    @classmethod
    async def delete_dept_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除部门service
        
        :param auth: 认证对象
        :param id: 部门ID
        """
        dept = await DeptCRUD(auth).get_by_id_crud(id=id)
        if not dept:
            raise CustomException(msg='删除失败，该部门不存在')
        await DeptCRUD(auth).delete(ids=[id])

    @classmethod
    async def batch_set_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        批量设置部门可用状态service
        
        :param auth: 认证对象
        :param data: 批量设置可用状态对象
        """
        dept_list = await DeptCRUD(auth).get_list_crud()
        total_ids = []
        
        if data.available:
            id_map = get_parent_id_map(model_list=dept_list)
            for dept_id in data.ids:
                enable_ids = get_parent_recursion(id=dept_id, id_map=id_map)
                total_ids.extend(enable_ids)
        else:
            id_map = get_child_id_map(model_list=dept_list)
            for dept_id in data.ids:
                disable_ids = get_child_recursion(id=dept_id, id_map=id_map)
                total_ids.extend(disable_ids)

        await DeptCRUD(auth).set_available_crud(ids=total_ids, available=data.available)
