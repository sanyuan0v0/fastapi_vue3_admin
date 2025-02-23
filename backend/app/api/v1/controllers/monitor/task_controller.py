# -*- coding: utf-8 -*-

from datetime import datetime, timezone
import json
from typing import Optional
import croniter
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, WebSocket, Request
from fastapi.responses import StreamingResponse
from celery.result import AsyncResult
from pydantic import BaseModel
from redis import Redis

from celery_app import celery_app
from app.core.dependencies import AuthPermission
from app.core.tasks import task
from app.common.response import SuccessResponse
from app.core.logger import logger

router = APIRouter()

@router.get("/list", summary="任务列表", dependencies=[Depends(AuthPermission(permissions=["monitor:task:query"]))])
async def get_tasks(request: Request):
    redis: Redis = request.app.state.redis
    task_keys = await redis.keys("celery-task-meta-*")  # 假设使用异步 Redis 客户端
    tasks = []
    if not task_keys:
        return SuccessResponse(msg="获取任务列表成功", data=[])
    for key in task_keys:
        if isinstance(key, bytes):  # 兼容字节类型
            task_id = key.decode().split("celery-task-meta-")[-1]
        else:  # 字符串类型
            task_id = key.split("celery-task-meta-")[-1]

        task_data = await redis.get(key)  # 假设使用异步 Redis 客户端
        if task_data:
            try:
                task_data = json.loads(task_data.decode()) if isinstance(task_data, bytes) else json.loads(task_data)
            except json.JSONDecodeError:
                task_data = task_data.decode() if isinstance(task_data, bytes) else task_data
        tasks.append({"task_id": task_id, "result": task_data})
    return SuccessResponse(msg="获取任务列表成功", data=tasks)

@router.get("/detail/{task_id}", summary="任务详情", dependencies=[Depends(AuthPermission(permissions=["monitor:task:query"]))])
async def check_task(task_id: str):
    result = AsyncResult(id=task_id, app=celery_app)
    if result.state == 'PENDING':  # 如果任务不存在或未启动
        raise HTTPException(status_code=404, detail="任务不存在")

    status_map = {
        'SUCCESS': '成功',
        'FAILURE': '失败',
        'PENDING': '等待中',
        'RETRY': '重试中',
        'STARTED': '运行中',
    }
    status = status_map.get(result.state, result.state)

    data = {
        "task_id": task_id,
        "status": status,
        "result": str(result.info) if result.failed() else result.info,  # 失败时转换为字符串
        "date_done": result.date_done.isoformat() if result.date_done else None,  # 转换为字符串并处理 None
    }
    return SuccessResponse(msg="获取任务详情成功", data=data)

class CreateTaskSchema(BaseModel):
    res: str
    is_cron: bool
    cron_expression: Optional[str] = None

@router.post("/create", summary="任务创建", dependencies=[Depends(AuthPermission(permissions=["monitor:task:create"]))])
async def start_task(data: CreateTaskSchema):
    try:
        if data.is_cron:
            if not data.cron_expression:
                raise HTTPException(status_code=400, detail="定时任务必须提供 cron 表达式")
            
            # 校验 cron 表达式
            try:
                now = datetime.now(timezone.utc)
                cron = croniter(data.cron_expression, now)
                next_run_time = cron.get_next(datetime)
            except Exception as e:
                logger.error(f"无效的 cron 表达式: {data.cron_expression}, 错误: {e}")
                raise HTTPException(status_code=400, detail="无效的 cron 表达式")
            result = task.apply_async(args=[data.res], eta=next_run_time)
        else:
            result = task.delay(data.res)
        logger.info(f"任务创建成功, 任务ID: {result.id}")
        return SuccessResponse(msg="创建任务成功", data=result.id)

    except Exception as e:
        logger.error(f"任务创建失败: {e}")
        raise HTTPException(status_code=500, detail="任务创建失败")

@router.put("/cancel/{task_id}", summary="任务取消(默认：强制终止)", dependencies=[Depends(AuthPermission(permissions=["monitor:task:update"]))])
async def cancel_task(task_id: str):
    result = AsyncResult(id=task_id, app=celery_app)
    if result.state in ('SUCCESS', 'FAILURE'):
        raise HTTPException(status_code=400, detail="任务已完成，无法取消")
    result.revoke(terminate=True)
    return SuccessResponse(msg=f"任务{task_id}已取消", data=task_id)

@router.delete("/delete/{task_id}", summary="任务删除", dependencies=[Depends(AuthPermission(permissions=["monitor:task:delete"]))])
async def delete_task(task_id: str):
    result = AsyncResult(id=task_id, app=celery_app)
    if result.state == 'STARTED':
        raise HTTPException(status_code=400, detail="任务正在运行，无法删除")
    result.forget()
    return SuccessResponse(msg=f"任务{task_id}已删除", data=task_id)

@router.post("/background_tasks", summary="模拟fastapi自带后台任务-模拟流式响应")
async def stream_response(background_tasks: BackgroundTasks, *args, **kwargs):
    background_tasks.add_task(task, *args, **kwargs)
    return StreamingResponse(
        data=task(*args, **kwargs),
        headers={"X-Custom-Header": "Streaming-Response"},
        media_type="text/plain",
    )

@router.websocket("/ws", name="websocket")
async def websocket_endpoint(websocket: WebSocket):
    # ws://127.0.0.1:8000/ws
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
