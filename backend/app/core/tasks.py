from celery import Celery

# 创建 Celery 实例
celery_app = Celery(
    "worker", 
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",  # 使用 Redis 存储任务结果
    include=["tasks"],  # 包含任务模块
)

# 配置 Celery
celery_app.conf.update(
    result_expires=3600,  # 任务结果过期时间（秒）
    timezone="Asia/Shanghai",  # 时区
)

@celery_app.task
def long_running_task(data):
    return f"Processed: {data}"


def background_task():
    for i in range(10):
        yield f"执行后台任务: {i}\n"
