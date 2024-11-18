FROM golang:1.21-alpine

WORKDIR /app

# 复制go模块文件
COPY backend/go.mod backend/go.sum ./

# 初始化并下载依赖
RUN go mod init ssh-manager && \
    go mod tidy && \
    go mod download

# 复制源代码
COPY . .

# 构建应用
RUN go build -o main .

EXPOSE 8080

CMD ["./main"]
