#!/bin/bash

input_video=$1
alignment_file=$2

python src/detect_video.py ${input_video} -m v --alignment_file ${alignment_file}