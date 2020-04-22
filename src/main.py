import cv2
from sound import create_audio_and_quiet_time as do_audio 
import video
from configs import constants

def main():
    # TODO: consider mp4 --> avi   mp3 --> wav
    fps = constants.fps
    output_path = "../files/output.mp4"
    output_audio = "../files/sped_up.mp3"
    vidFile = "../files/main_init.mkv"
    
    # set speed_up_f to -1 for cutting out quiet parts TODO implement feature 
    speed_up_f = 3 # has to be an int right now, that should change
    loop_over_time = 100
    quiet_opener, quiet_closer = do_audio(vidFile, output_audio, loop_over_time=loop_over_time, speed_up_f=speed_up_f)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # TODO for now, the output has to be the SAME resolution as the input
    out = cv2.VideoWriter(output_path, fourcc, fps, (1280, 720))
    cap = cv2.VideoCapture(vidFile)

    video.build_video(cap, out, quiet_opener, quiet_closer, loop_over_time, speed_up_f)
    video.stitch_audio_video(output_path, output_audio, "../files/output_final.mp4".format())

main()

### TODOS Main
# Only 1920 x 1080 curr supported
# different video formats mesh weirdly together
# competent print statements
# clean up code
# potentially some tests
