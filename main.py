import argparse
import sys
import os
from transcribe.summarize_model import save_summaries, split_text, summarize_in_parallel
from transcribe.transcribe import transcribe
from transcribe.get_video import convert_to_wav, process_local_video  # Adjusted import
from transcribe.utils import get_filename

def create_logseq_note(
    summary_path=None, 
    source=None,
    title=None
):
    """
    Takes the bullet point summary and formats it so that it becomes a logseq
    note.
    """
    if not summary_path or not title:
        raise ValueError("Please provide summary_path and title.")

    with open(summary_path, "r") as f:
        lines = f.readlines()

    formatted_lines = ["    " + line for line in lines]

    logseq_note_path = summary_path.replace("files/summaries", "files/logseq")
    os.makedirs(os.path.dirname(logseq_note_path), exist_ok=True)

    with open(logseq_note_path, "w") as f:
        f.write(f"- summarized [[{title}]]")
        f.write("\n- [[summary]]\n")
        f.writelines(formatted_lines)

    print(f"Logseq note saved at {logseq_note_path}")

def call_mlx_model(text_path=None, source=None, title=None):
    filename_only = get_filename(text_path)

    chunks = split_text(text_path=text_path, title=title)
    print(f"Found {len(chunks)} chunks. Summarizing using MLX model...")

    summaries = summarize_in_parallel(chunks)
    summary_path = save_summaries(summaries, filename_only)
    print(f"Summary saved at {summary_path}.")

    return summary_path

def process_local(input_path, title):
    """
    Processes a local video file, transcribes it, splits it into chunks,
    summarizes each chunk, and saves the summaries to a file.

    :input_path: The path of the local video file to be processed.
    :title: The title of the video.
    """
    if not input_path or not title:
        raise ValueError("Please provide input_path and title.")

    print(f"Processing local video file: {input_path}")
    audio_path = process_local_video(input_path)
    print(f"Audio extracted to: {audio_path}")
    print(f"Transcribing {audio_path} (this may take a while)...")
    elapsed_time, transcript_path = transcribe(audio_path)
    print(f"Audio has been transcribed in {int(elapsed_time)} seconds")
    summary_path = call_mlx_model(
        text_path=transcript_path, source=input_path, title=title
    )
    create_logseq_note(
        summary_path=summary_path, 
        source=input_path, 
        title=title
    )
    print("End of job for source: local video")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_path", type=str, help="Path to the local video file", required=True)
    parser.add_argument("--title", type=str, help="Title of the video", required=True)

    args = parser.parse_args()

    input_path = args.input_path
    title = args.title

    process_local(input_path=input_path, title=title)
    sys.exit(0)

