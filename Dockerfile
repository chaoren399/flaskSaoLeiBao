#FROM python:3.9-slim
FROM registry.cn-hangzhou.aliyuncs.com/baimeidashu/bmds:python-3.9-slim
# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5010

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5010

# 启动应用
CMD ["python", "app.py"]
