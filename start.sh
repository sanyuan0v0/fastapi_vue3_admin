#!/bin/bash

# 设置全局变量
PROJECT_NAME="fastapi_vue3_admin"
WORK_DIR="/home"
GIT_REPO="https://gitee.com/tao__tao/fastapi_vue3_admin.git"

# 第一步：设置工作目录
echo "🔍 第一步：设置工作目录"
echo "⏳ 正在切换到工作目录 ${WORK_DIR} ..."
cd "${WORK_DIR}" || { echo "❌ 无法切换到 ${WORK_DIR} 目录"; exit 1; }

# 第二步：清理旧项目文件夹（如果存在）
echo -e "\n🔍 第二步：清理旧项目文件夹（如存在）"
echo "⏳ 正在检查是否存在旧项目 ${PROJECT_NAME}/ ..."
if [ -d "${PROJECT_NAME}/" ]; then
    echo "🗑️ 正在删除旧项目文件夹 ${PROJECT_NAME}/ ..."
    rm -rf "${PROJECT_NAME}/" || { echo "❌ 删除旧项目文件夹失败"; exit 1; }
    echo "✅ 旧项目文件夹已成功删除。"
else
    echo "✨ 未找到旧项目文件夹，跳过删除步骤。"
fi

# 第三步：克隆项目仓库
echo -e "\n🔍 第三步：克隆项目代码库"
echo "📥 正在克隆项目代码库 ..."
git clone "${GIT_REPO}" || { echo "❌ 项目克隆失败"; exit 1; }
echo "✅ 项目克隆成功。"

# 第四步：进入项目根目录
echo -e "\n🔍 第四步：进入项目根目录"
echo "📁 正在进入项目目录 ${PROJECT_NAME} ..."
cd "${PROJECT_NAME}" || { echo "❌ 无法进入项目目录"; exit 1; }

# 第五步：停止并删除正在运行的容器
echo -e "\n🔍 第五步：停止并删除现有容器"
echo "🛑 正在停止并删除现有容器 ..."
docker compose kill || { echo "⚠️ 停止容器失败，可能没有运行的容器"; }
docker compose rm -f || { echo "⚠️ 删除容器失败，可能没有容器可删除"; }
echo "✅ 容器已停止并删除。"

# 第六步：打包前端项目
echo -e "\n🔍 第六步: 打包前端工程"
echo "📦 正在检查前端是否需要重新构建..."

# 检查是否需要重新构建
if [ ! -d "frontend/dist" ] || [ "$(git diff --name-only HEAD~1 HEAD)" ]; then
    echo "🔧 检测到代码变更，正在安装前端依赖并构建..."
    cd frontend || { echo "❌ 无法进入前端目录"; exit 1; }
    npm install || { echo "❌ 前端依赖安装失败"; exit 1; }
    npm run build || { echo "❌ 前端工程打包失败"; exit 1; }
    echo "✅ 前端工程打包成功。"
    cd .. || { echo "❌ 无法返回项目根目录"; exit 1; }
    
    echo "🏗️ 正在构建镜像..."
    docker compose build || { echo "❌ 镜像构建失败"; exit 1; }
else
    echo "✨ 代码未变更，跳过构建步骤。"
fi

docker compose up -d || { echo "❌ 容器启动失败"; exit 1; }
echo "🚀 服务已成功启动。"

# 部署完成提示
echo -e "\n🎉 部署流程已完成！"
echo "前端访问地址: http://8.137.99.5:80"
echo "后端API文档: http://8.137.99.5:8001/api/v1/docs"