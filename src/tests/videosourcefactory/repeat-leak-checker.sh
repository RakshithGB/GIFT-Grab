#!/usr/bin/env bash

ulimit -c unlimited

device=$1
colour=$2
num_reps=$3
for i in `seq 1 $num_reps`; do
    printf "${i}. run: "
    ./tests/videosourcefactory/video_source_factory_leak_checker $device $colour
    sleep 5
done

ulimit -c 0
