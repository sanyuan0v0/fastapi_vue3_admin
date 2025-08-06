#!/bin/bash

# 设置全局变量
PROJECT_NAME="fastapi_vue3_admin"
WORK_DIR="/home"
GIT_REPO="https://gitee.com/tao__tao/fastapi_vue3_admin.git"

# 打印带时间戳的日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 检查权限
check_permissions() {
    log "==========🔍 第一步：检查权限...=========="
    # 检查脚本文件是否有执行权限
    if [ ! -x "$0" ]; then
        log "⚠️ 当前脚本没有执行权限，尝试添加执行权限..."
        chmod +x "$0"
        if [ $? -eq 0 ]; then
            log "✅ 已成功为脚本添加执行权限"
        else
            log "❌ 为脚本添加执行权限失败"
            exit 1
        fi
    else
        log "✅ 脚本已有执行权限"
    fi
}

# 检查依赖
check_dependencies() {
    log "==========🔍 第二步：检查系统依赖...=========="
    for cmd in git docker node npm; do
        command -v $cmd &> /dev/null || { log "❌ $cmd 未安装"; exit 1; }
        log "🎉 $cmd 已安装 - $($cmd -v)"
    done
    log "✅ 所有依赖检查通过"
}

# 更新代码
update_code() {
    log "==========🔍 第三步：检查项目...=========="
    cd "${WORK_DIR}" || { log "❌ 无法进入工作目录：${WORK_DIR}"; exit 1; }
    if [ -d "${PROJECT_NAME}/" ]; then
        log "🔄 项目已存在，开始更新代码"
        cd "${PROJECT_NAME}" || { log "❌ 无法进入项目目录：${PROJECT_NAME}"; exit 1; }
        
        [ -f "docker-compose.yaml" ] || { log "❌ docker-compose.yaml 文件未找到"; exit 1; }
        docker compose down
        log "✅ 容器已停止并删除"
        
        git pull --force || { log "❌ 拉取更新失败"; exit 1; }
        git log -1 || { log "❌ 获取提交信息失败"; exit 1; }
        log "✅ 代码更新成功"
    else
        log "📥 项目不存在，开始克隆代码"
        git clone "${GIT_REPO}" || { log "❌ 项目克隆失败：${GIT_REPO}"; exit 1; }
        cd "${PROJECT_NAME}" || { log "❌ 无法进入项目目录：${PROJECT_NAME}"; exit 1; }
        log "✅ 代码克隆成功"
    fi
}

# 构建镜像
build_image() {
    log "==========🚀 第四步：构建镜像...==========🗑️ "

    cd frontend || { log "❌ 无法进入前端目录"; exit 1; }
    npm install || { log "❌ 前端依赖安装失败"; exit 1; }
    npm run docs:build || { log "❌ 项目文档打包生成失败"; exit 1; }
    log "✅ 项目文档打包成功"
    npm run build || { log "❌ 前端工程打包失败"; exit 1; }
    log "✅ 前端工程打包成功"
    cd .. || { log "❌ 无法返回项目根目录"; exit 1; }

    docker compose build || { log "❌ 镜像构建失败"; exit 1; }
    log "✅  Docker镜像构建成功"
}

# 启动容器
start_containers() {
    log "==========🚀 第五步：启动容器...==========🗑️ "
    docker compose up -d --force-recreate || { log "❌ 容器启动失败"; exit 1; }
    log "✅  容器启动成功"
}


# 清理旧镜像
cleanup_old_images() {
    log "==========🗑️ 第六步：清理72小时前的旧镜像...==========🗑️ "
    docker image prune -f --filter "until=72h"
    log "✅ 旧镜像清理完成"
}

# 主函数
main() {
    log "==========🚀 开始部署流程=========="
    check_permissions
    check_dependencies
    update_code
    build_image
    start_containers
    cleanup_old_images
    log "==========🎉 部署完成=========="
}

main
trap 'log "==========⚠️ 脚本中断=========="; exit 1' INT TERM