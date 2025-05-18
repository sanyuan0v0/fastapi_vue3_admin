#!/bin/bash

# 第一步：设置工作目录
echo "🔍 第一步：设置工作目录"
echo "⏳ 正在切换到工作目录 /home ..."
cd /home || { echo "❌ 无法切换到 /home 目录"; exit 1; }

# 第二步：清理旧项目文件夹（如果存在）
echo -e "\n🔍 第二步：清理旧项目文件夹（如存在）"
echo "⏳ 正在检查是否存在旧项目 fastapi_vue3_admin/ ..."
if [ -d "fastapi_vue3_admin/" ]; then
    echo "🗑️ 正在删除旧项目文件夹 fastapi_vue3_admin/ ..."
    rm -rf fastapi_vue3_admin/
    echo "✅ 旧项目文件夹已成功删除。"
else
    echo "✨ 未找到旧项目文件夹，跳过删除步骤。"
fi

# 第三步：克隆项目仓库
echo -e "\n🔍 第三步：克隆项目代码库"
echo "📥 正在克隆项目代码库 ..."
git clone https://gitee.com/tao__tao/fastapi_vue3_admin.git
if [ $? -eq 0 ]; then
    echo "✅ 项目克隆成功。"
else
    echo "❌ 项目克隆失败"
    exit 1
fi

# 第四步：进入项目根目录
echo -e "\n🔍 第四步：进入项目根目录"
echo "📁 正在进入项目目录 fastapi_vue3_admin ..."
cd fastapi_vue3_admin || { echo "❌ 无法进入项目目录"; exit 1; }

# 第五步：停止并删除正在运行的容器
echo -e "\n🔍 第五步：停止并删除现有容器"
echo "🛑 正在停止并删除现有容器 ..."
docker compose kill
docker compose rm -f
echo "✅ 容器已停止并删除。"

# 第六步：重新构建并启动服务
echo -e "\n🔍 第六步：构建镜像并启动容器"
echo "🏗️ 正在构建镜像并启动容器 ..."
docker compose build
docker compose up -d
echo "🚀 服务已成功构建并启动。"

# 部署完成提示
echo -e "\n🎉 部署流程已完成！"