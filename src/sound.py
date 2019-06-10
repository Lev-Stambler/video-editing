from pydub import AudioSegment
import moviepy.editor as mp

def convert_clip(path, output_path):
    clip = mp.VideoFileClip(path)
    clip.audio.write_audiofile(output_path)

def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

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
    return (quiet_periods_opener, quiet_periods_closer)

def create_new_clip(clip, quiet_opener, quiet_closer):
    time_start = 100
    new_clip = clip[:time_start]
    time_full_end = len(clip)
    if abs(len(quiet_closer) - len(quiet_opener)) > 1:
        print(len(quiet_closer), len(quiet_opener))
        raise ValueError("Opener and closer must be same or one diff in length")
    for i in range(0, len(quiet_closer)):
        new_clip += clip[time_start:quiet_opener[i]]
        if quiet_closer[i] > time_full_end or quiet_opener[i] > time_full_end:
            break
        sped_up = speed_change(clip[quiet_opener[i]:quiet_closer[i]], speed=2.0)
        new_clip += sped_up
        time_start = quiet_closer[i]
    if time_full_end is not time_start:
        new_clip += clip[time_start:time_full_end]
    return new_clip 

def create_audio_and_quiet_time():
    input_sound = "audiotemp.mp3"
    input_video = "../files/yotubevid1.mp4"
    # convert_clip(input_video, input_sound)
    sound = AudioSegment.from_file("audiotemp.mp3", format="mp3")
    quiet_openers, quiet_closers = get_quiet_time(sound)
    new_clip = create_new_clip(sound, quiet_openers, quiet_closers)
    new_clip.export("sped_up.mp3", format="mp3")

create_audio_and_quiet_time()
