FROM python:3.7-alpine
LABEL maintainer="zhoushuke <zhoushuke@sensetime.com>"

RUN apk add --no-cache tzdata

ENV TZ=Asia/Shanghai

RUN chmod -R 777 /var/log && mkdir /xmonitor && \
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /xmonitor
COPY . /xmonitor

RUN pip install --trusted-host pypi.douban.org --no-cache-dir -r requirements.txt
CMD [ "python", "/xmonitor/main.py" ]