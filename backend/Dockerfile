FROM golang:1.21-alpine

WORKDIR /app

COPY . .

RUN apk add --no-cache gcc musl-dev

RUN go mod download

RUN go get ssh-manager

ENV CGO_ENABLED=1
RUN go build -o main .

EXPOSE 8999

CMD ["./main"]
