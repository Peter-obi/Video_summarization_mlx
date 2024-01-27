import datetime
import os
import subprocess
import sys

from .utils import get_filename, slugify

def process_local_video(video_path, output_path="files/audio/"):
    """
    Processes a local video file and saves the converted audio to the given output
    path. Returns the path to the processed wav file.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    original_path, original_filename = os.path.split(video_path)
    original_file_base, file_ext = os.path.splitext(original_filename)
    slugified_base = slugify(original_file_base)
    new_file_path = os.path.join(
        output_path, f"{slugified_base}.wav"
    )
    convert_to_wav(video_path, new_file_path)
    return new_file_path

def convert_to_wav(movie_path, wav_path):
    """
    Converts an audio file to a wav file. Returns the path to the wav file.
    """
    cmd = (
        f'ffmpeg -y -i "{movie_path}" -ar 16000 -ac 1'
        f' -c:a pcm_s16le "{wav_path}"'
    )
    print("Converting to wav with command: ", cmd)
    return_code = subprocess.call(cmd, shell=True)
    print("ffmpeg return code: ", return_code)
    #if return_code == 0:
        #os.remove(movie_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        wav_path = process_local_video(video_path)
        print("Audio processed to: ", wav_path)
    else:
        print("Usage: python -m gpt_summarize.source_video.py <local_video_path>")
