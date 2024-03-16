FROM python:3.8.1

# Arguments
ARG DL_SERVER_PORT

# 환경 변수
ENV DL_SERVER_PORT=$DL_SERVER_PORT

# 컨테이너 내 디렉터리로 파일 복사
COPY . /usr/local/wip-deep-learning-server-v2
WORKDIR /usr/local/wip-deep-learning-server-v2
USER root

# 필요 패키지 및 라이브러리 설치
RUN apt-get update && apt-get -y install libgl1-mesa-glx libapache2-mod-wsgi \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip3 install compiler \
    && pip3 install -r /usr/local/wip-deep-learning-server-v2/requirements.txt \
    && python3 /usr/local/wip-deep-learning-server-v2/get_dl_model.py

# 포트
EXPOSE $DL_SERVER_PORT

# 실행
ENTRYPOINT [ "python3", "/usr/local/wip-deep-learning-server-v2/DL_main.py" ]