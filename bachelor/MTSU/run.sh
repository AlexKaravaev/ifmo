#!/bin/bash
echo "--------------BUILDING APP---------------------------"
docker build -t mcu8051ide .

echo "--------------ADDING XHOST SRV---------------------------"
xhost +local:

echo "--------------CREATING VOLUMES---------------------------"
mkdir -p $1

echo "--------------STARTING CONTAINER---------------------------"
docker run --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --volume="$(pwd)/$1:/root/$1" mcu8051ide