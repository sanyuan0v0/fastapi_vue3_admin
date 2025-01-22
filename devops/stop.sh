#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始停止服务...${NC}"

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: docker-compose 未安装${NC}"
    exit 1
fi

# 进入构建目录
cd "$(dirname "$0")" || exit 1

# 停止所有服务
echo -e "${GREEN}停止所有 Docker 服务...${NC}"
docker-compose down

# 清理未使用的镜像和卷（可选）
read -p "是否清理未使用的 Docker 镜像和卷？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}清理未使用的 Docker 镜像...${NC}"
    docker image prune -f
    echo -e "${GREEN}清理未使用的 Docker 卷...${NC}"
    docker volume prune -f
fi

echo -e "\n${GREEN}所有服务已停止！${NC}"