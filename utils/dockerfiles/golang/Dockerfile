FROM golang:1.16-alpine as build

ENV GO11MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64 \
    BASE_PATH=/go/src/app

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o main .

EXPOSE 8080
CMD ["./main"]
