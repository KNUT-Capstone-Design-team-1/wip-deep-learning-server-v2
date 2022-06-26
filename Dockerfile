FROM python:3.8.1
COPY . /usr/src/wip
WORKDIR /usr/src/wip
USER root

# install library for deeplearning server
RUN apt-get update && apt-get -y install libgl1-mesa-glx libapache2-mod-wsgi \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip3 install compiler \
    && pip3 install -r /usr/src/wip/requirements.txt \
    && python3 /usr/src/wip/deeplearning_server/get_dl_model.py

# execute deeplearning server
ENTRYPOINT [ "python3", "/usr/src/wip/deeplearning_server/DL_main.py" ]