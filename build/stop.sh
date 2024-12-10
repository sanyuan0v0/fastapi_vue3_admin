#!/bin/bash

# 检查是否已经处于虚拟环境中
if [[ ":$VIRTUAL_ENV:" != *":/opt/model-ai/backend/venv:"* ]]; then
    # 进入后端目录
    cd /opt/ || { echo "进入项目工程目录失败"; exit 1; }
    
fi

# 查找并停止使用 nohup 启动的应用
process_id=$(pgrep -f "python main.py run")

if [ -n "$process_id" ]; then
    echo "找到进程 ID: $process_id"
    
    # 发送 SIGINT 信号停止进程
    echo "向进程 $process_id 发送 SIGINT 信号"
    kill -INT $process_id
    
    # 等待进程结束，最多等待 10 秒
    echo "等待进程停止（最多 10 秒）"
    for i in $(seq 1 10); do
        if ! pgrep -f "python main.py run" > /dev/null; then
            break
        fi
        sleep 1
    done
    
    # 检查进程是否已经停止
    if pgrep -f "python main.py run" > /dev/null; then
        echo "进程 $process_id 在 10 秒内未停止，正在强制退出"
        kill -KILL $process_id
    else
        echo "进程 $process_id 已成功停止"
    fi
    
else
    echo "没有找到运行中的 python main.py run 进程"
fi