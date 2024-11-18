FROM golang:1.21-bullseye

WORKDIR /app

# 将当前目录的文件复制到容器中
COPY . .

# 更新软件源并安装编译 SQLite 所需的依赖
RUN apt-get update && apt-get install -y \
    gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# 下载依赖
RUN go mod download

# 安装缺少的依赖（如 go-sqlite3 所需的模块）
RUN go get ssh-manager

# 启用 CGO 并构建二进制文件
ENV CGO_ENABLED=1
RUN go build -o main .

# 暴露服务端口
EXPOSE 8999

# 启动服务
CMD ["./main"]
