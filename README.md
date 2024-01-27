# Video_summarization_mlx

Repository for summarization of videos using whisper and mlx llm models
### macOS Installation Guide

Below is the installation process for macOS.

#### Setting Up the Environment

```
conda create -n videomlx python=3.11
conda activate videomlx
pip install -r requirements.txt
brew install ffmpeg
python -m spacy download en_core_web_sm
```
#### Some things to take note of

Default model is the mistral 7b 4 bit model. If you want to change it, go to summarize_model.py and change
```
# Load MLX model and tokenizer
model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.2-4bit-mlx")
```
But that means you also have to change the following to match the model you want to use

```
MODEL_MAX_TOKENS = 8192  # Maximum tokens for prompt and response
WINDOW_SIZE = 4096  # Maximum tokens for the input
```
Run the full script using 
```
python main.py --input_path "/path/to/your/video" --title "My Video Title"
```
