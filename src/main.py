import numpy as np
import cv2
from sound import create_audio_and_quiet_time as do_audio 
# import manipulate_video as man_vid
import subprocess
import video

# def overlay_image(l_img, s_img, x_offset, y_offset):
#     y1, y2 = y_offset, y_offset + s_img.shape[0]
#     x1, x2 = x_offset, x_offset + s_img.shape[1]
#     l_img[y1:y2, x1:x2] = s_img[:, :]
#     return l_img

def build_offset(smll_shape, lrg_shape, padding=20):
    # return [x, y]
    return [
        lrg_shape[1] - smll_shape[1] - padding,
        lrg_shape[0] - smll_shape[0] - padding
    ]

def main():
    # TODO: consider mp4 --> avi   mp3 --> wav
    global fps
    fps = 24
    output_path = "../files/output.mp4"
    output_audio = "../files/sped_up.mp3"
    vidFile = "../files/main_init.webm"
    # small_file = '../files/small_init.mp4'
    # large_file = '../files/large_init.mp4'
    
    # man_vid.fix_frame_rate(fps, [large_file]) # TODO nicer implementation ig
    # print(small_file, large_file)
    # set speed_up_f to -1 for cutting out quiet parts TODO implement feature 
    speed_up_f = 3 # has to be an int right now, that should change
    loop_over_time = 100
    quiet_opener, quiet_closer = do_audio(vidFile, output_audio, loop_over_time=loop_over_time, speed_up_f=speed_up_f)
    print(quiet_opener, quiet_closer)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(output_path, fourcc, fps, (1920,1080))
    # cap_smll = cv2.VideoCapture(small_file)
    # cap_lrg = cv2.VideoCapture(large_file)

    cap = cv2.VideoCapture(vidFile)

    video.build_video(cap, out, quiet_opener, quiet_closer, loop_over_time, speed_up_f)
    video.stitch_audio_video(output_path, output_audio, "output_final.mp4".format())

main()

### TODOS Main
# Maybe don't use OpenCV and its big ass (but the potential endless if used)
# Only 1920 x 1080 curr supported
# different video formats mesh weirdly together
# competent print statements
# clean up code
# potentially some tests
