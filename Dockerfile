FROM python:3.8

ARG DL_SERVER_PORT

ENV DL_SERVER_PORT=$DL_SERVER_PORT
ENV TZ=Asia/Seoul

COPY . /usr/local/wip-deep-learning-server-v2
WORKDIR /usr/local/wip-deep-learning-server-v2
USER root

RUN apt update && apt -y install \
  libgl1-mesa-glx \
  libapache2-mod-wsgi \
  tcpdump \
  net-tools \
  vim \
  tzdata

RUN /usr/local/bin/python -m pip install --upgrade pip && \
  pip3 install compiler && \
  pip3 install --no-cache-dir -r /usr/local/wip-deep-learning-server-v2/requirements.txt && \
  python3 /usr/local/wip-deep-learning-server-v2/get_dl_model.py

EXPOSE $DL_SERVER_PORT

ENTRYPOINT [ "python3", "/usr/local/wip-deep-learning-server-v2/server.py" ]