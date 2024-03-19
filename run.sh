#!/bin/bash
echo "---- Set environment values ----"
unamestr=$(uname)

if [ $unamestr = "Linux" ]; then
  export $(grep -v '^#' .env | xargs -d '\n')

elif [ $unamestr = "FreeBSD" ] || [ $unamestr = "Darwin" ]; then
  export $(grep -v '^#' .env | xargs -0)
fi

echo "---- OK ----"
echo "---- $1 ----"

if [ $1 = "STAND-ALONE" ]; then
  echo "---- Stop wip-deep-learning-server-v2 ----"
  sudo systemctl stop wip-deep-learning-server-v2
  echo "---- OK ----"

  echo "---- Update require library ----"
  sudo pip3 install --upgrade --ignore-installed -r /must_be_madness/what_is_pill/wip-deep-learning-server-v2/requirements.txt
  sudo python3 /must_be_madness/what_is_pill/wip-deep-learning-server-v2/get_dl_model.py
  echo "---- OK ----"

  echo "---- Start wip-deep-learning-server-v2 ----"
  sudo systemctl start wip-deep-learning-server-v2
  echo "---- OK ----"
elif [ $1 = "SINGLE-CONTAINER" ]; then
  echo "---- Build container image ----"
  build_cmd="docker build --no-cache . -t wip-deep-learning-server-v2"

  while read line; do
    arg_temp=$(echo $line | cut -f 1 -d'=')
    build_cmd+=" --build-arg $arg_temp=$(eval echo '$'$arg_temp)"
  done < .env

  $(echo $build_cmd)
  echo "---- OK ----"

  echo "---- Remove previous container ----"
  docker container rm -f wip-deep-learning-server-v2
  echo "---- OK ----"

  echo "---- Run container ----"
  docker run -d --name wip-deep-learning-server-v2 wip-deep-learning-server-v2
  echo "---- OK ----"

  echo "---- Remove previous image ----"
  docker image prune -f
  echo "---- OK ----"
fi