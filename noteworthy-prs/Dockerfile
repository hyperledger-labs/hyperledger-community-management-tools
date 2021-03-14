FROM golang:1.15-buster
WORKDIR /app
COPY . /app
RUN go build
RUN rm *.go go.*
ENV PATH=${PATH}:/app

CMD ["noteworthy-prs"]
