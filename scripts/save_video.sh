#!/bin/bash

input_video=$1
save_path=$2
alignment_file=$3

python src/detect_video.py ${input_video} -m s -o ${save_path} --alignment_file ${alignment_file}