#!/bin/bash

# 设置全局变量
PROJECT_NAME="fastapi_vue3_admin"
WORK_DIR="/home"
GIT_REPO="https://gitee.com/tao__tao/fastapi_vue3_admin.git"
VERSION_TAG=$(date +%Y%m%d%H%M%S)
IMAGE_NAME="fastapi_vue3_admin:${VERSION_TAG}"
FRONTEND_URL="http://8.137.99.5:80"
BACKEND_DOC_URL="http://8.137.99.5:8001/api/v1/docs"

# 打印带时间戳的日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 检查权限
check_permissions() {
    log "🔍 第一步：检查权限..."
    [ "$(id -u)" = "0" ] || { log "❌ 需要 root 权限"; exit 1; }
    log "✅ 权限检查通过"
}

# 检查依赖
check_dependencies() {
    log "🔍 第二步：检查系统依赖..."
    for cmd in git docker node npm; do
        command -v $cmd &> /dev/null || { log "❌ $cmd 未安装"; exit 1; }
        log "🎉 $cmd 已安装 - $($cmd -v)"
    done
    log "✅ 所有依赖检查通过"
}

# 更新代码
update_code() {
    log "🔍 第三步：检查项目代码..."
    cd "${WORK_DIR}" || { log "❌ 无法进入工作目录：${WORK_DIR}"; exit 1; }
    if [ -d "${PROJECT_NAME}/" ]; then
        log "🔄 项目已存在，开始更新代码"
        cd "${PROJECT_NAME}" || { log "❌ 无法进入项目目录：${PROJECT_NAME}"; exit 1; }
        git fetch origin master || { log "❌ 拉取更新失败"; exit 1; }
        git reset --hard origin/master || { log "❌ 重置代码失败"; exit 1; }
        log "✅ 代码更新成功"
    else
        log "📥 项目不存在，开始克隆代码"
        git clone "${GIT_REPO}" || { log "❌ 项目克隆失败：${GIT_REPO}"; exit 1; }
        cd "${PROJECT_NAME}" || { log "❌ 无法进入项目目录：${PROJECT_NAME}"; exit 1; }
        log "✅ 代码克隆成功"
    fi
}

# 构建前端
build_frontend() {
    # 如果是首次克隆项目，或者检测到前端代码变更，则构建前端
    if [ ! -d "frontend/dist" ] || [ "$(git diff --name-only HEAD~1 HEAD)" ]; then
        log "🚀 检测到前端代码变更或首次克隆，开始构建前端..."
        cd frontend || { log "❌ 无法进入前端目录"; exit 1; }
        npm install --omit=optional --verbose || { log "❌ 前端依赖安装失败"; exit 1; }
        npm run build || { log "❌ 前端工程打包失败"; exit 1; }
        log "✅ 前端工程打包成功"
        cd .. || { log "❌ 无法返回项目根目录"; exit 1; }
    else
        log "⚠️ 未检测到前端代码变更且非首次克隆，跳过前端构建"
    fi
}

# 停止并删除容器
stop_and_remove_containers() {
    log "🗑️ 停止并删除现有容器..."
    [ -f "docker-compose.yaml" ] || { log "❌ docker-compose.yaml 文件未找到"; exit 1; }
    docker compose kill
    docker compose rm -f
    log "✅ 容器已停止并删除"
}

# 构建镜像
build_image() {
    log "🚀 开始构建Docker镜像..."
    docker compose build --build-arg VERSION_TAG=${VERSION_TAG} || { log "❌ 镜像构建失败"; exit 1; }
    log "✅  Docker镜像构建成功"
}

# 启动容器
start_containers() {
    log "🚀 启动容器..."
    docker compose up -d || { log "❌ 容器启动失败"; exit 1; }
    log "✅  容器启动成功"
}

# 健康检查
health_check() {
    log "⏱️ 等待服务启动..."
    sleep 10
    log "🔍 进行健康检查..."
    curl --output /dev/null --silent --head --fail "${FRONTEND_URL}" || { log "❌ 前端服务健康检查失败"; exit 1; }
    curl --output /dev/null --silent --head --fail "${BACKEND_DOC_URL}" || { log "❌ 后端服务健康检查失败"; exit 1; }
    log "✅ 服务健康检查通过"
}

# 清理旧镜像
cleanup_old_images() {
    log "🗑️ 清理24小时前的旧镜像..."
    docker image prune -f --filter "until=24h"
    log "✅ 旧镜像清理完成"
}

# 主函数
main() {
    log "🚀 开始部署流程"
    check_permissions
    check_dependencies
    update_code
    stop_and_remove_containers
    build_frontend
    build_image
    start_containers
    health_check
    cleanup_old_images
    log "🎉 部署完成"
    echo "🌐 前端地址: ${FRONTEND_URL}"
    echo "📚 API文档: ${BACKEND_DOC_URL}"
}

main
trap 'log "⚠️ 脚本中断"; exit 1' INT TERM