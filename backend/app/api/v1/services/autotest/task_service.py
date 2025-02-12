# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Dict

from app.api.v1.cruds.autotest.project_crud import ProjectCRUD
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.task_schema import TaskOutSchema, TaskCreateSchema, TaskUpdateSchema
from app.api.v1.params.autotest.task_param import TaskQueryParams
from app.api.v1.cruds.autotest.task_crud import TaskCRUD
from app.core.exceptions import CustomException
from app.core.tasks import background_task, celery_app

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
    @celery_app.task
    async def create_services(cls, auth: AuthSchema, data: TaskCreateSchema) -> Dict:
        # 1. 获取项目和环境信息
        project = await ProjectCRUD(auth).get_obj_by_id(id=data.project_id)
        if not project.cases:
            raise CustomException(msg="项目未关联测试用例")

        # 2. 创建任务记录
        task_data = TaskCreateSchema(
            name=f"{data.name}-{project.name}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            status="running",
            start_time=datetime.now(),
            total_count=len(project.cases),
            project_id=data.project_id,
            environment_id=data.environment_id,
            message_ids=data.message_ids,
            description=data.description
        )
        task = await TaskCRUD(auth).create_obj(data=task_data)
        # 3. 执行用例
        obj =  await background_task.delay(auth=auth, task=task)

        return TaskOutSchema.model_validate(obj).model_dump()

    @classmethod
    @celery_app.task
    async def update_services(cls, auth: AuthSchema, data: TaskUpdateSchema) -> Dict:
        # 1. 获取项目和环境信息
        project = await ProjectCRUD(auth).get_obj_by_id(id=data.project_id)
        if not project.cases:
            raise CustomException(msg="项目未关联测试用例")
        # 2. 创建任务记录
        task_data = TaskUpdateSchema(
            id=data.id,
            name=f"{data.name}-{project.name}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            status="running",
            start_time=datetime.now(),
            total_count=len(project.cases),
            project_id=data.project_id,
            environment_id=data.environment_id,
            message_ids=data.message_ids,
            description=data.description
        )
        task = await TaskCRUD(auth).update_obj(id=data.id, data=task_data)
        # 3. 执行用例
        obj =  await background_task.delay(auth=auth, task=task)

        return TaskOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await TaskCRUD(auth).delete_obj(ids=[id])
