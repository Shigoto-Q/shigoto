FROM golang:1.16-alpine as build

ENV GO11MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64 \
    BASE_PATH=/go/src/app

WORKDIR /app/websocket

COPY websocket/  /app/websocket

RUN go mod download
RUN go build -o websocket .

RUN sed -i 's/\r$//g' websocket
RUN chmod +x websocket

CMD ./websocket

EXPOSE 8080
