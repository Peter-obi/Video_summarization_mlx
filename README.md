# Transcribe and summarize youtube video using mlx 
### macOS Installation Guide

Below is the installation process for macOS. 

#### Setting Up the Environment

```
conda create -n VoiceAI python=3.11
conda activate VoiceAI
pip install -r requirements.txt
brew install ffmpeg
```
The default model is Mistral7b-4bit-mlx. If you want to change it, go to summarize_model.py and change this
```
# Load MLX model and tokenizer
model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.2-4bit-mlx")
```
But that means you also have to adjust this as appropriate 
```
MODEL_MAX_TOKENS = 8192  # Maximum tokens for prompt and response
WINDOW_SIZE = 4096  # Maximum tokens for the input
```
Run the whole workflow using
```
python main.py --input_path "/path/to/your/video" --title "My Video Title"
```
Remember the longer the longer the video, the more time it might take to summarize. If you have any suggested changes, submit a pull request and we can adjust as appropriate.
