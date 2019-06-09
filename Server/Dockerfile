FROM python:latest
RUN apt-get update -y
COPY . /site
WORKDIR /site
EXPOSE 8080
CMD python -m http.server 8080
