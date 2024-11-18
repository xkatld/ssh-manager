FROM golang:1.21-alpine

WORKDIR /app

COPY . .

RUN go mod download

RUN go get ssh-manager

RUN go build -o main .

EXPOSE 8999

CMD ["./main"]
