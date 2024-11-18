# 使用 Debian Slim 镜像
FROM debian:bullseye-slim

# 设置维护者信息（可选）
LABEL maintainer="your_email@example.com"

# 安装必要的软件包和 locales 支持
RUN apt-get update && apt-get install -y \
    nginx \
    locales \
    && rm -rf /var/lib/apt/lists/*

# 配置 locales 为 UTF-8
RUN sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8

# 设置环境变量以确保正确的字符集
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# 复制静态资源到自定义的 Nginx 网站目录
COPY index.html /usr/local/nginx/html/
COPY script.js /usr/local/nginx/html/

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
