#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#Starting camera-stream and main-web.py.
cd $DIR
trap 'kill %1;' SIGINT
mjpg_streamer -o "output_http.so" -i "input_uvc.so" | tee 1.log | sed -e 's/^/[mjpg_streamer] /' & ./main_web.py | tee 2.log | sed -e 's/^/[main_web] /'