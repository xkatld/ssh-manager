FROM golang:1.21-alpine

WORKDIR /app

# 复制go模块文件
RUN wget -O main.go https://raw.githubusercontent.com/xkatld/ssh-manager/refs/heads/main/backend/main.go && \
    wget -O go.mod https://raw.githubusercontent.com/xkatld/ssh-manager/refs/heads/main/backend/go.mod

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
