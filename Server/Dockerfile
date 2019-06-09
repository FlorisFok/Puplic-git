FROM python:latest
RUN apt-get update -y
COPY . /site
WORKDIR /site
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["-m http.server 8080"]
