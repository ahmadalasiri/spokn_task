import subprocess

def add_corner_radius(input_file, output_file, radius=40):
    ffmpeg_cmd = f"ffmpeg -f lavfi -i color=black:size=1080x1920 -i {input_file} -t 00:01:44 -filter_complex \"[1]format=yuva420p,geq=lum='p(X,Y)':a='if(gt(abs(W/2-X),W/2-{radius})*gt(abs(H/2-Y),H/2-{radius}),if(lte(hypot({radius}-(W/2-abs(W/2-X)),{radius}-(H/2-abs(H/2-Y))),{radius}),255,0),255)'[rounded];[0][rounded]overlay=x=(W-w)/2:y=(H-h)/2\" {output_file}"
    subprocess.call(ffmpeg_cmd, shell=True)

def remove_sound(input_file, output_file, seconds=3):
    ffmpeg_cmd = f"ffmpeg -i {input_file} -af \"volume=enable='lte(t,{seconds})':volume=0\" -c:v copy {output_file} -y"
    subprocess.call(ffmpeg_cmd, shell=True)

def merge_fade_out_fade_in(first_video, second_video, output_file):
    ffmpeg_cmd = f"ffmpeg -i {first_video} -i {second_video} -filter_complex \"[0:v]fade=t=out:st=101:d=3[v1];[1:v]fade=t=in:st=0:d=3[v2];[v1][v2]concat=n=2:v=1:a=0[outv];[0:a][1:a]concat=n=2:v=0:a=1[outa]\" -map \"[outv]\" -map \"[outa]\" {output_file}"
    subprocess.call(ffmpeg_cmd, shell=True)


# 1- regenerate the video using ffmpeg again with a corner radius 4px.
input_file = "audio-1722274616911-7904.mp4"
radius = 40 # 4px
output_corner_radius = "output_corner_radius.mp4"
add_corner_radius(input_file, output_corner_radius, radius)

# 2- using ffmpeg, please remove the sound of the first 3 seconds.
output_no_sound_F3s = "output_no_sound_F3s.mp4"
remove_sound(output_corner_radius, output_no_sound_F3s, 3)

# 3- merge the video again to the same video but with fading out the last 3 seconds of the first video, and fade in the first 3 seconds of the second video.
final_output = "final_output.mp4"
merge_fade_out_fade_in(output_no_sound_F3s, output_corner_radius, final_output)