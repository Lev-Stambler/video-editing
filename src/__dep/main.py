import numpy as np
import cv2
from sound import create_audio_and_quiet_time as do_audio 
import manipulate_video as man_vid
import subprocess

fps=24

def overlay_image(l_img, s_img, x_offset, y_offset):
    y1, y2 = y_offset, y_offset + s_img.shape[0]
    x1, x2 = x_offset, x_offset + s_img.shape[1]
    l_img[y1:y2, x1:x2] = s_img[:, :]
    return l_img

def rescale_frame(frame, factor):
    return cv2.resize(frame, (0, 0), fx=factor, fy=factor, interpolation=cv2.INTER_LINEAR)


def build_offset(smll_shape, lrg_shape, padding=20):
    # return [x, y]
    return [
        lrg_shape[1] - smll_shape[1] - padding,
        lrg_shape[0] - smll_shape[0] - padding
    ]

def frame_numb_to_milli(frame):
    return int((frame / fps) * 1000.0)

def max_diff_to_time(loop_over_time):
    return (1000 / fps) - (1000 / loop_over_time)

def build_video(cap_smll, cap_lrg, out, quiet_opener, quiet_closer, loop_over_time, speed_up_f):
    resize_factor = 0.2
    smll_width = int(cap_smll.get(3) * resize_factor)
    smll_height = int(cap_smll.get(4) * resize_factor)
    lrg_width = int(cap_lrg.get(3))
    lrg_height = int(cap_lrg.get(4))
    speed_up = False
    frame = 0
    max_difference = max_diff_to_time(loop_over_time)
    print("Max difference is:", max_difference)
    # global vars for loop
    wait_frames = 0
    # TODO, why are frames double counted?
    while(cap_smll.isOpened() and cap_lrg.isOpened()):
        # TODO framerate stuff
        milli = frame_numb_to_milli(frame)
        if speed_up is False:
            for i, opener in enumerate(quiet_opener):
                if abs(milli - opener) < max_difference:
                    speed_up = True
                    print("opener", quiet_opener[i])
                    print("frame", frame)
                    print("time", milli)
                    quiet_opener = quiet_opener[i+1:]
                    print("\n")
                    break
        else:
            for i, closer in enumerate(quiet_closer):
                if abs(milli - closer) < max_difference:
                    speed_up = False
                    print("closer", quiet_closer[i])
                    print("frame", frame)
                    print("time", milli)
                    quiet_closer = quiet_closer[i+1:]
                    print("\n")
                    break
        # get frames and track forward in cap
        ret, smll_img = cap_smll.read()
        ret, lrg_img = cap_lrg.read()

        if speed_up is True and wait_frames < speed_up_f - 1:
            wait_frames += 1
        else:
            if lrg_img is None or smll_img is None or ret is not True:
                break
            resized = rescale_frame(smll_img, resize_factor)
            lrg_shape = lrg_img.shape
            smll_shape = resized.shape
            offset = build_offset(smll_shape, lrg_shape)
            overlayed = overlay_image(lrg_img, resized, *offset)
            # needs to be converted back to rgb
            out.write(overlayed)
            # cv2.imshow('frame', overlayed)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            wait_frames = 0
        frame += 1

    print(frame_numb_to_milli(frame), frame)
    cap_smll.release()
    cap_lrg.release()
    out.release()
    cv2.destroyAllWindows()

def stitch_audio_video(video_path, audio_path, full_ouput):
    cmd = "ffmpeg -y -i {} -i {} -c:v copy -c:a aac -strict experimental {}".format(audio_path, video_path, full_ouput)
    subprocess.call(cmd, shell=True)                                     # "Muxing Done
    print('Muxing Done')

def main():
    # TODO: consider mp4 --> avi   mp3 --> wav
    global fps
    fps = 24
    output_path = "output.mp4"
    output_audio = "sped_up.mp3"
    small_file = '../files/small_init.mp4'
    large_file = '../files/large_init.mp4'
    
    # man_vid.fix_frame_rate(fps, [large_file]) # TODO nicer implementation ig
    # print(small_file, large_file)
    # set speed_up_f to -1 for cutting out quiet parts TODO implement feature 
    speed_up_f = 3 # has to be an int right now, that should change
    loop_over_time = 100
    quiet_opener, quiet_closer = do_audio(small_file, output_audio, loop_over_time=loop_over_time, speed_up_f=speed_up_f)
    print(quiet_opener, quiet_closer)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(output_path, fourcc, fps, (1920,1080))
    cap_smll = cv2.VideoCapture(small_file)
    cap_lrg = cv2.VideoCapture(large_file)
    build_video(cap_smll, cap_lrg, out, quiet_opener, quiet_closer, loop_over_time, speed_up_f)
    stitch_audio_video(output_path, output_audio, "output_final.mp4".format())

main()

### TODOS Main
# Maybe don't use OpenCV and its big ass (but the potential endless if used)
# Only 1920 x 1080 curr supported
# different video formats mesh weirdly together
# competent print statements
# clean up code
# potentially some tests
