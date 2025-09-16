#!/bin/bash

# 构建并启动服务
docker-compose up --build -d

echo "应用已启动，访问地址: http://localhost:5010"
