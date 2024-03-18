#!/bin/bash

# 서버 내 .env 파일로 부터 환경변수 정의
echo "---- set environment values ----"
unamestr=$(uname)

if [ $unamestr = "Linux" ]; then
  export $(grep -v '^#' .env | xargs -d '\n')

elif [ $unamestr = "FreeBSD" ] || [ $unamestr = "Darwin" ]; then
  export $(grep -v '^#' .env | xargs -0)
fi

echo "---- OK ----"
echo "---- $1 ----"

if [ $1 = "STAND-ALONE" ]; then
  sudo systemctl stop wip-deep-learning-server-v2
  sudo pip3 install -r /must_be_madness/what_is_pill/wip-deep-learning-server-v2/requirements.txt
  sudo python3 /must_be_madness/what_is_pill/wip-deep-learning-server-v2/get_dl_model.py
  sudo systemctl start wip-deep-learning-server-v2
elif [ $1 = "SINGLE-CONTAINER" ]; then
  # 도커 이미지 빌드
  echo "---- container image build ----"
  build_cmd="docker build . -t wip-deep-learning-server-v2"
  while read line; do
    arg_temp=$(echo $line | cut -f 1 -d'=')
    build_cmd+=" --build-arg $arg_temp=$(eval echo '$'$arg_temp)"
  done < .env

  $(echo $build_cmd)
  echo "---- OK ----"

  # 컨테이너 종료. 실행중인 컨테이너가 있으면 강제로 제거
  echo "---- remove previous container ----"
  docker container rm -f wip-deep-learning-server-v2
  echo "---- OK ----"

  # 컨테이너 실행
  echo "---- run container ----"
  docker run -d --name wip-deep-learning-server-v2 wip-deep-learning-server-v2
  echo "---- OK ----"
fi