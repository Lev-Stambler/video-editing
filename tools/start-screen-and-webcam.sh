#!/bin/sh

## record 1920 by 1080 with a 30 second framerate
# screen record
(ffmpeg -f x11grab -y -r 30 -s 1920x1080 -i /dev/video0 files/big_init.mpg) &

# webcam record
(ffmpeg -f oss -i /dev/dsp -f video4linux2 -s 1920x1080 -i /dev/video0 files/small_init.mpg) &

