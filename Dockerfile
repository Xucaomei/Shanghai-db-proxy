FROM python:3.9-slim

WORKDIR /app

# 安装依赖
RUN pip install flask requests

# 复制代码
COPY app.py .

# 暴露端口
EXPOSE 5000

# 运行应用
CMD ["python", "app.py"]
