FROM python:3.8.1

ARG DL_SERVER_PORT

ENV DL_SERVER_PORT=$DL_SERVER_PORT

COPY . /usr/local/wip-deep-learning-server-v2
WORKDIR /usr/local/wip-deep-learning-server-v2
USER root

RUN apt-get update && apt-get -y install libgl1-mesa-glx libapache2-mod-wsgi \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip3 install compiler \
    && pip3 install -r /usr/local/wip-deep-learning-server-v2/requirements.txt \
    && python3 /usr/local/wip-deep-learning-server-v2/get_dl_model.py

EXPOSE $DL_SERVER_PORT

ENTRYPOINT [ "python3", "/usr/local/wip-deep-learning-server-v2/DL_main.py" ]