#!/bin/bash
# $0 is the script name, $1 id the first ARG, $2 is second...
NAME=$1
echo Name: $NAME
ffprobe -show_frames -of compact=p=0 -f lavfi 'movie='${NAME}',select=gt(scene\,.4)' | sed -e 's/.*pkt_dts_time=\([0-9\.]*\).*/\1/'
