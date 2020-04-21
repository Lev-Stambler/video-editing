#!/bin/bash

## record 1920 by 1080 with a 30 second framerate
# screen record
(ffmpeg -y -f x11grab -y -r 25 -s 1920x1080 -i :0.0 -qscale 0 files/big_init.mp4)&
(echo HI) &
SCREEN_PID=$!
# webcam record
(streamer -c /dev/video0 -f rgb24 -F stereo -r 24 -t 10:00:00 -o files/big_init.avi)&
WEBCAM_PID=$!

echo "$SCREEN_PID $WEBCAM_PID"
killall() {
  trap '' INT TERM
  echo "**** SHUTTING DOWN ****"
  kill -SIGINT $SCREEN_PID $WEBCAM_PID
  wait
  # kill -TERM 0
# wait
  echo done
}
trap "killall" SIGINT
cat