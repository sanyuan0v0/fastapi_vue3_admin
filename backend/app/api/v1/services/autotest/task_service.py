# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.task_schema import TaskOutSchema, TaskCreateSchema, TaskUpdateSchema
from app.api.v1.params.autotest.task_param import TaskQueryParams
from app.api.v1.cruds.autotest.task_crud import TaskCRUD
from app.api.v1.cruds.autotest.api_case_crud import APICaseCRUD
from app.api.v1.cruds.autotest.project_crud import ProjectCRUD
from app.api.v1.cruds.autotest.environment_crud import EnvironmentCRUD
from app.api.v1.cruds.autotest.notification_config_crud import NotificationConfigCRUD
from app.api.v1.cruds.autotest.global_data_crud import GlobalDataCRUD
from app.api.v1.cruds.autotest.module_crud import ModuleCRUD
from app.api.v1.cruds.autotest.repont_crud import ReportCRUD
from app.utils.request_util import Requests



class TaskService:
    """
    执行记录服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await TaskCRUD(auth).get_obj_by_id(id=id)
        return TaskOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: TaskQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await TaskCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [TaskOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: TaskCreateSchema, id: int) -> Dict:

        api_case = await APICaseCRUD(auth).get_obj_by_id(id=id)
        request_data = {
            'url': api_case.url,
            'method': api_case.method,
            'data': api_case.body,
            'headers': api_case.headers,
        }

        # 发送请求并获取响应
        response = Requests().send_request(**request_data)
        
        # 验证结果
        validation_results = [
            api_case.expected_status_code == response['code'],
            api_case.expected_response in response['body']['msg'],
            api_case.assertions in str(response['body'])
        ]
        
        status = 'pass' if all(validation_results) else 'fail'
        
        data.status = status
        data.logs = response['time_total']
        data.actual_response = response['body']
        data.test_case_id = id
        data.description = api_case.description


        obj = await TaskCRUD(auth).create_obj(data=data)
        return TaskOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: TaskUpdateSchema) -> Dict:
        obj = await TaskCRUD(auth).update_obj(id=data.id, data=data)
        return TaskOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await TaskCRUD(auth).delete_obj(ids=[id])
