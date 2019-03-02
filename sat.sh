#!/bin/bash

if [ -z "$1" ]; then
  echo "please pass the path to your dimacs file!"
  exit 1
fi

s=2
p=''
l=3

while getopts ":S:l:p" opt; do
  case $opt in
    S) s=$OPTARG;;
    p) p=$OPTARG;;
    l) l=$OPTARG;;
    f) l=$OPTARG;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

shift $((OPTIND-1))

MNT=/data
TAG=sat
DIR=$(dirname "$1")
FILE=$(basename "$1")
ID=`docker images -q $TAG`

# navigate to src directory
cd src
# build docker image, use backslashes on Windows
# if [ -z "${ID}" ]; then
  docker build -t $TAG .
# fi
# test script thru docker on local file on our Desktop, mounting to /data, and passing it the file
docker run -v $DIR:$MNT $TAG -S=$s -p=$p -l=$l $MNT/$FILE
