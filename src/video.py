import cv2
import numpy as np
import subprocess
from configs import constants
# TODO fps should be a config
fps=constants.fps

def rescale_frame(frame, factor):
    return cv2.resize(frame, (0, 0), fx=factor, fy=factor, interpolation=cv2.INTER_LINEAR)

def frame_numb_to_milli(frame):
    return int((frame / fps) * 1000.0)

def max_diff_to_time(loop_over_time):
    return (1000 / fps) - (1000 / loop_over_time)

def build_video(cap, out, quiet_opener, quiet_closer, loop_over_time, speed_up_f):
    resize_factor = 0.2
    width = int(cap.get(3))
    height = int(cap.get(4))
    speed_up = False
    frame = 0
    max_difference = max_diff_to_time(loop_over_time)
    print("The time difference between the original video and the output is", max_difference, "seconds")
    # global vars for loop
    wait_frames = 0
    # TODO, why are frames double counted?
    while(cap.isOpened()):
        # TODO framerate stuff
        milli = frame_numb_to_milli(frame)
        # if speed_up is true, then it is currently in a "speed up cycle" (ie a quiet moment)
        if speed_up is False:
            for i, opener in enumerate(quiet_opener):
                if abs(milli - opener) < max_difference:
                    speed_up = True
                    # print("opener", quiet_opener[i])
                    # print("frame", frame)
                    # print("time", milli)
                    quiet_opener = quiet_opener[i+1:]
                    # print("\n")
                    break
        else:
            for i, closer in enumerate(quiet_closer):
                if abs(milli - closer) < max_difference:
                    speed_up = False
                    # print("closer", quiet_closer[i])
                    # print("frame", frame)
                    # print("time", milli)
                    quiet_closer = quiet_closer[i+1:]
                    # print("\n")
                    break
        # get frames and track forward in cap
        ret, img = cap.read()

        if speed_up is True and wait_frames < speed_up_f - 1:
            wait_frames += 1
        else:
            if img is None or ret is not True:
                break
            # resized = rescale_frame(img, resize_factor)
            # lrg_shape = lrg_img.shape
            # smll_shape = resized.shape
            # offset = build_offset(smll_shape, lrg_shape)
            # overlayed = overlay_image(lrg_img, resized, *offset)
            # needs to be converted back to rgb
            out.write(img)
            # cv2.imshow('frame', overlayed)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            wait_frames = 0
        frame += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def stitch_audio_video(video_path, audio_path, full_ouput):
    # TODO ERRORS NOT PRINTED
    cmd = "ffmpeg -y -i {} -i {} -c:v copy -c:a aac -strict experimental {} > /dev/null 2>&1".format(audio_path, video_path, full_ouput)
    subprocess.call(cmd, shell=True)                                     # "Muxing Done
    print('Muxing Done')