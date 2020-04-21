import subprocess

# has side effect on input arr (purpusful)
# this shit takes forever
# TODO make procs go parrallel
# TODO, do nothing if fps is already correct (I think openCV got smthng for that)
def fix_frame_rate(fps, inputs):
    output_paths = []
    for i, input_f in enumerate(inputs):
        splitPer = input_f.split('.')
        command = 'ffmpeg -i {} -r {} -y {}_fixed.{}'.format(input_f, fps, input_f, splitPer[-1])
        subprocess.call(command, shell=True)
        inputs[i] = "{}_fixed.{}".format(input_f, splitPer[-1])
