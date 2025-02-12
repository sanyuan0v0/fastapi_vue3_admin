# -*- coding: utf-8 -*-

from typing import Dict, Any
from celery import Celery
from datetime import datetime

from app.api.v1.cruds.autotest.task_crud import TaskCRUD
from app.api.v1.cruds.autotest.case_crud import CaseCRUD
from app.api.v1.cruds.autotest.project_crud import ProjectCRUD
from app.api.v1.models.autotest.task_model import TaskModel
from app.api.v1.schemas.autotest.case_schema import CaseOutSchema
from app.api.v1.schemas.autotest.task_schema import TaskUpdateSchema
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.utils.request_util import RequestHandler
from app.utils.email_util import EmailUtil
from app.utils.ding_talk_util import DingTalkUtil
from app.core.exceptions import CustomException
from app.config.setting import settings

# 创建 Celery 实例
celery_app = Celery(
    "worker", 
    broker=settings.get_redis_uri,
    backend=settings.get_redis_uri,  # 使用 Redis 存储任务结果
    include=["tasks"],  # 包含任务模块
)

# 配置 Celery
celery_app.conf.update(
    result_expires=3600,  # 任务结果过期时间（秒）
    timezone="Asia/Shanghai",  # 时区
)

@celery_app.task
async def background_task(auth: AuthSchema, task: TaskModel) -> TaskModel:
    """
    执行测试
    """
    try:
        # 1. 执行测试用例
        results = {
            "success": 0,
            "fail": 0,
            "skip": 0,
            "error": 0,
            "details": []
        }

        project = await ProjectCRUD(auth).get_obj_by_id(id=task.project_id)
        for case in project.cases:
            try:
                # 执行单个用例
                case_result = await execute_single_case(
                    auth=auth,
                    base_url=project.base_url,
                    headers=project.headers,
                    case=case
                )
                results["details"].append(case_result)

                # 更新统计数据
                if case_result["status"] == "success":
                    results["success"] += 1
                elif case_result["status"] == "fail":
                    results["fail"] += 1
                elif case_result["status"] == "skip":
                    results["skip"] += 1
                else:
                    results["error"] += 1

            except Exception as e:
                results["error"] += 1
                results["details"].append({
                    "case_id": case.id,
                    "case_name": case.name,
                    "status": "error",
                    "error": str(e)
                })

        # 2. 发送通知
        duration = (datetime.now() - task.start_time).total_seconds()
        pass_rate = f"{(results['success']/len(project.cases))*100:.2f}%"
        result = await send_notification(
            message=project.message,
            title=task.name,
            environment=task.environment.name,
            tester=auth.user.username,
            total=len(project.cases),
            pass_num=results["success"],
            fail_num=results["fail"],
            error_num=results["error"],
            skip_num=results["skip"],
            rate=pass_rate,
            duration=f"{duration:.2f}s"
        )

        # 3. 更新任务状态
        task_update = TaskUpdateSchema(
            id=task.id,
            status="completed",
            end_time=datetime.now(),
            success_count=results["success"],
            fail_count=results["fail"],
            skip_count=results["skip"],
            error_count=results["error"],
            summary={
                "total": len(project.cases),
                "pass_rate": pass_rate,
                "duration": f"{duration:.2f}s",
                "environment": project.environment.name,
                "details": results["details"]
            },
            logs=f"发送信息结果: {result}"
        )
        obj =  await TaskCRUD(auth).update_obj(id=task.id, data=task_update)
        return obj

    except Exception as e:
        # 如果任务已创建，更新为失败状态
        if 'task' in locals():
            await TaskCRUD(auth).update_obj(
                id=task.id,
                data=TaskUpdateSchema(
                    status="failed",
                    end_time=datetime.now(),
                    logs=str(e)
                )
            )
        raise CustomException(msg=f"任务执行失败: {str(e)}")

async def execute_single_case(auth: AuthSchema, base_url: str, headers: dict, case: CaseOutSchema) -> Dict[str, Any]:
    """执行单个测试用例"""
    try:
        # 1. 获取用例信息
        case = await CaseCRUD(auth).get_obj_by_id(id=case.id)

        if not case.status:
            raise CustomException(msg="测试用例跳过执行")
        
        # 优化请求头处理逻辑
        header = headers.copy()
        if case.parameter_need:
            header.update(case.headers)

        # 2. 准备请求数据
        request_data = {
            'url': base_url + case.url,
            'method': case.method,
            'headers': header,
            'params': case.params,
            'body': case.body,
            'files': case.files
        }

        # 3. 发送请求
        request_handler = RequestHandler()
        response = request_handler.send_request(**request_data)

        # 4. 断言结果
        assertion_results = request_handler.assert_response(response, case.expected)

        # 5. 判断用例执行结果
        is_passed = all(result["result"] for result in assertion_results)

        return {
            "case_id": case.id,
            "case_name": case.name,
            "status": "success" if is_passed else "fail",
            "request": request_data,
            "response": response,
            "assertions": assertion_results
        }

    except Exception as e:
        return {
            "case_id": case.id,
            "status": "error",
            "error": str(e)
        }

async def send_notification(message: dict, **kwargs) -> bool:
    """统一的消息发送处理"""
    # {   
    #     "dingtalk_statue": false,
    #     "email_statue": false,
    #     "dingtalk": {
    #         "webhook": "钉钉机器人的webhook地址",
    #         "secret": "钉钉机器人的密钥"
    #     },
    #     "email": {
    #         "smtp_host": "SMTP服务器地址",
    #         "smtp_port": "SMTP服务器端口",
    #         "smtp_username": "SMTP用户名",
    #         "smtp_password": "SMTP密码",
    #         "smtp_ssl": "是否使用SSL加密",
    #         "smtp_tls": "是否使用TLS加密",
    #         "smtp_from": "发件人地址",
    #         "smtp_to": "收件人地址"
    #     }
    # }
    try:
        if not message:
            return False
        if message["dingtalk_statue"]:
            await DingTalkUtil(message["dingtalk"]).send_dingtalk(**kwargs)
        if message["email_statue"]:
            await EmailUtil(message["email"]).send_default_email(**kwargs)
        return True
    except Exception as e:
        return False
