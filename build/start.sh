#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始启动服务...${NC}"

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: docker-compose 未安装${NC}"
    exit 1
fi

# 进入构建目录
cd "$(dirname "$0")" || exit 1

# 构建并启动所有服务
echo -e "${GREEN}构建并启动 Docker 服务...${NC}"
docker-compose up -d --build

# 检查服务状态
echo -e "${GREEN}检查服务状态...${NC}"
docker-compose ps

# 输出服务访问信息
echo -e "\n${GREEN}服务启动完成！${NC}"
echo -e "前端服务: http://localhost:80"
echo -e "后端服务: http://localhost:8000"
echo -e "MySQL: localhost:3306"
echo -e "Redis: localhost:6379"
echo -e "MongoDB: localhost:27017"