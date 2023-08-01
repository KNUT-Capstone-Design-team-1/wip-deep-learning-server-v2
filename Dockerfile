FROM python:3.8.1

# Arguments
ARG DL_PORT_NUMBER

# 환경 변수
ENV DL_PORT_NUMBER=$DL_PORT_NUMBER

# 컨테이너 내 디렉터리로 파일 복사
COPY . /usr/local/wip-dl
WORKDIR /usr/local/wip-dl
USER root

# 필요 패키지 및 라이브러리 설치
RUN apt-get update && apt-get -y install libgl1-mesa-glx libapache2-mod-wsgi \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip3 install compiler \
    && pip3 install -r /usr/local/wip-dl/requirements.txt \
    && python3 /usr/local/wip-dl/deeplearning_server/get_dl_model.py

# 포트
EXPOSE $DL_PORT_NUMBER

# 실행
ENTRYPOINT [ "python3", "/usr/local/wip-dl/deeplearning_server/DL_main.py" ]