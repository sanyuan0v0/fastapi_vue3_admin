#!/bin/bash

# 检查是否已经处于虚拟环境中
if [[ ":$VIRTUAL_ENV:" != *":/opt/model-ai/backend/venv:"* ]]; then
    # 切换到目标目录
    cd /opt/ || { echo "切换 /opt 目录失败"; exit 1; }
    
    # 替换现有仓库
    if [ -d "/opt/model-ai" ]; then
        rm -rf /opt/model-ai
    fi
    
    # 克隆仓库
    git clone git@gitee.com:tao__tao/model-ai.git || { echo "克隆仓库失败"; exit 1; }
    
    # 进入后端目录
    cd /opt/model-ai/backend || { echo "进入后端目录失败"; exit 1; }
    
    # 创建虚拟环境
    python3 -m venv venv || { echo "创建虚拟环境失败"; exit 1; }
    
    # 激活虚拟环境
    source ./venv/bin/activate || { echo "激活虚拟环境失败"; exit 1; }
fi

# 安装依赖
pip install -r requirements.txt || { echo "安装依赖失败"; exit 1; }

# 初始化应用
echo "开始初始化应用"
python main.py init || { echo "初始化应用失败"; exit 1; }
echo "应用初始化完成"

# 使用 nohup 在后台运行应用，并将输出重定向到日志文件
echo "开始启动应用"
nohup python main.py run > /opt/logs/main.log 2>&1 &

# 获取 nohup 的进程 ID
NOHUP_PID=$!

# 检查后台进程是否成功启动
if [ $? -eq 0 ]; then
    # 将后台进程从当前 shell 会话中分离出来
    echo "应用已启动，进程 ID: $NOHUP_PID"

    # 等待一段时间，确保日志文件中有内容
    sleep 3
    
    # 打印日志文件的内容
    cat /opt/logs/main.log

    echo "应用已启动"
else
    echo "启动应用失败"
    exit 1
fi