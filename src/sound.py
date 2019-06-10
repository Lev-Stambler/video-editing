from pydub import AudioSegment
import moviepy.editor as mp

def convert_clip(path, output_path):
    clip = mp.VideoFileClip(path)
    clip.audio.write_audiofile(output_path)

def get_quiet_time(sound):
    peak_amplitude = sound.max
    # split sound in 0.1-second slices and export
    quiet_period = False
    quiet_periods_opener = []
    quiet_periods_closer = []
    loop_over_time = 100 # milliseconds
    min_quiet_time = 1000
    turning_point = 300 # audio level
    for i, chunk in enumerate(sound[::loop_over_time]):
        curr_max = chunk.max 
        if curr_max < turning_point and quiet_period is False:
            quiet_periods_opener.append(i * loop_over_time)
            quiet_period = True
        elif quiet_period is True and curr_max >= turning_point:
            quiet_period = False
            if i * loop_over_time - quiet_periods_opener[-1] > min_quiet_time:
                quiet_periods_closer.append(i * loop_over_time)
            else:
                quiet_periods_opener.pop()
    print(quiet_periods_opener, quiet_periods_closer)

def get_amplitude():
    input_sound = "audiotemp.mp3"
    input_video = "../files/yotubevid1.mp4"
    # convert_clip(input_video, input_sound)
    sound = AudioSegment.from_file("audiotemp.mp3", format="mp3")
    get_quiet_time(sound)

get_amplitude()
