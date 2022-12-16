#!/bin/bash

TPS=$1

LOG=./result.log

function exit_trap() {
  echo -e "\nHTTP CODE"
  cut -f1 ${LOG} | sort | uniq -c | sort -nr

  echo "RESPONSE TIME"
  cut -f2 ${LOG} | awk '{ sum += $1 } END { print sum / NR}'
  exit 0
}

trap exit_trap INT

for((i=0;;i++))
do
  echo -en "\r$i sec"
  for _ in `seq 1 $TPS`
  do
    # curl -o /dev/null -s -w '%{http_code}\t%{time_total}' "${URL}" | awk 1  >> ${LOG} &
    # curl -o /dev/null -s --location --request POST 'http://192.168.219.114:5000/data' \
    # --header 'Content-Type: application/json' \
    # -d @test.json | awk 1 >> ${LOG} &
    curl -o /dev/null -s -w --request POST 'http://192.168.219.114:5000/data' \
    --header 'Content-Type: application/json' \
    -d @test.json | awk 1 >> ${LOG} &
  done
  sleep 1
done