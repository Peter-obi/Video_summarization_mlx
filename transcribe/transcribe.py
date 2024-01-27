import os
import sys
import timeit
import whisper
from whisper import load_models 

def get_filename(file_path):
    return os.path.basename(file_path).split('.')[0]

def transcribe(audio_file, output_path="files/transcripts"):
    """
    Transcribes the given audio file using the Whisper model. Returns a tuple
    containing the transcription result and the elapsed time in seconds.
    """
    filename_only = get_filename(audio_file)

    whisper_model = load_models.load_model("tiny")

    start_time = timeit.default_timer()
    result = whisper.transcribe(audio_file)

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    text_path = os.path.join(output_path, f"{filename_only}.txt")
    with open(text_path, "w") as file:
        file.write(result["text"])

    end_time = timeit.default_timer()
    elapsed_time = int(end_time - start_time)

    return elapsed_time, text_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        elapsed_time, transcript_path = transcribe(audio_path)
        print(f"Audio has been transcribed in {elapsed_time} seconds. Path: {transcript_path}")
    else:
        print("Usage: python whisper_transcribe.py <audio_path>")
